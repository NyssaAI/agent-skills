"""Synthetic fixture loader; this is not a real agent harness."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
host = sys.argv[1]
if host not in ("alpha", "beta"):
    raise SystemExit("Expected alpha or beta")
core = root / "core.md"
adapter = root / "adapters" / (host + ".json")
try:
    registration = json.loads(adapter.read_text(encoding="utf-8"))
    target = (adapter.parent / registration["core"]).resolve()
    if target != core or not target.is_file():
        raise ValueError("Adapter must load the canonical core.md")
    text = target.read_text(encoding="utf-8")
    if not text.startswith("Foundation v"):
        raise ValueError("Foundation content missing")
    result = {"host": host, "outcome": "Pass", "core_sha256": hashlib.sha256(core.read_bytes()).hexdigest(),
              "adapter_sha256": hashlib.sha256(adapter.read_bytes()).hexdigest(), "loaded": text}
except (OSError, ValueError, KeyError) as error:
    result = {"host": host, "outcome": "Fail", "error": str(error)}
with (root / "probe-events.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
    stream.write(json.dumps(result) + "\n")
print(json.dumps(result))
raise SystemExit(0 if result["outcome"] == "Pass" else 1)
