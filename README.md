# NyssaAI Agent Skills

Version: **0.2.0** (candidate; see [latest evaluation](evals/LATEST.md)).

Three skills share one maintained source tree: [file-management](skills/file-management/SKILL.md),
[para-vault](skills/para-vault/SKILL.md), and
[plugin-builder](skills/plugin-builder/SKILL.md). File-management has a lean
[startup foundation](skills/file-management/core.md); PARA guidance is selected
only for vault work. The plugin-builder skill provides the review, adversary,
assembly, and eval method for updates to this repository.

## Package and activation

The canonical content lives under `skills/`. The root `plugin.json`,
`.codex-plugin/plugin.json`, and `.claude-plugin/plugin.json` identify portable
and host packages. `scripts/assemble.py write` builds the project Antigravity
plugin at `.agents/plugins/agent-skills/` and refreshes the managed foundation
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
| Claude Code | `.claude-plugin/plugin.json` declares the skills and the named `agent-skills:adversary` and `agent-skills:eval` agents. Use the [Claude plugin manager](https://code.claude.com/docs/en/plugins-reference) or local `--plugin-dir` for development. | Manifest validation passes; this machine's expired OAuth prevents a fresh agent invocation. A project's root `CLAUDE.md` must be installed separately for startup rules. |
| Claude Cowork | The Claude package may be uploaded through its supported plugin flow. | Upload and runtime behavior have not been verified here. |
| OpenClaw | Install this package as a [compatible bundle](https://docs.openclaw.ai/plugins/bundles) with `openclaw plugins install <package-path>`, then inspect the detected format and loaded skills. | Bundle installation, startup guidance, and skill invocation remain unverified here. A native runtime adapter is unnecessary for these Markdown skills. |
| Hermes Agent | Shared Agent Skills content is available for its [plugin/skill flow](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins). | No Hermes project plugin has been assembled or activated yet. |
| Muse | Only a proposed JSON-executable shim contract is known. | Loader, manifest, and installation are unverified; no support claim. |

The exact per-host status and missing tests are in the
[review record](docs/2026.09.29-plugin-review.md) and
[coverage matrix](evals/matrix.json). Placement, manifest parsing, and skill
invocation are separate checks. Do not infer runtime support from a shared
`SKILL.md` alone.

## Development and evaluation

Run `python scripts/assemble.py write` after changing any skill, then
`python scripts/assemble.py check`. The [eval catalog](evals/README.md)
contains the behavioral cases, run commands, retained result format, and
latest-score checks. Temporary work belongs under `.temp/`; retained review
history belongs under `docs/`. User settings, when a plugin needs them, belong
in a separate `.{plugin-name}/` directory outside installed code.

[MIT License](LICENSE) © 2026 NyssaAI.
