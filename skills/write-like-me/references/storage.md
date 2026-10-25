# Scoped Writing Voice Storage

> [!IMPORTANT] Scope Directive
> This reference defines storage paths, atomic resolution rules (explicit pointer > project override > user fallback), privacy verification, and safe write procedures for writing voice profiles (`.nyssa-ai/agent-skills/writing-voice/`). It does NOT define schema fields (owned by `profile-schema.md`) or drafting workflows (owned by `drafting-and-review.md`).

## Resolve one complete bundle

Resolve the verified user home separately from the established project/workspace root. Use an explicit workspace binding, then the applicable repository root, or the established working root for non-Git work. A nested directory or subprocess cwd inside an installation cache does not change that binding. With no established project, resolve only user scope; never fabricate a project root. Installation scope does not restrict preference scope. Inspect exact conventional paths or an accepted explicit pointer, never recursively scan home.

Each scope stores the same bundle:

```text
<user-home>/.nyssa-ai/agent-skills/writing-voice/
<project-root>/.nyssa-ai/agent-skills/writing-voice/
  VOICE.md
  STYLE.md       # optional
  examples/      # approved curated examples, optional
```

Select an explicit task-selected profile first, otherwise the project bundle, otherwise the user bundle. Within a scope, an accepted explicit pointer wins; otherwise check `.nyssa-ai`, then existing `.nyssaai`, then existing `.nyssa` aliases at that scope root. Select one root without merging duplicates and report shadowed conflicting legacy locations. Legacy updates remain at the selected location until migration is requested; new stores use `.nyssa-ai`. Preserve original samples and legacy sources; no automatic relocation or deletion.

Selection is atomic: read VOICE, optional STYLE and examples only from the selected bundle. Never inherit a missing STYLE or examples from another scope or borrow another project's profile. Absence falls back; an existing incomplete or malformed bundle reports a diagnostic and does not silently fall through. Validate VOICE against [profile schema](profile-schema.md), and verify any style/example links before claiming a supported voice match. An empty root without VOICE is incomplete. When both bundles are absent, useful drafting continues from task instructions without claiming a profile match.

## Identify the write scope

Ordinary reads and one-off overrides never persist preferences. An explicit user request such as “for all projects” selects user scope, including from a project installation. An explicit project request requires the established project root. Reuse an accepted scope; otherwise new setup defaults to project scope when a project is established and user scope when none is established. State the chosen scope and exact destination before writing. Updating user defaults writes the user bundle even when a project override is active; inspect the destination independently of the selected read bundle. Personal setup requires no vault, project collection, or project decision-log entry. Report personal changes and their path in the task result. Project changes follow applicable project logging conventions.

Profile data belongs outside installation caches and public skill source. Do not introduce synchronization or multi-person selection.

## Privacy and temporary work

Before persisting a private profile, use the destination scope's accepted ignore convention or a narrowly scoped local exclusion for `/.nyssa-ai/agent-skills/writing-voice/`. For either scope, including a home directory that is itself versioned, inspect the repository covering the destination. In a Git repository, a local `.git/info/exclude` entry can avoid changing tracked policy; respect existing exclusions and verify with `git check-ignore` against the intended files. Also check whether any profile files are already tracked: ignore rules do not protect tracked content. Do not silently remove tracked files or alter a user's sharing decision. If privacy cannot be verified, keep proposed profile content in the conversation and report what blocks safe persistence.

Do not ignore all `.nyssa-ai/`; sibling plugins may have different sharing policies. Sharing a profile requires an explicit decision. In a non-Git project, inspect the actual applicable sharing/packaging rules rather than claiming the dot-prefix protects data. A Git exclusion protects against accidental Git inclusion, not against other synchronization services. Packages must exclude user and project configuration, legacy aliases, samples, and scratch data.

Keep disposable calibration drafts, comparisons, and recovery copies under the established workspace’s `.temp/agent-skills/writing-voice/`, or `<user-home>/.temp/agent-skills/writing-voice/` when no workspace is established. Never use an installed cache as scratch. Verify this private scratch location is excluded before writing samples, drafts, or recovery content there, using the same tracked-file and sharing checks as for the profile. If the existing project exclusion does not cover it, use the narrowly scoped `/.temp/agent-skills/writing-voice/` exclusion; do not assume `.temp/` is already ignored. Preserve unrelated temporary work. Raw samples are not persistent configuration by default. Retain excerpts or complete examples only with user approval; avoid unrelated personal details. Use readable Markdown without an opaque database or mandatory settings file.

## Safe profile writes

1. Read the existing files, their identity, and relevant project conventions. Determine the exact authorized change; profile creation does not authorize replacing unrelated files at the same path.
2. For substantive revisions, preserve the previous content through existing recoverable history or a noncolliding recovery copy in the scratch location before writing. Do not assume private files are backed up by Git. Keep that recovery content available until the result is verified and accepted.
3. Recheck the current file before replacement. If it changed since inspection or a destination belongs to unrelated content, stop the dependent write, reconcile the collision, and preserve both versions. An interrupted update must inspect current and recovery content before resuming.
4. Write only the approved portions; preserve unrelated profile guidance. Use noncolliding example names, preserving known dates and existing names. Do not invent sample dates.
5. Read back the result, check schema and relative example links, and verify private-data exclusion. Report the profile paths and recovery location when used. Delete retained content only with explicit authorization.

Use [manage-file-operations](../../manage-file-operations/SKILL.md) when copying, moving, importing, or archiving existing content or resolving destination collisions. Ordinary drafting performs none of these profile writes.
