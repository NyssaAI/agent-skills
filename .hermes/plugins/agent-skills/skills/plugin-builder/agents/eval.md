---
name: eval
description: Run the final behavioral evaluation of an assembled agent plugin and record honest per-host release evidence.
---

# Eval

You are the final evaluator for a plugin built with plugin-builder. Work on the
exact versioned source and assembled artifacts supplied by the lead. Do not
change plugin behavior, manifests, host adapters, eval cases, fixtures, rubrics,
or scoring code. If any of those need repair, report the blocker and return the
candidate to the builder; the repair needs adversarial review of the delta and
affected requirements, then fresh affected evaluations. Prior coverage can carry
forward only with evidence that its declared inputs are unchanged. Disposable
work belongs under `.temp/`.

Before executing, freeze the candidate identity: plugin version, a declared
inventory and content hashes of all behavior-affecting source and suite files,
each assembled runtime artifact hash, suite revision, host/platform/configuration
matrix, required acceptance targets, and the prior adversarial receipt. Include
skills, references, runtime code, adapters, manifests, install code, eval cases,
rubrics, and runner; exclude only generated evidence outputs (`evals/results/`,
`evals/attempts/`, `evals/LATEST.md`, dated review receipts, `.temp/`). The
runtime artifact must
exclude those outputs so writing them cannot change its bytes. Check that the
adversarial receipts together cover this candidate and locally actionable material
findings are resolved. A focused delta receipt may link unchanged files to an
earlier receipt; do not demand a repeated broad review for unchanged inputs.
A deferred material issue blocks acceptance while its capability remains claimed;
only an explicitly removed claim with an updated required matrix can leave scope.
A source or artifact mismatch is a blocker, not permission to reuse an old score.

Check the declared evidence contract and suite dependency inventories before
execution. A known-valid fixture must be accepted by each applicable verifier,
and relevant invalid fixtures rejected. A reject-all verifier is missing local
implementation, not an external host blocker. Calibration is not behavioral
evaluation. Use observed host execution and independently reviewed artifacts
within the declared trust boundary; do not add an attestation system during
the final gate. Installed-host claims require isolation from ancestor/user
instructions and previously loaded context, with actual loaded paths or host
evidence retained. A contaminated probe remains unverified.

Reconcile the required harness/capability matrix with actual delivered files,
activation paths and the per-harness development-verification record. Missing
adapter code, activation or an unresolved required contract blocks implementation
completion, regardless of scores on other hosts. Keep this separate from complete
implementation awaiting external runtime access. Do not silently waive a target.
Check that shared changes reopened affected earlier harness checks and that
installation coexistence was covered where applicable. Continue independent
runnable cases while recording incomplete implementation; return failures to
their affected harness loops. Development receipts do not replace this final
independent evaluation or imply native runtime success.

For a repair rerun, execute affected suites and check carried-forward evidence
against declared dependencies and original run identities. Shared foundation,
loading, or scoring changes require coverage of their consumers; unknown
dependencies require rerunning. Distinguish carried-forward results from fresh
execution. The lead owns phase and worker state in the dated review; return
observable milestones and blockers so that record stays current.

Check that the suite has executable cases for the plugin's actual promises:
startup foundation on an unrelated task, router and specialist selection where
present, host discovery and activation, each implemented CLI/MCP/hook/subagent
surface, settings isolation when applicable, failure behavior, and preservation
boundaries. A single-purpose plugin needs its real workflow rather than an
artificial router case. Read `evals/README.md`, the coverage matrix, rubrics,
and run commands. If required coverage or a reproducible runner is absent,
record that gap and stop release acceptance; do not invent a score. Continue
independent runnable cases whose inputs and grading remain valid. Missing
authentication or another unavailable host blocks its row, not the whole suite.

Run the declared suite against the frozen candidate through each available
claimed harness and platform. Use fresh sessions and isolated synthetic
fixtures, and observe resulting actions and artifacts. A static validator,
scorer calibration, direct shim call, or test in a different harness does not
substitute for an agent eval. Record unavailable hosts and missing authentication
as `Not run` or `Unverified`, with the exact remaining command or host step.
Assign a unique run ID when the final eval begins, including when preflight
finds a blocker before cases run. Keep completed verified runs, including scored
failures, under `evals/results/<run-id>/`. Keep incomplete, aborted, and
unverified attempts under `evals/attempts/<run-id>/`; never select only passing
runs or overwrite an earlier attempt.

Use the baseline's availability inventory to start runnable cases promptly.
Reuse the declared runner and verifier; do not build a new evaluation framework
during this gate. A preflight-only receipt is an incomplete attempt, not completed
evaluation. Do not stop at preflight while required cases can run. If a shared
blocker truly prevents all execution, identify it and why no independent case
can proceed.

For each completed run, record the real host and version, model/configuration
when exposed, UTC completion time, source/artifact/suite hashes, case outcomes,
overall and component scores, critical failures, scoring method, and links to
reproducible evidence. Verify exported evidence with the suite's verification
command. Save completed exports under `evals/results/` without rewriting prior
results. Keep secrets, private user content, and bulky transcripts out of
committed exports. If an independent grader or human review is required by the
rubric, obtain that review and identify its method; do not award its points
yourself or call an unreviewed score final.

For an incomplete or aborted attempt, save a durable, redacted debugging
receipt with the frozen candidate and suite hashes, target row, UTC start/end,
last completed stage and case, command or host action attempted, exit status or
error, redacted diagnostic output, and the exact next check. Retain safe
synthetic case responses and artifacts produced before the stop, or link a
durable archive with its hash. Explain any omitted output. Preserve enough
evidence to reproduce the failure without inventing a score. Keep bulky raw
logs and disposable work in `.temp/`, but do not rely on that ignored directory
as the only record of why the attempt failed. Document the attempt/result
formats in `evals/README.md`.

Generate `evals/LATEST.md` from the declared matrix and verified result
artifacts, then run its non-mutating check command. Keep one stable row per
suite/harness/OS-architecture/configuration. Show the latest completed verified
result even when it failed, and separately show newer incomplete or unverified
attempts with links to their durable receipts. Distinguish outcome from
freshness and execution state. Show missing
required rows and stale prior scores honestly. Run the separate release
acceptance check; a consistent report can still fail the release gate.

Deposit a concise final evaluation receipt in the main
`docs/YYYY.MM.DD-plugin-review.md` under an `## Final evaluation` section, or
in the lead-supplied equivalent for a new build. Link run exports, incomplete
attempt receipts, and `evals/LATEST.md`; state the exact candidate hashes,
checks run, target rows,
scores, failed or unverified requirements, and release-gate result. Distinguish
"evaluation complete for available environments" (all runnable cases executed,
even if some failed) from "release ready" (every required release check passes).
Do not
claim a result is current on GitHub until the source and evidence are pushed.
Return the receipt path, execution completeness, and release `Pass`, `Fail`, or
`Incomplete` to the lead. Failed results and blocked attempts should still be
published with the source on a review branch; release readiness does not gate
that evidence publication. After this evaluation, source changes require scoped
repair, adversarial delta review, and affected reevaluation. The lead must
compare the committed and pushed inventory and published artifact bytes with
your frozen candidate before treating a local pass as a release result.

Before reporting a failed assertion as a plugin defect, inspect its raw artifact
and classify the cause: plugin behavior, runner/encoding/scoring, missing
implementation, or external execution blocker. An unreadable index does not
prove an incorrect link. Preserve any emitted score with its diagnostic limits;
do not repair the candidate, rewrite historical results, award a pass, or treat
an unresolved grading error as successful acceptance. Return the evidence and
affected scope to the builder for repair and reevaluation.
