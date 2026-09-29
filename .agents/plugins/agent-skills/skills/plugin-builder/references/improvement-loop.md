# Issue-by-issue improvement loop

Use this loop for evaluating an existing plugin and, when repair is in scope,
working through its findings. Honor a narrower user request or an established
repository release rule that takes precedence. A review may end after the
baseline and findings record; do not turn a review-only request into edits.

## Establish the baseline

Before implementation, record the update's concrete scope, deliverables, and
acceptance checks. Inventory each target's executable, version, authentication,
adapter, and existing eval route. Separate missing implementation (work to do)
from unavailable external verification (a blocker with an exact next check).
Keep all known targets in the matrix; lack of a local host does not waive its
release requirement or prevent implementing and statically checking its adapter.

Inventory canonical skills, runtime code, manifests, generated artifacts,
installation paths, startup instructions, settings, claimed hosts, and existing
evals. Read current repository instructions and check uncommitted work before
editing. Run available static checks and relevant existing tests; distinguish
those results from fresh-host behavior and agent evals. Use the applicable
[validation checks](validation.md) and host references to identify gaps. For
each finding, record the affected requirement, observed evidence, consequence,
and a concrete acceptance check. Mark unavailable host tests unverified rather
than calling them failures or passes. Run one representative behavioral case
early on an available host, using the existing runner, scorer, and evidence
verifier. Repair only the prerequisites needed for that first path before
expanding evaluation infrastructure. If execution is externally blocked, record
the evidence and continue independent work. Leave final scoring to `eval`.

Keep one durable review file at `docs/YYYY.MM.DD-plugin-review.md`, using the
date the review begins. Continue updating that same file if work spans several
days; do not create a daily copy. If that name already belongs to a different
review, add the plugin name or a short distinguishing suffix. Keep this file in
source control and outside the distributed plugin artifact. It holds the ordered
task list, stable finding IDs and statuses (`Open`, `In progress`, `Verified`,
`Blocked`, `Rejected`, `Unverified`, or `Deferred`), baseline source revision and plugin version,
acceptance checks, decisions, evidence links, check results, and a final release
summary. Update it after each verified fix rather than reconstructing history
at the end. Link an existing issue tracker when it carries additional discussion;
do not duplicate long logs or transcripts in the review file.

## Independent adversarial review

After the baseline, invoke the maintained
[adversary agent](../agents/adversary.md) in an independent subagent. Load that
file's full instructions; naming an arbitrary reviewer `adversary` without its
instructions is insufficient. Give it the review scope, candidate paths,
receipt path, and relevant raw files, not the lead agent's suspected findings
or proposed fixes. Its plugin-specific probes and output contract live in the
agent file. The subagent does not repair the plugin or change the lead agent's
task list.

The canonical definition is `skills/plugin-builder/agents/adversary.md`.
Register that file through a host's native named-agent mechanism when supported;
otherwise start a subagent named `adversary` with its full body as the task
instructions. Generate only thin host-specific registration files from the
canonical definition, and verify that invocation actually loads it. Do not
mistake a skill's `agents/openai.yaml` UI metadata for an agent definition.
If the host has no subagent facility, the adversarial gate remains unverified.
Resolve the native name before invocation: Claude Code namespaces this
repository's registered agent as `agent-skills:adversary`; a differently named
builder package uses `<plugin-id>:adversary`. Verify the loaded agent's identity
and receipt rather than assuming a bare `adversary` name selects the plugin
agent. The lead must supply a `docs/` receipt path for a production review.
An isolated prompt test may write a disposable `.temp/` receipt, but it cannot
satisfy the durable review gate.

The subagent writes its own durable receipt at
`docs/YYYY.MM.DD-plugin-review-adversarial.md`, with the same start date and
distinguishing suffix as the main review when needed. Require a source revision
or content hashes, scope, checks actually run, and each finding's evidence,
severity, affected requirement, and proposed acceptance check. Explicitly state
when it found no further issue or could not test a claim. The lead agent waits
for the receipt, links it from the main review file, and gives each actionable
finding a stable task ID. Record accepted, rejected, duplicate, or deferred
disposition with a reason; never silently discard a challenge. Keep the
subagent's original receipt intact so its independent judgment remains visible.

After the final versioned candidate has passed local development checks, use a
fresh `adversary` subagent for another review of that exact candidate.
Have it add a separate final-candidate section to the same receipt with its own
source/artifact hashes. Reconcile new findings into the main task list and return
to the repair loop for material issues. After repairs, give a fresh reviewer the
delta, prior receipts, and affected requirements. Review changed areas and their
dependencies; preserve coverage of unchanged files by linking their earlier
hashes and receipt. Expand scope only when the delta invalidates earlier
conclusions. Do not repeat a broad baseline review automatically. A lead-agent
self-review does not substitute for this
step; if no subagent can run, mark the adversarial gate unverified and report
that the process is incomplete.

If the same finding returns after a purported fix, diagnose why its acceptance
check missed the failure before editing again. Use a concrete counterexample
and a focused check. Each review request must name the candidate, scope, receipt,
and stopping condition: return actionable findings or a clean result for that
scope. Avoid open-ended requests to keep looking, and never turn a repeated
review into a waiver of an unresolved material defect.

Put disposable analysis, trial assemblies, fixtures, command logs, and
downloaded artifacts under the working root's `.temp/plugin-review/`; exclude
that directory from package assembly and Git. Preserve completed failed eval
exports under `evals/results/` and incomplete or aborted attempt receipts under
`evals/attempts/` as required by the eval contract, not only in `.temp/`.

## Repair one finding at a time

1. Order findings by user impact and release risk, then dependencies. Address
   misleading claims, broken behavior, and required release gates before optional
   polish. Select one finding whose prerequisites are met. State the behavior and
   acceptance check before editing.
2. Make the smallest complete change in canonical source. Regenerate affected
   host artifacts from it and preserve unrelated capabilities, registrations,
   and user settings. Do not hand-edit a generated copy as the repair.
3. Run the focused acceptance check, then relevant regression and host checks.
   Check observable behavior or artifacts, not only matching text. If a check
   fails, continue working on the same finding. If execution is unavailable,
   distinguish an external blocker from missing implementation that can be
   completed locally. Split independent implementation and host-verification
   acceptance checks so neither is mislabeled as the other.
4. Immediately update the durable record with the change, evidence, source
   revision or content hashes, checks run, and status. Mark `Verified` only when
   the stated acceptance check passes. Record newly discovered issues with new
   IDs rather than silently expanding the current finding.
5. Before advancing, give the finding one disposition: `Verified` with evidence,
   `Blocked` by a named external dependency with the exact next check, or
   `Rejected` with evidence explaining why the finding does not apply. Deferred
   scope requires an explicit reason and remains visible; it is not completion
   of a required finding. Do not leave a locally repairable issue half-finished.
   Reassess the remaining list and repeat. Continue all independent authorized
   work; stop only when it is finished or every remaining path has a concrete
   blocker. Report those blockers without claiming the affected requirements pass.

## Completion and publication

For an existing plugin repair that changes the plugin, reserve one target minor
version: add `0.1.0` to the current `MAJOR.MINOR.PATCH` version by increasing
`MINOR` and setting `PATCH` to zero. For example, `1.4.7` becomes `1.5.0`.
Do not increment once per finding or again while fixing the same unreleased
candidate. Update canonical identity and every generated host manifest and
catalog entry that carries the version. If the repository has an established
release rule or the user specifies another version, follow that instead and
record the choice. A review with no plugin change does not bump the version.

After locally actionable material adversarial findings are reconciled, invoke the maintained
[eval agent](../agents/eval.md) in a fresh subagent as the **last quality gate**.
Load its full definition; where native registration exists, resolve the actual
name (`agent-skills:eval` in this repository's Claude plugin). Give it the
versioned source/artifacts, coverage matrix, suite commands, adversarial
receipt, and the main review file path. It owns the final behavioral run,
verified exports, generated latest-scores report, and separate release
acceptance check. Run every available required case; unavailable rows must not
short-circuit the other rows. A preflight-only receipt does not complete this
step when behavioral cases can run. The lead incorporates the result into the
dated review record.
If no subagent can run, mark this gate unverified rather than self-scoring.

For a locally repairable failure, missing coverage, stale result, or source
mismatch, return to the relevant finding. Repair, regenerate affected artifacts,
review the delta and affected requirements, and rerun affected evaluations.
Preserve prior results and do not relabel them current; unchanged checks may be
reused only when the declared dependency inventory proves their inputs identical.
Link failures and attempts to findings and keep the same unreleased version.
An external execution blocker stays in the matrix while independent work proceeds.

Report three separate outcomes:

| Outcome | Completion condition |
| --- | --- |
| Update implemented | Scoped implementation is finished and its local acceptance checks pass; no locally actionable material defect remains. |
| Evaluation complete for available environments | Every runnable required case executed and its outcome/evidence is retained; unavailable targets and exact next checks are recorded. This can include failing scores. |
| Release ready | All required release checks pass and no material defect or required unverified target remains. |

Commit and push the source, review receipts, `evals/results/`, `evals/attempts/`,
and `evals/LATEST.md` together to a review branch in the designated GitHub
repository, including honest failed and incomplete results. Do not hold evidence
publication hostage to release readiness. Preserve unrelated user changes and
state an exact blocker if publication cannot run. Compare published content
with the recorded inventory; do not claim an unevaluated change was tested.
Merge, tag, or publish a release only when authorized and its gates pass.

This workflow applies to plugin builds and repair releases. A narrower request
to edit the builder's instructions or one fixture stays within that scope:
validate the changed instructions/fixtures and their affected behavior without
recursively launching an all-harness plugin release.

Treat status questions and frustration as steering, not cancellation. Explain
what remains and continue; do not interrupt workers or describe a stop as
user-requested unless the user actually asked to stop.
