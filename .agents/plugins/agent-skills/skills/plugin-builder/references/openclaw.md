# OpenClaw

Documentation checked 2026-09-29; inspect the installed host's format detection.

## Compatible bundles

Prefer the generic root Agent Plugins bundle when its shared skills and portable
`mcp.json` cover the requested capabilities. OpenClaw also recognizes Codex and
Claude bundles. Shared skills can use this route without a native runtime
adapter. MCP bundle mappings can expose supported local stdio and remote HTTP
tools. Mapping is selective: Claude agents
become skill content; this does not preserve Claude subagent execution. Claude JSON
hook automation is detected but not executed, and Codex `.app.json` metadata does
not supply working integrations. Supported MCP configurations can expose tools in
embedded OpenClaw. [Bundle mappings](https://docs.openclaw.ai/plugins/bundles)

If several manifests coexist, check the documented detection precedence and inspect
which format actually wins. Do not assume the host merges every manifest. Separate
artifacts when a different winning format would drop required behavior.

## Native runtime plugins

Use a native plugin for OpenClaw-specific runtime capabilities. It requires root
`openclaw.plugin.json`; runtime entrypoint/package details belong in `package.json`
and implementation code. The manifest supplies an ID and configuration schema,
not executable registration. [Native manifest reference](https://docs.openclaw.ai/plugins/manifest)

Minimal manifest example:

```json
{
  "id": "research-tools",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

Replace the example ID and implement the actual entrypoint with the current plugin
SDK. Add real configuration properties when the capability needs them. Keep native
registration in its adapter rather than translating foreign hooks by filename.

## Installation and verification

When authorized, local development can use
`openclaw plugins install --link <plugin-directory>`. Inspect using
`openclaw plugins inspect <id>`; `--runtime --json` loads the plugin in the inspecting
process. Neither proves the running Gateway uses that code. Trigger the real
capability and observe its effect there. [Installation and runtime checks](https://docs.openclaw.ai/tools/plugin)

Record bundle format, enabled state, relevant policy, and the tested capability.
If native behavior is unnecessary, retain the simpler compatible bundle.
Use `.agents/packages/<name>/portable/` for the compatible bundle or a separate
destination for a native artifact. Explicit installation and enablement remain
required.
Follow [the OpenClaw project route](workspace-installation.md#openclaw-project-route)
for the link, inspection, enablement, and running-Gateway smoke test.
OpenClaw's `PLUGIN_DATA` is available to bundled stdio servers for runtime data;
keep user preferences in the separate `.{plugin-name}/` home.
