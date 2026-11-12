# Frontmatter Schemas

> [!IMPORTANT] Scope Directive
> This reference defines YAML frontmatter schemas, `RecordKind` work-record `state` values (`daily-tasks` aligned), `Document Maturity` (`document-maturity`) for knowledge notes, canonical authority precedence, and date rules inside `vault_root`. It does NOT define four-category classification logic (owned by `classification.md`) or folder structures (owned by `folder-conventions.md`).

Contents:

- [Field meanings](frontmatter-schemas.md#field-meanings)
- [Legacy compatibility](frontmatter-schemas.md#legacy-metadata-compatibility)
- [Authority and tags](frontmatter-schemas.md#authority-and-tags)
- [Dates and configuration](frontmatter-schemas.md#date-meanings-and-configuration)
- [Stable note](frontmatter-schemas.md#stable-note)
- [Draft note](frontmatter-schemas.md#draft-note)
- [MOC](frontmatter-schemas.md#map-of-content-moc)
- [Project index](frontmatter-schemas.md#project-index)
- [Work records (`daily-tasks` aligned)](frontmatter-schemas.md#work-records-daily-tasks-aligned)
- [Inbox intent](frontmatter-schemas.md#inbox-only-intent-fields)
- [Canonical rules](frontmatter-schemas.md#canonical-rules-note)
- [Archive fields](frontmatter-schemas.md#archive-fields)

Maintain a clean distinction between **knowledge/resource notes** and **`daily-tasks` work records**:

1. **Knowledge & Resource Notes** (`2-areas/` non-plan prose notes, `3-resources/`, MOCs, and supporting prose notes/registers): require `type` (`note` or `moc`), `created` (`YYYY-MM-DD`), and `document-maturity` (`raw`, `draft`, `reviewed`, `established`).
2. **`daily-tasks` Work Records (`RecordKind`)**: records with `type` in `project`, `milestone`, `task`, `blocker`, or `daily-plan` are governed by `state` (`ProjectState`, `MilestoneState`, `TaskState`, `BlockerState`) and do **not** require `document-maturity`. Never write the retired `task-state` frontmatter field.

Frontmatter calendar dates use ISO `YYYY-MM-DD` (timestamps use UTC ISO-8601 `YYYY-MM-DDTHH:MM:SSZ` where `daily-tasks` records `created_at` / `updated_at`); filename date prefixes, where applicable, use `YYYY.MM.DD`. Tags are optional YAML lists without `#`; omit the field or use `tags: []` when none are useful. Preserve native `Source Record` files such as `.eml` and `.ics` in their native format without inserting YAML.

Disposable scratch output in `vault_root/.temp/` and unchanged preserved originals are exempt from note frontmatter. Do not retrofit metadata into preserved evidence.

## Field meanings

`type` identifies the `RecordKind` (`project`, `milestone`, `task`, `blocker`, `daily-plan`) or knowledge-note form (`note`, `moc`), independently of maturity, `state`, `canonical` authority, location, and tags. Preserve existing `type` values; a procedure normally uses `type: note` and may use `tags: [procedure]`.

### `Document Maturity` (knowledge & resource notes)

| `document-maturity` | Meaning |
|---|---|
| `raw` | Captured and unchecked; may already be correctly filed |
| `draft` | Being written; incomplete or provisional |
| `reviewed` | Checked for clarity, completeness, and supporting evidence |
| `established` | Accepted as reliable; protected from casual revision |

Use `document-maturity` on prose knowledge notes (`2-areas/` non-plan notes, `3-resources/`, MOCs). Choose it from actual review and acceptance, not the filename, destination, or `type`. `developing` and `refining` are not supported maturity values.

### `state` (`daily-tasks` `RecordKind` work records)

| `RecordKind` (`type`) | Canonical Path | `state` Domain Type & Allowed Values |
|---|---|---|
| `project` | `1-projects/YYYY.MM.DD-<slug>/project-index.md` (or `1-projects/<slug>/`) | `ProjectState`: `not-started` \| `in-progress` \| `completed` \| `cancelled` |
| `milestone` | `1-projects/<project>/mN-<slug>/mN-<slug>.md` | `MilestoneState`: `not-started` \| `in-progress` \| `completed` \| `cancelled` |
| `task` | `1-projects/<project>/<milestone>/tN-<slug>.md` (or `tN-<slug>.md`) | `TaskState`: `not-started` \| `in-progress` \| `completed` \| `cancelled` |
| `blocker` | `1-projects/<project>/blockers/bN-<slug>.md` | `BlockerState`: `open` \| `resolved` |
| `daily-plan` | `2-areas/daily-plans/YYYY.MM.DD-daily-plan.md` | Daily selection snapshot (`timezone`, `date` / `created_at`, Carried Selection `↺` rows) |

Operational `state` describes work execution, not `document-maturity`; preserve them independently when a note carries both, and never require `document-maturity` on `RecordKind` work records. Completing work does not establish or change `document-maturity`.

When creating a prose document from a template or editing a template's metadata, read [template and output maturity](../../manage-file-operations/references/document-maturity.md).

### Legacy metadata compatibility

- **Legacy `status` on prose notes:** When `document-maturity` is absent on a prose note, read legacy `status` as maturity only if its value is exactly `raw`, `draft`, `reviewed`, or `established`. Operational values (such as `completed`, `in-progress`, `open`) do not establish `document-maturity` and must never be interpreted or renamed as maturity.
- **Conflicting maturity fields:** When both `document-maturity` and legacy `status` contain the same accepted maturity value, use that maturity without changing either field. When they disagree, or `document-maturity` is invalid, report the ambiguity and resolve it before work that depends on maturity. Do not select a winner silently or change unrelated operational `state`.
- **Retired `task-state` & hyphenated state aliases:** `para-vault`'s former `task-state` frontmatter field (and legacy `project-state`, `milestone-state`, `blocker-state` aliases) are retired in favor of `state`. Recognize them read-only when inspecting unmigrated legacy records, preserve untouched legacy files unless migration is explicitly authorized, and **never** write `task-state` on new or migrated work records.
- **Explicit migration gate:** New prose notes use `document-maturity` (without `status`), and new work records use `state` (without `task-state`). Reading, filing, editing, installing, or updating this skill does not authorize vault-wide migration of existing files. Rename a legacy field only with explicit user authorization for the affected files, preserving original creation dates, `canonical` authority, `state`, body, `## Definition of Done` items, and recoverable history.

### Authority and tags

`canonical` is an optional boolean on knowledge and policy notes, defaulting to `false` when omitted. Set `canonical: true` only with user authorization designating the document as the canonical source of truth. This is independent of `document-maturity`; do not infer canonical authority from a note being `established`.

When multiple canonical documents compete to govern the same purpose, the most recently designated canonical document wins. Sharing a subject alone does not make documents competitors: a canonical reconciliation procedure and a canonical monthly reconciliation record each govern their distinct purpose. Exclude unchanged preserved inbox originals and historical snapshots in `4-archives/`, even if their embedded metadata says `canonical: true`; use preservation context and companion metadata to identify them. An archived completed `Project` can still remain canonical for its own completed scope.

Determine precedence from documented canonical designation dates/times in the note bodies or reliable approval history; record the designation date/time when making a new authorized designation. Compare timestamps in a common timezone. Creation dates, filesystem modification times, import times, filename dates, and routine edits do not establish canonical precedence. If designation dates are missing or tied and approval history cannot establish which competing document governs, ask only when the unresolved conflict affects the task. A sole applicable canonical document remains authoritative even when its designation date is missing. Never invent a designation date or promote a noncanonical proposal by recency. Resolving which document to follow does not authorize rewriting or archiving the others.

When no applicable document is canonical, use relevant information according to its evidence and acceptance. Combine compatible information and resolve factual differences from supporting evidence where possible. Do not infer canonical authority from age, recency, maturity, or being the only document.

For prose knowledge notes, keep optional tags focused on cross-folder classification (`decision`, `policy`, `procedure`, `reference`, `analysis`) unless extended by user authorization or `daily-tasks` project/task tags. Preserve existing tags on `daily-tasks` work records and historical notes without silent removal. Avoid tags that duplicate the folder, `type`, `document-maturity`, `state`, or `canonical` designation.

## Date meanings and configuration

Explicit current user instructions take precedence over accepted vault conventions, which take precedence over defaults here. Do not rename historical records merely to impose a new convention. For new records:

| Date | Meaning |
|---|---|
| `created` / `created_at` | Date (or UTC timestamp on `daily-tasks` records) the record was first authored. Preserve a known original creation date when moving or importing an existing note; never reset on editing or filing. |
| `Project` folder prefix | Date the project was created (`1-projects/YYYY.MM.DD-<slug>/project-index.md`). Preserve a known original creation date when adding an existing project to `vault_root`. |
| `Daily Plan` filename prefix | Local calendar day being planned (`2-areas/daily-plans/YYYY.MM.DD-daily-plan.md`). |
| Email filename prefix and day folder | Received date for incoming mail; sent date for outgoing mail. If received time is unavailable, use sent timestamp and disclose that fallback in the capture body or index annotation. If neither is known, keep the `Inbox Capture` in `0-inbox/` and ask rather than invent a date. |
| Calendar filename prefix | Event start date, not invitation receipt date. Use `DTSTART` for a native recurring series and the occurrence start for a separately received exception. |
| Calendar week folder | Sunday ending the event start date's Monday–Sunday week. A September 23, 2026 event uses `we-2026.09.27/`. |
| Daily-note prefix | Day being described, even when written later. |
| Other document filename prefix | Date the document was produced ([naming defaults](../../manage-file-operations/references/naming.md)): signing date for an executed contract, publication date for a published report, creation date for a newly authored note. Unknown historical dates are never replaced with import dates. |
| `target_date` / `deadline` | Optional agreed target date (`YYYY-MM-DD`). Omit when no date is agreed; a missing target date never blocks `Project` or `Task` creation. Do not infer month-end from a project name. |
| `archived` | Date (`YYYY-MM-DD`) the item entered `4-archives/`. |

Locate existing accepted vault rules using [shared vault conventions](vault-conventions.md) before creating any settings note. Never store `.nyssa-ai/` files inside `vault_root`. For filing timezone, use a task-specific timezone explicitly requested by the user, then accepted vault rules or `NyssaAI.Configuration` timezone, then an explicitly supplied user timezone; ask when unknown timezone could change the filing day. Convert timestamped mail and events to that timezone for filing while retaining original timestamps and zones. All-day event dates remain their stated calendar dates.

When the task explicitly asks to persist vault-level prose conventions inside `vault_root`, update the designated note in `3-resources/rules/` under its protected-revision rules (or create `vault-settings.md` there with `type: note`, `created`, and justified `document-maturity`). Never write `.nyssa-ai/` configuration inside `vault_root`.

## Stable note

```yaml
---
type: note
created: YYYY-MM-DD
document-maturity: established
tags: []
---
```

## Draft note

```yaml
---
type: note
created: YYYY-MM-DD
document-maturity: draft
tags: [analysis]
---
```

## Map of Content (MOC)

Use `type: moc` for an area guide (`00-<area>-index.md`) or subtopic guide (`01-<subtopic>-index.md`). See [navigation](navigation.md#maps-of-content-guides-to-related-notes) for their purpose, filenames, placement, and creation rules. `Project` indexes use the `project` `RecordKind` schema below.

```yaml
---
type: moc
created: YYYY-MM-DD
document-maturity: draft
tags: []
---
```

## Project index

Place `project-index.md` at the root of `1-projects/YYYY.MM.DD-<slug>/project-index.md` (preserving existing `1-projects/<slug>/` or legacy `YYYY.MM.DD-<slug>-index.md` paths when maintaining an existing project). Projects use `type: project` (`RecordKind`) and `state` (`ProjectState`: `not-started` | `in-progress` | `completed` | `cancelled`) without requiring `document-maturity`. Omit `target_date` / `deadline` unless explicitly agreed.

```yaml
---
type: project
title: "Project Title"
state: not-started
created: YYYY-MM-DD
tags: []
---
```

When created or managed alongside `daily-tasks`, preserve all `daily-tasks` fields (`id`, `owner`, `assignee`, `created_at`, `updated_at`, `started_at`, `resolved_at`, `target_date`, `tags`) and milestone/task/blocker tables with `<!-- ref: UUID -->` comments intact.

## Work records (`daily-tasks` aligned)

### Milestone (`1-projects/<project>/mN-<slug>/mN-<slug>.md`)

```yaml
---
id: MILESTONE_UUID
type: milestone
title: "Milestone Title"
state: not-started
owner: "owner@example.com"
project_id: "PROJECT_UUID"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
---
```

Embed observable acceptance criteria under `## Definition of Done` (`- [ ] Criterion <!-- id: UUID -->`).

### Task (`1-projects/<project>/<milestone>/tN-<slug>.md` or `tN-<slug>.md`)

```yaml
---
id: TASK_UUID
type: task
title: "Task Title"
state: not-started
owner: "owner@example.com"
project_id: "PROJECT_UUID"
milestone_id: "MILESTONE_UUID"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
---
```

Embed observable acceptance criteria under `## Definition of Done` (`- [ ] Criterion <!-- id: UUID -->`). Never write retired `task-state`.

### External Blocker (`1-projects/<project>/blockers/bN-<slug>.md`)

```yaml
---
id: BLOCKER_UUID
type: blocker
title: "Blocker Title"
state: open
owner: "owner@example.com"
project_id: "PROJECT_UUID"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
---
```

### Daily Plan (`2-areas/daily-plans/YYYY.MM.DD-daily-plan.md`)

```yaml
---
id: PLAN_UUID
type: daily-plan
title: "Daily plan YYYY-MM-DD"
timezone: "IANA_TIMEZONE"
date: "YYYY-MM-DD"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
---
```

Preserve `My work`, `Delegated work`, and `Follow-up work` tables, Carried Selection markers (`↺`), and `<!-- ref: TASK_UUID -->` comments without time-fitting schedules.

## Inbox-only intent fields

While an `Inbox Capture` is in `0-inbox/`, it may include `filing-hint`, `context`, and `source`. Use these as filing signals. Before removing them from the working note, transfer any substantive context, rationale, relationships, and source attribution into its body without duplicating information already present. Remove purely procedural routing hints once applied; do not discard useful content merely because it appeared in an inbox-only field.

## Canonical rules note

```yaml
---
type: note
created: YYYY-MM-DD
document-maturity: established
canonical: true
tags: [policy]
---
```

Use this maturity and `canonical: true` designation only after explicit user acceptance and designation. See [protected revisions](revisions.md#protected-revisions).

## Archive fields

For an individually archived Markdown note, add these fields. For an archived `Project` bundle, add them to `project-index.md` (or its existing project index); they apply to the intact bundle without rewriting every child milestone, task, or blocker. For native `Source Record` files or unchanged historical snapshots, put them in the companion metadata note defined in [lifecycle](lifecycle.md#archive-workflow):

```yaml
archived: YYYY-MM-DD
archived-from: 2-areas/area-name/original-note.md
archive-reason: superseded # completed | cancelled | stale | abandoned
```

`archived-from` is the exact original `vault_root`-relative file path, or the original project folder path for a bundle. On [reactivation](lifecycle.md#reactivation), retain their values as dated body history and remove them from the active item's frontmatter. Archiving alone does not change `document-maturity` or revoke valid `canonical` authority on a completed project's authoritative record.
