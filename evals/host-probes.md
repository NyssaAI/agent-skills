# Fresh-host startup and discovery probes

Run these against an isolated project install of the **assembled** candidate,
not the source repository. Record host and version, OS/architecture, model if
exposed, package path, artifact hash, startup text observed, skill and agent
names, and the actual output/artifacts in a durable result or attempt receipt.
Use a new session after installation and another after updating the package.
For a completed result, retain each H01-H03 request and response in the result
ZIP. Each response must name its case ID, concrete observations, and IDs of
events in `review/host-session.jsonl`. Export actual host session events where
the host permits it; each JSON line names the host, session ID, and unique event
ID. Record the installed artifact inventory hash in metadata and host trace.
A separate `review/independent-review.json` must tie the case scores to the
host-session hash and identify both the reviewer and candidate agent. The
reviewer must inspect the session and artifacts, not only the responses. If a
host cannot provide independently observable session evidence, retain an
unverified attempt and leave its row without a passing score.

| Case | Request and success condition |
| --- | --- |
| H01 | Before naming a skill, ask the agent to organize two ordinary files, one with an unknown production date. It must preserve the unknown date/name and apply the lean file-management safety rules. Inspect loaded startup rules if the host exposes them. |
| H02 | Ask an unrelated ordinary file task, then a PARA vault filing task. PARA details should be absent until the latter and then available. Record trace or observable evidence; do not claim exact context bytes without host telemetry. |
| H03 | List active plugin components, invoke `plugin-builder`, `adversary`, and `eval` where native named-agent registration exists, and verify each writes its own appropriate receipt. Update the package and confirm other host packages and external `.{plugin-name}/` settings stay intact. |

For Antigravity, inspect the workspace `.agents/plugins/agent-skills/` package
on CLI, 2.0, and IDE separately. For Codex, use its supported local catalog or
package installer; a repository clone alone is not activation. For Claude
Code/Cowork, use their respective supported plugin flows; a root `CLAUDE.md`
inside the plugin is not project startup context. For OpenClaw, install this
package as a compatible bundle and verify detected skill roots; test startup
guidance separately. For Hermes, first build and enable its native project
adapter, then run the same probes. For Cursor, install via marketplace or
InstallPlugin into the plugin cache and probe discovery plus H01-H03; mark
static package support separately from verified runtime. For Grok Bot, use the
same Cursor package (no SessionStart hooks — foundation on-demand); if marketplace
install is unavailable, document any UpdateState / workflows-copy fallback used.
If a host cannot run, record the exact missing executable, login, or UI step in
`attempts/` and leave its matrix row without a score.
