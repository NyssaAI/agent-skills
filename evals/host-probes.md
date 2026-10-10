# Fresh-host startup and discovery probes

Run these against an isolated project install of the **assembled** candidate
in a directory tree outside this source repository and its parent directories.
Confirm that no ancestor supplies this repository's `AGENTS.md`, `CLAUDE.md`,
or other agent instructions. Record host and version, OS/architecture, model if
exposed, package path, artifact hash, startup text observed, skill
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
| H03 | List active plugin components, invoke `manage-file-operations` and each of the five PARA workflows on appropriate tasks, and retain each task's observed artifacts. Update the package and confirm other host packages and external `.{plugin-name}/` settings stay intact. |

Retain these focused variants within the corresponding H01/H03 probe evidence;
they add coverage without changing the three-case scoring rubric. Separate fresh
sessions prevent startup context from a previous variant contaminating the next.

- **H01 foundation delivery with separate anchors:** install the foundation block in `AGENTS.md` and
  leave a separate `CLAUDE.md` with unrelated project guidance. Where SessionStart
  exists, confirm the hook still emits the complete lean foundation: existence
  of a foundation-bearing file does not prove the host loaded it. Duplicate
  foundation text is acceptable when the host also loads that file. Confirm the
  host receives the applicable foundation and unrelated guidance. Also run the
  inverse placement and a no-foundation control. Record which files the host
  actually loads; a local hook subprocess test cannot prove host delivery.
- **H01 direct creation without startup injection:** in a host/configuration with
  startup injection unavailable or disabled and no ancestor foundation block,
  use a recognized PARA vault and ask: "Create a draft meeting note named
  meeting-notes.md in the existing 2-areas/meetings folder."
  Prepopulate that destination with unrelated
  content. Inspect discovery/read events and artifacts for access to the shared
  foundation, collision handling, preservation of the existing file, and the
  requested draft note. Do not name a skill in the request. Record a missing
  foundation route as a gap even if an artifact happens to be correct.
- **H03 template maturity discovery:** supply an established reusable template
  with a template-only provisional notice in a recognized vault with no stronger
  local maturity convention. Ask `file-para-content` to create a new draft note
  from that template in a known destination. Confirm the agent discovers the
  template/output maturity reference through installed relative paths, preserves
  the template, and creates a draft without inheriting the template's established
  maturity or template-only notice. Retain the file-read/invocation trace and both
  artifacts. Static reference
  resolution and existing C17/C18 migration tests do not establish this discovery.
- **H03 writing voice discovery and update isolation:** invoke both new skills
  against synthetic profiles only in an isolated established project. From a
  nested working directory, apply its root profile without changing profile
  bytes; confirm a separate project's profile is never inherited. Before an
  installation/update, seed `.nyssa-ai/agent-skills/writing-voice/VOICE.md`,
  optional `STYLE.md`, and an approved synthetic example, plus unrelated scratch
  in `.temp/`. Retain before/after byte hashes showing installation/update leaves
  this state intact. Inspect the actual packed archive to ensure project state
  and scratch do not ship. Record delivery of `rules/writing-voice.md` through
  the host's actual foundation/discovery route; do not infer startup delivery
  from a hook subprocess or manifest. A drafting-only run cannot establish this
  installation result. This new variant remains unexecuted until native evidence
  is retained; earlier file-workflow probes do not cover writing voice.

For hosts without SessionStart (including Grok Bot), mark the hook-delivery
variant inapplicable and still run the direct-creation fallback variant. Do not
infer a runtime pass from static hook, manifest, or reference checks.

For Antigravity, inspect the workspace `.agents/plugins/agent-skills/` package
on CLI, 2.0, and IDE separately. For Codex, use its supported local catalog or
package installer; a repository clone alone is not activation. For Claude
Code/Cowork, use their respective supported plugin flows; a root `CLAUDE.md`
inside the plugin is not project startup context. For OpenClaw, install this
package as a compatible bundle and verify detected skill roots; test startup
guidance separately. For Hermes, enable the generated native project plugin
with `HERMES_ENABLE_PROJECT_PLUGINS=true`, then run the same probes. For Cursor,
install via marketplace or InstallPlugin into the plugin cache and probe discovery plus H01-H03; mark
static package support separately from verified runtime. For Grok Bot, use the
same Cursor package (no SessionStart hooks — foundation on-demand); if marketplace
install is unavailable, document any UpdateState / workflows-copy fallback used.
If a host cannot run, record the exact missing executable, login, or UI step in
`attempts/` and leave its matrix row without a score.
