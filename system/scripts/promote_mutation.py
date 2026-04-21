#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUTATIONS = ROOT / "workspace" / "mutations"
SKILLS = ROOT / "skills"

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
BLOCKING_SNIPPETS = (
    "SYNTHESIS_REQUIRED",
    "MERGE_REQUIRED",
    "DRAFT:",
    "TODO:",
    "[Add change summary here]",
    "Initial governed skill scaffold; replace TODOs",
    "replace TODOs before validation",
    ":contentReference",
    "oaicite",
)
SKILL_ID_RE = re.compile(r"^epcb(?:\.[a-z0-9][a-z0-9_]*)+$")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "mutation"


def id_token(value: str) -> str:
    return slugify(value).replace("-", "_")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def resolve_stage_dir(value: str) -> Path:
    raw = Path(value)
    if raw.is_absolute():
        stage_dir = raw
    elif (ROOT / raw).exists():
        stage_dir = ROOT / raw
    else:
        stage_dir = MUTATIONS / slugify(value)

    stage_dir = stage_dir.resolve()
    try:
        stage_dir.relative_to(MUTATIONS.resolve())
    except ValueError:
        print("ERROR: mutation promotion must come from workspace/mutations/", file=sys.stderr)
        raise SystemExit(1)
    return stage_dir


def parse_frontmatter(text: str):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("skill.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("skill.md frontmatter is not closed") from exc

    meta = {}
    for line in lines[1:end]:
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    body = "\n".join(lines[end + 1 :]).strip("\n")
    return meta, body


def normalize_candidate(text: str, skill_name: str | None, domain: str | None) -> tuple[str, str]:
    meta, body = parse_frontmatter(text)
    name = slugify(skill_name or meta.get("name") or "")
    if not name:
        raise ValueError("candidate frontmatter is missing name; pass --skill-name")

    generated_skill_id = f"epcb.{id_token(domain)}.{id_token(name)}" if domain else f"epcb.mutated.{id_token(name)}"
    skill_id = generated_skill_id if domain or not meta.get("skill_id") else meta["skill_id"]

    ordered = {
        "build_number": "001",
        "skill_id": skill_id,
        "name": name,
        "description": meta.get("description", "").replace("DRAFT ", "").strip(),
        "trigger_keywords": meta.get("trigger_keywords", "").strip(),
        "owner": meta.get("owner", "EPCB") or "EPCB",
        "status": "active",
        "created_at": meta.get("created_at") or date.today().isoformat(),
        "last_updated": date.today().isoformat(),
    }

    frontmatter = ["---"]
    for key in REQUIRED_FRONTMATTER_KEYS:
        frontmatter.append(f"{key}: {yaml_quote(ordered[key])}")
    frontmatter.append("---")
    return "\n".join(frontmatter) + "\n\n" + body.rstrip() + "\n", name


def top_level_headings(text: str):
    return [
        (line_no, line.strip())
        for line_no, line in enumerate(text.splitlines(), start=1)
        if line.startswith("# ")
    ]


def candidate_path(stage_dir: Path) -> Path:
    current_file = stage_dir / "CURRENT"
    if current_file.exists():
        current = current_file.read_text().strip()
        path = stage_dir / current / "skill.md"
        if path.exists():
            return path

    legacy_path = stage_dir / "candidate.skill.md"
    if legacy_path.exists():
        return legacy_path

    fallback = stage_dir / "V001" / "skill.md"
    if fallback.exists():
        return fallback

    return stage_dir / "CURRENT" / "skill.md"


def validate_candidate(stage_dir: Path, candidate_text: str, path: Path):
    errors = []
    required_paths = (
        stage_dir / "CURRENT",
        stage_dir / "CHANGELOG.md",
        stage_dir / "references" / "mutation-brief.md",
        stage_dir / "references" / "parent-map.md",
        stage_dir / "references" / "merge-notes.md",
        stage_dir / "references" / "promotion-checklist.md",
    )
    if path.name != "skill.md":
        errors.append("staged candidate must be named V###/skill.md, not candidate.skill.md")
    for required_path in required_paths:
        if not required_path.exists():
            errors.append(f"missing staged file: {required_path.relative_to(stage_dir)}")

    parent_snapshots = sorted((stage_dir / "parents").glob("*/*/skill.md"))
    if len(parent_snapshots) < 2:
        errors.append("mutation must include at least two parent snapshots under parents/<skill>/<V###>/skill.md")

    checklist_path = stage_dir / "references" / "promotion-checklist.md"
    if checklist_path.exists():
        checklist = checklist_path.read_text()
        for snippet in BLOCKING_SNIPPETS:
            if snippet in checklist:
                errors.append(f"{checklist_path.relative_to(ROOT)} still contains {snippet!r}")

    meta, _ = parse_frontmatter(candidate_text)
    for key in REQUIRED_FRONTMATTER_KEYS:
        if key not in meta:
            errors.append(f"candidate frontmatter is missing {key}")

    description = meta.get("description", "").strip()
    if len(description) < 20:
        errors.append("candidate description is too short")
    if "\n" in description:
        errors.append("candidate description must be one line")

    skill_id = meta.get("skill_id", "")
    if not SKILL_ID_RE.fullmatch(skill_id):
        errors.append(f"candidate skill_id {skill_id!r} must match epcb.* format")

    keywords = [item.strip() for item in meta.get("trigger_keywords", "").split(",") if item.strip()]
    if len(keywords) < 3:
        errors.append("candidate trigger_keywords must contain at least 3 comma-separated entries")

    if not any(phrase in candidate_text for phrase in ("Use when", "Use this skill when")):
        errors.append("candidate must include a 'Use when' or 'Use this skill when' trigger phrase")

    for snippet in BLOCKING_SNIPPETS:
        if snippet in candidate_text:
            errors.append(f"candidate still contains blocking scaffold/source artifact: {snippet!r}")

    headings = top_level_headings(candidate_text)
    heading_positions = {heading: line_no for line_no, heading in headings}
    last_position = 0
    for section in REQUIRED_SECTIONS:
        position = heading_positions.get(section)
        if position is None:
            errors.append(f"candidate must include {section}")
            continue
        if position < last_position:
            errors.append(f"candidate has {section} out of required section order")
        last_position = max(last_position, position)

    if len(candidate_text.splitlines()) > 800:
        errors.append("candidate is over 800 lines; move support material out before promotion")

    results_path = stage_dir / "validation-results.md"
    checklist_path = stage_dir / "references" / "promotion-checklist.md"
    if checklist_path.exists():
        checklist = checklist_path.read_text()
        if not re.search(r"^Recommendation:\s*promote\s*$", checklist, flags=re.IGNORECASE | re.MULTILINE):
            errors.append("references/promotion-checklist.md must include exactly `Recommendation: promote`")
    elif results_path.exists():
        results = results_path.read_text()
        if not re.search(r"^Recommendation:\s*promote\s*$", results, flags=re.IGNORECASE | re.MULTILINE):
            errors.append("legacy validation-results.md must include exactly `Recommendation: promote`")

    return errors


def write_skill_folder(destination: Path, candidate_text: str, mutation_name: str, stage_dir: Path):
    version_dir = destination / "V001"
    version_dir.mkdir(parents=True, exist_ok=False)
    (destination / "archived").mkdir()
    (destination / "references").mkdir()
    (destination / "assets").mkdir()
    (destination / "scripts").mkdir()

    for dirname in ("archived", "references", "assets", "scripts"):
        (destination / dirname / ".gitkeep").write_text("")

    (destination / "CURRENT").write_text("V001\n")
    (version_dir / "skill.md").write_text(candidate_text)
    (destination / "CHANGELOG.md").write_text(
        "\n".join(
            [
                "# Change Log",
                "",
                "## V001",
                f"- Promoted from staged mutation `{mutation_name}`.",
                f"- Staging package: `{stage_dir.relative_to(ROOT).as_posix()}`.",
                "",
            ]
        )
    )


def run_repo_command(command: list[str]):
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(command)} failed with exit code {result.returncode}")


def promote(args):
    if not args.approve:
        print("ERROR: promotion requires explicit --approve", file=sys.stderr)
        return 1

    stage_dir = resolve_stage_dir(args.mutation)
    path = candidate_path(stage_dir)
    if not path.exists():
        print(f"ERROR: missing staged candidate at CURRENT -> V###/skill.md", file=sys.stderr)
        return 1

    mutation_name = stage_dir.name
    normalized_text, skill_name = normalize_candidate(
        path.read_text(),
        args.skill_name,
        args.domain,
    )
    destination = SKILLS / skill_name
    if destination.exists():
        print(f"ERROR: destination already exists: {destination.relative_to(ROOT)}", file=sys.stderr)
        return 1

    errors = validate_candidate(stage_dir, normalized_text, path)
    if errors:
        print("ERROR: mutation is not ready for promotion:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    created = False
    try:
        write_skill_folder(destination, normalized_text, mutation_name, stage_dir)
        created = True
        run_repo_command(["python3", "system/scripts/update_index.py"])
        run_repo_command(["python3", "system/scripts/validate_skills.py"])
        run_repo_command(["python3", "system/scripts/update_index.py", "--check"])
    except Exception as exc:
        if created and destination.exists():
            shutil.rmtree(destination)
            subprocess.run(["python3", "system/scripts/update_index.py"], cwd=ROOT)
        print(f"ERROR: promotion rolled back: {exc}", file=sys.stderr)
        return 1

    checklist_path = stage_dir / "references" / "promotion-checklist.md"
    if checklist_path.exists():
        with checklist_path.open("a") as handle:
            handle.write(
                "\n"
                f"Promoted on {date.today().isoformat()} to `skills/{skill_name}/V001/skill.md`.\n"
            )

    print("")
    print(f"Promoted mutation `{mutation_name}` to skills/{skill_name}/V001/skill.md")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Promote an approved staged mutation into the live skills folder."
    )
    parser.add_argument("mutation", help="mutation folder name or workspace/mutations/<name> path")
    parser.add_argument("--skill-name", help="override promoted skill folder/frontmatter name")
    parser.add_argument("--domain", help="override skill_id domain, for example meta or delivery")
    parser.add_argument("--approve", action="store_true", help="required human approval gate")
    args = parser.parse_args()
    return promote(args)


if __name__ == "__main__":
    raise SystemExit(main())
