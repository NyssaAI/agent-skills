# Validation and delivery

## Local package checks

- Parse each manifest using the appropriate JSON/YAML parser and target schema.
  Check required fields, real identity values, referenced components, and supported
  fields. Valid JSON alone is not manifest validation.
- Check each skill's frontmatter, folder/name match, trigger description, relative
  links, and bundled resources. A link must still resolve after packaging.
- Inspect the actual archive or assembled directory, including hidden manifest
  directories. Ensure its root shape matches the target importer. Exclude caches,
  scratch work, credentials, and unrelated repository files.
- Confirm catalog entries resolve to the intended plugin and public IDs remain
  consistent. Check stale references after renames or moves.
- Run new scripts against representative inputs. For runtime adapters, exercise
  registration and the behavior they add; parsing their manifest is insufficient.
- For CLI or MCP capabilities, compare each exposed operation with the shared
  input/output and side-effect contract. Verify the packaged executable and its
  dependencies, or the host-specific connection and transport declaration.
- For a bundled local MCP server, confirm the assembled `mcp/` or shared `bin/`
  executable exists at the declared path on each claimed platform, starts over
  stdio, reserves stdout for protocol traffic, and shuts down cleanly.
- For platform binaries, inspect the Windows, Linux, and macOS artifact matrix,
  executable permissions and suffixes, selected CPU architecture, and generated
  connection paths. Run the capability on each available target platform;
  record other platforms as unverified rather than extrapolating.
- Confirm package and generated artifacts exclude user settings. Check that each
  adapter passes explicit project scope to the shared settings resolver instead
  of deriving it from cwd or the installed package. Check that preferences stay
  in the documented external home.
- Run the required non-mutating latest-scores check against the declared eval
  matrix and result artifacts. Run the release acceptance check separately;
  a consistent report can accurately show missing, stale, or failing results.
- For project installs, check the resolved `.agents/packages/<name>/portable/`
  artifact and each distinct host destination, root `AGENTS.md` as the primary
  instruction anchor, and a minimal `CLAUDE.md` import or Claude-only delta.
  Preserve unrelated text and
  verify that host registration activates the package. When a setup entry point
  is shipped, run it twice: the second run must preserve the package, anchors,
  settings, and enabled state without adding duplicate entries.
- Check that each destination records its format, source revision, and assembly
  command. Incompatible formats must resolve to different directories. Exercise
  installing the portable and Antigravity artifacts in either order, then updating
  each independently. Compare hashes and registrations of the untouched artifact
  and verify it remains usable. A destination conflict must stop before overwriting
  another format, even when plugin IDs match. Record unavailable host checks.

Use existing repository validators first. Scope any new helper to deterministic
work such as assembly or path checks; do not encode speculative universal host
schemas. Run checks on generated output as well as source when assembly changes
paths or included files.

## Context-loading checks

For every target, inspect a fresh session before any skill invocation, then an
unrelated ordinary task, a router task, and direct specialist invocation when
supported. Record which rule bodies and references actually loaded and their
approximate context cost. Verify that the short foundation is present from the
start, specialized procedures are absent until needed, and the router reads
only its selected route. Check that generated adapters do not inject duplicate
copies of the same core. If the host does not expose reliable context traces,
use observable probes and state that the exact load set or size is unverified.
Where both root `AGENTS.md` and `CLAUDE.md` exist, confirm the shared rules load
once and the Claude shim adds only its host-specific delta.

Evaluate the cumulative material loaded during a normal task; separate files do
not imply that earlier material is unloaded. Compare the measured cost with the
task's usefulness before promoting another rule into startup context. Do not
set a universal token cap that ignores host limits and task complexity.
When the host supports session compaction or resumption, continue a selected
workflow afterward and verify that its governing rules are still available or
reloaded from canonical source. Record the limitation when this cannot be tested.

## Required evaluation suite and published result

Every plugin must carry an executable eval suite in its source repository. Define
representative, isolated tasks with observable success criteria and a way to
reproduce the run. Cover the capabilities the plugin actually promises: startup
foundation on an unrelated task, router selection, selected guidance, safety
boundaries, and each host adapter or runtime integration that exists. A
single-purpose plugin needs cases for its actual workflow instead of artificial
router cases. Use synthetic fixtures and assess resulting behavior or artifacts,
not exact wording or a particular tool sequence. A parser-only check is validation,
not an agent eval.

### Eval catalog and latest scores

Keep both documents inside each plugin's `evals/` directory:

- `evals/README.md` is the human-readable catalog. List every eval suite and
  case or case group, its purpose, entry skill/capability, success criteria,
  run command, and known coverage gaps. Link to detailed fixtures or rubrics
  instead of copying them into the index. Update the catalog whenever cases
  or claimed coverage change. Link the machine-readable coverage matrix and
  document report-generation, report-check, and release acceptance commands.
- `evals/LATEST.md` is a generated score receipt with a stable row per relevant
  **suite + harness + OS/architecture + eval configuration**. Define these keys
  in the coverage matrix independently of available result files. Include every
  required combination, even when it has no run; document inapplicable combinations
  and their reasons instead of inventing a meaningless full cross-product.
  Distinct model configurations need distinct keys when model choice affects the
  comparison; record actual model/version when available.

Each row identifies its latest **completed, verified** result with a run ID,
link under `results/`, UTC completion time, host/version, model when available,
source and assembled-artifact revisions or content hashes, suite revision, and
eval configuration. Include overall and meaningful component scores, critical
failures, and release-gate status. Link the evidence export; this document is
not the only score record. Record unavailable metadata honestly and enforce
the suite's declared evidence requirements before calling a result verified.

Keep outcome (`Pass` or `Fail`), freshness (`Current`, `Stale`, or `No result`),
and execution state separate. A completed failing run can be current. Select
the latest completed verified result by recorded UTC completion time with a
documented stable run-ID tie-breaker, never by file modification time or by
filtering for passing scores. Do not let another harness or platform replace
that row. Show a newer incomplete, aborted, or unverified attempt separately
alongside any older verified score so the failed attempt is visible.

If no completed verified run exists, show `No result; score unavailable` and
the remaining execution step; use `Not run` when no attempt exists. Keep a
stale historical score visible and labeled stale. Do not put a validator,
scorer-calibration run, partial run, or promised future run in the score column.
Preserve historical exports without relabeling or rewriting their scores.

Every plugin must provide a deterministic report-generation command and a
non-mutating check mode. Generate `LATEST.md` from the declared matrix and
recorded results, including each run's `score.json` or equivalent evidence.
The check must exit nonzero if the committed document differs from generated
output, required rows are absent, evidence links are broken, or report metadata
disagrees with the evidence. Exercise these failure conditions using isolated
fixtures. Wire the check into CI and the release workflow; generation must not
silently repair a report during check mode. Exclude the generated report itself
from candidate behavior hashes to avoid a self-invalidating freshness check.

Report consistency and release readiness are separate checks. A report can
correctly document missing or stale results and pass consistency; release
acceptance must still fail for required targets whose results are missing,
stale, unverified, or failing. Define required targets and any provisional
coverage gaps explicitly; never silently drop an unavailable target. Check
that both documents, the matrix, and linked artifacts are in the GitHub change.

When the plugin has user settings, evaluate project-versus-personal precedence,
a one-off instruction that must not become durable, and an update or reinstall
that preserves existing values. If multiple hosts are supported, confirm that
they read the same settings home and do not fork preferences by harness. Keep
synthetic settings outside the candidate plugin package and out of published
personal data.
For executable surfaces, run the cached CLI or local MCP from an unrelated
working directory with an explicit project root. Exercise two projects with
different preferences and missing-scope behavior. For a multi-project server,
alternate and overlap requests to verify settings cannot bleed between projects.
For remote MCP, inspect the request to confirm local resolution forwards only
the required non-secret values, not the settings tree or a path the server is
expected to read. Follow
[the shared resolution contract](package-organization.md#explicit-settings-resolution).
For a CLI or MCP-backed skill, include a successful call and a missing executable,
unreachable server, or failed-authentication case as applicable. Score the
observable result and the accuracy of the agent's limitation report, not just
the presence of a tool declaration.

For each release or change to plugin behavior, run the suite against the exact
source and assembled artifacts being shipped. Save the latest **completed** run
under a stable `evals/results/` location in the plugin repository. Commit and
push that result to the designated GitHub repository with the source change.
Include the suite revision, source commit or content hashes (including
dirty-worktree changes), UTC run time,
candidate host and version, model when exposed, case outcomes, scoring method,
and evidence or reproducible artifact references. Record unavailable fields as
unavailable; never invent run metadata. Keep secrets, personal data, and bulky
transcripts out of the committed result. Preserve any prior result needed to
explain a regression, but clearly identify which result is latest.

The committed result must match the current plugin source and suite revision.
An old result becomes stale after a relevant source, adapter, or eval change.
Report it as stale until a fresh run completes; do not relabel, rescore, or copy
responses to make it appear current. If an essential host cannot be exercised,
record the gap and do not mark that capability runtime verified. A new plugin is
not complete until its suite has a completed, pushed current result.
Local-only output and a promised future run do not satisfy this requirement.
Keep a failing run as evidence, fix the cause, and run the suite again. Do not
declare release readiness while required acceptance cases fail.

## Runtime evidence

For each default or explicitly selected harness, record the actual version,
installation surface,
artifact tested, and outcome. Use precise statuses:

| Status | Evidence |
| --- | --- |
| Packaged | Files and required resources were assembled |
| Statically validated | Applicable parsers, paths, and schema checks passed |
| Runtime verified | The host discovered the package and the tested workflow worked |
| Eval current | This matrix row's latest completed verified result is checked into GitHub and matches the candidate source, artifact, suite, and configuration; outcome is reported separately |
| Eval stale or missing | The current revision has no completed, checked-in result |
| Unverified | A necessary host, account, dependency, or test was unavailable |
| Unsupported | A requested capability has no implemented mapping for that target |

Statuses apply per capability when support is mixed. A discovered plugin does not
prove its hook fired, connector authenticated, or subagent ran.

Useful smoke checks are a representative skill invocation, a benign tool call,
and an observed hook effect where those components are included. Exercise a missing
dependency or unavailable integration when graceful fallback is part of the design.
Use isolated fixtures and avoid external writes merely to demonstrate a plugin.
For MCP, verify initialization, advertised tools, a representative call, and
authorization in the actual target host. For CLI, verify the real command,
exit status, and resulting artifact on a supported platform. Do not infer
Cowork execution from a Claude Code CLI test.
For a JSON executable shim, validate its declared input/output schemas and
example, run `--help`, success, bad input, missing secret when relevant, and
non-mutating `--dry-run` for writes. Confirm stdout/stderr JSON and exit status;
then test the operation through the selected host rather than treating the
direct command as harness evidence. Follow [the executable contract](executable-contract.md).
For an OpenClaw project link, verify the linked path and enablement, then call
the capability through the running Gateway; `inspect --runtime` alone is not
runtime evidence for that Gateway. For Hermes, verify the `.hermes/plugins/`
artifact was generated from canonical source, the project-plugin gate and
enablement took effect, and a fresh session can load the skill or MCP tool.
Record host consent or trust gates that prevented completion.

## Review prompts

Use these scenarios when evaluating substantial changes to this skill or its output;
they are acceptance questions, not evidence that a runtime test happened:

- A skills-only plugin uses the default target set. Does it share canonical
  content, generate an Antigravity package, give Hermes a skill route, avoid
  empty native runtime adapters, and mark Muse's loader unverified?
- A Claude plugin includes an event hook and subagent. Does an OpenClaw adaptation
  distinguish supported instructions from missing runtime behavior?
- A package targets Claude Code and Cowork and contains `bin/`. Does the Cowork
  artifact omit that incompatible component and explain the resulting capability?
- A catalog already contains local changes and several entries. Does adding a
  plugin preserve those changes, ordering, and correct source resolution?
- A portable plugin and its Antigravity artifact are installed in the same
  project. Can either be installed or updated without changing the other's
  manifests, content, or registrations?
- Only Codex is installed locally. Does the report distinguish other targets'
  static checks from actual runtime results?
- A release changes the router or an adapter. Does its committed latest result
  identify this source revision, cover the changed behavior, and disclose hosts
  that could not be exercised?
- A user changes a project preference and reinstalls through another host. Does
  that host read the same `.{plugin-name}/` state without copying or resetting it?
- A cached CLI starts in an unrelated directory, or one MCP serves two projects.
  Does explicit scope select the correct settings without cross-project leakage?
- One harness passes, another fails, and a third has no run. Does the generated
  matrix retain all three, reveal a newer aborted attempt, and distinguish report
  consistency from release readiness? Does check mode reject a hand-edited score
  or a missing required row without rewriting the document?
- A plugin exposes one operation through a CLI on Claude Code and a remote MCP
  server on Cowork. Do both follow the same contract, and does an unavailable
  CLI or server produce an honest capability limit?

## Handoff

Provide the source and artifact paths, the selected installation route, the
settings home and precedence, the eval suite path and link to its latest
committed result, and the smallest actionable support matrix. Include checks
run and unresolved capabilities. For unavailable runtimes, give the exact
remaining smoke test instead of claiming success. Publish or install only when
within the requested scope.
