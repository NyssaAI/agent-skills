# Synthetic per-harness loop

Scope: the supplied alpha and beta adapter contract only. `host-probe.py` is a local synthetic loader, not a native agent harness. No installation, agent evaluation, or release certification was performed.

| Harness | Contract and deliverables | Activation and acceptance check | Initial-core evidence | Final-core evidence | Disposition |
| --- | --- | --- | --- | --- | --- |
| alpha | `adapters/alpha.json` resolves `../core.md` to the canonical `core.md`; existing adapter retained | `python host-probe.py alpha`; exit 0, loaded core text and hash match | Event 1: Pass, core SHA-256 `1a0996784ff69c37a086415c8ea2dcf0b1b937bd65d73104b19d7d2f88979387` | Event 3: Pass, core SHA-256 `5efbe8548220ea844d7974b4f4783dcc774faf3e4d09c217c89585f8284db09a` | Local synthetic integration verified for v2; native runtime unverified |
| beta | New `adapters/beta.json` resolves `../core.md` to the same canonical `core.md` | `python host-probe.py beta`; exit 0, loaded core text and hash match | Event 2: Pass, same v1 core hash | Event 4: Pass, same v2 core hash | Local synthetic integration verified for v2; native runtime unverified |

The first two probe events tested the initial v1 core. Changing shared `core.md` invalidated those results for the final content, so both probes were repeated. Events 3 and 4 load exactly `Foundation v2: preserve notes and use .temp/.` followed by a newline. All four events remain in append-only `probe-events.jsonl`. Both adapters have SHA-256 `21c72c583d6f1052eb4504c368eede027a26c8b23a2f56b82b77eb686ac8571d`. The retained user note and supplied probe were not changed.

Implementation is complete against this synthetic contract. Evaluation is complete only for the two supplied local probes. Native host activation, independent agent evaluation, and release readiness are outside this fixture and unverified.
