# Codex

Documentation checked 2026-09-29; verify the target version before generating files.

## Generic source package

For new plugins, use the portable Agent Plugins `plugin.json` at the package
root. Codex discovers root `skills/` and optional portable `mcp.json` from that
package. Use `.codex-plugin/plugin.json` only when a Codex-specific overlay or
compatibility path is required. Do not maintain a separate Codex skill tree.
[Packaging reference](https://developers.openai.com/plugins/build/plugins)

Minimal root `plugin.json`:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "research-tools",
  "version": "0.1.0",
  "description": "Research workflows with reusable source checks"
}
```

Replace example identity with actual values. Add listing metadata only as
required by the install or publication surface. Existing compatibility packages
can keep `.codex-plugin/plugin.json` while being updated; that is a migration
constraint, not a second authored workflow.

Skill discovery supplies metadata before invocation, not an always-on foundation.
If the plugin promises startup rules, provide them through a verified Codex
startup context mechanism and keep the maintained text in shared source. Do not
assume a plugin-cache `AGENTS.md` will be loaded. Test foundation availability
before the router or another skill is invoked.

## Components and distribution

Use portable root `mcp.json` for a bundled local or remote MCP server. Its
entries declare transport, such as stdio or streamable HTTP. Keep Codex-only
hooks and app mappings in the Codex extension or compatibility overlay; avoid
competing declarations in both. Do not rename a Claude `.mcp.json` and assume
the schema matches. Marketplace `source.path` resolves from the marketplace root,
not its `.agents/plugins/` subdirectory. Local installs use a cached copy. [Packaging and marketplace rules](https://developers.openai.com/plugins/build/plugins)

Resolve the user's requested personal or repository catalog before writing one.
For a project install, a marketplace entry can point to a package staged under
`.agents/packages/<name>/portable/`; the marketplace's `source.path` must resolve from
the repository root. Enable it through the supported project configuration
when required. Root `AGENTS.md` may describe the package location and load a
lean startup foundation, but does not install the plugin by itself.
Inspect available `codex plugin` commands for the installed version and verify the
resolved package source. Reinstall or refresh through that version's supported
flow, then test in a new session. Do not assume a bundled validator implements
newer documentation: report version/schema disagreements explicitly.
