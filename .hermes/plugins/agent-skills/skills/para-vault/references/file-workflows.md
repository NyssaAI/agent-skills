# File Workflows

Use [para-vault](../SKILL.md) to resolve vault locations, [navigation](navigation.md) for indexes and attachments, [schemas](frontmatter-schemas.md) for metadata and dates, and [file-management](../../file-management/references/safe-operations.md) for general collision and interrupted-operation handling. These workflows do not authorize reorganizing existing content.

## Source records and project identities

For colliding new project names, append the [general collision suffix](../../file-management/references/safe-operations.md#identity-and-collisions) to the project slug and use that same slug in its index filename; do not suffix the index independently.

For email, retain Message-ID when available, sender, recipients, received/sent timestamps and zones, and source attribution in the body of a Markdown capture or in the native record. For invitations retain UID, recurrence identity, sequence/update metadata, and original timezone data in the native file. Do not add YAML to native formats. Matching titles alone do not prove identity. If no source identifier exists, compare content and provenance; do not discard uncertain matches.

An exact duplicate import needs no second file; link to the existing record. If the same source identity has a changed payload, preserve the stored record and retain the incoming version with collision handling. Import order alone does not establish which version is current. Do not silently replace a changed source record, and do not move historical versions merely to make all versions share a folder.

For calendar organizer updates and cancellations with the same UID and recurrence identity, compare `SEQUENCE` first (omission means zero under iCalendar), then `DTSTAMP` when sequences match. Only a newer applicable update changes current index links, event details, or cancellation state. Preserve an older import as labeled history without regressing the current record. If differing payloads tie or required ordering evidence is unusable, preserve both, flag the conflict, and leave the current designation unchanged until resolved. An attendee reply is not a replacement organizer update. A recurring series and its occurrence exceptions are distinct identities. See [iTIP revision ordering](https://www.rfc-editor.org/rfc/rfc5546.html#section-2.1.5).

File each invitation version at its applicable [source-record destination](folder-conventions.md#source-record-destinations), using the [date rules](frontmatter-schemas.md#date-meanings-and-configuration). A newer reschedule updates current links to its new destination while retaining a labeled link to the previous version; a newer cancellation is marked in index text. Keep a recurring invitation as one native series record; do not manufacture occurrence copies.

For a calendar update or cancellation without a usable event start, first match the original event by UID and recurrence identity. For a cancellation, use the matched event's applicable start date when recoverable. For a reschedule, recover the new start from the update or reliable associated source evidence; do not use the old date as if it were the new date. If identity or the required date remains unresolved, preserve the native payload in the inbox location and ask for the missing information. Use an undated descriptive filename such as `unresolved-calendar-update.ics`, with collision handling, until the event date is known. Explain the missing information in an existing relevant index annotation or a sibling Markdown capture (`type: note`, its own `created`, `status: raw`, `canonical: false`). Do not invent a filing date, substitute receipt date, or insert YAML into the native record. Once resolved, apply normal source-record filing and link maintenance.

For independently authored notes, overlapping text or subject matter alone does not establish redundancy. Preserve unique content and provenance, identify contradictory claims, and do not merge or archive merely because the notes overlap. When reconciliation is requested, distinguish supported resolutions from unresolved claims and apply protected-revision rules to substantive changes in established notes. Canonical precedence selects the governing document; it does not by itself disprove every differing claim. Ask only when an unresolved conflict prevents the requested reconciliation.

## Inbox processing

Known destinations allow direct filing. The inbox workflow applies to unclassified captures and to source records temporarily held because required filing information is unresolved. Once that information is resolved, process the held record using the steps below.

1. Inspect `filing-hint`, `context`, `source`, maturity, authority, and any tags. Apply protected-revision rules before substantive editing.
2. Resolve the destination from the user or accepted folder conventions. Use [PARA classification](../SKILL.md#evaluation-order) when choosing among its four categories; apply [vault folder conventions](folder-conventions.md) for the actual layout and source-record destinations. Leave a capture in the inbox if its destination or usefulness remains unresolved; uncertainty is not grounds for archiving.
3. Preserve an unchanged original in the preserved-originals location, applying collision handling. These preserved originals are historical evidence, not competing current canonical documents, even if their captured metadata says otherwise.
4. On the working note, correct metadata and apply the [inbox intent-field rule](frontmatter-schemas.md#inbox-only-intent-fields), preserving substantive context in the body before removing those fields. Filing alone promotes neither maturity nor authority. Preserve native formats unchanged.
5. Apply the naming and date rules; move the working note without overwriting another item. Follow the [move checklist](navigation.md#move-checklist) to update source and destination indexes and working-folder registers, repair affected references, and verify the result before removing the working source.
6. Add `## Related` only when clear, valuable links exist.

If a note is not useful, delete only with explicit user authorization; otherwise archive it with a reason, subject to the archive exclusions below.

## Protected revisions

For a substantive revision to an established note, create a sibling `<original-stem>-proposed-revision.md`, applying collision handling if necessary. This is a proposal, not an additional MOC or project index, so use `type: note`, its own `created` date, `status: draft`, and `canonical: false`. Link to the accepted original in the body and describe the proposed changes and supporting evidence. Preserve the original and its existing canonical links while approval is pending. An explicit instruction approving that specific revision already supplies approval; do not ask again.

After approval:

1. Preserve the accepted version in verified durable version history that can actually restore it. If such history is unavailable, save an unchanged snapshot as `YYYY.MM.DD-<original-stem>-prior-version.md` in the resolved archive location, using the snapshot date and collision rules. Create its companion metadata note as described below. Do not use the temporary location as the sole durable copy of an accepted version.
2. For the same document purpose, apply the approved content at the original path, preserving its original `created` date, filename, and canonical designation. Editing permission alone is not evidence that every new claim is established: use `established` when the user accepts the revised document as reliable, `reviewed` when it has been checked but not accepted, or `draft` while provisional. Preserve source evidence and useful content.
3. For a changed purpose, retain the original until the user approves a replacement and explicitly identifies which document becomes the source of truth. Transfer authority and redirect current links only as authorized; label the superseded document and preserve its history.
4. Update existing relevant indexes and mark the proposal as applied in its body, with a link to the accepted document. Archive it when authorized under the archive rules; do not leave it apparently pending or delete it without authorization.

Minor corrections and routine index maintenance can be applied directly when they preserve accepted meaning. Before overwriting, retain a recoverable copy in existing version history or the temporary location until the result is verified; substantive accepted-version preservation follows the durable procedure above. Do not use revision proposals to justify unrelated cleanup.

## Archive workflow

Do not automatically archive area MOCs, active area notes, or resource documents. Saving a prior-version snapshot during an approved revision preserves evidence; it does not move the current resource document. Archiving these requires a specific user instruction. A completed, abandoned, or superseded project can be archived as an intact folder, including its project index, after its lifecycle outcome is known. Preserve its complete working-folder structure, including nested Markdown, native documents, and attachments; do not flatten or ZIP the bundle to meet a depth preference. Use the accepted archive destination and preserve the bundle as a unit.

- Individual items go to the resolved archive location with their existing filenames, disambiguated on collision.
- Project bundles retain their existing folder name within the resolved archive location. If that folder name collides, stop to distinguish the same project from a different bundle rather than merging or silently renaming it. Add archive fields to the project index; those fields describe the bundle, including native children.
- Add `archived`, exact `archived-from`, and `archive-reason` to individually archived Markdown notes. Archiving does not replace maturity. Native records remain unchanged; use a companion metadata note for an individually archived native record or unchanged snapshot.

A companion metadata note is named `<archived-stem>-<extension>-archive-metadata.md` alongside the archived item, with the extension written as a slug without its dot, for example `2026.09.23-project-review-ics-archive-metadata.md`. Reserve both paths before writing; if either collides, disambiguate the archived filename and derive the companion name from it. The companion uses `type: note`, its own `created`, `status: raw`, `canonical: false`, and the archive fields. Its body links to the item and explains why it was preserved. For an unchanged snapshot, explicitly identify it as historical evidence, including any canonical flag captured inside it; that embedded flag does not confer current authority. This companion is metadata, not a new MOC.

Archiving alone does not revoke canonical authority: a completed project's authoritative record may remain canonical. For a superseded source of truth, identify the approved successor and set `canonical: false` on the superseded maintained note. Resolve competing canonical documents using the schemas' most-recent-designation rule. If the successor/authority decision remains unknown, resolve it before archiving a current canonical document as superseded. Selecting the current source of truth does not itself authorize moving or deleting older documents. Unchanged snapshots and preserved inbox originals are historical copies as described above.

Follow the [move checklist](navigation.md#move-checklist) for archive moves, including source and destination indexes and working-folder registers. A content-preserving move needs no extra permanent backup. If archive metadata edits would destroy needed original evidence, preserve an unchanged snapshot first. Never overwrite an unrelated archive item.

## Reactivation

When the task calls for returning archived material to active use, resolve its current owner through the user's instruction or PARA classification. The former `archived-from` path is provenance, not an automatic destination. Move a reactivated project as an intact bundle; resolve destination collisions without merging unrelated content.

Before removing `archived`, `archived-from`, and `archive-reason` from a reactivated maintained note or project index, preserve their values in a dated body history entry recording the return to active use. For an individually archived native record, move its companion metadata note with it, retain the archive details in that companion's body history, clear the companion's current archive fields, and update its link and description. Preserve the native payload. Reactivation alone changes neither original creation dates, maturity, nor canonical authority; a superseded document does not regain authority merely by moving.

Preserved originals and historical snapshots remain unchanged evidence. If their content is needed for current work, create or restore a working copy with appropriate metadata and provenance rather than converting the evidence copy into a maintained note. Apply protected-revision rules before replacing an existing established document.

Follow the [move checklist](navigation.md#move-checklist), including attachments and companion links. Update active navigation and relabel useful archive cross-references as reactivated; verify that the returned material is no longer described as currently archived. Leave unrelated historical copies and their archive metadata intact.

## Temporary work

Use [file-management's intermediate-work convention](../../file-management/SKILL.md#intermediate-work). Disposable output, including Markdown output, needs no note frontmatter or index entry. Do not put scripts, exports, or backup folders at the vault root.

If output becomes a retained deliverable, file it in its known retained-content destination, add metadata if it is a maintained Markdown note, and update the applicable index. Verify the retained copy before cleanup.

## Dot-folders and ignore rules

Treat dot-folders other than the designated temporary workspace as external tool, sync, or version control directories. Exclude them from note scans, indexing, and file cleanup; do not move vault content into them or alter them as part of file maintenance.

Preserve root configuration and ignore files. Apply [file-management's `.temp/` exclusion rule](../../file-management/SKILL.md#intermediate-work); other tool dot-folders follow accepted local ignore rules. Do not change unrelated configuration during filing.
