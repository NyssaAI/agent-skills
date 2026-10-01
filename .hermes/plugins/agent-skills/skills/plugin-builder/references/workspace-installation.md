# Workspace installation and instruction anchors

Keep the maintained source in its repository. Assemble the generic project
artifact at `project-root/.agents/packages/<plugin-name>/portable/` and register
compatible hosts against that path. This is our installation convention, not
a directory that every harness automatically scans. Incompatible formats get
separate destinations generated from the same canonical source. In particular,
reserve `.agents/plugins/<plugin-name>/` for Antigravity's project artifact.
Keep `project-root/.agents/plugins/marketplace.json` as catalog metadata and
`project-root/.{plugin-name}/` as user-owned project settings; neither is the
plugin's maintained implementation. If the project package is copied from an
upstream repository, treat it as an installed or generated artifact, not a second
source to hand-edit.

```text
project-root/
  AGENTS.md                         # Small project instruction anchor
  CLAUDE.md                         # Claude Code anchor when needed
  .agents/
    packages/plugin-name/portable/   # Generic artifact; explicitly registered
      plugin.json
      skills/
    plugins/
      marketplace.json              # Codex catalog when used
      plugin-name/                  # Generated Antigravity artifact
        plugin.json
        skills/
  .hermes/plugins/plugin-name/       # Generated Hermes project artifact if used
  .plugin-name/                     # Project settings, never bundled as code
```

Make root `AGENTS.md` the primary project instruction anchor. It may name the
installed path, the router invocation, where settings live, and how to obtain
deeper guidance. Keep it short; do not paste the plugin's full skill tree or
host-specific connection schemas into it. If the installed Claude Code version
reads `AGENTS.md` directly and no Claude-specific rule is needed, omit
`CLAUDE.md`. Otherwise use root `CLAUDE.md` only for a Claude-specific delta and
to import the shared anchor with `@AGENTS.md` where that syntax is supported.
Do not maintain a second Claude copy of the same rules. A `CLAUDE.md` inside a
plugin package is not project startup context.

A path pointer alone does not prove that the lean foundation is loaded at
session start. Use a verified host import when available, or generate the small
startup text from its single canonical source and test it in a fresh session.
Never maintain separate handwritten copies. Treat root instruction files as
context and location guides, not executable registration or an authorization
mechanism.

Placement is distinct from activation:

- **Codex:** Point the project marketplace to `.agents/packages/<name>/portable/`;
  verify `source.path` from the marketplace root and project enablement in the
  supported Codex configuration. Do not treat the marketplace file as an install.
- **Claude Code:** Load the package from the project path through its supported
  plugin-directory or marketplace flow. Verify both plugin discovery and the
  project-root instruction anchor. Use the portable artifact with its Claude
  manifest when compatible, or a separate generated format under `.agents/packages/`.
- **Claude Cowork:** Assemble and upload its accepted artifact. The `.agents/`
  workspace copy may be build source but is not Cowork's installed location.
- **Antigravity:** Generate an Antigravity-format package under
  `.agents/plugins/<name>/` for project loading. Its `plugin.json` has its own
  strict schema; generate it from the canonical identity rather than copying
  the portable manifest. Verify the plugin and its skills in the selected 2.0,
  CLI, or IDE surface. Keep Gemini CLI's `gemini-extension.json` separate.
- **Hermes Agent:** Project skills can live in `.agents/skills/` with project
  trust. Portable or native project runtime plugins are discovered from
  `.hermes/plugins/` with their own enablement gate. Generate that install
  artifact from canonical source, reusing the portable assembly when compatible.
- **OpenClaw:** Install or link `.agents/packages/<name>/portable/` through the
  supported CLI, then enable it according to policy. Merely placing it there
  does not activate it.
- **Muse:** The supplied `.agent/plugins/<name>/` layout is a proposal until
  its actual loader and manifest are verified. Keep it in the default coverage
  report; do not substitute that path for other hosts' artifact destinations.

An invoked installer may place or register a project plugin idempotently and
update the root instruction anchors without replacing unrelated content. Check
the resolved package, active state, startup rules, and a representative skill
or tool call after installation. Do not let a plugin silently install itself at
session start. Keep user settings in `.{plugin-name}/` through updates and
host changes.
When the plugin promises project installation, provide a repeatable setup entry
point. It should detect already-correct state, refuse unrelated same-name
packages or a destination owned by another format, update only its owned anchor
text, and leave host consent and trust prompts to the host. Document how to
refresh a generated host artifact after
the generic package changes.

Record each installed artifact's format, canonical source revision, and assembly
command in an installation receipt outside schema-restricted manifests. Resolve
destination paths before writing so two incompatible formats cannot alias the
same directory. Share an artifact between hosts only when its files and manifests
are compatible without rewriting. A native OpenClaw variant, for example, may
use `.agents/packages/<name>/openclaw-native/` while the portable artifact stays
intact. If an older install occupies the new destination with another format,
stage that artifact at its own location and update its registrations before
reusing the destination; never overwrite it as part of the new host's install.

## Repeatable installation sequence

1. Resolve the project root and stable plugin ID. Inspect existing package,
   catalog, root instructions, host settings, and user state before editing.
2. Assemble the self-contained generic package at
   `.agents/packages/<plugin-name>/portable/`. Record its format, canonical source
   revision, and assembly command. Refuse to overwrite an unrelated package or
   another format, even if the plugin ID matches.
3. Add only a short managed location/invocation note to root `AGENTS.md`.
   Omit `CLAUDE.md` where Claude reads `AGENTS.md` directly; otherwise use a
   short `@AGENTS.md` import and Claude-only delta. Preserve other instructions.
   Deliver the lean startup foundation through a verified mechanism, not a
   path pointer alone.
4. Register the compatible artifact or generate a separate host-specific artifact
   from canonical source. Record its ownership and provenance as in step 2. Keep
   generated copies reproducible and out of the canonical edit path. Do not move
   user settings into them or rewrite a different artifact's manifest.
5. Start a fresh host session. Verify discovery, enabled state, startup content,
   and a real operation. Verify that the other installed formats and registrations
   remain intact and usable. Save the install command and observed result for the
   plugin's eval suite and handoff.

### OpenClaw project route

Use the generic package when its skills and MCP tools are supported. The local
path must exist on the Gateway host. Link it without copying:

```text
openclaw plugins install --link ./.agents/packages/<plugin-name>/portable
openclaw plugins inspect <plugin-id> --runtime --json
```

Inspect the result and enable the plugin if it remains disabled with
`openclaw plugins enable <plugin-id>`; reload or restart the running Gateway as
the installed version requires. A local link can require source confirmation
and capability consent. Do not bypass those controls or assume `inspect`
proves the Gateway is using the plugin. Trigger a real skill or MCP tool through
the running Gateway and observe the result. If a native OpenClaw capability is
required, generate its native adapter from the same source; do not claim a
bundle preserved unsupported hooks or in-process behavior.

### Hermes project route

Hermes does not scan `.agents/packages/` as a project plugin root. Assemble a
self-contained artifact from canonical source plus any Hermes adapter into
`.hermes/plugins/<plugin-name>/`. Use root `plugin.json` for the portable subset
of skills and supported MCP transports; use `plugin.yaml` plus Python
registration only for behavior that requires Hermes' native plugin API. The
`.hermes/` copy is an install artifact: regenerate it after source changes and
never hand-edit it.
This catalog uses native registration for its startup foundation. The generated
`plugin.yaml` and `__init__.py` register the shared skills and load the lean
foundation from the copied canonical `core.md`.

Project plugin loading requires the host's explicit
`HERMES_ENABLE_PROJECT_PLUGINS` gate. Run
`hermes plugins doctor ./.hermes/plugins/<plugin-name> --ci` when available,
then `hermes plugins list` and `hermes plugins enable <plugin-id>` according to
the installed version's controls. In a fresh session, verify the namespaced
skill or registered tool actually runs. For a skills-only project integration,
`.agents/skills/` with Hermes project trust is another host route; it does not
replace a plugin install that needs MCP or runtime registration.

When project plugin loading cannot be enabled, use Hermes' supported Git or
catalog install flow and record that its managed installation lives outside
`.agents/`. Do not invent a local-path `hermes plugins install` command from
OpenClaw's syntax.

Current references: [Codex plugin marketplace](https://developers.openai.com/plugins/build/plugins),
[Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Claude project memory](https://code.claude.com/docs/en/memory),
[Hermes project plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/),
and [OpenClaw installs](https://docs.openclaw.ai/cli/plugins/install).
