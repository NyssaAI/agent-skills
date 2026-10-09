# Navigation and Attachments

Use the vault's existing collection roles and destinations. The area and project conventions below apply where those roles exist; they do not require creating PARA folders.

## Maps of Content: guides to related notes

A **Map of Content (MOC)** is a Markdown note that helps you understand and navigate a collection of related notes. Think of it as the area's home page: it explains what the area covers, groups links by subject, and briefly explains why each linked note matters. It is a document, not another folder.

- **Main map (L0, or level zero):** each area has one, named `00-area-slug-index.md`. It introduces the whole area and provides access to its notes, directly or through subtopic maps. Its permanent filename has no date prefix.
- **Subtopic map (L1, or level one):** an optional note named `01-subtopic-slug-index.md`, created when the user requests it or it materially improves navigation through a coherent subtopic. Around 15 related notes is a useful signal, not a minimum. The main map links to it. Both map files remain at the area root, including in optional email and calendar areas when present. Subtopic index filenames also have no date prefix.
- **No level-two maps (L2):** do not create maps beneath subtopic maps. Reconsider the topic boundaries if another level seems necessary.
- **Project index:** `YYYY.MM.DD-project-slug-index.md` stays at the project root and records its goal and an optional agreed deadline. It guides users to key notes, milestone folders, and other working collections without needing to list every file. Do not create a separate main MOC for that project; local working-folder registers are supporting notes, not additional project indexes.

Start a map with a short explanation of the subject and current understanding, followed by sections of links with brief descriptions, open questions, and links to related areas. For example, `2-areas/bookkeeping/00-bookkeeping-index.md` explains bookkeeping practices and links to procedures and monthly reconciliation projects. Keep the map current as notes are added or changed. The `00-` prefix identifies the main map and `01-` identifies a subtopic map. All subtopic maps share `01-`; these prefixes indicate map level, not a running sequence. Area maps organize notes and working collections; a map does not require a matching folder. Email/calendar records and their day/week folders use dates instead of map-level prefixes.

## Index ownership and links

Update the owning area MOC or project index with useful annotated links when adding meaningful work or context. An area's main MOC may reach notes and working folders through its subtopic MOC; do not duplicate every link at both levels. Link finite projects from the Area that owns the ongoing responsibility. Link email and calendar records from relevant projects while keeping them at their resolved source-record destinations. For resources, inbox, and archives, update an existing relevant index if present; do not invent a MOC or index to satisfy this instruction.

Use note-name wikilinks only when unambiguous. Otherwise use vault-relative wikilinks, for example `[[2-areas/bookkeeping/00-bookkeeping-index|Bookkeeping]]`. Link attachments using the attachment rule below; for other native records, use relative Markdown links with the extension, resolving them from the linking note. Retain useful historical links and describe archived or superseded targets accurately. Routine link maintenance does not require a separate proposal unless it changes accepted assertions or policy.

## Move checklist

For every move, rename, or archive, including an intact folder bundle:

1. Identify the source and destination owners and their existing indexes, MOCs, and working-folder registers. Search maintained notes across the vault for references to the old paths and filenames, including extensionless wikilinks. Resolve matches to their actual targets rather than replacing matching text blindly. Exclude disposable temporary output and external tool dot-folders from scans; preserve unchanged originals and historical snapshots without rewriting their links.
2. Update both source and destination navigation. Remove or relabel a source entry that presents the item as locally owned; retain a useful cross-reference to its new home. Add or update the destination entry where the index's purpose calls for it. Include existing working-folder registers, and follow the index-creation rules above rather than creating an index in every folder.
3. Repair affected inbound links, outgoing relative links, attachment references, and links within moved bundles for the final paths. Update descriptions that would otherwise misstate location, ownership, or archive status.
4. Verify the destination content and that changed links resolve to their intended targets, including heading or block references. Check the source and destination indexes for stale or duplicate entries, then repeat the old-reference search to find missed repairs. Old paths in provenance or historical descriptions can remain when intentional. Finish these checks before removing a remaining working source; report any unresolved references.

## General index scan

Run this procedure when the user requests an index check or repair, reports moves made outside the workflow that affect the task, or stale links reveal that the affected scope is unknown. Start with the named collection; use the whole vault when requested or when the affected collections cannot be bounded. An ordinary known move uses the checklist above and its vault-wide reference search without requiring an audit of every index.

- Discover existing indexes through accepted naming conventions, `type: moc` or `type: project`, and links from parent indexes. Inspect working-folder registers by their content and role; they may have `type: note` and names other than `*-index.md`.
- Compare index entries with actual files and folders. Check broken or ambiguous targets, stale location or lifecycle descriptions, duplicate entries, and meaningful content missing from the navigation the index is intended to provide. Indexes need not list every file.
- For a missing target, search for its current location and establish identity from content, provenance, or reliable move history. Do not retarget a link solely because a filename matches. Apply routine repairs within the requested scope; for a review-only request, report findings instead. Preserve unresolved entries and explain the uncertainty rather than deleting them or inventing targets.
- Recheck repaired links and summarize the collections scanned, repairs made, and unresolved items or inaccessible scope. Use the same exclusions as the move checklist. This procedure runs during an agent task; it does not provide background monitoring.

## Attachments

Keep attachments at the locations selected by the vault's folder conventions, preserving their relationship to the owning document or working collection. Use a simple descriptive kebab-case document name with its original extension, such as `bank-statement.pdf`, without requiring a date prefix. Link from the owning Markdown document with `[[bank-statement.pdf]]`; qualify the wikilink with the vault-relative path when the name is ambiguous. For a native owner that cannot contain wikilinks without changing its format, place the attachment link in its existing index annotation or companion Markdown capture. Preserve native attachment contents and apply [general collision rules](../../manage-file-operations/references/safe-operations.md#identity-and-collisions) and [source-record identity rules](../../import-vault-source-records/references/source-records.md#source-record-identity-and-updates). When moving or archiving an owner, preserve access to its attachments and repair affected links; do not remove an attachment still used by another document.
