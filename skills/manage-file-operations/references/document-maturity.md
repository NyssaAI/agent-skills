# Templates and document maturity

> [!IMPORTANT] Scope Directive
> This reference defines `Document Maturity` (`document-maturity`) inheritance for templates and derived knowledge notes. It does NOT define full YAML frontmatter schemas or `RecordKind` work-record states (owned by `para-vault/references/frontmatter-schemas.md`).

Use `document-maturity` for a prose template's own maturity; do not add a separate
`template-maturity` field. Supported values are `raw` (captured and unchecked),
`draft` (incomplete or provisional), `reviewed` (checked for clarity, completeness,
and evidence), and `established` (accepted as reliable).

A template's maturity describes the template, not documents created from it.
Do not copy that maturity or template-only provisional notices into new documents.
For knowledge and resource notes (`2-areas/` non-plan notes, `3-resources/`, MOCs),
choose each resulting note's `document-maturity` from its actual review and
acceptance; using an established template does not establish its output.

Structured `daily-tasks` work records (`RecordKind`: `project`, `milestone`,
`task`, `blocker`, `daily-plan`) are governed by `state` (`ProjectState`,
`MilestoneState`, `TaskState`, `BlockerState`) without requiring
`document-maturity`. Preserve operational `state` independently, never write
retired `task-state`, and apply the destination's metadata conventions.
