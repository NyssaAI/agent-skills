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
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "evals"))

from cases import build_cases, build_writing_voice_cases, check, note
from calibrate import calibrate, mutations
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

    def test_calendar_history_calibration_detects_lost_payload(self):
        mutation = next(item for item in mutations() if item['id'] == 'lost-calendar-history')
        relative = '2-areas/calendar/we-2026.10.04/2026.09.30-planning.ics'
        candidate = self.root / 'candidate'
        payload = self.write('candidate/cases/C08/workspace/' + relative, 'BEGIN:VCALENDAR\nEND:VCALENDAR\n')
        self.write('candidate/PACKET.md', 'Frozen calendar request')
        self.write('candidate/cases/C08/request.md', 'Retain calendar history')
        assertions = [check('Current payload untouched', 'preservation', 'unchanged', True, path=relative)]
        assertions.extend(check(dimension, dimension, 'unchanged', path=relative)
                          for dimension in ('task', 'metadata', 'navigation'))
        suite = {'version': 'test', 'cases': [{'id': 'C08', 'title': 'Calendar history',
                 'files': {relative: payload.read_text(encoding='utf-8')}, 'checks': assertions}]}
        manifest = {'run_id': 'calendar-history', 'case_ids': ['C08'],
                    'initial_files': inventory(candidate), 'execution': {'kind': 'test'}}
        write_json(self.root / 'control/suite.json', suite)
        write_json(self.root / 'control/manifest.json', manifest)
        write_json(self.root / 'control/review.json', {'reviewer': 'test', 'method': 'artifact review',
                   'cases': {'C08': {'score': 2, 'evidence': 'Native payload retained'}}})
        write_json(candidate / 'cases/C08/response.json', {'case_id': 'C08', 'status': 'completed',
                   'summary': 'Retained calendar history', 'questions': [], 'limitations': [], 'decisions': {}})
        output = self.root / 'calibration.json'
        with patch('calibrate.mutations', return_value=[mutation]), contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(calibrate(self.root, output))
        result = read_json(output)
        self.assertEqual(result['detected'], 1)
        self.assertLessEqual(result['mutations'][0]['score'], 59)
        self.assertTrue(payload.is_file())

    def test_frontmatter_dates_parse_as_dates_without_false_failure(self):
        self.write("note.md", note("Body", created="2026-09-29"))
        assertion = check("Date", "metadata", "frontmatter", path="note.md", fields={"created": "2026-09-29"}, absent=["canonical"])
        self.assertTrue(self.evaluate(assertion))

    def test_maturity_migration_checks_preserve_task_state_and_reject_legacy_alias(self):
        assertion = check("Migrated metadata", "metadata", "frontmatter", path="note.md",
                          fields={"document-maturity": "reviewed", "task-state": "completed"},
                          absent=["status"])
        correct = note("Body", maturity="reviewed", extra="task-state: completed\n")
        self.write("note.md", correct)
        self.assertTrue(self.evaluate(assertion))
        for corrupt in (
            correct.replace("document-maturity:", "status:"),
            correct.replace("document-maturity: reviewed", "document-maturity: completed"),
            correct.replace("task-state: completed", "task-state: reviewed"),
            correct.replace("task-state: completed", "task-state: completed\nstatus: reviewed"),
        ):
            with self.subTest(metadata=corrupt):
                self.write("note.md", corrupt)
                self.assertFalse(self.evaluate(assertion))

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

    def test_malformed_prose_byte_does_not_hide_current_link(self):
        index = self.root / "index.md"
        index.write_bytes(b"Current: [Planning](event.ics)\nHistorical: older\x97invitation\n")
        self.write("event.ics", "BEGIN:VCALENDAR\nEND:VCALENDAR\n")
        assertion = check("Current link", "task", "links_to", source="index.md",
                          target="event.ics", line_prefix="Current:")
        passed, evidence = evaluate_check(assertion, self.root, {}, {})
        self.assertTrue(passed)
        self.assertIn("malformed text replaced", evidence)

    def test_startup_hook_loads_core_in_fresh_project(self):
        project = self.root / "fresh-project"
        project.mkdir()
        (project / ".git").mkdir()
        environment = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(REPOSITORY)}
        command = [sys.executable, str(REPOSITORY / "hooks/session-start.py")]
        first = subprocess.run(command, cwd=project, env=environment,
                               capture_output=True, text=True, check=True)
        core = (REPOSITORY / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
        voice = (REPOSITORY / "rules/writing-voice.md").read_text(encoding="utf-8").strip()
        foundation = core + "\n\n" + voice
        self.assertEqual(first.stdout.strip(), foundation)
        (project / "AGENTS.md").write_text("<!-- agent-skills:file-management:begin -->\n" + core +
                                           "\n<!-- agent-skills:file-management:end -->",
                                           encoding="utf-8")
        second = subprocess.run(command, cwd=project, env=environment,
                                capture_output=True, text=True, check=True)
        self.assertEqual(second.stdout.strip(), foundation)
        (project / "AGENTS.md").write_text("<!-- agent-skills:file-management:begin -->\nStale core.\n"
                                           "<!-- agent-skills:file-management:end -->", encoding="utf-8")
        third = subprocess.run(command, cwd=project, env=environment,
                               capture_output=True, text=True, check=True)
        self.assertEqual(third.stdout.strip(), foundation)
        (project / "AGENTS.md").write_text("<!-- agent-skills:file-management:begin -->\n" + core +
                                           "\n<!-- agent-skills:file-management:end -->",
                                           encoding="utf-8")
        nested = project / "nested"
        nested.mkdir()
        inherited = subprocess.run(command, cwd=nested, env=environment,
                                   capture_output=True, text=True, check=True)
        self.assertEqual(inherited.stdout.strip(), foundation)
        (project / "AGENTS.md").write_text("<!-- agent-skills:file-management:begin -->\nStale core.\n"
                                           "<!-- agent-skills:file-management:end -->", encoding="utf-8")
        stale_inherited = subprocess.run(command, cwd=nested, env=environment,
                                        capture_output=True, text=True, check=True)
        self.assertEqual(stale_inherited.stdout.strip(), foundation)

    def test_startup_hook_loads_core_when_project_instructions_may_not_load_agents(self):
        core = (REPOSITORY / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
        voice = (REPOSITORY / "rules/writing-voice.md").read_text(encoding="utf-8").strip()
        foundation = core + "\n\n" + voice
        block = "<!-- agent-skills:file-management:begin -->\n" + core + "\n<!-- agent-skills:file-management:end -->"
        for instruction_file, root_variable in (
            ("CLAUDE.md", "CLAUDE_PLUGIN_ROOT"),
            ("AGENTS.override.md", "PLUGIN_ROOT"),
        ):
            with self.subTest(instruction_file=instruction_file):
                project = self.root / instruction_file.removesuffix(".md")
                project.mkdir()
                (project / ".git").mkdir()
                (project / "AGENTS.md").write_text(block, encoding="utf-8")
                (project / instruction_file).write_text("# Project instructions\n", encoding="utf-8")
                environment = {key: value for key, value in os.environ.items()
                               if key not in {"CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT"}}
                environment[root_variable] = str(REPOSITORY)
                result = subprocess.run([sys.executable, str(REPOSITORY / "hooks/session-start.py")],
                                        cwd=project, env=environment,
                                        capture_output=True, text=True, check=True)
                self.assertEqual(result.stdout.strip(), foundation)

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


class WritingVoiceScaffoldTests(unittest.TestCase):
    def test_voice_corpus_does_not_extend_frozen_file_suite(self):
        self.assertEqual([item["id"] for item in build_cases()], [f"C{i:02}" for i in range(1, 25)])
        self.assertEqual([item["id"] for item in build_writing_voice_cases()],
                         [f"WV{i:02}" for i in range(1, 7)])

    def test_tessl_fixtures_match_independent_corpus_and_rubrics(self):
        root = REPOSITORY / "evals/tessl/writing-voice"
        scenarios = sorted((root / "performance").glob("*/scenario.json"))
        self.assertEqual(len(scenarios), 6)
        cases = {item["title"]: item for item in build_writing_voice_cases()}
        for scenario in scenarios:
            data = read_json(scenario)
            item = cases.pop(data["description"])
            fixture = scenario.parent / data["fixtures"]["workspace"]["path"]
            actual = {path.relative_to(fixture).as_posix(): path.read_text(encoding="utf-8")
                      for path in fixture.rglob("*") if path.is_file()}
            self.assertEqual(actual, item["files"])
            self.assertIn(item["prompt"], (scenario.parent / "task.md").read_text(encoding="utf-8"))
            rubric = read_json(scenario.parent / "criteria.json")
            self.assertEqual(rubric["type"], "weighted_checklist")
            self.assertEqual(sum(row["max_score"] for row in rubric["checklist"]), 10)
        self.assertFalse(cases)
        controls = {path.parent.name for path in (root / "activation-only").glob("*/scenario.json")}
        self.assertEqual(controls, {"maintain-preference", "apply-profile", "unrelated-explanation",
                                    "third-party-house-style"})
        for scenario in (root / "activation-only").glob("*/scenario.json"):
            data = read_json(scenario)
            fixture = scenario.parent / data["fixtures"]["workspace"]["path"]
            self.assertTrue((fixture / ".nyssa-ai/agent-skills/writing-voice/VOICE.md").is_file())
            rubric = read_json(scenario.parent / "criteria.json")
            self.assertEqual(rubric["type"], "weighted_checklist")
            self.assertEqual(sum(row["max_score"] for row in rubric["checklist"]), 1)
            self.assertTrue((scenario.parent / "task.md").is_file())

    def test_drafting_preservation_detects_profile_and_example_mutation(self):
        item = next(item for item in build_writing_voice_cases() if item["id"] == "WV02")
        scratch = REPOSITORY / ".temp/eval-unit-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            workspace = Path(temporary)
            for relative, content in item["files"].items():
                path = workspace / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
            assertions = [row for row in item["checks"] if row["operation"] == "unchanged"]
            for assertion in assertions:
                self.assertTrue(evaluate_check(assertion, workspace, item["files"], {})[0])
                path = workspace / assertion["path"]
                path.write_text("Unauthorized learned preference.\n", encoding="utf-8")
                self.assertFalse(evaluate_check(assertion, workspace, item["files"], {})[0])
                path.write_text(item["files"][assertion["path"]], encoding="utf-8", newline="\n")

    def test_privacy_checks_require_both_narrow_exclusions(self):
        scratch = REPOSITORY / ".temp/eval-unit-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            workspace = Path(temporary)
            for item in build_writing_voice_cases():
                if item["id"] not in {"WV01", "WV03"}:
                    continue
                assertion = next(row for row in item["checks"]
                                 if row["label"] == "Narrow exclusions and existing rule retained")
                path = workspace / ".gitignore"
                correct = "/build/\n/.nyssa-ai/agent-skills/writing-voice/\n/.temp/agent-skills/writing-voice/\n"
                path.write_text(correct, encoding="utf-8")
                self.assertTrue(evaluate_check(assertion, workspace, item["files"], {})[0])
                for corrupt in (
                    correct.replace("/.temp/agent-skills/writing-voice/\n", ""),
                    correct.replace("/.nyssa-ai/agent-skills/writing-voice/", "/.nyssa-ai/"),
                    correct.replace("/build/\n", ""),
                ):
                    path.write_text(corrupt, encoding="utf-8")
                    self.assertFalse(evaluate_check(assertion, workspace, item["files"], {})[0])


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
