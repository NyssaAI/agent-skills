---
name: file-management
description: "Manage files and folders within an existing organization. Use for naming, creation, moves, revisions, archiving, time-bound names, and temporary workspace output."
metadata:
  version: "0.2.0"
---

# File Management

The [lean foundation](core.md) is the canonical startup rule text. When the
host has not loaded it, read it before acting. Load the references below only
for the current operation.

Preserve content and the existing organization when creating, renaming,
revising, moving, or archiving. Follow the user's instructions and applicable
local conventions before these defaults. Use the user's destination or an
existing location; do not invent a new top-level scheme.

For a recognized PARA vault, also use [para-vault](../para-vault/SKILL.md) for
placement, metadata, navigation, and vault-specific safety. Do not impose PARA
on other workspaces.

## Naming

Preserve existing names and extensions unless renaming is requested. Default
new names to lowercase kebab-case. For time-bound items, use the original
production or creation date in `YYYY.MM.DD-descriptive-slug`; never substitute
an import date or invent an unknown date. Read [naming details](references/naming.md)
when choosing a date or resolving a naming exception.

## Intermediate work

Put disposable task output under the working root's `.temp/`, separate from
retained deliverables. Exclude it from Git and applicable sync where authorized;
preserve unrelated temporary work. Read [intermediate work details](references/intermediate-work.md)
when creating the directory, configuring exclusions, or cleaning up.

## Safe operations

Check identity and collisions before writing; never overwrite unrelated
content. Verify moved content, links, and indexes before removing a source.
Preserve recoverable history for substantive revisions. Archive within the
existing scheme; delete retained content only when explicitly authorized.
Read [safe operations](references/safe-operations.md) for collisions or
interrupted work.
