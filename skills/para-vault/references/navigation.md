# Navigation and Attachments

> [!IMPORTANT] Scope Directive
> This reference defines navigation guidelines, Maps of Content (MOCs), `project-index.md` files (`daily-tasks` aligned), `Daily Plan` references, wikilink formats, move checklists, and attachment conventions inside `vault_root`. It does NOT define general move mechanics (owned by `manage-file-operations`) or frontmatter schema definitions (owned by `frontmatter-schemas.md`).

Use `vault_root`'s existing collection roles and destinations. The Area and Project conventions below apply where those roles exist; they do not require creating PARA folders in non-PARA workspaces.

## Maps of Content: guides to related notes

A **Map of Content (MOC)** is a Markdown note (`type: moc`) that helps you understand and navigate a collection of related notes inside an Area:

- **Main map (L0, or level zero):** each Area has one, named `00-area-slug-index.md` (for example `2-areas/bookkeeping/00-bookkeeping-index.md`). It introduces the whole Area and provides access to its notes, active `Project` links, or subtopic maps. Its permanent filename has no date prefix.
- **Subtopic map (L1, or level one):** an optional note named `01-subtopic-slug-index.md`, created when the user requests it or it materially improves navigation through a coherent subtopic. Around 15 related notes is a useful signal, not a minimum. The main map links to it. Both map files remain at the Area root, including in optional email and calendar Areas when present. Subtopic index filenames have no date prefix.
- **No level-two maps (L2):** do not create maps beneath subtopic maps. Reconsider the topic boundaries if another level seems necessary.
- **Project index (`daily-tasks` aligned):** `project-index.md` stays at the root of `1-projects/YYYY.MM.DD-<slug>/project-index.md` (preserving existing `1-projects/<slug>/project-index.md` or legacy `YYYY.MM.DD-<slug>-index.md` files when already present). It records the `Project` outcome, `state`, optional agreed `target_date`, milestone/task summary tables (`mN-<slug>/mN-<slug>.md`, `tN-<slug>.md` with `<!-- ref: UUID -->`), `External Blocker` rows (`blockers/bN-<slug>.md`), and key working collections without needing to list every supporting file. Do not create a separate main MOC for a `Project`; local working-folder registers are supporting notes, not additional project identities.
- **Daily Plans (`2-areas/daily-plans/YYYY.MM.DD-daily-plan.md`):** dated `Daily Plan` documents link directly to selected `Task` and `External Blocker` records inside `1-projects/` with `<!-- ref: UUID -->` comments and Carried Selection (`↺`) markers; they do not require an `00-daily-plans-index.md` MOC unless requested.

Start an Area MOC with a short explanation of the subject and current understanding, followed by sections of links with brief descriptions, open questions, and links to related Areas and active `Project` indexes. The `00-` prefix identifies the main map and `01-` identifies a subtopic map; all subtopic maps share `01-`. Email/calendar records, `Daily Plan` records, and their day/week folders use dates instead of map-level prefixes.

## Index ownership and links

Update the owning Area MOC or `project-index.md` with useful annotated links when adding meaningful work or context. An Area's main MOC may reach notes and working folders through its subtopic MOC; do not duplicate every link at both levels. Link finite `Project` indexes from the Area that owns the ongoing responsibility. Link email and calendar `Source Record` files from relevant projects while keeping them at their resolved source-record destinations. For `3-resources/`, `0-inbox/`, and `4-archives/`, update an existing relevant index if present; do not invent a MOC or index solely to satisfy this instruction.

Use note-name wikilinks only when unambiguous across `vault_root`. Otherwise use `vault_root`-relative wikilinks, for example `[[2-areas/bookkeeping/00-bookkeeping-index|Bookkeeping]]` or relative milestone/task links with escaped table pipes (`[[m1-design/t1-spike\|Architecture spike]] <!-- ref: UUID -->`). Link attachments using the attachment rule below; for other native `Source Record` files, use relative Markdown links with the extension, resolving them from the linking note. Retain useful historical links and describe archived or superseded targets accurately. Routine link maintenance does not require a separate proposal unless it changes accepted assertions or policy.

## Move checklist

For every move, rename, or archive in `vault_root`, including an intact `Project` bundle:

1. Identify the source and destination owners and their existing MOCs, `project-index.md` files, `Daily Plan` files (`2-areas/daily-plans/`), and working-folder registers. Search maintained notes across `vault_root` for references to the old paths and filenames, including extensionless wikilinks. Resolve matches to their actual targets rather than replacing matching text blindly. Exclude `vault_root/.temp/` and external tool dot-folders from scans; preserve unchanged originals and historical snapshots without rewriting their links.
2. Update both source and destination navigation. Remove or relabel a source entry that presents the item as locally owned; retain a useful cross-reference to its new home. Add or update the destination entry where the index's purpose calls for it, preserving `<!-- ref: UUID -->` and Carried Selection (`↺`) markers on `daily-tasks` records. Follow the index-creation rules above rather than creating an index in every folder.
3. Repair affected inbound links, outgoing relative links, attachment references, and links within moved bundles for the final paths. Update descriptions that would otherwise misstate location, ownership, or archive status.
4. Verify the destination content and that changed links resolve to their intended targets, including heading or block references. Check the source and destination indexes for stale or duplicate entries, then repeat the old-reference search to find missed repairs. Old paths in `archived-from` provenance or historical descriptions remain when intentional. Finish these checks before removing a remaining working source; report any unresolved references.

## General index scan

Run this procedure when the user requests an index check or repair, reports moves made outside the workflow that affect the task, or stale links reveal that the affected scope is unknown. Start with the named collection; scan `vault_root` when requested or when the affected collections cannot be bounded. An ordinary known move uses the checklist above without requiring an audit of every index.

- Discover existing indexes through accepted naming conventions (`00-*-index.md`, `01-*-index.md`, `project-index.md`, or existing legacy `*-index.md`), `type: moc` or `type: project`, `2-areas/daily-plans/*.md`, and links from parent indexes. Inspect working-folder registers by their content and role; they may have `type: note` and names other than `*-index.md`.
- Compare index entries with actual files and folders. Check broken or ambiguous targets, stale location or lifecycle descriptions, duplicate entries, and meaningful content missing from the navigation the index is intended to provide. Indexes need not list every file.
- For a missing target, search for its current location and establish identity from UUID (`id` / `<!-- ref: UUID -->`), content, provenance, or reliable move history. Do not retarget a link solely because a filename matches. Apply routine repairs within the requested scope; for a review-only request, report findings without modifying files. Preserve unresolved entries and explain the uncertainty rather than deleting them or inventing targets.
- Recheck repaired links and summarize the collections scanned, repairs made, and unresolved items or inaccessible scope. Use the same exclusions (`vault_root/.temp/` and external tool dot-folders) as the move checklist.

## Attachments

Keep attachments at the locations selected by `vault_root`'s folder conventions (such as `inputs/` or `outputs/` in structured `daily-tasks` milestones/tasks, or beside their owning Area/Resource document), preserving their relationship to the owning document or working collection. Use a simple descriptive kebab-case document name with its original extension, such as `bank-statement.pdf`, without requiring a date prefix. Link from the owning Markdown document with `[[bank-statement.pdf]]` (or `[[inputs/bank-statement.pdf|Bank statement]]`); qualify the wikilink with the `vault_root`-relative path when the name is ambiguous. For a native `Source Record` owner that cannot contain wikilinks without changing its format, place the attachment link in its existing index annotation or companion Markdown capture. Preserve native attachment bytes and apply [general collision rules](../../manage-file-operations/references/safe-operations.md#identity-and-collisions) and [source-record identity rules](source-records.md#source-record-identity-and-updates). When moving or archiving an owner, preserve access to its attachments and repair affected links; do not remove an attachment still used by another document.
