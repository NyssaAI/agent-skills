# Scoped Writing Voice Storage

> [!IMPORTANT] Scope Directive
> This reference defines canonical storage paths, atomic resolution rules (explicit pointer > `repo_root` override > `user_home` fallback), privacy verification, and safe write procedures for `Writing Voice Profile` bundles (`.nyssa-ai/agent-skills/writing-voice/`). It does NOT define schema fields (owned by `profile-schema.md`) or drafting workflows (owned by `drafting-and-review.md`).

## Resolve one complete bundle

Resolve `user_home` (`~`) separately from the active `repo_root` (and `runtime_root` / `plugin_root` / `vault_root`). Use an explicit workspace binding or the applicable `repo_root`. A nested directory or subprocess `cwd` inside `plugin_root` or an installation cache never changes `repo_root`, and `vault_root` NEVER hosts `.nyssa-ai/` configuration or `Writing Voice Profile` bundles. With no active `repo_root`, resolve only `user_home` scope; never fabricate a `repo_root`. `plugin_root` installation scope does not restrict preference scope. Inspect exact canonical `.nyssa-ai/` paths (`NyssaAI.Configuration` layered static plugin config: `user_home` `~/.nyssa-ai/agent-skills/config.json` $\rightarrow$ `repo_root` `<repo_root>/.nyssa-ai/agent-skills/config.json`) or an accepted explicit pointer; never recursively scan `user_home`, and never read retired `NYSSA_PLUGIN_STATE_DIR`.

Each scope stores optional static plugin configuration at `.nyssa-ai/agent-skills/config.json` and the atomic `Writing Voice Profile` bundle (never legacy `settings.json` or `profile.json`):

```text
~/.nyssa-ai/agent-skills/                              # user_home
<repo_root>/.nyssa-ai/agent-skills/                    # repo_root
  config.json          # optional static plugin config (runtimeRoot, telemetry.enabled)
  writing-voice/
    VOICE.md
    STYLE.md           # optional
    examples/          # approved curated examples, optional
```

Select an explicit task-selected profile first, otherwise the `repo_root` bundle (`<repo_root>/.nyssa-ai/agent-skills/writing-voice/`), otherwise the `user_home` bundle (`~/.nyssa-ai/agent-skills/writing-voice/`). Only `.nyssa-ai/` is recognized as a canonical configuration directory: retired legacy `.nyssaai` and `.nyssa` directories are never probed, read, or written automatically unless explicitly pointed to by the user for a one-off migration, in which case original files remain preserved without automatic deletion.

Selection is atomic: read `VOICE.md`, optional `STYLE.md`, and `examples/` only from the selected bundle. Never inherit a missing `STYLE.md` or `examples/` from another scope or borrow another `repo_root`'s profile. Absence falls back; an existing incomplete or malformed bundle reports a diagnostic and does not silently fall through. Validate `VOICE.md` against [profile schema](profile-schema.md), and verify any style/example links before claiming a supported voice match. An empty `.nyssa-ai/agent-skills/writing-voice/` root without `VOICE.md` is incomplete. When both bundles are absent, useful drafting continues from task instructions without claiming a profile match.

## Identify the write scope

Ordinary reads and one-off overrides never persist preferences. An explicit user request such as "for all projects" selects `user_home` scope (`~/.nyssa-ai/agent-skills/writing-voice/`), including when invoked from a `repo_root` installation. An explicit project/repository request requires an established `repo_root` (`<repo_root>/.nyssa-ai/agent-skills/writing-voice/`). Never write `.nyssa-ai/` into `vault_root` or `plugin_root`. Reuse an accepted scope; otherwise new setup defaults to `repo_root` when an active `repo_root` is established and `user_home` when none is established. State the chosen scope and exact destination before writing. Updating `user_home` defaults writes `~/.nyssa-ai/agent-skills/writing-voice/` even when a `repo_root` override is active; inspect the destination independently of the selected read bundle. Personal setup requires no `vault_root`, project collection, or project decision-log entry. Report personal changes and their path in the task result. `repo_root` changes follow applicable repository logging conventions.

Profile data belongs outside `plugin_root`, installation caches, `vault_root`, and public skill source. Do not introduce synchronization or multi-person selection.

## Privacy and temporary work

Before persisting a private profile, use the destination scope's accepted ignore convention or a narrowly scoped local exclusion for `/.nyssa-ai/agent-skills/writing-voice/`. For either scope (`user_home` or `repo_root`), including a `user_home` directory that is itself versioned, inspect the repository covering the destination. In a Git repository, a local `.git/info/exclude` entry can avoid changing tracked policy; respect existing exclusions and verify with `git check-ignore` against the intended files. Also check whether any profile files are already tracked: ignore rules do not protect tracked content. Do not silently remove tracked files or alter a user's sharing decision. If privacy cannot be verified, keep proposed profile content in the conversation and report what blocks safe persistence.

Do not ignore all `.nyssa-ai/`; sibling plugins may have different sharing policies (while `.nyssa-ai/*/runtime/` is always gitignored). Sharing a profile requires an explicit decision. In a non-Git directory, inspect the actual applicable sharing/packaging rules rather than claiming the dot-prefix protects data. A Git exclusion protects against accidental Git inclusion, not against other synchronization services. Packaged `harness-adapter` bundles must exclude `user_home` and `repo_root` `.nyssa-ai/` configuration, samples, and `.temp/` scratch data.

Keep disposable calibration drafts, comparisons, and recovery copies under `<repo_root>/.temp/agent-skills/writing-voice/` (or `<runtime_root>/.temp/agent-skills/writing-voice/` when executing inside a resolved `runtime_root`, or `<user_home>/.temp/agent-skills/writing-voice/` when no `repo_root` or `runtime_root` is established). Resolve `runtime_root` in 4 steps: `--runtime-root` $\rightarrow$ `NYSSA_RUNTIME_ROOT` (`<NYSSA_RUNTIME_ROOT>/.nyssa-ai/agent-skills/runtime/` when containing `SOUL.md` + `IDENTITY.md`, else `<NYSSA_RUNTIME_ROOT>`) $\rightarrow$ `<persona_cwd>/.nyssa-ai/agent-skills/runtime/` when `cwd` contains `SOUL.md` + `IDENTITY.md` $\rightarrow$ configured `runtimeRoot` in layered `config.json` (else `<repo_root>/.nyssa-ai/agent-skills/runtime/` when `<repo_root>/.nyssa-ai/agent-skills/` exists, else `~/.nyssa-ai/agent-skills/runtime/`). Usage telemetry is strictly opt-in (`"telemetry": { "enabled": false }` by default in `config.json`): create zero `usage/` directories or files unless `telemetry.enabled === true`, writing `<runtime_root>/usage/events.jsonl` when enabled. Never use `plugin_root` or an installed cache as scratch. Verify this private scratch location is excluded before writing samples, drafts, or recovery content there, using the same tracked-file and sharing checks as for the profile. If the existing exclusion does not cover it, use the narrowly scoped `/.temp/agent-skills/writing-voice/` exclusion; do not assume `.temp/` is already ignored. Preserve unrelated temporary work. Raw samples are not persistent configuration by default. Retain excerpts or complete examples only with user approval; avoid unrelated personal details. Use readable Markdown without an opaque database or mandatory settings file.

## Safe profile writes

1. Read the existing files, their identity, and relevant `repo_root` conventions. Determine the exact authorized change; profile creation does not authorize replacing unrelated files at the same path.
2. For substantive revisions, preserve the previous content through existing recoverable history or a noncolliding recovery copy in the `.temp/agent-skills/writing-voice/` scratch location before writing. Do not assume private files are backed up by Git. Keep that recovery content available until the result is verified and accepted.
3. Recheck the current file before replacement. If it changed since inspection or a destination belongs to unrelated content, stop the dependent write, reconcile the collision, and preserve both versions. An interrupted update must inspect current and recovery content before resuming.
4. Write only the approved portions; preserve unrelated profile guidance. Use noncolliding example names, preserving known dates and existing names. Do not invent sample dates.
5. Read back the result, check schema and relative example links, and verify private-data exclusion. Report the profile paths and recovery location when used. Delete retained content only with explicit authorization.

Use [manage-file-operations](../../manage-file-operations/SKILL.md) when copying, moving, importing, or archiving existing content or resolving destination collisions. Ordinary drafting performs none of these profile writes.
