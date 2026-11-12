"""Assemble root harness-adapter manifests and stage packaged host bundles."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / ".temp" / "dist"
BEGIN = "<!-- agent-skills:file-management:begin -->"
END = "<!-- agent-skills:file-management:end -->"
CORE = ROOT / "skills" / "manage-file-operations" / "core.md"
TESSL_RULE = ROOT / "rules" / "file-management.md"
VOICE_RULE = ROOT / "rules" / "writing-voice.md"
VOICE_BEGIN = "<!-- agent-skills:writing-voice:begin -->"
VOICE_END = "<!-- agent-skills:writing-voice:end -->"
HERMES_ADAPTER = ROOT / "harness-adapters" / "hermes" / "plugin.py"
CODEX_ADAPTER_DIR = ROOT / "harness-adapters" / "codex"
EXCLUDED_SKILL_PARTS = frozenset({"__pycache__", ".pytest_cache", ".nyssa-ai", ".temp"})
FORBIDDEN_REPO_TREES = frozenset({".agents", ".hermes", "artifacts"})


def _encode_json(value: object) -> bytes:
    return (json.dumps(value, indent=2) + "\n").encode("utf-8")


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
    output: dict[str, bytes] = {}
    for source in sorted((ROOT / "skills").rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT)
        if any(part in EXCLUDED_SKILL_PARTS for part in relative.parts):
            continue
        output[relative.as_posix()] = source.read_bytes()
    return output


def codex_skill_metadata() -> dict[str, bytes]:
    """Map Codex UI harness-adapter metadata into portable skill paths."""
    output: dict[str, bytes] = {}
    if not CODEX_ADAPTER_DIR.is_dir():
        return output
    for source in sorted(CODEX_ADAPTER_DIR.glob("*/openai.yaml")):
        skill_name = source.parent.name
        if (ROOT / "skills" / skill_name / "SKILL.md").is_file():
            output[f"skills/{skill_name}/agents/openai.yaml"] = source.read_bytes()
    return output


def source_hash(files: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name in sorted(files):
        content = canonical_hash_content(files[name])
        digest.update(name.encode("utf-8") + b"\0" + content + b"\0")
    return digest.hexdigest()


def root_harness_manifests() -> dict[str, bytes]:
    identity = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    claude = {
        "name": identity["name"],
        "version": identity["version"],
        "description": identity["description"],
        "author": identity["author"],
        "repository": identity["repository"],
        "license": identity["license"],
        "keywords": ["nyssa", "agent", "skills", "workflows", "tools"],
    }
    codex = {
        "name": identity["name"],
        "version": identity["version"],
        "description": identity["description"],
        "author": identity["author"],
        "homepage": identity["homepage"],
        "repository": identity["repository"],
        "license": identity["license"],
        "keywords": ["nyssa", "skills", "agent", "para-vault", "workflows"],
        "skills": "./skills/",
        "interface": {
            "displayName": "NyssaAI Agent Skills",
            "shortDescription": "Foundational skills and conventions for AI agents",
            "longDescription": (
                "Foundational skills and conventions for how Jeremy and NyssaAI's "
                "AI agents organize information, manage files, and carry out work."
            ),
            "developerName": "NyssaAI",
            "category": "Productivity",
            "capabilities": ["Interactive", "Read", "Write"],
            "websiteURL": "https://github.com/NyssaAI/agent-skills",
            "defaultPrompt": ["Organize my PARA vault", "File these notes into PARA"],
        },
    }
    cursor = {
        "name": identity["name"],
        "version": identity["version"],
        "description": identity["description"],
        "author": identity["author"],
        "homepage": identity["homepage"],
        "repository": identity["repository"],
        "license": identity["license"],
        "keywords": ["nyssa", "skills", "para-vault", "workflows"],
    }
    tessl = {
        "name": f"nyssa-ai/{identity['name']}",
        "version": identity["version"],
        "description": "Private evaluation of NyssaAI file operations, PARA, and writing voice skills",
        "private": True,
        "skills": "./skills",
        "rules": "./rules",
    }
    gemini = {
        "name": identity["name"],
        "description": identity["description"],
        "version": identity["version"],
        "contextFileName": "GEMINI.md",
    }
    return {
        ".claude-plugin/plugin.json": _encode_json(claude),
        ".codex-plugin/plugin.json": _encode_json(codex),
        ".cursor-plugin/plugin.json": _encode_json(cursor),
        ".tessl-plugin/plugin.json": _encode_json(tessl),
        "gemini-extension.json": _encode_json(gemini),
    }


def portable_expected_files() -> dict[str, bytes]:
    identity = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    manifests = root_harness_manifests()
    output: dict[str, bytes] = {
        "plugin.json": (ROOT / "plugin.json").read_bytes(),
        "LICENSE": (ROOT / "LICENSE").read_bytes(),
        **manifests,
        "hooks/hooks.json": (ROOT / "hooks" / "hooks.json").read_bytes(),
        "hooks/session-start.py": (ROOT / "hooks" / "session-start.py").read_bytes(),
        "rules/file-management.md": (CORE.read_text(encoding="utf-8").strip() + "\n").encode("utf-8"),
        "rules/writing-voice.md": VOICE_RULE.read_bytes(),
    }
    output.update(skill_files())
    output.update(codex_skill_metadata())
    output["assembly.json"] = _encode_json({
        "format": "portable-plugin",
        "source": "scripts/assemble.py",
        "source_sha256": source_hash(output),
        "version": identity["version"],
    })
    return output


def expected_files() -> dict[str, bytes]:
    identity = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    manifest = {
        "$schema": "https://antigravity.google/schemas/v1/plugin.json",
        "name": identity["name"],
        "description": identity["description"],
    }
    output: dict[str, bytes] = {"plugin.json": _encode_json(manifest)}
    rule_header = (
        "---\n"
        "trigger: always_on\n"
        "description: Core file-management naming and safety rules.\n"
        "---\n\n"
    ).encode("utf-8")
    output["rules/file-management.md"] = rule_header + CORE.read_bytes().rstrip() + b"\n"
    output["rules/writing-voice.md"] = (
        b"---\ntrigger: always_on\ndescription: Apply the user's applicable writing voice.\n---\n\n"
        + VOICE_RULE.read_bytes().rstrip() + b"\n"
    )
    output.update(skill_files())
    output["assembly.json"] = _encode_json({
        "format": "antigravity-plugin",
        "source": "scripts/assemble.py",
        "source_sha256": source_hash(output),
        "version": identity["version"],
    })
    return output


def hermes_expected_files() -> dict[str, bytes]:
    identity = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    manifest = (
        f"name: {json.dumps(identity['name'])}\n"
        f"version: {json.dumps(identity['version'])}\n"
        f"description: {json.dumps(identity['description'])}\n"
    )
    output: dict[str, bytes] = {
        "plugin.yaml": manifest.encode("utf-8"),
        "__init__.py": HERMES_ADAPTER.read_bytes(),
        "rules/writing-voice.md": VOICE_RULE.read_bytes(),
    }
    output.update(skill_files())
    output["assembly.json"] = _encode_json({
        "format": "hermes-plugin",
        "source": "scripts/assemble.py",
        "source_sha256": source_hash(output),
        "version": identity["version"],
    })
    return output


def build_packages() -> dict[str, tuple[str, dict[str, bytes]]]:
    return {
        "portable": ("portable-plugin", portable_expected_files()),
        "antigravity": ("antigravity-plugin", expected_files()),
        "hermes": ("hermes-plugin", hermes_expected_files()),
    }


def current_files(destination: Path) -> dict[str, bytes]:
    if not destination.exists():
        return {}
    return {
        p.relative_to(destination).as_posix(): p.read_bytes()
        for p in destination.rglob("*")
        if p.is_file()
    }


def validate_output_dir(output_dir: Path) -> Path:
    if output_dir.is_symlink():
        raise ValueError(f"Unsafe symlink output directory: {output_dir}")
    resolved = output_dir.resolve()
    repo_resolved = ROOT.resolve()
    if resolved == repo_resolved:
        raise ValueError(f"Refusing to stage bundles directly into repo_root: {output_dir}")
    if resolved.is_relative_to(repo_resolved):
        rel_parts = resolved.relative_to(repo_resolved).parts
        if rel_parts and rel_parts[0] in FORBIDDEN_REPO_TREES:
            raise ValueError(f"Forbidden self-loaded host tree inside repo_root: {output_dir}")
        if not rel_parts or rel_parts[0] != ".temp":
            raise ValueError(f"In-repo bundle staging must live under <repo_root>/.temp/: {output_dir}")
    return resolved


def ensure_owned_destination(destination: Path, package_format: str) -> None:
    if destination.is_symlink():
        raise ValueError(f"Unsafe package destination: {destination}")
    if destination.exists():
        marker = destination / "assembly.json"
        if not marker.is_file() or json.loads(marker.read_text(encoding="utf-8")).get("format") != package_format:
            raise ValueError(f"Refusing to replace unowned destination: {destination}")


def write_package(destination: Path, package: dict[str, bytes]) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in package.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def assemble(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("write", "check"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for staged host bundles (defaults to <repo_root>/.temp/dist).",
    )
    args = parser.parse_args(argv)
    explicit_output_dir = args.output_dir is not None
    output_dir = validate_output_dir(args.output_dir or DEFAULT_OUTPUT_DIR)

    target_agents = anchored_agents()
    target_rule = CORE.read_text(encoding="utf-8").strip() + "\n"
    manifests = root_harness_manifests()
    packages = build_packages()

    if args.mode == "check":
        errors: list[str] = []
        for forbidden in FORBIDDEN_REPO_TREES:
            if (ROOT / forbidden).exists():
                errors.append(f"Forbidden directory present in repo_root: {forbidden}/")
        if (ROOT / "AGENTS.md").read_text(encoding="utf-8") != target_agents:
            errors.append("AGENTS.md foundation differs from canonical core")
        if not TESSL_RULE.is_file() or TESSL_RULE.read_text(encoding="utf-8") != target_rule:
            errors.append("Tessl foundation rule differs from canonical core")
        for rel_manifest, expected_bytes in manifests.items():
            manifest_path = ROOT / rel_manifest
            if not manifest_path.is_file() or canonical_hash_content(manifest_path.read_bytes()) != canonical_hash_content(expected_bytes):
                errors.append(f"Harness manifest differs from canonical plugin.json: {rel_manifest}")
        if explicit_output_dir or output_dir.exists():
            for bundle_name, (_, expected) in packages.items():
                destination = output_dir / bundle_name
                current = current_files(destination)
                normalized_current = {k: canonical_hash_content(v) for k, v in current.items()}
                normalized_expected = {k: canonical_hash_content(v) for k, v in expected.items()}
                if normalized_current != normalized_expected:
                    missing = sorted(normalized_expected.keys() - normalized_current.keys())
                    extra = sorted(normalized_current.keys() - normalized_expected.keys())
                    changed = sorted(
                        name for name in normalized_expected.keys() & normalized_current.keys()
                        if normalized_expected[name] != normalized_current[name]
                    )
                    errors.append(
                        f"{bundle_name} bundle differs: missing={missing}, extra={extra}, changed={changed}"
                    )
        for error in errors:
            print(error, file=sys.stderr)
        if not errors:
            counts = ", ".join(f"{len(files)} {name}" for name, (_, files) in packages.items())
            print(f"Startup, harness manifests, Tessl rule, and staged bundles ({counts}) match canonical source")
        return 1 if errors else 0

    for rel_manifest, expected_bytes in manifests.items():
        manifest_path = ROOT / rel_manifest
        if manifest_path.is_symlink() or not manifest_path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f"Unsafe manifest destination: {manifest_path}")
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_bytes(expected_bytes)

    if not TESSL_RULE.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError(f"Unsafe rule destination: {TESSL_RULE}")
    (ROOT / "AGENTS.md").write_text(target_agents, encoding="utf-8")
    TESSL_RULE.parent.mkdir(parents=True, exist_ok=True)
    TESSL_RULE.write_text(target_rule, encoding="utf-8")

    output_dir.mkdir(parents=True, exist_ok=True)
    for bundle_name, (package_format, expected) in packages.items():
        destination = output_dir / bundle_name
        ensure_owned_destination(destination, package_format)
        write_package(destination, expected)

    counts = ", ".join(f"{len(files)} {name}" for name, (_, files) in packages.items())
    print(f"Wrote startup foundation, harness manifests, Tessl rule, and staged bundles ({counts}) to {output_dir}")
    return 0


def main() -> int:
    return assemble()


if __name__ == "__main__":
    raise SystemExit(main())
