#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUTATIONS = ROOT / "workspace" / "mutations"
VERSION_RE = re.compile(r"^V(\d{3})$")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "mutation"


def resolve_stage_dir(value: str) -> Path:
    raw = Path(value)
    if raw.is_absolute():
        stage_dir = raw
    elif (ROOT / raw).exists():
        stage_dir = ROOT / raw
    else:
        stage_dir = MUTATIONS / slugify(value)
    return stage_dir.resolve()


def update_frontmatter(text: str, next_number: str) -> str:
    today = date.today().isoformat()
    text = re.sub(r'build_number:\s*"\d+"', f'build_number: "{next_number}"', text, count=1)
    text = re.sub(r'last_updated:\s*"[^"]*"', f'last_updated: "{today}"', text, count=1)
    return text


def bump(args):
    stage_dir = resolve_stage_dir(args.mutation)
    current_file = stage_dir / "CURRENT"
    if not current_file.exists():
        print(f"ERROR: missing {current_file.relative_to(ROOT)}", file=sys.stderr)
        return 1

    current = current_file.read_text().strip()
    match = VERSION_RE.fullmatch(current)
    if not match:
        print("ERROR: CURRENT must contain a V### version", file=sys.stderr)
        return 1

    current_dir = stage_dir / current
    current_skill = current_dir / "skill.md"
    if not current_skill.exists():
        print(f"ERROR: missing {current_skill.relative_to(ROOT)}", file=sys.stderr)
        return 1

    next_number = f"{int(match.group(1)) + 1:03d}"
    next_version = f"V{next_number}"
    next_dir = stage_dir / next_version
    archived_dir = stage_dir / "archived" / current
    if next_dir.exists():
        print(f"ERROR: {next_dir.relative_to(ROOT)} already exists", file=sys.stderr)
        return 1
    if archived_dir.exists():
        print(f"ERROR: {archived_dir.relative_to(ROOT)} already exists", file=sys.stderr)
        return 1

    next_dir.mkdir(parents=True)
    next_skill = next_dir / "skill.md"
    next_skill.write_text(update_frontmatter(current_skill.read_text(), next_number))

    archived_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(current_dir), str(archived_dir))
    current_file.write_text(f"{next_version}\n")

    changelog = stage_dir / "CHANGELOG.md"
    with changelog.open("a") as handle:
        handle.write(
            "\n"
            f"## {next_version}\n"
            f"- Bumped from {current} on {date.today().isoformat()}.\n"
            f"- {args.reason}\n"
        )

    print(f"Bumped mutation {stage_dir.name} to {next_version}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Create the next staged mutation version.")
    parser.add_argument("mutation", help="mutation folder name or workspace/mutations/<name> path")
    parser.add_argument("reason", nargs="?", default="Reason not provided")
    args = parser.parse_args()
    return bump(args)


if __name__ == "__main__":
    raise SystemExit(main())
