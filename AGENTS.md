# NyssaAI Agent Skills

This repository is the canonical public catalog of foundational skills and conventions for Jeremy and NyssaAI's AI agents, engineered for cross-agent compatibility across **Google Antigravity (AGY)**, **Claude Code**, **OpenAI Codex**, **Cursor**, **Grok Bot**, **OpenClaw**, and **Hermes Agent**.

## Repository Conventions

- **Skills Directory**: All skills reside under `skills/<skill-name>/`.
- **Primary Instruction**: Each skill must contain a `SKILL.md` with standard YAML frontmatter (`name:`, `description:`).
- **Progressive Disclosure**: Detailed guides, checklists, rules, and schemas belong in `references/` within the skill folder and are loaded on-demand.
- **Relative References**: All internal markdown links within a skill must use relative paths (e.g. `[Rules](references/para-rules.md)`), never host-specific absolute paths.
- **Agent Metadata**: Host-specific metadata stays scoped:
  - Codex / OpenAI UI: `skills/<skill-name>/agents/openai.yaml`
  - Claude Code: `.claude-plugin/plugin.json`
  - Codex Plugin: `.codex-plugin/plugin.json`
  - Cursor / Grok Bot: `.cursor-plugin/plugin.json` (shared shim; Grok Bot has no SessionStart)
  - Antigravity: generated `.agents/plugins/agent-skills/plugin.json`; `gemini-extension.json` is separate Gemini CLI metadata

## Available Skills

- **para-vault** (`skills/para-vault/`): Apply PARA placement and vault conventions for layout, metadata, indexes, and archiving.
- **file-management** (`skills/file-management/`): Manage files and folders generally, including time-bound naming, `.temp/` intermediate work, and safe operations within an existing folder scheme.
- **plugin-builder** (`skills/plugin-builder/`): Build and organize plugins with shared skills and target-specific packaging for Antigravity, Codex, Claude Code, Claude Cowork, Cursor, Grok Bot, Hermes Agent, OpenClaw, and provisional Muse.

<!-- agent-skills:file-management:begin -->
# File-management foundation

Follow the user's destination and existing folder scheme. Preserve names and
extensions unless a rename is requested. For new files, use lowercase kebab-case;
for dated files, use the real creation or production date in
`YYYY.MM.DD-descriptive-slug`, never an invented or import date.

Keep disposable task output under the working root's `.temp/`, separate from
retained deliverables. Check identity and collisions before writing. Verify a
move and its links before removing the source. Preserve recoverable history for
substantive revisions. Delete retained content only with explicit authorization.

Use `para-vault` only when the task concerns a recognized PARA vault. Load
file-management and PARA details from their skills only when needed.
<!-- agent-skills:file-management:end -->
