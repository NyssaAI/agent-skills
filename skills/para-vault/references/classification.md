# PARA Classification

> [!IMPORTANT] Scope Directive
> This reference defines the four `PARA Category` evaluation order (`Projects`, `Areas`, `Resources`, `Archives`) and single-home placement rules inside `vault_root`. It does NOT define folder naming conventions (owned by `folder-conventions.md`) or frontmatter metadata (owned by `frontmatter-schemas.md`).

Choose a folder inside `vault_root` based on the content's current operational use. Follow the user's stated purposes and existing category names.

## Evaluation order

Honor an explicit user-selected home or an applicable accepted ownership rule first. Otherwise evaluate in this order and stop at the first matching `PARA Category`:

1. **Projects (`1-projects/`):** Is this primarily owned by a specific active finite effort (`Project`) with a defined outcome and completion point — including its `project-index.md`, `Milestone` checkpoints (`mN-<slug>/`), `Task` items (`tN-<slug>.md`), `External Blocker` records (`blockers/bN-<slug>.md`), or project working collections? Use that project's folder.
2. **Areas (`2-areas/`):** Is this maintained as part of an ongoing responsibility with a standard to uphold, including `Daily Plan` documents (`2-areas/daily-plans/YYYY.MM.DD-daily-plan.md`), operational procedures, or recurring area records? Use that area's folder.
3. **Resources (`3-resources/`):** Is this retained for a current topic of interest, learning, or reusable reference need? Use the matching resource folder.
4. **Archives (`4-archives/`):** Is this inactive material from the other categories, retained for history or possible future reuse? Use Archives. Completed, cancelled, or abandoned `Project` bundles belong here when they have no continuing active owner.

If several folders within the matching `PARA Category` fit, retain an existing suitable home or resolve which one owns the content. Do not skip to another category to avoid the choice. If no category fits with confidence, leave an `Inbox Capture` in `0-inbox/` and resolve the missing context; uncertainty alone does not justify archiving.

## One home per item

Each piece of content in `vault_root` has one current working home. Other contexts reference that home rather than maintaining duplicate working copies (for example, a `Daily Plan` in `2-areas/daily-plans/` links to `Task` records in `1-projects/` via relative wikilinks and `<!-- ref: UUID -->` without duplicating task files). Preserved originals, historical snapshots, and recovery copies in `vault_root/.temp/` are exceptions for evidence and restoration; they are not additional current working homes. Follow the preservation and cleanup rules in [vault workflows](../SKILL.md). A shared interview guide maintained by the recruiting Area stays there even when several hiring projects use it. A candidate evaluation belongs to its specific hiring `Project`.

Reevaluate placement when the content's role changes, including when archived material becomes active again. Relocate it when a different folder becomes its home; follow [reactivation](lifecycle.md#reactivation) when returning archived material to active use. Age, format, `document-maturity`, `state`, and `canonical` authority alone do not determine placement.

The category definitions follow [Tiago Forte's PARA method](https://fortelabs.com/blog/para/). Single-folder ownership and `daily-tasks` work-record alignment are explicit rules for this catalog.
