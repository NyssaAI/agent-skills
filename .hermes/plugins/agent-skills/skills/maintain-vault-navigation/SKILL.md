---
name: maintain-vault-navigation
description: "Review or repair a PARA vault's indexes, maps of content, registers, and links. Use for navigation checks, stale or ambiguous links, or moves made outside the managed workflow."
metadata:
  version: "0.1.0"
---

# Maintain Vault Navigation

Review or repair the requested collection's navigation without reorganizing its contents.

1. Resolve the request's scope and whether it is review-only. Read [shared vault conventions](../file-para-content/references/vault-conventions.md) for accepted rules and scan exclusions.
2. Read [navigation guidance](references/navigation.md) and follow its **general index scan**: discover indexes and registers by role, compare entries with actual content, and establish target identity before proposing a repair. Begin with the named collection; widen only when requested or the affected scope cannot be bounded.
3. For repair requests, fix links, annotations, useful missing entries, and duplicates within scope. Preserve uncertain entries with an explanation. For review-only requests, report findings without modifying files. If creating a justified map, use the [MOC schema](../revise-vault-documents/references/frontmatter-schemas.md#map-of-content-moc).
4. Verify intended targets, including headings and blocks; report scanned collections, changes, remaining ambiguity, and inaccessible scope.

Known moves use the [move checklist](references/navigation.md#move-checklist), composed with [manage-file-operations](../manage-file-operations/SKILL.md); they do not require an audit of every index. Copy/import links follow that skill's copy rules, retaining original references and resolving links from the copy.

Routine navigation edits do not need a proposal. If an edit changes accepted assertions or policy, apply [protected revisions](../revise-vault-documents/references/revisions.md#protected-revisions). This skill runs when requested or needed for the current task; it is not a background monitor.
