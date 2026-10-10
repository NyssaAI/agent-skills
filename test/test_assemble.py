import sys
import unittest
import tempfile
import runpy
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from assemble import canonical_hash_content  # noqa: E402
import assemble  # noqa: E402


class AssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT / ".temp").mkdir(exist_ok=True)

    def test_voice_rule_reaches_both_generated_packages(self):
        for package in (assemble.expected_files(), assemble.hermes_expected_files()):
            self.assertIn("rules/writing-voice.md", package)
            self.assertIn(b"write-in-user-voice", package["rules/writing-voice.md"])

    def test_private_state_and_scratch_cannot_enter_skill_package(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".temp") as directory:
            root = Path(directory)
            skill = root / "skills" / "sample"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("public", encoding="utf-8")
            for folder in (".nyssa-ai/agent-skills/writing-voice", ".temp", "__pycache__"):
                private = skill / folder / "private.md"
                private.parent.mkdir(parents=True)
                private.write_text("private", encoding="utf-8")
            with patch.object(assemble, "ROOT", root):
                self.assertEqual(assemble.skill_files(), {"skills/sample/SKILL.md": b"public"})

    def test_anchored_project_preserves_content_and_updates_both_conventions(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".temp") as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            agents.write_text("# User instructions\n\n" + assemble.BEGIN + "\nOld\n" + assemble.END,
                              encoding="utf-8")
            with patch.object(assemble, "ROOT", root):
                updated = assemble.anchored_agents()
                self.assertTrue(updated.startswith("# User instructions\n"))
                self.assertIn(assemble.VOICE_RULE.read_text(encoding="utf-8").strip(), updated)
                self.assertEqual(updated.count(assemble.VOICE_BEGIN), 1)
                agents.write_text(updated, encoding="utf-8")
                self.assertEqual(assemble.anchored_agents(), updated)

    def test_hermes_supplies_voice_when_project_only_has_file_foundation(self):
        foundation = runpy.run_path(str(ROOT / "adapters/hermes/plugin.py"))["foundation"]
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
            self.assertIn("write-in-user-voice", prompt)

    def test_generated_provenance_hash_is_stable_across_line_endings(self):
        lf = canonical_hash_content(b"one\ntwo\n")
        crlf = canonical_hash_content(b"one\r\ntwo\r\n")
        cr = canonical_hash_content(b"one\rtwo\r")
        self.assertEqual(lf, crlf)
        self.assertEqual(lf, cr)


if __name__ == "__main__":
    unittest.main()
