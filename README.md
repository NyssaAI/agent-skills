# NyssaAI Agent Skills

Version: **0.6.3** (candidate; see [latest evaluation](evals/LATEST.md)).
Private Tessl evaluations cover representative PARA workflows; prior full-suite and host results predate this split.

Eight workflow skills share one maintained source tree, a brief
[startup foundation](skills/manage-file-operations/core.md), and a
[writing voice convention](rules/writing-voice.md). Its PARA section
applies only to recognized vaults; detailed guidance loads on demand.
Plugin-builder is maintained separately in the private `NyssaAI/plugin-builder` repository.

| Skill | Workflow |
| --- | --- |
| [manage-file-operations](skills/manage-file-operations/SKILL.md) | Safely move, rename, copy, import, or archive existing content, resolve collisions, and resume interrupted operations. Its `core.md` owns the shared startup foundation; deferred conventions remain in its references. |
| [file-para-content](skills/file-para-content/SKILL.md) | Classify and file vault content, process inbox captures, or create a project and its index |
| [maintain-vault-navigation](skills/maintain-vault-navigation/SKILL.md) | Review and repair vault indexes, MOCs, registers, and links |
| [manage-vault-lifecycle](skills/manage-vault-lifecycle/SKILL.md) | Archive or reactivate vault items and intact project bundles, preserving history and lifecycle metadata. |
| [import-vault-source-records](skills/import-vault-source-records/SKILL.md) | Ingest supplied email/calendar records, resolve versions and dates, and preserve native source evidence. |
| [revise-vault-documents](skills/revise-vault-documents/SKILL.md) | Reconcile notes and propose or apply protected revisions |
| [maintain-writing-voice](skills/maintain-writing-voice/SKILL.md) | Establish, inspect, and refine a project-local writing voice from authorized samples and preferences |
| [write-in-user-voice](skills/write-in-user-voice/SKILL.md) | Draft and revise material the user will send or publish as themselves, preserving meaning and task constraints |

`para-vault` is retired. Its capabilities now live in the five focused vault
workflows above. Shared guidance stays with one owning skill and is linked by
consumers; reading a reference does not require activating its owner's workflow.
Existing startup hooks/rules deliver the foundation. When it is absent from context,
`manage-file-operations` and the shared vault conventions load the same core
on demand without activating an additional workflow. Tessl loads the generated
`rules/file-management.md` declared in `.tessl-plugin/plugin.json`; its source
is the same `skills/manage-file-operations/core.md`. The canonical
`rules/writing-voice.md` is also delivered by the existing startup hook, managed
project anchor, Antigravity rules, Tessl rules, and Hermes prompt section. This adds no commands,
MCP dependencies, or background automation. The workflows compose with
`manage-file-operations` for actual file transfers and recovery.

`manage-file-operations` replaces the retired `file-management` skill. It covers
moves, renames, copies, imports, archives, and interrupted-operation recovery.
The startup foundation remains shared. Existing [file and folder naming](skills/manage-file-operations/references/naming.md),
[temporary storage](skills/manage-file-operations/references/intermediate-work.md),
and [document maturity](skills/manage-file-operations/references/document-maturity.md)
guidance loads from the relevant workflow references when naming, temporary work,
or template/output maturity decisions require it; these are not new skills.

## Inbox filing and source retention

Inbox filing keeps one working copy at its resolved PARA home; it no longer
creates an automatic archive under Inbox. Substantive rewrites preserve
recoverable history, using the existing archive when a snapshot is needed.
Existing historical copies are preserved until an explicit cleanup is requested.
Email and calendar services govern live source state. Prefer source references;
retain a local snapshot only for requested retention, evidence, offline access,
or an otherwise unavailable source. See the [source retention rule](skills/file-para-content/references/folder-conventions.md#source-record-destinations).

## Document maturity compatibility

New PARA notes use `document-maturity` instead of `status`. Work-state fields
such as `task-state` remain independent. Existing accepted legacy maturity values
are readable without changing notes; migrating existing notes requires explicit
user authorization. Conflicting fields are reported rather than overwritten.
See the [migration rule](skills/revise-vault-documents/references/frontmatter-schemas.md#legacy-metadata-compatibility).

## Package and activation

The canonical content lives under `skills/`. The root `plugin.json`,
`.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and
`.cursor-plugin/plugin.json` identify portable and host packages. The Cursor
shim also covers Grok Bot (same packaging; no SessionStart hooks). `scripts/assemble.py write` builds the project Antigravity
plugin at `.agents/plugins/agent-skills/`, the Hermes plugin at
`.hermes/plugins/agent-skills/`, and the managed foundation
in `AGENTS.md`; the generated Antigravity rules and `hooks/hooks.json` deliver
the same foundation and writing convention to supported plugin sessions. Codex requires users to trust the
installed hook before it runs. `scripts/assemble.py check` verifies exact source equality
without modifying files. `CLAUDE.md` imports the root anchor for a project that
loads it. A plugin installed into an unrelated project does not automatically
bring that project's startup anchor with it; startup delivery depends on the
host's hook or rule activation.

Hosts without startup delivery can load writing guidance through the relevant
skill. Native host acceptance of the new writing workflows remains unverified;
existing file-workflow results do not establish voice accuracy or activation.

| Host | Package route | Activation evidence |
| --- | --- | --- |
| Antigravity CLI / 2.0 / IDE | The generated `.agents/plugins/agent-skills/` is the [documented workspace plugin location](https://antigravity.google/docs/plugins). | Native discovery and fresh-session behavior remain to be tested per surface. `gemini-extension.json` is Gemini CLI metadata, not an Antigravity plugin manifest. |
| Codex | The root and `.codex-plugin` manifests plus `skills/` form the [portable package source](https://developers.openai.com/plugins/build/plugins). | An arbitrary clone does not register a plugin. Use a supported plugin catalog/install flow and verify the skills appear in a new session. |
| Claude Code | `.claude-plugin/plugin.json` declares the shared skills. Use the [Claude plugin manager](https://code.claude.com/docs/en/plugins-reference) or local `--plugin-dir` for development. | Manifest validation passes; this machine's expired OAuth prevents a fresh agent invocation. A project's root `CLAUDE.md` must be installed separately for startup rules. |
| Claude Cowork | The Claude package may be uploaded through its supported plugin flow. | Upload and runtime behavior have not been verified here. |
| OpenClaw | Install this package as a [compatible bundle](https://docs.openclaw.ai/plugins/bundles) with `openclaw plugins install <package-path>`, then inspect the detected format and loaded skills. | Bundle installation, startup guidance, and skill invocation remain unverified here. A native runtime adapter is unnecessary for these Markdown skills. |
| Hermes Agent | The generated `.hermes/plugins/agent-skills/` provides a [native project plugin](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) with the shared skills and startup foundation. | Enable project plugins with `HERMES_ENABLE_PROJECT_PLUGINS=true`, then enable this plugin. Fresh-session behavior remains unverified. |
| Cursor | `.cursor-plugin/plugin.json` plus root `skills/` form the [Cursor plugin package](https://cursor.com/docs/reference/plugins). Install via marketplace / InstallPlugin into the plugin cache. | Static package support only so far; fresh-session and skill-invocation runtime remain unverified here. |
| Grok Bot | Same Cursor package (`.cursor-plugin/plugin.json` + `skills/`). Fallback: UpdateState / workflows copy when marketplace install is unavailable. | Static/package support only. **No SessionStart hooks** â€” foundation is on-demand, not hook-injected. Runtime install and invocation remain unverified here. |
| Muse | Only a proposed JSON-executable shim contract is known. | Loader, manifest, and installation are unverified; no support claim. |

The exact per-host status and missing tests are in the
[coverage matrix](evals/matrix.json) and [latest evaluation](evals/LATEST.md).
Placement, manifest parsing, and skill
invocation are separate checks. Do not infer runtime support from a shared
`SKILL.md` alone.

## Development and evaluation

Run `python scripts/assemble.py write` after changing any skill, then
`python scripts/assemble.py check`. The [eval catalog](evals/README.md)
contains the behavioral cases, run commands, retained result format, and
latest-score checks. Temporary work belongs under `.temp/`; retained review
history belongs under the private, Git-ignored `docs/`.

## Project configuration and writing voice

Plugin-owned configuration and persistent state belongs under
`<project-root>/.nyssa-ai/<plugin-name>/`, outside installed code. Resolve the
explicit project/workspace root first, then the applicable repository root;
for non-Git workspaces use the established working root. Nested directories
share that root. Do not silently choose the home directory or create competing roots.

Agent Skills stores voice guidance in `.nyssa-ai/agent-skills/writing-voice/`:
`VOICE.md` for voice characteristics, optional `STYLE.md` for editorial standards,
and `examples/` for approved curated examples. The maintenance skill owns the
[detailed storage contract](skills/maintain-writing-voice/references/storage.md).
Existing user-selected samples and profiles remain in place. Disposable calibration
work belongs under `.temp/agent-skills/writing-voice/`.

Private profiles require a verified, narrowly scoped local Git exclusion or an
accepted project ignore convention; a dot-prefixed directory alone provides no
privacy. Do not ignore all `.nyssa-ai/`, as sibling plugins may share their data.
Sharing profiles requires an explicit decision. Packages exclude user configuration,
state, and scratch data. Ordinary drafting reads profiles without changing them.

[MIT License](LICENSE) Â© 2026 NyssaAI.
