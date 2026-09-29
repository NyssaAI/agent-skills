---
name: file-management
description: "Manage files and folders within an existing organization. Use for naming, creation, moves, revisions, archiving, time-bound names, and temporary workspace output."
metadata:
  version: "0.1.0"
---

# File Management

Create, rename, revise, move, and archive files and folders while preserving their content and existing organization. Follow the user's instructions and applicable local conventions before these defaults.

For work in a recognized PARA vault, also use [para-vault](../para-vault/SKILL.md). Its placement, metadata, navigation, protected-revision, and archive rules govern vault-specific operations; this skill supplies general naming and operation safety. Do not impose PARA conventions on other workspaces.

## Naming

- Use lowercase kebab-case slugs for new names unless the destination has an established convention. Preserve existing names and file extensions unless a rename is part of the task.
- For time-bound work or records, use `YYYY.MM.DD-descriptive-slug` as the file stem or folder name. The default date is when the document was produced or the folder was created. A project folder uses the project's creation date; an executed contract uses its signing date, and a published report uses its publication date. Keep the prefix stable through later edits or deadline changes.
- Preserve an existing document's original production date when copying, downloading, or importing it; those operations do not create a new document. A newly authored document uses its own creation date. Follow an explicit local date convention where one applies.
- Use `descriptive-slug` for enduring, undated items. If an existing document's production date is unknown, preserve its name or use an undated name rather than inventing a date.

## Intermediate work

- An AI working root, whether a project, folder, or other workspace, uses a `.temp/` directory for intermediate output. Create it at that root when needed if it does not exist. Keep scripts, exports, drafts, and other disposable work in a task-specific subdirectory such as `.temp/reconciliation-check/`.
- Exclude `.temp/` from Git and applicable sync services through supported configuration accessible within the task's authorized workspace. When the Git repository root is the working root, use `/.temp/` in its `.gitignore`. When the Syncthing folder root is the working root, use `/.temp` in its root `.stignore` (without a trailing slash). If the working root is nested, use the corresponding path relative to each repository or synced folder root. Preserve existing rules and verify that rule ordering allows the exclusion to take effect. Ignore rules do not untrack files already in Git; report those separately without silently removing them from the index.
- Syncthing does not sync `.stignore` itself; a verified local exclusion does not establish exclusion on other devices. Report unsupported or inaccessible sync settings and unverified devices. Do not expand ordinary file work into remote-device configuration or claim exclusions that were not verified.
- Keep retained deliverables in their intended permanent locations. Verify a retained copy before removing its intermediate version. Clean up only disposable files created for the current task; preserve unrelated `.temp/` contents.

## Safe operations

- Use the destination supplied by the user or the existing organization. Do not create a new top-level structure merely to complete a move.
- Check identity and destination collisions before writing. Preserve distinct content and source evidence; never overwrite an unrelated item. Follow [safe operations](references/safe-operations.md) for collisions and interrupted work.
- When moving or renaming, verify the destination content and repair affected links or references before removing the working source. Update existing source and destination folder indexes or registers to reflect the move, preserving useful cross-references. Keep recoverable history for substantive revisions.
- Archive in the existing archive location when the item's lifecycle or the user's instruction calls for it. Preserve a folder's internal structure and links. Delete retained content only when explicitly authorized.
