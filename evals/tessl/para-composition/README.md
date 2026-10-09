# PARA composition evaluations

Five task scenarios reuse the existing synthetic fixtures from C03, C09, C14,
C17, and C21 in `evals/cases.py`. Rubrics score visible final artifacts; they do
not claim to observe hidden execution order. An unrelated-writing scenario is
used only for natural activation. No external fixtures or setup scripts are used.

| Scenario | Primary workflow | Original case |
| --- | --- | --- |
| inbox-filing | file-para-content | C03 |
| navigation-review | maintain-vault-navigation | C21 |
| reactivate-project | manage-vault-lifecycle | C14 |
| calendar-reschedule | import-vault-source-records | C09 |
| approved-revision | revise-vault-documents | C17 |

Run natural activation across this directory first using the full plugin context,
`--skip-baseline --skip-forced-context-activation --skip-scoring`, and a label.
Run scored baseline-versus-context evaluations on `performance/` with the full
plugin context and a separate label. Use absolute scenario and context paths on
Windows. Do not use a skill filter: dependencies and shared guidance are part of
the composition being measured. Record the agent/model actually returned by Tessl.

To verify outcomes under natural selection, keep
`--skip-forced-context-activation` but omit `--skip-scoring`. A targeted rerun can
use `--skip-baseline` when an unchanged scenario already has baseline evidence;
report it separately from the earlier full run rather than implying every case
was rerun on the new version.

These scenarios sample the workflows; they do not cover every capability or prove
host installation support. Keep raw results and analysis under private `docs/`.
