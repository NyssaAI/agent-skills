# Vault Folder Conventions

> [!IMPORTANT] Scope Directive
> This reference defines operational folder layout conventions inside `vault_root` (`0-inbox/`, `1-projects/`, `2-areas/` including `2-areas/daily-plans/`, `3-resources/`, `4-archives/`), aligned directly with `daily-tasks`. It does NOT define four-category classification logic (owned by `classification.md`) or frontmatter schema definitions (owned by `frontmatter-schemas.md`).

Use these operational defaults when maintaining a `vault_root` that follows this catalog's numbered `PARA Category` scheme. Preserve accepted local conventions (including non-PARA vaults or existing `1-projects/<slug>/` folders).

## Capture and scratch locations

Use `0-inbox/` for `Inbox Capture` items awaiting classification. Newly supplied content with a known destination needs no inbox stage. Process existing captures through [inbox filing](../workflows/file.md), moving unchanged content to one working home without an automatic `0-inbox/archive/` duplicate. Preserve unresolved captures in `0-inbox/` until their destination or required source information is known. Preserve recoverable history before substantive rewriting; necessary snapshots use `4-archives/`, not an inbox subfolder. Existing historical copies remain unchanged unless their migration or deletion is explicitly requested.

Use [file-management's intermediate-work convention](../../manage-file-operations/references/intermediate-work.md) for `vault_root/.temp/`. Never create `.nyssa-ai/` (or retired `.nyssaai/` / `.nyssa/`) inside `vault_root`. Preserve existing root entries and external tool directories. Do not add loose root notes or additional top-level directories without explicit authorization. Follow the [shared vault conventions](vault-conventions.md#temporary-work) for vault-specific preservation and ignore rules.

## Folder layout

- Use lowercase kebab-case folder slugs, with the date conventions below. Preserve existing names unless renaming is part of the task.
- **Projects (`1-projects/`, aligned to `daily-tasks`):** New projects use `1-projects/YYYY.MM.DD-<slug>/` with `project-index.md` at the project root, dated when the project was created (`YYYY.MM.DD-<slug>`), while preserving existing `1-projects/<slug>/` or legacy `*-index.md` layouts without unsolicited renaming. Structured `daily-tasks` children inside a project use:
  - Milestones: `mN-<slug>/mN-<slug>.md` (e.g., `m1-design/m1-design.md`)
  - Tasks: `mN-<slug>/tN-<slug>.md` or `tN-<slug>.md` (e.g., `m1-design/t1-architecture-spike.md`)
  - External Blockers: `blockers/bN-<slug>.md` (e.g., `blockers/b1-oauth-verification.md`)
  - Supporting inputs/outputs and working collections: `inputs/`, `outputs/`, `discovery/`, `evidence/`, etc., created only as the work needs them.
- **Areas (`2-areas/`):** Ongoing responsibilities without completion dates (`2-areas/<area>/`).
  - **Canonical `Daily Plan` folder (`daily-tasks` aligned):** `2-areas/daily-plans/YYYY.MM.DD-daily-plan.md` is the canonical `Daily Plan` location inside `vault_root`.
  - Optional communication/capture areas (`email/`, `calendar/`, `daily-notes/`): create or use them only when the vault's needs or accepted layout call for them. When present, the email Area uses `2-areas/email/YYYY.MM.DD/` and the calendar Area uses `2-areas/calendar/we-YYYY.MM.DD/`. Choose their dates using [date meanings and timezone rules](frontmatter-schemas.md#date-meanings-and-configuration).
- **Resources (`3-resources/`):** Broad, stable reference collections: `company-context/`, `people/`, `goals/`, `rules/`, and `templates/`. New resource categories require explicit authorization; do not create a top-level resource folder for every micro-topic.
- **Archives (`4-archives/`):** Inactive material and completed/abandoned `Project` bundles.
- Use folders for ownership and working purpose; do not create folders for `document-maturity`, `state`, `canonical` authority, or tags.

## Area working folders

Keep an Area's main MOC (`00-<area>-index.md`) and information that governs the whole responsibility at its root (`2-areas/<area>/`). Store recurring procedures, operational records, metrics, and ongoing work in the Area that owns them. `2-areas/daily-plans/` holds dated `Daily Plan` records (`YYYY.MM.DD-daily-plan.md`) managed by `daily-tasks`. Other Areas may use purpose-specific working folders for coherent collections (such as `campaign-operations/` and `reporting/`) without creating a folder for every note.

A finite effort with a defined outcome and completion point belongs in its own `Project` under `1-projects/`. Link the `Project` (`project-index.md`) from the relevant Area MOC instead of duplicating project working files inside `2-areas/`.

## Project working folders

Keep `project-index.md` and project-wide coordination at `1-projects/YYYY.MM.DD-<slug>/` (or existing `1-projects/<slug>/`). Milestone folders (`mN-<slug>/`) hold `mN-<slug>.md`, milestone tasks (`tN-<slug>.md`), and milestone deliverables (`inputs/`, `outputs/`), while `blockers/` holds `External Blocker` records (`bN-<slug>.md`). Projects may also include concrete working collections such as `discovery/requests/` or `evidence/contracts/` when the work calls for them. Supporting prose notes may live alongside the material they explain. File purpose determines placement; extension alone does not justify separating related material. Avoid generic nested `notes/` trees.

Outside projects, attachments stay beside their owners, including within Area working folders, without extra attachment folders. Use [navigation](navigation.md#attachments) for attachment names and links.

## Source-record destinations

The email or calendar service is authoritative for live source state when available. Prefer a source link and reliable identifier when the task needs no local evidence or offline access; do not download a payload solely to create a vault copy. Retain one native `Source Record` or provenance-bearing capture when the user requests local retention, the work needs historical evidence or offline access, or the supplied record is the only available source. Label retained records as snapshots rather than synchronized masters, with source attribution and an observed/as-of time when known; do not invent unavailable source links or freshness.

When retaining a `Source Record` and `vault_root` uses an email or calendar Area, route it to that Area's date folders and link it from relevant projects. Otherwise use the user-selected or accepted destination; do not create either Area just to file a record. Derived analysis may belong directly to the `Project` it advances. Reuse an identical retained record instead of adding another copy; inbox processing does not require a second evidence copy.

Use [date meanings and timezone rules](frontmatter-schemas.md#date-meanings-and-configuration) for filename and folder dates, including email timestamp fallbacks and calendar week endings. Use [record-update handling](source-records.md#source-record-identity-and-updates) for version precedence, reschedules, cancellations, and unresolved records.

## Archive destinations

Completed, cancelled, abandoned, or superseded `Project` bundles move intact to `4-archives/<existing-project-folder>/`. Preserve the complete internal structure (`project-index.md`, `mN-<slug>/`, `tN-<slug>.md`, `blockers/`, working folders, native files, and `## Definition of Done` checklists); do not flatten, ZIP, or scatter the bundle to satisfy depth preferences.

Individual archived items and necessary historical snapshots go directly into `4-archives/`. Do not add category or year folders or create an archive under `0-inbox/`. An unchanged filed capture needs no additional archived original. Preserve existing historical copies in their existing locations unless a separate migration or cleanup is authorized.

Use [archive workflows](lifecycle.md#archive-workflow) for eligibility, collisions, preservation, metadata, and link repairs.

## Project identities

For colliding new `Project` folder names (`1-projects/YYYY.MM.DD-<slug>/`), append the [general collision suffix](../../manage-file-operations/references/safe-operations.md#identity-and-collisions) to the project folder slug (`YYYY.MM.DD-<slug>-2/project-index.md`). Keep `project-index.md` at the root of that folder (or match the folder slug if maintaining an existing legacy `*-index.md` convention).
