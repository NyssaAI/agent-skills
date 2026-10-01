# Latest plugin evaluation

Generated from `matrix.json`, verified `results/`, and `attempts/` by `python evals/report.py generate`.
Candidate SHA-256: `33963b665d1bc28d9a7ca4ed0dcaf61eb85ea0f248f2ff2beb64628eed3e5895`. Suite revision: `0.4.0`.

A missing or failing required row blocks release. A consistent report does not imply release readiness.

Supplemental builder process decisions: [latest scoped scores](builder-process/LATEST.md) (not native-host release certification).

| Suite | Harness | Platform | Configuration | Required | Latest completed result | Outcome / score | Freshness | Newer attempt / next check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| file-and-para-24 | Codex | windows-x86_64 | default | Yes | [final-c24-v3-20261001](results/final-c24-v3-20261001/metadata.json) | Pass / 100.0/100 | Current | Execute all 24 cases in a fresh Codex agent and export reviewed evidence. |
| plugin-builder | Codex | windows-x86_64 | default | Yes | [final-builder-v3-20261001](results/final-builder-v3-20261001/metadata.json) | Pass / 100.0/100 | Current | Run builder, adversary, and eval cases in a fresh Codex agent with isolated plugin fixtures. |
| startup-and-discovery | Codex | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-codex-startup-20261001](attempts/final-v3-codex-startup-20261001/metadata.json): unverified; Rerun installed-package H01-H03 with a durable native host trace; determine why the bundled hook is not activated, then add trusted host-export verification before any startup Pass. |
| startup-and-discovery | Claude Code | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-claude-code-startup-20261001](attempts/final-v3-claude-code-startup-20261001/metadata.json): incomplete; Renew Claude Code authentication, install the package, and retain fresh H01-H03 host evidence. |
| startup-and-discovery | Claude Cowork | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-claude-cowork-startup-20261001](attempts/final-v3-claude-cowork-startup-20261001/metadata.json): incomplete; Open an authenticated Claude Cowork session, upload the package, and run H01-H03. |
| startup-and-discovery | Antigravity CLI | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-agy-cli-startup-20261001](attempts/final-v3-agy-cli-startup-20261001/metadata.json): unverified; Run from a truly isolated Antigravity project whose parent context cannot supply this repository instructions, then inspect project plugin discovery and H01-H03 with a native trace. |
| startup-and-discovery | Antigravity 2.0 | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-agy-2-startup-20261001](attempts/final-v3-agy-2-startup-20261001/metadata.json): incomplete; Open an Antigravity 2.0 workspace with the assembled package and run H01-H03. |
| startup-and-discovery | Antigravity IDE | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-agy-ide-startup-20261001](attempts/final-v3-agy-ide-startup-20261001/metadata.json): incomplete; Open an Antigravity IDE workspace with the assembled package and run H01-H03. |
| startup-and-discovery | OpenClaw | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-openclaw-startup-20261001](attempts/final-v3-openclaw-startup-20261001/metadata.json): incomplete; Install OpenClaw, install this compatible bundle, inspect detected skills, and run H01-H03. |
| startup-and-discovery | Hermes Agent | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-hermes-startup-20261001](attempts/final-v3-hermes-startup-20261001/metadata.json): incomplete; Implement and enable the Hermes project adapter, install Hermes Agent, and run H01-H03. |
| startup-and-discovery | Cursor | windows-x86_64 | default | No | Not run | Score unavailable | No result | Static package support via .cursor-plugin/plugin.json + skills/; probe marketplace/InstallPlugin cache install and H01-H03 before claiming runtime. Do not invent verified SessionStart foundation. |
| startup-and-discovery | Grok Bot | windows-x86_64 | default | No | Not run | Score unavailable | No result | Same Cursor package. Static/package support only. No SessionStart hooks (foundation on-demand). Fallback UpdateState/workflows copy unverified; probe install and skill invocation before claiming runtime. |
| startup-and-discovery | Muse | unknown | provisional | No | Not run | Score unavailable | No result | Identify the product and verify its loader and manifest before adding a required runtime row. |

Release acceptance: **Fail — required evidence missing, stale, or failing**.
