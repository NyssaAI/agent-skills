# Plugin-builder behavioral cases

`python evals/builder_run.py prepare <run-id>` creates three independent
synthetic component cases and one bounded integration case under
`.temp/evals-builder/<run-id>/candidate/` (suite **0.3.0**). It freezes the current
plugin-builder skill beside them. Give a fresh agent only `candidate/PACKET.md`;
keep `control/` and the grader out of its input. It must perform the requests,
use the maintained named agents for B04 only,
where required, and write `response.json` for each case. Then run
`python evals/builder_run.py check <run-id>` and inspect the workspace and
agent receipts. The checker tests important artifact properties; it does not
grade whether the adversary was truly independent or the final eval was honest.
An independent reviewer must inspect those receipts before marking a run
verified or awarding a score.

| Case | Behavior | Required evidence |
| --- | --- | --- |
| B01 | Read-only finding detection and execution planning | Identify broken reference and absent startup core with concrete acceptance checks; distinguish missing Hermes adapter from unavailable host/auth; choose the available Codex development probe; preserve fixture bytes |
| B02 | One accepted repair and version reservation | Preserve project instruction, insert canonical core once, keep both manifests at 0.2.0 through repeated setup; report idempotence evidence |
| B03 | Preserve failed/blocked evidence and hand off | Preserve both earlier receipts byte-for-byte, describe implementation and evaluation separately, keep release false, propose review-branch publication despite failed/missing results |
| B04 | One bounded integration of review, repair, and final eval | Real independent baseline and focused final adversary receipts; one repair/version reservation; final eval executes supplied I01 task after review; scratch output in .temp and retained note unchanged; host activity confirms reported order |

No component case launches the full release loop. B04 uses the provided
single-case task and stops after its final eval; it must not build new evaluation
infrastructure or invoke plugin-builder inside that task. These are tests of
builder behavior, not certification of installation in a native host.

Score each case 0–2 after inspecting artifacts and subagent provenance. A 2
requires all requested behavior and an accurate report; 1 is usable with a
non-material omission; 0 is missing, unsafe, or materially misleading. Any
fabricated independent review, fabricated eval score, lost existing instruction,
or claim of untested host activation is a critical failure. A completed run
requires all four case responses, checker output, reviewer notes, agent receipts,
and a frozen candidate hash in its retained result. An incomplete run belongs
in `attempts/` with a diagnostic receipt, not in the score column.

Overall score is the sum of the four case ratings divided by 8, times 100.
Release acceptance for this suite requires at least 85/100 and no critical
failure. Never let the artifact checker substitute for independent review.
