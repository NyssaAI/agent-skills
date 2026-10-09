---
trigger: always_on
description: Core file-management naming and safety rules.
---

# File-management foundation

Apply these conventions whenever a task creates or changes files or folders.
Follow the user's instructions and applicable local conventions before these
defaults. Use the user's destination or the existing folder scheme; do not
invent a new top-level organization. Preserve names and extensions unless a
rename is requested. Default new names to lowercase kebab-case; for time-bound
items, use the real creation or production date in `YYYY.MM.DD-descriptive-slug`.
Never invent an unknown date or substitute an import date.

Keep disposable task output under the working root's `.temp/`, separate from
retained deliverables, and preserve unrelated temporary work. Check identity and
collisions before writing; never overwrite unrelated content. Verify moved
content, links, and indexes before removing the source. Preserve recoverable
history for substantive revisions. Archive within the existing scheme. Delete
retained content only with explicit authorization.

Use `manage-file-operations` when moving, renaming, copying, importing, or
archiving existing content, resolving destination collisions, or resuming
interrupted operations. These foundation rules apply whether or not a skill is loaded.

## PARA foundation

Apply PARA guidance only in a recognized PARA vault. Follow the user's instructions
and accepted local rules before catalog defaults, preserving existing layout.
Each item has one current working home; preserved originals, historical snapshots,
and recovery copies are evidence/restoration exceptions. Placement follows current
use, not age, format, maturity, or authority. Load the relevant filing, navigation,
lifecycle, source-record, or document-revision skill only when its workflow applies.
