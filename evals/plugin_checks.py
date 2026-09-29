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
    for filename in ["plugin.json", "gemini-extension.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".agents/plugins.json"]:
        checks += 1
        try:
            manifest = json.loads((repository / filename).read_text(encoding="utf-8-sig"))
            if filename == ".codex-plugin/plugin.json" and not (repository / manifest["skills"]).is_dir():
                findings.append("Codex skills path does not exist")
            if filename == ".agents/plugins.json":
                declared = {(repository / item).resolve() for item in manifest["skills"]}
                actual = {path.parent.resolve() for path in skills}
                if declared != actual:
                    findings.append("Declared skill directories differ from catalog inventory")
        except (OSError, ValueError, KeyError, TypeError) as error:
            findings.append(f"{filename}: {error}")
    return {"passed": not findings, "checks": checks, "skills": len(skills), "findings": findings,
            "scope": "Local packaging and references only; no runtime installation claims"}
