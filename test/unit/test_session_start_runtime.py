"""Responsibility: Verify hooks/session-start.py layered config.json loading, 4-step runtime_root resolution, and opt-in usage telemetry."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


REPOSITORY = Path(__file__).resolve().parents[2]
HOOK_PATH = REPOSITORY / "hooks" / "session-start.py"


def _load_session_start():
    spec = importlib.util.spec_from_file_location("session_start_unit", HOOK_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SessionStartRuntimeAndTelemetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (REPOSITORY / ".temp").mkdir(exist_ok=True)

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(dir=REPOSITORY / ".temp")
        self.sandbox = Path(self._tmp.name)
        self.fake_home = self.sandbox / "home"
        self.fake_repo = self.sandbox / "repo"
        self.plain_cwd = self.sandbox / "cwd"
        self.fake_home.mkdir()
        self.fake_repo.mkdir()
        (self.fake_repo / ".git").mkdir()
        self.plain_cwd.mkdir()
        self.session_start = _load_session_start()

    def tearDown(self):
        self._tmp.cleanup()

    def _write_json(self, path: Path, payload: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def test_load_plugin_config_layers_user_home_then_repo_root_and_ignores_retired_dirs(self):
        self._write_json(
            self.fake_home / ".nyssaai" / "agent-skills" / "config.json",
            {"runtimeRoot": str(self.sandbox / "legacy-nyssaai"), "telemetry": {"enabled": True}},
        )
        self._write_json(
            self.fake_repo / ".nyssa" / "agent-skills" / "config.json",
            {"runtimeRoot": str(self.sandbox / "legacy-nyssa"), "telemetry": {"enabled": True}},
        )
        self.assertEqual(
            self.session_start.load_plugin_config(user_home=self.fake_home, repo_root=self.fake_repo),
            {},
        )

        self._write_json(
            self.fake_home / ".nyssa-ai" / "agent-skills" / "config.json",
            {
                "runtimeRoot": str(self.sandbox / "home-configured-runtime"),
                "telemetry": {"enabled": False, "channel": "local"},
            },
        )
        home_only = self.session_start.load_plugin_config(user_home=self.fake_home, repo_root=self.fake_repo)
        self.assertEqual(home_only["runtimeRoot"], str(self.sandbox / "home-configured-runtime"))
        self.assertEqual(home_only["telemetry"], {"enabled": False, "channel": "local"})

        self._write_json(
            self.fake_repo / ".nyssa-ai" / "agent-skills" / "config.json",
            {
                "runtimeRoot": str(self.sandbox / "repo-configured-runtime"),
                "telemetry": {"enabled": True},
            },
        )
        layered = self.session_start.load_plugin_config(user_home=self.fake_home, repo_root=self.fake_repo)
        self.assertEqual(layered["runtimeRoot"], str(self.sandbox / "repo-configured-runtime"))
        self.assertEqual(layered["telemetry"], {"enabled": True, "channel": "local"})

    def test_step_3_persona_cwd_resolves_nested_plugin_runtime_without_polluting_persona_root(self):
        persona = self.sandbox / "persona-work"
        persona.mkdir()
        (persona / "SOUL.md").write_text("# Soul\n", encoding="utf-8")

        with patch.dict(
            os.environ,
            {"NYSSA_PLUGIN_STATE_DIR": str(self.sandbox / "retired-env")},
            clear=False,
        ):
            os.environ.pop("NYSSA_RUNTIME_ROOT", None)
            # Only SOUL.md without IDENTITY.md must NOT match Step 3.
            self.assertEqual(
                self.session_start.resolve_runtime_root(cwd=persona, user_home=self.fake_home),
                (self.fake_home / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
            )

            # Both SOUL.md and IDENTITY.md trigger Step 3 -> <cwd>/.nyssa-ai/agent-skills/runtime.
            (persona / "IDENTITY.md").write_text("# Identity\n", encoding="utf-8")
            resolved = self.session_start.resolve_runtime_root(cwd=persona, user_home=self.fake_home)
            self.assertEqual(
                resolved,
                (persona / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
            )
            self.assertEqual(sorted(p.name for p in persona.iterdir()), ["IDENTITY.md", "SOUL.md"])

    def test_steps_1_2_and_4_runtime_root_precedence_and_layered_config_override(self):
        persona = self.sandbox / "persona"
        persona.mkdir()
        (persona / "SOUL.md").write_text("# Soul\n", encoding="utf-8")
        (persona / "IDENTITY.md").write_text("# Identity\n", encoding="utf-8")

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("NYSSA_RUNTIME_ROOT", None)

            # Step 4c: fallback to user_home/.nyssa-ai/agent-skills/runtime
            self.assertEqual(
                self.session_start.resolve_runtime_root(
                    cwd=self.plain_cwd,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                ),
                (self.fake_home / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
            )

            # Step 4b: repo_root/.nyssa-ai/agent-skills exists -> repo_root/.nyssa-ai/agent-skills/runtime
            (self.fake_repo / ".nyssa-ai" / "agent-skills").mkdir(parents=True)
            self.assertEqual(
                self.session_start.resolve_runtime_root(
                    cwd=self.plain_cwd,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                ),
                (self.fake_repo / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
            )

            # Step 4a: user_home config.json runtimeRoot overrides repo_root default directory
            home_custom = self.sandbox / "home-runtime-override"
            self._write_json(
                self.fake_home / ".nyssa-ai" / "agent-skills" / "config.json",
                {"runtimeRoot": str(home_custom)},
            )
            self.assertEqual(
                self.session_start.resolve_runtime_root(
                    cwd=self.plain_cwd,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                ),
                home_custom.resolve(),
            )

            # Step 4a: repo_root config.json runtimeRoot overrides user_home config.json runtimeRoot
            repo_custom = self.sandbox / "repo-runtime-override"
            self._write_json(
                self.fake_repo / ".nyssa-ai" / "agent-skills" / "config.json",
                {"runtimeRoot": str(repo_custom)},
            )
            self.assertEqual(
                self.session_start.resolve_runtime_root(
                    cwd=self.plain_cwd,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                ),
                repo_custom.resolve(),
            )

            # Step 3 beats Step 4 configured runtimeRoot
            self.assertEqual(
                self.session_start.resolve_runtime_root(
                    cwd=persona,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                ),
                (persona / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
            )

        # Step 2: NYSSA_RUNTIME_ROOT plain directory vs persona directory
        env_plain = self.sandbox / "env-plain"
        env_plain.mkdir()
        with patch.dict(os.environ, {"NYSSA_RUNTIME_ROOT": str(env_plain)}):
            self.assertEqual(
                self.session_start.resolve_runtime_root(
                    cwd=persona,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                ),
                env_plain.resolve(),
            )

        env_persona = self.sandbox / "env-persona"
        env_persona.mkdir()
        (env_persona / "SOUL.md").write_text("# Soul\n", encoding="utf-8")
        (env_persona / "IDENTITY.md").write_text("# Identity\n", encoding="utf-8")
        with patch.dict(os.environ, {"NYSSA_RUNTIME_ROOT": str(env_persona)}):
            self.assertEqual(
                self.session_start.resolve_runtime_root(
                    cwd=self.plain_cwd,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                ),
                (env_persona / ".nyssa-ai" / "agent-skills" / "runtime").resolve(),
            )

            # Step 1: explicit runtime_root parameter beats NYSSA_RUNTIME_ROOT
            explicit = self.sandbox / "explicit-override"
            self.assertEqual(
                self.session_start.resolve_runtime_root(
                    runtime_root=explicit,
                    cwd=persona,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                ),
                explicit.resolve(),
            )

    def test_usage_telemetry_is_opt_in_and_creates_zero_directories_when_disabled(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("NYSSA_RUNTIME_ROOT", None)

            # Default (no config.json) -> False, zero usage/ directory created
            self.assertFalse(
                self.session_start.is_telemetry_enabled(user_home=self.fake_home, repo_root=self.fake_repo)
            )
            self.assertIsNone(
                self.session_start.resolve_usage_telemetry_dir(
                    cwd=self.plain_cwd,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                )
            )
            self.assertIsNone(
                self.session_start.record_usage_event(
                    "unit_probe",
                    {"step": 1},
                    cwd=self.plain_cwd,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                )
            )
            default_runtime = self.fake_home / ".nyssa-ai" / "agent-skills" / "runtime"
            self.assertFalse(default_runtime.exists())

            # Non-boolean truthy value ("true") must remain disabled (strict === true check)
            self._write_json(
                self.fake_home / ".nyssa-ai" / "agent-skills" / "config.json",
                {"telemetry": {"enabled": "true"}},
            )
            self.assertFalse(
                self.session_start.is_telemetry_enabled(user_home=self.fake_home, repo_root=self.fake_repo)
            )
            self.assertIsNone(
                self.session_start.record_usage_event(
                    "unit_probe",
                    cwd=self.plain_cwd,
                    user_home=self.fake_home,
                    repo_root=self.fake_repo,
                )
            )
            self.assertFalse((default_runtime / "usage").exists())

            # Opt-in enabled in repo_root config.json -> writes <runtime_root>/usage/events.jsonl
            self._write_json(
                self.fake_repo / ".nyssa-ai" / "agent-skills" / "config.json",
                {"telemetry": {"enabled": True}},
            )
            self.assertTrue(
                self.session_start.is_telemetry_enabled(user_home=self.fake_home, repo_root=self.fake_repo)
            )
            expected_runtime = (self.fake_repo / ".nyssa-ai" / "agent-skills" / "runtime").resolve()
            usage_dir = self.session_start.resolve_usage_telemetry_dir(
                cwd=self.plain_cwd,
                user_home=self.fake_home,
                repo_root=self.fake_repo,
            )
            self.assertEqual(usage_dir, expected_runtime / "usage")
            self.assertFalse((expected_runtime / "usage").exists())

            events_file = self.session_start.record_usage_event(
                "skill_invoked",
                {"skill": "write-like-me"},
                cwd=self.plain_cwd,
                user_home=self.fake_home,
                repo_root=self.fake_repo,
            )
            self.assertEqual(events_file, expected_runtime / "usage" / "events.jsonl")
            assert events_file is not None
            self.assertTrue(events_file.is_file())
            lines = events_file.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            event_payload = json.loads(lines[0])
            self.assertEqual(event_payload["plugin"], "agent-skills")
            self.assertEqual(event_payload["event"], "skill_invoked")
            self.assertEqual(event_payload["data"], {"skill": "write-like-me"})

    def test_session_start_cli_creates_zero_usage_dir_by_default_and_writes_events_when_opted_in(self):
        env = {
            key: value
            for key, value in os.environ.items()
            if key not in {"NYSSA_RUNTIME_ROOT", "NYSSA_PLUGIN_STATE_DIR"}
        }
        env["HOME"] = str(self.fake_home)
        env["USERPROFILE"] = str(self.fake_home)
        env["CLAUDE_PLUGIN_ROOT"] = str(REPOSITORY)

        explicit_rt = self.sandbox / "cli-runtime"
        disabled_run = subprocess.run(
            [sys.executable, str(HOOK_PATH), "--runtime-root", str(explicit_rt)],
            cwd=self.fake_repo,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("# File-management foundation", disabled_run.stdout)
        self.assertFalse(explicit_rt.exists())
        self.assertFalse((self.fake_home / ".nyssa-ai" / "agent-skills" / "runtime" / "usage").exists())

        self._write_json(
            self.fake_repo / ".nyssa-ai" / "agent-skills" / "config.json",
            {"telemetry": {"enabled": True}},
        )
        enabled_run = subprocess.run(
            [sys.executable, str(HOOK_PATH), "--runtime-root", str(explicit_rt)],
            cwd=self.fake_repo,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("# File-management foundation", enabled_run.stdout)
        events_file = explicit_rt / "usage" / "events.jsonl"
        self.assertTrue(events_file.is_file())
        recorded = json.loads(events_file.read_text(encoding="utf-8").strip())
        self.assertEqual(recorded["event"], "session_start")
        self.assertEqual(recorded["plugin"], "agent-skills")


if __name__ == "__main__":
    unittest.main()
