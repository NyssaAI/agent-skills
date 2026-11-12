# NyssaAI Agent Skills

Version: **0.7.3** (see [authoritative glossary](docs/GLOSSARY.md) and [latest evaluation](evals/LATEST.md)).

Three canonical skills share one maintained source tree at `repo_root`, a concise [startup foundation](skills/manage-file-operations/core.md), and a [writing voice convention](rules/writing-voice.md). The PARA section applies exclusively to recognized PARA vaults (`vault_root`); detailed runbooks and references load on demand.

| Skill | Pattern | Scope & Workflows |
| --- | --- | --- |
| [manage-file-operations](skills/manage-file-operations/SKILL.md) | Peer Skill | Safely move, rename, copy, import, or archive existing content, resolve destination collisions, and resume interrupted operations across `repo_root`, `vault_root`, and `runtime_root`. Its `core.md` owns the shared startup foundation. |
| [para-vault](skills/para-vault/SKILL.md) | Sibling Facade Skill | Manage a PARA vault (`vault_root`) aligned with `daily-tasks` work records: classify and file `Inbox Capture` items (`workflows/file.md`), reconcile and revise notes without flattening work records (`workflows/reconcile.md`), archive or reactivate projects (`workflows/archive.md`), maintain navigation (`workflows/navigate.md`), and import `Source Record` snapshots (`workflows/import-records.md`). |
| [write-like-me](skills/write-like-me/SKILL.md) | Sibling Facade Skill | Draft or rewrite communications in the user's authentic voice (`workflows/draft.md`) and establish, inspect, calibrate, or update scoped `Writing Voice Profile` bundles (`workflows/maintain.md`). |

## Canonical 5-Root Ubiquitous Language

See [`docs/GLOSSARY.md`](docs/GLOSSARY.md) for full definitions:

- **`user_home` (`~`)**: Account-level `.nyssa-ai/` configuration (`~/.nyssa-ai/agent-skills/writing-voice/`).
- **`repo_root`**: Git repository root containing tracked source (`skills/`, `rules/`, `hooks/`, `harness-adapters/`, `docs/`, `scripts/`, `test/`, `evals/`) and optional repository-scoped `.nyssa-ai/` overrides (`<repo_root>/.nyssa-ai/agent-skills/writing-voice/`). Never self-loads `.agents/`, `.hermes/`, or `artifacts/`.
- **`vault_root`**: Shared Markdown PARA vault (`0-inbox/`, `1-projects/`, `2-areas/`, `3-resources/`, `4-archives/`). Zero `.nyssa-ai/` config or runtime files are ever stored inside `vault_root` (only disposable scratch at `vault_root/.temp/`).
- **`runtime_root`**: Autonomous agent persona working directory (`--runtime-root` $\rightarrow$ `NYSSA_RUNTIME_ROOT` $\rightarrow$ persona `cwd` with `SOUL.md` + `IDENTITY.md` $\rightarrow$ `~/.nyssa-ai/<plugin>/runtime/` or `<repo_root>/.nyssa-ai/<plugin>/runtime/`).
- **`plugin_root`**: Installed read-only plugin bundle root (`CLAUDE_PLUGIN_ROOT`, `CURSOR_PLUGIN_ROOT`, etc.).

## `para-vault` and `daily-tasks` Vault Alignment

`para-vault` shares `vault_root` cleanly with `daily-tasks`:

1. **Structured Work Records (`RecordKind`)**: Records with `type` in `project`, `milestone`, `task`, `blocker`, or `daily-plan` are governed by `state` (`ProjectState`, `MilestoneState`, `TaskState`: `not-started | in-progress | completed | cancelled`; `BlockerState`: `open | resolved`) and `## Definition of Done` (`- [ ]` / `- [x]` checklists):
   - Projects: `1-projects/YYYY.MM.DD-<slug>/project-index.md` (canonical `daily-tasks` folder) or existing `1-projects/<slug>/`
   - Milestones: `mN-<slug>/mN-<slug>.md`
   - Tasks: `tN-<slug>.md` (project root or milestone folder)
   - External Blockers: `blockers/bN-<slug>.md`
   - Daily Plans: `2-areas/daily-plans/YYYY.MM.DD-daily-plan.md`
2. **Knowledge Notes (`document-maturity`)**: Non-plan area notes (`2-areas/`) and reusable resource notes (`3-resources/`) use `document-maturity` (`draft`, `current`, `deprecated`, `historical`, `archived`, `template`, `fixture`). Structured `daily-tasks` work records do not require `document-maturity`, and `workflows/reconcile.md` preserves valid `daily-tasks` records in place rather than rewriting them into prose notes. The retired `task-state` frontmatter key is never written (recognized read-only only during authorized legacy migrations). See [vault conventions](skills/para-vault/references/vault-conventions.md) and [frontmatter schemas](skills/para-vault/references/frontmatter-schemas.md#legacy-metadata-compatibility).
3. **Inbox Filing & `Source Record` Retention**: Filing from `0-inbox/` keeps one canonical working copy at its resolved PARA destination without creating an inbox shadow archive. Email and calendar services govern live source state; retain local snapshots only when requested or required as durable evidence. See [source record destinations](skills/para-vault/references/folder-conventions.md#source-record-destinations).

## `harness-adapter` Packaging and Activation

Canonical plugin source lives under `skills/`, `rules/`, `hooks/`, and `harness-adapters/`. Root `harness-adapter` manifests (`plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.tessl-plugin/plugin.json`, and `gemini-extension.json`) stay synchronized via `python3 scripts/assemble.py write`.

`scripts/assemble.py` **never** writes `.agents/`, `.hermes/`, or `artifacts/` into `repo_root`. Instead, `python3 scripts/assemble.py write` updates tracked root `harness-adapter` manifests in place and stages host distribution bundles under `--output-dir` (defaulting to `<repo_root>/.temp/dist/`):

- `.temp/dist/portable/` — portable bundle with `harness-adapters/codex/<skill>/openai.yaml` projected to `skills/<skill>/agents/openai.yaml` for Codex UI discovery.
- `.temp/dist/antigravity/` — Antigravity plugin bundle with `always_on` rules (installed to a target workspace's `.agents/plugins/agent-skills/`).
- `.temp/dist/hermes/` — Hermes Agent plugin bundle using `harness-adapters/hermes/plugin.py` (installed to a target workspace's `.hermes/plugins/agent-skills/`).

`python3 scripts/assemble.py check` verifies exact synchronization of tracked manifests and staged bundles and fails if `.agents/`, `.hermes/`, or `artifacts/` appear inside `repo_root`.

| Host | `harness-adapter` Route | Activation Notes |
| --- | --- | --- |
| Antigravity CLI / 2.0 / IDE | Staged `.temp/dist/antigravity/` installed to target workspace `.agents/plugins/agent-skills/` ([docs](https://antigravity.google/docs/plugins)). | `gemini-extension.json` is separate Gemini CLI metadata. |
| Codex | Root `.codex-plugin/plugin.json` + staged `.temp/dist/portable/` (includes Codex UI `openai.yaml` projections) ([docs](https://developers.openai.com/plugins/build/plugins)). | Install via supported catalog/install flow and trust `hooks/hooks.json` for `SessionStart`. |
| Claude Code & Cowork | `.claude-plugin/plugin.json` + `skills/` and `hooks/hooks.json` ([docs](https://code.claude.com/docs/en/plugins-reference)). | Install via Claude plugin manager or `--plugin-dir` outside `repo_root`. |
| OpenClaw | Install compatible bundle with `openclaw plugins install <package-path>` ([docs](https://docs.openclaw.ai/plugins/bundles)). | Markdown skills load directly without a custom runtime shim. |
| Hermes Agent | Staged `.temp/dist/hermes/` from `harness-adapters/hermes/plugin.py` installed to target `.hermes/plugins/agent-skills/` ([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)). | Install into target workspace/home plugin path (`HERMES_ENABLE_PROJECT_PLUGINS=true`). |
| Cursor & Grok Bot | `.cursor-plugin/plugin.json` + `skills/` ([docs](https://cursor.com/docs/reference/plugins)). | Grok Bot shares the Cursor package without `SessionStart` hooks (foundation loads on demand). |

See the [coverage matrix](evals/matrix.json) and [latest evaluation](evals/LATEST.md) for exact per-host verification evidence.

## Configuration and `Writing Voice Profile` Bundles

`NyssaAI.Configuration` resolves canonical `.nyssa-ai/` directories across `user_home` (`~/.nyssa-ai/`) and `repo_root` (`<repo_root>/.nyssa-ai/`). Legacy `.nyssaai` and `.nyssa` directory names are retired and never probed or written automatically.

`write-like-me` stores atomic `Writing Voice Profile` bundles (`VOICE.md`, optional `STYLE.md`, optional `examples/`) at `~/.nyssa-ai/agent-skills/writing-voice/` (`user_home`) or `<repo_root>/.nyssa-ai/agent-skills/writing-voice/` (`repo_root`). Atomic bundle selection resolves explicit task pointer $\rightarrow$ `repo_root` override $\rightarrow$ `user_home` fallback without merging files across scopes. Disposable calibration comparisons and recovery snapshots belong under `<repo_root>/.temp/agent-skills/writing-voice/` (or `<runtime_root>/.temp/agent-skills/writing-voice/` / `<user_home>/.temp/agent-skills/writing-voice/`). See [scoped storage](skills/write-like-me/references/storage.md) for privacy verification and safe write rules.

## Development, Testing, and Evaluation

```bash
python3 scripts/assemble.py write
python3 scripts/assemble.py check
python3 evals/run.py validate
python3 evals/report.py check
pytest test/unit test/use_case
```

Raw evaluation exports and failed attempt diagnostics live in gitignored `.temp/evals/{results,attempts}/`; durable human-readable summaries and verified receipts live in tracked [`evals/reports/`](evals/reports/) and [`evals/LATEST.md`](evals/LATEST.md). See [`evals/README.md`](evals/README.md) for full suite documentation.

[MIT License](LICENSE) © 2026 NyssaAI.
