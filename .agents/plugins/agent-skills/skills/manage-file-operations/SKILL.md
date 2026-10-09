---
name: manage-file-operations
description: "Safely move, rename, copy, import, or archive files and folders within an existing organization. Use when changing file locations or names, resolving destination collisions, or resuming interrupted operations. Preserve content, repair affected references, and verify completion."
metadata:
  version: "0.1.2"
---

# Manage File Operations

Complete the requested operation while preserving content and navigation. Follow
the user's instructions and applicable local conventions. If the host has not
loaded the [file-management foundation](core.md), read it before acting.

## 1. Establish the intended result

Identify the source items, requested operation, and destination. Use the user's
destination or the existing organization; do not invent a new top-level scheme.
Preserve names and extensions unless renaming is part of the request. When a
requested name depends on dates or naming exceptions, read the existing
[naming guidance](references/naming.md).

For a recognized PARA vault, read [shared vault conventions](../file-para-content/references/vault-conventions.md)
and, if placement is undecided, [classification](../file-para-content/references/classification.md).
For vault moves, renames, and archives, apply the [navigation checklist](../maintain-vault-navigation/references/navigation.md#move-checklist).
For archive/reactivation semantics, compose with [manage-vault-lifecycle](../manage-vault-lifecycle/SKILL.md).
For email/calendar import semantics, compose with [import-vault-source-records](../import-vault-source-records/SKILL.md).
Do not impose PARA on other workspaces or load unrelated vault workflows.

## 2. Inspect identity and existing work

Inspect the sources, intended destinations, affected references, and existing
folder indexes or registers before changing anything. A matching name alone
does not establish identity. For an import, copy, occupied destination, or
uncertain identity, read [identity and collisions](references/safe-operations.md#identity-and-collisions).

For a retry or evidence of a partially completed operation, first follow
[interrupted operations](references/safe-operations.md#interrupted-operations).
Reuse verified completed work and perform only the missing steps.

## 3. Perform the operation

Never overwrite unrelated content. Preserve native file contents and a folder's
internal structure unless the requested task includes changing them. Keep
recoverable history for substantive revisions needed by the operation.

A copy or import retains its source. A move, rename, or archive relocates the
working item; retain a recoverable source or rollback path until verification
is complete. Use the existing archive location when archiving. Do not interpret
an operation as permission to delete other retained content or reorganize
unrelated items.

## 4. Verify content and navigation

Verify destination content against the source or recorded pre-operation state,
accounting for intentional changes. For a move, rename, or archive, repair
incoming links and relative links inside relocated content, and update existing
source and destination indexes or registers.

For a copy or import, resolve outgoing links from the destination: links between
copied items should reach their copied counterparts, while links to items not
copied should retain their original targets. Adjust relative links in the copy
as needed; do not edit the source to make the copy work. Preserve existing links
and index entries pointing to the original unless the requested result calls
for changing them, and add the copy to the destination's existing index or
register. Verify the links resolve to the intended items, not merely to an
existing file with the same name.

Before removing a remaining working source for a move or archive, verify the
destination and affected references. If content diverges or verification fails,
preserve recoverable copies and report the unresolved difference; do not claim
completion or guess at lost evidence. Retain backups required by local policy.

## 5. Report the result

State the completed operations and final locations, including any collision
renames or reuse of existing items. Identify unresolved content or reference
issues and retained recovery copies that need attention. Report only the
verification actually performed.
