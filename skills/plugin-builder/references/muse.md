# Muse (provisional)

The user supplied a proposed Muse layout, not a verified loader specification:
`.agent/plugins/<name>/` with root `SKILL.md`, `plugin.json`, `shims/`,
`mcp-servers/`, and `bin/`. Include Muse in the default target inventory so it
is not silently forgotten. Before generating or installing a Muse artifact,
check its current first-party docs, version, manifest schema, discovery path,
tool execution policy, and context-loading behavior. Treat each item that
cannot be checked as unverified and do not claim runtime compatibility.

Keep canonical skills under root `skills/<name>/` and portable identity in the
source package. If Muse truly requires one root `SKILL.md`, generate a short
Muse-specific entry point that routes to the shared skills; do not move or
duplicate their detailed procedures. If its actual loader requires
`.agent/plugins/`, generate that install artifact from source rather than
changing the package home used by other harnesses.

Apply [the JSON executable contract](executable-contract.md) to operations
Muse invokes as processes. A skill shim cannot force its Markdown instructions
into an agent's context merely by executing; verify Muse's skill loader or
subagent API before promising that behavior. Use Muse's native MCP connection
when supported; a local MCP-client shim is an alternative only when necessary
and tested. Keep user settings in `.{plugin-name}/`, not the Muse artifact.

The provisional proposal asks for shim metadata, environment variable names,
and examples in `plugin.json`. Check Muse's actual manifest schema before
emitting those fields. The source `capabilities.json` can supply the data for
a generated Muse manifest without placing unsupported fields in the portable
root `plugin.json`.
