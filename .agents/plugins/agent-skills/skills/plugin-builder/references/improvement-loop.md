# Per-harness implementation and verification loop

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
than calling them failures or passes.

The first development probe must exercise the installed candidate on an available
target before substantial repairs: discovery, the startup foundation before
selection when promised, and one real operation. Keep fixtures under `.temp/`,
but establish host isolation explicitly: repository ancestors, user instructions,
registrations, and previously loaded context must not supply the plugin's rules.
A nested scratch directory alone does not establish isolation. Retain the actual
loaded paths and redacted host output; a self-report that the foundation loaded
is insufficient when an inherited copy could explain it. A contaminated probe
is unverified and must be repeated with isolation before claiming activation.
For a new plugin, build only the minimal installable path needed for this probe.
For an explicitly scoped component or instruction edit, exercise that component
instead and record that native installation is outside this acceptance scope.
Use the existing runner, scorer, and verifier. Missing adapters or verifier code
are implementation work; unavailable authentication or hosts are external
blockers. Record either before continuing independent work. Leave final scoring
to `eval`.

## Agree on evidence before changing its verifier

For each claimed capability, record its acceptance check, evidence producer,
retained artifacts or host trace, independent review, and replay method. State
what is trusted: ordinary evaluation relies on observed execution and independent
review; hashes detect changed bytes, not whether a trusted evaluator fabricated
them. Require stronger attestation only when the task's threat model calls for
it. Do not silently turn ordinary evaluation into resistance to a malicious
authorized evaluator. A field such as `verified: true` alone proves nothing.

Before accepting a verifier repair, exercise a known-valid evidence fixture and
relevant invalid fixtures, including the actual counterexample. Calibration is
not a model run. A verifier that rejects every Pass is unfinished implementation,
even if it blocks the counterexample. Keep the acceptance requirement visible;
do not relabel absent verifier code as an unavailable host or waive the gate.

## Maintain visible run state

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

At the top, maintain one short current-state block: phase, candidate identity,
active finding, worker/task ID, last completed action with timestamp, next action,
and blocker. Update it at phase changes and after each verified fix; keep the
append-only history below it. Define an inactivity check interval at run start
(default five minutes). If no observable action or artifact appears in that
interval, inspect worker status, last tool result, and resource contention.
Distinguish a long-running command from a failed worker before intervening.
Record the diagnosis and recovery; elapsed time alone is not cancellation or
permission to duplicate an active worker. Continue giving concise user updates
while waiting. Disposable logs and analysis belong in `.temp/`.

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

After two unsuccessful repairs of the same finding, pause further edits to that
finding for a mandatory diagnosis checkpoint. Record the smallest reproducer,
why both checks missed it, the revised causal explanation and acceptance check,
and a materially different next action. Then resume the scoped repair; this is
not a waiver, a request to restart broad review, or an automatic end to the task.
A reviewer must link repeated findings to their stable ID so renaming them does
not reset this count.

Put disposable analysis, trial assemblies, fixtures, command logs, and
downloaded artifacts under the working root's `.temp/plugin-review/`; exclude
that directory from package assembly and Git. Preserve completed failed eval
exports under `evals/results/` and incomplete or aborted attempt receipts under
`evals/attempts/` as required by the eval contract, not only in `.temp/`.

## Iterate per harness

After establishing the shared core and acceptance checks, work through each
required harness with the loop below. Start with an available representative
host so the early installed-package probe informs the other integrations.
Keep one canonical implementation; this is an execution order, not permission
to fork workflows or create a separate business implementation for each host.

1. **Establish the contract.** Confirm the target's package, loader, activation,
   and capability requirements. An unknown contract stays unresolved. A
   provisional target such as Muse must have an explicit disposition; do not
   invent its interface, imply support, or silently remove a required target.
2. **Record deliverables.** Give each required capability its actual source and
   assembled file paths, registration/activation command or host step, local
   implementation acceptance check, and native runtime verification check.
   Include discovery, foundation, routing, and applicable hooks, agents, CLI/MCP
   connections and settings behavior. Reference shared files when no dedicated
   adapter is necessary, with evidence that the host can consume them. A guide
   describing an adapter is not the adapter; metadata alone is not activation.
3. **Implement and assemble.** Build the smallest adapter to the shared core,
   register its capabilities, and generate any required host-specific package.
   Resolve this harness's findings using the repair loop below.
4. **Verify before advancing.** Run local package/reference checks, then install
   and activate in an isolated host when available. Confirm discovery, promised
   startup foundation before routing, selected procedures, and real operations
   for applicable capabilities. Check repeat installation and user-settings
   preservation. Retain commands, observations, source/artifact identities and
   dependencies, including honest failures; do not defer all host checks until
   the final evaluator.
5. **Diagnose and repeat on failure.** Classify the cause, repair the responsible
   layer, regenerate artifacts, and repeat affected checks for this harness.
   Keep the repeated-repair diagnosis checkpoint and stable finding IDs.
6. **Record the disposition.** Keep implementation and runtime verification in
   separate columns. Advance from a verified harness, or one whose complete
   implementation passes local checks but whose runtime is externally blocked.
   Record the exact external dependency and next check; it remains a release
   blocker. Missing code, adapter, activation path, or contract is incomplete
   implementation, even if that host is also unavailable. Keep it open while
   doing independent work on other targets; do not count advancing as completion.

The durable per-harness table must contain target/capability, contract status,
actual deliverable paths, activation path, implementation status/evidence,
runtime status/evidence, dependency hashes, and remaining action. Label an
inapplicable capability with its reason instead of creating an empty adapter.
Only a user-authorized scope change can remove a required target or capability.

After the individual loops, verify cross-harness interactions: installing or
updating one artifact preserves the others and their registrations/settings,
and all adapters still use the canonical content. A shared-core, assembly,
settings, or loader change reopens affected earlier harness verifications.
Identify consumers from the dependency inventories; when impact is unknown,
treat all possible consumers as affected. Reverify their changed behavior and
record new evidence before marking them verified again. This is development
verification; the independent final evaluator still owns the last quality gate.

**Implementation completion gate:** every required harness/capability must have
real deliverables and passing local implementation acceptance. Missing or
unresolved implementation blocks "update implemented", even when all runnable
behavioral evals pass. External runtime blockers may coexist with implementation
completion, but never with a release-ready claim. Adversary and eval findings
return to the affected harness loop; shared findings reopen all affected loops.

## Repair one finding at a time within the loop

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
   Before prescribing a fix, inspect raw outputs and classify the cause as
   plugin behavior, runner/encoding/scoring, missing implementation, or external
   execution blocker. Separate observed facts from unverified hypotheses. A
   parser error means the behavior could not be graded, not that the asserted
   behavior was violated. Preserve the original score and artifact; repair the
   responsible layer without editing the evaluated workspace or inventing a
   pass. An unresolved grading error still blocks acceptance.
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
Declare each suite's source, shared guidance, adapter, runtime configuration,
fixture, runner, and scoring dependencies before using selective reevaluation.
Run focused cases during repair; the final evaluator runs the affected suites
and verifies any carried-forward results against those inventories. Changes to
shared foundation, discovery/loading, or scoring require broader coverage of
their consumers. If dependencies are unknown, rerun rather than assume isolation.
Record reuse as carried-forward evidence with its original run identity, never
as a fresh execution. Review-only history or unrelated documentation changes
do not force behavioral reruns when the dependency evidence establishes that.
Link failures and attempts to findings and keep the same unreleased version.
An external execution blocker stays in the matrix while independent work proceeds.

Report three separate outcomes:

| Outcome | Completion condition |
| --- | --- |
| Update implemented | Every required harness/capability has actual deliverables, an established activation path, and passing local implementation checks; no required implementation or contract is missing or unresolved. Runtime-only external blockers are reported separately. |
| Evaluation complete for available environments | Every runnable required case executed and its outcome/evidence is retained; unavailable targets and exact next checks are recorded. This can include failing scores. |
| Release ready | All required release checks pass and no material defect or required unverified target remains. |

Commit and push the source, `evals/results/`, `evals/attempts/`,
`evals/LATEST.md`, and any review receipts authorized for publication together
to a review branch in the designated GitHub repository, including honest failed
and incomplete results. Keep private receipts local. Do not hold evidence
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
