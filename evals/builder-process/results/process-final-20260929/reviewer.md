# Independent process evaluation

Run `process-final-20260929` completed on 2026-09-29 at
22:11:15.475689 UTC. Reviewer `/root/process_eval` read the maintained
`skills/plugin-builder/agents/eval.md`, the declared corpus, rubric, focused
adversarial receipt, all actual responses, and every supplied workspace file.
The review is independent agent review, not human review or cryptographic
attestation. The explicit scope is P01-P05, corpus 0.1.0, on unreleased plugin
0.2.0. No native startup or all-host release gate was attempted.

**Scoped result: Pass, 100/100 (10/10 points), no critical failures.**

## Execution and identity

All 19 declared live source inputs and 29 protected candidate files matched
before execution. The scoped digest was independently recomputed from sorted,
compact JSON of the input-hash map:
`6a02d7bf543c2e5c7d8a7310b324ce69157ff57ee57e8d35d9cc05a88c3567c9`.
The focused adversarial receipt reports no actionable scoped finding and its
listed scoped source/corpus hashes match this candidate.

Exactly one fresh candidate was spawned with `fork_turns=none`, task ID
`/root/process_eval/process_candidate`, and only the prepared candidate path
plus the corpus execution request. The evaluator observed running status,
the five response files, the completion notification, and completed host status.
The full request, observations, unknown host/model details, and observation
limits are retained in [provenance.json](provenance.json) and
[candidate-request.txt](candidate-request.txt). No rubric or intended answers
were supplied to the candidate. Its detailed tool transcript was not exposed;
this receipt does not invent tool-level observations or native context isolation.

## Per-case review

### P01 — 2/2

[Response](P01/response.json), especially `diagnosis`, `next_actions`, and
`acceptance_checks`, identifies the only loaded source `repo/AGENTS.md` and
`operation_run: false`. It calls the probe contaminated and unverified. It
requires a fresh isolated Codex session, installed-candidate discovery, startup
foundation on an unrelated task before selection, and a real filing operation
before broad repairs. It separately classifies Claude authentication as an
external blocker and Hermes's absent adapter as implementation work. This
matches both raw JSON fixtures and every rubric requirement; no native success
is inferred from the supplied self-report.

### P02 — 2/2

[Response](P02/response.json), `observed_facts`, accurately reports byte `0x97`
and Windows-1252 decoding. Independent byte inspection confirms that the index
points Current to `current.ics` (UID planning, sequence 4) and Historical to
`old.ics` (same UID, sequence 2). `diagnosis` correctly attributes the error to
grading/encoding rather than proven precedence regression. It retains score
59 and the original failure assertion with a diagnostic qualification, proposes
repair of the responsible decoder/scorer layer, positive and true-regression
controls, and fresh affected final suites. `status.release` keeps acceptance
blocked. No replacement score or behavioral pass is invented.

### P03 — 2/2

[Response](P03/response.json) keeps ADV-06 open and identifies the local verifier
defect: `gate.py` rejects every Pass and the valid control was rejected. The
mandatory `diagnosis_checkpoint` links both failed repairs to the stable ID,
explains self-asserted flags/trace shape versus observed provenance, and gives
the valid/unobserved Pass pair as a concrete reproducer. It proposes a
materially different evidence-backed path, accepting positive controls and
rejecting fabricated flags/traces, mismatched artifacts and replay failures.
Its trust boundary uses observed execution and independent review and expressly
excludes malicious-maintainer attestation. It distinguishes retaining authentic
failed evidence from satisfying release acceptance. All required decisions are
present; ADV-06 is neither closed nor relabeled an external host blocker.

### P04 — 2/2

[Response](P04/response.json), `reevaluation_plan`, matches the raw dependency
sets: A carries filing, startup and CLI forward; B reruns filing and startup
while carrying CLI; C reruns filing while carrying startup and CLI. Legacy is
conservatively rerun for each independent change because its inventory is null.
`next_actions` and `acceptance_checks` require complete inventories, unchanged
dependency bytes/configuration, retained original run IDs/timestamps, and
explicit carried-forward labels. Final affected suites must execute; scorer
calibration or a cherry-picked case cannot substitute. The response does not
pretend to have performed any of these future evaluations.

### P05 — 2/2

[Response](P05/response.json) reads the supplied clock correctly: C07 was retained
two minutes ago and C08 started one minute ago. It keeps the active worker and
checks status/output/resources only if no progress occurs through the five-minute
interval (21:19Z measured from the latest observed action). The
`current_state_block` includes phase, candidate, F-09, worker, timestamped last
completed action, current action, next action and blockers. `status` states
implementation incomplete, evaluation incomplete at 7/24, and release not ready.
It separates missing verifier code from unavailable Claude authentication and
does not equate user frustration or total elapsed time with cancellation.

## Preservation and reproducibility

[preservation.json](preservation.json) records unchanged protected candidate
files, unchanged live source inputs, and unchanged 69 historical evidence files
from the reviewer snapshot. That historical snapshot was taken after spawn and
before responses appeared; its timing is explicit in [preflight.json](preflight.json).
Only the five expected `response.json` files were added to the candidate.
All responses parse as JSON. [initial.json](initial.json), [final.json](final.json),
[frozen.json](frozen.json), and [source-final.json](source-final.json) retain the
hash inventories. The full safe frozen skill, corpus, fixtures, and outputs
are in [candidate.zip](candidate.zip), verified by ZIP integrity check and
per-member SHA-256 comparison with `final.json`.

Archive SHA-256:
`bc6676576acac52119d38fec44542ec9c593bc8d53555a9ce3b2ae3cd772cec0`.

For reproduction, extract the archive to a new disposable candidate directory,
remove only its five prior response files from that new copy, verify the
remaining bytes against `initial.json`, and run the retained request in a fresh
agent. Keep [suite/rubric.md](suite/rubric.md) separate until execution completes.
The original archive and result are retained unchanged. The corpus uses host
fresh-agent execution and independent review; there is no separate supplemental
runner/report-check command, and none was invented for this gate.

## Limits

The five decision tests all executed and were independently reviewed. They
assess reasoning against supplied facts, not native discovery, installation,
startup isolation, runtime support, real wall-clock efficiency, or recovery
from an actual crashed worker. B01-B04 and verifier implementation are outside
this receipt. Whole-plugin release acceptance remains incomplete/unverified
by this scoped run. Source/evidence publication and a final published-byte
comparison remain the lead's work; the evaluator did not commit or push.
