# Workflow: Maintain Vault Navigation

> [!IMPORTANT] Scope Directive
> This workflow handles reviewing and repairing PARA vault indexes, maps of content (MOCs), registers, and links. It does NOT own reorganizing vault content (owned by `file.md`), executing file renames/moves (owned by `manage-file-operations`), or revising note authority (owned by `reconcile.md`).

Review or repair the requested collection's navigation without reorganizing its contents.

1. Resolve the request's scope and whether it is review-only. Read [shared vault conventions](../references/vault-conventions.md) for accepted rules and scan exclusions.
2. Read [navigation guidance](../references/navigation.md) and follow its **general index scan**: discover indexes and registers by role, compare entries with actual content, and establish target identity before proposing a repair. Begin with the named collection; widen only when requested or the affected scope cannot be bounded.
3. For repair requests, fix links, annotations, useful missing entries, and duplicates within scope. Preserve uncertain entries with an explanation. For review-only requests, report findings without modifying files. If creating a justified map, use the [MOC schema](../references/frontmatter-schemas.md#map-of-content-moc).
4. Verify intended targets, including headings and blocks; report scanned collections, changes, remaining ambiguity, and inaccessible scope.

Known moves use the [move checklist](../references/navigation.md#move-checklist), composed with [manage-file-operations](../../manage-file-operations/SKILL.md); they do not require an audit of every index. Copy/import links follow that skill's copy rules, retaining original references and resolving links from the copy.

Routine navigation edits do not need a proposal. If an edit changes accepted assertions or policy, apply [protected revisions](../references/revisions.md#protected-revisions). This workflow runs when requested or needed for the current task; it is not a background monitor.
