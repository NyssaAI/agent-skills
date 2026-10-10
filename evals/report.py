"""Generate, check, and gate the latest plugin evaluation evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
EXCLUDED = {".temp", ".git", "__pycache__", "results", "attempts"}
PUBLIC_SCRATCH_FIXTURES = {
    "evals/tessl/writing-voice/performance/approved-edits-interrupted-update/fixture/workspace/.temp/agent-skills/writing-voice/pending.md",
    "evals/tessl/writing-voice/performance/approved-edits-interrupted-update/fixture/workspace/.temp/other-task/keep.txt",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_inventory() -> dict[str, str]:
    """Freeze the declared behavior/assembly/suite inputs, not evidence outputs."""
    paths = []
    for top in ("skills", "rules", ".tessl-plugin", "scripts", "adapters", "hooks", ".agents", ".claude-plugin", ".codex-plugin", ".cursor-plugin", ".hermes", ".github", "evals"):
        paths.extend((ROOT / top).rglob("*"))
    paths.extend(ROOT / name for name in ("plugin.json", "gemini-extension.json",
                                          "AGENTS.md", "CLAUDE.md", "GEMINI.md",
                                          "README.md"))
    result = {}
    for path in sorted(set(paths)):
        relative = path.relative_to(ROOT)
        if not path.is_file() or (relative.as_posix() not in PUBLIC_SCRATCH_FIXTURES and
                                 any(part in EXCLUDED for part in relative.parts)):
            continue
        if path.name == "LATEST.md" or path.is_symlink():
            continue
        content = path.read_bytes()
        # Git may check text out as CRLF on Windows and LF on Linux. Hash the
        # same canonical text while preserving binary inputs byte-for-byte.
        try:
            content.decode("utf-8")
        except UnicodeDecodeError:
            pass
        else:
            if b"\0" not in content:
                content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        result[path.relative_to(ROOT).as_posix()] = hashlib.sha256(content).hexdigest()
    return result


def candidate_sha256() -> str:
    data = json.dumps(source_inventory(), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def key(row: dict) -> tuple[str, str, str, str]:
    return tuple(row[name] for name in ("suite", "harness", "platform", "config"))


def records(kind: str, matrix_keys: set[tuple[str, str, str, str]]) -> list[tuple[Path, dict]]:
    root = EVALS / kind
    output = []
    if root.exists():
        for path in sorted(root.glob("*/metadata.json")):
            data = read_json(path)
            if tuple(data.get("key", [])) not in matrix_keys:
                raise ValueError(f"Undeclared evaluation row: {path}")
            output.append((path, data))
    return output


def latest(items: list[tuple[Path, dict]]) -> tuple[Path, dict] | None:
    return max(items, key=lambda item: (item[1]["completed_at"], item[0].parent.name), default=None)


def valid_completed(path: Path, data: dict) -> None:
    if data.get("state") != "completed" or data.get("verified") is not True:
        raise ValueError(f"Result is not completed and verified: {path}")
    if data.get("outcome") not in ("Pass", "Fail") or not isinstance(data.get("score"), (int, float)):
        raise ValueError(f"Result has no real scored outcome: {path}")
    if not 0 <= data["score"] <= 100:
        raise ValueError(f"Result score out of range: {path}")
    for field in ("host_version", "model", "artifact", "artifact_sha256",
                  "suite_sha256", "scoring_method", "reviewer", "review_method",
                  "critical_failures", "case_outcomes"):
        if field not in data or data[field] in (None, ""):
            raise ValueError(f"Result lacks {field}: {path}")
    if data.get("host") != data["key"][1] or data.get("platform") != data["key"][2] or data.get("config") != data["key"][3]:
        raise ValueError(f"Result host/platform/config disagrees with row: {path}")
    if not isinstance(data["critical_failures"], list) or not isinstance(data["case_outcomes"], list):
        raise ValueError(f"Result case or failure record has wrong shape: {path}")
    suite = data["key"][0]
    # Startup claims currently have no trusted host-export verifier. Retain
    # completed failures, but do not let submitter-authored files certify a Pass.
    if suite == "startup-and-discovery" and data["outcome"] == "Pass":
        raise ValueError(f"Startup Pass requires a trusted host attestation verifier: {path}")
    expected_cases = {
        "file-and-para-24": [f"C{i:02}" for i in range(1, 25)],
        "startup-and-discovery": ["H01", "H02", "H03"],
    }.get(suite)
    if expected_cases is None or sorted(item.get("id") for item in data["case_outcomes"]) != expected_cases:
        raise ValueError(f"Result lacks complete case outcomes: {path}")
    artifact_name = data["artifact"]
    if Path(artifact_name).is_absolute() or ".." in Path(artifact_name).parts:
        raise ValueError(f"Unsafe artifact path: {path}")
    artifact = path.parent / artifact_name
    if not artifact.is_file() or hashlib.sha256(artifact.read_bytes()).hexdigest() != data["artifact_sha256"]:
        raise ValueError(f"Result artifact missing or hash mismatch: {path}")
    if not zipfile.is_zipfile(artifact):
        raise ValueError(f"Result artifact is not an inspectable ZIP: {path}")
    with zipfile.ZipFile(artifact) as archive:
        names = archive.namelist()
        if not names or any(name.startswith("/") or ".." in Path(name).parts for name in names):
            raise ValueError(f"Result artifact has invalid paths: {path}")
    if not data.get("reviewer_independent") is True:
        raise ValueError(f"Result lacks independent review: {path}")
    if data["critical_failures"] and data["outcome"] == "Pass":
        raise ValueError(f"Critical failure cannot pass release: {path}")
    if suite == "file-and-para-24":
        # This suite ships a replay verifier that regrades the retained
        # candidate and checks every exported artifact hash.
        from run import verify as replay_export
        replay_export(path.parent, ROOT)
        score_data = read_json(path.parent / "score.json")
        if score_data.get("score") != data["score"] or bool(score_data.get("release_ready")) != (data["outcome"] == "Pass"):
            raise ValueError(f"Replayed score disagrees with metadata: {path}")
        if not data.get("suite_sha256") == hashlib.sha256((path.parent / "suite.json").read_bytes()).hexdigest():
            raise ValueError(f"Frozen suite hash disagrees with export: {path}")
    else:
        # The other suites must retain independently reviewable case artifacts.
        # A bare score claim or a one-word evidence file cannot be accepted.
        if data["scoring_method"] != "independent-case-review-v1":
            raise ValueError(f"Unsupported scoring method: {path}")
        for item in data["case_outcomes"]:
            if item.get("score") not in (0, 1, 2) or not item.get("review_note") or not item.get("artifact_path"):
                raise ValueError(f"Case lacks reviewed artifact evidence: {path}")
            member = item["artifact_path"]
            if member not in names:
                raise ValueError(f"Case artifact missing from ZIP: {path}")
            with zipfile.ZipFile(artifact) as archive:
                digest = hashlib.sha256(archive.read(member)).hexdigest()
            if digest != item.get("artifact_sha256"):
                raise ValueError(f"Case artifact hash mismatch: {path}")
        computed = round(sum(item["score"] for item in data["case_outcomes"]) / (2 * len(expected_cases)) * 100, 2)
        if computed != data["score"] or (data["outcome"] == "Pass") != (computed >= 85 and not data["critical_failures"]):
            raise ValueError(f"Case review does not reproduce score/outcome: {path}")
        if data["suite_sha256"] != suite_sha256(suite):
            raise ValueError(f"Suite source hash mismatch: {path}")
    evidence_name = data.get("evidence", "")
    if Path(evidence_name).is_absolute() or ".." in Path(evidence_name).parts:
        raise ValueError(f"Unsafe result evidence path: {path}")
    evidence = path.parent / evidence_name
    if not data.get("evidence") or not evidence.is_file():
        raise ValueError(f"Result evidence missing: {path}")
    actual = hashlib.sha256(evidence.read_bytes()).hexdigest()
    if actual != data.get("evidence_sha256"):
        raise ValueError(f"Result evidence hash mismatch: {path}")
    if suite != "file-and-para-24":
        validate_behavioral_evidence(path, data, artifact, names)
    datetime.fromisoformat(data["completed_at"].replace("Z", "+00:00"))


def validate_behavioral_evidence(path: Path, data: dict, artifact: Path, names: list[str]) -> None:
    """Replay observable suite checks and require a separately reviewable host trace."""
    trace_path = path.parent / "host-trace.json"
    if not trace_path.is_file():
        raise ValueError(f"Result lacks host invocation trace: {path}")
    trace = read_json(trace_path)
    invocations = trace.get("invocations")
    if (trace.get("host") != data["host"] or not isinstance(invocations, list)
            or not invocations or not all(isinstance(item, dict) and (item.get("tool") or item.get("tool_name"))
                                          and (item.get("returned_task_name") or item.get("returned_agent_id")
                                               or item.get("checks_passed")) for item in invocations)):
        raise ValueError(f"Result has no structured host invocation evidence: {path}")
    evidence = read_json(path.parent / data["evidence"])
    if (evidence.get("reviewer") != data["reviewer"] or
            evidence.get("reviewer_independent") is not True or
            evidence.get("case_outcomes") != data["case_outcomes"]):
        raise ValueError(f"Independent review receipt disagrees with result: {path}")
    with zipfile.ZipFile(artifact) as archive:
        required = {f"candidate/{case}/request.md" for case in ("H01", "H02", "H03")}
        required.update(f"candidate/{case}/response.json" for case in ("H01", "H02", "H03"))
        required.update({"review/host-session.jsonl", "review/independent-review.json"})
        if not required.issubset(names):
            raise ValueError(f"Host probe lacks request/response artifacts: {path}")
        raw_log = archive.read("review/host-session.jsonl")
        events = [json.loads(line) for line in raw_log.splitlines() if line.strip()]
        if (not events or any(not isinstance(event, dict) or
                              event.get("host") != data["host"] or
                              not event.get("session_id") or not event.get("event_id")
                              for event in events)):
            raise ValueError(f"Host probe lacks structured session events: {path}")
        event_ids = {event["event_id"] for event in events}
        if len(event_ids) != len(events):
            raise ValueError(f"Host probe has duplicate session events: {path}")
        for case in ("H01", "H02", "H03"):
            response = read_json_from_zip(archive, f"candidate/{case}/response.json")
            observations = response.get("observations", {})
            if (response.get("case_id") != case or
                    not isinstance(observations, dict) or
                    not response.get("session_event_ids") or
                    not set(response["session_event_ids"]).issubset(event_ids)):
                raise ValueError(f"Host probe {case} lacks observed session evidence: {path}")
        review = read_json_from_zip(archive, "review/independent-review.json")
        if (review.get("reviewer") != data["reviewer"] or
                review.get("case_outcomes") != data["case_outcomes"] or
                review.get("host_session_sha256") != hashlib.sha256(raw_log).hexdigest() or
                not review.get("reviewer_observed_session") or
                review.get("reviewer_agent_id") == review.get("candidate_agent_id")):
            raise ValueError(f"Host probe lacks attributable independent review: {path}")
        if (not data.get("assembled_artifact_inventory_sha256") or
                trace.get("assembled_artifact_inventory_sha256") != data["assembled_artifact_inventory_sha256"]):
            raise ValueError(f"Host probe lacks installed package identity: {path}")


def read_json_from_zip(archive: zipfile.ZipFile, member: str) -> dict:
    return json.loads(archive.read(member))


def suite_sha256(suite: str) -> str:
    files = {
        "startup-and-discovery": ("host-probes.md",),
    }.get(suite)
    if files is None:
        raise ValueError(f"Unknown suite: {suite}")
    digest = hashlib.sha256()
    for name in files:
        content = (EVALS / name).read_bytes()
        content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        digest.update(name.encode() + b"\0" + content + b"\0")
    return digest.hexdigest()


def valid_attempt(path: Path, data: dict) -> None:
    if data.get("state") not in ("incomplete", "aborted", "unverified"):
        raise ValueError(f"Attempt has invalid state: {path}")
    for field in ("started_at", "completed_at", "stage", "diagnostic", "next_check", "candidate_sha256"):
        if not data.get(field):
            raise ValueError(f"Attempt lacks {field}: {path}")
    datetime.fromisoformat(data["completed_at"].replace("Z", "+00:00"))


def render() -> tuple[str, bool]:
    matrix = read_json(EVALS / "matrix.json")
    rows = matrix["rows"]
    if len({key(row) for row in rows}) != len(rows):
        raise ValueError("Coverage matrix contains duplicate keys")
    matrix_keys = {key(row) for row in rows}
    results = records("results", matrix_keys)
    attempts = records("attempts", matrix_keys)
    for path, data in results:
        valid_completed(path, data)
    for path, data in attempts:
        valid_attempt(path, data)
    current = candidate_sha256()
    lines = ["# Latest plugin evaluation", "",
             "Generated from `matrix.json`, verified `results/`, and `attempts/` by `python evals/report.py generate`.",
             f"Candidate SHA-256: `{current}`. Suite revision: `{matrix['suite_revision']}`.", "",
             "A missing or failing required row blocks release. A consistent report does not imply release readiness.", "",
             "| Suite | Harness | Platform | Configuration | Required | Latest completed result | Outcome / score | Freshness | Newer attempt / next check |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    ready = True
    for row in rows:
        selected = latest([(p, d) for p, d in results if tuple(d["key"]) == key(row)])
        selected_attempt = latest([(p, d) for p, d in attempts if tuple(d["key"]) == key(row)])
        if selected:
            path, data = selected
            result_link = f"[{path.parent.name}](results/{path.parent.name}/metadata.json)"
            outcome = f"{data['outcome']} / {data['score']}/100"
            freshness = "Current" if (data.get("candidate_sha256") == current and
                                      data.get("suite_revision") == matrix["suite_revision"]) else "Stale"
        else:
            result_link, outcome, freshness = "Not run", "Score unavailable", "No result"
            data = None
        attempt_text = row["remaining"]
        if selected_attempt and (not selected or selected_attempt[1]["completed_at"] > selected[1]["completed_at"]):
            path, attempt = selected_attempt
            attempt_link = f"[{path.parent.name}](attempts/{path.parent.name}/metadata.json)"
            if attempt["candidate_sha256"] == current:
                attempt_text = f"{attempt_link}: {attempt['state']}; {attempt['next_check']}"
            else:
                attempt_text = f"{attempt_link}: {attempt['state']} on an earlier candidate; {row['remaining']}"
        if row["required"] and (not data or data["outcome"] != "Pass" or freshness != "Current"):
            ready = False
        cells = [*key(row), "Yes" if row["required"] else "No", result_link,
                 outcome, freshness, attempt_text]
        lines.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
    lines += ["", f"Release acceptance: **{'Pass' if ready else 'Fail — required evidence missing, stale, or failing'}**.", ""]
    return "\n".join(lines), ready


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "check", "release", "hash"))
    args = parser.parse_args()
    if args.command == "hash":
        print(candidate_sha256())
        return 0
    report, ready = render()
    path = EVALS / "LATEST.md"
    if args.command == "generate":
        path.write_text(report, encoding="utf-8")
        print(path)
        return 0
    if not path.exists() or path.read_text(encoding="utf-8") != report:
        print("LATEST.md differs from evidence; run generate and inspect the diff", file=sys.stderr)
        return 1
    if args.command == "release" and not ready:
        print("Release acceptance failed: required rows lack current passing evidence", file=sys.stderr)
        return 1
    print("Report consistent" + ("; release ready" if ready else "; release incomplete"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
