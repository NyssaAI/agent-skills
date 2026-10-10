# Project-local writing voice storage

## Resolve the root

Use the user's explicit project/workspace root first, then the applicable repository root. A nested working directory is not a separate project. In a non-Git workspace, use its established working root. Inspect project context and existing configuration before creating anything; ask only when the root is genuinely ambiguous. Never silently choose the home directory or create competing profile roots.

Resolve this location on each relevant task:

```text
<project-root>/.nyssa-ai/agent-skills/writing-voice/
  VOICE.md
  STYLE.md       # optional; create only when editorial standards are needed
  examples/      # approved, curated examples
```

All plugin-owned persistent configuration belongs beneath `<project-root>/.nyssa-ai/agent-skills/`; this reference owns the writing-voice subdivision. The dot-prefix does not require a Windows Hidden attribute. Each project has its own profile. Do not synchronize globally, inherit another project's profile, or introduce multi-person selection.

Read existing user-selected samples or profiles when authorized. Preserve their original location and content. Requested setup or updating may copy approved derived guidance into this contract; do not automatically migrate, move, or delete source material. Profile data belongs outside plugin installation caches and the public skill source.

## Privacy and temporary work

Before persisting a private profile, use the project's accepted ignore convention or a narrowly scoped local exclusion for `/.nyssa-ai/agent-skills/writing-voice/`. In a Git repository, a local `.git/info/exclude` entry can avoid changing tracked policy; respect existing exclusions and verify with `git check-ignore` against the intended files. Also check whether any profile files are already tracked: ignore rules do not protect tracked content. Do not silently remove tracked files or alter a user's sharing decision. If privacy cannot be verified, keep proposed profile content in the conversation and report what blocks safe persistence.

Do not ignore all `.nyssa-ai/`; sibling plugins may have different sharing policies. Sharing a profile requires an explicit decision. In a non-Git project, inspect the actual applicable sharing/packaging rules rather than claiming the dot-prefix protects data. A Git exclusion protects against accidental Git inclusion, not against other synchronization services. Packages must exclude project configuration and scratch data.

Keep disposable calibration drafts, comparisons, and recovery copies under `<project-root>/.temp/agent-skills/writing-voice/`. Verify this private scratch location is excluded before writing samples, drafts, or recovery content there, using the same tracked-file and sharing checks as for the profile. If the existing project exclusion does not cover it, use the narrowly scoped `/.temp/agent-skills/writing-voice/` exclusion; do not assume `.temp/` is already ignored. Preserve unrelated temporary work. Raw samples are not persistent configuration by default. Retain excerpts or complete examples only with user approval; avoid unrelated personal details. Use readable Markdown without an opaque database or mandatory settings file.

## Safe profile writes

1. Read the existing files, their identity, and relevant project conventions. Determine the exact authorized change; profile creation does not authorize replacing unrelated files at the same path.
2. For substantive revisions, preserve the previous content through existing recoverable history or a noncolliding recovery copy in the scratch location before writing. Do not assume private files are backed up by Git. Keep that recovery content available until the result is verified and accepted.
3. Recheck the current file before replacement. If it changed since inspection or a destination belongs to unrelated content, stop the dependent write, reconcile the collision, and preserve both versions. An interrupted update must inspect current and recovery content before resuming.
4. Write only the approved portions; preserve unrelated profile guidance. Use noncolliding example names, preserving known dates and existing names. Do not invent sample dates.
5. Read back the result, check schema and relative example links, and verify private-data exclusion. Report the profile paths and recovery location when used. Delete retained content only with explicit authorization.

Use [manage-file-operations](../../manage-file-operations/SKILL.md) when copying, moving, importing, or archiving existing content or resolving destination collisions. Ordinary drafting performs none of these profile writes.
