# Builder process decision evals

This supplemental corpus, version **0.2.0**, tests recovery and execution
planning in plugin-builder. It complements B01-B04; it does not certify native
installation or replace a required release row. Latest scores and limitations
are in [LATEST.md](LATEST.md).

| Case | What is exercised |
| --- | --- |
| P01 | Early installed-plugin probe, inherited context, unavailable host |
| P02 | Raw artifact inspection before diagnosing a scoring failure |
| P03 | Repeated repair recovery, trust boundary, reject-all verifier |
| P04 | Dependency-based reevaluation and honest carried-forward evidence |
| P05 | Worker inactivity, run-state reporting, completion distinctions |
| P06 | Repair a missing synthetic harness adapter, verify both hosts, then reverify after a shared-core change |
| P07 | Reject multi-harness completion with missing implementation or an unresolved required contract |

Use the existing host's fresh-agent facility; no new runner or nested plugin
release is needed. Prepare a unique `.temp/plugin-review/<run-id>/candidate/`
with a frozen copy of `skills/plugin-builder/` and [cases.json](cases.json).
Materialize each case's `files` under `<case>/workspace/`, using its declared
encoding (UTF-8 when omitted). Keep the rubric and reviewer material outside
the candidate. Record hashes of the skill, cases, rubric, and initial fixture
bytes before execution. These are decision tests with supplied host facts, not
live host probes; fixture isolation does not claim native context isolation.

Give the candidate only this request with the prepared candidate path:

> Use the frozen plugin-builder skill to handle each independent case in
> cases.json. Inspect the supplied workspace artifacts and treat supplied host
> facts as this fixture's facts. For each case write `<case>/response.json` with
> observed facts and uncertainty, diagnosis, next actions, acceptance checks,
> and implementation/evaluation/release status where relevant. P06 alone permits
> its explicitly listed workspace changes and execution of its supplied synthetic
> probe; follow that case's bounded implementation request. Otherwise preserve
> fixtures. Do not install real hosts, delegate, execute a full plugin update,
> or access the network. Do not read grading material or prior results. Report limitations.

After execution, a separate evaluator reads [rubric.md](rubric.md), the actual
responses, and fixture bytes. Retain the candidate output, initial/final hashes,
host task IDs and observed activity, and reviewer evidence under
`results/<run-id>/`. Record unknown model/version fields as unknown. Inspect
preservation and score each case; no keyword matching substitutes for review.
For P06, inspect actual adapter/core bytes and the probe's chronological events:
both hosts must pass on v1 before the change, then both must pass on v2. Preserve
the probe, original adapter and user note; only the case's authorized paths may
change. Replay the supplied probe in a disposable copy when checking the final
adapter. That replay validates the fixture, not a native host or a fresh agent run.
Write `LATEST.md` with the newest completed score, per-case scores, source/corpus
hashes, limitations, and links to retained evidence. Keep older failures and
attempts, and mark a score stale when its declared skill/corpus inputs change.
These results use scoped hashes; the root report's whole-plugin freshness is a
separate release condition. Commit the source and evaluation evidence together.
