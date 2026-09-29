# Plugin evaluation CLI

This suite exercises the `para-vault` and `file-management` skills through 24 isolated user tasks. A run means one independent candidate executes **all 24 cases**, producing real workspace artifacts and one JSON response per case. Three runs mean 72 case executions, not three executions of a linter.

Use `run.py` to prepare, execute, score, export, and verify runs. The [scoring rubric and coverage map](../docs/eval-suite.md) define what the scores mean.

## Set up

Requires Python 3.11 or later and PyYAML. From the repository root on Windows:

```powershell
python -m venv .temp/eval-venv
.temp/eval-venv/Scripts/python.exe -m pip install -r evals/requirements.txt
.temp/eval-venv/Scripts/python.exe evals/run.py validate
.temp/eval-venv/Scripts/python.exe -m unittest discover -s test -v
```

On macOS/Linux, use `.temp/eval-venv/bin/python` in place of the Windows Python path. The harness itself uses portable Python paths. Runtime/model installation and authentication are supplied by the host, not this plugin.

## Prepare a fresh run

```powershell
.temp/eval-venv/Scripts/python.exe evals/run.py prepare run-01
```

Preparation creates `.temp/evals/run-01/` and refuses to reuse an existing run id. It copies the plugin and creates all fixtures from `cases.py`. The prepared `control/suite.json` freezes the prompts, fixtures, assertions, and suite version; the manifest records its hash, the source commit, and all initial plugin/file hashes. Files in the worktree are snapshotted, so hashes identify the actual evaluated version even when it differs from the commit.

The candidate receives **only** `.temp/evals/run-01/candidate/PACKET.md` and access to that candidate directory. It must not see `control/`, `cases.py`, `scoring.py`, completed results, or the reviewer rubric. A read-only plugin snapshot plus a writable per-case workspace is the preferred host configuration. The packet is an instruction boundary; the Python harness does not establish an OS sandbox.

All cases supply synthetic records and a fixed date of September 29, 2026. Each workspace is a separate user environment. The candidate starts with the indicated skill and follows its references. These are explicit-invocation behavior tests, not automatic skill-discovery tests.

## Execute with a fresh agent

Give a fresh agent this instruction, replacing the run path:

> Read `.temp/evals/run-01/candidate/PACKET.md` and execute all its requests using the frozen plugin. Read only the candidate directory and host tools needed to operate it. Write only case workspaces and their response.json files. Do not read grading materials, delegate, contact external services, or modify the plugin/requests. Record missing-input questions instead of waiting. Report the case ids completed and runtime limitations.

Record the actual host, model/version if exposed, start/end time, execution receipt, and context/isolation policy under `control/manifest.json` → `execution`. Do not invent unavailable model identifiers, seeds, tokens, or tool transcripts. Put a textual host receipt in `control/execution-notes.md` when the host cannot export its transcript. Case responses are not a substitute for filesystem artifacts.

For a CLI candidate, `execute` accepts a JSON argument array, uses no shell, passes PACKET.md on stdin, and captures stdout/stderr:

```powershell
.temp/eval-venv/Scripts/python.exe evals/run.py execute .temp/evals/run-01 --command-json '["candidate-runner", "--workspace", "{candidate}", "--prompt-stdin"]' --timeout 1800
```

`candidate-runner` is a placeholder for your installed host adapter, not a bundled executable. `{candidate}` and `{packet}` are replaced only when they occupy an entire argument. The adapter must obey the packet, expose filesystem tools, and emit the requested response files; ordinary text generation alone is insufficient. Use the host's supported model and sandbox settings. Never put credentials in command arguments, which are retained in the execution receipt.

## Review and score

```powershell
.temp/eval-venv/Scripts/python.exe evals/run.py score .temp/evals/run-01
.temp/eval-venv/Scripts/python.exe evals/run.py review-template .temp/evals/run-01 --output .temp/evals/run-01/control/review.json
```

The first command produces a **provisional** score with no human-review credit. Fill every case's `score` (0, 1, or 2) and `evidence` in the review template, plus `reviewer` and `method`. Read actual responses and artifacts; do not assign scores solely from the candidate's claims. The reviewer can be a human or a disclosed independent reviewing agent. Never label agent review as human review.

```powershell
.temp/eval-venv/Scripts/python.exe evals/run.py score .temp/evals/run-01 --review .temp/evals/run-01/control/review.json --export evals/results/run-01
.temp/eval-venv/Scripts/python.exe evals/run.py verify evals/results/run-01
```

Exports refuse an existing directory and retain the frozen suite, manifest, per-check scores/evidence, review, candidate ZIP (skills, requests, responses, final artifacts), a grader source ZIP, and hashes. `verify` checks artifact integrity, safely extracts into `.temp/`, and recomputes the score exactly. Hashes detect accidental changes; they are not a signed attestation. The grader snapshot preserves the scoring implementation if the harness later changes.

For repeated trials, prepare and execute a fresh run each time. Never copy responses between runs, repair failed candidate artifacts before scoring, or count rescoring as a new run. Keep the same plugin/corpus hashes when comparing repeated runs. Changes to prompts, fixtures, or expected outcomes require a new suite version and fresh runs.

## Check scorer sensitivity

```powershell
.temp/eval-venv/Scripts/python.exe evals/calibrate.py .temp/evals/run-01 --output .temp/eval-calibration.json
```

Calibration copies a completed run into disposable workspaces and injects 12 known faults. It checks that the intended assertions fail and critical gates activate. Calibration results are **not model runs**. Some mutations expect the concrete artifacts in this corpus; a missing precondition is an error rather than a claimed detection.

## Maintainer surfaces

| File | Responsibility |
|---|---|
| `cases.py` | User requests, raw fixtures, and declarative expected outcomes |
| `scoring.py` | Outcome assertions, link resolution, scoring, and release gates |
| `run.py` | Preparation, candidate invocation, receipts, exports, replay |
| `plugin_checks.py` | Local skill/manifest/reference validation |
| `calibrate.py` | Known-fault scorer calibration |
| `../test/test_evals.py` | Harness behavior and evidence replay tests |

Add assertions about observable outcomes, not exact prose or a particular tool sequence. Use exact bytes for native or protected evidence, parsed fields for metadata, and resolved paths for navigation. Reserve critical gates for preservation, unauthorized changes, or misleading current state. Keep fixtures synthetic and avoid personal vault data in durable exports.
