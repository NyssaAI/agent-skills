# Workflow: Import Vault Source Records

> [!IMPORTANT] Scope Directive
> This workflow handles importing supplied email and calendar `Source Record` payloads into `vault_root`, resolving source versions and dates, and preserving immutable native evidence. It does NOT own setting up email/calendar API connectors, general file operations (owned by `manage-file-operations`), candidate task extraction/acceptance (owned by `daily-tasks`), or reconciling independently authored notes (owned by `reconcile.md`).

Import supplied email and calendar `Source Record` files into `vault_root` using available authorized inputs and tools. This workflow does not set up a communication connector or authorize fetching or sending messages.

1. Resolve accepted rules and locations through [shared vault conventions](../references/vault-conventions.md). Read [source destinations](../references/folder-conventions.md#source-record-destinations) to decide between a source reference and needed local evidence. The live email/calendar service governs current source state; a retained `Source Record` is an observed snapshot. Keep a local payload only for requested retention, historical evidence, offline access, or an otherwise unavailable source. Use a source link and identifier when enough; never invent either. Read the [date/timezone guidance](../references/frontmatter-schemas.md#date-meanings-and-configuration) before selecting a dated path.
2. Read [source-record identity and updates](../references/source-records.md). Compare source identifiers (`Message-ID`, `UID`, `RECURRENCE-ID`), payload bytes, provenance, and applicable update ordering (`SEQUENCE`, `DTSTAMP`) against retained records. Reuse exact duplicates; retain differing versions and distinguish organizer updates, attendee replies, recurring series, and exceptions.
3. Resolve missing information from reliable supplied evidence. Preserve unresolved native payloads as an `Inbox Capture` in `0-inbox/` and record what is missing rather than inventing a date or current version. Complete independent records while that decision remains unresolved.
4. For records already captured in `0-inbox/`, follow [inbox filing](file.md), even when their destination is known. File needed native evidence once, or reuse an identical retained record; do not manufacture a second original in `0-inbox/archive/`. Newly supplied records with a direct destination need no inbox detour. Distinguish copying a supplied external source from moving a processed `Inbox Capture`; an import does not authorize deleting the external source or discarding an existing local payload solely because a link is available. Use [manage-file-operations](../../manage-file-operations/SKILL.md) for actual transfers, collisions, and retries. Native payloads remain unchanged; metadata belongs in a capture note, index annotation, or archive companion as applicable.
5. Apply [navigation guidance](../references/navigation.md#index-ownership-and-links) to current and historical links. Verify payload preservation and intended targets; current links and cancellation state must follow applicable source evidence, not import order.

Report source references, retained/reused snapshots and why needed, current versus historical observations, final locations, date fallbacks, and missing information. State when live source state could not be checked; local version ordering does not prove it. Ask only when missing evidence or authorization prevents a requested decision; report routine choices under accepted conventions without asking for confirmation. Independently authored notes needing reconciliation belong to [reconcile](reconcile.md). When imported email or calendar `Source Record` payloads surface candidate action items that the user wants tracked as tasks, milestones, or daily plans, route candidate extraction and acceptance to **`daily-tasks`** (never hand-authoring unaccepted `daily-tasks` task records during general note filing or source import).

---

## Verification

Before reporting completion of any `Source Record` import task:
- [ ] Confirm retained `.eml` and `.ics` payloads remain bit-for-bit identical to supplied sources without injected YAML frontmatter or altered bytes.
- [ ] Confirm source identifiers (`Message-ID`, `UID`, `RECURRENCE-ID`) and version ordering (`SEQUENCE`, `DTSTAMP`) accurately distinguish exact duplicates, updates, replies, and recurring exceptions.
- [ ] Confirm records lacking reliable dates or version evidence remain in `0-inbox/` with explicit questions rather than invented dates, and candidate action items were routed to `daily-tasks`.
- [ ] Confirm destination indexes, companion notes, and current-versus-historical links resolve to the intended payloads.
