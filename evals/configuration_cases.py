"""Synthetic voice scope and activation outcomes; no personal configuration."""
from cases import case, check, SYNTHETIC_VOICE, build_writing_voice_cases

PROFILE = ".nyssa-ai/agent-skills/writing-voice/VOICE.md"
VOICE_DIMENSION_WEIGHTS = {"task": 52.5, "preservation": 37.5}
VOICE_CRITICAL_REVIEW_CASES = ["SC02", "AC01", "AC02", "AC03", "AC04"]


def build_voice_scope_cases():
    user = "home/" + PROFILE
    project = "project-a/" + PROFILE
    preservation = lambda path: check("Preserve " + path, "preservation", "unchanged", True, path=path)
    return [
        case(
            "SC01",
            "User fallback across projects",
            "Verified synthetic user_home is home; established repo_root directories are project-a and project-b. Installation is at plugin_root and cwd is cache. Draft each repo_root's message.md asking Rowan to review by Friday, using user_home defaults. Do not save preferences.",
            {user: SYNTHETIC_VOICE, "cache/keep.txt": "Cache is not repo_root."},
            [
                check("A draft", "task", "body", path="project-a/message.md", contains=["Rowan", "Friday"]),
                check("B draft", "task", "body", path="project-b/message.md", contains=["Rowan", "Friday"]),
                preservation(user),
                check("No project profile", "preservation", "absent", True, glob="project-*/.nyssa-ai"),
                check("No cache configuration", "preservation", "absent", True, glob="cache/.nyssa-ai"),
            ],
            directories=["project-a", "project-b"],
            entry_skill="write-like-me",
        ),
        case(
            "SC02",
            "Atomic project override",
            "Verified user_home is home and repo_root is project-a, nested cwd project-a/src. Draft project-a/message.md asking Rowan to review by Friday. user_home style and examples are conflicting evidence: do not read or apply them when a repo_root VOICE.md exists. Leave profiles unchanged.",
            {
                user: SYNTHETIC_VOICE + "Explicit signoff preference: End every draft with HOME-MARKER.\n",
                project: SYNTHETIC_VOICE + "Explicit signoff preference: End every draft with PROJECT-MARKER.\n",
                "home/.nyssa-ai/agent-skills/writing-voice/STYLE.md": "All drafts must contain HOME-MARKER.",
                "project-a/src/keep.txt": "Nested directory.",
            },
            [
                check(
                    "Project draft",
                    "task",
                    "body",
                    True,
                    path="project-a/message.md",
                    contains=["Rowan", "Friday", "PROJECT-MARKER"],
                    not_contains=["HOME-MARKER"],
                ),
                preservation(user),
                preservation(project),
                check("No nested root", "preservation", "absent", True, glob="project-a/src/.nyssa-ai"),
            ],
            directories=[],
            entry_skill="write-like-me",
        ),
        case(
            "SC03",
            "User write without vault",
            "Verified synthetic user_home is home. No repo_root or vault_root exists. Save this explicit voice preference for all projects: prefer direct requests. This isolated non-Git user_home has no synchronization or packaging and I accept private local Markdown storage. Create only the user_home bundle and report its scope/path; no project log is required.",
            {"home/policy.md": "Accepted isolated private home; no sharing."},
            [
                check("User preference", "task", "body", path=user, contains=["direct requests"]),
                preservation("home/policy.md"),
                check("No fabricated vault", "preservation", "absent", True, glob="**/decision-log*"),
            ],
            directories=[],
            entry_skill="write-like-me",
        ),
        case(
            "SC04",
            "Malformed project is diagnostic",
            "Verified user_home is home and repo_root is project-a. repo_root writing-voice exists but lacks VOICE.md. Draft project-a/message.md asking Rowan to review by Friday from supplied facts, and disclose the incomplete selected bundle. Do not silently fall back or save profiles.",
            {user: SYNTHETIC_VOICE, "project-a/.nyssa-ai/agent-skills/writing-voice/STYLE.md": "Incomplete bundle."},
            [
                check("Useful draft", "task", "body", path="project-a/message.md", contains=["Rowan", "Friday"]),
                check("Diagnostic", "task", "response_nonempty", field="limitations"),
                preservation(user),
                check("No repair", "preservation", "absent", True, glob=project),
            ],
            directories=[],
            entry_skill="write-like-me",
        ),
        case(
            "SC05",
            "Retired legacy directory ignored",
            "Verified user_home is home; repo_root project-a has no voice bundle. Home contains only a retired .nyssaai directory, which is not a valid .nyssa-ai configuration root. Draft project-a/message.md asking Rowan to review by Friday from supplied facts, disclose that no .nyssa-ai profile was found, and leave all existing directories unchanged.",
            {"home/.nyssaai/agent-skills/writing-voice/VOICE.md": SYNTHETIC_VOICE},
            [
                check("Draft", "task", "body", path="project-a/message.md", contains=["Rowan", "Friday"]),
                check("Missing canonical profile disclosed", "task", "response_nonempty", field="limitations"),
                preservation("home/.nyssaai/agent-skills/writing-voice/VOICE.md"),
                check("No migration", "preservation", "absent", True, glob="home/.nyssa-ai"),
            ],
            directories=["project-a"],
            entry_skill="write-like-me",
        ),
    ]


def build_voice_activation_cases():
    profile = PROFILE
    return [
        case(
            "AC01",
            "Natural preference maintenance",
            "Save my writing preference for this repo_root: use direct requests. Isolated non-Git unshared workspace; private local storage accepted. Do not ask approval again.",
            {},
            [check("Preference persisted", "task", "body", path=profile, contains=["direct requests"])],
            directories=[],
            entry_skill="natural",
        ),
        case(
            "AC02",
            "Natural drafting is read only",
            "Write a message as me asking Rowan to review by Friday; save message.md. Do not update my preferences.",
            {profile: SYNTHETIC_VOICE},
            [
                check("Draft", "task", "body", path="message.md", contains=["Rowan", "Friday"]),
                check("Profile unchanged", "preservation", "unchanged", True, path=profile),
            ],
            directories=[],
            entry_skill="natural",
        ),
        case(
            "AC03",
            "Third party house style",
            "Edit publication.md only to correct the spelling of teh. This is third-party publication copy in its required house style, not my personal writing. Preserve its tone and capitalization.",
            {profile: SYNTHETIC_VOICE, "publication.md": "BEHOLD teh PUBLICATION!"},
            [
                check("House style retained", "task", "body", path="publication.md", contains=["BEHOLD the PUBLICATION!"]),
                check("Profile unchanged", "preservation", "unchanged", True, path=profile),
            ],
            directories=[],
            entry_skill="natural",
        ),
        case(
            "AC04",
            "Unrelated explanation",
            "Explain how rain forms in response.json. Do not create documents or change configuration.",
            {profile: SYNTHETIC_VOICE},
            [
                check("No file changes", "preservation", "no_changes", True),
                check("Explanation", "task", "response_pattern", field="summary", pattern=r"\S"),
            ],
            directories=[],
            entry_skill="natural",
        ),
    ]


def build_voice_cases():
    return build_writing_voice_cases() + build_voice_scope_cases() + build_voice_activation_cases()
