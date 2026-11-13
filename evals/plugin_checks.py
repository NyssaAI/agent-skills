"""Plugin checks — validate skill packaging, frontmatter, harness-adapters, and local reference reachability.
validate_plugin(repository)
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import runpy
import subprocess

try:
    import yaml
except ImportError:  # pragma: no cover - stdlib fallback when PyYAML is absent
    yaml = None


FORBIDDEN_REPO_TREES = (".agents", ".hermes", "artifacts", "adapters", "plugins")
EXCLUDED_PACKAGE_PARTS = (".nyssa-ai", ".nyssaai", ".nyssa", ".temp")
IGNORED_SCAN_PARTS = frozenset({
    ".git",
    ".temp",
    ".agents",
    ".hermes",
    ".worktrees",
    ".obsidian",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    "artifacts",
    ".nyssa-ai",
})

PERMITTED_ROOT_DIRECTORIES = frozenset({
    # Canonical plugin source & repository directories:
    "skills",
    "rules",
    "hooks",
    "harness-adapters",
    "scripts",
    "docs",
    "evals",
    "test",
    "src",
    "commands",
    ".github",
    ".temp",
    ".nyssa-ai",
    # Tracked root harness-adapter manifest directories:
    ".claude-plugin",
    ".codex-plugin",
    ".cursor-plugin",
    ".tessl-plugin",
    # Standard VCS, cache & IDE directories:
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    ".worktrees",
    ".vscode",
    ".idea",
})

PERMITTED_ROOT_FILES = frozenset({
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "GEMINI.md",
    "LICENSE",
    "README.md",
    "gemini-extension.json",
    "hooks.json",
    "plugin.json",
    "tessl.json",
})

PERMITTED_SCRIPTS_ENTRIES = frozenset({"assemble.py", "validate.py", "__pycache__"})

ALLOWED_DOCS_FILES = frozenset({"GLOSSARY.md", "product.md", "features.md", "tech-stack.md"})
ALLOWED_DOCS_DIRECTORIES = frozenset({"concepts", "features", "plans", "learnings", "specs", "code-map"})

PERMITTED_EVALS_DIRECTORIES = frozenset({"waza", "tessl", "scenarios", "verifiers", "reports", "__pycache__"})

PERMITTED_TEST_SUBDIRECTORIES = frozenset({"unit", "use_case", "e2e", "__pycache__"})
PERMITTED_TEST_ROOT_FILES = frozenset({"__init__.py", "conftest.py"})
TEST_FILE_PATTERNS = (
    re.compile(r"^test_.*\.py$"),
    re.compile(r"^.*_test\.py$"),
    re.compile(r"^.*\.test\.[jt]sx?$"),
    re.compile(r"^.*_test\.go$"),
    re.compile(r"^.*Tests\.cs$"),
)

SCOPE_DIRECTIVE = "> [!IMPORTANT] Scope Directive"
VERIFICATION_HEADING_RE = re.compile(r"^##\s+(?:\d+\.\s+)?Verification\b", re.M)

LOCAL_PATH_LEAK_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("/srv/repos/NyssaAI/", re.compile(r"/srv/repos/NyssaAI/")),
    ("/root/.gemini/antigravity-cli/brain/", re.compile(r"/root/\.gemini/antigravity-cli/brain/")),
    ("C:\\Users\\", re.compile(r"[Cc]:[\\/][Uu]sers[\\/]")),
)


class _FallbackYAMLError(ValueError):
    """Raised when the stdlib YAML fallback encounters invalid syntax."""


YAML_ERRORS: tuple[type[BaseException], ...] = (
    (yaml.YAMLError, _FallbackYAMLError) if yaml is not None else (_FallbackYAMLError,)
)


def _strip_yaml_comment(line: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    for idx, ch in enumerate(line):
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_double:
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            if idx == 0 or line[idx - 1].isspace():
                return line[:idx].rstrip()
    return line.rstrip()


def _parse_yaml_scalar(token: str):
    val = token.strip()
    if val == "":
        return None
    if val == "{}":
        return {}
    if val == "[]":
        return []
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [_parse_yaml_scalar(part) for part in inner.split(",")]
    if len(val) >= 2 and val[0] == '"' and val[-1] == '"':
        body = val[1:-1]
        return (
            body.replace('\\"', '"')
            .replace("\\n", "\n")
            .replace("\\t", "\t")
            .replace("\\\\", "\\")
        )
    if len(val) >= 2 and val[0] == "'" and val[-1] == "'":
        return val[1:-1].replace("''", "'")
    low = val.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "~"):
        return None
    if re.fullmatch(r"-?\d+", val):
        return int(val)
    if re.fullmatch(r"-?\d+\.\d+", val):
        return float(val)
    return val


def _parse_yaml_fallback(text: str):
    if "\t" in text:
        raise _FallbackYAMLError("Tab indentation is not valid in YAML")
    raw_lines = text.splitlines()
    lines: list[tuple[int, str, str]] = []
    for raw in raw_lines:
        cleaned = _strip_yaml_comment(raw)
        if not cleaned.strip():
            lines.append((-1, "", raw))
        else:
            indent = len(raw) - len(raw.lstrip(" "))
            lines.append((indent, cleaned.lstrip(" "), raw))

    def next_non_empty(idx: int) -> int:
        while idx < len(lines) and lines[idx][0] == -1:
            idx += 1
        return idx

    def collect_block_scalar(start_idx: int, parent_indent: int, folded: bool) -> tuple[str, int]:
        collected: list[str] = []
        block_indent: int | None = None
        idx = start_idx
        while idx < len(lines):
            ind, _, raw = lines[idx]
            if ind == -1:
                if block_indent is not None:
                    collected.append("")
                idx += 1
                continue
            raw_ind = len(raw) - len(raw.lstrip(" "))
            if raw_ind <= parent_indent:
                break
            if block_indent is None:
                block_indent = raw_ind
            collected.append(raw[min(block_indent, len(raw)):])
            idx += 1
        while collected and collected[-1] == "":
            collected.pop()
        if not folded:
            return "\n".join(collected), idx
        paragraphs: list[str] = []
        current_para: list[str] = []
        for ln in collected:
            if ln == "":
                if current_para:
                    paragraphs.append(" ".join(current_para))
                    current_para = []
                paragraphs.append("")
            else:
                current_para.append(ln.strip())
        if current_para:
            paragraphs.append(" ".join(current_para))
        return "\n".join(paragraphs), idx

    def parse_block(idx: int, min_indent: int):
        idx = next_non_empty(idx)
        if idx >= len(lines) or lines[idx][0] < min_indent:
            return None, idx
        base_indent = lines[idx][0]
        if lines[idx][1] == "-" or lines[idx][1].startswith("- "):
            items = []
            while True:
                idx = next_non_empty(idx)
                if idx >= len(lines) or lines[idx][0] != base_indent:
                    break
                content = lines[idx][1]
                if not (content == "-" or content.startswith("- ")):
                    break
                rest = content[1:].lstrip(" ")
                if not rest:
                    item, idx = parse_block(idx + 1, base_indent + 1)
                    items.append(item)
                elif ":" in rest and not rest.startswith(('"', "'")):
                    k_part, _, v_part = rest.partition(":")
                    key_name = _parse_yaml_scalar(k_part)
                    v_str = v_part.strip()
                    obj: dict = {}
                    idx += 1
                    if v_str in (">", ">-", "|", "|-"):
                        val, idx = collect_block_scalar(idx, base_indent, v_str.startswith(">"))
                        obj[key_name] = val
                    elif v_str == "":
                        val, idx = parse_block(idx, base_indent + 1)
                        obj[key_name] = val
                    else:
                        obj[key_name] = _parse_yaml_scalar(v_str)
                    nxt = next_non_empty(idx)
                    if nxt < len(lines) and lines[nxt][0] > base_indent:
                        extra, idx = parse_mapping(nxt, lines[nxt][0])
                        obj.update(extra)
                    items.append(obj)
                else:
                    items.append(_parse_yaml_scalar(rest))
                    idx += 1
            return items, idx
        return parse_mapping(idx, base_indent)

    def parse_mapping(idx: int, base_indent: int) -> tuple[dict, int]:
        mapping: dict = {}
        while True:
            idx = next_non_empty(idx)
            if idx >= len(lines) or lines[idx][0] != base_indent:
                break
            content = lines[idx][1]
            if content == "-" or content.startswith("- ") or ":" not in content:
                break
            k_part, _, v_part = content.partition(":")
            key_name = _parse_yaml_scalar(k_part)
            v_str = v_part.strip()
            idx += 1
            if v_str in (">", ">-", "|", "|-"):
                val, idx = collect_block_scalar(idx, base_indent, v_str.startswith(">"))
                mapping[key_name] = val
            elif v_str == "":
                val, idx = parse_block(idx, base_indent + 1)
                mapping[key_name] = val
            else:
                mapping[key_name] = _parse_yaml_scalar(v_str)
        return mapping, idx

    parsed, stop_idx = parse_block(0, 0)
    if next_non_empty(stop_idx) < len(lines):
        raise _FallbackYAMLError("Trailing unparsed YAML content")
    return parsed


def _load_yaml_text(text: str):
    if yaml is not None:
        return yaml.safe_load(text)
    return _parse_yaml_fallback(text)


def _is_docs_gitignored(repository: Path) -> bool:
    gitignore_path = repository / ".gitignore"
    if gitignore_path.is_file():
        ignored = False
        for raw_line in gitignore_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("!"):
                negated = line[1:].strip()
                if re.fullmatch(r"/?docs(?:/\*\*|/\*|/)?", negated):
                    ignored = False
                continue
            if re.fullmatch(r"/?docs(?:/\*\*|/\*|/)?", line):
                ignored = True
        if ignored:
            return True
    if (repository / ".git").exists():
        try:
            res = subprocess.run(
                ["git", "check-ignore", "-q", "docs"],
                cwd=repository,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            return res.returncode == 0
        except OSError:
            return False
    return False


def _load_assemble_module(repository: Path):
    script = repository / "scripts" / "assemble.py"
    if not script.is_file():
        return None
    spec = importlib.util.spec_from_file_location("agent_skills_assemble", script)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _parse_rule_frontmatter(content: str) -> tuple[dict | None, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n*", content, re.S)
    if not match:
        return None, content.strip()
    metadata = _load_yaml_text(match.group(1))
    return (metadata if isinstance(metadata, dict) else None), content[match.end():].strip()


def validate_evals_directory(repository: Path, skill_names: set[str]) -> tuple[int, list[str]]:
    """Validate repository-level evals metadata and Waza single-TestCase suites when evals/ is present."""
    findings: list[str] = []
    checks = 0
    evals_dir = repository / "evals"
    if not evals_dir.is_dir():
        return checks, findings

    for item in sorted(evals_dir.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            checks += 1
            if item.name not in PERMITTED_EVALS_DIRECTORIES:
                findings.append(f"Disallowed directory in evals/: evals/{item.name}/")

    checks += 1
    if not (evals_dir / "README.md").is_file():
        findings.append("Missing evaluation documentation: evals/README.md")

    checks += 1
    latest_path = evals_dir / "LATEST.md"
    if not latest_path.is_file():
        findings.append("Missing generated evaluation summary: evals/LATEST.md")
    else:
        checks += 1
        latest_text = latest_path.read_text(encoding="utf-8")
        if "../.temp/" in latest_text:
            findings.append("evals/LATEST.md contains dead ../.temp/ links")

    checks += 1
    matrix_path = evals_dir / "matrix.json"
    if not matrix_path.is_file():
        findings.append("Missing evaluation coverage matrix: evals/matrix.json")
    else:
        try:
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            if not isinstance(matrix, dict):
                findings.append("evals/matrix.json root must be an object")
            else:
                if matrix.get("schema") != 1:
                    findings.append("evals/matrix.json schema must equal 1")
                if not isinstance(matrix.get("suite_revision"), str) or not matrix["suite_revision"].strip():
                    findings.append("evals/matrix.json missing non-empty suite_revision")
                rows = matrix.get("rows")
                if not isinstance(rows, list) or not rows:
                    findings.append("evals/matrix.json rows must be a non-empty list")
                else:
                    seen_keys: set[tuple[str, str, str, str]] = set()
                    for idx, row in enumerate(rows):
                        if not isinstance(row, dict):
                            findings.append(f"evals/matrix.json row {idx} must be an object")
                            continue
                        row_tuple_parts = []
                        missing_fields = []
                        for field in ("suite", "harness", "platform", "config"):
                            val = row.get(field)
                            if not isinstance(val, str) or not val.strip():
                                missing_fields.append(field)
                            else:
                                row_tuple_parts.append(val)
                        if missing_fields:
                            findings.append(f"evals/matrix.json row {idx} missing fields: {missing_fields}")
                            continue
                        row_key = (
                            row_tuple_parts[0],
                            row_tuple_parts[1],
                            row_tuple_parts[2],
                            row_tuple_parts[3],
                        )
                        if row_key in seen_keys:
                            findings.append(f"evals/matrix.json duplicate row key: {row_key}")
                        seen_keys.add(row_key)
        except (OSError, ValueError) as error:
            findings.append(f"evals/matrix.json: {error}")

    for skill_name in sorted(skill_names):
        checks += 1
        eval_yaml = evals_dir / "waza" / "skills" / skill_name / "eval.yaml"
        if not eval_yaml.is_file():
            findings.append(f"Missing Waza eval spec: evals/waza/skills/{skill_name}/eval.yaml")
            continue
        try:
            spec = _load_yaml_text(eval_yaml.read_text(encoding="utf-8-sig"))
        except YAML_ERRORS as error:
            findings.append(f"{eval_yaml.relative_to(repository)}: {error}")
            continue
        if not isinstance(spec, dict):
            findings.append(f"{eval_yaml.relative_to(repository)}: eval spec must be a YAML mapping")
            continue
        if spec.get("skill") != skill_name:
            findings.append(f"{eval_yaml.relative_to(repository)}: skill field must equal {skill_name!r}")
        task_patterns = spec.get("tasks")
        if not isinstance(task_patterns, list) or not task_patterns or not all(isinstance(p, str) and p.strip() for p in task_patterns):
            findings.append(f"{eval_yaml.relative_to(repository)}: tasks must be a non-empty list of glob strings")
            continue
        matched_tasks: list[Path] = []
        for pattern in task_patterns:
            matched_tasks.extend(sorted(p for p in eval_yaml.parent.glob(pattern) if p.is_file()))
        matched_tasks = sorted(dict.fromkeys(matched_tasks))
        checks += 1
        if not matched_tasks:
            findings.append(f"{eval_yaml.relative_to(repository)}: tasks patterns resolved 0 task files")
            continue

        seen_task_ids: set[str] = set()
        for task_file in matched_tasks:
            checks += 1
            rel_task = task_file.relative_to(repository)
            try:
                task_doc = _load_yaml_text(task_file.read_text(encoding="utf-8-sig"))
            except YAML_ERRORS as error:
                findings.append(f"{rel_task}: {error}")
                continue
            if not isinstance(task_doc, dict):
                findings.append(f"{rel_task}: Waza task file must be a single TestCase mapping (dict), not {type(task_doc).__name__}")
                continue
            task_id = task_doc.get("id")
            if not isinstance(task_id, str) or not task_id.strip():
                findings.append(f"{rel_task}: missing non-empty TestCase id")
            elif task_id in seen_task_ids:
                findings.append(f"{rel_task}: duplicate TestCase id {task_id!r}")
            else:
                seen_task_ids.add(task_id)

            task_name = task_doc.get("name")
            if not isinstance(task_name, str) or not task_name.strip():
                findings.append(f"{rel_task}: missing non-empty TestCase name")

            inputs = task_doc.get("inputs")
            prompt = inputs.get("prompt") if isinstance(inputs, dict) else None
            if not isinstance(prompt, str) or not prompt.strip():
                findings.append(f"{rel_task}: missing non-empty inputs.prompt")

            graders = task_doc.get("graders")
            if not isinstance(graders, list) or not graders:
                findings.append(f"{rel_task}: missing non-empty graders list")
                continue

            trigger_graders = [g for g in graders if isinstance(g, dict) and g.get("type") == "trigger"]
            if not trigger_graders:
                findings.append(f"{rel_task}: requires at least one grader with type 'trigger'")
                continue
            for grader in trigger_graders:
                config = grader.get("config")
                if not isinstance(config, dict):
                    findings.append(f"{rel_task}: trigger grader missing config mapping")
                    continue
                mode = config.get("mode")
                if mode not in {"positive", "negative"}:
                    findings.append(f"{rel_task}: trigger grader config.mode must be 'positive' or 'negative'")
                skill_path = config.get("skill_path")
                if not isinstance(skill_path, str) or not skill_path.strip():
                    findings.append(f"{rel_task}: trigger grader missing config.skill_path")
                elif not (repository / skill_path).is_file():
                    findings.append(f"{rel_task}: trigger grader skill_path does not exist: {skill_path}")

    return checks, findings


def validate_plugin(repository: Path) -> dict:
    """Check the local catalog contract without claiming runtime installation compatibility."""
    findings: list[str] = []
    checks = 0

    for forbidden in FORBIDDEN_REPO_TREES:
        checks += 1
        if (repository / forbidden).exists():
            findings.append(f"Forbidden tree in repo_root: {forbidden}/")

    if repository.is_dir():
        for entry in sorted(repository.iterdir()):
            checks += 1
            if entry.is_dir():
                if entry.name in FORBIDDEN_REPO_TREES:
                    continue
                if entry.name not in PERMITTED_ROOT_DIRECTORIES:
                    findings.append(f"Unexpected top-level directory in repo_root: {entry.name}/")
            elif entry.is_file():
                if entry.name not in PERMITTED_ROOT_FILES:
                    findings.append(f"Unexpected loose root file in repo_root: {entry.name}")

    scripts_dir = repository / "scripts"
    if scripts_dir.is_dir():
        for entry in sorted(scripts_dir.iterdir()):
            checks += 1
            if entry.name not in PERMITTED_SCRIPTS_ENTRIES:
                findings.append(f"Unexpected entry in scripts/: scripts/{entry.name}")

    checks += 1
    gitattributes_path = repository / ".gitattributes"
    if not gitattributes_path.is_file():
        findings.append("Missing .gitattributes with LF line-ending normalization (eol=lf)")
    elif "eol=lf" not in gitattributes_path.read_text(encoding="utf-8", errors="ignore"):
        findings.append(".gitattributes must enforce LF line endings (eol=lf)")

    checks += 1
    if (repository / "harness-adapters" / "codex").exists():
        findings.append("Retired Codex openai.yaml directory present: harness-adapters/codex/")

    docs_dir = repository / "docs"
    checks += 1
    if _is_docs_gitignored(repository):
        findings.append("docs/ directory must not be gitignored")

    checks += 1
    if not (docs_dir / "GLOSSARY.md").is_file():
        findings.append("Missing authoritative Ubiquitous Language glossary: docs/GLOSSARY.md")

    if docs_dir.is_dir():
        for item in sorted(docs_dir.iterdir()):
            checks += 1
            if item.is_file() and item.name not in ALLOWED_DOCS_FILES:
                findings.append(
                    f"Disallowed file in docs/: docs/{item.name} "
                    f"(allowed: {', '.join(sorted(ALLOWED_DOCS_FILES))})"
                )
            elif item.is_dir() and item.name not in ALLOWED_DOCS_DIRECTORIES:
                findings.append(
                    f"Disallowed directory in docs/: docs/{item.name}/ "
                    f"(allowed: {', '.join(sorted(ALLOWED_DOCS_DIRECTORIES))})"
                )
        specs_dir = docs_dir / "specs"
        if specs_dir.is_dir():
            for md_spec in sorted(specs_dir.rglob("*.md")):
                checks += 1
                findings.append(
                    f"Disallowed prose markdown in docs/specs/: {md_spec.relative_to(repository).as_posix()}"
                )

    if repository.is_dir():
        skip_top = IGNORED_SCAN_PARTS | {"test", "evals", "docs"}
        for dirpath, dirnames, filenames in os.walk(repository):
            rel_dir = Path(dirpath).relative_to(repository)
            if rel_dir == Path("."):
                dirnames[:] = sorted(d for d in dirnames if d not in skip_top)
            else:
                dirnames[:] = sorted(
                    d for d in dirnames if d not in IGNORED_SCAN_PARTS and d != "examples"
                )
            for fname in sorted(filenames):
                if any(pattern.match(fname) for pattern in TEST_FILE_PATTERNS):
                    checks += 1
                    rel_file = (rel_dir / fname).as_posix()
                    findings.append(
                        f"Co-mingled test file outside test/: {rel_file}; "
                        "tests must live under test/unit/, test/use_case/, or test/e2e/"
                    )

    test_dir = repository / "test"
    if test_dir.is_dir():
        for item in sorted(test_dir.iterdir()):
            checks += 1
            if item.is_file() and (
                any(pattern.match(item.name) for pattern in TEST_FILE_PATTERNS)
                or item.name not in PERMITTED_TEST_ROOT_FILES
            ):
                findings.append(
                    f"Loose file in test/ root: test/{item.name}; "
                    "tests must live under test/unit/, test/use_case/, or test/e2e/"
                )
            elif item.is_dir() and not item.name.startswith(".") and item.name not in PERMITTED_TEST_SUBDIRECTORIES:
                findings.append(
                    f"Non-canonical test subdirectory: test/{item.name}/; "
                    "use test/unit/, test/use_case/, or test/e2e/"
                )

    checks += 1
    license_path = repository / "LICENSE"
    if not license_path.is_file():
        findings.append("Missing repository license file: LICENSE")
    else:
        license_text = license_path.read_text(encoding="utf-8")
        if (
            "Apache License" not in license_text
            or "Version 2.0, January 2004" not in license_text
            or "Copyright 2026 NyssaAI" not in license_text
            or "MIT License" in license_text
        ):
            findings.append("LICENSE must contain the canonical NyssaAI Apache License 2.0 text")

    checks += 1
    changelog_path = repository / "CHANGELOG.md"
    if not changelog_path.is_file():
        findings.append("Missing tracked release history: CHANGELOG.md")
    else:
        changelog_text = changelog_path.read_text(encoding="utf-8")
        if not changelog_text.startswith("# Changelog\n") or "## Unreleased" not in changelog_text:
            findings.append("CHANGELOG.md must start with '# Changelog' and include '## Unreleased'")

    skills = sorted((repository / "skills").glob("*/SKILL.md"))
    skill_names = {path.parent.name for path in skills}
    checks += 1
    expected_skills = {"manage-file-operations", "para-vault", "write-like-me"}
    if not expected_skills.issubset(skill_names):
        missing = sorted(expected_skills - skill_names)
        findings.append(f"Missing canonical skills: {missing}")
    if not skills:
        findings.append("No skill entrypoints found")

    for path in skills:
        checks += 1
        if (path.parent / "agents").exists():
            findings.append(
                f"{path.parent.relative_to(repository)}/agents: retired openai.yaml / agents/ directory is not permitted"
            )
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            findings.append(f"{path.relative_to(repository)}: BOM prevents strict frontmatter discovery")
        content = raw.decode("utf-8-sig")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---", content, re.S)
        if not match:
            findings.append(f"{path.relative_to(repository)}: missing frontmatter")
            continue
        try:
            metadata = _load_yaml_text(match.group(1))
            if not isinstance(metadata, dict) or metadata.get("name") != path.parent.name:
                findings.append(f"{path.relative_to(repository)}: name does not match folder")
            description = metadata.get("description", "") if isinstance(metadata, dict) else ""
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                findings.append(f"{path.relative_to(repository)}: invalid description")
            if isinstance(metadata, dict) and isinstance(metadata.get("metadata"), dict) and "version" in metadata["metadata"]:
                findings.append(
                    f"{path.relative_to(repository)}: duplicate metadata.version is not permitted; plugin.json owns version"
                )
        except YAML_ERRORS as error:
            findings.append(f"{path.relative_to(repository)}: {error}")

    for scope_glob in ("skills/*/SKILL.md", "skills/*/workflows/*.md", "skills/*/references/*.md", "rules/*.md"):
        for path in sorted(repository.glob(scope_glob)):
            if not path.is_file():
                continue
            checks += 1
            rel_path = path.relative_to(repository).as_posix()
            content = path.read_text(encoding="utf-8-sig")
            if SCOPE_DIRECTIVE not in content:
                findings.append(f"{rel_path}: missing '{SCOPE_DIRECTIVE}'")
            if (path.name == "SKILL.md" or path.parent.name == "workflows") and not VERIFICATION_HEADING_RE.search(content):
                findings.append(f"{rel_path}: missing '## Verification' section")

    for path in (repository / "skills").rglob("*.md"):
        content = path.read_text(encoding="utf-8-sig")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if "://" in target:
                continue
            checks += 1
            filename, _, anchor = target.partition("#")
            if Path(filename).is_absolute() or ":" in filename:
                findings.append(f"{path.relative_to(repository)}: non-relative internal link {target}")
                continue
            destination = (path.parent / filename).resolve() if filename else path
            try:
                destination.relative_to(repository.resolve())
            except ValueError:
                findings.append(f"{path.relative_to(repository)}: link escapes catalog {target}")
                continue
            if not destination.exists():
                findings.append(f"{path.relative_to(repository)}: missing target {target}")
            elif anchor and destination.is_file():
                headings = re.findall(r"^#{1,6}\s+(.+)$", destination.read_text(encoding="utf-8-sig"), re.M)
                anchors = {re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-") for heading in headings}
                if anchor not in anchors:
                    findings.append(f"{path.relative_to(repository)}: missing anchor {target}")

    for yaml_root in ("skills", "harness-adapters"):
        base = repository / yaml_root
        if not base.exists():
            continue
        for path in base.rglob("*.yaml"):
            checks += 1
            try:
                _load_yaml_text(path.read_text(encoding="utf-8-sig"))
            except YAML_ERRORS as error:
                findings.append(f"{path.relative_to(repository)}: {error}")

    checks += 1
    hermes_adapter = repository / "harness-adapters" / "hermes" / "plugin.py"
    if not hermes_adapter.is_file():
        findings.append("Missing Hermes harness-adapter: harness-adapters/hermes/plugin.py")
    else:
        try:
            hermes_ns = runpy.run_path(str(hermes_adapter))
            foundation_fn = hermes_ns.get("foundation")
            register_fn = hermes_ns.get("register")
            if not callable(foundation_fn) or not callable(register_fn):
                findings.append("Hermes harness-adapter must expose callable foundation and register")
            else:
                rendered_foundation = foundation_fn({})
                if len(rendered_foundation) > 4000:
                    findings.append(f"Hermes foundation exceeds 4000 chars ({len(rendered_foundation)})")

                registered_skills: list[tuple[str, Path]] = []
                registered_sections: list[tuple[str, object, str, int]] = []

                class _ProbeContext:
                    def register_skill(self, name: str, path: Path) -> None:
                        registered_skills.append((name, Path(path)))

                    def register_system_prompt_section(
                        self, section_id: str, content: object, *, position: str = "after_memory", max_chars: int = 4000
                    ) -> None:
                        registered_sections.append((section_id, content, position, max_chars))

                register_fn(_ProbeContext())
                if {name for name, _ in registered_skills} != skill_names:
                    findings.append("Hermes register(ctx) did not register all canonical skills")
                if len(registered_sections) != 1 or registered_sections[0][:1] != ("agent-skills.foundation",) or registered_sections[0][2:] != ("after_memory", 4000):
                    findings.append("Hermes register(ctx) did not register agent-skills.foundation section cleanly")
        except Exception as error:  # noqa: BLE001
            findings.append(f"Hermes harness-adapter probe failed: {error}")

    root_identity = None
    manifest_files = [
        "plugin.json",
        "gemini-extension.json",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        ".cursor-plugin/plugin.json",
        ".tessl-plugin/plugin.json",
    ]
    for filename in manifest_files:
        checks += 1
        try:
            manifest = json.loads((repository / filename).read_text(encoding="utf-8-sig"))
            if not isinstance(manifest, dict):
                raise ValueError("manifest root must be an object")
            if filename == "plugin.json":
                root_identity = manifest
                if manifest.get("license") != "Apache-2.0":
                    findings.append("plugin.json license must equal 'Apache-2.0'")
                for required_field in ("author", "homepage", "repository"):
                    if not manifest.get(required_field):
                        findings.append(f"plugin.json missing non-empty {required_field}")
                keywords = manifest.get("keywords")
                if not isinstance(keywords, list) or not keywords or not all(isinstance(k, str) and k.strip() for k in keywords):
                    findings.append("plugin.json keywords must be a non-empty list of strings")
            elif root_identity is not None:
                expected_name = (
                    f"nyssa-ai/{root_identity.get('name')}"
                    if filename == ".tessl-plugin/plugin.json"
                    else root_identity.get("name")
                )
                if manifest.get("name") != expected_name:
                    findings.append(f"{filename} name differs from root plugin.json")
                if manifest.get("version") != root_identity.get("version"):
                    findings.append(f"{filename} version differs from root plugin.json")
                if manifest.get("description") != root_identity.get("description"):
                    findings.append(f"{filename} description differs from root plugin.json")
            if filename == "gemini-extension.json" and set(manifest.keys()) != {"name", "version", "description"}:
                findings.append("gemini-extension.json must contain only name, version, and description")
            if filename == ".codex-plugin/plugin.json" and not (repository / manifest["skills"]).is_dir():
                findings.append("Codex skills path does not exist")
            if filename == ".tessl-plugin/plugin.json":
                if not (repository / manifest["skills"]).is_dir():
                    findings.append("Tessl skills path does not exist")
                if not (repository / manifest["rules"]).is_dir():
                    findings.append("Tessl rules path does not exist")
            if filename in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json") and root_identity is not None:
                for field in ("author", "homepage", "repository", "license", "keywords"):
                    if manifest.get(field) != root_identity.get(field):
                        findings.append(f"{filename} {field} differs from root plugin.json")
        except (OSError, ValueError, KeyError, TypeError) as error:
            findings.append(f"{filename}: {error}")

    checks += 1
    try:
        core = (repository / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
        file_meta, file_body = _parse_rule_frontmatter(
            (repository / "rules/file-management.md").read_text(encoding="utf-8")
        )
        if not file_meta or file_meta.get("trigger") != "always_on" or not file_meta.get("description"):
            findings.append("rules/file-management.md lacks valid always_on trigger frontmatter")
        if file_body != core:
            findings.append("rules/file-management.md differs from canonical core.md")
    except (OSError, *YAML_ERRORS) as error:
        findings.append(f"rules/file-management.md: {error}")

    checks += 1
    try:
        voice_meta, voice_body = _parse_rule_frontmatter(
            (repository / "rules/writing-voice.md").read_text(encoding="utf-8")
        )
        if not voice_meta or voice_meta.get("trigger") != "always_on" or not voice_meta.get("description"):
            findings.append("rules/writing-voice.md lacks valid always_on trigger frontmatter")
        if not voice_body:
            findings.append("rules/writing-voice.md has empty body")
    except (OSError, *YAML_ERRORS) as error:
        findings.append(f"rules/writing-voice.md: {error}")

    assemble_mod = _load_assemble_module(repository)
    checks += 1
    if assemble_mod is None:
        findings.append("Missing scripts/assemble.py")
    else:
        packages = assemble_mod.build_packages()
        portable_pkg = packages["portable"][1]
        antigravity_pkg = packages["antigravity"][1]
        hermes_pkg = packages["hermes"][1]

        checks += 1
        try:
            hermes = _load_yaml_text(hermes_pkg["plugin.yaml"].decode("utf-8"))
            if root_identity is not None:
                for field in ("name", "version", "description"):
                    if hermes.get(field) != root_identity.get(field):
                        findings.append(f"Hermes bundle {field} differs from root plugin.json")
            for required_hermes_file in ("skills/manage-file-operations/core.md", "rules/writing-voice.md"):
                if required_hermes_file not in hermes_pkg:
                    findings.append(f"Hermes bundle missing {required_hermes_file}")
        except (KeyError, AttributeError, *YAML_ERRORS) as error:
            findings.append(f"Hermes bundle manifest: {error}")

        checks += 1
        try:
            agy_manifest = json.loads(antigravity_pkg["plugin.json"].decode("utf-8"))
            if root_identity is not None:
                for field in ("name", "version", "description", "author", "homepage", "repository"):
                    if agy_manifest.get(field) != root_identity.get(field):
                        findings.append(f"Antigravity bundle plugin.json {field} differs from root plugin.json")
            for required_agy_file in ("hooks.json", "hooks/session-start.py"):
                if required_agy_file not in antigravity_pkg:
                    findings.append(f"Antigravity bundle missing {required_agy_file}")
            meta, body = _parse_rule_frontmatter(antigravity_pkg["rules/file-management.md"].decode("utf-8"))
            if not meta or meta.get("trigger") != "always_on":
                findings.append("Antigravity foundation rule lacks an always_on trigger")
            core = (repository / "skills/manage-file-operations/core.md").read_text(encoding="utf-8").strip()
            if body != core:
                findings.append("Antigravity foundation rule differs from canonical core")
        except (KeyError, OSError, ValueError, *YAML_ERRORS) as error:
            findings.append(f"Antigravity bundle: {error}")

        for bundle_name, pkg_files in (("portable", portable_pkg), ("antigravity", antigravity_pkg), ("hermes", hermes_pkg)):
            checks += 1
            declared = {
                Path(rel).parts[1]
                for rel in pkg_files
                if rel.startswith("skills/") and Path(rel).name == "SKILL.md" and len(Path(rel).parts) == 3
            }
            if declared != skill_names:
                findings.append(f"{bundle_name}: packaged skill inventory differs from catalog")
            checks += 1
            try:
                source = (repository / "rules/writing-voice.md").read_text(encoding="utf-8").strip()
                content = pkg_files["rules/writing-voice.md"].decode("utf-8")
                meta, _ = _parse_rule_frontmatter(content)
                if not meta or meta.get("trigger") != "always_on":
                    findings.append(f"{bundle_name}: writing voice rule lacks an always_on trigger")
                if content.strip() != source:
                    findings.append(f"{bundle_name}: writing voice rule differs from canonical source")
            except (KeyError, OSError, *YAML_ERRORS) as error:
                findings.append(f"{bundle_name}: writing voice rule: {error}")

        checks += 1
        retired_codex_projections = [rel for rel in portable_pkg if rel.endswith("/agents/openai.yaml")]
        if retired_codex_projections:
            findings.append(f"portable: retired Codex openai.yaml projections present: {retired_codex_projections}")

    for directory in ("skills", "rules", "harness-adapters"):
        base = repository / directory
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                checks += 1
                parts = path.relative_to(base).parts
                if any(part in EXCLUDED_PACKAGE_PARTS for part in parts):
                    findings.append(f"{path.relative_to(repository)}: private configuration or scratch in package source")

    for leak_dir in ("skills", "rules", "hooks"):
        base = repository / leak_dir
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(base).parts
            if any(part in {"__pycache__", ".pytest_cache"} for part in rel_parts) or path.suffix == ".pyc":
                continue
            raw = path.read_bytes()
            if b"\x00" in raw:
                continue
            checks += 1
            text = raw.decode("utf-8", errors="ignore")
            rel_path = path.relative_to(repository).as_posix()
            for label, pattern in LOCAL_PATH_LEAK_PATTERNS:
                if pattern.search(text):
                    findings.append(f"{rel_path}: leaked machine-local path ({label})")

    checks += 1
    try:
        hooks = json.loads((repository / "hooks/hooks.json").read_text(encoding="utf-8"))
        handlers = hooks["hooks"]["SessionStart"][0]["hooks"]
        if not any(
            handler.get("type") == "command"
            and "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.py" in handler.get("command", "")
            for handler in handlers
        ):
            findings.append("Codex/Claude startup hook is not registered")
        hook_script = repository / "hooks/session-start.py"
        if not hook_script.is_file():
            findings.append("Codex/Claude startup hook script is missing")
        else:
            hook_source = hook_script.read_text(encoding="utf-8")
            if ".nyssaai" in hook_source or '".nyssa"' in hook_source or "'.nyssa'" in hook_source:
                findings.append("hooks/session-start.py still references retired .nyssaai/.nyssa config directories")
            if "NYSSA_PLUGIN_STATE_DIR" in hook_source:
                findings.append("hooks/session-start.py still references retired NYSSA_PLUGIN_STATE_DIR")
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        findings.append(f"Codex/Claude startup hook: {error}")

    checks += 1
    try:
        agy_hooks = json.loads((repository / "hooks.json").read_text(encoding="utf-8"))
        agy_handlers = agy_hooks["agent-skills"]["SessionStart"]
        if not any(
            isinstance(handler, dict)
            and handler.get("type") == "command"
            and handler.get("command") == 'python "./hooks/session-start.py"'
            for handler in agy_handlers
        ):
            findings.append("Antigravity root hooks.json SessionStart handler is not registered")
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        findings.append(f"Antigravity root hooks.json: {error}")

    eval_checks, eval_findings = validate_evals_directory(repository, skill_names)
    checks += eval_checks
    findings.extend(eval_findings)

    return {
        "passed": not findings,
        "checks": checks,
        "skills": len(skills),
        "findings": findings,
        "scope": "Local packaging, harness-adapters, and references only; no runtime installation claims",
    }
