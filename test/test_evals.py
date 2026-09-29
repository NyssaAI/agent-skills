"""Evaluation tests — challenge grading with correct, corrupt, missing, and unsafe artifacts.
OutcomeScoringTests
  setUp()
  tearDown()
  write(relative, content)
  evaluate(assertion, original, response)
  test_native_preservation_detects_content_changes()
  test_frontmatter_dates_parse_as_dates_without_false_failure()
  test_canonical_string_is_not_a_boolean()
  test_read_only_detects_empty_directory_mutation()
  test_body_context_does_not_count_stripped_frontmatter()
  test_wikilink_basename_ambiguity_fails()
  test_markdown_percent_encoding_and_heading_resolve()
  test_missing_heading_fails()
  test_dotted_date_wikilink_appends_markdown_extension()
  test_missing_response_cannot_release()
  test_critical_failure_caps_score()
  test_absent_manual_review_cannot_release()
  test_correct_artifact_with_review_can_release()
  test_candidate_cannot_modify_the_packet()
  sample_run()
EvidenceExportTests
  setUp()
  tearDown()
  test_prepare_refuses_reusing_a_run_id()
  test_safe_paths_reject_escape_and_windows_drive()
  test_export_can_be_regraded_and_tampering_is_detected()
  test_candidate_command_receives_packet_and_receipt()
  test_candidate_timeout_records_failure()
"""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "evals"))

from cases import check, note
from run import execute, inventory, prepare, read_json, safe_child, score, verify, write_json
from scoring import evaluate_check, score_run


class OutcomeScoringTests(unittest.TestCase):
    def setUp(self):
        scratch = REPOSITORY / ".temp" / "eval-unit-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return path

    def evaluate(self, assertion, original=None, response=None):
        return evaluate_check(assertion, self.root, original or {}, response or {})[0]

    def test_native_preservation_detects_content_changes(self):
        self.write("record.ics", "BEGIN:VCALENDAR\nEND:VCALENDAR\n")
        assertion = check("Native bytes", "preservation", "same_as", True, path="record.ics", source="source.ics")
        original = {"source.ics": "BEGIN:VCALENDAR\nEND:VCALENDAR\n"}
        self.assertTrue(self.evaluate(assertion, original))
        self.write("record.ics", "---\ntype: note\n---\nBEGIN:VCALENDAR\nEND:VCALENDAR\n")
        self.assertFalse(self.evaluate(assertion, original))

    def test_frontmatter_dates_parse_as_dates_without_false_failure(self):
        self.write("note.md", note("Body", created="2026-09-29"))
        assertion = check("Date", "metadata", "frontmatter", path="note.md", fields={"created": "2026-09-29"}, absent=["canonical"])
        self.assertTrue(self.evaluate(assertion))

    def test_body_context_does_not_count_stripped_frontmatter(self):
        self.write("note.md", note("Body", extra="context: audit-A17\n"))
        assertion = check("Context", "task", "body", path="note.md", contains=["audit-A17"])
        self.assertFalse(self.evaluate(assertion))
        self.write("note.md", note("Body. audit-A17"))
        self.assertTrue(self.evaluate(assertion))

    def test_canonical_string_is_not_a_boolean(self):
        self.write("note.md", note("Body", extra='canonical: "true"\n'))
        assertion = check("Authority", "metadata", "frontmatter", path="note.md", not_true=["canonical"])
        self.assertFalse(self.evaluate(assertion))

    def test_read_only_detects_empty_directory_mutation(self):
        (self.root / "unexpected").mkdir()
        assertion = check("Read only", "preservation", "no_changes", True)
        passed, _ = evaluate_check(assertion, self.root, {}, {}, [])
        self.assertFalse(passed)

    def test_wikilink_basename_ambiguity_fails(self):
        self.write("index.md", "[[policy]]")
        self.write("finance/policy.md", "# Policy")
        assertion = check("Links", "navigation", "links_valid", glob="index.md")
        self.assertTrue(self.evaluate(assertion))
        self.write("marketing/policy.md", "# Policy")
        self.assertFalse(self.evaluate(assertion))

    def test_markdown_percent_encoding_and_heading_resolve(self):
        self.write("index.md", "[Note](Notes/Legacy%20Notes.md#evidence)")
        self.write("Notes/Legacy Notes.md", "# Note\n\n## Evidence\n\nProof.")
        self.assertTrue(self.evaluate(check("Links", "navigation", "links_valid", glob="index.md")))

    def test_missing_heading_fails(self):
        self.write("index.md", "[Note](note.md#missing)")
        self.write("note.md", "# Note")
        self.assertFalse(self.evaluate(check("Links", "navigation", "links_valid", glob="index.md")))

    def test_dotted_date_wikilink_appends_markdown_extension(self):
        self.write("index.md", "[[projects/2026.09.29-project-index]]")
        self.write("projects/2026.09.29-project-index.md", "# Project")
        self.assertTrue(self.evaluate(check("Links", "navigation", "links_valid", glob="index.md")))

    def sample_run(self):
        self.write("PACKET.md", "Frozen packet")
        self.write("cases/C01/request.md", "Frozen request")
        self.write("cases/C01/workspace/record.txt", "Evidence")
        manifest = {"run_id": "sample", "case_ids": ["C01"], "initial_files": inventory(self.root), "execution": {"kind": "test"}}
        assertions = [check(dimension, dimension, "unchanged", dimension == "preservation", path="record.txt")
                      for dimension in ["task", "preservation", "metadata", "navigation"]]
        suite = {"version": "test", "cases": [{"id": "C01", "title": "Sample", "files": {"record.txt": "Evidence"}, "checks": assertions}]}
        response = {"case_id": "C01", "status": "completed", "summary": "Retained evidence", "questions": [], "limitations": [], "decisions": {}}
        review = {"reviewer": "test", "method": "artifact review", "cases": {"C01": {"score": 2, "evidence": "Verified retained evidence"}}}
        return manifest, suite, response, review

    def test_missing_response_cannot_release(self):
        manifest, suite, _, review = self.sample_run()
        result = score_run(self.root, suite, manifest, review)
        self.assertFalse(result["complete"])
        self.assertFalse(result["release_ready"])
        self.assertEqual(result["cases_total"], 1)

    def test_critical_failure_caps_score(self):
        manifest, suite, response, review = self.sample_run()
        write_json(self.root / "cases/C01/response.json", response)
        suite["cases"][0]["checks"][1] = check("Missing preservation", "preservation", "exists", True, path="missing.txt")
        result = score_run(self.root, suite, manifest, review)
        self.assertEqual(result["score"], 59)
        self.assertGreater(result["uncapped_score"], result["score"])
        self.assertFalse(result["release_ready"])

    def test_absent_manual_review_cannot_release(self):
        manifest, suite, response, _ = self.sample_run()
        write_json(self.root / "cases/C01/response.json", response)
        result = score_run(self.root, suite, manifest)
        self.assertEqual(result["score"], 90)
        self.assertFalse(result["reviewed"])
        self.assertFalse(result["release_ready"])

    def test_correct_artifact_with_review_can_release(self):
        manifest, suite, response, review = self.sample_run()
        write_json(self.root / "cases/C01/response.json", response)
        result = score_run(self.root, suite, manifest, review)
        self.assertEqual(result["score"], 100)
        self.assertTrue(result["release_ready"])

    def test_candidate_cannot_modify_the_packet(self):
        manifest, suite, response, review = self.sample_run()
        write_json(self.root / "cases/C01/response.json", response)
        self.write("PACKET.md", "Changed packet")
        result = score_run(self.root, suite, manifest, review)
        self.assertFalse(result["release_ready"])
        self.assertIn("Evaluation boundary modified: PACKET.md", result["critical_failures"])


class EvidenceExportTests(unittest.TestCase):
    def setUp(self):
        scratch = REPOSITORY / ".temp" / "eval-unit-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temporary.name)
        (self.root / "skills/demo").mkdir(parents=True)
        (self.root / "skills/demo/SKILL.md").write_text("---\nname: demo\ndescription: Demo\n---\n", encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def test_prepare_refuses_reusing_a_run_id(self):
        with contextlib.redirect_stdout(io.StringIO()):
            prepare(self.root, "duplicate")
            with self.assertRaises(FileExistsError):
                prepare(self.root, "duplicate")

    def test_safe_paths_reject_escape_and_windows_drive(self):
        for relative in ["../outside", "C:/outside", "/absolute", "folder/../../escape", "..\\outside"]:
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                safe_child(self.root, relative)

    def test_export_can_be_regraded_and_tampering_is_detected(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run_root = prepare(self.root, "evidence")
            export = self.root / "results/evidence"
            score(run_root, export_path=export)
            verify(export, self.root)
            (export / "score.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hashes"):
                verify(export, self.root)

    def test_candidate_command_receives_packet_and_receipt(self):
        with contextlib.redirect_stdout(io.StringIO()):
            root = prepare(self.root, "command")
        code = "import sys; print('packet-received' if 'Candidate execution packet' in sys.stdin.read() else 'bad')"
        self.assertEqual(execute(root, [sys.executable, "-c", code], 10), 0)
        self.assertIn("packet-received", (root / "control/stdout.txt").read_text())
        self.assertEqual(read_json(root / "control/manifest.json")["execution"]["return_code"], 0)

    def test_candidate_timeout_records_failure(self):
        with contextlib.redirect_stdout(io.StringIO()):
            root = prepare(self.root, "timeout")
        self.assertEqual(execute(root, [sys.executable, "-c", "import time; time.sleep(10)"], 0.1), 1)
        self.assertTrue(read_json(root / "control/manifest.json")["execution"]["timed_out"])


if __name__ == "__main__":
    unittest.main()
