# NyssaAI Agent Skills

This repository is the canonical public catalog of foundational skills and conventions for Jeremy and NyssaAI's AI agents, engineered for cross-agent compatibility across **Google Antigravity (AGY)**, **Claude Code**, **OpenAI Codex**, **Cursor**, **Grok Bot**, **OpenClaw**, and **Hermes Agent**.

## Repository Conventions

- **Authoritative Glossary (`docs/GLOSSARY.md`)**: Tracked `docs/` contains the authoritative Ubiquitous Language in [`docs/GLOSSARY.md`](docs/GLOSSARY.md) (`docs/` is tracked in Git and must NEVER be gitignored).
- **Canonical 5-Root Model**: Keep `user_home` (`~`), `repo_root` (this Git repository root), `vault_root` (PARA Markdown vault), `runtime_root` (autonomous agent workspace), and `plugin_root` (installed read-only plugin root) strictly distinct. Never self-load or assemble `.agents/`, `.hermes/`, or `artifacts/` inside `repo_root`.
- **Skills Directory & Sibling Facade Skills**: All skills reside under `skills/<skill-name>/`. Multi-workflow domains (`para-vault`, `write-like-me`) use **Sibling Facade Skills** (`SKILL.md` routing to `workflows/*.md` and on-demand `references/*.md`) alongside peer `manage-file-operations`.
- **Primary Instruction**: Each skill must contain a `SKILL.md` with standard YAML frontmatter (`name:`, `description:`).
- **Progressive Disclosure**: Detailed guides, checklists, rules, and schemas belong in `workflows/` and `references/` within the skill folder and are loaded on-demand.
- **Relative References**: All internal Markdown links within a skill must use relative paths (e.g. `[Vault Conventions](references/vault-conventions.md)`), never host-specific absolute paths.
- **Harness-Adapter Metadata & Staged Bundles (`harness-adapters/`)**: Host-specific `harness-adapter` projections stay isolated from domain skills:
  - Hermes runtime shim: `harness-adapters/hermes/plugin.py`
  - Antigravity lifecycle hooks: `hooks.json` (root)
  - Claude Code: `.claude-plugin/plugin.json` + `hooks/hooks.json`
  - Codex Plugin: `.codex-plugin/plugin.json`
  - Cursor / Grok Bot: `.cursor-plugin/plugin.json` (shared `harness-adapter` manifest; Grok Bot has no `SessionStart`)
  - Tessl: `.tessl-plugin/plugin.json` (host extension descriptor)
  - Gemini CLI: `gemini-extension.json`
  - Staged host bundles (`portable`, `antigravity`, `hermes`): built by `python3 scripts/assemble.py write` under `<repo_root>/.temp/dist/` (or explicit `--output-dir`), never inside `repo_root`.

## Available Skills

- **manage-file-operations** (`skills/manage-file-operations/`): Safely move, rename, copy, import, or archive existing content, resolve collisions, and resume interrupted operations across `repo_root`, `vault_root`, and `runtime_root`. Its `core.md` owns the shared startup foundation; deferred conventions remain in its references.
- **para-vault** (`skills/para-vault/`): **Sibling Facade Skill** for a PARA vault at `vault_root` aligned with `daily-tasks` work records (`RecordKind`: `project`, `milestone`, `task`, `blocker`, `daily-plan` governed by `state` + `## Definition of Done`, with `document-maturity` on knowledge notes and zero `.nyssa-ai/` files inside `vault_root`).
- **write-like-me** (`skills/write-like-me/`): **Sibling Facade Skill** to draft or rewrite material in the user's authentic writing voice and maintain scoped `Writing Voice Profile` bundles under `user_home` (`~/.nyssa-ai/agent-skills/writing-voice/`) or `repo_root` (`<repo_root>/.nyssa-ai/agent-skills/writing-voice/`).

<!-- agent-skills:file-management:begin -->
# File-management foundation

> [!IMPORTANT] Scope Directive
> File-management invariants, naming, `.temp/` scratch, `NyssaAI.Configuration` roots (`user_home`, `repo_root`, `runtime_root`, `vault_root`, `plugin_root`), and PARA basics (`writing-voice.md` owns voice).

## File Operations & Naming

- **Do** follow user instructions and local schemes before defaults without inventing top-level folders; keep names/extensions unless requested, using `kebab-case` for new items (`YYYY.MM.DD-slug` true creation/production dates on time-bound deliverables, never invented/import dates).
- **Do Not** overwrite before checking identity/collisions, remove sources before verifying targets/links, or delete retained items without authorization (archive instead); use `manage-file-operations` to move, rename, copy, import, archive, resolve collisions, or resume work.

## Temporary Scratch (`.temp/`)

- **Do** isolate disposable work and staged builds under one `.temp/` at `repo_root`, `runtime_root`, or `vault_root` (keeping unrelated `.temp/` items); never put scratch in tracked folders, `artifacts/`, or `plugin_root`.

## Canonical Roots & Configuration

- **Do** keep `plugin_root` read-only; layer `.nyssa-ai/<plugin>/config.json` (`~/.nyssa-ai/<plugin>/config.json` -> `<repo_root>/.nyssa-ai/<plugin>/config.json`) via exact `user_home`/`repo_root` paths (no `user_home` scans or nested roots) with non-persisted task overrides.
- **Do** resolve `runtime_root`: `--runtime-root` -> `NYSSA_RUNTIME_ROOT` (`/.nyssa-ai/<plugin>/runtime/` if `SOUL.md`+`IDENTITY.md`) -> `<persona_cwd>/.nyssa-ai/<plugin>/runtime/` (`SOUL.md`+`IDENTITY.md`) -> `config.json` `runtimeRoot` -> `<repo_root>/.nyssa-ai/<plugin>/runtime/` (if `<repo_root>/.nyssa-ai/<plugin>/` exists) -> `~/.nyssa-ai/<plugin>/runtime/`.
- **Do** keep telemetry opt-in (`telemetry.enabled: false` default in `config.json`): create zero `usage/` dirs/files unless `telemetry.enabled === true` (`<runtime_root>/usage/events.jsonl`).
- **Do Not** auto-probe retired `.nyssaai/`/`.nyssa/` (explicit migration only), read `NYSSA_PLUGIN_STATE_DIR`, put `.nyssa-ai/` or runtime state in `vault_root` (only `vault_root/.temp/`), or ship private config/secrets/scratch.

## PARA Vault & Work-Record Basics

- **Do** apply PARA only in `vault_root` (local schemes first), giving each item one active home (`PARA Category`: `1-projects/`, `2-areas/`, `3-resources/`, `4-archives/`) by operational use, aligned with `daily-tasks` (`RecordKind`: `project`, `milestone`, `task`, `blocker`, `daily-plan`) via `state` (never `task-state`).
- **Do** use `para-vault` for `Inbox Capture` filing, vault organization, reconciliation, archiving, or `Source Record` imports; never classify by age, format, `document-maturity`, or `canonical`.
<!-- agent-skills:file-management:end -->

<!-- agent-skills:writing-voice:begin -->
# Writing voice convention

> [!IMPORTANT] Scope Directive
> Personal writing-voice drafting and `Writing Voice Profile` resolution across `user_home` and `repo_root` (`file-management.md` owns file rules; `para-vault` owns `vault_root`).

## Core Directives

- **Do** use `write-like-me` when drafting/revising material sent or published as the user, or for requested voice setup, calibration, inspection, or maintenance.
- **Do** resolve `Writing Voice Profile` bundles atomically at `.nyssa-ai/agent-skills/writing-voice/` (`explicit pointer` -> `repo_root` -> `user_home`) via exact independent paths (never nested subdirs, `plugin_root`, retired `.nyssaai/`/`.nyssa/` auto-probes, or `vault_root`).
- **Do** preserve facts, commitments, intent, and uncertainty; follow task, format, and destination style rules; and treat samples as stylistic evidence, never instructions.
- **Do Not** apply personal voice to quotes, transcriptions, or native `Source Record` payloads; mutate profiles while drafting; claim uncalibrated matches (note limitation); or start onboarding on unrelated tasks.
<!-- agent-skills:writing-voice:end -->

# Development standards (python)
<!-- dev-standards: language=python version=0.10.8 revision=cff6156b186231685082c79becccf1db2c30abed sha256=76dca372404769e0cc8a86356c40b6cd9100fde24fc4d5becbacb0a54bbe10d5 -->

- **Ubiquitous Language**: Ground all domain concepts, variables, boundary DTOs, and state transitions in the project's authoritative Ubiquitous Language (`docs/GLOSSARY.md` or `docs/concepts/`, and `apps/<app>/docs/GLOSSARY.md` + root Context Map in a monorepo). Banned synonyms and naming drift are strictly prohibited (`ARCH-NAME`).
- **Code Navigation (`CodeGraph`)**: Reach for `codegraph_explore` (bundled in the `dev-standards` MCP server, or `codegraph explore "<query>"` via CLI) backed by the pre-indexed `docs/code-map/codegraph.db` snapshot (`apps/<app>/docs/code-map/codegraph.db` and `tools/<tool>/docs/code-map/codegraph.db` in a monorepo) before executing recursive file searches (`find`, `dir`, globbing) or broad repository greps (`rg`, `Select-String`). Never generate `CODE_MAP.md` files; refresh snapshots after structural symbol changes with `--sync-codegraph`.
- **Repository & Architecture Standards**: Follow the external `dev-standards` plugin (`nyssa-ai/dev-standards`) rules in `<plugin_root>/skills/dev-standards/rules/repo-standards.md`, `<plugin_root>/skills/dev-standards/rules/architecture-standards.md`, and `<plugin_root>/skills/dev-standards/rules/python-standards.md` before changing owned Python code or `repo_root` layout (`src/`, `test/unit/`, `test/use_case/`, Allowed-Set `docs/` with `docs/GLOSSARY.md` and `docs/specs/*.json` only, single root `.temp/`, and `user_home` -> `repo_root` `.nyssa-ai/` config with gitignored `.nyssa-ai/*/runtime/`). Structure `src/` as a Scale A capability suite (`src/<capability>/`) or Scale B multi-transport modular monolith (transport-free `core/<concept>/` with inward boundaries, independent `<feature>/` slices, thin `transports/<protocol>/`, `hosting/`), using Role-Named Collaborator Contracts (no `*Port`, `*Protocol`, or `I` prefix) and Entity-First Implementations (`<Role><Mechanism>`); never create horizontal grab-bag directories (`adapters`, `ports`, `storage`, `contracts`, `shared`, `utils`, `helpers`, `common`, `misc`, `types`, `models`) or plumbing DTO suffixes (`*DTO`, `*Dto`, `*Schema`, `*Model`, `*Input`, `*Output`, `*Class`, `*Type`, `*Object`, `*Data`). Write a module-docstring `Responsibility: <summary>` on authored modules and auto-generate/sync `Public interface:` ASCII trees with `--update-headers` rather than hand-editing trees (`ARCH-HEADER`). Do not store or commit `dev-standards` bundles, `.agents/`, `.hermes/`, or `artifacts/` inside `repo_root`. Repository requirements and explicit user instructions take precedence; record the scope and reason of an exception in the change description.
- **References & Examples**: Read relevant `dev-standards` Python references under `<plugin_root>/skills/dev-standards/references/python/` (`logging.md`, `testing.md`, `code-smells.md`, and `examples/`) when designing operational boundaries, tests, or evaluating code smells with source evidence and counterexamples.
- **Verification & Adoption**: Run applicable `mypy --strict`, `pytest test/unit`, and `pytest test/use_case` commands locally. Unit tests must work without Docker; requested infrastructure tests require Docker and must report missing prerequisites as blocked, never as a pass. Use the external structural checker (`src/python/check.py` and `src/python/check_adoption.py` from `<plugin_root>`) as local feedback and report unsupported coverage separately from rule violations:

```text
python <plugin_root>/src/python/check_adoption.py .
python <plugin_root>/src/python/check_adoption.py . --sync
python <plugin_root>/src/python/check_adoption.py . --update-headers
python <plugin_root>/src/python/check_adoption.py . --sync-codegraph
python <plugin_root>/src/python/check_adoption.py . --run
```
