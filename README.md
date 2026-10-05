# NyssaAI Agent Skills

Version: **0.5.0** (candidate; see [latest evaluation](evals/LATEST.md)).

Two skills share one maintained source tree: [file-management](skills/file-management/SKILL.md)
and [para-vault](skills/para-vault/SKILL.md). File-management has a lean
[startup foundation](skills/file-management/core.md); PARA guidance is selected
only for vault work. Plugin-builder is maintained separately in the private
`NyssaAI/plugin-builder` repository.

## Document maturity compatibility

New PARA notes use `document-maturity` instead of `status`. Work-state fields
such as `task-state` remain independent. Existing accepted legacy maturity values
are readable without changing notes; migrating existing notes requires explicit
user authorization. Conflicting fields are reported rather than overwritten.
See the [migration rule](skills/para-vault/references/frontmatter-schemas.md#legacy-metadata-compatibility).

## Package and activation

The canonical content lives under `skills/`. The root `plugin.json`,
`.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and
`.cursor-plugin/plugin.json` identify portable and host packages. The Cursor
shim also covers Grok Bot (same packaging; no SessionStart hooks). `scripts/assemble.py write` builds the project Antigravity
plugin at `.agents/plugins/agent-skills/`, the Hermes plugin at
`.hermes/plugins/agent-skills/`, and the managed foundation
in `AGENTS.md`; the generated Antigravity rule and `hooks/hooks.json` deliver
the same core to supported plugin sessions. Codex requires users to trust the
installed hook before it runs. `scripts/assemble.py check` verifies exact source equality
without modifying files. `CLAUDE.md` imports the root anchor for a project that
loads it. A plugin installed into an unrelated project does not automatically
bring that project's startup anchor with it; startup delivery depends on the
host's hook or rule activation.

| Host | Package route | Activation evidence |
| --- | --- | --- |
| Antigravity CLI / 2.0 / IDE | The generated `.agents/plugins/agent-skills/` is the [documented workspace plugin location](https://antigravity.google/docs/plugins). | Native discovery and fresh-session behavior remain to be tested per surface. `gemini-extension.json` is Gemini CLI metadata, not an Antigravity plugin manifest. |
| Codex | The root and `.codex-plugin` manifests plus `skills/` form the [portable package source](https://developers.openai.com/plugins/build/plugins). | An arbitrary clone does not register a plugin. Use a supported plugin catalog/install flow and verify the skills appear in a new session. |
| Claude Code | `.claude-plugin/plugin.json` declares the shared skills. Use the [Claude plugin manager](https://code.claude.com/docs/en/plugins-reference) or local `--plugin-dir` for development. | Manifest validation passes; this machine's expired OAuth prevents a fresh agent invocation. A project's root `CLAUDE.md` must be installed separately for startup rules. |
| Claude Cowork | The Claude package may be uploaded through its supported plugin flow. | Upload and runtime behavior have not been verified here. |
| OpenClaw | Install this package as a [compatible bundle](https://docs.openclaw.ai/plugins/bundles) with `openclaw plugins install <package-path>`, then inspect the detected format and loaded skills. | Bundle installation, startup guidance, and skill invocation remain unverified here. A native runtime adapter is unnecessary for these Markdown skills. |
| Hermes Agent | The generated `.hermes/plugins/agent-skills/` provides a [native project plugin](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) with the shared skills and startup foundation. | Enable project plugins with `HERMES_ENABLE_PROJECT_PLUGINS=true`, then enable this plugin. Fresh-session behavior remains unverified. |
| Cursor | `.cursor-plugin/plugin.json` plus root `skills/` form the [Cursor plugin package](https://cursor.com/docs/reference/plugins). Install via marketplace / InstallPlugin into the plugin cache. | Static package support only so far; fresh-session and skill-invocation runtime remain unverified here. |
| Grok Bot | Same Cursor package (`.cursor-plugin/plugin.json` + `skills/`). Fallback: UpdateState / workflows copy when marketplace install is unavailable. | Static/package support only. **No SessionStart hooks** — foundation is on-demand, not hook-injected. Runtime install and invocation remain unverified here. |
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
history belongs under the private, Git-ignored `docs/`. User settings, when a plugin needs them, belong
in a separate `.{plugin-name}/` directory outside installed code.

[MIT License](LICENSE) © 2026 NyssaAI.
