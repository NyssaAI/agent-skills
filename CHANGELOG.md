# Changelog

## Unreleased

## 0.7.4 - Cross-plugin 11-host adapters, 30 Waza tasks, runtime_root & telemetry, Apache-2.0, routing, and validator parity

- Aligned 11-host `harness-adapter` packaging in `scripts/assemble.py` and `evals/plugin_checks.py`, adding root Antigravity `hooks.json`, keeping `.tessl-plugin/plugin.json` and `gemini-extension.json` synchronized with `plugin.json`, projecting unified `author`, `homepage`, `repository`, `license`, and `keywords` metadata across `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and `.cursor-plugin/plugin.json`, and removing duplicate `SKILL.md` `metadata.version` frontmatter.
- Retired dead Codex `openai.yaml` files (`harness-adapters/codex/` and `skills/*/agents/openai.yaml`) in favor of `.codex-plugin/plugin.json` and standard `SKILL.md` discovery.
- Replaced multi-entry Waza list YAML files with 30 single-`TestCase` Waza trigger task specs (`evals/waza/skills/{manage-file-operations,para-vault,write-like-me}/tasks/*.yaml`) validated by `evals/plugin_checks.py` and `waza run`.
- Hardened CI validation (`.github/workflows/validate.yml`) and `evals/report.py` release/report gates against stale or missing evaluation receipts while keeping raw runs isolated under `.temp/evals/`.
- Implemented 4-step `runtime_root` precedence (`--runtime-root` -> `NYSSA_RUNTIME_ROOT` -> `<persona_cwd>/.nyssa-ai/agent-skills/runtime/` -> layered `config.json` `runtimeRoot` / `repo_root` / `user_home` defaults), layered `.nyssa-ai/agent-skills/config.json` loading (`user_home` -> `repo_root`), and opt-in usage telemetry (`telemetry.enabled === true` writing `<runtime_root>/usage/events.jsonl`) in `hooks/session-start.py`.
- Clarified reciprocal cross-plugin and sibling routing boundaries across `para-vault`, `manage-file-operations`, `write-like-me`, and `daily-tasks` (routing candidate action-item capture, live planning sessions, check-ins, and structured work-record mutations to `daily-tasks` without hand-authoring unaccepted task records during general note filing or `Source Record` imports).
- Migrated the public repository license from `MIT` to `Apache-2.0` (`LICENSE`, `plugin.json`, host manifests, and `README.md`) and added this tracked `CHANGELOG.md`.
- Added canonical `scripts/validate.py` CLI entrypoint (with zero-dependency stdlib YAML fallback), domain-specific `## Verification` checklists across all 7 `para-vault` and `write-like-me` workflow runbooks, and `plugin-builder` validator parity rules in `evals/plugin_checks.py` (top-level directory/file allowlist, `.gitattributes` LF enforcement, `docs/` Allowed-Set lockdown, `test/` directory isolation, `Scope Directive` + `## Verification` gates, and machine-local path leak bans).

## 0.7.3 - Cross-plugin Ubiquitous Language, `para-vault` work-record alignment, and staged `harness-adapters`

- Adopted the canonical 5-root Ubiquitous Language (`user_home`, `repo_root`, `vault_root`, `runtime_root`, `plugin_root`) in `docs/GLOSSARY.md`, eliminated self-loaded `.agents/` and `.hermes/` trees from `repo_root`, and moved staged host bundles (`portable`, `antigravity`, `hermes`) to `.temp/dist/` via `scripts/assemble.py`.
- Aligned `para-vault` workflows and schemas with `daily-tasks` structured work records (`RecordKind`: `project`, `milestone`, `task`, `blocker`, `daily-plan` governed by `state` and `## Definition of Done`, keeping `document-maturity` scoped to prose notes and banning `.nyssa-ai/` inside `vault_root`).
- Standardized `Writing Voice Profile` storage under `.nyssa-ai/agent-skills/writing-voice/` (`user_home` and `repo_root` atomic bundle precedence without automatic `.nyssaai`/`.nyssa` probing) and relocated raw evaluation outputs to `.temp/evals/` with durable ledger summaries under `evals/reports/`.

## 0.7.2 - Marketplace release dispatch and evaluation runner sync

- Added automated GitHub Actions marketplace release dispatch (`.github/workflows/release-marketplace.yml`) and synchronized `0.7.2` manifest and assembly versions across host bundles and `evals/LATEST.md`.

## 0.7.1 - Cross-platform evaluation digest normalization and host manifest sync

- Normalized CRLF/LF line endings in `evals/run.py` and `evals/report.py` verifier and evidence SHA-256 digest checks for cross-platform Windows/Linux parity.
- Added tag-triggered marketplace dispatch groundwork and synchronized host manifests and `evals/LATEST.md` to `0.7.1`.

## 0.7.0 - Facade skill consolidation and Waza trigger evaluation suites

- Consolidated granular leaf skills into three cohesive skills (`manage-file-operations`, `para-vault`, and `write-like-me`) with progressive `workflows/` and `references/`.
- Added Waza trigger evaluation suites under `evals/waza/skills/` and refreshed assembled host distributions for `0.7.0`.

## 0.6.4 - Scoped `Writing Voice Profile` precedence and provenance gates

- Added deterministic explicit -> project (`repo_root`) -> user (`user_home`) `Writing Voice Profile` bundle selection, scoped write/privacy protections, and independently reviewed configuration and activation evaluation cases (`SC01`–`SC05`, `AC01`–`AC04`) with critical provenance gates.

## 0.6.3 - Project-level writing voice profiles and `write-like-me` skill

- Introduced the `write-like-me` skill, always-on `rules/writing-voice.md` convention, and Tessl/frozen evaluation suites (`WV01`–`WV06`) for personal writing voice emulation, calibration, and profile maintenance.

## 0.6.2 - Single canonical working copy during inbox filing

- Updated `para-vault` inbox filing rules and evaluation cases so filing from `0-inbox/` retains one canonical working copy at its resolved PARA destination without creating redundant `0-inbox/archive/` shadow duplicates.

## 0.6.1 - Focused vault workflows, template maturity, and multi-host adapters

- Separated `document-maturity` from operational task state, defined `template` maturity independently of generated outputs, moved `plugin-builder` out of the public `agent-skills` catalog, and added Cursor/Grok Bot and Hermes host adapter packaging alongside cross-platform hash normalization.

## 0.1.0 - Initial `agent-skills` catalog and deterministic evaluation harness

- Initial public release of `agent-skills` with foundational file-management and PARA vault skills, Claude/Codex/Gemini/Antigravity host metadata, and the 24-case deterministic filesystem and PARA evaluation suite (`evals/`).
