# Manage File Operations: Tessl evaluations

These six synthetic scenarios test the `manage-file-operations` skill without
operating on personal files. Each scenario supplies a nonempty local directory
fixture; no remote repository, credentials, or setup script is needed.

| Scenario | Expected behavior |
| --- | --- |
| `performance/move-with-navigation` | Relocate a folder and repair incoming and outgoing links and indexes. |
| `performance/rename-collision` | Preserve distinct records and select the first unused numeric suffix. |
| `performance/repeat-import` | Reuse an existing identical record and avoid duplicates on a second pass. |
| `performance/resume-partial-move` | Finish a partially completed move without duplicating or losing content. |
| `performance/copy-preserves-source` | Produce a usable copy while preserving its source and source references. |
| `activation-only/unrelated-writing-task` | Answer a writing request without activating either file operations or PARA. |

The task prompts do not name the skill or spell out the desired safety process.
Performance rubrics judge final workspace artifacts. Activation is measured
separately through Tessl's built-in skill-loading records. Preserve the same
tasks, fixtures, rubrics, and agent configuration when comparing revisions.

Tessl's file-based scorer cannot establish operation ordering or prove that a
second pass happened from final files alone. The recovery and import rubrics
were corrected after the first run to remove those process-observation demands.
They check content, deduplication, and navigation outcomes; they do not prove
that verification preceded cleanup or independently observe each import pass.

Run from the repository root after linking to the intended private Tessl project:

```powershell
tessl plugin lint .
tessl eval lint evals/tessl/manage-file-operations
$activationPath = (Resolve-Path evals/tessl/manage-file-operations).Path.Replace("\", "/")
$pluginPath = (Get-Location).Path.Replace("\", "/")
tessl eval run $activationPath --context $pluginPath --skip-forced-context-activation --skip-scoring --label "manage-file-operations initial activation" --json
$scenarioPath = (Resolve-Path evals/tessl/manage-file-operations/performance).Path.Replace("\", "/")
tessl eval run $scenarioPath --context $pluginPath --skill manage-file-operations --label "manage-file-operations initial performance" --json
```

Activation uses the full six-skill plugin to reveal workflow routing. The scoped
activation command discovers only the six cases listed above. Running against
the plugin root instead discovers all 20 scenarios under `evals/`: six file
operations, six PARA composition, five calendar routing, and three source-record
boundaries. Tessl CLI 0.113.0 rejected the relative
scenario-subdirectory invocation on Windows with an invalid-scenario-path error.
Absolute scenario and context paths with forward slashes successfully submit the
performance subset. Normalize separators on Windows to avoid mixed-path errors.
The Free plan requires omitting explicit agent/model selection; the initial
activation run uses `claude` / `deepseek-v4.1-flash`.

Performance compares the selected skill against Tessl's default no-context
baseline and excludes the unrelated writing case from forced activation.
These tests do not establish PARA coverage or native-host startup
integration. CLI submission alone is not a completed result.

Reusable scenarios belong here; downloaded run output belongs in `.temp/` and
retained private review notes belong in Git-ignored `docs/`.
