# Safe File Operations

## Identity and collisions

Before a write or move, inspect the source and destination. Match a returning item by its reliable identifier or content and provenance; a matching name alone does not prove identity. Reuse an existing identical item instead of creating a duplicate. Preserve both items when identity or differences remain uncertain.

Never overwrite an unrelated item. For distinct items that need the same name, append `-2`, `-3`, and so on before the extension, using the first unused name. Apply the suffix to a folder name when folders collide. Keep an established item's name stable on later imports or revisions; a retry of the same operation is not a new collision.

## Interrupted operations

Before retrying a partially completed create, copy, move, or archive, inspect the source, intended destination, any preserved original or backup, and affected references. Compare content and provenance while allowing for edits that the operation intentionally made.

If the destination belongs to the same operation, reuse verified completed work and finish only the missing steps. Verify destination content and references before removing a remaining source. If the source is already gone, finish missing references or metadata without recreating it. Do not reconstruct lost evidence by guessing.

If copies diverged beyond the intended changes or identity is uncertain, preserve both and resolve the difference before overwriting, merging, or removing either. Report unresolved recovery work instead of claiming completion.

## Moves, revisions, and archives

Use the destination supplied by the user or the existing organization. Do not
create a new top-level structure merely to complete a move. When moving or
renaming, verify destination content and repair affected links or references
before removing the working source. Update existing source and destination
folder indexes or registers to reflect the move, preserving useful
cross-references. Keep recoverable history for substantive revisions.

Archive in the existing archive location when the item's lifecycle or the
user's instruction calls for it. Preserve a folder's internal structure and
links. Delete retained content only when explicitly authorized.
