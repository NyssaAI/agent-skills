"""Load the shared file-management core into Codex and Claude sessions."""

from pathlib import Path
import os
import sys


def main() -> int:
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or
                       os.environ.get("PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
    core = plugin_root / "skills" / "manage-file-operations" / "core.md"
    if not core.is_file():
        print(f"Missing plugin foundation: {core}", file=sys.stderr)
        return 1
    core_text = core.read_text(encoding="utf-8").strip()
    # Instruction files on disk do not establish what the host loaded into this session.
    print(core_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
