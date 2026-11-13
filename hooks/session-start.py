"""Load the shared foundation and writing convention into startup sessions.

Root & configuration invariants enforced by the emitted foundation:
- plugin_root: CLAUDE_PLUGIN_ROOT -> PLUGIN_ROOT -> parent of hooks/ (read-only).
- NyssaAI.Configuration: user_home (~/.nyssa-ai/<plugin>/config.json)
  -> repo_root (<repo_root>/.nyssa-ai/<plugin>/config.json).
  Only canonical .nyssa-ai/ directories are consulted; legacy directory fallbacks are retired.
- runtime_root: --runtime-root -> NYSSA_RUNTIME_ROOT -> <persona_cwd>/.nyssa-ai/<plugin>/runtime/
  (when cwd has SOUL.md + IDENTITY.md) -> layered config.json runtimeRoot, else
  <repo_root>/.nyssa-ai/<plugin>/runtime/ (when <repo_root>/.nyssa-ai/<plugin>/ exists),
  else ~/.nyssa-ai/<plugin>/runtime/.
- Usage telemetry: opt-in only (telemetry.enabled === true in layered config.json; default false).
  Zero usage/ directories or files are created unless telemetry.enabled is True.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Any


def strip_frontmatter(text: str) -> str:
    """Strip leading YAML frontmatter from rule files before injecting into session context."""
    match = re.match(r"\A---\r?\n.*?\r?\n---\r?\n*", text, re.S)
    return text[match.end():].strip() if match else text.strip()


def resolve_plugin_root() -> Path:
    return Path(
        os.environ.get("CLAUDE_PLUGIN_ROOT")
        or os.environ.get("PLUGIN_ROOT")
        or Path(__file__).resolve().parents[1]
    )


def _is_persona_workspace(directory: Path) -> bool:
    return (directory / "SOUL.md").is_file() and (directory / "IDENTITY.md").is_file()


def _merge_config_dicts(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)
    for key, value in override.items():
        existing = merged.get(key)
        if isinstance(existing, dict) and isinstance(value, Mapping):
            merged[key] = _merge_config_dicts(existing, value)
        else:
            merged[key] = dict(value) if isinstance(value, Mapping) else value
    return merged


def resolve_config_roots(user_home: Path | None = None, repo_root: Path | None = None) -> tuple[Path, ...]:
    """Return canonical NyssaAI.Configuration roots in order: user_home -> repo_root (.nyssa-ai only)."""
    home = Path(user_home or Path.home()).expanduser().resolve()
    roots: list[Path] = [home / ".nyssa-ai"]
    if repo_root is not None:
        resolved_repo = Path(repo_root).expanduser().resolve()
        if resolved_repo != home:
            roots.append(resolved_repo / ".nyssa-ai")
    return tuple(roots)


def load_plugin_config(
    plugin_name: str = "agent-skills",
    repo_root: Path | None = None,
    user_home: Path | None = None,
) -> dict[str, Any]:
    """Load layered static config.json in order: user_home -> repo_root (.nyssa-ai/<plugin>/config.json)."""
    merged: dict[str, Any] = {}
    for config_root in resolve_config_roots(user_home=user_home, repo_root=repo_root):
        config_path = config_root / plugin_name / "config.json"
        if not config_path.is_file():
            continue
        try:
            parsed = json.loads(config_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(parsed, Mapping):
            merged = _merge_config_dicts(merged, parsed)
    return merged


def resolve_runtime_root(
    plugin_name: str = "agent-skills",
    explicit_runtime_root: str | Path | None = None,
    cwd: Path | None = None,
    user_home: Path | None = None,
    repo_root: Path | None = None,
    *,
    runtime_root: str | Path | None = None,
    config: Mapping[str, Any] | None = None,
) -> Path:
    """Resolve runtime_root using the locked 4-step precedence."""
    override = runtime_root if runtime_root is not None else explicit_runtime_root
    if isinstance(override, Path) or (isinstance(override, str) and override.strip()):
        return Path(override).expanduser().resolve()

    env_runtime = os.environ.get("NYSSA_RUNTIME_ROOT", "").strip()
    if env_runtime:
        env_dir = Path(env_runtime).expanduser().resolve()
        if _is_persona_workspace(env_dir):
            return (env_dir / ".nyssa-ai" / plugin_name / "runtime").resolve()
        return env_dir

    active_cwd = Path(cwd or Path.cwd()).expanduser().resolve()
    if _is_persona_workspace(active_cwd):
        return (active_cwd / ".nyssa-ai" / plugin_name / "runtime").resolve()

    home = Path(user_home or Path.home()).expanduser().resolve()
    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root is not None else None
    merged_config = (
        dict(config)
        if config is not None
        else load_plugin_config(plugin_name=plugin_name, repo_root=resolved_repo, user_home=home)
    )
    configured_runtime = merged_config.get("runtimeRoot")
    if isinstance(configured_runtime, str) and configured_runtime.strip():
        return Path(configured_runtime.strip()).expanduser().resolve()

    if resolved_repo is not None and (resolved_repo / ".nyssa-ai" / plugin_name).is_dir():
        return (resolved_repo / ".nyssa-ai" / plugin_name / "runtime").resolve()
    return (home / ".nyssa-ai" / plugin_name / "runtime").resolve()


def is_telemetry_enabled(
    config: Mapping[str, Any] | None = None,
    *,
    plugin_name: str = "agent-skills",
    repo_root: Path | None = None,
    user_home: Path | None = None,
) -> bool:
    """Return True only when layered config.json explicitly sets telemetry.enabled === true."""
    merged = (
        config
        if config is not None
        else load_plugin_config(plugin_name=plugin_name, repo_root=repo_root, user_home=user_home)
    )
    telemetry = merged.get("telemetry") if isinstance(merged, Mapping) else None
    return isinstance(telemetry, Mapping) and telemetry.get("enabled") is True


def resolve_usage_telemetry_dir(
    plugin_name: str = "agent-skills",
    explicit_runtime_root: str | Path | None = None,
    cwd: Path | None = None,
    user_home: Path | None = None,
    repo_root: Path | None = None,
    *,
    runtime_root: str | Path | None = None,
    config: Mapping[str, Any] | None = None,
) -> Path | None:
    """Return <runtime_root>/usage when telemetry.enabled is True, else None (creates zero directories)."""
    merged = (
        dict(config)
        if config is not None
        else load_plugin_config(plugin_name=plugin_name, repo_root=repo_root, user_home=user_home)
    )
    if not is_telemetry_enabled(merged):
        return None
    resolved_runtime = resolve_runtime_root(
        plugin_name=plugin_name,
        explicit_runtime_root=explicit_runtime_root,
        cwd=cwd,
        user_home=user_home,
        repo_root=repo_root,
        runtime_root=runtime_root,
        config=merged,
    )
    return resolved_runtime / "usage"


def record_usage_event(
    event: str,
    payload: Mapping[str, Any] | None = None,
    *,
    plugin_name: str = "agent-skills",
    explicit_runtime_root: str | Path | None = None,
    cwd: Path | None = None,
    user_home: Path | None = None,
    repo_root: Path | None = None,
    runtime_root: str | Path | None = None,
    config: Mapping[str, Any] | None = None,
) -> Path | None:
    """Append an event to <runtime_root>/usage/events.jsonl only when telemetry.enabled is True."""
    usage_dir = resolve_usage_telemetry_dir(
        plugin_name=plugin_name,
        explicit_runtime_root=explicit_runtime_root,
        cwd=cwd,
        user_home=user_home,
        repo_root=repo_root,
        runtime_root=runtime_root,
        config=config,
    )
    if usage_dir is None:
        return None
    usage_dir.mkdir(parents=True, exist_ok=True)
    events_path = usage_dir / "events.jsonl"
    entry: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "plugin": plugin_name,
        "event": event,
    }
    if payload:
        entry["data"] = dict(payload)
    with events_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
    return events_path


def _discover_repo_root(start: Path) -> Path | None:
    resolved = start.resolve()
    for candidate in (resolved, *resolved.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--runtime-root", default=None)
    args, _ = parser.parse_known_args(argv)

    plugin_root = resolve_plugin_root()
    core = plugin_root / "skills" / "manage-file-operations" / "core.md"
    sources = (core, plugin_root / "rules" / "writing-voice.md")
    for source in sources:
        if not source.is_file():
            print(f"Missing plugin foundation: {source}", file=sys.stderr)
            return 1
    core_text = "\n\n".join(strip_frontmatter(source.read_text(encoding="utf-8")) for source in sources)
    # Instruction files on disk do not establish what the host loaded into this session.
    print(core_text)

    active_cwd = Path.cwd().resolve()
    repo_root = _discover_repo_root(active_cwd)
    try:
        record_usage_event(
            "session_start",
            {"hook": "SessionStart"},
            plugin_name="agent-skills",
            explicit_runtime_root=args.runtime_root,
            cwd=active_cwd,
            repo_root=repo_root,
        )
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
