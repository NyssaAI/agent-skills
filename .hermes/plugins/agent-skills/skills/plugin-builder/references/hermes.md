# Hermes Agent

Documentation checked 2026-09-29. Choose skills or native runtime extensions based
on the requested behavior.

Prefer the generic root Agent Plugins package when its supported skills and
`mcp.json` cover the capability. Hermes can also connect to user-configured
local stdio or remote HTTP MCP servers. Verify the installed version's package
and connection behavior instead of assuming a Claude declaration is portable.
[Portable plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins),
[MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp/)
For project installation, follow [the Hermes project route](workspace-installation.md#hermes-project-route): keep the portable artifact under `.agents/packages/<name>/portable/`,
generate the loadable copy from canonical source under `.hermes/plugins/`, enable the project-plugin
gate, then doctor, list, enable, and exercise the capability.
This catalog's `scripts/assemble.py write` generates a native Hermes package at
`.hermes/plugins/agent-skills/`. Its small Python adapter registers the shared
skills and loads `file-management/core.md` as a startup prompt section. The
project's managed `AGENTS.md` block supplies that text when present, so the
adapter avoids inserting the full core twice.
Hermes' host-managed `PLUGIN_DATA` may hold runtime caches; canonical user
preferences still live in the separate `.{plugin-name}/` home.

## Skills and taps

For instruction workflows, publish ordinary `skills/<name>/SKILL.md` directories
with their supporting resources. Hermes supports GitHub skill sources and taps;
a tap normally indexes a repository's `skills/`. Use `hermes skills inspect` before
installation and `hermes skills list` to inspect installed skills. Project skills
under `.hermes/skills/` or `.agents/skills/` require project trust. [Skills system](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)

Preserve the canonical skill tree and use the documented skill installation route.
Copying a Claude or Codex manifest does not register Hermes runtime tools.

## Native Python plugins

Native plugins use `plugin.yaml` plus Python registration, commonly `__init__.py`
with `register(ctx)`. User plugins live under `~/.hermes/plugins/`; project plugin
loading uses `.hermes/plugins/` and is separately gated. A generic package may
be staged under `.agents/packages/<name>/portable/`, but that path alone does not register a
native Hermes plugin. General third-party plugins require enablement;
discovery alone does not activate them. [Plugin reference](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/)

Minimal identity example:

```yaml
name: research-tools
version: "0.1.0"
description: Research tools for Hermes
```

This is only the manifest. Implement the actual tool schemas, handlers, and
registration against the target Hermes API. Consult its current manifest rules
for dependencies, environment requirements, and privileged capabilities. Keep
Python-specific behavior in the Hermes adapter.

The supported lifecycle includes `hermes plugins list`, `install`, `enable`, and
`disable`. Installation, dependency preparation, and capability grants are distinct
steps; respect their host controls. Plugin packs' declared `skills` are not yet
automatically installed according to the checked documentation. [Lifecycle and packs](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/)

When installation is in scope, verify both skill discovery and native tool calls
as applicable. Keep these results separate in the support report.
