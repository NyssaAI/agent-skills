---
name: plugin-builder
description: >-
  Build agent plugins for Antigravity, Codex, Claude Code, Claude Cowork,
  Hermes Agent, OpenClaw, and provisional Muse from one maintained core. Use
  for plugin packages, routers, startup utilities, CLI or MCP capabilities,
  host adapters, and project installation.
---

# Plugin Builder

Build each plugin from one maintained core. Use a generic package identity,
shared skills, and `AGENTS.md` as the primary project instruction anchor.
Harness files load that core and translate host interfaces; they do not contain
separate workflow copies. Follow [the single package method](references/package-organization.md).
Add host-specific files only as thin adapters where a target requires them.

## Assign content roles

Inspect the destination repository, its agent instructions, existing manifests,
skill inventory, release process, and uncommitted changes. Preserve its layout
unless the requested change requires reorganizing it.

Infer the plugin purpose and distribution scope. Unless the user explicitly
narrows the target set, build and evaluate for **all known targets**:
Antigravity (2.0, CLI, and IDE where applicable), Codex, Claude Code, Claude
Cowork, Hermes Agent, OpenClaw, and Muse. Distinguish Claude Cowork from Claude
Code even when they share a package. Muse has only the user-supplied shim
proposal so far; include it in the coverage matrix, but do not claim its
installation or runtime works without a verified loader and manifest schema.
Do not omit a target merely because its host is not installed locally: assemble
and statically validate what can be checked, then record the exact runtime gap.
Ask only for missing information that changes the implementation. Give
instructions one of these roles:

- **Foundation:** A few broadly useful rules needed before the agent knows to
  search. Load their shared source text at session start through each target's
  verified startup mechanism. Keep only the decisions and safety rules useful
  across ordinary tasks; point to details instead of loading them. In this
  catalog, file-management is foundational.
- **Router:** One small user-facing skill for multiple related use cases. It
  recognizes the request, loads only the chosen procedure, and verifies the
  result. Allow direct use of a specialist when the task already names it. Use
  the host's native invocation syntax. A single-purpose plugin may use its one
  skill as the router.
- **Selected guidance:** Specialized skills and substantial procedures that
  load only for relevant tasks. PARA is selected for vault work, not loaded at
  the start of every session.

Classify requested tools, MCP connections, hooks, subagents, UI, and providers
separately. Give each host a thin adapter where its interface differs, calling
the same shared implementation. A Markdown-only workflow may need no executable
adapter; its skill and references are the implementation.

For executable capabilities, define the operation once, then expose it through
a CLI, a local MCP server, a remote MCP server, or the smallest combination the
targets need. Follow [CLI and MCP capabilities](references/runtime-capabilities.md)
when the plugin calls code or an external service; skills select and evaluate
these capabilities but do not create a working connection by themselves.
Keep a bundled local MCP server under `mcp/` and its portable connection
declaration at package-root `mcp.json`; a remote MCP connection has no bundled
server binary. Keep a user-facing CLI under `bin/`. Both may call the same
shared implementation. For bundled executables, plan Windows, Linux, and macOS
artifacts by supported CPU architecture. The installed `mcp.json` or host
adapter must select a binary that runs on its actual platform; follow the
[platform packaging rules](references/runtime-capabilities.md#platform-builds).
When an operation needs a direct executable surface across harnesses, give it
the [JSON executable contract](references/executable-contract.md). Do not turn
a Markdown skill into a subprocess merely to make every capability look alike:
its instructions must enter agent context through a verified skill or startup
loader.

## Control context

Treat startup context as a scarce shared budget. Include a rule in the foundation
only when it is short, applies to many unrelated tasks, and must be available
before selection can occur. Keep examples, exceptions, host mechanics, and
substantial procedures in references. If a rule is useful only for a recognized
task, make it selected guidance. Do not load all skills or all references at
startup to make them discoverable.

Use shallow routing: load the selected procedure and only the references needed
for its current step. Avoid duplicate startup text across adapters and avoid
re-reading unchanged guidance. Reading a file does not guarantee that its
content leaves conversation context later; judge the total material a normal
task actually loads, not merely the size of each file.

For long sessions or handoffs, retain the selected route, source paths, and
current decisions in concise task state. Reload the needed canonical guidance
after compaction when necessary; do not copy whole procedures into every
handoff or assume the initial load survives unchanged.

## Keep user state separate

Store user settings and preferences in a dedicated `.{plugin-name}/` directory
outside the distributed plugin and installed caches. Use the project root for
project-scoped state and the user's home for personal state. Harness directories
such as `.agents/plugins/` hold registration and package files, not the
canonical preference store. Keep immutable defaults in plugin source; have each
host adapter pass explicit project scope to the same settings resolver; never
infer it from the process working directory or installed package. Define scope
and precedence for project and personal values, and load only task-relevant
preferences into context. Follow [package organization](references/package-organization.md#user-settings-and-preferences)
for layout, migration, and exceptions required by a host.

For project installs, prefer `.agents/packages/<plugin-name>/portable/` for
the generic artifact and register compatible hosts against it. Give incompatible
formats separate directories; Antigravity's generated project artifact lives
at `.agents/plugins/<plugin-name>/`. One package format owns each destination.
Make root `AGENTS.md` the shared instruction anchor. Omit `CLAUDE.md` when the
target Claude version reads `AGENTS.md` directly and needs no extra guidance;
otherwise use a small Claude-specific shim that imports it. Follow
[workspace installation](references/workspace-installation.md) for activation
rules and hosts that require another installed location.

## Apply the method

Read the references needed for the default target set, or for the subset the
user explicitly selected:

| Target | Read for |
| --- | --- |
| [Codex](references/codex.md) | Shared skills, Codex manifest, local catalogs |
| [Claude Code and Cowork](references/claude.md) | Shared manifest, different runtime and distribution checks |
| [Google Antigravity](references/antigravity.md) | Project plugin format, rules, skills, and three surfaces |
| [Hermes Agent](references/hermes.md) | Skills/taps versus Python runtime plugins |
| [OpenClaw](references/openclaw.md) | Compatible bundles versus native runtime plugins |
| [Muse](references/muse.md) | Provisional shim proposal; verify loader before claiming support |

These references apply the same method to each host; they are not alternative
authoring styles. Check current official documentation and installed versions
before relying on a schema, install command, or capability mapping. Record any
version mismatch and unverified assumption.

For each target, decide which capabilities work directly, need an adapter, or
remain unavailable. Keep useful supported behavior when an optional capability is
missing. If a required capability has no implementation on a target, report that
gap rather than claiming compatibility. Report coverage per target; a portable
source package alone does not make all seven runtimes supported.

## Build or reorganize

1. Choose a stable lowercase hyphenated plugin name and real publisher metadata.
   For a new package, put generic identity in root `plugin.json`; add host
   manifests only as needed. Preserve established identifiers and versions
   when adapting an existing package unless the task changes them.
2. Author canonical skills under `skills/<skill-name>/SKILL.md` with YAML `name`
   and `description`. Keep detailed procedures in `references/`, output templates
   in `assets/`, and shared executable behavior in `scripts/` or a named library
   when needed. Bundle every relative link target.
3. Define each CLI or MCP operation's inputs, result, side effects, and errors
   independently of the host. Keep executable business logic in one shared
   implementation when the plugin owns it. Add a small executable shim for
   operations that need a process-call surface; use the same operation contract
   for native CLI and MCP adapters.
4. Implement host adapters for startup loading, command syntax, tool registration,
   MCP connection, event translation, and authentication as needed. Each adapter
   calls the shared implementation with explicit project scope when applicable
   and uses the shared settings resolver; a manifest alone implements no behavior.
5. Assemble a host-specific package only when the host cannot consume the shared
   source package directly. Generate it from the same core plus its adapter;
   never hand-edit generated copies or create empty adapters.
6. If adapting an existing plugin, inventory its components before moving them.
   Preserve behavior, public names, and user settings; update consumers of
   moved paths, and explain omissions or replacements.
7. Update the repository's skill/plugin inventory and relevant catalog entries.
   A marketplace indexes packages; it is not the package manifest. Resolve each
   catalog's source paths using that host's rules.
8. Add or update the plugin's eval suite. Run it against the current plugin
   source and commit and push the latest completed results to the designated
   GitHub repository as part of the build. A manifest check or local-only score
   is not a substitute. If GitHub publication is unavailable, report the build
   as incomplete rather than claiming this requirement passed. In `evals/`,
   maintain a [catalog and latest-scores document](references/validation.md#eval-catalog-and-latest-scores)
   with separate rows for suite, harness, platform, and eval configuration.
   Require deterministic generation and a non-mutating check command for the
   latest-scores document; retain failures and missing coverage without inventing data.

## Install a project plugin

When installation is in scope, carry it through to activation. Assemble the
generic artifact at `.agents/packages/<plugin-name>/portable/` and generate
incompatible host artifacts separately from the same canonical source. Never
rewrite the generic manifest in place to install another format. Record each
destination's format, source revision, and assembly command; refuse a destination
owned by another format. Update the root `AGENTS.md` location pointer and a minimal
`CLAUDE.md` shim only when needed, preserving existing instructions. Then use
the selected harness's documented registration, trust, and enablement flow;
the `.agents/` path alone is not activation. For OpenClaw, link the package
there when supported. For Hermes, generate its required `.hermes/plugins/`
project artifact from the same source and enable project plugin loading. Follow
[workspace installation](references/workspace-installation.md) and the selected
host reference for concrete steps. If project installation is part of the
plugin's promised experience, include an idempotent install entry point or
documented setup command that performs this sequence. Never hand-maintain
generated copies.

Verify the installed package path, active state, startup guidance, and one
real skill or CLI/MCP operation in a fresh host session. Verify that installing
or updating one host artifact preserves other artifacts and their registrations.
Record the exact
unverified step if a host, account, or required consent is unavailable.

Write requested local artifacts without an extra approval step. Pushing the eval
results and corresponding source to the designated GitHub repository is part of
the requested build method. Marketplace publication, installation into a personal
profile, and account settings are separate actions; perform them when requested.

## Validate and hand off

Follow [validation and delivery](references/validation.md). For each target,
verify that foundational rules load at session start without router invocation,
that unrelated procedures stay unloaded, that the router selects the correct
procedure, and that adapters execute requested behavior. For each executable
shim, check help, success, failure, and non-mutating dry-run where applicable;
keep real example I/O in the selected procedure or an on-demand reference.
Fix local packaging errors. Report source and artifact locations,
per-target capabilities, eval suite and latest committed result, checks actually
run, and remaining verification. Confirm `evals/README.md` lists the cases and
the required check command confirms `evals/LATEST.md` agrees with the coverage
matrix and recorded evidence. Report consistency is separate from release
readiness; never claim a stale or missing result is current.
