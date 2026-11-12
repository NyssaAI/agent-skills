"""Use-case tests for scripts/assemble.py, harness-adapters/, and hooks/session-start.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from assemble import canonical_hash_content  # noqa: E402
import assemble  # noqa: E402


def _load_session_start():
    spec = importlib.util.spec_from_file_location("session_start", ROOT / "hooks" / "session-start.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT / ".temp").mkdir(exist_ok=True)

    def test_repo_root_contains_no_self_loaded_host_trees(self):
        for forbidden in (".agents", ".hermes", "artifacts", "adapters"):
            self.assertFalse((ROOT / forbidden).exists(), f"{forbidden}/ must never exist inside repo_root")
        for skill_dir in (ROOT / "skills").glob("*"):
            if skill_dir.is_dir():
                self.assertFalse((skill_dir / "agents").exists(), f"{skill_dir}/agents must live under harness-adapters/codex/")

    def test_voice_rule_reaches_all_staged_packages(self):
        packages = assemble.build_packages()
        for bundle_name in ("portable", "antigravity", "hermes"):
            package = packages[bundle_name][1]
            self.assertIn("rules/writing-voice.md", package)
            self.assertIn(b"write-like-me", package["rules/writing-voice.md"])

    def test_codex_ui_metadata_projects_from_harness_adapters_into_portable_bundle(self):
        portable = assemble.portable_expected_files()
        for skill_name in ("manage-file-operations", "para-vault", "write-like-me"):
            self.assertTrue((ROOT / "harness-adapters" / "codex" / skill_name / "openai.yaml").is_file())
            self.assertIn(f"skills/{skill_name}/agents/openai.yaml", portable)

    def test_private_state_and_scratch_cannot_enter_skill_package(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".temp") as directory:
            root = Path(directory)
            skill = root / "skills" / "sample"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("public", encoding="utf-8")
            for folder in (".nyssa-ai/agent-skills/writing-voice", ".temp", "__pycache__", ".pytest_cache"):
                private = skill / folder / "private.md"
                private.parent.mkdir(parents=True)
                private.write_text("private", encoding="utf-8")
            with patch.object(assemble, "ROOT", root):
                self.assertEqual(assemble.skill_files(), {"skills/sample/SKILL.md": b"public"})

    def test_anchored_project_preserves_content_and_updates_both_conventions(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".temp") as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            agents.write_text(
                "# User instructions\n\n" + assemble.BEGIN + "\nOld\n" + assemble.END,
                encoding="utf-8",
            )
            with patch.object(assemble, "ROOT", root):
                updated = assemble.anchored_agents()
                self.assertTrue(updated.startswith("# User instructions\n"))
                self.assertIn(assemble.VOICE_RULE.read_text(encoding="utf-8").strip(), updated)
                self.assertEqual(updated.count(assemble.VOICE_BEGIN), 1)
                agents.write_text(updated, encoding="utf-8")
                self.assertEqual(assemble.anchored_agents(), updated)

    def test_hermes_harness_adapter_supplies_voice_when_repo_only_has_file_foundation(self):
        foundation = runpy.run_path(str(ROOT / "harness-adapters/hermes/plugin.py"))["foundation"]
        foundation.__globals__["CORE"] = assemble.CORE
        foundation.__globals__["VOICE"] = assemble.VOICE_RULE
        with tempfile.TemporaryDirectory(dir=ROOT / ".temp") as directory:
            project = Path(directory)
            (project / ".git").mkdir()
            core = assemble.CORE.read_text(encoding="utf-8").strip()
            voice = assemble.VOICE_RULE.read_text(encoding="utf-8").strip()
            file_block = f"{assemble.BEGIN}\n{core}\n{assemble.END}"
            (project / "AGENTS.md").write_text(file_block, encoding="utf-8")
            nested = project / "nested"
            nested.mkdir()
            prompt = foundation({"cwd": str(nested)})
            self.assertIn(voice, prompt)
            self.assertNotIn(core, prompt)
            (project / "AGENTS.md").write_text(assemble.startup_text(), encoding="utf-8")
            prompt = foundation({"cwd": str(nested)})
            self.assertNotIn(voice, prompt)
            self.assertIn("write-like-me", prompt)

    def test_write_and_check_stage_into_output_dir_and_reject_repo_root_trees(self):
        for forbidden in (ROOT, ROOT / ".agents", ROOT / ".hermes", ROOT / "artifacts", ROOT / "dist"):
            with self.subTest(forbidden=forbidden), self.assertRaises(ValueError):
                assemble.validate_output_dir(forbidden)

        with tempfile.TemporaryDirectory(dir=ROOT / ".temp") as directory:
            staging = Path(directory) / "dist"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(assemble.assemble(["write", "--output-dir", str(staging)]), 0)
                self.assertEqual(assemble.assemble(["check", "--output-dir", str(staging)]), 0)
            for bundle in ("portable", "antigravity", "hermes"):
                self.assertTrue((staging / bundle / "assembly.json").is_file())
            self.assertFalse((ROOT / ".agents").exists())
            self.assertFalse((ROOT / ".hermes").exists())

    def test_session_start_resolves_canonical_nyssa_ai_and_runtime_root_precedence(self):
        session_start = _load_session_start()
        with tempfile.TemporaryDirectory(dir=ROOT / ".temp") as directory:
            sandbox = Path(directory)
            fake_home = sandbox / "home"
            fake_repo = sandbox / "repo"
            (fake_home / ".nyssa-ai" / "agent-skills").mkdir(parents=True)
            (fake_home / ".nyssaai" / "agent-skills").mkdir(parents=True)
            (fake_repo / ".git").mkdir(parents=True)
            (fake_repo / ".nyssa-ai" / "agent-skills").mkdir(parents=True)
            (fake_repo / ".nyssa" / "agent-skills").mkdir(parents=True)

            roots = session_start.resolve_config_roots(user_home=fake_home, repo_root=fake_repo)
            self.assertEqual(
                roots,
                (
                    (fake_home / ".nyssa-ai").resolve(),
                    (fake_repo / ".nyssa-ai").resolve(),
                ),
            )

            persona = sandbox / "persona"
            persona.mkdir()
            (persona / "SOUL.md").write_text("soul", encoding="utf-8")
            (persona / "IDENTITY.md").write_text("identity", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop("NYSSA_RUNTIME_ROOT", None)
                self.assertEqual(
                    session_start.resolve_runtime_root(cwd=persona, user_home=fake_home),
                    persona.resolve(),
                )
                self.assertEqual(
                    session_start.resolve_runtime_root(
                        explicit_runtime_root=str(sandbox / "explicit"),
                        cwd=persona,
                        user_home=fake_home,
                    ),
                    (sandbox / "explicit").resolve(),
                )
                plain_cwd = sandbox / "plain"
                plain_cwd.mkdir()
                self.assertEqual(
                    session_start.resolve_runtime_root(cwd=plain_cwd, user_home=fake_home),
                    (fake_home / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
                )
            with patch.dict(os.environ, {"NYSSA_RUNTIME_ROOT": str(sandbox / "env-runtime")}):
                self.assertEqual(
                    session_start.resolve_runtime_root(cwd=persona, user_home=fake_home),
                    (sandbox / "env-runtime").resolve(),
                )

    def test_generated_provenance_hash_is_stable_across_line_endings(self):
        lf = canonical_hash_content(b"one\ntwo\n")
        crlf = canonical_hash_content(b"one\r\ntwo\r\n")
        cr = canonical_hash_content(b"one\rtwo\r")
        self.assertEqual(lf, crlf)
        self.assertEqual(lf, cr)


if __name__ == "__main__":
    unittest.main()
