# File-management foundation

> [!IMPORTANT] Scope Directive
> This foundation defines file management invariants, naming standards, single-root `.temp/` scratch rules, `NyssaAI.Configuration` root precedence (`user_home`, `repo_root`, `runtime_root`, `vault_root`, `plugin_root`), and PARA vault placement basics. It does NOT define voice profile emulation (owned by `writing-voice.md`).

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

## Temporary Scratch (`.temp/`)

- **Do** isolate disposable task output, intermediate work, and staged build outputs under a single `.temp/` directory at `repo_root`, `runtime_root`, or `vault_root`.
- **Do** preserve existing, unrelated temporary work residing in `.temp/`.
- **Do Not** place disposable scratch in tracked delivery folders, `artifacts/`, or `plugin_root`.

## Canonical Roots & Plugin Configuration (`NyssaAI.Configuration`)

- **Do** keep `plugin_root` strictly read-only; never write user configuration, mutable runtime state, or `.temp/` scratch inside `plugin_root`.
- **Do** resolve `NyssaAI.Configuration` settings and namespaces via `.nyssa-ai/` in order **`user_home` (`~/.nyssa-ai/<plugin>/`) $\rightarrow$ `repo_root` (`<repo_root>/.nyssa-ai/<plugin>/`)**.
- **Do** resolve `runtime_root` for mutable operational state in order: `--runtime-root` $\rightarrow$ `NYSSA_RUNTIME_ROOT` $\rightarrow$ agent persona `cwd` containing `SOUL.md` + `IDENTITY.md` $\rightarrow$ `~/.nyssa-ai/<plugin>/runtime/` (`user_home`) or `<repo_root>/.nyssa-ai/<plugin>/runtime/` (`repo_root`).
- **Do** resolve `user_home` and `repo_root` independently using exact paths; do not recursively scan `user_home` or treat nested subdirectories as new roots.
- **Do** apply explicit task instructions as runtime overrides without persisting them to saved configuration.
- **Do Not** read or write retired legacy `.nyssaai/` or `.nyssa/` configuration directories.
- **Do Not** place `.nyssa-ai/` configuration, secrets, or machine-local runtime state inside `vault_root` (only `vault_root/.temp/` is permitted for scratch).
- **Do Not** include private configuration, credentials, or scratch files in published packages.

## PARA Vault & Work-Record Basics

- **Do** apply PARA guidelines exclusively within a recognized `vault_root`; follow local conventions before catalog defaults.
- **Do** assign each item in `vault_root` exactly one current working home (`PARA Category`: `1-projects/`, `2-areas/`, `3-resources/`, `4-archives/`) based strictly on current operational use.
- **Do** align `1-projects/` and `2-areas/daily-plans/` with `daily-tasks` structured work records (`RecordKind`: `project`, `milestone`, `task`, `blocker`, `daily-plan`) governed by `state` rather than `task-state`.
- **Do** use `para-vault` whenever filing `Inbox Capture` items, organizing vaults, reconciling notes, archiving projects, or importing `Source Record` payloads.
- **Do Not** classify PARA items by age, format, `document-maturity`, or `canonical` authority.
