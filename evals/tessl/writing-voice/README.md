# Writing voice evaluation scaffold

These six performance scenarios and four natural activation controls contain
only synthetic evidence. **Hosted Tessl baseline-versus-context evaluation has not been executed.** Static
fixture checks, packaging results, and model self-scores do not prove voice
resemblance or native host delivery.

Fresh local Codex sessions exercised these ten scenarios on 2026-10-09.
Independent artifact/trace review awarded 60/60 across the six synthetic
performance cases and passed all four activation controls; 29 observable
artifact checks passed. See the [local probe receipt](../../attempts/local-writing-voice-20261009/metadata.json).
This is unverified release evidence: local skill-folder discovery does not
certify marketplace installation, trusted startup-hook delivery, hosted
baseline comparisons, or personal voice resemblance.

| Performance scenario | Plan scenarios | Primary workflow |
| --- | --- | --- |
| sparse-preferences-injection | 1, 2, 8 | maintain-writing-voice |
| modes-and-house-style | 3, 5, 11 | write-in-user-voice |
| approved-edits-interrupted-update | 4, 12 | maintain-writing-voice |
| missing-profile | 6 | write-in-user-voice |
| nested-project-isolation | 7 | write-in-user-voice |
| selected-source-preservation | 10 | maintain-writing-voice |

Plan scenario 9 requires an actual installation/update and archive inspection;
it is covered by the writing-voice H03 variant in
[host probes](../../host-probes.md), not a drafting model's promise about an
installation. Scenario 6 also has an unrelated explanation activation control.
Positive controls distinguish exact preference maintenance from read-only
application; the third-party house-style negative control rejects indiscriminate
personal voice activation. Existing unrelated-writing controls in the file and
PARA suites remain valid controls for those workflows, even when this composition
properly selects write-in-user-voice.

`build_writing_voice_cases()` in [cases.py](../../cases.py) provides the raw
fixtures and observable assertions independently of the unchanged C01–C24
runner. Tessl's `performance/` tasks use equivalent fixtures. Their weighted
checklists add independent review of meaning, uncertainty, mode choice, consent,
and evidence boundaries. A phrase/token check alone cannot establish factual
preservation: a draft can include every token while reversing a commitment.
Review actual output and retained artifacts, and compare source bytes.

Run only after composition lint, pack, archive inspection, and generated-package
validation succeed. Use the full plugin context and absolute Windows paths;
do not filter to one skill or expose criteria to the candidate. First run natural
activation across this directory with `--skip-baseline
--skip-forced-context-activation --skip-scoring` and a distinct label. Then run
scored baseline-versus-context performance evaluation on `performance/` with
another label. For natural-selection performance keep
`--skip-forced-context-activation` and omit `--skip-scoring`. Preserve model and
agent identifiers actually returned by Tessl; missing identifiers stay unknown.
Keep private raw results and analysis under ignored `docs/`, and disposable
execution artifacts in `.temp/`. Do not fabricate results or host receipts.

The pending matrix row records the work to execute; `report.py` currently has no
writing-voice export verifier and cannot certify a passing result for this suite.
Keep Tessl evidence separate until a compatible independent verifier exists.
Do not repurpose the file-and-PARA suite's score or its release rubric.

For subsequent authorized personal-sample work, use a private project workspace,
hold out approved examples from profile creation, and randomize/blind comparisons
between baseline and profile-assisted drafts. Record the model, fixtures, rubric,
factual-preservation findings, and the user's preference judgments. Disclose
reviewer identity and limitations. The current synthetic tests establish safety
and instruction-following coverage only; personal resemblance remains unmeasured.
