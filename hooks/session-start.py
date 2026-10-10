"""Load the shared foundation and writing convention into existing startup sessions."""

from pathlib import Path
import os
import sys


def main() -> int:
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or
                       os.environ.get("PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
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
