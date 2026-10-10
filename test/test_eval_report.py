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
        self.row = {"suite": "startup-and-discovery", "harness": "Codex", "platform": "windows-x86_64",
                    "config": "default", "required": True, "remaining": "Run the fixture."}
        (self.evals / "matrix.json").write_text(json.dumps({"schema": 1, "suite_revision": "1",
                                                        "rows": [self.row]}), encoding="utf-8")
        self.root_patch = patch.object(report, "ROOT", self.root)
        self.eval_patch = patch.object(report, "EVALS", self.evals)
        self.root_patch.start()
        self.eval_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.addCleanup(self.eval_patch.stop)

        (self.evals / "host-probes.md").write_text("host fixture", encoding="utf-8")

    def test_suite_hash_is_stable_across_line_endings(self):
        (self.evals / "host-probes.md").write_bytes(b"host\r\nfixture\r\n")
        crlf_hash = report.suite_sha256("startup-and-discovery")
        (self.evals / "host-probes.md").write_bytes(b"host\nfixture\n")
        self.assertEqual(crlf_hash, report.suite_sha256("startup-and-discovery"))

    def test_candidate_hash_tracks_rules_but_not_personal_configuration(self):
        rules = self.root / "rules"
        rules.mkdir()
        rule = rules / "writing-voice.md"
        rule.write_text("Use the approved voice.", encoding="utf-8")
        original = report.candidate_sha256()
        rule.write_text("Preserve facts and use the approved voice.", encoding="utf-8")
        changed = report.candidate_sha256()
        self.assertNotEqual(original, changed)
        profile = self.root / ".nyssa-ai" / "agent-skills" / "writing-voice"
        profile.mkdir(parents=True)
        (profile / "VOICE.md").write_text("Private voice", encoding="utf-8")
        self.assertEqual(changed, report.candidate_sha256())

    def test_candidate_hash_tracks_public_interrupted_update_fixtures(self):
        scratch = self.evals / "tessl/writing-voice/performance/approved-edits-interrupted-update/fixture/workspace/.temp"
        for name in ("agent-skills/writing-voice/pending.md", "other-task/keep.txt"):
            with self.subTest(fixture=name):
                fixture = scratch / name
                fixture.parent.mkdir(parents=True, exist_ok=True)
                fixture.write_text("Synthetic original", encoding="utf-8")
                before = report.candidate_sha256()
                fixture.write_text("Synthetic changed", encoding="utf-8")
                self.assertNotEqual(before, report.candidate_sha256())

    def test_candidate_hash_normalizes_text_but_preserves_binary_bytes(self):
        source = self.evals / "host-probes.md"
        source.write_bytes(b"host\r\nfixture\r\n")
        crlf_hash = report.candidate_sha256()
        source.write_bytes(b"host\nfixture\n")
        self.assertEqual(crlf_hash, report.candidate_sha256())

        binary = self.evals / "fixture.bin"
        binary.write_bytes(b"\0host\r\nfixture")
        binary_hash = report.candidate_sha256()
        binary.write_bytes(b"\0host\nfixture")
        self.assertNotEqual(binary_hash, report.candidate_sha256())

    def result(self, outcome="Fail"):
        folder = self.evals / "results" / "run-1"
        folder.mkdir(parents=True)
        evidence = folder / "evidence.json"
        evidence.write_text('{"case":"observed"}', encoding="utf-8")
        artifact = folder / "artifact.zip"
        with zipfile.ZipFile(artifact, "w") as archive:
            archive.writestr("H01.txt", "observed one")
            archive.writestr("H02.txt", "observed two")
            archive.writestr("H03.txt", "observed three")
        (folder / "host-trace.json").write_text('{"invocations":["Codex fresh session"]}', encoding="utf-8")
        cases = [{"id": "H01", "score": 2, "review_note": "artifact observed",
                  "artifact_path": "H01.txt", "artifact_sha256": hashlib.sha256(b"observed one").hexdigest()},
                 {"id": "H02", "score": 2 if outcome == "Pass" else 0,
                  "review_note": "artifact observed", "artifact_path": "H02.txt",
                  "artifact_sha256": hashlib.sha256(b"observed two").hexdigest()}]
        for case_id, body, score in (("H03", b"observed three", 2 if outcome == "Pass" else 1),):
            cases.append({"id": case_id, "score": score, "review_note": "artifact observed",
                          "artifact_path": case_id + ".txt",
                          "artifact_sha256": hashlib.sha256(body).hexdigest()})
        data = {"key": list(report.key(self.row)), "state": "completed", "verified": True,
                "completed_at": "2026-09-29T10:00:00Z", "outcome": outcome,
                "score": 100 if outcome == "Pass" else 50,
                "candidate_sha256": report.candidate_sha256(), "suite_revision": "1",
                "suite_sha256": report.suite_sha256("startup-and-discovery"),
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
        evidence = self.result()
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
        self.result()
        with self.assertRaisesRegex(ValueError, "structured host invocation evidence"):
            report.render()

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
