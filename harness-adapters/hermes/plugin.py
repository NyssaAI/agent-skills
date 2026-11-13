"""Register the shared skills and startup foundation in Hermes Agent (harness-adapter)."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import re
from typing import Any


_HERE = Path(__file__).resolve().parent
PLUGIN_ROOT = _HERE if (_HERE / "skills").is_dir() else _HERE.parents[1]
SKILLS = PLUGIN_ROOT / "skills"
CORE = SKILLS / "manage-file-operations" / "core.md"
BEGIN = "<!-- agent-skills:file-management:begin -->"
END = "<!-- agent-skills:file-management:end -->"
VOICE = PLUGIN_ROOT / "rules" / "writing-voice.md"
VOICE_BEGIN = "<!-- agent-skills:writing-voice:begin -->"
VOICE_END = "<!-- agent-skills:writing-voice:end -->"
SKILL_HINT = (
    "Use skill_view to load the relevant agent-skills workflow: "
    "manage-file-operations, para-vault, or write-like-me."
)


def _strip_frontmatter(text: str) -> str:
    match = re.match(r"\A---\r?\n.*?\r?\n---\r?\n*", text, re.S)
    return text[match.end():].strip() if match else text.strip()


def foundation(session_info: Mapping[str, Any]) -> str:
    """Use the repo_root anchor when it already supplies the canonical core."""
    core = _strip_frontmatter(CORE.read_text(encoding="utf-8"))
    voice = _strip_frontmatter(VOICE.read_text(encoding="utf-8"))
    cwd_value = session_info.get("cwd") if isinstance(session_info, Mapping) else None
    if not cwd_value:
        return core + "\n\n" + voice + "\n\n" + SKILL_HINT
    cwd = Path(str(cwd_value)).resolve()
    directories = (cwd, *cwd.parents)
    repo_root = next((directory for directory in directories if (directory / ".git").exists()), cwd)
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
        if directory == repo_root:
            break
    sections = ["The repository AGENTS.md supplies the file-management foundation." if core_supplied else core]
    if not voice_supplied:
        sections.append(voice)
    sections.append(SKILL_HINT)
    return "\n\n".join(sections)


def register(ctx: Any) -> None:
    """Hermes Agent harness-adapter entry point."""
    for skill in sorted((PLUGIN_ROOT / "skills").glob("*/SKILL.md")):
        ctx.register_skill(skill.parent.name, skill)
    ctx.register_system_prompt_section(
        "agent-skills.foundation",
        foundation,
        position="after_memory",
        max_chars=4000,
    )
