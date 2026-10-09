# Source-record filing boundaries

These four synthetic scenarios distinguish a new direct import from processing
an existing inbox capture. They extend the calendar-reschedule fixture without
changing the earlier comparison or activation scenarios.

| Scenario | Boundary under test |
| --- | --- |
| accessible-source-link-only | Link to an explicitly reachable native source without fetching or manufacturing a local payload. |
| direct-calendar-import | File a supplied update directly, retaining its external source without manufacturing an inbox capture or evidence copy. |
| duplicate-inbox-capture | Reuse the filed current record and remove only the verified identical inbox working item, without creating an archive duplicate. |
| duplicate-preserved-original | Reuse the filed record and leave the existing historical inbox archive copy untouched, without creating more copies. |

Rubrics inspect final payloads, current/historical links, evidence copies, and
reported completion. They do not infer the sequence of operations. Fixtures
contain only synthetic records and require no connectors or credentials.

Run with the full plugin context and natural selection, preserving baseline
comparison and recording the actual model. For example, from the repository:

```powershell
$scenarioPath = (Resolve-Path evals/tessl/source-record-boundaries).Path.Replace("\", "/")
$pluginPath = (Get-Location).Path.Replace("\", "/")
tessl eval run $scenarioPath --context $pluginPath --skip-forced-context-activation --label "Source-record filing boundaries"
```

Use absolute paths with forward slashes on Windows. Inspect each repeat's activation separately from
its artifact scores; an empty activation list alone does not establish whether
guidance influenced the result. Keep raw results and analysis in ignored
`docs/tessl/`. Scenario lint verifies structure, not agent performance.
