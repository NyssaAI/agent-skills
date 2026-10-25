"""Plugin checks — validate skill packaging, frontmatter, and local reference reachability.
validate_plugin(repository)
"""

import json
from pathlib import Path
import re

import yaml


def validate_plugin(repository):
    """Check the local catalog contract without claiming runtime installation compatibility."""
    findings = []
    checks = 0
    skills = sorted((repository / "skills").glob("*/SKILL.md"))
    required_voice_skills = {"maintain-writing-voice", "write-in-user-voice"}
    checks += 1
    missing_voice_skills = required_voice_skills - {path.parent.name for path in skills}
    if missing_voice_skills:
        findings.append(f"Missing writing voice skills: {sorted(missing_voice_skills)}")
    if not skills:
        findings.append("No skill entrypoints found")
    for path in skills:
        checks += 1
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            findings.append(f"{path.relative_to(repository)}: BOM prevents strict frontmatter discovery")
        content = raw.decode("utf-8-sig")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---", content, re.S)
        if not match:
            findings.append(f"{path.relative_to(repository)}: missing frontmatter")
            continue
        try:
            metadata = yaml.safe_load(match.group(1))
            if not isinstance(metadata, dict) or metadata.get("name") != path.parent.name:
                findings.append(f"{path.relative_to(repository)}: name does not match folder")
            description = metadata.get("description", "") if isinstance(metadata, dict) else ""
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                findings.append(f"{path.relative_to(repository)}: invalid description")
        except yaml.YAMLError as error:
            findings.append(f"{path.relative_to(repository)}: {error}")
    for path in (repository / "skills").rglob("*.md"):
        content = path.read_text(encoding="utf-8-sig")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if "://" in target:
                continue
            checks += 1
            filename, _, anchor = target.partition("#")
            if Path(filename).is_absolute() or ":" in filename:
                findings.append(f"{path.relative_to(repository)}: non-relative internal link {target}")
                continue
            destination = (path.parent / filename).resolve() if filename else path
            try:
                destination.relative_to(repository.resolve())
            except ValueError:
                findings.append(f"{path.relative_to(repository)}: link escapes catalog {target}")
                continue
            if not destination.exists():
                findings.append(f"{path.relative_to(repository)}: missing target {target}")
            elif anchor and destination.is_file():
                headings = re.findall(r"^#{1,6}\s+(.+)$", destination.read_text(encoding="utf-8-sig"), re.M)
                anchors = {re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-") for heading in headings}
                if anchor not in anchors:
                    findings.append(f"{path.relative_to(repository)}: missing anchor {target}")
    for path in (repository / "skills").rglob("*.yaml"):
        checks += 1
        try:
            yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        except yaml.YAMLError as error:
            findings.append(f"{path.relative_to(repository)}: {error}")
    root_identity = None
    for filename in ["plugin.json", "gemini-extension.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json", ".agents/plugins.json"]:
        checks += 1
        try:
            manifest = json.loads((repository / filename).read_text(encoding="utf-8-sig"))
            if not isinstance(manifest, dict):
                raise ValueError("manifest root must be an object")
            if filename == "plugin.json":
                root_identity = manifest
            elif root_identity is not None:
                for field in ("name", "version"):
                    if manifest.get(field) != root_identity.get(field):
                        findings.append(f"{filename} {field} differs from root plugin.json")
                if filename != ".agents/plugins.json" and manifest.get("description") != root_identity.get("description"):
                    findings.append(f"{filename} description differs from root plugin.json")
            if filename == ".codex-plugin/plugin.json" and not (repository / manifest["skills"]).is_dir():
                findings.append("Codex skills path does not exist")
            if filename == ".agents/plugins.json":
                declared = {(repository / item).resolve() for item in manifest["skills"]}
                actual = {path.parent.resolve() for path in skills}
                if declared != actual:
                    findings.append("Declared skill directories differ from catalog inventory")
            if filename in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json") and root_identity is not None:
                for field in ("author", "license"):
                    if manifest.get(field) != root_identity.get(field):
                        findings.append(f"{filename} {field} differs from root plugin.json")
        except (OSError, ValueError, KeyError, TypeError) as error:
            findings.append(f"{filename}: {error}")
    checks += 1
    try:
        hermes = yaml.safe_load((repository / ".hermes/plugins/agent-skills/plugin.yaml").read_text(encoding="utf-8"))
        for field in ("name", "version", "description"):
            if hermes.get(field) != root_identity.get(field):
                findings.append(f"Hermes plugin {field} differs from root plugin.json")
    except (OSError, AttributeError, yaml.YAMLError) as error:
        findings.append(f"Hermes plugin manifest: {error}")
    rule = repository / ".agents/plugins/agent-skills/rules/file-management.md"
    checks += 1
    try:
        content = rule.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
        metadata = yaml.safe_load(match.group(1)) if match else None
        if not isinstance(metadata, dict) or metadata.get("trigger") != "always_on":
            findings.append("Antigravity foundation rule lacks an always_on trigger")
        body = content[match.end():].strip() if match else ""
        core = (repository / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
        if body != core:
            findings.append("Antigravity foundation rule differs from canonical core")
    except (OSError, yaml.YAMLError) as error:
        findings.append(f"Antigravity foundation rule: {error}")
    for package in (".agents/plugins/agent-skills", ".hermes/plugins/agent-skills"):
        checks += 1
        declared = {path.parent.name for path in (repository / package / "skills").glob("*/SKILL.md")}
        if declared != {path.parent.name for path in skills}:
            findings.append(f"{package}: packaged skill inventory differs from catalog")
        checks += 1
        try:
            source = (repository / "rules/writing-voice.md").read_text(encoding="utf-8").strip()
            content = (repository / package / "rules/writing-voice.md").read_text(encoding="utf-8")
            if package.startswith(".agents/"):
                match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
                metadata = yaml.safe_load(match.group(1)) if match else None
                if not isinstance(metadata, dict) or metadata.get("trigger") != "always_on":
                    findings.append("Antigravity writing voice rule lacks an always_on trigger")
                content = content[match.end():] if match else ""
            if content.strip() != source:
                findings.append(f"{package}: writing voice rule differs from canonical source")
        except (OSError, yaml.YAMLError) as error:
            findings.append(f"{package}: writing voice rule: {error}")
    for directory in ("skills", "rules", ".agents/plugins/agent-skills", ".hermes/plugins/agent-skills"):
        for path in (repository / directory).rglob("*"):
            if path.is_file():
                checks += 1
                parts = path.relative_to(repository / directory).parts
                if any(part in (".nyssa-ai", ".temp") for part in parts):
                    findings.append(f"{path.relative_to(repository)}: private configuration or scratch in package source")
    checks += 1
    try:
        hooks = json.loads((repository / "hooks/hooks.json").read_text(encoding="utf-8"))
        handlers = hooks["hooks"]["SessionStart"][0]["hooks"]
        if not any(handler.get("type") == "command" and
                   "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.py" in handler.get("command", "")
                   for handler in handlers):
            findings.append("Codex/Claude startup hook is not registered")
        if not (repository / "hooks/session-start.py").is_file():
            findings.append("Codex/Claude startup hook script is missing")
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        findings.append(f"Codex/Claude startup hook: {error}")
    return {"passed": not findings, "checks": checks, "skills": len(skills), "findings": findings,
            "scope": "Local packaging and references only; no runtime installation claims"}
