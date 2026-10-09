# Latest plugin evaluation

Generated from `matrix.json`, verified `results/`, and `attempts/` by `python evals/report.py generate`.
Candidate SHA-256: `86284326b0340f8ae535dcd51c0181ee8412ee880becafba12ebfff9bee20816`. Suite revision: `0.6.0`.

A missing or failing required row blocks release. A consistent report does not imply release readiness.

| Suite | Harness | Platform | Configuration | Required | Latest completed result | Outcome / score | Freshness | Newer attempt / next check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| file-and-para-24 | Codex | windows-x86_64 | default | Yes | [windows-final-20261005](results/windows-final-20261005/metadata.json) | Pass / 100.0/100 | Stale | [template-maturity-final-local-20261006](attempts/template-maturity-final-local-20261006/metadata.json): incomplete on an earlier candidate; Execute all 24 cases in a fresh Codex agent and export reviewed evidence. |
| startup-and-discovery | Codex | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-codex-startup-20261001](attempts/final-v3-codex-startup-20261001/metadata.json): unverified on an earlier candidate; Install the current package and probe H01-H03 with a native trace, including hook trust and startup delivery. |
| startup-and-discovery | Claude Code | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-claude-code-startup-20261001](attempts/final-v3-claude-code-startup-20261001/metadata.json): incomplete on an earlier candidate; Renew Claude authentication; install and invoke both skills in a fresh project. |
| startup-and-discovery | Claude Cowork | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-claude-cowork-startup-20261001](attempts/final-v3-claude-cowork-startup-20261001/metadata.json): incomplete on an earlier candidate; Upload the package and probe a fresh Cowork session. |
| startup-and-discovery | Antigravity CLI | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-agy-cli-startup-20261001](attempts/final-v3-agy-cli-startup-20261001/metadata.json): unverified on an earlier candidate; Probe project plugin loading and H01-H03 outside the source repository tree, with a native CLI trace. |
| startup-and-discovery | Antigravity 2.0 | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-agy-2-startup-20261001](attempts/final-v3-agy-2-startup-20261001/metadata.json): incomplete on an earlier candidate; Inspect workspace plugin loading and invoke a bundled skill in a fresh 2.0 session. |
| startup-and-discovery | Antigravity IDE | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-agy-ide-startup-20261001](attempts/final-v3-agy-ide-startup-20261001/metadata.json): incomplete on an earlier candidate; Inspect workspace plugin loading and invoke a bundled skill in a fresh IDE session. |
| startup-and-discovery | OpenClaw | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-openclaw-startup-20261001](attempts/final-v3-openclaw-startup-20261001/metadata.json): incomplete on an earlier candidate; Install the compatible bundle, inspect detected skills, then probe startup and invocation in a fresh session. |
| startup-and-discovery | Hermes Agent | windows-x86_64 | default | Yes | Not run | Score unavailable | No result | [final-v3-hermes-startup-20261001](attempts/final-v3-hermes-startup-20261001/metadata.json): incomplete on an earlier candidate; Enable the generated native project plugin, then probe startup foundation and namespaced skill invocation in a fresh Hermes session. |
| startup-and-discovery | Cursor | windows-x86_64 | default | No | Not run | Score unavailable | No result | Static package support via .cursor-plugin/plugin.json + skills/; probe marketplace/InstallPlugin cache install and H01-H03 before claiming runtime. Do not invent verified SessionStart foundation. |
| startup-and-discovery | Grok Bot | windows-x86_64 | default | No | Not run | Score unavailable | No result | Same Cursor package. Static/package support only. No SessionStart hooks (foundation on-demand). Fallback UpdateState/workflows copy unverified; probe install and skill invocation before claiming runtime. |
| startup-and-discovery | Muse | unknown | provisional | No | Not run | Score unavailable | No result | Identify the product and verify its loader and manifest before adding a required runtime row. |

Release acceptance: **Fail — required evidence missing, stale, or failing**.
