"""Load the shared file-management core into Codex and Claude sessions."""

from pathlib import Path
import os
import sys


def main() -> int:
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or
                       os.environ.get("PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
    core = plugin_root / "skills" / "file-management" / "core.md"
    if not core.is_file():
        print(f"Missing plugin foundation: {core}", file=sys.stderr)
        return 1
    core_text = core.read_text(encoding="utf-8").strip()
    current_block = ("<!-- agent-skills:file-management:begin -->\n" + core_text +
                     "\n<!-- agent-skills:file-management:end -->")
    directories = (Path.cwd(), *Path.cwd().parents)
    project_root = next((directory for directory in directories if (directory / ".git").exists()),
                        Path.cwd())
    for directory in directories:
        anchor = directory / "AGENTS.md"
        if anchor.is_file() and current_block in anchor.read_text(encoding="utf-8-sig"):
            return 0
        # A project's instructions can be inherited by sessions in subdirectories.
        # An unrelated ancestor beyond its repository root is not reliably loaded.
        if directory == project_root:
            break
    print(core_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
