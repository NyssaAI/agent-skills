"""Plugin checks — validate skill packaging, frontmatter, harness-adapters, and local reference reachability.
validate_plugin(repository)
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re

import yaml


FORBIDDEN_REPO_TREES = (".agents", ".hermes", "artifacts", "adapters")
EXCLUDED_PACKAGE_PARTS = (".nyssa-ai", ".nyssaai", ".nyssa", ".temp")


def _load_assemble_module(repository: Path):
    script = repository / "scripts" / "assemble.py"
    if not script.is_file():
        return None
    spec = importlib.util.spec_from_file_location("agent_skills_assemble", script)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_plugin(repository: Path) -> dict:
    """Check the local catalog contract without claiming runtime installation compatibility."""
    findings: list[str] = []
    checks = 0

    for forbidden in FORBIDDEN_REPO_TREES:
        checks += 1
        if (repository / forbidden).exists():
            findings.append(f"Forbidden tree in repo_root: {forbidden}/")

    checks += 1
    if not (repository / "docs" / "GLOSSARY.md").is_file():
        findings.append("Missing authoritative Ubiquitous Language glossary: docs/GLOSSARY.md")

    skills = sorted((repository / "skills").glob("*/SKILL.md"))
    skill_names = {path.parent.name for path in skills}
    checks += 1
    expected_skills = {"manage-file-operations", "para-vault", "write-like-me"}
    if not expected_skills.issubset(skill_names):
        missing = sorted(expected_skills - skill_names)
        findings.append(f"Missing canonical skills: {missing}")
    if not skills:
        findings.append("No skill entrypoints found")

    for path in skills:
        checks += 1
        if (path.parent / "agents").exists():
            findings.append(
                f"{path.parent.relative_to(repository)}/agents: Codex UI metadata belongs under harness-adapters/codex/"
            )
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

    for yaml_root in ("skills", "harness-adapters"):
        base = repository / yaml_root
        if not base.exists():
            continue
        for path in base.rglob("*.yaml"):
            checks += 1
            try:
                yaml.safe_load(path.read_text(encoding="utf-8-sig"))
            except yaml.YAMLError as error:
                findings.append(f"{path.relative_to(repository)}: {error}")

    checks += 1
    if not (repository / "harness-adapters" / "hermes" / "plugin.py").is_file():
        findings.append("Missing Hermes harness-adapter: harness-adapters/hermes/plugin.py")

    for skill_name in sorted(skill_names):
        checks += 1
        codex_yaml = repository / "harness-adapters" / "codex" / skill_name / "openai.yaml"
        if not codex_yaml.is_file():
            findings.append(f"Missing Codex UI harness-adapter metadata: {codex_yaml.relative_to(repository)}")

    root_identity = None
    manifest_files = [
        "plugin.json",
        "gemini-extension.json",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        ".cursor-plugin/plugin.json",
        ".tessl-plugin/plugin.json",
    ]
    for filename in manifest_files:
        checks += 1
        try:
            manifest = json.loads((repository / filename).read_text(encoding="utf-8-sig"))
            if not isinstance(manifest, dict):
                raise ValueError("manifest root must be an object")
            if filename == "plugin.json":
                root_identity = manifest
            elif root_identity is not None:
                expected_name = (
                    f"nyssa-ai/{root_identity.get('name')}"
                    if filename == ".tessl-plugin/plugin.json"
                    else root_identity.get("name")
                )
                if manifest.get("name") != expected_name:
                    findings.append(f"{filename} name differs from root plugin.json")
                if manifest.get("version") != root_identity.get("version"):
                    findings.append(f"{filename} version differs from root plugin.json")
                if filename != ".tessl-plugin/plugin.json" and manifest.get("description") != root_identity.get("description"):
                    findings.append(f"{filename} description differs from root plugin.json")
            if filename == ".codex-plugin/plugin.json" and not (repository / manifest["skills"]).is_dir():
                findings.append("Codex skills path does not exist")
            if filename == ".tessl-plugin/plugin.json":
                if not (repository / manifest["skills"]).is_dir():
                    findings.append("Tessl skills path does not exist")
                if not (repository / manifest["rules"]).is_dir():
                    findings.append("Tessl rules path does not exist")
            if filename in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json") and root_identity is not None:
                for field in ("author", "license"):
                    if manifest.get(field) != root_identity.get(field):
                        findings.append(f"{filename} {field} differs from root plugin.json")
        except (OSError, ValueError, KeyError, TypeError) as error:
            findings.append(f"{filename}: {error}")

    checks += 1
    try:
        core = (repository / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
        tessl_rule = (repository / "rules/file-management.md").read_text(encoding="utf-8").strip()
        if tessl_rule != core:
            findings.append("rules/file-management.md differs from canonical core.md")
    except OSError as error:
        findings.append(f"rules/file-management.md: {error}")

    assemble_mod = _load_assemble_module(repository)
    checks += 1
    if assemble_mod is None:
        findings.append("Missing scripts/assemble.py")
    else:
        packages = assemble_mod.build_packages()
        portable_pkg = packages["portable"][1]
        antigravity_pkg = packages["antigravity"][1]
        hermes_pkg = packages["hermes"][1]

        checks += 1
        try:
            hermes = yaml.safe_load(hermes_pkg["plugin.yaml"].decode("utf-8"))
            if root_identity is not None:
                for field in ("name", "version", "description"):
                    if hermes.get(field) != root_identity.get(field):
                        findings.append(f"Hermes bundle {field} differs from root plugin.json")
        except (KeyError, AttributeError, yaml.YAMLError) as error:
            findings.append(f"Hermes bundle manifest: {error}")

        checks += 1
        try:
            content = antigravity_pkg["rules/file-management.md"].decode("utf-8")
            match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
            metadata = yaml.safe_load(match.group(1)) if match else None
            if not isinstance(metadata, dict) or metadata.get("trigger") != "always_on":
                findings.append("Antigravity foundation rule lacks an always_on trigger")
            body = content[match.end():].strip() if match else ""
            core = (repository / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
            if body != core:
                findings.append("Antigravity foundation rule differs from canonical core")
        except (KeyError, OSError, yaml.YAMLError) as error:
            findings.append(f"Antigravity foundation rule: {error}")

        for bundle_name, pkg_files in (("portable", portable_pkg), ("antigravity", antigravity_pkg), ("hermes", hermes_pkg)):
            checks += 1
            declared = {
                Path(rel).parts[1]
                for rel in pkg_files
                if rel.startswith("skills/") and Path(rel).name == "SKILL.md" and len(Path(rel).parts) == 3
            }
            if declared != skill_names:
                findings.append(f"{bundle_name}: packaged skill inventory differs from catalog")
            checks += 1
            try:
                source = (repository / "rules/writing-voice.md").read_text(encoding="utf-8").strip()
                content = pkg_files["rules/writing-voice.md"].decode("utf-8")
                if bundle_name == "antigravity":
                    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
                    metadata = yaml.safe_load(match.group(1)) if match else None
                    if not isinstance(metadata, dict) or metadata.get("trigger") != "always_on":
                        findings.append("Antigravity writing voice rule lacks an always_on trigger")
                    content = content[match.end():] if match else ""
                if content.strip() != source:
                    findings.append(f"{bundle_name}: writing voice rule differs from canonical source")
            except (KeyError, OSError, yaml.YAMLError) as error:
                findings.append(f"{bundle_name}: writing voice rule: {error}")

        checks += 1
        expected_codex_projections = {f"skills/{name}/agents/openai.yaml" for name in skill_names}
        if not expected_codex_projections.issubset(portable_pkg.keys()):
            findings.append("portable: missing Codex openai.yaml projections")

    for directory in ("skills", "rules", "harness-adapters"):
        base = repository / directory
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                checks += 1
                parts = path.relative_to(base).parts
                if any(part in EXCLUDED_PACKAGE_PARTS for part in parts):
                    findings.append(f"{path.relative_to(repository)}: private configuration or scratch in package source")

    checks += 1
    try:
        hooks = json.loads((repository / "hooks/hooks.json").read_text(encoding="utf-8"))
        handlers = hooks["hooks"]["SessionStart"][0]["hooks"]
        if not any(
            handler.get("type") == "command"
            and "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.py" in handler.get("command", "")
            for handler in handlers
        ):
            findings.append("Codex/Claude startup hook is not registered")
        hook_script = repository / "hooks/session-start.py"
        if not hook_script.is_file():
            findings.append("Codex/Claude startup hook script is missing")
        else:
            hook_source = hook_script.read_text(encoding="utf-8")
            if ".nyssaai" in hook_source or '".nyssa"' in hook_source or "'.nyssa'" in hook_source:
                findings.append("hooks/session-start.py still references retired .nyssaai/.nyssa config directories")
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        findings.append(f"Codex/Claude startup hook: {error}")

    return {
        "passed": not findings,
        "checks": checks,
        "skills": len(skills),
        "findings": findings,
        "scope": "Local packaging, harness-adapters, and references only; no runtime installation claims",
    }
