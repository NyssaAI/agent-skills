# Intermediate work details

An AI working root, whether a project, folder, or other workspace, uses a
`.temp/` directory for intermediate output. Create it at that root when needed
if it does not exist. Keep scripts, exports, drafts, and other disposable work
in a task-specific subdirectory such as `.temp/reconciliation-check/`.

Exclude `.temp/` from Git and applicable sync services through supported
configuration accessible within the task's authorized workspace. When the Git
repository root is the working root, use `/.temp/` in its `.gitignore`. When the
Syncthing folder root is the working root, use `/.temp` in its root `.stignore`
(without a trailing slash). If the working root is nested, use the corresponding
path relative to each repository or synced folder root. Preserve existing rules
and verify that rule ordering allows the exclusion to take effect. Ignore rules
do not untrack files already in Git; report those separately without silently
removing them from the index.

Syncthing does not sync `.stignore` itself; a verified local exclusion does not
establish exclusion on other devices. Report unsupported or inaccessible sync
settings and unverified devices. Do not expand ordinary file work into
remote-device configuration or claim exclusions that were not verified.

Keep retained deliverables in their intended permanent locations. Verify a
retained copy before removing its intermediate version. Clean up only
disposable files created for the current task; preserve unrelated `.temp/`
contents.
