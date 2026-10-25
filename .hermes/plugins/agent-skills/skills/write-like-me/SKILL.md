---
name: write-like-me
description: >-
  Use this skill when the user asks to "draft this email in my voice", "rewrite this message like me",
  "sound like me", "learn my writing style", "update my voice profile", or "inspect my writing voice".
  Covers personal writing style emulation, tone calibration, and profile maintenance.
  Do NOT use this skill for filing notes or organizing vaults (use `para-vault`) or raw file operations (use `manage-file-operations`).
---

# Write Like Me

> [!IMPORTANT] Scope Directive
> This is the unified facade and orchestrator for authentic user writing voice emulation and profile maintenance. It routes between runtime drafting and administrative voice profile management. It owns voice emulation, style calibration, and learning from approved edits. It does NOT own filing drafted notes into a PARA vault (delegated to `para-vault`) or raw filesystem mechanics (delegated to `manage-file-operations`).

---

## Triage Matrix: Selecting the Action Runbook

Match the user's intent to the appropriate workflow:

| User Intent / Request | Target Runbook | Core Output / Focus |
| :--- | :--- | :--- |
| **Draft or rewrite in personal voice** | [`workflows/draft.md`](workflows/draft.md) | Draft emails, chat messages, posts, or memos preserving user habits, facts, and intent. |
| **Setup, inspect, or calibrate voice profile** | [`workflows/maintain.md`](workflows/maintain.md) | Extract habits from samples, update `VOICE.md`/`STYLE.md`, learn from approved edits. |

---

## Core Guidelines & Invariants

1. **Facts & Intent Preservation**: Emulating voice never authorizes changing supplied facts, commitments, constraints, or uncertainty levels.
2. **Drafting Reads; Maintenance Writes**: Ordinary drafting reads profile files and leaves their bytes unchanged. Profile updates occur only when explicitly requested or when draft corrections are approved for learning.
3. **Evidence-Backed Calibration**: Base tone guidelines strictly on authentic user samples, never on agent hallucinations or third-party boilerplate.
4. **Scope Precedence**: Resolve configurations in canonical order: explicit pointer $\rightarrow$ project override (`.nyssa-ai/agent-skills/writing-voice/`) $\rightarrow$ user fallback (`~/.nyssa-ai/agent-skills/writing-voice/`).

---

## Verification

Before reporting completion of any writing voice task:
- [ ] For drafting tasks, confirm facts and meaning match the source request, with personal tone applied without altering commitments.
- [ ] For profile updates, verify modified files are saved in the authorized user or project scope.
- [ ] Confirm no private scratch or confidential sample text leaks into persistent public outputs.
- [ ] Confirm `VOICE.md` and `STYLE.md` conform to the profile schema in [`references/profile-schema.md`](references/profile-schema.md).
