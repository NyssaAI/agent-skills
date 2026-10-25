# Workflow: Manage Vault Lifecycle

> [!IMPORTANT] Scope Directive
> This workflow handles archiving or reactivating PARA vault notes, native records, or entire project bundles, while preserving lifecycle metadata, provenance, and navigation links. It does NOT own filing new captures (owned by `file.md`) or performing raw file system moves/retries (owned by `manage-file-operations`).

Complete the requested lifecycle transition while preserving the item's identity, evidence, and useful navigation.

1. Read [shared vault conventions](../references/vault-conventions.md) and resolve the current owner and accepted archive/active destination. Use [classification](../references/classification.md) if ownership is undecided; `archived-from` is provenance, not an automatic return destination.
2. Read the applicable **archive workflow** or **reactivation** procedure in [lifecycle guidance](../references/lifecycle.md). Establish eligibility and any authority decision before moving. Keep project bundles intact and distinguish collisions before changing their names.
3. Prepare [archive metadata](../references/frontmatter-schemas.md#archive-fields), unchanged evidence, and companion notes as the lifecycle procedure requires. On reactivation preserve archive values in dated history before clearing the current archive fields. Use [protected revisions](../references/revisions.md#protected-revisions) before replacing established content.
4. Use [manage-file-operations](../../manage-file-operations/SKILL.md) for transfers, collisions, and recovery. Follow the vault [move checklist](../references/navigation.md#move-checklist) for indexes, attachments, companion links, and verification before source cleanup.
5. Report final locations, lifecycle and authority changes, preserved history, and unresolved decisions or references. Archiving or reactivation alone changes neither document maturity nor canonical authority.
