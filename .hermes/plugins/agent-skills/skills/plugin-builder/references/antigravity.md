# Google Antigravity

Cover Antigravity 2.0, Antigravity CLI, and Antigravity IDE by default. Check
the version and surface in use; sharing a product name does not prove identical
discovery or activation. The current project plugin location is
`.agents/plugins/<name>/`. A project-local package is an installed artifact
generated from the one canonical plugin source, not a second place to edit
skills. Inspect active components in the host after placement or installation.
Keep this artifact separate from `.agents/packages/<name>/portable/`. Generate
the Antigravity manifest in its own destination; never replace the generic
artifact's manifest or reuse a directory owned by another package format.

Antigravity's published root `plugin.json` schema names `name` and
`description` and sets `additionalProperties: false`; its example also shows
an editor `$schema` key. Generate a minimal manifest from the canonical plugin
identity and validate it in the target version. Do not assume a portable Agent
Plugins manifest with `version`, `extensions`, and other fields passes that
schema. Bundle shared `skills/<name>/SKILL.md`
and their references unchanged. Translate only needed runtime surfaces into
Antigravity's `mcp_config.json`, `hooks.json`, `rules/`, and `agents/` layout.
Do not copy portable `mcp.json` by renaming it; validate the target configuration
and tool calls. Keep user preferences outside the package in `.{plugin-name}/`.

Antigravity reads project `AGENTS.md` as an always-active rule. Use that shared
anchor or a generated, small plugin rule to load the lean foundation at startup.
Check that the rule is loaded once. Keep specialist procedures in skills for
on-demand activation. Do not mistake skill discovery, which starts with names
and descriptions, for loading the full foundation text. Antigravity's rules
support an explicit content include syntax; verify it in the installed version
before using it to share startup text without duplication.

For Antigravity CLI, `agy plugin list` can inspect installed plugins and
`agy plugin install <local-path>` can stage a local package. Direct project
placement is also documented. Test the route actually used, including a fresh
session, router invocation, and any CLI or MCP operation. A `gemini-extension.json`
is a Gemini CLI extension manifest, not the Antigravity plugin manifest; keep
the existing extension when the repository supports Gemini CLI, but do not
count it as Antigravity plugin validation.

Current primary references: [Antigravity plugins](https://antigravity.google/docs/plugins),
[skills](https://antigravity.google/docs/skills), and
[rules](https://antigravity.google/docs/rules).
