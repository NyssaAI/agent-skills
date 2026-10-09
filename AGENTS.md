# NyssaAI Agent Skills

This repository is the canonical public catalog of foundational skills and conventions for Jeremy and NyssaAI's AI agents, engineered for cross-agent compatibility across **Google Antigravity (AGY)**, **Claude Code**, **OpenAI Codex**, **Cursor**, **Grok Bot**, **OpenClaw**, and **Hermes Agent**.

## Repository Conventions

- **Skills Directory**: All skills reside under `skills/<skill-name>/`.
- **Primary Instruction**: Each skill must contain a `SKILL.md` with standard YAML frontmatter (`name:`, `description:`).
- **Progressive Disclosure**: Detailed guides, checklists, rules, and schemas belong in `references/` within the skill folder and are loaded on-demand.
- **Relative References**: All internal markdown links within a skill must use relative paths (e.g. `[Rules](references/para-rules.md)`), never host-specific absolute paths.
- **Private Documentation**: Keep `docs/` local and ignored by Git. Do not force-add or publish review or planning documents from that directory.
- **Agent Metadata**: Host-specific metadata stays scoped:
  - Codex / OpenAI UI: `skills/<skill-name>/agents/openai.yaml`
  - Claude Code: `.claude-plugin/plugin.json`
  - Codex Plugin: `.codex-plugin/plugin.json`
  - Cursor / Grok Bot: `.cursor-plugin/plugin.json` (shared shim; Grok Bot has no SessionStart)
  - Antigravity: generated `.agents/plugins/agent-skills/plugin.json`; `gemini-extension.json` is separate Gemini CLI metadata

## Available Skills

- **manage-file-operations** (`skills/manage-file-operations/`): Safely move, rename, copy, import, or archive existing content, resolve collisions, and resume interrupted operations. Its `core.md` owns the shared startup foundation; deferred conventions remain in its references.
- **file-para-content** (`skills/file-para-content/`): Classify and file vault content, process inbox captures, or create a project and its index. Owns shared classification, location, and folder guidance.
- **maintain-vault-navigation** (`skills/maintain-vault-navigation/`): Review and repair vault indexes, MOCs, registers, and links. Owns navigation and attachment guidance.
- **manage-vault-lifecycle** (`skills/manage-vault-lifecycle/`): Archive or reactivate vault items and intact project bundles, preserving history and lifecycle metadata.
- **import-vault-source-records** (`skills/import-vault-source-records/`): Ingest supplied email/calendar records, resolve versions and dates, and preserve native source evidence.
- **revise-vault-documents** (`skills/revise-vault-documents/`): Reconcile notes and propose or apply protected revisions. Owns shared metadata, maturity, and authority schemas.

<!-- agent-skills:file-management:begin -->
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
<!-- agent-skills:file-management:end -->
