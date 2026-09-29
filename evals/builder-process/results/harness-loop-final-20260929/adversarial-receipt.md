# Plugin-builder harness-loop adversarial review

## Scope and verdict

Independent reviewer: `harness_loop_adversary`, using the full maintained
`skills/plugin-builder/agents/adversary.md` role. Review date: 2026-09-29.
Base revision: `b73f16cda88c24e8f87d0eef98c7cabda0a1d958`. The raw content hashes below identify the
reviewed working-tree delta; the base revision alone does not identify it.

Reviewed the per-harness implementation and verification instructions, the
adversary/eval role alignment, supplemental corpus 0.2.0 with P06/P07, and
its README, rubric and root catalog entry. This is a builder instruction and
component review. It neither requires nor certifies implementing real OpenClaw,
Hermes or Muse adapters. The lead is separately updating generated artifacts
and latest scores; their temporarily stale state is outside this source review.

**No actionable finding remains in this scoped candidate.** The instructions
and executable fixture support independent behavioral evaluation. This receipt
does not award that evaluation a score or establish release readiness.

The [prior scoped receipt](2026.09.29-plugin-builder-process-adversarial.md)
continues to cover unchanged baseline guidance, P01-P05 semantics and their
original evidence-trust, recovery and selective-reevaluation requirements.
The present delta does not invalidate that coverage. P01-P05 JSON formatting
changed, but their case requests and fixture values remain unchanged.

## Candidate identity

SHA-256 of raw source bytes:

| File | SHA-256 |
| --- | --- |
| `skills/plugin-builder/SKILL.md` | `bbf68baa2943bd326eba5acd17d57eb3ce06806d58bcbbec8dc04ec683e434e8` |
| `skills/plugin-builder/references/improvement-loop.md` | `d1b4b05749e5021db1b3d88e22545fab0d3b16a9b9a4edf661b51e45fb3668ea` |
| `skills/plugin-builder/agents/adversary.md` | `7af5a4ab7ab93c17c915936d6bc633a7007e40dbe017a3970c24e43f50b219f1` |
| `skills/plugin-builder/agents/eval.md` | `772c9d423879294b3173541db7cfa261528bb7fd3430eaf1a43a99dc5d300bdd` |
| `evals/builder-process/cases.json` | `3315f77991f910942eab6adb1abbd6c4f41ab5fef0163dfd794d7c67f4c40d3d` |
| `evals/builder-process/README.md` | `b26d664b26ff834eec3d18cce870ab48905ada235acd44a6e51f1ec02ef7dce8` |
| `evals/builder-process/rubric.md` | `5a3feb18196ea13355be9de7ba21cbdc9a2949f2e13b5839b3231749e1a65e67` |
| `evals/README.md` | `2685781230731683fdf4b56a969ad15e2c2161f48352d6ea8bf1c750e4129145` |

## Checks actually run

- Read the scoped source files, full maintained reviewer/evaluator definitions,
  prior receipt and diff against the base revision. Ran `git diff --check`
  over the eight scoped files: passed, with only Git checkout LF/CRLF warnings.
- Parsed corpus JSON, confirmed distinct ordered P01-P07 IDs, round-tripped
  every fixture through its declared encoding and parsed all nested JSON
  fixtures. Checked local Markdown file targets for existence and confirmed
  the new `#iterate-per-harness` link matches its heading.
- Materialized P06 exactly from corpus fixture bytes under
  `.temp/plugin-review/harness-loop-adversary-p06/`. Executed the unmodified
  supplied probe with Python. Alpha passed with v1; missing beta failed with
  exit 1. Created beta's canonical-core adapter, which passed with v1. Changed
  the core to the exact requested v2 text and executed both probes again:
  both passed with the new core hash. Parsed all five retained JSONL events,
  confirming the order and the two distinct source hashes.
- Verified protected alpha adapter, note and probe bytes remained unchanged.
  In a separate disposable copy, pointed beta at an identical-content duplicate
  core: the unmodified probe rejected it with exit 1 and the canonical-core
  error. The valid and invalid controls therefore exercise actual loader
  behavior rather than a reject-all or existence-only check.
- Rechecked every scoped source hash before writing this receipt. No source
  or retained candidate evidence was modified by this review. Only scratch
  fixtures and this receipt were written.

| Synthetic evidence | SHA-256 / result |
| --- | --- |
| v1 core | `1a0996784ff69c37a086415c8ea2dcf0b1b937bd65d73104b19d7d2f88979387` |
| v2 core | `5efbe8548220ea844d7974b4f4783dcc774faf3e4d09c217c89585f8284db09a` |
| Protected alpha adapter | `21c72c583d6f1052eb4504c368eede027a26c8b23a2f56b82b77eb686ac8571d` |
| Protected note | `d3b2a51de24ffd8c8aaf249ce85484cd685dc97cff41ed7c107ff83af3efee19` |
| Protected probe | `625d6fa3929604dc5a40276c674a6c7b57f035444afcaf1039a075c466b506a1` |
| Chronological outcomes | alpha/v1 Pass; missing beta Fail; beta/v1 Pass; alpha/v2 Pass; beta/v2 Pass |
| Duplicate-core control | Fail: adapter must load canonical `core.md` |

## Requirement assessment

| Requirement | Assessment |
| --- | --- |
| Per-harness verification before advancement | The loop establishes each contract, records actual paths and activation, implements/assembles, verifies, diagnoses failures and records a disposition before advancement. Missing implementation stays open while independent work can proceed; advancement is explicitly not completion. |
| Missing implementation versus external blocking | The implementation gate and both permanent roles reject absent code, activation or contracts even when a host is unavailable. Complete local implementation can coexist with an external runtime blocker, while release remains blocked. |
| Shared-core invalidation | Shared core, assembly, settings and loader changes reopen affected checks. Unknown impact includes every possible consumer. The independent final evaluator remains a separate gate. P06 requires both hosts to be reverified after v2. |
| Compatible shared-package route | The loop accepts shared files when supported by evidence, instead of requiring empty or unnecessary adapters. P07 explicitly tests this with its supplied OpenClaw contract. |
| Required target completeness | P07 distinguishes verified Codex/OpenClaw, implemented Claude with unavailable auth, missing Hermes integration and unresolved required Muse contract. It rejects unauthorized removal while permitting independent runnable work. These are fixture facts, not current host-format claims. |
| Corpus and rubric | Version, seven-case inventory and 14-point denominator agree. P06 requires actual artifacts, chronological execution and independent replay; P07 checks the completion distinctions. Protected-byte checks, exact v2 inspection and independent grading complement the probe, which alone checks loading rather than the entire case contract. |

The fixture's append-only event history is evidence under the existing observed
execution and independent-review contract, not tamper-resistant attestation.
The README also retains host task IDs/activity, and the rubric rejects invented
probe events. No stronger adversarial-maintainer trust model is claimed.

## Limits and next acceptance check

No native host installation, network access, independent candidate run,
source repair or delegation occurred. The direct Python probes establish that
P06 is executable and discriminates the tested controls; they do not test an
agent's decisions or native discovery, startup, activation and coexistence.
P07 was inspected as a decision fixture, not as evidence about real host support.
Generated package freshness and pending latest-score updates were not graded.

The next acceptance check is the separately observed fresh-agent P01-P07 run
and independent grading against these frozen sources, including preservation,
P06 chronological evidence and disposable replay. Any later source change
needs its own affected-delta check and updated identity.
