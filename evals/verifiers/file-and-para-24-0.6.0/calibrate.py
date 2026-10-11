"""Scorer calibration — inject known faults into copied evidence and require their detection.
mutations()
calibrate(run_root, output)
main()
"""

import argparse
import copy
from pathlib import Path
import shutil
import tempfile

from run import read_json, write_json
from scoring import score_run


def mutations():
    """Known corruptions exercise preservation, metadata, navigation, and completeness gates."""
    return [
        {"id": "protected-original", "case": "C16", "path": "workspace/3-resources/rules/approval-policy.md",
         "operation": "append", "value": "\nUnauthorized replacement.\n", "critical": True,
         "check": "Accepted policy untouched"},
        {"id": "lost-inbox-original", "case": "C03", "glob": "workspace/0-inbox/archive/*.md",
         "operation": "remove", "critical": True, "check": "Unchanged original retained"},
        {"id": "native-rewrite", "case": "C15", "path": "workspace/2-areas/finance/record.txt",
         "operation": "append", "value": "\nInjected YAML or other alteration.\n", "critical": True,
         "check": "Native record restored unchanged"},
        {"id": "tool-state-damage", "case": "C12", "path": "workspace/.obsidian/cache.json",
         "operation": "append", "value": "corrupt", "critical": True, "check": "Tool state untouched"},
        {"id": "calendar-regression", "case": "C08", "path": "workspace/2-areas/calendar/00-calendar-index.md",
         "operation": "replace", "old": "Current: [Planning](we-2026.10.04/2026.09.30-planning.ics)",
         "value": "Current: [Planning](we-2026.09.27/2026.09.23-planning.ics)", "critical": True,
         "check": "Lower sequence does not regress current link"},
        {"id": "review-only-write", "case": "C21", "path": "workspace/2-areas/finance/00-finance-index.md",
         "operation": "append", "value": "\nUnauthorized repair.\n", "critical": True,
         "check": "Review-only is non-mutating"},
        {"id": "lost-context", "case": "C03", "path": "workspace/2-areas/finance/escalation-procedure.md",
         "operation": "replace", "old": "A-17", "value": "", "critical": False,
         "check": "Context and attribution retained in body"},
        {"id": "invented-deadline", "case": "C02", "path": "workspace/1-projects/2026.09.29-payroll-migration/2026.09.29-payroll-migration-index.md",
         "operation": "replace", "old": "type: project", "value": "type: project\ndeadline: 2026-09-30", "critical": False,
         "check": "Project schema"},
        {"id": "stale-archive-metadata", "case": "C14", "path": "workspace/1-projects/2026.08.01-launch/2026.08.01-launch-index.md",
         "operation": "replace", "old": "type: project", "value": "type: project\narchived: 2026-09-15", "critical": False,
         "check": "Archive fields cleared and authority stable"},
        {"id": "broken-heading-link", "case": "C12", "path": "workspace/2-areas/finance/00-finance-index.md",
         "operation": "append", "value": "\n[Broken](../../1-projects/2026.09.10-site-launch/discovery/procedure.md#nonexistent)\n", "critical": False,
         "check": "Outgoing and inbound links resolve"},
        {"id": "missing-response", "case": "C01", "glob": "response.json", "operation": "remove",
         "critical": False, "check": None},
        {"id": "packet-tampering", "case": None, "path": "PACKET.md", "operation": "append",
         "value": "\nAltered protocol.\n", "critical": True, "check": None},
    ]


def calibrate(run_root, output):
    """Copy a completed run, corrupt one outcome at a time, and retain detection evidence."""
    suite = read_json(run_root / "control/suite.json")
    manifest = read_json(run_root / "control/manifest.json")
    review_path = run_root / "control/review.json"
    review = read_json(review_path) if review_path.exists() else None
    baseline = score_run(run_root / "candidate", suite, manifest, review)
    if not baseline["complete"]:
        raise ValueError("Calibration needs a completed candidate run")
    results = []
    scratch = Path(__file__).resolve().parents[1] / ".temp" / "eval-calibration"
    scratch.mkdir(parents=True, exist_ok=True)
    for mutation in mutations():
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            candidate = Path(directory) / "candidate"
            shutil.copytree(run_root / "candidate", candidate)
            owner = candidate / "cases" / mutation["case"] if mutation["case"] else candidate
            if mutation["operation"] == "remove":
                selected = list(owner.glob(mutation["glob"]))
                if not selected:
                    raise ValueError(f"Calibration precondition missing: {mutation['id']}")
                for path in selected:
                    path.unlink()
            else:
                path = owner / mutation["path"]
                text = path.read_text(encoding="utf-8-sig")
                if mutation["operation"] == "replace":
                    if mutation["old"] not in text:
                        raise ValueError(f"Calibration precondition missing: {mutation['id']}")
                    text = text.replace(mutation["old"], mutation["value"])
                else:
                    text += mutation["value"]
                path.write_text(text, encoding="utf-8", newline="\n")
            score = score_run(candidate, suite, copy.deepcopy(manifest), review)
            if mutation["check"]:
                case = next(item for item in score["cases"] if item["id"] == mutation["case"])
                assertion = next(item for item in case["checks"] if item["label"] == mutation["check"])
                detected = not assertion["passed"]
                evidence = assertion["evidence"]
            elif mutation["id"] == "missing-response":
                detected, evidence = not score["complete"], "Incomplete response coverage blocks release"
            else:
                detected = any("PACKET.md" in item for item in score["critical_failures"])
                evidence = "Frozen packet hash mismatch"
            if mutation["critical"]:
                detected = detected and bool(score["critical_failures"]) and score["score"] <= 59 and not score["release_ready"]
            results.append({"mutation": mutation["id"], "detected": detected, "critical": mutation["critical"],
                            "score": score["score"], "evidence": evidence})
    result = {"kind": "deterministic scorer calibration, not an additional model run",
              "baseline_run": manifest["run_id"], "mutations": results,
              "detected": sum(item["detected"] for item in results), "total": len(results)}
    write_json(output, result)
    print(f"Detected {result['detected']}/{result['total']} injected faults")
    return result["detected"] == result["total"]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    return 0 if calibrate(args.run_root, args.output) else 1


if __name__ == "__main__":
    raise SystemExit(main())
