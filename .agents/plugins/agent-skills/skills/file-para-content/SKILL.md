---
name: file-para-content
description: "Choose a PARA home, file notes or captures, process a vault inbox, or create a project and its index. Use in a recognized PARA vault when placement or inbox processing is the task."
metadata:
  version: "0.1.2"
---

# File PARA Content

Choose a working home or file content in a recognized PARA vault. This workflow also creates a requested project's folder and index. For a placement-only request, give the decision and rationale without changing files.

## Establish the destination

Read [vault conventions](references/vault-conventions.md) to resolve accepted locations and governing rules. Use [classification](references/classification.md) when ownership is undecided and [folder conventions](references/folder-conventions.md) for the actual layout. Preserve the user's destination and existing scheme.

## File the content

New content with a known destination can be filed directly. Content already captured in an inbox follows the inbox workflow below, even when its destination is known. This includes source records held while required filing information was unresolved; process them once that information is resolved.

For newly authored content with a known home, create it there using the applicable [note schema](../revise-vault-documents/references/frontmatter-schemas.md), [naming guidance](../manage-file-operations/references/naming.md), and [index ownership rules](../maintain-vault-navigation/references/navigation.md#index-ownership-and-links). There is no captured original to preserve or inbox stage to create. For an existing inbox capture:

1. Inspect `filing-hint`, `context`, `source`, maturity, authority, and any tags. Apply [protected-revision rules](../revise-vault-documents/references/revisions.md#protected-revisions) before substantive editing.
2. Resolve the destination from the user or accepted folder conventions. Use [PARA classification](references/classification.md#evaluation-order) when choosing among its four categories; apply [vault folder conventions](references/folder-conventions.md) for the actual layout and source-record destinations. Leave a capture in the inbox if its destination or usefulness remains unresolved; uncertainty is not grounds for archiving.
3. Preserve an unchanged original in the preserved-originals location, applying collision handling. These preserved originals are historical evidence, not competing current canonical documents, even if their captured metadata says otherwise.
4. On the working note, correct metadata and apply the [inbox intent-field rule](../revise-vault-documents/references/frontmatter-schemas.md#inbox-only-intent-fields), preserving substantive context in the body before removing those fields. Filing alone promotes neither maturity nor authority. Preserve native formats unchanged.
5. Apply the naming and date rules; move the working note without overwriting another item. Follow the [move checklist](../maintain-vault-navigation/references/navigation.md#move-checklist) to update source and destination indexes and working-folder registers, repair affected references, and verify the result before removing the working source.
6. Add `## Related` only when clear, valuable links exist.

If a note is not useful, delete only with explicit user authorization; otherwise archive it with a reason, subject to the [archive exclusions](../manage-vault-lifecycle/references/lifecycle.md#archive-workflow).

## Compose only the work needed

- For moves, copies, collisions, and recovery, use [manage-file-operations](../manage-file-operations/SKILL.md); apply the vault navigation checklist linked above before source cleanup.
- For supplied email/calendar identity, version precedence, or unresolved filing dates, use [import-vault-source-records](../import-vault-source-records/SKILL.md). It owns source interpretation; use this workflow only for its inbox filing steps.
- For project creation, use the [project schema](../revise-vault-documents/references/frontmatter-schemas.md#project-index) and [project identity convention](references/folder-conventions.md#project-identities); create only the working folders the task needs and connect the index to its owning Area. An unagreed deadline stays absent.
- When the requested result is archiving/reactivation, use [manage-vault-lifecycle](../manage-vault-lifecycle/SKILL.md); when it is reconciling or revising accepted content, use [revise-vault-documents](../revise-vault-documents/SKILL.md).

Report final homes, preserved originals, navigation changes, and any unresolved captures or placement decisions. Filing alone does not promote maturity or authority.
