# Claude Code and Claude Cowork

Documentation checked 2026-09-29. Treat these as two runtime targets even when they
share one artifact.

## Shared package

Use `.claude-plugin/plugin.json` for identity. Keep `skills/`, `agents/`, `hooks/`,
and other components at the plugin root. Prefer skills over new legacy command
files. Component paths generally start with `./`, must exist, and stay inside the
package. Validate using `claude plugin validate <plugin-directory>` when available.
[Claude manifest reference](https://code.claude.com/docs/en/plugins-reference)

```json
{
  "name": "research-tools",
  "version": "0.1.0",
  "description": "Research workflows with reusable source checks"
}
```

This example relies on standard `skills/` discovery; replace its identity with the
real plugin details. Declare custom paths only when needed.

Generate this Claude manifest as a host adapter to the generic root package.
For MCP, declare the local stdio or remote HTTP connection in Claude's supported
`.mcp.json` or manifest `mcpServers` form. Do not copy portable `mcp.json` without
checking its schema and substitution rules. A Claude Code skill may call a
bundled CLI when the process tool and dependency are available; test that path
separately from MCP discovery. [MCP fields](https://code.claude.com/docs/en/plugins-reference)

Skill discovery does not put foundational rules into every session. A root
`CLAUDE.md` inside the plugin is not loaded as project context. If the plugin
promises an always-on foundation, implement and test a supported startup adapter
for each Claude runtime. Keep the foundation's maintained text in the shared
source and leave specialized procedures to skill selection. Test the router using
the runtime's native skill invocation.

## Claude Code

For an isolated local trial, load the package with
`claude --plugin-dir <plugin-directory>`. A marketplace belongs in
`.claude-plugin/marketplace.json`, separate from each plugin manifest.
Check the installed CLI help before constructing distribution commands.
[Loading and manifest rules](https://code.claude.com/docs/en/plugins-reference)
When registered from a project's `.agents/packages/<name>/portable/` or a
separate compatible artifact, keep shared location and
startup guidance in root `AGENTS.md`. Current Claude Code can read that file
directly when no project `CLAUDE.md` takes precedence; otherwise a small root
`CLAUDE.md` can import it with `@AGENTS.md` and add only Claude-specific guidance.
Neither file registers the plugin by itself.
[Project instruction precedence](https://code.claude.com/docs/en/memory)

## Cowork

Cowork accepts a `.zip` or `.plugin` upload containing one
`.claude-plugin/plugin.json`. The archive may contain the package folder or its
contents. Upload through Customize > Plugins > Add > Upload plugin when requested.
Account installation differs from a local Claude Code install.
[Claude plugin installation](https://claude.com/docs/plugins/overview)

Cowork supports skills, commands, agents, and hooks. Remote connectors require
reachable services; local MCP servers depend on desktop execution and organization
policy. Test the actual connection and execution environment.
[Runtime support](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)

Do not bundle Claude Code's `bin/` directory in a Cowork artifact: Cowork rejects
packages containing it. Separate artifacts when a Code-only feature requires it.
[Component support](https://code.claude.com/docs/en/plugins-reference)

Validate the archive's contents, then verify discovery and one representative
workflow in Cowork separately from Claude Code. A successful Code test is not a
Cowork test. If the UI is unavailable, deliver the archive and state that limit.
