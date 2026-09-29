# Latest builder process evaluation

Corpus: plugin-builder-process 0.2.0 (P01-P07).

Latest completed run: [harness-loop-final-20260929](results/harness-loop-final-20260929/result.json),
2026-09-29 23:34:37 UTC. **Pass: 100/100 (14/14)**, no critical failures.
All seven cases were freshly executed by one independent Codex CLI candidate
and graded by a separate evaluator. Both synthetic P06 harnesses passed before
and after the shared-core change, and the evaluator's disposable replay passed.
Inputs matched live source at completion; scoped freshness is separate from
the root report's whole-plugin freshness.

| Case | Points | Retained response |
| --- | --- | --- |
| P01 | 2/2 | [Startup probe decisions](results/harness-loop-final-20260929/P01/response.json) |
| P02 | 2/2 | [Raw-artifact diagnosis](results/harness-loop-final-20260929/P02/response.json) |
| P03 | 2/2 | [Repeated-repair recovery](results/harness-loop-final-20260929/P03/response.json) |
| P04 | 2/2 | [Affected-suite reevaluation](results/harness-loop-final-20260929/P04/response.json) |
| P05 | 2/2 | [Worker and completion status](results/harness-loop-final-20260929/P05/response.json) |
| P06 | 2/2 | [Harness repair and shared-core reverification](results/harness-loop-final-20260929/P06/response.json) |
| P07 | 2/2 | [Incomplete required harness coverage](results/harness-loop-final-20260929/P07/response.json) |

Scoped input SHA-256:
`9db2bcd6700ee32cbc4e73fa45da3bbd12695c2775383c9ff1395cb6299ac6e5`.
Corpus SHA-256:
`3315f77991f910942eab6adb1abbd6c4f41ab5fef0163dfd794d7c67f4c40d3d`.
Rubric SHA-256:
`5a3feb18196ea13355be9de7ba21cbdc9a2949f2e13b5839b3231749e1a65e67`.
Full source inventory: [frozen.json](results/harness-loop-final-20260929/frozen.json).

[Independent ratings](results/harness-loop-final-20260929/reviewer.md),
[host provenance](results/harness-loop-final-20260929/provenance.json),
[preservation checks](results/harness-loop-final-20260929/preservation.json),
[final replay](results/harness-loop-final-20260929/replay.json), and
[complete candidate archive](results/harness-loop-final-20260929/candidate.zip)
retain the evidence. All 33 protected original candidate files, 19 frozen source
files and 92 prior evidence files remained unchanged. P06 changed only its
authorized core and added its adapter, loop record and probe events.

Codex CLI 0.155.1 ran a fresh session after the collaboration host rejected
a spawn for its thread limit. Effective model/version are unknown. Existing
user/repository instructions and authenticated configuration were not isolated;
this is an instruction-bounded decision test, not native startup certification.
These supplied-host decisions and synthetic probes supplement B01-B04; they
do not certify real harness support, installation, coexistence, crashed-worker
recovery, actual release efficiency or whole-plugin release readiness. Source
and this new evidence are local pending publication.

Historical result: [process-final-20260929](results/process-final-20260929/result.json)
scored 100/100 on corpus 0.1.0 (P01-P05). Its evidence remains unchanged; its
source/corpus identity is historical and does not certify the current 0.2.0
corpus or harness-loop delta.
