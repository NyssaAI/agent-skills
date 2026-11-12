# Workflow: Manage Vault Lifecycle

> [!IMPORTANT] Scope Directive
> This workflow handles archiving or reactivating `vault_root` notes, native `Source Record` files, or entire `Project` bundles (`1-projects/`), while preserving lifecycle metadata (`state`, `archived`, `archived-from`, `archive-reason`), `## Definition of Done` checklists, and navigation links. It does NOT own filing new captures (owned by `file.md`) or performing raw filesystem moves/retries (owned by `manage-file-operations`).

Complete the requested lifecycle transition in `vault_root` while preserving the item's identity, evidence, and useful navigation.

1. Read [shared vault conventions](../references/vault-conventions.md) and resolve the current owner and accepted archive/active destination (`4-archives/` or active `PARA Category`). Use [classification](../references/classification.md) if ownership is undecided; `archived-from` is provenance, not an automatic return destination.
2. Read the applicable **archive workflow** or **reactivation** procedure in [lifecycle guidance](../references/lifecycle.md). Establish eligibility and any `canonical` authority decision before moving. Keep `Project` bundles (`project-index.md`, `mN-<slug>/`, `tN-<slug>.md`, `blockers/bN-<slug>.md`, working collections, and attachments) intact and distinguish collisions before changing their names.
3. Prepare [archive metadata](../references/frontmatter-schemas.md#archive-fields), unchanged evidence, and companion notes as the lifecycle procedure requires. On reactivation preserve archive values in dated body history before clearing the current archive fields. Preserve `state` (`ProjectState`, `MilestoneState`, `TaskState`, `BlockerState`) on `daily-tasks` work records without writing retired `task-state`. Use [protected revisions](../references/revisions.md#protected-revisions) before replacing `established` content.
4. Use [manage-file-operations](../../manage-file-operations/SKILL.md) for transfers, collisions, and recovery. Follow the vault [move checklist](../references/navigation.md#move-checklist) for indexes, attachments, companion links, and verification before source cleanup.
5. Report final locations, lifecycle and canonical authority changes, preserved history, and unresolved decisions or references. Archiving or reactivation alone changes neither `document-maturity` nor `canonical` authority.
