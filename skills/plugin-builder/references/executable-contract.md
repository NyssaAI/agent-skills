# JSON executable contract

Use this contract when an agent or host needs to call a plugin operation as a
local process. The shim is a small adapter over one shared operation. It does
not replace the canonical skill that tells an agent when and why to call it,
or an MCP server that the host can connect to directly. Do not create a shim
for a guidance-only skill just to fill a directory.

## Command behavior

- Name one operation with a stable verb-noun name, such as `search-tickets`.
  Put its entry point under `shims/` only when a local executable surface is
  needed. It may call the shared library, an existing CLI, or an MCP tool.
- Make it executable on each claimed platform, non-interactive, and callable
  without a shell-specific wrapper. `--help` must describe required flags,
  side effects, environment variable names, and exit behavior.
- Accept ordinary inputs as named flags. For structured or long values, allow
  an input-file flag so callers need not put sensitive or complex JSON in a
  shell command. Validate inputs before making side effects.
- For project-scoped operations, accept an explicit absolute `--project-root`
  and pass it to the shared resolver. Follow
  [settings resolution](package-organization.md#explicit-settings-resolution)
  for missing scope and remote calls; never use the shim's working directory
  as an implicit project selection. Describe scope in help and input metadata.
- Print exactly one JSON value to stdout on success. On failure, print one JSON
  object with an `error` string to stderr and exit nonzero. Keep logs, banners,
  prompts, and protocol traffic out of stdout. Document stable error codes if
  callers need to branch on them.
- A mutating operation must support `--dry-run` that reports its proposed effect
  as JSON without writing. If the underlying service cannot safely preview the
  effect, do not claim dry-run support or expose that write through this contract
  until a truthful preview is implemented.
- Read credentials from host-supported secret storage exposed through environment
  variables at invocation. Record variable **names**, never values. Do not embed
  credentials in the package, a command flag, an example, or checked-in settings.
  Keep non-secret user preferences in the separate `.{plugin-name}/` directory.

## Operation metadata

Keep portable identity in root `plugin.json`. Use root `mcp.json` for portable
MCP connections and host-specific registration files only where required.
Maintain a companion `capabilities.json` when executable shims exist. For each
shim, record its name, relative path, purpose, input and output JSON Schemas,
side-effect class, required environment variable names, and an invocation with
sample JSON output. Include the upstream CLI command or MCP server/tool mapping
when applicable. Treat this file as the plugin's own contract, not as a manifest
that hosts automatically discover. Generate host schemas from this contract
where practical and validate them against the installed host.

An MCP-backed shim uses a maintained MCP client and the declared transport;
do not implement an ad hoc JSON-RPC exchange that skips connection lifecycle,
tool discovery, structured results, errors, authentication, or shutdown. Prefer
the host's native MCP registration when it is available. Use a local MCP-client
shim only when the host can execute a process but cannot use the needed MCP
connection directly. A CLI-backed shim normalizes arguments and parses the
underlying command into the same output contract without hiding its failures.

## Documentation and verification

In the selected skill procedure or an on-demand reference, show a real, redacted
command and its observed JSON result for each shim. Keep the router and startup
foundation lean; link to these examples rather than pasting all of them into a
session-start file. Mark a sample as illustrative until it has been exercised.

For each claimed platform and host, run `--help`, a success case, invalid input,
missing credentials when relevant, and `--dry-run` for writes. Parse stdout and
stderr according to the contract, check exit status, and confirm dry-run left
the fixture unchanged. Then call the capability through each claimed harness:
direct shim success does not prove that an MCP server or skill was discovered.
Include these cases in the plugin eval suite and publish its current results.

References: [Agent Plugins package format](https://developers.openai.com/plugins/build/plugins),
[OpenClaw bundle mapping](https://docs.openclaw.ai/plugins/bundles), and
[MCP client tool calls](https://ts.sdk.modelcontextprotocol.io/v2/clients/calling).
