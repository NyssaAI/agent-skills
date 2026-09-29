# Package organization

Use one source method for every plugin: a generic package identity, a canonical
skill tree, an optional shared executable implementation, and the smallest host
adapters needed to expose it. Prefer the portable Agent Plugins root format for
new packages. Harnesses may require different manifests or assembled packages;
those are subordinate distribution interfaces, not separate authored workflows.

## Canonical source

```text
plugin-root/
  plugin.json                 # Generic package identity
  skills/
    router/                    # When several use cases share an entry point
      SKILL.md
      references/
    file-management/           # Example of a lean foundation
      SKILL.md
      references/
    para-vault/                # Example of selected guidance
      SKILL.md
      references/
  lib/                         # Shared implementation when needed
  bin/                         # Optional user-facing CLI entry or platform builds
  shims/                       # Optional JSON executables for operations
  capabilities.json            # Optional operation/shim contract
  mcp/                         # Optional local MCP server entry or platform builds
  mcp.json                     # Root MCP declaration; generate per platform if needed
  adapters/                    # Only for host-specific behavior, including AGY
  .claude-plugin/plugin.json   # When targeting Claude
  .codex-plugin/plugin.json    # Only for required Codex-specific compatibility
  evals/
    README.md                    # Suite and case catalog
    LATEST.md                    # Latest verified scores or explicit no-run state
    results/                     # Completed verified runs, including failures
    attempts/                    # Incomplete, aborted, and unverified run receipts
```

Maintain each skill and shared procedure once. Skills link to their own bundled
references with relative paths. A host may install a copy in its cache, but edits
start in the canonical source and propagate through release assembly. Do not edit
host caches or generated artifacts as source. Keep every referenced resource
inside the distributed package; do not rely on symlinks or links out of it.
Keep `evals/`, review receipts under `docs/`, and `.temp/` in the source
repository, not in assembled runtime artifacts. The evaluator runs the suite
from source against the already assembled artifact. This lets evaluation write
results and the latest report without changing the artifact it tested. If a
host installs directly from the repository root, build or stage a runtime-only
artifact first and test that exact artifact; do not count a whole-repository
copy containing changing eval evidence as byte-identical after evaluation.

The foundation contains only rules worth paying for in every session. Make its
shared text available through each target's verified startup mechanism; ordinary
skill discovery exposes a description, not necessarily the foundation's rules.
The router is a small user-facing entry point that loads one selected procedure
and its references. Specialized skills such as PARA remain discoverable and load
only for matching work. If a host has no way to provide the requested startup
behavior, record that target as unsupported for that capability.

Keep the package root separate from its project installation path. For this
catalog, `.agents/packages/<name>/portable/` is the preferred generic artifact
location for hosts with explicit registration. Use separate destinations for
incompatible formats, including `.agents/plugins/<name>/` for Antigravity's
generated project artifact. Generate each from canonical source and keep one
format's ownership of its destination; never convert a shared install in place.
The `.agents/packages/` path is our convention, not automatic host discovery.
Muse's `.agent/plugins/<name>/` still requires a verified loader.
A package still uses root `skills/` and portable
`plugin.json`, rather than one root `SKILL.md` that hides multiple skills.

## Host interfaces

The portable root `plugin.json` supplies generic identity and the root `skills/`
is the behavioral source. Root `mcp.json` describes portable MCP connections
when present. Codex, Hermes, and OpenClaw can consume supported portions of
that package; verify their actual format detection. Antigravity's documented
`plugin.json` schema has a different, narrow shape, so generate an Antigravity
package from the same source and skills. Claude requires its
`.claude-plugin/plugin.json` adapter for plugin distribution. Generate host-only
declarations from the same contract when a schema differs. Do not copy a root
MCP file by renaming it. Keep shim schemas, examples, and required environment
variable names in `capabilities.json` or a supported extension namespace; do
not add arbitrary top-level `shims`, `mcpServers`, or `requiredEnv` fields to
the portable `plugin.json`. Give all manifests consistent identity and version
fields while respecting their schemas. Plugin-level Claude `agents/` defines
subagents; a skill's `agents/openai.yaml` is Codex UI metadata. They are not
interchangeable. Verify actual discovery and invocation in each host.

Put native registration code in a named adapter such as `adapters/hermes/` or
`adapters/openclaw/`. It should translate host calls to the shared implementation,
not copy business logic. A Markdown-only workflow needs no executable adapter.
Assemble a self-contained release artifact when a host expects runtime files at
different paths or rejects a component. Generate each artifact from canonical
source and its adapter. Document and test the assembly command. A manifest alone
does not implement startup loading, a hook, or a tool.

Keep host-specific MCP, hook, command, and UI declarations scoped to the host.
Preserve the same behavior where supported, and test any behavior that a format
translation might lose. In particular, inspect OpenClaw's winning bundle format
when multiple manifests coexist.
Use [CLI and MCP capabilities](runtime-capabilities.md) for executable surfaces
and [workspace installation](workspace-installation.md) for project placement.

## User settings and preferences

Keep user-owned state in a tree separate from maintained plugin code, release
artifacts, and installed caches. The conventional homes are
`project-root/.{plugin-name}/` for settings governing that project and
`user-home/.{plugin-name}/` for personal settings.
These are state directories, not additional skill or manifest locations. Do not
store canonical preferences under `.agents/plugins/`, `.claude-plugin/`,
`.codex-plugin/`, or a host's plugin cache. Harness files may register the plugin
or point to its settings home, but the shared implementation reads the values
from the dedicated directory regardless of host.

Keep packaged defaults in source and write only user-selected values to the
external settings home. Document each setting's scope and precedence. Unless an
accepted project rule specifies otherwise, use explicit current instructions,
then applicable project settings, personal settings, and packaged defaults. Do
not promote a one-off task choice into a durable preference. Read only the
settings relevant to the selected task;
the existence of a settings directory does not make its entire contents startup
context. Keep credentials in a host-supported secret store or environment
reference rather than in a checked-in project settings file.
Keep private project state untracked; track shared team settings only when that
is intentional. If the project root is also the plugin source root, exclude its
`.{plugin-name}/` state directory from assembled plugin artifacts.

If an existing plugin kept user values in a host directory or installed package,
inventory and migrate them to the dedicated home without overwriting distinct
values. Update readers, verify the new path and precedence, then retire the old
copy only when safe. Package assembly must exclude local settings and test
fixtures must keep state separate from the installed code.

### Explicit settings resolution

For a project-scoped operation, each adapter must supply an absolute
`project_root` from an explicitly selected project or a verified host workspace
binding. Pass it as a CLI flag such as `--project-root` or an MCP request field.
Never infer it from the executable location, installed cache, or process working
directory. Validate the supplied root before reading or writing project state.

Use one shared resolver for executable surfaces. Resolve applicable values in
this order: explicit current-task settings, `<project_root>/.<plugin-name>/`,
`<user-home>/.<plugin-name>/`, then packaged defaults. A Markdown-only skill
follows the same procedure without adding a resolver executable. Document any
accepted project-specific precedence exception. Durable writes must name their
project or personal scope; a task override is not a request to save a preference.

When project scope is absent, personal operations may use personal settings and
defaults. An operation requiring project scope must report the missing scope
before project-dependent work; it must not guess or create a settings directory
under the package or cache.

A single-project local MCP process may receive an explicit root at startup if
its connection is bound to that project. A server serving multiple projects
must receive scope per request and keep resolved settings isolated per request;
do not use mutable global project state. A remote MCP server cannot resolve a
client's filesystem path. Resolve client settings locally and send only the
non-secret values needed for that operation, using an explicit server-side
project identifier when required. Never send the entire settings tree or treat
a client path as a server path. Keep authentication on its separate supported
channel. If the host cannot supply this context, add a thin client adapter or
report that project-scoped capability unavailable.

## Catalog and release

Group skills by cohesive user workflow and dependency requirements, not by
harness. Split plugins when users need separate installation, ownership,
permissions, or release lifecycles. Marketplaces index packages and use their
own schemas; resolve each entry's source path from that catalog's documented root.
Create only the catalogs needed for the selected targets.

Keep plugin name, publisher, purpose, and release version consistent across
artifacts for the same release. Record native ID mappings when required. Keep
secrets and machine-specific paths out of distributed files. Use host-supported
secret mechanisms where needed and the external settings home for user-writable
preferences and state.

Every plugin carries its own evaluation suite. Its latest completed run for the
current source and suite revision belongs in the repository and must be committed
and pushed to GitHub with the corresponding source. Follow
[validation and delivery](validation.md) for evidence, freshness, and failure
handling. Keep the case inventory in `evals/README.md` and the current score
receipt in `evals/LATEST.md`. Do not present an old or local-only run as the
current release result.

Publish failed results and blocked attempts with the candidate on a review
branch as well. Evidence publication and release approval are separate; use
the [completion rules](improvement-loop.md#completion-and-publication) to report
implementation, available-environment evaluation, and release readiness.
