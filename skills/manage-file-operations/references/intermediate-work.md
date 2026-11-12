# Intermediate work details

> [!IMPORTANT] Scope Directive
> This reference defines single-root scratch conventions (`.temp/`) across `repo_root`, `runtime_root`, and `vault_root`, sync service exclusions (Git, Syncthing), and cleanup rules for disposable task work. It does NOT define general move mechanics (owned by `safe-operations.md`).

Each active root (`repo_root`, `runtime_root`, or `vault_root` — never read-only
`plugin_root`) uses a single root `.temp/` directory for intermediate output and
staged build bundles (`<repo_root>/.temp/dist/`). Create `.temp/` at that root
when needed if it does not exist; do not create `artifacts/` or nested sub-unit
`.temp/` trees. Keep scripts, exports, drafts, and other disposable work in a
task-specific subdirectory such as `.temp/reconciliation-check/`.

Exclude `.temp/` from Git and applicable sync services through supported
configuration accessible within the task's authorized root. When `repo_root` is
the active root, use `/.temp/` in its `.gitignore`. When a Syncthing folder root
(such as `vault_root`) is the active root, use `/.temp` in its root `.stignore`
(without a trailing slash). Preserve existing rules and verify that rule
ordering allows the exclusion to take effect. Ignore rules do not untrack files
already in Git; report those separately without silently removing them from the
index.

Syncthing does not sync `.stignore` itself; a verified local exclusion does not
establish exclusion on other devices. Report unsupported or inaccessible sync
settings and unverified devices. Do not expand ordinary file work into
remote-device configuration or claim exclusions that were not verified.

Keep retained deliverables in their intended permanent locations. Verify a
retained copy before removing its intermediate version. Clean up only
disposable files created for the current task; preserve unrelated `.temp/`
contents.
