# Plugin Evaluation CLI

The scored suites exercise the three canonical `agent-skills` skills (`manage-file-operations`, `para-vault`, and `write-like-me`) across isolated synthetic tasks:

- **`file-and-para-24`** (`C01`–`C24`): 24 isolated user tasks exercising `para-vault` (`workflows/file.md`, `workflows/reconcile.md`, `workflows/archive.md`, `workflows/navigate.md`, `workflows/import-records.md`) and `manage-file-operations`. Structured `daily-tasks` work records (`RecordKind`: `project`, `milestone`, `task`, `blocker`, `daily-plan`) use `state` (`ProjectState`, `MilestoneState`, `TaskState`, `BlockerState`) and `1-projects/YYYY.MM.DD-<slug>/project-index.md` (`C02`, `C04`, `C12`, `C13`, `C14`), whereas knowledge/resource notes use `document-maturity` (`C03`, `C16`, `C17`, `C18`). `C17` exercises explicitly authorized legacy `status` $\rightarrow$ `document-maturity` migration while preserving `state` and accepted history; `C18` checks legacy reading, conflicting fields, and rejection of operational `status` values as maturity without mutating source notes.
- **`startup-and-discovery`** (`H01`–`H03`): Fresh-host startup foundation, progressive disclosure, and `harness-adapter` bundle discovery probes ([host-probes.md](host-probes.md)).
- **`writing-voice`** (`WV01`–`WV06`, `SC01`–`SC05`, `AC01`–`AC04`): 15-case synthetic `write-like-me` suite covering `Writing Voice Profile` safety, modes, approved learning, missing profiles, `user_home` vs `repo_root` `.nyssa-ai/` isolation, retired `.nyssaai` rejection (`SC05`), and positive/negative activation controls.

## Directory Layout

- `evals/cases.py`, `evals/configuration_cases.py`, `evals/scoring.py`, `evals/run.py`, `evals/calibrate.py`, `evals/plugin_checks.py`, `evals/report.py` — evaluation harness and validators.
- `evals/verifiers/` — hash-pinned historical verifier snapshots (`revisions.json`, `file-and-para-24-0.6.0/`, `configuration-scopes/`) used to replay historical exports without executing untrusted receipt code.
- `evals/tessl/` — Tessl scenario definitions (`para-composition/`, `source-record-boundaries/`, `calendar-routing/`, `writing-voice/`).
- `evals/reports/` — tracked durable evaluation reports and verified receipt ledger (`evidence-ledger.json`).
- `evals/LATEST.md` — tracked generated summary table verified by `python3 evals/report.py check`.
- `<repo_root>/.temp/evals/` — gitignored local workspace for prepared runs (`.temp/evals/<run-id>/`), raw scored exports (`.temp/evals/results/<run-id>/`), and incomplete/unverified attempt receipts (`.temp/evals/attempts/<run-id>/`).

## Commands

From `<repo_root>`:

```bash
python3 scripts/assemble.py write
python3 scripts/assemble.py check
python3 evals/run.py validate
python3 evals/report.py check
pytest test/unit test/use_case
```

### Prepare, Execute, Score, and Verify a Run

```bash
python3 evals/run.py prepare run-01
python3 evals/run.py prepare voice-01 --suite writing-voice
python3 evals/run.py execute .temp/evals/run-01 --command-json '["candidate-runner", "--workspace", "{candidate}", "--prompt-stdin"]' --timeout 1800
python3 evals/run.py review-template .temp/evals/run-01 --output .temp/evals/run-01/control/review.json
python3 evals/run.py score .temp/evals/run-01 --review .temp/evals/run-01/control/review.json --export .temp/evals/results/run-01
python3 evals/run.py verify .temp/evals/results/run-01
python3 evals/calibrate.py .temp/evals/run-01 --output .temp/eval-calibration.json
```

After adding or updating raw evidence under `.temp/evals/results/` or `.temp/evals/attempts/`, run `python3 evals/report.py generate` to refresh `evals/reports/evidence-ledger.json` and `evals/LATEST.md`, then verify with `python3 evals/report.py check`. `python3 evals/report.py release` requires live `.temp/evals/results/` artifacts and fails on any missing, stale, or failing required row in [`matrix.json`](matrix.json).

## Revision Integrity & Security Invariants

Historical exports select `evals/verifiers/revisions.json` by exact `(suite, suite_revision, suite_sha256)` tuple and verify pinned SHA-256 hashes before replaying repository-owned grader snapshots. Exported `grader.zip` archives are hash-checked for integrity and never executed. `startup-and-discovery` rows continue to reject self-certified `Pass` claims until a trusted native host-session attestation verifier is available.
