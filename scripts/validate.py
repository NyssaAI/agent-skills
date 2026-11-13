"""Validate the agent-skills repository layout, manifests, docs lockdown, skills, and evals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "evals") not in sys.path:
    sys.path.insert(0, str(ROOT / "evals"))

from plugin_checks import validate_plugin  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repo_root",
        nargs="?",
        type=Path,
        default=ROOT,
        help="Path to the plugin repository root to validate (defaults to repo_root).",
    )
    args = parser.parse_args(argv)
    result = validate_plugin(args.repo_root.resolve())
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
