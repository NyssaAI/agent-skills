# CLI and MCP capabilities

Treat a CLI, a local MCP server, and a remote MCP server as ways to expose a
capability, not separate skill trees. Define the operation first: its name,
inputs, result, side effects, errors, authorization, and version. Shared skills
describe when to use it and how to judge the result. Host adapters bind that
contract to the executable or tool names available in each harness.
Read [the JSON executable contract](executable-contract.md) when adding a
process-call surface. It does not replace a host's skill loader or MCP transport.

| Surface | Implementation and connection | Use when |
| --- | --- | --- |
| CLI | Bundle or declare an executable and a small invocation wrapper; the host must have a permitted process tool and the correct platform/runtime | Work can run locally without a new tool protocol |
| Local MCP | Run a bundled or installed server over stdio; each host registers its own connection declaration | The agent needs discoverable structured tools backed by local code or data |
| Remote MCP | Register a reachable HTTPS MCP endpoint with host-supported authentication | The capability uses a service, shared data, or server-managed access |

When a plugin offers both CLI and MCP, make them call one shared implementation or
the same service API. Do not maintain two copies of business logic. A remote MCP
implementation may live in a separate service repository; record its API/tool
version and the plugin revision it is compatible with. If a host cannot execute
the CLI or connect to the chosen MCP transport, use another verified surface
backed by the same contract or report the capability unavailable there.

Keep a user-facing CLI executable at `bin/<plugin-name>` and a bundled local
MCP server executable at `mcp/<server-name>` in canonical source. Put shared
business logic in `lib/` or a named library. A single executable that genuinely
serves both roles may live in `bin/`, with the MCP declaration pointing to that
same file; do not copy it into two places. Bundle required runtime and platform
artifacts, or declare the external dependency and check it at setup. An
installed or generated host package must contain the executable at the path its
connection declaration uses. A CLI skill should name the actual
command in its selected procedure, avoid shell-specific assumptions, and check
exit status and produced artifacts. It must not claim a command ran merely
because the agent described one. Cowork packaging may require a separate
assembled artifact when a Code-only binary component is rejected.

## Platform builds

For every bundled CLI or local MCP executable, define the supported operating
system and CPU architecture matrix before packaging. Target Windows, Linux,
and macOS by default; include only architectures for which a working artifact
can be built and tested, and state any gaps. Build all platform variants from
the same source and operation contract. Keep platform binaries in clearly named
subdirectories such as `bin/windows-x64/` and `mcp/linux-arm64/`, or assemble
separate self-contained packages per platform. Do not edit compiled artifacts
or maintain platform-specific copies of business logic.

At installation or release assembly, select the matching executable and
generate the connection declaration for that artifact. A fixed `mcp.json`
command must never point to a Windows executable on Linux or to one CPU
architecture on every host. A portable launcher is another option only when
its runtime is packaged or declared and verified on all claimed platforms.
Preserve executable permissions on Unix-like systems and the executable suffix
needed on Windows. Verify the packaged path, startup, and representative call
on each claimed platform; static inspection alone is not runtime evidence.
If a platform cannot be exercised, mark that platform unverified rather than
using a result from another operating system.

Keep the connection metadata at package-root `mcp.json` in each distributed
artifact, generating that file from the canonical contract when its command
path varies by platform. Translate it into host-specific declarations when a
host requires another schema. A local
stdio declaration launches the bundled server through a host-supported path
relative to the installed plugin root; verify path resolution on every claimed
platform. The server writes only MCP protocol messages to stdout and diagnostics
to stderr. This is distinct from the one-shot JSON stdout contract for agent
shims. A remote declaration points to a running service and needs no server
binary in the plugin. Do not put credentials or user-selected endpoints into distributed
manifests. Store non-secret endpoint preferences under the external
`.{plugin-name}/` settings home; use host-supported secret storage or
environment references for credentials. A portable `mcp.json` may declare a
fixed bundled server or stable service endpoint. When the endpoint varies by
user or project, the setup entry point must read `.{plugin-name}/` and register
the resulting host connection; a static manifest cannot infer that choice.
Apply [explicit settings resolution](package-organization.md#explicit-settings-resolution)
to CLI invocations and MCP calls. The installed executable path locates code,
not the user's project. Bind a single-project server explicitly or pass scope
per request for a multi-project server. Resolve client preferences locally for
remote MCP and forward only operation-required non-secret values; registering
an endpoint alone does not provide per-request project settings.
Limit the advertised tools and schemas to what the plugin needs, since
unnecessary tool descriptions consume context.
Register and test the connection separately from the skill. A skill file does
not start a server or prove the model can call its tools.

Validate each promised surface through the actual harness: CLI invocation on a
representative fixture; local MCP startup, discovery, tool call, and shutdown;
or remote MCP reachability, authentication, discovery, and tool call. Exercise
invalid input and unavailable-dependency behavior. Then evaluate the skill's
choice of capability and its use of the result. Record which host and transport
were actually tested. Follow current host schemas rather than copying one MCP
configuration file into another format.

Current host references: [Codex packaging](https://developers.openai.com/plugins/build/plugins),
[Claude plugin MCP](https://code.claude.com/docs/en/plugins-reference),
[Hermes MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp/),
and [OpenClaw bundles](https://docs.openclaw.ai/plugins/bundles).
