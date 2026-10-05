# Frontmatter Schemas

All new maintained Markdown notes require `type`, `created`, and `document-maturity`, including supporting notes and registers inside project working folders. Existing notes follow the legacy compatibility rule below. Frontmatter dates use ISO `YYYY-MM-DD`; filename date prefixes, where applicable, use `YYYY.MM.DD`. Undated filenames still retain `created` in frontmatter. Tags are optional YAML lists without `#`; omit the field or use `tags: []` when none are useful. Preserve native records such as `.ics` invitations in their native format without inserting YAML.

Disposable tool output in the resolved temporary location and unchanged preserved originals are exempt, including imported Markdown retained as original evidence inside a working collection. Do not retrofit metadata into preserved evidence. File extension or subdirectory placement alone does not establish this exemption.

## Field meanings

`type` identifies document form, independently of maturity, authority, location, and tags. For new notes use `note` (including email captures, daily notes, rules, and procedures), `moc` (area or subtopic guide), or `project` (project index). Preserve existing types; use additional types only when an accepted vault schema defines them. A procedure normally uses `type: note` and may use `tags: [procedure]`.

| Document maturity | Meaning |
|---|---|
| `raw` | Captured and unchecked; may already be correctly filed |
| `draft` | Being written; incomplete or provisional |
| `reviewed` | Checked for clarity, completeness, and supporting evidence |
| `established` | Accepted as reliable; protected from casual revision |

Use exactly one `document-maturity`. Choose it from actual review and acceptance, not the filename, destination, or document type. `developing` and `refining` are not supported maturity values. Operational fields such as `project-state`, `milestone-state`, `task-state`, and `blocker-state` describe work, not document maturity; preserve them independently. Completing work does not establish or change document maturity.

### Legacy metadata compatibility

- When `document-maturity` is absent, read legacy `status` as maturity only if its value is exactly `raw`, `draft`, `reviewed`, or `established`. Other `status` values do not establish maturity and must not be interpreted or renamed as it.
- When both fields contain the same accepted maturity value, use that maturity without changing either field. When they disagree, or `document-maturity` is invalid, report the ambiguity and resolve it before work that depends on maturity. Do not select a winner silently or change unrelated operational metadata.
- New maintained notes use `document-maturity`; do not add a legacy `status` alias. Unchanged originals and historical snapshots retain their original metadata.
- Reading, filing, editing, installing, or updating this skill does not authorize migration of existing notes. Rename a legacy field only with explicit user authorization for the affected notes. Preserve its accepted value, original creation date, authority, body, operational fields, and recoverable history. If both fields already agree, authorized migration may remove only the redundant legacy field; conflicting or unrecognized values need explicit resolution first. Never run a vault-wide migration merely because this skill was updated.

### Authority and tags

`canonical` is an optional boolean, defaulting to false when omitted. Set `canonical: true` only with user authorization designating the document as the source of truth. This is independent of maturity; do not infer authority from a note being established.

When multiple canonical documents compete to govern the same purpose, the most recently designated canonical document wins. Sharing a subject alone does not make documents competitors: a canonical reconciliation procedure and a canonical monthly reconciliation record can each govern their distinct purpose. Exclude unchanged preserved inbox originals and historical snapshots, even if their embedded metadata says `canonical: true`; use preservation context and companion metadata to identify them. An archived completed project can still be authoritative for its own distinct purpose.

Determine precedence from documented canonical designation dates/times in the note bodies or reliable approval history; record the designation date/time when making a new authorized designation. Compare timestamps in a common timezone. Creation dates, filesystem modification times, import times, filename dates, and routine edits do not establish designation or canonical precedence. If designation dates are missing or tied and the available approval history cannot establish which competing document governs, ask only when the unresolved conflict affects the task. A sole applicable canonical document remains authoritative even when its designation date is missing. Never invent a designation date or promote a noncanonical proposal by recency. Resolving which document to follow does not authorize rewriting or archiving the others.

When no applicable document is canonical, use relevant information according to its evidence and acceptance. Combine compatible information and resolve factual differences from supporting evidence where possible. Do not infer canonical authority from age, recency, maturity, or being the only document. Ask only when an unresolved conflict affects the task; using a document does not itself designate it as canonical.

The optional tag vocabulary is closed to the five values below. Extend it only with explicit user authorization. Preserve unrecognized tags in existing notes until their migration is authorized; do not propagate them into new maintained notes or silently remove historical metadata.

Tags describe useful classifications across folders:

| Tag | Meaning |
|---|---|
| `decision` | Recorded decision and rationale |
| `policy` | Rule or governing expectation |
| `procedure` | Instructions for a repeatable activity |
| `reference` | Factual material for later consultation |
| `analysis` | Interpretation, comparison, or evaluation |

Avoid tags that duplicate the folder, `type`, `document-maturity`, operational state, or canonical designation. Do not use maturity or authority as tags.

## Date meanings and configuration

Explicit current user instructions take precedence over accepted vault conventions, which take precedence over defaults here. For conflicting canonical rules, apply the authority rule above; if the conflict remains unresolved, ask before dependent filing. Do not rename historical records merely to impose a new convention. For new records:

| Date | Meaning |
|---|---|
| `created` | Date this note was first authored. For a new transcription/import note, the capture date; preserve a known original note creation date when moving/importing an existing note. Never reset on editing or filing. |
| Project folder/index prefix | Date the project was created, normally when its project folder was first created. Preserve a known original project creation date when adding an existing project to the vault. Folder and index prefixes match, even if the index is authored later. Accounting period belongs in the slug/goal; deadline is separate. |
| Email filename prefix and day folder | Received date for incoming mail; sent date for outgoing mail. If received time is unavailable, use the message's sent timestamp and disclose that fallback in the capture body or the native record's index annotation. If neither is known, retain the record in the inbox and ask rather than invent a date. |
| Calendar filename prefix | Event start date, not invitation receipt date. Use `DTSTART` for a native recurring series and the occurrence start for a separately received exception. |
| Calendar week folder | Sunday ending the event start date's Monday–Sunday week. A September 23, 2026 event uses `we-2026.09.27/`. |
| Daily-note prefix | Day being described, even when the note is written later. |
| Other document filename prefix | Date the document was produced, following [file-management's naming defaults](../../file-management/SKILL.md#naming). Use the signing date for an executed contract and publication date for a published report. A newly authored note uses its own creation date. Preserve an existing document's production date on import; an unknown historical date is not replaced with the import date. |
| `deadline` | Optional agreed target date. Omit when no date is agreed; a missing deadline does not block project creation. Do not infer month-end from a project name. |
| `archived` | Date the item entered the archive. |

Creation is the default date meaning. The email, calendar, and daily-note conventions above are explicit exceptions; the project index shares its project's date for consistent naming. A report's coverage period or an event discussed in a document does not replace its production date; retain that context in the slug or body.

Locate existing accepted settings using [the vault-rule discovery procedure](../SKILL.md) before creating any settings note. For filing timezone, use a task-specific timezone explicitly requested by the user; otherwise use the accepted vault setting, then an explicitly supplied user timezone. If none is available, ask when timezone could change the day. Convert timestamped mail and events to that timezone for filing, while retaining original timestamps and zones. All-day event dates remain their stated calendar dates. Do not infer missing source timezones.

When the task calls for persisting settings in the vault, update the existing designated rules note under its protected-revision rules; do not create a competing file. Only if no such note exists, use `vault-settings.md` in the resolved rules location with `type: note`, `created`, and the maturity justified by acceptance. Designation as canonical still requires user authorization. Read settings from clear body text; do not invent configuration schema keys. A skill-only update does not itself require editing vault documents.

For calendar version precedence, recurring-record preservation, and recovery of missing starts on reschedules or cancellations, follow [record-update handling](file-workflows.md#source-records-and-project-identities). Folder paths and source ownership are defined in [source-record destinations](folder-conventions.md#source-record-destinations).

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

Use `type: moc` for an area guide or subtopic guide. See [navigation](navigation.md#maps-of-content-guides-to-related-notes) for their purpose, filenames, placement, and creation rules. Project indexes use the separate schema below.

```yaml
---
type: moc
created: YYYY-MM-DD
document-maturity: draft
tags: []
---
```

## Project index

Name the index `YYYY.MM.DD-project-slug-index.md` at the root of its matching `YYYY.MM.DD-project-slug/` folder. Supporting working-folder registers use the note schema; they do not create separate project identities.

```yaml
---
type: project
created: YYYY-MM-DD
document-maturity: draft
tags: []
goal: "concrete outcome"
---
```

Add `deadline: YYYY-MM-DD` when a target date is agreed; otherwise omit the field.

## Inbox-only intent fields

While a note is in the resolved inbox location, it may include `filing-hint`, `context`, and `source`. Use these as filing signals. Before removing them from the working note, transfer any substantive context, rationale, relationships, and source attribution into its body without duplicating information already present. Remove purely procedural routing hints once applied; do not discard useful content merely because it appeared in an inbox-only field. Keep the preserved original unchanged.

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

Use this maturity and authority only after acceptance and designation. See the protected-document rules in [file workflows](file-workflows.md#protected-revisions).

## Archive fields

For an individually archived Markdown note, add these fields. For a whole project, add them to its index; they apply to the bundle without rewriting every child. For native records or unchanged historical snapshots, put them in the companion metadata note defined in [file workflows](file-workflows.md#archive-workflow):

```yaml
archived: YYYY-MM-DD
archived-from: 2-areas/area-name/original-note.md
archive-reason: superseded # completed | stale | abandoned
```

`archived-from` is the exact original vault-relative file path, or the original project folder path for a bundle. These fields describe the current archive state; on [reactivation](file-workflows.md#reactivation), retain their values as body history and remove them from the active item's metadata. Archiving alone does not change maturity. Resolve canonical authority as described in the archive workflow.
