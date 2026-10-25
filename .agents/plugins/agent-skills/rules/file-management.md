---
trigger: always_on
description: Core file-management naming and safety rules.
---

# File-management foundation

> [!IMPORTANT] Scope Directive
> This foundation defines workspace file management invariants, naming standards, temporary workspace rules (`.temp/`), plugin configuration scopes, and PARA vault placement basics. It does NOT define voice profile emulation (owned by `writing-voice.md`).

## File Operations & Naming

- **Do** apply these conventions whenever creating, moving, renaming, copying, or modifying files and folders.
- **Do** prioritize user instructions and established local directory schemes before falling back to defaults; do not invent new top-level directories.
- **Do** preserve existing file names and file extensions unless a rename or conversion is explicitly requested.
- **Do** format new file and folder names in lowercase kebab-case (`kebab-case`).
- **Do** prefix time-bound deliverables with the true creation or production date in `YYYY.MM.DD-descriptive-slug` format.
- **Do Not** invent unknown dates or substitute file import/copy dates for creation dates.
- **Do Not** overwrite existing files without first verifying identity and collision state.
- **Do Not** remove source files before verifying that target content, cross-references, and index links are intact.
- **Do Not** delete retained content without explicit user authorization; archive within the existing scheme instead.
- **Do** use `manage-file-operations` to safely move, rename, copy, import, archive, resolve collisions, or resume interrupted operations.

## Temporary Workspace & Scratch

- **Do** isolate disposable task output, intermediate artifacts, and scratch files under `.temp/` at the working workspace root.
- **Do** preserve existing, unrelated temporary work residing in `.temp/`.
- **Do Not** place disposable scratch or intermediate work in tracked delivery folders.

## Plugin Configuration & Scopes

- **Do** store plugin-owned configuration and persistent state outside installation caches.
- **Do** read personal preferences from `<user-home>/.nyssa-ai/<plugin-name>/` and project overrides from `<project-root>/.nyssa-ai/<plugin-name>/`.
- **Do** resolve user home and project roots independently using exact paths; do not recursively scan user home.
- **Do** respect configuration aliases (`.nyssaai`, `.nyssa`) using explicit pointer, canonical, then legacy precedence; report conflicts without merging or deleting sources.
- **Do** apply explicit task instructions as runtime overrides without persisting them to saved configuration.
- **Do Not** include private configuration, credentials, or scratch files in published packages.

## PARA Foundation Basics

- **Do** apply PARA guidelines exclusively within recognized PARA vaults; follow local conventions before catalog defaults.
- **Do** assign each vault item exactly one current working home based strictly on current operational use.
- **Do** use `para-vault` whenever filing captures, organizing inboxes, revising notes, archiving projects, or ingesting vault records.
- **Do Not** classify PARA items by age, format, document maturity, or source authority.
