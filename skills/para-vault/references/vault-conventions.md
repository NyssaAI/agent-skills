# Shared Vault Conventions

> [!IMPORTANT] Scope Directive
> This reference defines governing locations, zero-`.nyssa-ai/` boundaries, `vault_root/.temp/` scratch rules, and `daily-tasks` work-record alignment for a recognized `vault_root`. It does NOT define four-category classification logic (owned by `classification.md`) or individual document schemas (owned by `frontmatter-schemas.md`).

Apply this guidance only inside a recognized `vault_root`. It is shared reference material; reading it does not start a filing or revision workflow.

If the [file-management foundation](../../manage-file-operations/core.md) is not already in context, read it before acting. Reading the foundation does not activate the file-operations workflow.

## Locations and governing rules

For operations inside `vault_root`, resolve the accepted inbox, project, daily-plan, archive, and rules locations before using them. In this catalog's default layout (aligned with `daily-tasks`), these are `0-inbox/`, `1-projects/`, `2-areas/daily-plans/`, `4-archives/`, and `3-resources/rules/`. Do not create an archive inside `0-inbox/` for processed `Inbox Capture` items. Preserve existing local layouts and historical copies; an updated convention does not authorize moving or deleting them. Do not invent a top-level folder when a necessary location is unknown.

For decisions that depend on vault conventions, check a supplied rules path or explicit task override, then links in existing indexes, then `3-resources/rules/` (or the accepted local rules location). Use accepted rules found there; a filename alone does not establish authority. If no applicable rule exists, use the defaults in these references while preserving the existing layout. Resolve competing canonical rules through the [authority rule](frontmatter-schemas.md#authority-and-tags); ask only when the conflict affects the task. These conventions do not authorize reorganizing unrelated content.

Knowledge and resource notes (`2-areas/` non-plan notes, `3-resources/`, MOCs) use `document-maturity`, whereas `daily-tasks` structured work records (`RecordKind`: `project`, `milestone`, `task`, `blocker`, `daily-plan`) are governed by `state` (`ProjectState`, `MilestoneState`, `TaskState`, `BlockerState`) without requiring `document-maturity`. Retire `task-state` in favor of `state`: preserve read-only awareness of legacy fields on existing files, never write `task-state`, and follow the [compatibility and migration rule](frontmatter-schemas.md#legacy-metadata-compatibility) before changing note metadata.

## Temporary work

Use [file-management's intermediate-work convention](../../manage-file-operations/references/intermediate-work.md) at `vault_root/.temp/`. Disposable output, including Markdown scratch output, needs no note frontmatter or index entry. Do not put scripts, exports, `artifacts/`, or backup folders at the `vault_root` top level.

If output becomes a retained deliverable, file it in its known retained-content destination, add metadata if it is a maintained Markdown note or work record, and update the applicable index. Verify the retained copy before cleanup.

## Dot-folders and ignore rules

`vault_root` contains **zero** `.nyssa-ai/` configuration, secrets, or machine-local runtime state files (`NyssaAI.Configuration` lives strictly in `user_home` and `repo_root`, and mutable runtime state lives in `runtime_root`). Never create `.nyssa-ai/` (or retired `.nyssaai/` / `.nyssa/`) inside `vault_root`; only `vault_root/.temp/` is permitted for disposable scratch.

Treat external editor or sync dot-folders (such as `.obsidian/` or `.git/`) other than `vault_root/.temp/` as external tool, sync, or version-control directories. Exclude them from note scans, indexing, and file cleanup; do not move vault content into them or alter them as part of file maintenance.

Preserve root ignore files (`.gitignore`, `.stignore`). Apply [file-management's `.temp/` exclusion rule](../../manage-file-operations/references/intermediate-work.md); other tool dot-folders follow accepted local ignore rules. Do not change unrelated configuration during filing.

For actual paths, read [folder conventions](folder-conventions.md). For ownership decisions, read [classification](classification.md).
