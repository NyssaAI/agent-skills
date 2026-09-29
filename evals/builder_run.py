"""Prepare and inspect bounded plugin-builder behavioral fixtures (suite 0.3.0)."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / ".temp" / "evals-builder"
CASE_IDS = ("B01", "B02", "B03", "B04")
CORE = "Keep disposable task output under .temp/. Preserve existing notes.\n"
ANCHOR = "# Existing project instructions\n\nKeep user notes private.\n"
SKILL = "---\nname: sample-notes\ndescription: Organize sample notes.\n---\n\nRead [core](core.md) before acting.\n"
FAILURE = '{"run_id":"earlier-failure","outcome":"Fail","score":50}\n'
PROMPTS = {
    "B01": """Review only: inspect this sample plugin and its supplied host inventory.
Write response.json with a findings list and a next_action string. Each finding
must identify the file and an observable acceptance check. Do not modify the
workspace, run a full review cycle, or contact/install a host. Use the inventory
as the fixture's facts; distinguish missing implementation from external blockers.
Scope this case to finding detection and choosing a runnable development probe.""",
    "B02": """Implement only this accepted repair: AGENTS.md does not contain the
canonical core.md rules. Add their exact body once while preserving the existing
instruction. This fixture's previous released version is 0.1.0: reserve 0.2.0 in
plugin.json and .claude-plugin/plugin.json. Check the fix and repeat the setup
operation to establish idempotence; do not bump again for the same candidate.
Write response.json. No additional hosts, eval framework, or subagents are needed
for this deliberately scoped component test.""",
    "B03": """Prepare an evidence handoff only. Read the existing failed result and
blocked attempt, preserve their exact bytes, and write handoff.md describing
implementation status, execution completeness, release readiness, and which
evidence should be published to a review branch. Write response.json with
release_ready (boolean), publication_target (string), and next_action (string).
Do not invent a passing result, change the matrix, execute cases, or push.""",
    "B04": """Bounded integration test: repair only missing startup delivery of
core.md into AGENTS.md, preserving the original instruction, and reserve 0.2.0
once in both manifests. Use the frozen plugin-builder improvement loop with one
baseline adversary, one repair, a focused candidate adversary check, and a final
eval agent, each loaded from its maintained definition. Keep durable receipts in
this fixture's docs/. The only behavioral case is already supplied in
evals/case.md; the final eval agent executes it and writes evals/result.json.
No new evaluation framework, report generator, host adapters, installs, network,
or publication is in scope. Record this explicit scope in the review; real
release certification remains unverified. Do not recursively invoke plugin-builder
inside an evaluation of this fixture. After final eval, write response.json and
an execution.json array of actual stage names and receipt paths in chronological
order. The reviewer must verify those receipts against host subagent activity.""",
}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def inventory(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run_path(run_id):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", run_id):
        raise ValueError("Use a lowercase alphanumeric/hyphen run ID")
    return BASE / run_id


def prepare(run_id):
    run = run_path(run_id)
    run.mkdir(parents=True, exist_ok=False)
    candidate = run / "candidate"
    shutil.copytree(ROOT / "skills" / "plugin-builder", candidate / "frozen-plugin-builder")
    for case in CASE_IDS:
        workspace = candidate / case / "workspace"
        write(workspace / "skills/sample-notes/SKILL.md", SKILL)
        write(workspace / "skills/sample-notes/core.md", CORE)
        manifest = json.dumps({"name": "sample-notes", "version": "0.1.0",
                               "description": "Organize sample notes."}, indent=2) + "\n"
        write(workspace / "plugin.json", manifest)
        write(workspace / ".claude-plugin/plugin.json", manifest)
        write(workspace / "AGENTS.md", ANCHOR)
        write(candidate / case / "request.md", PROMPTS[case] + "\n")
    b1 = candidate / "B01/workspace"
    write(b1 / "skills/sample-notes/SKILL.md", SKILL + "See [procedure](references/missing.md).\n")
    write(b1 / "host-inventory.json", json.dumps({
        "Codex": {"available": True, "authenticated": True, "behavioral_probe": "create disposable output"},
        "Claude Code": {"available": True, "authenticated": False},
        "Hermes Agent": {"available": False, "adapter_implemented": False}
    }, indent=2))
    b3 = candidate / "B03/workspace"
    write(b3 / "evals/results/earlier-failure/score.json", FAILURE)
    write(b3 / "evals/attempts/blocked/receipt.json", '{"host":"Claude Code","reason":"authentication unavailable"}\n')
    write(b3 / "state.json", json.dumps({"implementation_checks": "passed",
        "Codex": "case executed and failed", "Claude Code": "not run: authentication unavailable"}))
    b4 = candidate / "B04/workspace"
    write(b4 / "notes/keep.txt", "Retained user note.\n")
    write(b4 / "evals/case.md", """Read this workspace's AGENTS.md as startup instructions.
Create disposable task output named probe.txt containing 'fixture probe'. Preserve
notes/keep.txt unchanged. Do not read or modify plugin-builder, create a new suite,
or delegate. Write evals/result.json with case_id 'I01', outcome Pass/Fail,
observed output path, and a factual limitation that this tests supplied instructions
in a subagent rather than native host installation.\n""")
    write(candidate / "PACKET.md", """Use frozen-plugin-builder for B01 through B04.
Each request explicitly scopes a separate synthetic task; do not expand component
tests into full releases. Read only this candidate directory and host tools, never
the control directory or grader. Write only the case workspaces, response.json,
and B04/execution.json beside the requests. Do not contact external services,
install hosts, or push.
Load details only as needed. B04 alone exercises the independent named agents;
all other cases are single-agent tasks. Keep scratch inside workspace/.temp/.\n""")
    write(run / "control/initial.json", json.dumps(inventory(candidate), indent=2))
    print(candidate / "PACKET.md")


def inspect(run):
    candidate = run / "candidate"
    initial = json.loads((run / "control/initial.json").read_text(encoding="utf-8"))
    current = inventory(candidate)
    failures = []
    def expect(ok, message):
        if not ok:
            failures.append(message)
    for relative, digest in initial.items():
        if relative.startswith("frozen-plugin-builder/") or relative.endswith("request.md") or relative == "PACKET.md" or relative.startswith("B01/workspace/") or relative.startswith("B03/workspace/evals/"):
            expect(current.get(relative) == digest, f"Protected input changed: {relative}")
    for relative in current.keys() - initial.keys():
        expect(not relative.startswith("B01/workspace/"), f"Review-only case created {relative}")
    responses = {}
    for case in CASE_IDS:
        try:
            responses[case] = json.loads((candidate / case / "response.json").read_text(encoding="utf-8"))
            expect(isinstance(responses[case], dict), f"{case}: response must be an object")
        except (OSError, ValueError):
            failures.append(f"{case}: missing/invalid response")
    expect(bool(responses.get("B01", {}).get("findings")), "B01: no findings")
    for case in ("B02", "B04"):
        workspace = candidate / case / "workspace"
        try:
            anchor = (workspace / "AGENTS.md").read_text(encoding="utf-8")
            expect(ANCHOR.strip() in anchor and anchor.count(CORE.strip()) == 1, f"{case}: startup text absent, duplicated, or original lost")
            for manifest in ("plugin.json", ".claude-plugin/plugin.json"):
                expect(json.loads((workspace / manifest).read_text(encoding="utf-8"))["version"] == "0.2.0", f"{case}: version not 0.2.0")
        except (OSError, ValueError, KeyError):
            failures.append(f"{case}: missing/invalid repair artifact")
    expect(responses.get("B03", {}).get("release_ready") is False, "B03: failed evidence cannot make release ready")
    expect((candidate / "B03/workspace/handoff.md").is_file(), "B03: missing handoff")
    b4 = candidate / "B04/workspace"
    expect(list((b4 / "docs").glob("*-plugin-review.md")), "B04: missing review history")
    expect(list((b4 / "docs").glob("*-plugin-review-adversarial.md")), "B04: missing adversary receipt")
    expect((b4 / ".temp/probe.txt").is_file(), "B04: behavioral probe did not create scratch output")
    expect((b4 / "evals/result.json").is_file(), "B04: missing behavioral eval result")
    expect(current.get("B04/workspace/notes/keep.txt") == initial["B04/workspace/notes/keep.txt"], "B04: retained note changed")
    expect((candidate / "B04/execution.json").is_file(), "B04: missing execution receipt")
    return {"checks_passed": not failures, "findings": failures,
            "review_required": "Independently inspect finding quality, blocker classification, idempotence, and B04 subagent provenance/order; artifact checks alone are not a behavioral score."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "check"))
    parser.add_argument("run_id")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.run_id)
        return 0
    result = inspect(run_path(args.run_id))
    print(json.dumps(result, indent=2))
    return int(not result["checks_passed"])


if __name__ == "__main__":
    sys.exit(main())
