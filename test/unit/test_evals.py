"""Evaluation tests — challenge grading with correct, corrupt, missing, and unsafe artifacts."""

import contextlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY / "evals"))

from cases import build_cases, build_writing_voice_cases, check, note
from calibrate import calibrate, mutations
from plugin_checks import validate_evals_directory, validate_plugin
import report
from run import execute, file_hash, inventory, prepare, read_json, safe_child, score, suite_definition, verify, write_json
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

    def test_validate_plugin_passes_for_repository(self):
        result = validate_plugin(REPOSITORY)
        self.assertTrue(result["passed"], f"Plugin validation findings: {result['findings']}")
        self.assertEqual(result["findings"], [])

    def test_validate_plugin_enforces_host_manifest_parity_license_changelog_and_single_skill_version(self):
        import shutil

        fixture = self.root / "repo-copy"
        fixture.mkdir()
        for rel_dir in (
            "docs",
            "skills",
            "rules",
            "hooks",
            "harness-adapters",
            "scripts",
            ".claude-plugin",
            ".codex-plugin",
            ".cursor-plugin",
            ".tessl-plugin",
        ):
            shutil.copytree(
                REPOSITORY / rel_dir,
                fixture / rel_dir,
                ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".temp", ".nyssa-ai"),
            )
        for rel_file in ("plugin.json", "gemini-extension.json", "hooks.json", "LICENSE", "CHANGELOG.md", ".gitattributes"):
            shutil.copy2(REPOSITORY / rel_file, fixture / rel_file)

        baseline = validate_plugin(fixture)
        self.assertTrue(baseline["passed"], baseline["findings"])

        for manifest_rel in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
            original_text = (fixture / manifest_rel).read_text(encoding="utf-8")
            for field, mutated_value in (
                ("homepage", "https://example.invalid/drift"),
                ("repository", "https://example.invalid/drift-repo"),
                ("license", "MIT"),
                ("author", {"name": "DriftAuthor"}),
                ("keywords", ["drift"]),
            ):
                mutated = json.loads(original_text)
                mutated[field] = mutated_value
                (fixture / manifest_rel).write_text(json.dumps(mutated, indent=2) + "\n", encoding="utf-8")
                drift_result = validate_plugin(fixture)
                self.assertFalse(drift_result["passed"])
                self.assertIn(f"{manifest_rel} {field} differs from root plugin.json", drift_result["findings"])
            (fixture / manifest_rel).write_text(original_text, encoding="utf-8")

        # Duplicate metadata.version in SKILL.md must be rejected
        skill_path = fixture / "skills" / "manage-file-operations" / "SKILL.md"
        original_skill = skill_path.read_text(encoding="utf-8")
        head, tail = original_skill.split("\n---\n", 1)
        skill_path.write_text(f'{head}\nmetadata:\n  version: "0.7.3"\n---\n{tail}', encoding="utf-8")
        dup_version = validate_plugin(fixture)
        self.assertFalse(dup_version["passed"])
        self.assertTrue(any("duplicate metadata.version" in item for item in dup_version["findings"]))
        skill_path.write_text(original_skill, encoding="utf-8")

        # Stale MIT LICENSE or missing CHANGELOG.md must be rejected
        (fixture / "LICENSE").write_text("MIT License\n", encoding="utf-8")
        (fixture / "CHANGELOG.md").unlink()
        stale_lic = validate_plugin(fixture)
        self.assertFalse(stale_lic["passed"])
        self.assertIn("LICENSE must contain the canonical NyssaAI Apache License 2.0 text", stale_lic["findings"])
        self.assertIn("Missing tracked release history: CHANGELOG.md", stale_lic["findings"])

    def test_validate_plugin_enforces_layout_lockdown_verification_sections_and_path_leak_ban(self):
        import shutil

        fixture = self.root / "layout-copy"
        fixture.mkdir()
        for rel_dir in (
            "docs",
            "skills",
            "rules",
            "hooks",
            "harness-adapters",
            "scripts",
            ".claude-plugin",
            ".codex-plugin",
            ".cursor-plugin",
            ".tessl-plugin",
        ):
            shutil.copytree(
                REPOSITORY / rel_dir,
                fixture / rel_dir,
                ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".temp", ".nyssa-ai"),
            )
        for rel_file in ("plugin.json", "gemini-extension.json", "hooks.json", "LICENSE", "CHANGELOG.md", ".gitattributes"):
            shutil.copy2(REPOSITORY / rel_file, fixture / rel_file)

        # Stdlib YAML fallback must validate the repository cleanly without PyYAML
        with patch("plugin_checks.yaml", None):
            fallback_result = validate_plugin(REPOSITORY)
        self.assertTrue(fallback_result["passed"], fallback_result["findings"])

        # scripts/validate.py CLI entrypoint must pass on valid repo and fail on invalid repo
        cli_ok = subprocess.run(
            [sys.executable, str(REPOSITORY / "scripts" / "validate.py"), str(fixture)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(cli_ok.returncode, 0, cli_ok.stdout + cli_ok.stderr)
        self.assertTrue(json.loads(cli_ok.stdout)["passed"])

        # 1. Top-level directory & loose root file allowlist
        (fixture / "rogue-dir").mkdir()
        (fixture / "rogue.txt").write_text("loose\n", encoding="utf-8")
        rogue_res = validate_plugin(fixture)
        self.assertFalse(rogue_res["passed"])
        self.assertIn("Unexpected top-level directory in repo_root: rogue-dir/", rogue_res["findings"])
        self.assertIn("Unexpected loose root file in repo_root: rogue.txt", rogue_res["findings"])
        cli_fail = subprocess.run(
            [sys.executable, str(REPOSITORY / "scripts" / "validate.py"), str(fixture)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(cli_fail.returncode, 0)
        (fixture / "rogue-dir").rmdir()
        (fixture / "rogue.txt").unlink()

        # 2. .gitattributes LF check
        orig_gitattr = (fixture / ".gitattributes").read_text(encoding="utf-8")
        (fixture / ".gitattributes").write_text("* text=auto\n", encoding="utf-8")
        no_lf = validate_plugin(fixture)
        self.assertFalse(no_lf["passed"])
        self.assertIn(".gitattributes must enforce LF line endings (eol=lf)", no_lf["findings"])
        (fixture / ".gitattributes").unlink()
        missing_gitattr = validate_plugin(fixture)
        self.assertFalse(missing_gitattr["passed"])
        self.assertIn("Missing .gitattributes with LF line-ending normalization (eol=lf)", missing_gitattr["findings"])
        (fixture / ".gitattributes").write_text(orig_gitattr, encoding="utf-8")

        # 3. docs/ Allowed-Set Lockdown & not gitignored
        (fixture / ".gitignore").write_text("docs/\n", encoding="utf-8")
        (fixture / "docs" / "roadmap.md").write_text("# Disallowed\n", encoding="utf-8")
        (fixture / "docs" / "reviews").mkdir()
        (fixture / "docs" / "specs").mkdir()
        (fixture / "docs" / "specs" / "prose.md").write_text("# Disallowed\n", encoding="utf-8")
        docs_res = validate_plugin(fixture)
        self.assertFalse(docs_res["passed"])
        self.assertIn("docs/ directory must not be gitignored", docs_res["findings"])
        self.assertTrue(any("Disallowed file in docs/: docs/roadmap.md" in f for f in docs_res["findings"]))
        self.assertTrue(any("Disallowed directory in docs/: docs/reviews/" in f for f in docs_res["findings"]))
        self.assertTrue(any("Disallowed prose markdown in docs/specs/: docs/specs/prose.md" in f for f in docs_res["findings"]))
        (fixture / ".gitignore").unlink()
        (fixture / "docs" / "roadmap.md").unlink()
        shutil.rmtree(fixture / "docs" / "reviews")
        shutil.rmtree(fixture / "docs" / "specs")

        # 4. test/ isolation
        (fixture / "test" / "unit").mkdir(parents=True)
        (fixture / "test" / "test_loose.py").write_text("def test_x(): pass\n", encoding="utf-8")
        (fixture / "test" / "integration").mkdir()
        (fixture / "skills" / "test_stray.py").write_text("def test_y(): pass\n", encoding="utf-8")
        test_res = validate_plugin(fixture)
        self.assertFalse(test_res["passed"])
        self.assertTrue(any("Loose file in test/ root: test/test_loose.py" in f for f in test_res["findings"]))
        self.assertTrue(any("Non-canonical test subdirectory: test/integration/" in f for f in test_res["findings"]))
        self.assertTrue(any("Co-mingled test file outside test/: skills/test_stray.py" in f for f in test_res["findings"]))
        shutil.rmtree(fixture / "test")
        (fixture / "skills" / "test_stray.py").unlink()

        # 5. Scope Directive & ## Verification check
        wf_path = fixture / "skills" / "para-vault" / "workflows" / "archive.md"
        orig_wf = wf_path.read_text(encoding="utf-8")
        wf_path.write_text(
            orig_wf.replace("> [!IMPORTANT] Scope Directive", "> Note").replace("## Verification", "## Summary"),
            encoding="utf-8",
        )
        ref_path = fixture / "skills" / "para-vault" / "references" / "lifecycle.md"
        orig_ref = ref_path.read_text(encoding="utf-8")
        ref_path.write_text(orig_ref.replace("> [!IMPORTANT] Scope Directive", "> Note"), encoding="utf-8")
        scope_res = validate_plugin(fixture)
        self.assertFalse(scope_res["passed"])
        self.assertIn(
            "skills/para-vault/workflows/archive.md: missing '> [!IMPORTANT] Scope Directive'",
            scope_res["findings"],
        )
        self.assertIn(
            "skills/para-vault/workflows/archive.md: missing '## Verification' section",
            scope_res["findings"],
        )
        self.assertIn(
            "skills/para-vault/references/lifecycle.md: missing '> [!IMPORTANT] Scope Directive'",
            scope_res["findings"],
        )
        wf_path.write_text(orig_wf, encoding="utf-8")
        ref_path.write_text(orig_ref, encoding="utf-8")

        # 6. Machine-local path leak ban across skills/, rules/, and hooks/
        hook_path = fixture / "hooks" / "session-start.py"
        orig_hook = hook_path.read_text(encoding="utf-8")
        hook_path.write_text(
            orig_hook
            + "\n# /srv/repos/NyssaAI/agent-skills\n"
            + "# /root/.gemini/antigravity-cli/brain/123\n"
            + "# C:\\Users\\dev\\secret\n",
            encoding="utf-8",
        )
        leak_res = validate_plugin(fixture)
        self.assertFalse(leak_res["passed"])
        self.assertIn("hooks/session-start.py: leaked machine-local path (/srv/repos/NyssaAI/)", leak_res["findings"])
        self.assertIn(
            "hooks/session-start.py: leaked machine-local path (/root/.gemini/antigravity-cli/brain/)",
            leak_res["findings"],
        )
        self.assertIn("hooks/session-start.py: leaked machine-local path (C:\\Users\\)", leak_res["findings"])
        hook_path.write_text(orig_hook, encoding="utf-8")
        self.assertTrue(validate_plugin(fixture)["passed"])

    def test_native_preservation_detects_content_changes(self):
        self.write("record.ics", "BEGIN:VCALENDAR\nEND:VCALENDAR\n")
        assertion = check("Native bytes", "preservation", "same_as", True, path="record.ics", source="source.ics")
        original = {"source.ics": "BEGIN:VCALENDAR\nEND:VCALENDAR\n"}
        self.assertTrue(self.evaluate(assertion, original))
        self.write("record.ics", "---\ntype: note\n---\nBEGIN:VCALENDAR\nEND:VCALENDAR\n")
        self.assertFalse(self.evaluate(assertion, original))

    def test_custom_email_destination_preserves_native_record_without_redundant_archive(self):
        case = next(item for item in build_cases() if item["id"] == "C05")
        assertion = next(item for item in case["checks"] if item["label"] == "Native original preserved")
        target = "Work/launch/evidence/approval.eml"
        self.write(target, case["files"]["Capture/approval.eml"])
        self.assertTrue(self.evaluate(assertion, case["files"]))
        self.write(target, "Changed native message")
        self.assertFalse(self.evaluate(assertion, case["files"]))

    def test_calendar_history_calibration_detects_lost_payload(self):
        mutation = next(item for item in mutations() if item["id"] == "lost-calendar-history")
        relative = "2-areas/calendar/we-2026.10.04/2026.09.30-planning.ics"
        candidate = self.root / "candidate"
        payload = self.write("candidate/cases/C08/workspace/" + relative, "BEGIN:VCALENDAR\nEND:VCALENDAR\n")
        self.write("candidate/PACKET.md", "Frozen calendar request")
        self.write("candidate/cases/C08/request.md", "Retain calendar history")
        assertions = [check("Current payload untouched", "preservation", "unchanged", True, path=relative)]
        assertions.extend(
            check(dimension, dimension, "unchanged", path=relative)
            for dimension in ("task", "metadata", "navigation")
        )
        suite = {
            "version": "test",
            "cases": [
                {
                    "id": "C08",
                    "title": "Calendar history",
                    "files": {relative: payload.read_text(encoding="utf-8")},
                    "checks": assertions,
                }
            ],
        }
        manifest = {
            "run_id": "calendar-history",
            "case_ids": ["C08"],
            "initial_files": inventory(candidate),
            "execution": {"kind": "test"},
        }
        write_json(self.root / "control/suite.json", suite)
        write_json(self.root / "control/manifest.json", manifest)
        write_json(
            self.root / "control/review.json",
            {
                "reviewer": "test",
                "method": "artifact review",
                "cases": {"C08": {"score": 2, "evidence": "Native payload retained"}},
            },
        )
        write_json(
            candidate / "cases/C08/response.json",
            {
                "case_id": "C08",
                "status": "completed",
                "summary": "Retained calendar history",
                "questions": [],
                "limitations": [],
                "decisions": {},
            },
        )
        output = self.root / "calibration.json"
        with patch("calibrate.mutations", return_value=[mutation]), contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(calibrate(self.root, output))
        result = read_json(output)
        self.assertEqual(result["detected"], 1)
        self.assertLessEqual(result["mutations"][0]["score"], 59)
        self.assertTrue(payload.is_file())

    def test_frontmatter_dates_parse_as_dates_without_false_failure(self):
        self.write("note.md", note("Body", created="2026-09-29"))
        assertion = check(
            "Date",
            "metadata",
            "frontmatter",
            path="note.md",
            fields={"created": "2026-09-29"},
            absent=["canonical"],
        )
        self.assertTrue(self.evaluate(assertion))

    def test_maturity_migration_checks_preserve_state_and_reject_legacy_alias(self):
        assertion = check(
            "Migrated metadata",
            "metadata",
            "frontmatter",
            path="note.md",
            fields={"document-maturity": "reviewed", "state": "completed"},
            absent=["status", "task-state"],
        )
        correct = note("Body", maturity="reviewed", extra="state: completed\n")
        self.write("note.md", correct)
        self.assertTrue(self.evaluate(assertion))
        for corrupt in (
            correct.replace("document-maturity:", "status:"),
            correct.replace("document-maturity: reviewed", "document-maturity: completed"),
            correct.replace("state: completed", "state: reviewed"),
            correct.replace("state: completed", "task-state: completed"),
            correct.replace("state: completed", "state: completed\nstatus: reviewed"),
        ):
            with self.subTest(metadata=corrupt):
                self.write("note.md", corrupt)
                self.assertFalse(self.evaluate(assertion))

    def test_project_cases_use_daily_tasks_project_index_and_state(self):
        c02 = next(item for item in build_cases() if item["id"] == "C02")
        schema_check = next(row for row in c02["checks"] if row["label"] == "Project schema")
        self.assertEqual(schema_check["path"], "1-projects/2026.09.29-payroll-migration/project-index.md")
        self.assertEqual(schema_check["fields"], {"type": "project", "state": "not-started"})
        self.assertIn("task-state", schema_check["absent"])

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
        self.write("index.md", "[[1-projects/2026.09.29-payroll/project-index]]")
        self.write("1-projects/2026.09.29-payroll/project-index.md", "# Project")
        self.assertTrue(self.evaluate(check("Links", "navigation", "links_valid", glob="index.md")))

    def test_malformed_prose_byte_does_not_hide_current_link(self):
        index = self.root / "index.md"
        index.write_bytes(b"Current: [Planning](event.ics)\nHistorical: older\x97invitation\n")
        self.write("event.ics", "BEGIN:VCALENDAR\nEND:VCALENDAR\n")
        assertion = check(
            "Current link",
            "task",
            "links_to",
            source="index.md",
            target="event.ics",
            line_prefix="Current:",
        )
        passed, evidence = evaluate_check(assertion, self.root, {}, {})
        self.assertTrue(passed)
        self.assertIn("malformed text replaced", evidence)

    def test_startup_hook_loads_core_in_fresh_project(self):
        project = self.root / "fresh-project"
        project.mkdir()
        (project / ".git").mkdir()
        environment = {**os.environ, "CLAUDE_PLUGIN_ROOT": str(REPOSITORY)}
        command = [sys.executable, str(REPOSITORY / "hooks/session-start.py")]
        first = subprocess.run(command, cwd=project, env=environment, capture_output=True, text=True, check=True)
        core = (REPOSITORY / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
        voice = re.sub(
            r"\A---\r?\n.*?\r?\n---\r?\n*",
            "",
            (REPOSITORY / "rules/writing-voice.md").read_text(encoding="utf-8"),
            flags=re.S,
        ).strip()
        foundation = core + "\n\n" + voice
        self.assertEqual(first.stdout.strip(), foundation)
        self.assertNotIn("trigger: always_on", first.stdout)
        (project / "AGENTS.md").write_text(
            "<!-- agent-skills:file-management:begin -->\n" + core + "\n<!-- agent-skills:file-management:end -->",
            encoding="utf-8",
        )
        second = subprocess.run(command, cwd=project, env=environment, capture_output=True, text=True, check=True)
        self.assertEqual(second.stdout.strip(), foundation)
        (project / "AGENTS.md").write_text(
            "<!-- agent-skills:file-management:begin -->\nStale core.\n<!-- agent-skills:file-management:end -->",
            encoding="utf-8",
        )
        third = subprocess.run(command, cwd=project, env=environment, capture_output=True, text=True, check=True)
        self.assertEqual(third.stdout.strip(), foundation)
        (project / "AGENTS.md").write_text(
            "<!-- agent-skills:file-management:begin -->\n" + core + "\n<!-- agent-skills:file-management:end -->",
            encoding="utf-8",
        )
        nested = project / "nested"
        nested.mkdir()
        inherited = subprocess.run(command, cwd=nested, env=environment, capture_output=True, text=True, check=True)
        self.assertEqual(inherited.stdout.strip(), foundation)
        (project / "AGENTS.md").write_text(
            "<!-- agent-skills:file-management:begin -->\nStale core.\n<!-- agent-skills:file-management:end -->",
            encoding="utf-8",
        )
        stale_inherited = subprocess.run(
            command, cwd=nested, env=environment, capture_output=True, text=True, check=True
        )
        self.assertEqual(stale_inherited.stdout.strip(), foundation)

    def test_startup_hook_loads_core_when_project_instructions_may_not_load_agents(self):
        core = (REPOSITORY / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
        voice = re.sub(
            r"\A---\r?\n.*?\r?\n---\r?\n*",
            "",
            (REPOSITORY / "rules/writing-voice.md").read_text(encoding="utf-8"),
            flags=re.S,
        ).strip()
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
                environment = {
                    key: value
                    for key, value in os.environ.items()
                    if key not in {"CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT"}
                }
                environment[root_variable] = str(REPOSITORY)
                result = subprocess.run(
                    [sys.executable, str(REPOSITORY / "hooks/session-start.py")],
                    cwd=project,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.assertEqual(result.stdout.strip(), foundation)

    def sample_run(self):
        self.write("PACKET.md", "Frozen packet")
        self.write("cases/C01/request.md", "Frozen request")
        self.write("cases/C01/workspace/record.txt", "Evidence")
        manifest = {
            "run_id": "sample",
            "case_ids": ["C01"],
            "initial_files": inventory(self.root),
            "execution": {"kind": "test"},
        }
        assertions = [
            check(dimension, dimension, "unchanged", dimension == "preservation", path="record.txt")
            for dimension in ["task", "preservation", "metadata", "navigation"]
        ]
        suite = {
            "version": "test",
            "cases": [{"id": "C01", "title": "Sample", "files": {"record.txt": "Evidence"}, "checks": assertions}],
        }
        response = {
            "case_id": "C01",
            "status": "completed",
            "summary": "Retained evidence",
            "questions": [],
            "limitations": [],
            "decisions": {},
        }
        review = {
            "reviewer": "test",
            "method": "artifact review",
            "cases": {"C01": {"score": 2, "evidence": "Verified retained evidence"}},
        }
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

    def test_voice_dimensions_can_earn_full_score_without_unrelated_file_metadata(self):
        manifest, suite, response, review = self.sample_run()
        suite["dimension_weights"] = {"task": 52.5, "preservation": 37.5}
        suite["cases"][0]["checks"] = suite["cases"][0]["checks"][:2]
        write_json(self.root / "cases/C01/response.json", response)
        result = score_run(self.root, suite, manifest, review)
        self.assertEqual(result["score"], 100)
        self.assertTrue(result["release_ready"])

    def test_custom_dimensions_cannot_omit_checks_or_reduce_the_score_denominator(self):
        manifest, suite, response, review = self.sample_run()
        write_json(self.root / "cases/C01/response.json", response)
        for weights in ({"task": 90}, {"task": 35, "preservation": 25}, {"task": True}):
            suite["dimension_weights"] = weights
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                score_run(self.root, suite, manifest, review)

    def test_candidate_cannot_modify_the_packet(self):
        manifest, suite, response, review = self.sample_run()
        write_json(self.root / "cases/C01/response.json", response)
        self.write("PACKET.md", "Changed packet")
        result = score_run(self.root, suite, manifest, review)
        self.assertFalse(result["release_ready"])
        self.assertIn("Evaluation boundary modified: PACKET.md", result["critical_failures"])

    def test_required_independent_review_rejects_failed_partial_or_missing_annotations(self):
        manifest, suite, response, review = self.sample_run()
        suite["critical_review_cases"] = ["C01"]
        write_json(self.root / "cases/C01/response.json", response)
        for annotation in (
            {"score": 0, "evidence": "Wrong activation"},
            {"score": 1, "evidence": "Partial provenance"},
            {"score": 2, "evidence": " "},
            {},
            {"score": True, "evidence": "Invalid score type"},
        ):
            with self.subTest(annotation=annotation):
                review["cases"]["C01"] = annotation
                result = score_run(self.root, suite, manifest, review)
                self.assertEqual(result["automatic_score_out_of_90"], 90)
                self.assertFalse(result["release_ready"])
                self.assertTrue(any("C01: Required independent review" in row for row in result["critical_failures"]))
        result = score_run(self.root, suite, manifest)
        self.assertFalse(result["release_ready"])
        self.assertTrue(result["critical_failures"])

    def test_required_independent_review_allows_full_review_and_preserves_default_scoring(self):
        manifest, suite, response, review = self.sample_run()
        write_json(self.root / "cases/C01/response.json", response)
        suite["critical_review_cases"] = ["C01"]
        self.assertTrue(score_run(self.root, suite, manifest, review)["release_ready"])
        del suite["critical_review_cases"]
        review["cases"]["C01"]["score"] = 0
        result = score_run(self.root, suite, manifest, review)
        self.assertEqual(result["score"], 90)
        self.assertTrue(result["release_ready"])
        self.assertFalse(result["critical_failures"])

    def test_required_independent_review_ids_must_be_unique_known_case_ids(self):
        manifest, suite, response, review = self.sample_run()
        write_json(self.root / "cases/C01/response.json", response)
        for ids in (["C01", "C01"], ["unknown"], "C01", None, [True], [[]]):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                suite["critical_review_cases"] = ids
                score_run(self.root, suite, manifest, review)

    def test_atomic_project_override_rejects_user_and_merged_drafts(self):
        from configuration_cases import build_voice_scope_cases
        item = next(item for item in build_voice_scope_cases() if item["id"] == "SC02")
        manifest, _, response, review = self.sample_run()
        case_root = self.root / "cases/SC02"
        for relative, content in item["files"].items():
            self.write("cases/SC02/workspace/" + relative, content)
        manifest["case_ids"] = ["C01", "SC02"]
        manifest["initial_files"] = inventory(self.root)
        response["case_id"] = "SC02"
        write_json(case_root / "response.json", response)
        review["cases"] = {"SC02": {"score": 2, "evidence": "Verified project-only provenance"}}
        suite = {
            "version": "test",
            "cases": [item],
            "dimension_weights": {"task": 52.5, "preservation": 37.5},
            "critical_review_cases": ["SC02"],
        }
        user = item["files"]["home/.nyssa-ai/agent-skills/writing-voice/VOICE.md"]
        project = item["files"]["project-a/.nyssa-ai/agent-skills/writing-voice/VOICE.md"]
        self.assertNotEqual(user, project)
        self.assertIn("HOME-MARKER", user)
        self.assertIn("PROJECT-MARKER", project)
        for signoff, accepted in (
            ("PROJECT-MARKER", True),
            ("HOME-MARKER", False),
            ("PROJECT-MARKER HOME-MARKER", False),
            ("PROJECT-MARKER home-marker", False),
        ):
            with self.subTest(signoff=signoff):
                self.write("cases/SC02/workspace/project-a/message.md", "Rowan, please review by Friday.\n" + signoff)
                result = score_run(self.root, suite, manifest, review)
                self.assertEqual(result["release_ready"], accepted)
                self.assertEqual(bool(result["critical_failures"]), not accepted)

    def test_sc05_ignores_retired_nyssaai_directory(self):
        from configuration_cases import build_voice_scope_cases
        item = next(item for item in build_voice_scope_cases() if item["id"] == "SC05")
        self.assertEqual(item["title"], "Retired legacy directory ignored")
        self.assertEqual(item["entry_skill"], "write-like-me")
        labels = {row["label"] for row in item["checks"]}
        self.assertIn("Missing canonical profile disclosed", labels)


class WritingVoiceScaffoldTests(unittest.TestCase):
    def test_voice_suite_requires_full_activation_and_atomic_provenance_review(self):
        self.assertEqual(
            suite_definition("writing-voice")["critical_review_cases"],
            ["SC02", "AC01", "AC02", "AC03", "AC04"],
        )
        self.assertNotIn("critical_review_cases", suite_definition("file-and-para-24"))

    def test_unrelated_explanation_accepts_a_nonempty_string_summary(self):
        from configuration_cases import build_voice_activation_cases
        item = next(item for item in build_voice_activation_cases() if item["id"] == "AC04")
        assertion = next(row for row in item["checks"] if row["label"] == "Explanation")
        self.assertTrue(evaluate_check(assertion, REPOSITORY, {}, {"summary": "Rain forms from cooling moist air."})[0])
        self.assertFalse(evaluate_check(assertion, REPOSITORY, {}, {"summary": " "})[0])

    def test_voice_corpus_does_not_extend_frozen_file_suite(self):
        self.assertEqual([item["id"] for item in build_cases()], [f"C{i:02}" for i in range(1, 25)])
        self.assertEqual([item["id"] for item in build_writing_voice_cases()], [f"WV{i:02}" for i in range(1, 7)])

    def test_tessl_fixtures_match_independent_corpus_and_rubrics(self):
        root = REPOSITORY / "evals/tessl/writing-voice"
        scenarios = sorted((root / "performance").glob("*/scenario.json"))
        self.assertEqual(len(scenarios), 6)
        cases = {item["title"]: item for item in build_writing_voice_cases()}
        for scenario in scenarios:
            data = read_json(scenario)
            item = cases.pop(data["description"])
            fixture = scenario.parent / data["fixtures"]["workspace"]["path"]
            actual = {
                path.relative_to(fixture).as_posix(): path.read_text(encoding="utf-8")
                for path in fixture.rglob("*")
                if path.is_file()
            }
            self.assertEqual(actual, item["files"])
            self.assertIn(item["prompt"], (scenario.parent / "task.md").read_text(encoding="utf-8"))
            rubric = read_json(scenario.parent / "criteria.json")
            self.assertEqual(rubric["type"], "weighted_checklist")
            self.assertEqual(sum(row["max_score"] for row in rubric["checklist"]), 10)
        self.assertFalse(cases)
        controls = {path.parent.name for path in (root / "activation-only").glob("*/scenario.json")}
        self.assertEqual(
            controls,
            {"maintain-preference", "apply-profile", "unrelated-explanation", "third-party-house-style"},
        )
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
                assertion = next(
                    row for row in item["checks"] if row["label"] == "Narrow exclusions and existing rule retained"
                )
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
            export = self.root / ".temp/evals/results/evidence"
            score(run_root, export_path=export)
            verify(export, self.root)
            (export / "score.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hashes"):
                verify(export, self.root)

    def test_unknown_historical_revision_rejects_before_execution(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run_root = prepare(self.root, "unknown-revision")
            export = self.root / ".temp/evals/results/unknown"
            score(run_root, export_path=export)
            write_json(
                export / "metadata.json",
                {
                    "key": ["file-and-para-24"],
                    "suite_revision": "untrusted",
                    "suite_sha256": file_hash(export / "suite.json"),
                },
            )
            definitions = self.root / "evals/verifiers"
            definitions.mkdir(parents=True)
            write_json(definitions / "revisions.json", {"revisions": []})
            hashes = inventory(export)
            hashes.pop("artifact-hashes.json")
            write_json(export / "artifact-hashes.json", hashes)
            with self.assertRaisesRegex(ValueError, "Unknown trusted verifier"):
                verify(export, self.root)

    def test_voice_preparation_has_fresh_scope_fixtures_and_replay(self):
        with contextlib.redirect_stdout(io.StringIO()):
            root = prepare(self.root, "voice", "writing-voice")
            suite = read_json(root / "control/suite.json")
            self.assertEqual(len(suite["cases"]), 15)
            self.assertTrue(
                (root / "candidate/cases/SC01/workspace/home/.nyssa-ai/agent-skills/writing-voice/VOICE.md").is_file()
            )
            export = self.root / ".temp/evals/results/voice"
            score(root, export_path=export)
            verify(export, self.root)

    def test_historical_export_rejects_rehashed_untrusted_grader(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run_root = prepare(self.root, "rehashed-history")
            export = self.root / ".temp/evals/results/rehashed-history"
            score(run_root, export_path=export)
            suite_sha = file_hash(export / "suite.json")
            trusted_files = read_json(export / "grader-files.json")
            write_json(
                export / "metadata.json",
                {
                    "key": ["file-and-para-24"],
                    "suite_revision": "0.6.0-fixture",
                    "suite_sha256": suite_sha,
                },
            )
            definitions = self.root / "evals/verifiers"
            definitions.mkdir(parents=True, exist_ok=True)
            write_json(
                definitions / "revisions.json",
                {
                    "revisions": [
                        {
                            "suite": "file-and-para-24",
                            "revision": "0.6.0-fixture",
                            "suite_sha256": suite_sha,
                            "grader_directory": ".",
                            "grader_files": dict(trusted_files),
                        }
                    ]
                },
            )
            tampered_files = dict(trusted_files)
            tampered_files["run.py"] = "0" * 64
            write_json(export / "grader-files.json", tampered_files)
            hashes = inventory(export)
            hashes.pop("artifact-hashes.json")
            write_json(export / "artifact-hashes.json", hashes)
            with self.assertRaisesRegex(ValueError, "trusted revision"):
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


class WazaAndReportIntegrityTests(unittest.TestCase):
    def setUp(self):
        scratch = REPOSITORY / ".temp" / "eval-unit-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def _write_valid_evals_fixture(self) -> None:
        (self.root / "skills" / "demo").mkdir(parents=True, exist_ok=True)
        (self.root / "skills" / "demo" / "SKILL.md").write_text(
            "---\nname: demo\ndescription: Demo skill\n---\n",
            encoding="utf-8",
        )
        evals_dir = self.root / "evals"
        evals_dir.mkdir(parents=True, exist_ok=True)
        (evals_dir / "README.md").write_text("# Evals\n", encoding="utf-8")
        (evals_dir / "LATEST.md").write_text("# Latest plugin evaluation\n\n`demo-run-01`\n", encoding="utf-8")
        write_json(
            evals_dir / "matrix.json",
            {
                "schema": 1,
                "suite_revision": "1.0-test",
                "rows": [
                    {
                        "suite": "file-and-para-24",
                        "harness": "Codex",
                        "platform": "windows-x86_64",
                        "config": "default",
                        "required": True,
                        "remaining": "Run cases.",
                    }
                ],
            },
        )
        waza_dir = evals_dir / "waza" / "skills" / "demo"
        (waza_dir / "tasks").mkdir(parents=True, exist_ok=True)
        (waza_dir / "eval.yaml").write_text(
            'name: demo-eval\nskill: demo\nschemaVersion: "1.4"\nversion: "0.7.3"\ntasks:\n  - "tasks/*.yaml"\n',
            encoding="utf-8",
        )
        (waza_dir / "tasks" / "positive-1.yaml").write_text(
            "id: positive-1\n"
            "name: Positive demo trigger\n"
            "inputs:\n"
            '  prompt: "Run demo skill"\n'
            "expected:\n"
            "  should_trigger: true\n"
            "graders:\n"
            "  - type: trigger\n"
            "    name: demo-positive-trigger\n"
            "    config:\n"
            "      skill_path: skills/demo/SKILL.md\n"
            "      mode: positive\n",
            encoding="utf-8",
        )

    def test_staged_bundle_without_evals_skips_evals_validation(self):
        checks, findings = validate_evals_directory(self.root, {"demo"})
        self.assertEqual(checks, 0)
        self.assertEqual(findings, [])

    def test_waza_single_testcase_validation_accepts_valid_and_rejects_invalid_schemas(self):
        self._write_valid_evals_fixture()
        checks, findings = validate_evals_directory(self.root, {"demo"})
        self.assertGreater(checks, 0)
        self.assertEqual(findings, [])

        # Reject legacy multi-task list YAML
        task_path = self.root / "evals" / "waza" / "skills" / "demo" / "tasks" / "positive-1.yaml"
        task_path.write_text("- id: legacy-list\n  prompt: bad\n", encoding="utf-8")
        _, list_findings = validate_evals_directory(self.root, {"demo"})
        self.assertTrue(any("single TestCase mapping (dict)" in item for item in list_findings))

        # Reject invalid mode and missing skill_path target
        task_path.write_text(
            "id: bad-grader\n"
            "name: Bad grader\n"
            "inputs:\n"
            '  prompt: "Run demo"\n'
            "graders:\n"
            "  - type: trigger\n"
            "    name: demo-trigger\n"
            "    config:\n"
            "      skill_path: skills/nonexistent/SKILL.md\n"
            "      mode: invalid\n",
            encoding="utf-8",
        )
        _, grader_findings = validate_evals_directory(self.root, {"demo"})
        self.assertTrue(any("config.mode" in item for item in grader_findings))
        self.assertTrue(any("skill_path does not exist" in item for item in grader_findings))

        # Reject dead ../.temp/ links in LATEST.md and duplicate matrix rows
        self._write_valid_evals_fixture()
        (self.root / "evals" / "LATEST.md").write_text(
            "[run](../.temp/evals/results/run/metadata.json)\n",
            encoding="utf-8",
        )
        dup_row = {
            "suite": "file-and-para-24",
            "harness": "Codex",
            "platform": "windows-x86_64",
            "config": "default",
            "required": True,
            "remaining": "Run cases.",
        }
        write_json(
            self.root / "evals" / "matrix.json",
            {"schema": 1, "suite_revision": "1.0-test", "rows": [dup_row, dup_row]},
        )
        _, meta_findings = validate_evals_directory(self.root, {"demo"})
        self.assertTrue(any("dead ../.temp/ links" in item for item in meta_findings))
        self.assertTrue(any("duplicate row key" in item for item in meta_findings))

    def test_latest_md_rendering_is_link_free_and_uses_inline_code_receipts(self):
        rendered, _ = report.render()
        self.assertNotIn("../.temp/", rendered)
        self.assertIn("`configuration-scopes-para-portable-20261011`", rendered)
        self.assertIn("`native-061-codex-yolo-20261009`", rendered)


if __name__ == "__main__":
    unittest.main()
