---
name: para-vault
description: "Apply PARA vault conventions. Use to choose among Projects, Areas, Resources, and Archives, or manage vault layout, inboxes, metadata, indexes, source records, and archiving."
metadata:
  version: "0.2.0"
---

# PARA Vault

Choose a folder based on the content's current use. Follow the user's stated purposes and existing category names.

## Evaluation order

Honor an explicit user-selected home or an applicable accepted ownership rule first. Otherwise evaluate in this order and stop at the first matching owner:

1. **Projects:** Is this primarily owned by a specific active effort with a defined outcome and completion point? Use that project's folder.
2. **Areas:** Is this maintained as part of an ongoing responsibility with a standard to uphold? Use that area's folder.
3. **Resources:** Is this retained for a current topic of interest, learning, or reusable reference need? Use the matching resource folder.
4. **Archives:** Is this inactive material from the other categories, retained for history or possible future reuse? Use Archives. Completed or paused project material belongs here when it has no continuing active owner.

If several folders within the matching category fit, retain an existing suitable home or resolve which one owns the content. Do not skip to another category to avoid the choice. If no category fits with confidence, resolve the missing context; uncertainty alone does not justify archiving.

## One home per item

Each piece of content has one current working home. Other contexts reference that home rather than maintaining duplicate working copies. Preserved originals, historical snapshots, and recovery copies are exceptions for evidence and restoration; they are not additional current working homes. Follow the preservation and cleanup rules in [vault workflows](references/file-workflows.md). A shared interview guide maintained by the recruiting Area stays there even when several hiring projects use it. A candidate evaluation belongs to its specific hiring Project.

Reevaluate placement when the content's role changes, including when archived material becomes active again. Relocate it when a different folder becomes its home; follow [reactivation](references/file-workflows.md#reactivation) when returning archived material to active use. Age, format, maturity, and authority alone do not determine placement.

For vault operations, resolve the accepted inbox, preserved-originals, archive, and rules locations before using them. In this catalog's default layout these are `0-inbox/`, `0-inbox/archive/`, `4-archives/`, and `3-resources/rules/`. Preserve other layouts; do not invent a top-level folder when a necessary location is unknown. Use [file-management](../file-management/SKILL.md#intermediate-work) for the working root's `.temp/` directory.

For decisions that depend on vault conventions, check a supplied rules path or configuration, then links in existing indexes, then the existing rules location. Use accepted rules found there; a filename alone does not establish authority. If no applicable rule exists, use the defaults in these references while preserving the existing layout. Resolve competing canonical rules through the authority rule in the schemas; ask only when the conflict affects the task.

Document maturity uses `document-maturity`, independently of operational fields such as `task-state`. Before interpreting legacy `status` or changing note metadata, follow the [compatibility and migration rule](references/frontmatter-schemas.md#legacy-metadata-compatibility); a skill update does not authorize changing existing vault notes.

Load the relevant guide on demand:

- [Folder conventions](references/folder-conventions.md) for vault locations, layout, source-record destinations, and archives.
- [Frontmatter schemas](references/frontmatter-schemas.md) for note metadata, maturity, authority, and dates.
- [Navigation](references/navigation.md) for maps, indexes, and attachments. For every move, rename, or archive, follow its move checklist. For an index check or repair request, reported moves outside the workflow, or stale links whose affected scope is unknown, follow its general index scan procedure.
- [Vault workflows](references/file-workflows.md) for filing, source records, revisions, temporary work, archiving, and reactivation.

Use [file-management](../file-management/SKILL.md) for general naming and operation safety.

The category definitions follow [Tiago Forte's PARA method](https://fortelabs.com/blog/para/). Single-folder ownership is an explicit rule for this skill.
