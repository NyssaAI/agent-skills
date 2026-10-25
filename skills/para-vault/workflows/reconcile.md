# Workflow: Reconcile Vault Documents

> [!IMPORTANT] Scope Directive
> This workflow handles reconciling overlapping or conflicting vault notes, proposing substantive revisions, and applying approved revisions while preserving document history and authority. It does NOT own filing new captures (owned by `file.md`), general file operations (owned by `manage-file-operations`), or archiving completed projects (owned by `archive.md`).

Revise or reconcile the named documents within the requested purpose and approval scope.

1. Read [shared vault conventions](../references/vault-conventions.md) to locate applicable governing rules. Inspect the documents, evidence, and existing approval history. Read the relevant [metadata and authority rules](../references/frontmatter-schemas.md), including legacy compatibility before interpreting maturity. A workflow update does not authorize metadata migration.
2. Follow [reconciliation and protected revisions](../references/revisions.md). Distinguish duplicates from independently authored notes; preserve unique content and provenance, identify contradictory claims, and separate supported resolutions from unresolved claims. Canonical precedence selects the governing document without automatically disproving every other claim.
3. For substantive changes to established notes, create the specified proposal unless the user has already approved that specific revision. Keep the accepted original and current links while approval is pending. Complete independent work and report only conflicts that block the requested result.
4. Apply approved changes using the protected-revision procedure: preserve durable accepted history, retain identity for the same purpose, and change authority only as authorized. For unchanged archive snapshots, use [companion metadata](../references/lifecycle.md#archive-workflow). Use [manage-file-operations](../../manage-file-operations/SKILL.md) when copies or moves are needed.
5. Check the result against the approved changes and preserved evidence. Update [relevant navigation](../references/navigation.md#index-ownership-and-links), mark applied proposals accurately, and report document paths, recovery history, acceptance/authority state, and unresolved claims.

Minor corrections and routine link maintenance can be applied directly with the recoverability required by the revision guidance. Read the schema directly for metadata-only questions; consulting it does not require starting a revision workflow.
