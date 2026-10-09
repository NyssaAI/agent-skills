# Document Revisions

## Reconcile independently authored notes

For independently authored notes, overlapping text or subject matter alone does not establish redundancy. Preserve unique content and provenance, identify contradictory claims, and do not merge or archive merely because the notes overlap. When reconciliation is requested, distinguish supported resolutions from unresolved claims and apply protected-revision rules to substantive changes in established notes. Canonical precedence selects the governing document; it does not by itself disprove every differing claim. Ask only when an unresolved conflict prevents the requested reconciliation.

## Protected revisions

For a substantive revision to an established note, create a sibling `<original-stem>-proposed-revision.md`, applying collision handling if necessary. This is a proposal, not an additional MOC or project index, so use `type: note`, its own `created` date, `document-maturity: draft`, and `canonical: false`. Link to the accepted original in the body and describe the proposed changes and supporting evidence. Preserve the original and its existing canonical links while approval is pending. An explicit instruction approving that specific revision already supplies approval; do not ask again.

After approval:

1. Preserve the accepted version in verified durable version history that can actually restore it. If such history is unavailable, save an unchanged snapshot as `YYYY.MM.DD-<original-stem>-prior-version.md` in the resolved archive location, using the snapshot date and collision rules. Create its companion metadata note under the [archive workflow](../../manage-vault-lifecycle/references/lifecycle.md#archive-workflow). Do not use the temporary location as the sole durable copy of an accepted version.
2. For the same document purpose, apply the approved content at the original path, preserving its original `created` date, filename, and canonical designation. Editing permission alone is not evidence that every new claim is established: use `established` when the user accepts the revised document as reliable, `reviewed` when it has been checked but not accepted, or `draft` while provisional. Preserve source evidence and useful content.
3. For a changed purpose, retain the original until the user approves a replacement and explicitly identifies which document becomes the source of truth. Transfer authority and redirect current links only as authorized; label the superseded document and preserve its history.
4. Update existing relevant indexes and mark the proposal as applied in its body, with a link to the accepted document. Archive it when authorized under the archive rules; do not leave it apparently pending or delete it without authorization.

Minor corrections and routine index maintenance can be applied directly when they preserve accepted meaning. Before overwriting, retain a recoverable copy in existing version history or the temporary location until the result is verified; substantive accepted-version preservation follows the durable procedure above. Do not use revision proposals to justify unrelated cleanup.
