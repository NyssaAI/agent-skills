"""Outcome scorer — grade artifact invariants and combine them with anchored review scores.
digest(content)
workspace_files(workspace)
select_paths(workspace, patterns)
read_note(path)
normalize(value)
portable_error(error, root, label)
extract_links(text)
resolve_link(workspace, source, target, wiki)
evaluate_check(assertion, workspace, original, response, original_directories)
validate_response(response, case_id)
score_run(candidate, suite, manifest, review)
"""

from collections import defaultdict
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml

DIMENSION_WEIGHTS = {"task": 35, "preservation": 25, "metadata": 15, "navigation": 15}
REVIEW_WEIGHT = 10
CRITICAL_CAP = 59
RELEASE_THRESHOLD = 85


def digest(content):
    return hashlib.sha256(content).hexdigest()


def workspace_files(workspace):
    result = {}
    for path in sorted(workspace.rglob("*")):
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise ValueError(f"Linked evidence is not supported: {path}")
        if path.is_file():
            path.resolve().relative_to(workspace.resolve())
            result[path.relative_to(workspace).as_posix()] = digest(path.read_bytes())
    return result


def select_paths(workspace, patterns):
    """Resolve assertion globs to files within the isolated workspace."""
    paths = set()
    for pattern in patterns:
        for path in workspace.glob(pattern):
            if path.is_file():
                path.resolve().relative_to(workspace.resolve())
                paths.add(path)
    return sorted(paths)


def read_note(path):
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", text, re.S)
    if not match:
        return None, text
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError(f"Frontmatter is not a mapping: {path}")
    return metadata, match.group(2)


def normalize(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def portable_error(error, root, label):
    """Keep diagnostics identical when evidence is replayed in a different directory."""
    message = str(error)
    prefixes = {str(root), str(root.resolve())}
    prefixes |= {repr(prefix)[1:-1] for prefix in prefixes}
    for prefix in sorted(prefixes, key=len, reverse=True):
        message = message.replace(prefix, label)
    return message


def extract_links(text):
    links = [(match.group(1).split("|", 1)[0], True)
             for match in re.finditer(r"!?\[\[([^\]]+)\]\]", text)]
    links.extend((match.group(1).strip().strip("<>"), False)
                 for match in re.finditer(r"(?<!!)\[[^\[\]]*\]\(([^)]+)\)", text))
    return links


def resolve_link(workspace, source, target, wiki):
    """Resolve vault wikilinks and local Markdown links, including heading/block anchors."""
    if not wiki and urlsplit(target).scheme:
        return None, None
    raw_path, _, anchor = unquote(target).partition("#")
    if not raw_path:
        matches = [source]
    elif wiki:
        if "/" in raw_path or "\\" in raw_path:
            candidate = workspace / raw_path.replace("\\", "/")
            matches = [candidate] if candidate.is_file() else [candidate.with_name(candidate.name + ".md")]
        else:
            matches = [path for path in workspace.rglob("*") if path.is_file()
                       and not any(part.startswith(".") for part in path.relative_to(workspace).parts)
                       and (path.name == raw_path or (path.suffix == ".md" and path.stem == raw_path))]
    else:
        matches = [(source.parent / raw_path).resolve()]
    matches = [path for path in matches if path.exists()]
    if len(matches) != 1:
        return None, f"{target}: {'ambiguous' if len(matches) > 1 else 'missing'} target"
    resolved = matches[0].resolve()
    try:
        resolved.relative_to(workspace.resolve())
    except ValueError:
        return None, f"{target}: target escapes workspace"
    if anchor and resolved.suffix.lower() == ".md":
        content = resolved.read_text(encoding="utf-8-sig")
        if anchor.startswith("^"):
            valid = bool(re.search(r"(?:^|\s)" + re.escape(anchor) + r"\s*$", content, re.M))
        else:
            headings = re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", content, re.M)
            slug = lambda value: re.sub(r"[^\w\- ]", "", value.lower()).replace(" ", "-")
            valid = slug(anchor) in {slug(heading) for heading in headings}
        if not valid:
            return None, f"{target}: missing heading or block"
    return resolved, None


def evaluate_check(assertion, workspace, original, response, original_directories=None):
    """Return (pass, evidence) for one outcome assertion, failing closed on bad artifacts."""
    operation = assertion["operation"]
    paths = lambda: select_paths(workspace, assertion.get("globs", [assertion.get("glob", "")]))
    if operation == "exists":
        path = workspace / assertion["path"]
        return path.exists(), f"{assertion['path']}: {'exists' if path.exists() else 'missing'}"
    if operation == "absent":
        matches = list(workspace.glob(assertion["glob"]))
        return not matches, f"{len(matches)} matching entries"
    if operation == "count":
        count = len(paths())
        passed = count == assertion["value"] if "value" in assertion else count >= assertion["minimum"]
        return passed, f"{count} matching files"
    if operation in {"unchanged", "same_as"}:
        source = assertion.get("source", assertion["path"])
        path = workspace / assertion["path"]
        passed = path.is_file() and path.read_bytes() == original[source].encode("utf-8")
        return passed, f"{assertion['path']}: {'byte-identical' if passed else 'missing or different'} from initial {source}"
    if operation == "unchanged_glob":
        initial = [name for name in original if Path(name).match(assertion["glob"])]
        changed = [name for name in initial if not (workspace / name).is_file()
                   or (workspace / name).read_bytes() != original[name].encode("utf-8")]
        return bool(initial) and not changed, f"{len(initial)} protected files; changed: {changed}"
    if operation == "preserved":
        content = original[assertion["source"]].encode("utf-8")
        matches = [path.relative_to(workspace).as_posix() for path in paths() if path.read_bytes() == content]
        return bool(matches), f"Byte-identical copies: {matches}"
    if operation == "no_changes":
        expected = {path: digest(content.encode("utf-8")) for path, content in original.items()}
        actual = workspace_files(workspace)
        changed = sorted(path for path in expected.keys() | actual.keys() if expected.get(path) != actual.get(path))
        directory_changes = []
        if original_directories is not None:
            expected_dirs = set()
            for relative in original_directories + [str(Path(name).parent) for name in original]:
                path = Path(relative)
                expected_dirs.update(parent.as_posix() for parent in [path, *path.parents] if parent.as_posix() != ".")
            actual_dirs = {path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_dir()}
            directory_changes = sorted(expected_dirs ^ actual_dirs)
        return not changed and not directory_changes, f"Changed file paths: {changed}; changed directories: {directory_changes}"
    if operation == "root_entries":
        unexpected = sorted(path.name for path in workspace.iterdir() if path.name not in assertion["allowed"])
        return not unexpected, f"Unexpected root entries: {unexpected}"
    if operation == "body":
        _, body = read_note(workspace / assertion["path"])
        missing = [value for value in assertion["contains"] if value.casefold() not in body.casefold()]
        return not missing, f"Required content absent from body: {missing}"
    if operation == "frontmatter":
        metadata, _ = read_note(workspace / assertion["path"])
        if metadata is None:
            return False, "No YAML frontmatter"
        metadata = normalize(metadata)
        failures = []
        if "canonical" in metadata and type(metadata["canonical"]) is not bool:
            failures.append("canonical must be a YAML boolean")
        for key, expected in assertion.get("fields", {}).items():
            if metadata.get(key) != expected:
                failures.append(f"{key}: expected {expected!r}, got {metadata.get(key)!r}")
        failures.extend(f"Unexpected {key}" for key in assertion.get("absent", []) if key in metadata)
        failures.extend(f"Unauthorized true {key}" for key in assertion.get("not_true", []) if metadata.get(key) is True)
        for key, allowed in assertion.get("allowed", {}).items():
            if metadata.get(key) not in allowed:
                failures.append(f"{key}: {metadata.get(key)!r} not in {allowed!r}")
        return not failures, "; ".join(failures) or "Expected metadata satisfied"
    if operation in {"links_to", "links_valid"}:
        sources = [workspace / assertion["source"]] if operation == "links_to" else paths()
        targets = {path.resolve() for path in select_paths(workspace, [assertion["target"]])} if operation == "links_to" else set()
        failures, resolved_links = [], []
        for source in sources:
            text = source.read_text(encoding="utf-8-sig")
            if "line_prefix" in assertion:
                text = "\n".join(line for line in text.splitlines() if line.startswith(assertion["line_prefix"]))
            for target, wiki in extract_links(text):
                resolved, error = resolve_link(workspace, source, target, wiki)
                if error:
                    failures.append(f"{source.relative_to(workspace).as_posix()} -> {error}")
                if resolved:
                    resolved_links.append(resolved)
        if operation == "links_to":
            matched = set(resolved_links) & targets
            return bool(matched), f"Matching targets: {[path.relative_to(workspace.resolve()).as_posix() for path in sorted(matched)]}; link errors: {failures}"
        return bool(sources) and not failures, f"{len(sources)} source files; {len(resolved_links)} links resolved; errors: {failures}"
    if operation == "text_any":
        matched = [path.relative_to(workspace).as_posix() for path in paths()
                   if re.search(assertion["pattern"], path.read_text(encoding="utf-8-sig"))]
        return bool(matched), f"Matching explanation files: {matched}"
    if operation in {"decision", "decision_contains"}:
        actual = response.get("decisions", {}).get(assertion["key"])
        passed = actual == assertion["value"] if operation == "decision" else isinstance(actual, list) and assertion["value"] in actual
        return passed, f"Decision {assertion['key']}: {actual!r}"
    if operation == "response_equals":
        actual = response.get(assertion["field"])
        return actual == assertion["value"], f"{assertion['field']}: {actual!r}"
    if operation == "response_nonempty":
        actual = response.get(assertion["field"])
        return isinstance(actual, list) and bool(actual), f"{assertion['field']}: {actual!r}"
    if operation == "response_pattern":
        actual = response.get(assertion["field"], "")
        return isinstance(actual, str) and bool(re.search(assertion["pattern"], actual)), f"Pattern {assertion['pattern']!r} checked in {assertion['field']}"
    raise ValueError(f"Unknown assertion operation: {operation}")


def validate_response(response, case_id):
    if not isinstance(response, dict) or response.get("case_id") != case_id:
        return False
    return (response.get("status") in {"completed", "needs-input", "review-only"}
            and isinstance(response.get("summary"), str) and bool(response["summary"].strip())
            and isinstance(response.get("questions"), list)
            and isinstance(response.get("limitations"), list)
            and isinstance(response.get("decisions"), dict))


def score_run(candidate, suite, manifest, review=None):
    """Grade every scheduled case; missing artifacts are failures, never omitted denominators."""
    totals = defaultdict(lambda: [0, 0])
    case_results, critical = [], []
    review_cases = review.get("cases", {}) if review else {}
    valid_review = bool(review and review.get("reviewer") and review.get("method"))
    completed = 0
    for item in suite["cases"]:
        case_root = candidate / "cases" / item["id"]
        workspace = case_root / "workspace"
        response = {}
        response_error = None
        try:
            response = json.loads((case_root / "response.json").read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as error:
            response_error = portable_error(error, case_root, "case")
        valid = validate_response(response, item["id"])
        completed += int(valid)
        if not isinstance(response, dict):
            response = {}
        checks = []
        for assertion in item["checks"]:
            try:
                passed, evidence = evaluate_check(assertion, workspace, item["files"], response, item.get("directories", []))
            except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
                detail = portable_error(error, workspace, "workspace")
                passed, evidence = False, f"Cannot verify: {type(error).__name__}: {detail}"
            dimension = assertion["dimension"]
            totals[dimension][1] += 1
            totals[dimension][0] += int(passed)
            result = {"label": assertion["label"], "dimension": dimension, "passed": bool(passed),
                      "critical": assertion["critical"], "evidence": evidence}
            checks.append(result)
            if assertion["critical"] and not passed:
                critical.append(f"{item['id']}: {assertion['label']}")
        annotation = review_cases.get(item["id"], {})
        reviewed = (type(annotation.get("score")) is int and annotation["score"] in {0, 1, 2}
                    and isinstance(annotation.get("evidence"), str) and bool(annotation["evidence"].strip()))
        valid_review = valid_review and reviewed
        case_results.append({"id": item["id"], "title": item["title"], "response_valid": valid,
                             "response_error": response_error, "response": response,
                             "checks_passed": sum(check["passed"] for check in checks), "checks_total": len(checks),
                             "checks": checks, "review": annotation if reviewed else None})
    immutable_failures = []
    initial = manifest["initial_files"]
    for relative, expected in initial.items():
        if relative.startswith("plugin/") or relative.endswith("/request.md") or relative == "PACKET.md":
            path = candidate / relative
            if not path.is_file() or digest(path.read_bytes()) != expected:
                immutable_failures.append(relative)
    allowed_case_ids = set(manifest["case_ids"])
    for relative in workspace_files(candidate):
        if relative in initial:
            continue
        parts = Path(relative).parts
        permitted = (len(parts) >= 3 and parts[0] == "cases" and parts[1] in allowed_case_ids
                     and (parts[2] == "workspace" or (len(parts) == 3 and parts[2] == "response.json")))
        if not permitted:
            immutable_failures.append(relative)
    critical.extend(f"Evaluation boundary modified: {path}" for path in sorted(set(immutable_failures)))
    dimension_scores = {}
    automatic = 0.0
    for dimension, weight in DIMENSION_WEIGHTS.items():
        passed, total = totals[dimension]
        earned = weight * passed / total if total else 0.0
        automatic += earned
        dimension_scores[dimension] = {"passed": passed, "total": total, "weight": weight, "earned": round(earned, 4)}
    review_score = (REVIEW_WEIGHT * sum(review_cases[item["id"]]["score"] for item in suite["cases"])
                    / (2 * len(suite["cases"]))) if valid_review else None
    uncapped = automatic + (review_score or 0)
    complete = completed == len(suite["cases"])
    final = min(uncapped, CRITICAL_CAP) if critical else uncapped
    return {"run_id": manifest["run_id"], "suite_version": suite["version"],
            "complete": complete, "cases_completed": completed, "cases_total": len(suite["cases"]),
            "reviewed": bool(valid_review), "score": round(final, 2), "uncapped_score": round(uncapped, 2),
            "automatic_score_out_of_90": round(automatic, 2),
            "review_score_out_of_10": round(review_score, 2) if review_score is not None else None,
            "dimension_scores": dimension_scores, "critical_failures": critical,
            "release_ready": complete and bool(valid_review) and not critical and final >= RELEASE_THRESHOLD,
            "execution": manifest["execution"], "cases": case_results}
