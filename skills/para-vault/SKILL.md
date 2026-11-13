---
name: para-vault
description: >-
  Use this skill when the user asks to "file this note into PARA", "process vault inbox", "organize my PARA vault",
  "reconcile vault documents", "propose note revision", "archive this project", "reactivate archived note",
  "check vault navigation", "repair broken MOC links", or "import calendar/email records into vault".
  Covers the full PARA knowledge lifecycle (Projects, Areas, Resources, Archives).
  Do NOT use this skill for live `daily-tasks` planning sessions, check-ins, action-item extraction, or structured task/milestone/blocker authoring (use `daily-tasks`),
  standalone filesystem moves, renames, or copies outside PARA vault classification (use `manage-file-operations`),
  or personal-voice email/communication drafting and style emulation (use `write-like-me`).
---

# PARA Vault Manager

> [!IMPORTANT] Scope Directive
> This is the Sibling Facade Skill and orchestrator for PARA knowledge and work-record vault management inside `vault_root`. It routes vault operations through internal progressive workflows and references, aligned directly with `daily-tasks` for `1-projects/` and `2-areas/daily-plans/`. Cross-plugin and sibling routing boundaries:
> - **Live planning, check-ins & structured work-record authoring (`daily-tasks`)**: Route live `daily-tasks` planning sessions, daily-plan selection, check-ins, unaccepted action-item extraction, and structured `task`/`milestone`/`blocker` authoring to **`daily-tasks`**.
> - **Standalone filesystem operations (`manage-file-operations`)**: Route standalone non-destructive filesystem moves, renames, and copies outside PARA vault classification to **`manage-file-operations`**.
> - **Personal-voice drafting & style emulation (`write-like-me`)**: Route first-person email/communication drafting and personal-voice style emulation to **`write-like-me`**.

---

## The PARA Vault Lifecycle

```text
PARA Vault Architecture (vault_root)
│
├── 1. Placement & Record Import
│   ├── Inbox Capture Filing & Classification ──> workflows/file.md
│   └── Source Records (Email/Calendar) ────────> workflows/import-records.md
│
├── 2. Maintenance & Revisions
│   ├── Document Reconciliation ────────────────> workflows/reconcile.md
│   └── Navigation, Indexes & MOCs ─────────────> workflows/navigate.md
│
└── 3. Lifecycle Transitions
    └── Project Archiving & Reactivation ───────> workflows/archive.md
```

---

## Triage Matrix: Selecting the Action Runbook

Match the user's intent to the appropriate workflow:

| User Intent / Request | Target Runbook | Core Output / Focus |
| :--- | :--- | :--- |
| **File notes, process `0-inbox/`, create `Project`** | [`workflows/file.md`](workflows/file.md) | Classify into `PARA Category` folders, file `Inbox Capture` items, create `1-projects/YYYY.MM.DD-<slug>/project-index.md`. |
| **Reconcile notes or propose/apply revisions** | [`workflows/reconcile.md`](workflows/reconcile.md) | Reconcile overlapping prose notes, preserve valid `daily-tasks` `RecordKind` work records intact, apply protected canonical changes. |
| **Archive or reactivate projects/notes** | [`workflows/archive.md`](workflows/archive.md) | Move completed `Project` bundles to `4-archives/`, preserve provenance metadata, reactivate when needed. |
| **Audit or repair indexes, links, MOCs** | [`workflows/navigate.md`](workflows/navigate.md) | Check collection registers, fix broken wikilinks, preserve `<!-- ref: UUID -->` anchors, ensure index ownership. |
| **Import email or calendar `Source Record` files** | [`workflows/import-records.md`](workflows/import-records.md) | Import `Source Record` payloads, resolve timestamps, preserve immutable native evidence bytes. |

---

## Core Guidelines & Invariants

1. **Four-Category Evaluation Order (`PARA Category`)**: Evaluate placement in strict order: **Projects** (`1-projects/`, active finite efforts) $\rightarrow$ **Areas** (`2-areas/`, ongoing responsibilities including canonical `2-areas/daily-plans/YYYY.MM.DD-daily-plan.md`) $\rightarrow$ **Resources** (`3-resources/`, reference topics) $\rightarrow$ **Archives** (`4-archives/`, inactive history).
2. **`daily-tasks` Work-Record Alignment (`RecordKind` & `state`)**: Projects (`project`), Milestones (`milestone`), Tasks (`task`), External Blockers (`blocker`), and Daily Plans (`daily-plan`) use `state` (`ProjectState`, `MilestoneState`, `TaskState`, `BlockerState`) and `## Definition of Done` checklists without requiring `document-maturity`. Never write retired `task-state`. Knowledge and resource notes (`2-areas/` non-plan notes, `3-resources/`) use `document-maturity`.
3. **Zero `.nyssa-ai/` Inside `vault_root`**: Never create `.nyssa-ai/` configuration, secrets, or runtime state inside `vault_root`; only `vault_root/.temp/` is permitted for disposable scratch.
4. **Native Evidence & Protected Canonical Revisions**: Never modify or inject YAML into native `Source Record` payloads (`.eml`, `.ics`). For substantive changes to `established` or `canonical: true` knowledge notes, draft a proposal and preserve durable historical snapshots before applying changes.
5. **Non-Destructive Movement**: Compose with `manage-file-operations` when moving or renaming items; verify destination content and link integrity before removing the working source.

---

## Verification

Before reporting completion of any PARA vault task:
- [ ] Confirm prose notes (`document-maturity`) and `daily-tasks` work records (`RecordKind` + `state`, never writing `task-state`) conform to [`references/frontmatter-schemas.md`](references/frontmatter-schemas.md).
- [ ] Confirm related collection indexes, `project-index.md` files, and MOCs have been updated with valid relative links and intact `<!-- ref: UUID -->` / `## Definition of Done` markers.
- [ ] Confirm original native `Source Record` files remain bit-for-bit identical and zero `.nyssa-ai/` directories exist inside `vault_root`.
- [ ] For lifecycle changes, verify `state` (`completed`, `cancelled`, `resolved`) and archive fields (`archived`, `archived-from`, `archive-reason`) are accurately recorded.
