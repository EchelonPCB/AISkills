#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUTATIONS = ROOT / "workspace" / "mutations"
VERSION_RE = re.compile(r"^V\d{3}$")
RECOMMEND_PROMOTE_RE = re.compile(r"^Recommendation:\s*promote\s*$", re.IGNORECASE | re.MULTILINE)
BLOCKING_MARKERS = (
    "SYNTHESIS_REQUIRED",
    "MERGE_REQUIRED",
    "DRAFT:",
    "TODO:",
    "[Add change summary here]",
    "Initial governed skill scaffold",
    "replace TODOs",
    ":contentReference",
    "oaicite",
)
REQUIRED_REFERENCE_FILES = (
    "mutation-brief.md",
    "parent-map.md",
    "merge-notes.md",
    "promotion-checklist.md",
)
REQUIRED_SECTIONS = (
    "# Index",
    "# Objective",
    "# Trigger",
    "# Do Not Use When",
    "# Required Inputs",
    "# Optional Inputs",
    "# Outputs",
    "# Support Layers",
    "# Procedure",
    "# Decision Logic",
    "# Validation",
    "# Rules",
    "# Failure Modes",
    "# Dependencies",
    "# Assumptions",
    "# Change Log",
)
REQUIRED_FRONTMATTER_KEYS = (
    "build_number",
    "skill_id",
    "name",
    "description",
    "trigger_keywords",
    "owner",
    "status",
    "created_at",
    "last_updated",
)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "mutation"


def resolve_stage_dir(value: str) -> Path:
    raw = Path(value)
    if raw.is_absolute():
        return raw.resolve()
    if (ROOT / raw).exists():
        return (ROOT / raw).resolve()
    return (MUTATIONS / slugify(value)).resolve()


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def frontmatter_lines(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return []
    try:
        end = lines.index("---", 1)
    except ValueError:
        return []
    return lines[1:end]


def top_level_headings(text: str) -> list[tuple[int, str]]:
    return [
        (line_no, line.strip())
        for line_no, line in enumerate(text.splitlines(), start=1)
        if line.startswith("# ")
    ]


def read_current(stage_dir: Path, errors: list[str]) -> tuple[str | None, Path | None]:
    current_file = stage_dir / "CURRENT"
    if not current_file.exists():
        errors.append("missing CURRENT")
        return None, None

    current = current_file.read_text().strip()
    if not VERSION_RE.fullmatch(current):
        errors.append("CURRENT must contain a V### version")
        return current, None

    skill_path = stage_dir / current / "skill.md"
    if not skill_path.exists():
        errors.append(f"CURRENT points to missing {rel(skill_path)}")
        return current, None
    return current, skill_path


def validate_candidate(skill_path: Path, errors: list[str]):
    text = skill_path.read_text()
    frontmatter = frontmatter_lines(text)
    if not frontmatter:
        errors.append(f"{rel(skill_path)} must start with YAML frontmatter")
    else:
        present_keys = [
            line.split(":", 1)[0].strip()
            for line in frontmatter
            if ":" in line and not line.lstrip().startswith("#")
        ]
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in present_keys:
                errors.append(f"{rel(skill_path)} frontmatter missing {key}")

    headings = top_level_headings(text)
    heading_positions = {heading: line_no for line_no, heading in headings}
    last_position = 0
    for section in REQUIRED_SECTIONS:
        position = heading_positions.get(section)
        if position is None:
            errors.append(f"{rel(skill_path)} missing {section}")
            continue
        if position < last_position:
            errors.append(f"{rel(skill_path)} has {section} out of required order")
        last_position = max(last_position, position)
    return text


def validate_mutation(stage_dir: Path, promotable: bool) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    if not stage_dir.exists():
        errors.append(f"mutation folder does not exist: {rel(stage_dir)}")
        return result(stage_dir, None, None, errors, warnings)
    try:
        stage_dir.relative_to(MUTATIONS.resolve())
    except ValueError:
        errors.append("mutation folder must live under workspace/mutations/")

    current, skill_path = read_current(stage_dir, errors)
    candidate_text = ""
    if skill_path:
        candidate_text = validate_candidate(skill_path, errors)

    root_markdown = sorted(
        path.name
        for path in stage_dir.glob("*.md")
        if path.name != "CHANGELOG.md"
    )
    if root_markdown:
        errors.append(f"root mutation folder has loose markdown files: {', '.join(root_markdown)}")

    if not (stage_dir / "CHANGELOG.md").exists():
        errors.append("missing CHANGELOG.md")

    parent_snapshots = sorted((stage_dir / "parents").glob("*/*/skill.md"))
    if len(parent_snapshots) < 2:
        errors.append("expected at least two parent snapshots under parents/<skill>/<V###>/skill.md")

    references_dir = stage_dir / "references"
    for filename in REQUIRED_REFERENCE_FILES:
        path = references_dir / filename
        if not path.exists():
            errors.append(f"missing references/{filename}")

    checklist_path = references_dir / "promotion-checklist.md"
    checklist_text = checklist_path.read_text() if checklist_path.exists() else ""
    recommendation = "missing"
    match = re.search(r"^Recommendation:\s*(.+?)\s*$", checklist_text, flags=re.IGNORECASE | re.MULTILINE)
    if match:
        recommendation = match.group(1).strip().lower()
    elif checklist_path.exists():
        errors.append("promotion checklist must include Recommendation: <promote|revise|reject>")

    active_texts = [candidate_text]
    for filename in REQUIRED_REFERENCE_FILES:
        path = references_dir / filename
        if path.exists():
            active_texts.append(path.read_text())

    if promotable:
        if not RECOMMEND_PROMOTE_RE.search(checklist_text):
            errors.append("promotable mutation must have references/promotion-checklist.md set to Recommendation: promote")
        for marker in BLOCKING_MARKERS:
            for text in active_texts:
                if marker in text:
                    errors.append(f"promotable mutation still contains marker {marker!r}")
                    break
    else:
        markers = sorted({marker for marker in BLOCKING_MARKERS if any(marker in text for text in active_texts)})
        if markers:
            warnings.append(f"staged mutation contains unresolved markers: {', '.join(markers)}")
        if recommendation != "promote":
            warnings.append(f"promotion recommendation is {recommendation!r}")

    return result(stage_dir, current, skill_path, errors, warnings, parent_snapshots, recommendation)


def result(
    stage_dir: Path,
    current: str | None,
    skill_path: Path | None,
    errors: list[str],
    warnings: list[str],
    parent_snapshots: list[Path] | None = None,
    recommendation: str | None = None,
) -> dict:
    return {
        "ok": not errors,
        "path": rel(stage_dir),
        "current_version": current,
        "current_skill_path": rel(skill_path) if skill_path else None,
        "parent_snapshot_count": len(parent_snapshots or []),
        "parent_snapshots": [rel(path) for path in parent_snapshots or []],
        "promotion_recommendation": recommendation,
        "errors": errors,
        "warnings": warnings,
    }


def print_plain(payload: dict):
    if payload["ok"]:
        print(f"Mutation is structurally valid: {payload['path']}")
    else:
        print(f"Mutation has errors: {payload['path']}", file=sys.stderr)
    for warning in payload["warnings"]:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in payload["errors"]:
        print(f"ERROR: {error}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a staged AISkills mutation workspace.")
    parser.add_argument("mutation", help="mutation folder name or workspace/mutations/<name> path")
    parser.add_argument("--promotable", action="store_true", help="enforce promotion-ready checks")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()

    payload = validate_mutation(resolve_stage_dir(args.mutation), args.promotable)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_plain(payload)
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
