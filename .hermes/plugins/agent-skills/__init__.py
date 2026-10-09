"""Register the shared skills and startup foundation in Hermes Agent."""

from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent
SKILLS = PLUGIN_ROOT / "skills"
CORE = SKILLS / "manage-file-operations" / "core.md"
BEGIN = "<!-- agent-skills:file-management:begin -->"
END = "<!-- agent-skills:file-management:end -->"
SKILL_HINT = (
    "Use skill_view to load the relevant agent-skills workflow: "
    "manage-file-operations, file-para-content, maintain-vault-navigation, "
    "manage-vault-lifecycle, import-vault-source-records, or revise-vault-documents."
)


def foundation(session_info):
    """Use the project anchor when it already supplies the canonical core."""
    core = CORE.read_text(encoding="utf-8").strip()
    cwd_value = session_info.get("cwd")
    if not cwd_value:
        return core + "\n\n" + SKILL_HINT
    cwd = Path(cwd_value).resolve()
    directories = (cwd, *cwd.parents)
    project_root = next((directory for directory in directories if (directory / ".git").exists()), cwd)
    block = f"{BEGIN}\n{core}\n{END}"
    for directory in directories:
        anchor = directory / "AGENTS.md"
        if anchor.is_file() and block in anchor.read_text(encoding="utf-8-sig"):
            return "The project AGENTS.md supplies the file-management foundation.\n" + SKILL_HINT
        if directory == project_root:
            break
    return core + "\n\n" + SKILL_HINT


def register(ctx):
    ctx.register_system_prompt_section(
        "agent-skills.file-management", foundation, position="after_memory", max_chars=4000
    )
    for skill in sorted(SKILLS.iterdir()):
        entrypoint = skill / "SKILL.md"
        if skill.is_dir() and entrypoint.is_file():
            ctx.register_skill(skill.name, entrypoint)
