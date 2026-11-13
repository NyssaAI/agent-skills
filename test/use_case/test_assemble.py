"""Use-case tests for scripts/assemble.py, harness-adapters/, and hooks/session-start.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
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

    def test_repo_root_contains_no_self_loaded_or_retired_host_trees(self):
        for forbidden in (".agents", ".hermes", "artifacts", "adapters"):
            self.assertFalse((ROOT / forbidden).exists(), f"{forbidden}/ must never exist inside repo_root")
        self.assertFalse((ROOT / "harness-adapters" / "codex").exists())
        self.assertFalse(hasattr(assemble, "codex_skill_metadata"))
        for skill_dir in (ROOT / "skills").glob("*"):
            if skill_dir.is_dir():
                self.assertFalse((skill_dir / "agents").exists())

    def test_root_manifests_align_tessl_gemini_codex_and_hooks(self):
        identity = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["license"], "Apache-2.0")
        self.assertEqual(
            identity["keywords"],
            [
                "nyssa",
                "agent-skills",
                "skills",
                "para-vault",
                "write-like-me",
                "manage-file-operations",
                "workflows",
            ],
        )
        manifests = assemble.root_harness_manifests()
        for host_manifest_rel in (
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
            ".cursor-plugin/plugin.json",
        ):
            projected = json.loads(manifests[host_manifest_rel].decode("utf-8"))
            tracked = json.loads((ROOT / host_manifest_rel).read_text(encoding="utf-8"))
            for field in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords"):
                self.assertEqual(
                    projected.get(field),
                    identity[field],
                    f"Projected {host_manifest_rel} {field} drifted from plugin.json",
                )
                self.assertEqual(
                    tracked.get(field),
                    identity[field],
                    f"Tracked {host_manifest_rel} {field} drifted from plugin.json",
                )
        tessl = json.loads(manifests[".tessl-plugin/plugin.json"].decode("utf-8"))
        self.assertEqual(
            tessl,
            {
                "name": "nyssa-ai/agent-skills",
                "version": identity["version"],
                "description": identity["description"],
                "private": True,
                "skills": "./skills",
                "rules": "./rules",
            },
        )
        gemini = json.loads(manifests["gemini-extension.json"].decode("utf-8"))
        self.assertEqual(
            gemini,
            {
                "name": identity["name"],
                "version": identity["version"],
                "description": identity["description"],
            },
        )
        self.assertNotIn("contextFileName", gemini)
        codex = json.loads(manifests[".codex-plugin/plugin.json"].decode("utf-8"))
        self.assertEqual(codex["skills"], "./skills/")
        self.assertIn("interface", codex)
        hooks = json.loads(manifests["hooks.json"].decode("utf-8"))
        self.assertEqual(
            hooks,
            {
                "agent-skills": {
                    "SessionStart": [
                        {
                            "type": "command",
                            "command": 'python "./hooks/session-start.py"',
                            "timeout": 60,
                        }
                    ]
                }
            },
        )

    def test_license_changelog_and_single_version_source_of_truth(self):
        import yaml

        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)
        self.assertIn("Version 2.0, January 2004", license_text)
        self.assertIn("Copyright 2026 NyssaAI", license_text)
        self.assertNotIn("MIT License", license_text)

        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Licensed under the [Apache License 2.0](LICENSE) © 2026 NyssaAI.", readme_text)
        self.assertIn("See [CHANGELOG.md](CHANGELOG.md) for release history.", readme_text)
        self.assertNotIn("MIT License", readme_text)

        changelog_text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(changelog_text.startswith("# Changelog\n"))
        for expected_heading in (
            "## Unreleased",
            "## 0.7.4 -",
            "## 0.7.3 -",
            "## 0.7.2 -",
            "## 0.7.1 -",
            "## 0.7.0 -",
            "## 0.6.4 -",
            "## 0.6.3 -",
            "## 0.6.2 -",
            "## 0.6.1 -",
            "## 0.1.0 -",
        ):
            self.assertIn(expected_heading, changelog_text)

        for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
            raw = skill_md.read_text(encoding="utf-8")
            self.assertTrue(raw.startswith("---\n"))
            frontmatter_text = raw.split("\n---\n", 1)[0].removeprefix("---\n")
            frontmatter = yaml.safe_load(frontmatter_text)
            self.assertIsInstance(frontmatter, dict)
            nested_meta = frontmatter.get("metadata")
            if isinstance(nested_meta, dict):
                self.assertNotIn("version", nested_meta, f"{skill_md} must not duplicate plugin.json version")

    def test_rules_and_antigravity_bundle_include_always_on_frontmatter_version_and_hooks(self):
        identity = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        packages = assemble.build_packages()
        for bundle_name in ("portable", "antigravity", "hermes"):
            package = packages[bundle_name][1]
            self.assertIn("rules/writing-voice.md", package)
            self.assertTrue(
                package["rules/writing-voice.md"].decode("utf-8").startswith(assemble.VOICE_RULE_FRONTMATTER)
            )
            self.assertIn(b"write-like-me", package["rules/writing-voice.md"])
            self.assertFalse(any(name.endswith("/agents/openai.yaml") for name in package))

        for bundle_name in ("portable", "antigravity"):
            package = packages[bundle_name][1]
            self.assertTrue(
                package["rules/file-management.md"].decode("utf-8").startswith(assemble.FILE_RULE_FRONTMATTER)
            )
            self.assertIn("hooks.json", package)
            self.assertIn("hooks/session-start.py", package)

        agy_manifest = json.loads(packages["antigravity"][1]["plugin.json"].decode("utf-8"))
        self.assertEqual(agy_manifest["version"], identity["version"])
        self.assertEqual(agy_manifest["author"], identity["author"])
        self.assertEqual(agy_manifest["homepage"], identity["homepage"])
        self.assertEqual(agy_manifest["repository"], identity["repository"])

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

    def test_anchored_project_preserves_content_and_strips_rule_frontmatter(self):
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
                voice_body = assemble.strip_frontmatter(assemble.VOICE_RULE.read_text(encoding="utf-8"))
                self.assertIn(voice_body, updated)
                self.assertNotIn("trigger: always_on", updated)
                self.assertEqual(updated.count(assemble.VOICE_BEGIN), 1)
                agents.write_text(updated, encoding="utf-8")
                self.assertEqual(assemble.anchored_agents(), updated)

    def test_hermes_harness_adapter_registers_skills_and_bounded_deduplicated_foundation(self):
        hermes_pkg = assemble.hermes_expected_files()
        self.assertIn("skills/manage-file-operations/core.md", hermes_pkg)
        self.assertIn("rules/writing-voice.md", hermes_pkg)

        hermes_ns = runpy.run_path(str(ROOT / "harness-adapters/hermes/plugin.py"))
        foundation = hermes_ns["foundation"]
        register = hermes_ns["register"]
        foundation.__globals__["CORE"] = assemble.CORE
        foundation.__globals__["VOICE"] = assemble.VOICE_RULE

        full_prompt = foundation({})
        self.assertLessEqual(len(full_prompt), 4000)
        self.assertNotIn("trigger: always_on", full_prompt)

        registered_skills: list[tuple[str, Path]] = []
        registered_sections: list[tuple[str, object, str, int]] = []

        class _Ctx:
            def register_skill(self, name: str, path: Path) -> None:
                registered_skills.append((name, path))

            def register_system_prompt_section(
                self, section_id: str, content: object, *, position: str = "after_memory", max_chars: int = 4000
            ) -> None:
                registered_sections.append((section_id, content, position, max_chars))

        register(_Ctx())
        self.assertEqual(
            [name for name, _ in registered_skills],
            ["manage-file-operations", "para-vault", "write-like-me"],
        )
        self.assertEqual(registered_sections, [("agent-skills.foundation", foundation, "after_memory", 4000)])

        with tempfile.TemporaryDirectory(dir=ROOT / ".temp") as directory:
            project = Path(directory)
            (project / ".git").mkdir()
            core = assemble.strip_frontmatter(assemble.CORE.read_text(encoding="utf-8"))
            voice = assemble.strip_frontmatter(assemble.VOICE_RULE.read_text(encoding="utf-8"))
            file_block = f"{assemble.BEGIN}\n{core}\n{assemble.END}"
            (project / "AGENTS.md").write_text(file_block, encoding="utf-8")
            nested = project / "nested"
            nested.mkdir()
            prompt = foundation({"cwd": str(nested)})
            self.assertIn(voice, prompt)
            self.assertNotIn(core, prompt)
            self.assertNotIn("trigger: always_on", prompt)
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
            with patch.dict(os.environ, {"NYSSA_PLUGIN_STATE_DIR": str(sandbox / "retired-state")}, clear=False):
                os.environ.pop("NYSSA_RUNTIME_ROOT", None)
                self.assertEqual(
                    session_start.resolve_runtime_root(cwd=persona, user_home=fake_home),
                    (persona / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
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
                self.assertEqual(
                    session_start.resolve_runtime_root(cwd=plain_cwd, user_home=fake_home, repo_root=fake_repo),
                    (fake_repo / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
                )
            with patch.dict(os.environ, {"NYSSA_RUNTIME_ROOT": str(sandbox / "env-runtime")}):
                self.assertEqual(
                    session_start.resolve_runtime_root(cwd=persona, user_home=fake_home),
                    (sandbox / "env-runtime").resolve(),
                )
            with patch.dict(os.environ, {"NYSSA_RUNTIME_ROOT": str(persona)}):
                self.assertEqual(
                    session_start.resolve_runtime_root(cwd=plain_cwd, user_home=fake_home),
                    (persona / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
                )

    def test_generated_provenance_hash_is_stable_across_line_endings(self):
        lf = canonical_hash_content(b"one\ntwo\n")
        crlf = canonical_hash_content(b"one\r\ntwo\r\n")
        cr = canonical_hash_content(b"one\rtwo\r")
        self.assertEqual(lf, crlf)
        self.assertEqual(lf, cr)


if __name__ == "__main__":
    unittest.main()
