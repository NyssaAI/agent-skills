# Cursor and Grok Bot

Documentation checked 2026-09-30; verify the target version before generating files.

## Shared package

**Cursor** and **Grok Bot** share the same Cursor plugin packaging:

- Manifest: `.cursor-plugin/plugin.json` at the package root
- Skills: `skills/*/SKILL.md` (default folder discovery; keep the canonical skill tree)

Declare that the Cursor shim also covers Grok Bot. Do not maintain a separate
Grok Bot skill tree or a second manifest. Keep identity fields in
`.cursor-plugin/plugin.json` synchronized with root `plugin.json` (`name`,
`version`, `description`, `author`, `homepage`, `repository`, `license`,
`keywords`). Skills stay under `skills/`; do not invent a parallel layout.
[Cursor Plugins reference](https://cursor.com/docs/reference/plugins)

Example `.cursor-plugin/plugin.json` (identity only; skills use default discovery):

```json
{
  "name": "research-tools",
  "version": "0.1.0",
  "description": "Research workflows with reusable source checks",
  "author": { "name": "Example" },
  "homepage": "https://github.com/example/research-tools",
  "repository": "https://github.com/example/research-tools",
  "license": "MIT",
  "keywords": ["skills", "workflows"]
}
```

Replace example identity with the real plugin values. Optional Cursor component
paths (`rules`, `agents`, `commands`, `hooks`, `mcpServers`, `variables`) are
host-specific and must not become a second authored workflow copy of the shared
skills.

## Installation and activation

### Cursor

Install through the Cursor marketplace or an InstallPlugin / team marketplace
flow that places the package in the Cursor plugin cache. An arbitrary repository
clone does not register the plugin. After install or update, verify skills appear
in a new session and that one representative skill can be invoked.

### Grok Bot

Grok Bot consumes the same `.cursor-plugin/plugin.json` + `skills/` package.
**Grok Bot has no SessionStart hooks.** Do not promise always-on foundation
injection via hooks for Grok Bot. Keep foundational guidance discoverable through
skills and load it on demand (foundation on-demand). Record missing SessionStart
as a known Grok Bot limitation in the coverage matrix rather than inventing a
hook adapter.

### Fallback when marketplace install is unavailable

If marketplace or InstallPlugin cannot run, use a documented host-supported
fallback such as **UpdateState** or a workflows copy into the host's expected
plugin/skills location. Prefer the host's official install path when available.
Document the exact destination used, keep the copy generated from canonical
source, and re-verify after updates. Never hand-edit an installed cache as source.

## Assembly and validation

`scripts/assemble.py` currently generates only the Antigravity project artifact
and the managed `AGENTS.md` foundation block. It does **not** emit
`.cursor-plugin/plugin.json`. Maintain that file as a **static host shim** in
source (same pattern as `.claude-plugin/plugin.json` and
`.codex-plugin/plugin.json`).

When adding or updating the Cursor shim:

1. Create or refresh `.cursor-plugin/plugin.json` so identity matches root
   `plugin.json`.
2. Confirm `skills/*/SKILL.md` remain the only skill authoring location.
3. Statically validate JSON and that internal skill links resolve
   (`python evals/plugin_checks.py` coverage / local packaging checks).
4. Do not claim marketplace install, SessionStart foundation, or fresh-session
   runtime behavior unless those were actually probed on that host.
5. For Cursor, note package support separately from verified runtime. For Grok
   Bot, explicitly note no SessionStart and foundation-on-demand only.

Optional Cursor-only components (rules, hooks, commands) may be added later as
thin adapters. They are not required for Markdown skill packaging shared with
Grok Bot.
