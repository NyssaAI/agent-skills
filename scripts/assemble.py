"""Assemble the project Antigravity plugin and shared startup foundation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / ".agents" / "plugins" / "agent-skills"
BEGIN = "<!-- agent-skills:file-management:begin -->"
END = "<!-- agent-skills:file-management:end -->"
CORE = ROOT / "skills" / "file-management" / "core.md"


def canonical_hash_content(content: bytes) -> bytes:
    """Make generated source hashes independent of platform line endings."""
    return content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def startup_text() -> str:
    core = CORE.read_text(encoding="utf-8").strip()
    return f"{BEGIN}\n{core}\n{END}"


def anchored_agents() -> str:
    original = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    block = startup_text()
    if BEGIN in original or END in original:
        if original.count(BEGIN) != 1 or original.count(END) != 1:
            raise ValueError("AGENTS.md has an invalid managed foundation block")
        start = original.index(BEGIN)
        stop = original.index(END) + len(END)
        return original[:start] + block + original[stop:]
    return original.rstrip() + "\n\n" + block + "\n"


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
    for source in sorted((ROOT / "skills").rglob("*")):
        if not source.is_file() or "__pycache__" in source.parts:
            continue
        relative = source.relative_to(ROOT).as_posix()
        output[relative] = source.read_bytes()
    # These are native Antigravity agent registrations generated from the same
    # maintained definitions that the Claude manifest names.
    for name in ("adversary", "eval"):
        output[f"agents/{name}.md"] = (
            ROOT / "skills" / "plugin-builder" / "agents" / f"{name}.md"
        ).read_bytes()
    source_hash = hashlib.sha256()
    for name in sorted(output):
        # Git may check out text files with CRLF on Windows and LF elsewhere.
        # Normalize line endings so the generated provenance hash is portable.
        content = canonical_hash_content(output[name])
        source_hash.update(name.encode() + b"\0" + content + b"\0")
    output["assembly.json"] = (
        json.dumps({
            "format": "antigravity-plugin",
            "source": "scripts/assemble.py",
            "source_sha256": source_hash.hexdigest(),
            "version": identity["version"],
        }, indent=2) + "\n"
    ).encode()
    return output


def current_files() -> dict[str, bytes]:
    if not DEST.exists():
        return {}
    return {p.relative_to(DEST).as_posix(): p.read_bytes()
            for p in DEST.rglob("*") if p.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("write", "check"))
    args = parser.parse_args()
    target_agents = anchored_agents()
    package = expected_files()
    if args.mode == "check":
        errors = []
        if (ROOT / "AGENTS.md").read_text(encoding="utf-8") != target_agents:
            errors.append("AGENTS.md foundation differs from canonical core")
        if current_files() != package:
            missing = sorted(package.keys() - current_files().keys())
            extra = sorted(current_files().keys() - package.keys())
            changed = sorted(name for name in package.keys() & current_files().keys()
                             if package[name] != current_files()[name])
            errors.append(f"Antigravity artifact differs: missing={missing}, extra={extra}, changed={changed}")
        for error in errors:
            print(error, file=sys.stderr)
        if not errors:
            print(f"Startup and {len(package)} Antigravity artifact files match canonical source")
        return bool(errors)
    if DEST.exists():
        marker = DEST / "assembly.json"
        if not marker.exists() or json.loads(marker.read_text(encoding="utf-8")).get("format") != "antigravity-plugin":
            raise ValueError(f"Refusing to replace unowned destination: {DEST}")
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    for name, content in package.items():
        path = DEST / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    (ROOT / "AGENTS.md").write_text(target_agents, encoding="utf-8")
    print(f"Wrote startup foundation and {len(package)} Antigravity artifact files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
