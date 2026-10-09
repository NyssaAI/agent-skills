---
name: import-vault-source-records
description: "Process supplied email records and calendar invitations in a PARA vault, including filing an inbox invitation or reschedule. Use for duplicate deliveries, organizer updates, cancellations, or unresolved source identity and event dates."
metadata:
  version: "0.1.3"
---

# Import Vault Source Records

Ingest supplied email and calendar records using available authorized inputs and tools. This skill does not set up a connector or authorize fetching or sending messages.

1. Resolve accepted rules and locations through [shared vault conventions](../file-para-content/references/vault-conventions.md). Read [source destinations](../file-para-content/references/folder-conventions.md#source-record-destinations) and the [date/timezone guidance](../revise-vault-documents/references/frontmatter-schemas.md#date-meanings-and-configuration) before selecting a dated path.
2. Read [source-record identity and updates](references/source-records.md). Compare source identifiers, payload, provenance, and applicable update ordering against retained records. Reuse exact duplicates; retain differing versions and distinguish organizer updates, attendee replies, recurring series, and exceptions.
3. Resolve missing information from reliable supplied evidence. Preserve unresolved native payloads in the accepted inbox and record what is missing rather than inventing a date or current version. Complete independent records while that decision remains unresolved.
4. For records already captured in an inbox, follow [inbox filing](../file-para-content/SKILL.md#file-the-content), even when their destination is known. Preserve its required unchanged original in the accepted preserved-originals location, including for native invitations; the filed working record does not replace this evidence copy. Newly supplied records with a direct destination need no inbox detour. Distinguish copying a supplied source from moving a processed inbox working item; an import does not authorize removing the supplied source. Use [manage-file-operations](../manage-file-operations/SKILL.md) for actual transfers, collisions, and retries. Native payloads remain unchanged; metadata belongs in a capture, index annotation, or companion as applicable.
5. Apply [navigation guidance](../maintain-vault-navigation/references/navigation.md#index-ownership-and-links) to current and historical links. Verify payload preservation and intended targets; current links and cancellation state must follow applicable source evidence, not import order.

Report retained/reused records, current versus historical versions, final locations, date fallbacks, and missing information. Ask only when missing evidence or authorization prevents a requested decision; report routine choices under accepted conventions without asking for confirmation. Independently authored notes needing reconciliation belong to [revise-vault-documents](../revise-vault-documents/SKILL.md).
