"""Register the shared skills and startup foundation in Hermes Agent."""

from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent
SKILLS = PLUGIN_ROOT / "skills"
CORE = SKILLS / "manage-file-operations" / "core.md"
BEGIN = "<!-- agent-skills:file-management:begin -->"
END = "<!-- agent-skills:file-management:end -->"
VOICE = PLUGIN_ROOT / "rules" / "writing-voice.md"
VOICE_BEGIN = "<!-- agent-skills:writing-voice:begin -->"
VOICE_END = "<!-- agent-skills:writing-voice:end -->"
SKILL_HINT = (
    "Use skill_view to load the relevant agent-skills workflow: "
    "manage-file-operations, file-para-content, maintain-vault-navigation, "
    "manage-vault-lifecycle, import-vault-source-records, revise-vault-documents, "
    "maintain-writing-voice, or write-in-user-voice."
)


def foundation(session_info):
    """Use the project anchor when it already supplies the canonical core."""
    core = CORE.read_text(encoding="utf-8").strip()
    voice = VOICE.read_text(encoding="utf-8").strip()
    cwd_value = session_info.get("cwd")
    if not cwd_value:
        return core + "\n\n" + voice + "\n\n" + SKILL_HINT
    cwd = Path(cwd_value).resolve()
    directories = (cwd, *cwd.parents)
    project_root = next((directory for directory in directories if (directory / ".git").exists()), cwd)
    block = f"{BEGIN}\n{core}\n{END}"
    voice_block = f"{VOICE_BEGIN}\n{voice}\n{VOICE_END}"
    core_supplied = False
    voice_supplied = False
    for directory in directories:
        anchor = directory / "AGENTS.md"
        if anchor.is_file():
            text = anchor.read_text(encoding="utf-8-sig")
            core_supplied = core_supplied or block in text
            voice_supplied = voice_supplied or voice_block in text
        if directory == project_root:
            break
    sections = ["The project AGENTS.md supplies the file-management foundation." if core_supplied else core]
    if not voice_supplied:
        sections.append(voice)
    sections.append(SKILL_HINT)
    return "\n\n".join(sections)


def register(ctx):
    ctx.register_system_prompt_section(
        "agent-skills.file-management", foundation, position="after_memory", max_chars=6000
    )
    for skill in sorted(SKILLS.iterdir()):
        entrypoint = skill / "SKILL.md"
        if skill.is_dir() and entrypoint.is_file():
            ctx.register_skill(skill.name, entrypoint)
