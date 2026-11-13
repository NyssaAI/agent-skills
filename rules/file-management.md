---
trigger: always_on
description: Core file-management naming and safety rules.
---

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
