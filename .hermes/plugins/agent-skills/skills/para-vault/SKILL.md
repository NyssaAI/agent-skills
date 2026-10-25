---
name: para-vault
description: >-
  Use this skill when the user asks to "file this note into PARA", "process vault inbox", "organize my PARA vault",
  "reconcile vault documents", "propose note revision", "archive this project", "reactivate archived note",
  "check vault navigation", "repair broken MOC links", or "import calendar/email records into vault".
  Covers the full PARA knowledge lifecycle (Projects, Areas, Resources, Archives).
  Do NOT use this skill for raw filesystem moves outside a PARA vault (use `manage-file-operations`)
  or drafting user communications (use `write-like-me`).
---

# PARA Vault Manager

> [!IMPORTANT] Scope Directive
> This is the unified facade and orchestrator for PARA knowledge management. It routes vault operations through internal progressive workflows and references. It owns vault classification, document revision, navigation integrity, lifecycle archiving, and source record imports. It does NOT own standalone file system safety mechanics (delegated to `manage-file-operations`) or personal voice drafting (delegated to `write-like-me`).

---

## The PARA Vault Lifecycle

```text
PARA Vault Architecture
│
├── 1. Ingestion & Placement
│   ├── Inbox Filing & Classification ──> workflows/file.md
│   └── Source Records (Email/Calendar) ─> workflows/import-records.md
│
├── 2. Maintenance & Revisions
│   ├── Document Reconciliation ─────────> workflows/reconcile.md
│   └── Navigation, Indexes & MOCs ──────> workflows/navigate.md
│
└── 3. Lifecycle Transitions
    └── Project Archiving & Reactivation ─> workflows/archive.md
```

---

## Triage Matrix: Selecting the Action Runbook

Match the user's intent to the appropriate workflow:

| User Intent / Request | Target Runbook | Core Output / Focus |
| :--- | :--- | :--- |
| **File notes, process inbox, create project** | [`workflows/file.md`](workflows/file.md) | Classify into Projects/Areas/Resources/Archives, file inbox items, create project indexes. |
| **Reconcile notes or propose/apply revisions** | [`workflows/reconcile.md`](workflows/reconcile.md) | Compare conflicting documents, author revision proposals, apply protected changes. |
| **Archive or reactivate projects/notes** | [`workflows/archive.md`](workflows/archive.md) | Move completed bundles to Archives, preserve provenance metadata, reactivate when needed. |
| **Audit or repair indexes, links, MOCs** | [`workflows/navigate.md`](workflows/navigate.md) | Check collection registers, fix broken wikilinks, ensure index ownership. |
| **Ingest email records or calendar invites** | [`workflows/import-records.md`](workflows/import-records.md) | Ingest source records, resolve timestamps, preserve immutable evidence payloads. |

---

## Core Guidelines & Invariants

1. **Four-Category Evaluation Order**: When classifying items, evaluate in strict order: **Projects** (active, finite) $\rightarrow$ **Areas** (ongoing standards) $\rightarrow$ **Resources** (reference topics) $\rightarrow$ **Archives** (inactive history).
2. **Native Evidence Preservation**: Never modify, rewrite, or delete native payloads (e.g. `.eml`, `.ics`, original attachments) during filing.
3. **Protected Revisions**: For substantive changes to established canonical notes, draft a proposal and preserve durable historical versions before applying changes.
4. **Non-Destructive Movement**: Always use `manage-file-operations` conventions when moving or renaming notes; verify destination existence and link integrity before removing the source.

---

## Verification

Before reporting completion of any PARA vault task:
- [ ] Confirm all target notes conform to frontmatter schemas in [`references/frontmatter-schemas.md`](references/frontmatter-schemas.md).
- [ ] Confirm related collection indexes and MOCs have been updated with valid relative links.
- [ ] Confirm original native evidence files remain bit-for-bit identical.
- [ ] For project state changes, verify lifecycle fields (`status`, `completed`, `archived-from`) are accurately recorded.
