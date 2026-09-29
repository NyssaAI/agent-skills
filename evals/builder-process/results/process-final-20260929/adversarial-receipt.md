# Plugin-builder process adversarial review

## Scope and result

Independent reviewer: `process_adversary`, using the complete maintained
`skills/plugin-builder/agents/adversary.md` instructions. Review date:
2026-09-29. Base Git revision: `03be9d9df3e339381b3c8e90356a425a52db7010`.
The hashes below identify the reviewed working-tree candidate, including
uncommitted files; the base revision alone does not identify this candidate.

Reviewed the seven approved process corrections in the four canonical builder
instruction files, the new supplemental process corpus, its root catalog entry,
and the single supplemental link added to the report generator. Inspected raw
current files and the tracked diff. Checked the corresponding generated copies.
This is an instruction/component review, not an all-host release review.
Existing startup verifier implementation and historical runtime defects are
outside this scope. Pending final evaluation and `LATEST.md` are not defects
at this phase.

**No actionable finding remains in the scoped candidate.** This result accepts
the process design and fixture/rubric consistency for independent behavioral
evaluation; it does not award that evaluation a score or certify native hosts.

## Candidate identity

SHA-256 of raw file bytes:

| File | SHA-256 |
| --- | --- |
| `skills/plugin-builder/SKILL.md` | `b8ac3a9a5cc38081759c426d2b9ed5ad5c85eb549974e2929ecce1c67d005c2e` |
| `skills/plugin-builder/references/improvement-loop.md` | `6c88a318063a2688bce2a0a83d8d5fa2ea7a0f03a51ce9f9111b87a660ee1085` |
| `skills/plugin-builder/agents/adversary.md` | `766d8b2e2cfacdfa912c2527efaaf6860f93eeabfc921baa6cfcd2b586185b56` |
| `skills/plugin-builder/agents/eval.md` | `8005c0a6d5acddf3aac9ff7c2e243c668f5648028636bb561f21d6c2a69060f7` |
| `evals/builder-process/README.md` | `a70d67e874f911add428e6ef1c5cb4c4378abb9e00870faeffbddcd8b719c8e6` |
| `evals/builder-process/cases.json` | `8b467cd31a469130fa2b2960dad918f9253165421383cfc07d3c35b795df5b8d` |
| `evals/builder-process/rubric.md` | `116af7c71930a2e9e46fe292c47f634137c8be41fde4154574819f9dadc7d79c` |
| `evals/README.md` | `b4af4a79d4e30d44e8fd45049165cd6743d229ea3f24032d37538e983021f09e` |
| `evals/report.py` | `5ec50b996e4c95db5a7619a27437d7ffc5de14827fc1d7ff28d06f58fc0f7e33` |

For `report.py`, semantic review covers only the added supplemental link;
the whole-file hash identifies where that delta was reviewed.

## Checks and evidence

- Read all scoped files directly, plus the lead's dated scope and evidence
  contract. Compared tracked changes with `git diff` and read the untracked
  corpus directly. `git diff --check` on the tracked scoped files passed;
  Git emitted only its LF/CRLF checkout warnings.
- Compared raw bytes for each of the four canonical instruction files with
  `.agents/plugins/agent-skills/skills/plugin-builder/` counterparts. All
  matched. Also compared both canonical agent definitions with the generated
  package-root `agents/adversary.md` and `agents/eval.md`; both matched.
- Parsed `cases.json` with Python, verified distinct ordered IDs P01-P05,
  encoded and decoded every fixture using its declared encoding, and parsed
  every nested JSON fixture successfully. No candidate source or fixture was
  changed by these checks.
- Verified P02's raw intended fixture bytes: the CP1252 dash produces byte
  `0x97`, and strict UTF-8 decoding fails as claimed. Direct examination of
  the index and ICS text confirms that `current.ics` has sequence 4 and
  `old.ics` sequence 2. Console-rendered mojibake is not a fixture defect.
- Checked every local Markdown file target in the scoped Markdown files for
  existence. All existed, including the process latest-score placeholder.
  This was a file-target check, not a native host invocation or anchor parser.

## Process and coverage assessment

| Requirement | Assessment |
| --- | --- |
| Early executable evidence | The lead must probe discovery, promised foundation, and one real operation before broad repair; P01 challenges inherited instructions and an operation never run. The explicit component exception is appropriate to this task and does not certify installation. |
| Evidence trust and verifier controls | Lead, adversary, and eval agree on observed execution, independent review, applicable replay, and positive/negative controls. P03 rejects both self-certification and reject-all behavior without inventing malicious-maintainer attestation requirements. |
| Bounded repeated repair | Two unsuccessful repairs trigger a stable-ID diagnosis checkpoint, concrete reproducer, causal revision, and materially different action. Work then resumes within scope; the rule neither waives findings nor forces broad review or abandonment. P03 exercises the threshold. |
| Failure attribution | The lead and evaluator inspect raw artifacts and separate plugin behavior, grading/encoding, missing implementation, and external blockers. P02 supplies a concrete encoding counterexample and requires preserving the score while withholding acceptance. |
| Selective reevaluation | Declared dependency inventories and unchanged inputs are required for reuse, original run identities remain visible, and unknown dependencies force rerun or inventory establishment. P04 exercises documentation, shared foundation, scorer, and unknown-dependency changes. |
| Visible progress and recovery | Current-state fields, an inactivity interval, and inspection before intervention are actionable. P05 tests recent activity versus perceived elapsed delay and distinguishes implementation, evaluation, and release status. The corpus expressly disclaims testing an actual crashed worker. |
| Supplemental eval integrity | Five independent decision cases cover the seven corrections, with protected-fixture hashes, separate reviewer scoring, critical failures, retained results, and explicit native-host limits. The root catalog/report additions do not replace or remove any required release row. |

The existing independent adversarial and final evaluator gates remain intact.
The changes preserve failed evidence, forbid invented passes, keep unavailable
targets visible, and distinguish evidence publication from release acceptance.
The new corpus is intentionally a bounded decision test rather than a recursive
plugin release. Its separate reviewer must still inspect actual responses and
fixture preservation; this review does not substitute for that run.

## Limits and next acceptance check

No host installation, runtime activation, network access, source repair, or
delegation occurred in this review. The Python checks validate fixture bytes
and file relationships, not model decisions. No historical runtime claim was
reopened, and no existing verifier defect was reclassified as resolved.

Next: the maintained independent eval agent should execute and separately grade
P01-P05 against this frozen candidate, retain responses and preservation hashes,
and publish scoped scores with the corpus's stated limits. If scoped source
changes before that run, review the delta and record its new hashes.
