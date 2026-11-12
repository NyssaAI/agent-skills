"""Load the shared foundation and writing convention into startup sessions.

Root & configuration invariants enforced by the emitted foundation:
- plugin_root: CLAUDE_PLUGIN_ROOT -> PLUGIN_ROOT -> parent of hooks/ (read-only).
- NyssaAI.Configuration: user_home (~/.nyssa-ai/) -> repo_root (<repo_root>/.nyssa-ai/).
  Only canonical .nyssa-ai/ directories are consulted; legacy directory fallbacks are retired.
- runtime_root: --runtime-root -> NYSSA_RUNTIME_ROOT -> persona cwd (SOUL.md + IDENTITY.md)
  -> ~/.nyssa-ai/<plugin>/runtime/ or <repo_root>/.nyssa-ai/<plugin>/runtime/.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys


def resolve_plugin_root() -> Path:
    return Path(
        os.environ.get("CLAUDE_PLUGIN_ROOT")
        or os.environ.get("PLUGIN_ROOT")
        or Path(__file__).resolve().parents[1]
    )


def resolve_runtime_root(
    plugin_name: str = "agent-skills",
    explicit_runtime_root: str | Path | None = None,
    cwd: Path | None = None,
    user_home: Path | None = None,
    repo_root: Path | None = None,
) -> Path:
    """Resolve runtime_root using the locked 4-step precedence."""
    if explicit_runtime_root:
        return Path(explicit_runtime_root).expanduser().resolve()
    env_runtime = os.environ.get("NYSSA_RUNTIME_ROOT")
    if env_runtime:
        return Path(env_runtime).expanduser().resolve()
    active_cwd = (cwd or Path.cwd()).resolve()
    if (active_cwd / "SOUL.md").is_file() and (active_cwd / "IDENTITY.md").is_file():
        return active_cwd
    if repo_root is not None and (repo_root / ".nyssa-ai" / plugin_name).is_dir():
        return (repo_root / ".nyssa-ai" / plugin_name / "runtime").resolve()
    home = (user_home or Path.home()).expanduser().resolve()
    return home / ".nyssa-ai" / plugin_name / "runtime"


def resolve_config_roots(user_home: Path | None = None, repo_root: Path | None = None) -> tuple[Path, ...]:
    """Return canonical NyssaAI.Configuration roots in order: user_home -> repo_root (.nyssa-ai only)."""
    home = (user_home or Path.home()).expanduser().resolve()
    roots: list[Path] = [home / ".nyssa-ai"]
    if repo_root is not None:
        resolved_repo = repo_root.resolve()
        if resolved_repo != home:
            roots.append(resolved_repo / ".nyssa-ai")
    return tuple(roots)


def main() -> int:
    plugin_root = resolve_plugin_root()
    core = plugin_root / "skills" / "manage-file-operations" / "core.md"
    sources = (core, plugin_root / "rules" / "writing-voice.md")
    for source in sources:
        if not source.is_file():
            print(f"Missing plugin foundation: {source}", file=sys.stderr)
            return 1
    core_text = "\n\n".join(source.read_text(encoding="utf-8").strip() for source in sources)
    # Instruction files on disk do not establish what the host loaded into this session.
    print(core_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
