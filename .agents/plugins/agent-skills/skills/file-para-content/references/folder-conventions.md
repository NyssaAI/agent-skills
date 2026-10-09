# Vault Folder Conventions

Use these operational defaults when maintaining a vault that follows this catalog's numbered folder scheme. Preserve accepted local conventions. These catalog defaults extend the four PARA category definitions.

## Capture and workspace locations

Use `0-inbox/` for captures awaiting classification. Newly supplied content with a known destination needs no inbox stage. Process existing captures through [inbox filing](../SKILL.md#file-the-content), moving unchanged content to one working home without an automatic archive duplicate. Preserve unresolved captures in the inbox until their destination or required source information is known. Preserve recoverable history before substantive rewriting; necessary snapshots use the accepted archive location, not an Inbox subfolder. Existing historical copies remain unchanged unless their migration or deletion is explicitly requested.

Use [file-management's intermediate-work convention](../../manage-file-operations/references/intermediate-work.md) for `.temp/`. Preserve existing root entries and external tool directories. Do not add loose root notes or additional top-level directories without explicit authorization. Follow the [workspace guidance](vault-conventions.md#temporary-work) for vault-specific preservation and ignore rules.

## Folder layout


- Use lowercase kebab-case folder slugs, with the date conventions below. Preserve existing names unless renaming is part of the task.
- Projects use `1-projects/YYYY.MM.DD-project-slug/`, dated when the project was created, following the [project date convention](../../revise-vault-documents/references/frontmatter-schemas.md#date-meanings-and-configuration). Keep project-wide notes at its root and use purpose-specific working folders for coherent collections. Projects have no fixed maximum depth; create only folders the work needs and preserve tool-required layouts.
- Areas use `2-areas/{area}/` for ongoing responsibilities without completion dates. An Area may be a function such as marketing or finance, or a personal responsibility such as fitness. `email/`, `calendar/`, and `daily-notes/` are optional Areas; create or use them only when the vault's needs or accepted layout call for them. Use an existing suitable Area before adding one. A topic kept only for interest or reference belongs to Resources.
- When present, the email Area uses `2-areas/email/YYYY.MM.DD/` and the calendar Area uses `2-areas/calendar/we-YYYY.MM.DD/`. Choose their dates using the [date meanings and timezone rules](../../revise-vault-documents/references/frontmatter-schemas.md#date-meanings-and-configuration). Other Areas may use purpose-specific working folders as described below.
- Resources use broad, stable types: `company-context/`, `people/`, `goals/`, `rules/`, and `templates/`. New resource types require explicit authorization. Do not create a folder for each topic.
- In Areas and Projects, create only working-folder levels that the work needs. Resources remain broad, stable collections; archived project bundles retain their complete internal structure.
- Use folders for ownership and working purpose; do not create folders for document maturity, authority, or tags.


## Area working folders

Keep the Area's index and information that governs the whole responsibility at its root. Store recurring tasks, procedures, operational records, metrics, and other ongoing work in the Area that owns them. Use purpose-specific working folders for coherent collections when that makes the work easier to maintain; for example, a marketing Area might have `campaign-operations/` and `reporting/`. Do not create a folder for every task or topic. An Area has no fixed maximum depth, but each level needs a working purpose.

For example, a reusable marketing process can live at `2-areas/marketing/marketing-process.md`. A continuously updated view of the function's status can live at `2-areas/marketing/marketing-status.md`; a periodic snapshot can live at `2-areas/marketing/reporting/YYYY.MM.DD-marketing-status.md`, dated when the snapshot was produced. Put a differing as-of date or reporting period in the slug or body. Link useful records from `00-marketing-index.md`.

A finite initiative with a defined outcome and completion point belongs in its own Project. A status report about that initiative stays with the Project, while `marketing-status.md` describes the ongoing marketing function. Link the Project from the relevant Area index instead of duplicating its working files in the Area. Recurring operational work remains in the Area even when individual tasks have due dates.

## Project working folders

Keep project-wide planning, strategy, decisions, and coordination at the project root. Projects may have milestone folders that hold the planning documents and work products completed in each milestone. Use other concrete working collections such as `discovery/requests/` or `evidence/employment/` when the work calls for them. Supporting notes may live with the material they explain. Put non-note working artifacts in purpose-specific subdirectories by default, while preserving tool-required locations. File purpose determines placement; extension alone does not justify separating related material. Preserve useful source-package structure and avoid generic nested `notes/` trees.

Outside projects, attachments stay beside their owners, including within Area working folders, without extra attachment folders. Use [navigation](../../maintain-vault-navigation/references/navigation.md#attachments) for attachment names and links.


## Source-record destinations

The email or calendar service is authoritative for live source state when available. Prefer a source link and reliable identifier when the task needs no local evidence or offline access; do not download a payload solely to create a vault copy. Retain one native record or provenance-bearing capture when the user requests local retention, the work needs historical evidence or offline access, or the supplied record is the only available source. Label retained records as snapshots rather than synchronized masters, with source attribution and an observed/as-of time when known; do not invent unavailable source links or freshness.

When retaining a record and the vault uses an email or calendar Area, route it to that Area's date folders and link it from relevant projects. Otherwise use the user-selected or accepted destination; do not create either Area just to file a record. Derived analysis may belong directly to the project it advances. Reuse an identical retained record instead of adding another copy; Inbox processing does not require a second evidence copy.


Use the [date meanings and timezone rules](../../revise-vault-documents/references/frontmatter-schemas.md#date-meanings-and-configuration) for filename and folder dates, including email timestamp fallbacks and calendar week endings. Use [record-update handling](../../import-vault-source-records/references/source-records.md#source-record-identity-and-updates) for version precedence, reschedules, cancellations, and unresolved records.


## Archive destinations

Completed, abandoned, or superseded projects go intact to `4-archives/<existing-project-folder>/`. Preserve the complete internal structure; do not flatten, ZIP, or scatter the bundle to satisfy depth preferences.

Individual archived items and necessary historical snapshots go directly into `4-archives/`. Do not add category or year folders or create an archive under the inbox. An unchanged filed capture needs no additional archived original. Preserve existing historical copies in their existing locations unless a separate migration or cleanup is authorized.


Use [archive workflows](../../manage-vault-lifecycle/references/lifecycle.md#archive-workflow) for eligibility, collisions, preservation, metadata, and link repairs.

## Project identities

For colliding new project names, append the [general collision suffix](../../manage-file-operations/references/safe-operations.md#identity-and-collisions) to the project slug and use that same slug in its index filename; do not suffix the index independently.
