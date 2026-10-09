# Shared Vault Conventions

Apply this guidance only in a recognized PARA vault. It is shared reference material; reading it does not start a filing or revision workflow.

If the [file-management foundation](../../manage-file-operations/core.md) is not already in context, read it before acting. Reading the foundation does not activate the file-operations workflow.

## Locations and governing rules

For vault operations, resolve the accepted inbox, preserved-originals, archive, and rules locations before using them. In this catalog's default layout these are `0-inbox/`, `0-inbox/archive/`, `4-archives/`, and `3-resources/rules/`. Preserve other layouts; do not invent a top-level folder when a necessary location is unknown. Use [file-management](../../manage-file-operations/references/intermediate-work.md) for the working root's `.temp/` directory.

For decisions that depend on vault conventions, check a supplied rules path or configuration, then links in existing indexes, then the existing rules location. Use accepted rules found there; a filename alone does not establish authority. If no applicable rule exists, use the defaults in these references while preserving the existing layout. Resolve competing canonical rules through the [authority rule](../../revise-vault-documents/references/frontmatter-schemas.md#authority-and-tags); ask only when the conflict affects the task. These conventions do not authorize reorganizing unrelated content.

Document maturity uses `document-maturity`, independently of operational fields such as `task-state`. Before interpreting legacy `status` or changing note metadata, follow the [compatibility and migration rule](../../revise-vault-documents/references/frontmatter-schemas.md#legacy-metadata-compatibility); a skill update does not authorize changing existing vault notes.


## Temporary work

Use [file-management's intermediate-work convention](../../manage-file-operations/references/intermediate-work.md). Disposable output, including Markdown output, needs no note frontmatter or index entry. Do not put scripts, exports, or backup folders at the vault root.

If output becomes a retained deliverable, file it in its known retained-content destination, add metadata if it is a maintained Markdown note, and update the applicable index. Verify the retained copy before cleanup.

## Dot-folders and ignore rules

Treat dot-folders other than the designated temporary workspace as external tool, sync, or version control directories. Exclude them from note scans, indexing, and file cleanup; do not move vault content into them or alter them as part of file maintenance.

Preserve root configuration and ignore files. Apply [file-management's `.temp/` exclusion rule](../../manage-file-operations/references/intermediate-work.md); other tool dot-folders follow accepted local ignore rules. Do not change unrelated configuration during filing.

For actual paths, read [folder conventions](folder-conventions.md). For ownership decisions, read [classification](classification.md).
