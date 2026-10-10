"""Assemble project plugins and the shared startup foundation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / ".agents" / "plugins" / "agent-skills"
HERMES_DEST = ROOT / ".hermes" / "plugins" / "agent-skills"
BEGIN = "<!-- agent-skills:file-management:begin -->"
END = "<!-- agent-skills:file-management:end -->"
CORE = ROOT / "skills" / "manage-file-operations" / "core.md"
TESSL_RULE = ROOT / "rules" / "file-management.md"
VOICE_RULE = ROOT / "rules" / "writing-voice.md"
VOICE_BEGIN = "<!-- agent-skills:writing-voice:begin -->"
VOICE_END = "<!-- agent-skills:writing-voice:end -->"


def canonical_hash_content(content: bytes) -> bytes:
    """Make generated source hashes independent of platform line endings."""
    return content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def startup_text() -> str:
    core = CORE.read_text(encoding="utf-8").strip()
    voice = VOICE_RULE.read_text(encoding="utf-8").strip()
    return f"{BEGIN}\n{core}\n{END}\n\n{VOICE_BEGIN}\n{voice}\n{VOICE_END}"


def anchored_agents() -> str:
    original = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for begin, end, source in ((BEGIN, END, CORE), (VOICE_BEGIN, VOICE_END, VOICE_RULE)):
        block = f"{begin}\n{source.read_text(encoding='utf-8').strip()}\n{end}"
        if begin in original or end in original:
            if original.count(begin) != 1 or original.count(end) != 1 or original.index(begin) > original.index(end):
                raise ValueError("AGENTS.md has an invalid managed foundation block")
            start = original.index(begin)
            stop = original.index(end) + len(end)
            original = original[:start] + block + original[stop:]
        else:
            original = original.rstrip() + "\n\n" + block + "\n"
    return original


def skill_files() -> dict[str, bytes]:
    output = {}
    for source in sorted((ROOT / "skills").rglob("*")):
        if not source.is_file() or any(part in ("__pycache__", ".nyssa-ai", ".temp")
                                       for part in source.relative_to(ROOT).parts):
            continue
        output[source.relative_to(ROOT).as_posix()] = source.read_bytes()
    return output


def source_hash(files: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name in sorted(files):
        content = canonical_hash_content(files[name])
        digest.update(name.encode() + b"\0" + content + b"\0")
    return digest.hexdigest()


def expected_files() -> dict[str, bytes]:
    identity = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    manifest = {
        "$schema": "https://antigravity.google/schemas/v1/plugin.json",
        "name": identity["name"],
        "description": identity["description"],
    }
    output = {"plugin.json": (json.dumps(manifest, indent=2) + "\n").encode()}
    rule_header = (
        "---\n"
        "trigger: always_on\n"
        "description: Core file-management naming and safety rules.\n"
        "---\n\n"
    ).encode()
    output["rules/file-management.md"] = rule_header + CORE.read_bytes().rstrip() + b"\n"
    output["rules/writing-voice.md"] = (
        b"---\ntrigger: always_on\ndescription: Apply the user's project writing voice.\n---\n\n"
        + VOICE_RULE.read_bytes().rstrip() + b"\n"
    )
    output.update(skill_files())
    output["assembly.json"] = (
        json.dumps({
            "format": "antigravity-plugin",
            "source": "scripts/assemble.py",
            "source_sha256": source_hash(output),
            "version": identity["version"],
        }, indent=2) + "\n"
    ).encode()
    return output


def hermes_expected_files() -> dict[str, bytes]:
    identity = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    manifest = (
        f"name: {json.dumps(identity['name'])}\n"
        f"version: {json.dumps(identity['version'])}\n"
        f"description: {json.dumps(identity['description'])}\n"
    )
    output = {
        "plugin.yaml": manifest.encode("utf-8"),
        "__init__.py": (ROOT / "adapters" / "hermes" / "plugin.py").read_bytes(),
        "rules/writing-voice.md": VOICE_RULE.read_bytes(),
    }
    output.update(skill_files())
    output["assembly.json"] = (
        json.dumps({
            "format": "hermes-plugin",
            "source": "scripts/assemble.py",
            "source_sha256": source_hash(output),
            "version": identity["version"],
        }, indent=2) + "\n"
    ).encode()
    return output


def current_files(destination: Path = DEST) -> dict[str, bytes]:
    if not destination.exists():
        return {}
    return {p.relative_to(destination).as_posix(): p.read_bytes()
            for p in destination.rglob("*") if p.is_file()}


def ensure_owned_destination(destination: Path, package_format: str) -> None:
    if destination.is_symlink() or not destination.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError(f"Unsafe package destination: {destination}")
    if destination.exists():
        marker = destination / "assembly.json"
        if not marker.is_file() or json.loads(marker.read_text(encoding="utf-8")).get("format") != package_format:
            raise ValueError(f"Refusing to replace unowned destination: {destination}")


def write_package(destination: Path, package: dict[str, bytes]) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for name, content in package.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("write", "check"))
    args = parser.parse_args()
    target_agents = anchored_agents()
    target_rule = CORE.read_text(encoding="utf-8").strip() + "\n"
    package = expected_files()
    hermes_package = hermes_expected_files()
    if args.mode == "check":
        errors = []
        if (ROOT / "AGENTS.md").read_text(encoding="utf-8") != target_agents:
            errors.append("AGENTS.md foundation differs from canonical core")
        if not TESSL_RULE.is_file() or TESSL_RULE.read_text(encoding="utf-8") != target_rule:
            errors.append("Tessl foundation rule differs from canonical core")
        for label, destination, expected in (
            ("Antigravity", DEST, package), ("Hermes", HERMES_DEST, hermes_package)
        ):
            current = current_files(destination)
            if current != expected:
                missing = sorted(expected.keys() - current.keys())
                extra = sorted(current.keys() - expected.keys())
                changed = sorted(name for name in expected.keys() & current.keys()
                                 if expected[name] != current[name])
                errors.append(f"{label} artifact differs: missing={missing}, extra={extra}, changed={changed}")
        for error in errors:
            print(error, file=sys.stderr)
        if not errors:
            print(f"Startup, Tessl rule, {len(package)} Antigravity files, and {len(hermes_package)} Hermes files match canonical source")
        return bool(errors)
    ensure_owned_destination(DEST, "antigravity-plugin")
    ensure_owned_destination(HERMES_DEST, "hermes-plugin")
    if not TESSL_RULE.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError(f"Unsafe rule destination: {TESSL_RULE}")
    write_package(DEST, package)
    write_package(HERMES_DEST, hermes_package)
    (ROOT / "AGENTS.md").write_text(target_agents, encoding="utf-8")
    TESSL_RULE.parent.mkdir(parents=True, exist_ok=True)
    TESSL_RULE.write_text(target_rule, encoding="utf-8")
    print(f"Wrote startup foundation, Tessl rule, {len(package)} Antigravity files, and {len(hermes_package)} Hermes files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
