"""Meaningful report checks: missing rows, failed runs, and altered evidence."""

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evals"))
import report  # noqa: E402


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.evals = self.root / "evals"
        self.evals.mkdir()
        (self.root / "plugin.json").write_text('{"name":"fixture"}', encoding="utf-8")
        self.row = {"suite": "plugin-builder", "harness": "Codex", "platform": "windows-x86_64",
                    "config": "default", "required": True, "remaining": "Run the fixture."}
        (self.evals / "matrix.json").write_text(json.dumps({"schema": 1, "suite_revision": "1",
                                                        "rows": [self.row]}), encoding="utf-8")
        self.root_patch = patch.object(report, "ROOT", self.root)
        self.eval_patch = patch.object(report, "EVALS", self.evals)
        self.root_patch.start()
        self.eval_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.addCleanup(self.eval_patch.stop)

        (self.evals / "builder_run.py").write_text("builder fixture", encoding="utf-8")
        (self.evals / "builder-cases.md").write_text("case fixture", encoding="utf-8")

    def result(self, outcome="Fail"):
        folder = self.evals / "results" / "run-1"
        folder.mkdir(parents=True)
        evidence = folder / "evidence.json"
        evidence.write_text('{"case":"observed"}', encoding="utf-8")
        artifact = folder / "artifact.zip"
        with zipfile.ZipFile(artifact, "w") as archive:
            archive.writestr("B01.txt", "observed one")
            archive.writestr("B02.txt", "observed two")
            archive.writestr("B03.txt", "observed three")
            archive.writestr("B04.txt", "observed four")
        (folder / "host-trace.json").write_text('{"invocations":["Codex fresh session"]}', encoding="utf-8")
        cases = [{"id": "B01", "score": 2, "review_note": "artifact observed",
                  "artifact_path": "B01.txt", "artifact_sha256": hashlib.sha256(b"observed one").hexdigest()},
                 {"id": "B02", "score": 2 if outcome == "Pass" else 0,
                  "review_note": "artifact observed", "artifact_path": "B02.txt",
                  "artifact_sha256": hashlib.sha256(b"observed two").hexdigest()}]
        for case_id, body, score in (("B03", b"observed three", 2),
                                    ("B04", b"observed four", 2 if outcome == "Pass" else 0)):
            cases.append({"id": case_id, "score": score, "review_note": "artifact observed",
                          "artifact_path": case_id + ".txt",
                          "artifact_sha256": hashlib.sha256(body).hexdigest()})
        data = {"key": list(report.key(self.row)), "state": "completed", "verified": True,
                "completed_at": "2026-09-29T10:00:00Z", "outcome": outcome,
                "score": 100 if outcome == "Pass" else 50,
                "candidate_sha256": report.candidate_sha256(), "suite_revision": "1",
                "suite_sha256": report.suite_sha256("plugin-builder"),
                "host": "Codex", "host_version": "test", "platform": "windows-x86_64",
                "config": "default", "model": "test", "scoring_method": "independent-case-review-v1",
                "reviewer": "independent fixture reviewer", "review_method": "artifact inspection",
                "reviewer_independent": True, "critical_failures": [], "case_outcomes": cases,
                "artifact": "artifact.zip", "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
                "evidence": "evidence.json",
                "evidence_sha256": hashlib.sha256(evidence.read_bytes()).hexdigest()}
        (folder / "metadata.json").write_text(json.dumps(data), encoding="utf-8")
        return evidence

    def test_missing_required_row_is_consistent_but_not_release_ready(self):
        text, ready = report.render()
        self.assertFalse(ready)
        self.assertIn("Score unavailable", text)
        self.assertIn("Not run", text)

    def test_latest_failed_result_is_visible_and_current(self):
        self.result()
        with patch.object(report, "valid_completed", return_value=None):
            text, ready = report.render()
        self.assertFalse(ready)
        self.assertIn("Fail / 50/100", text)
        self.assertIn("Current", text)

    def test_tampered_evidence_is_rejected(self):
        evidence = self.result("Pass")
        evidence.write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            report.render()

    def test_self_certified_text_result_is_rejected(self):
        folder = self.evals / "results" / "fake"
        folder.mkdir(parents=True)
        (folder / "pass.txt").write_text("pass", encoding="utf-8")
        (folder / "metadata.json").write_text(json.dumps({
            "key": list(report.key(self.row)), "state": "completed", "verified": True,
            "completed_at": "2026-09-29T10:00:00Z", "outcome": "Pass", "score": 100,
            "candidate_sha256": report.candidate_sha256(), "suite_revision": "1",
            "evidence": "pass.txt", "evidence_sha256": hashlib.sha256(b"pass").hexdigest()
        }), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "lacks"):
            report.render()

    def test_stale_result_does_not_pass_release(self):
        self.result("Pass")
        (self.root / "plugin.json").write_text('{"name":"changed"}', encoding="utf-8")
        with patch.object(report, "valid_completed", return_value=None):
            text, ready = report.render()
        self.assertFalse(ready)
        self.assertIn("Stale", text)

    def test_newer_incomplete_attempt_is_separate(self):
        self.result("Pass")
        folder = self.evals / "attempts" / "run-2"
        folder.mkdir(parents=True)
        (folder / "metadata.json").write_text(json.dumps({
            "key": list(report.key(self.row)), "state": "incomplete",
            "started_at": "2026-09-29T11:00:00Z", "completed_at": "2026-09-29T12:00:00Z",
            "stage": "host invocation", "diagnostic": "authentication expired",
            "next_check": "renew authentication", "candidate_sha256": report.candidate_sha256()
        }), encoding="utf-8")
        with patch.object(report, "valid_completed", return_value=None):
            text, ready = report.render()
        self.assertTrue(ready)
        self.assertIn("run-2", text)
        self.assertIn("renew authentication", text)

    def test_full_shape_self_certified_result_is_rejected(self):
        self.result("Pass")
        with self.assertRaisesRegex(ValueError, "structured host invocation evidence"):
            report.render()

    def test_retained_builder_run_replays(self):
        repository = Path(__file__).resolve().parents[1]
        with patch.object(report, "ROOT", repository), patch.object(report, "EVALS", repository / "evals"):
            path = repository / "evals/results/workflow-final-20260929/metadata.json"
            report.valid_completed(path, report.read_json(path))

    def test_generic_startup_claim_cannot_pass_release(self):
        self.row["suite"] = "startup-and-discovery"
        (self.evals / "matrix.json").write_text(json.dumps({"schema": 1, "suite_revision": "1",
                                                        "rows": [self.row]}), encoding="utf-8")
        (self.evals / "host-probes.md").write_text("fixture", encoding="utf-8")
        folder = self.evals / "results" / "claim"
        folder.mkdir(parents=True)
        artifact = folder / "artifact.zip"
        cases = []
        with zipfile.ZipFile(artifact, "w") as archive:
            for case in ("H01", "H02", "H03"):
                archive.writestr(f"candidate/{case}/request.md", "Check startup.\n")
                member = f"candidate/{case}/response.json"
                response = b'{"observed":"pass"}'
                archive.writestr(member, response)
                cases.append({"id": case, "score": 2, "review_note": "Pass claimed",
                              "artifact_path": member, "artifact_sha256": hashlib.sha256(response).hexdigest()})
        (folder / "host-trace.json").write_text(json.dumps({"host": "Codex", "invocations": [
            {"tool": "claimed_tool", "checks_passed": True}]}), encoding="utf-8")
        evidence = folder / "evidence.json"
        evidence.write_text(json.dumps({"reviewer": "claimant", "reviewer_independent": True,
                                        "case_outcomes": cases}), encoding="utf-8")
        metadata = {"key": list(report.key(self.row)), "state": "completed", "verified": True,
                    "outcome": "Pass", "score": 100, "completed_at": "2026-09-29T10:00:00Z",
                    "candidate_sha256": report.candidate_sha256(), "suite_revision": "1",
                    "suite_sha256": report.suite_sha256("startup-and-discovery"),
                    "host": "Codex", "host_version": "claimed", "platform": "windows-x86_64",
                    "config": "default", "model": "claimed", "scoring_method": "independent-case-review-v1",
                    "reviewer": "claimant", "review_method": "claimed", "reviewer_independent": True,
                    "critical_failures": [], "case_outcomes": cases, "artifact": "artifact.zip",
                    "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
                    "evidence": "evidence.json", "evidence_sha256": hashlib.sha256(evidence.read_bytes()).hexdigest()}
        (folder / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Startup Pass requires a trusted host attestation verifier"):
            report.render()


if __name__ == "__main__":
    unittest.main()
