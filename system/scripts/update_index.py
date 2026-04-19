from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import sys

ROOT = Path(".")
SKILLS = ROOT / "skills"
REFERENCES = ROOT / "references"
ASSETS = ROOT / "assets"
VENDOR = ROOT / "vendor"
INDEXES = ROOT / "system" / "indexes"

VERSION_RE = re.compile(r"V\d{3}$")
SKILL_ID_RE = re.compile(r"^epcb(?:\.[a-z0-9][a-z0-9_]*)+$")


@dataclass(frozen=True)
class SkillRecord:
    folder: str
    name: str
    skill_id: str
    description: str
    trigger_keywords: str
    current_version: str
    current_path: Path


REQUIRED_SKILL_DIRS = ("archived", "references", "assets", "scripts", "logs")
def read_meta(skill_file: Path):
    meta = {
        "skill_id": "",
        "name": "",
        "description": "",
        "trigger_keywords": "",
    }

    for line in skill_file.read_text().splitlines():
        if line.startswith("skill_id:"):
            meta["skill_id"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("name:"):
            meta["name"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("description:"):
            meta["description"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("trigger_keywords:"):
            meta["trigger_keywords"] = line.split(":", 1)[1].strip().strip('"')
    return meta


def escape_cell(value: str):
    return value.replace("|", "\\|").replace("\n", " ").strip()


def collect_skills():
    records = []
    errors = []
    seen_ids = {}

    if not SKILLS.exists():
        return records, ["Missing skills directory"]

    standalone = sorted(p for p in SKILLS.glob("*.md") if p.is_file())
    for path in standalone:
        errors.append(
            f"{path.as_posix()} is a standalone skill file; move it to "
            "skills/<skill-name>/V001/skill.md with a CURRENT file"
        )

    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        current_file = skill_dir / "CURRENT"
        if not current_file.exists():
            errors.append(f"{skill_dir.as_posix()} is missing CURRENT")
            continue

        for dirname in REQUIRED_SKILL_DIRS:
            if not (skill_dir / dirname).is_dir():
                errors.append(f"{skill_dir.as_posix()} is missing {dirname}/")

        current_version = current_file.read_text().strip()
        if not VERSION_RE.fullmatch(current_version):
            errors.append(f"{current_file.as_posix()} must contain a V### version")
            continue

        skill_file = skill_dir / current_version / "skill.md"
        if not skill_file.exists():
            errors.append(
                f"{current_file.as_posix()} points to missing {skill_file.as_posix()}"
            )
            continue

        meta = read_meta(skill_file)
        name = meta["name"] or skill_dir.name
        skill_id = meta["skill_id"]
        trigger_keywords = meta["trigger_keywords"]

        if not meta["name"]:
            errors.append(f"{skill_file.as_posix()} is missing name")
        if not skill_id:
            errors.append(f"{skill_file.as_posix()} is missing skill_id")
        elif not SKILL_ID_RE.fullmatch(skill_id):
            errors.append(
                f"{skill_file.as_posix()} has non-standard skill_id {skill_id!r}; "
                "expected epcb.* with dot-separated lowercase underscore tokens"
            )
        elif skill_id in seen_ids:
            errors.append(
                f"{skill_file.as_posix()} duplicates skill_id {skill_id!r} from "
                f"{seen_ids[skill_id]}"
            )
        else:
            seen_ids[skill_id] = skill_file.as_posix()
        if not trigger_keywords:
            errors.append(f"{skill_file.as_posix()} is missing trigger_keywords")

        records.append(
            SkillRecord(
                folder=skill_dir.name,
                name=name,
                skill_id=skill_id,
                description=meta["description"],
                trigger_keywords=trigger_keywords,
                current_version=current_version,
                current_path=skill_file,
            )
        )

    return sorted(records, key=lambda r: r.name), errors


def render_manifest(records):
    lines = [
        "# MANIFEST",
        "",
        "| skill_name | skill_id | description | trigger_keywords | current_version | current_path |",
        "|------------|----------|-------------|------------------|-----------------|--------------|",
    ]
    for record in records:
        lines.append(
            f"| {escape_cell(record.name)} | "
            f"{escape_cell(record.skill_id)} | "
            f"{escape_cell(record.description)} | "
            f"{escape_cell(record.trigger_keywords)} | "
            f"{escape_cell(record.current_version)} | "
            f"{record.current_path.as_posix()} |"
        )
    return "\n".join(lines) + "\n"


def render_path_index(title, base_path):
    lines = [
        f"# {title}",
        "",
        "| Path |",
        "|------|",
    ]
    if base_path.exists():
        for path in sorted(x for x in base_path.rglob("*") if x.is_file()):
            lines.append(f"| {path.as_posix()} |")
    return "\n".join(lines) + "\n"


def write_or_check(path, content, check):
    if check:
        if not path.exists() or path.read_text() != content:
            return [f"{path.as_posix()} is out of date"]
        return []

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate generated indexes without writing files",
    )
    args = parser.parse_args()

    records, errors = collect_skills()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    INDEXES.mkdir(parents=True, exist_ok=True)
    generated = {
        ROOT / "MANIFEST.md": render_manifest(records),
        INDEXES / "reference-index.md": render_path_index("REFERENCE INDEX", REFERENCES),
        INDEXES / "asset-index.md": render_path_index("ASSET INDEX", ASSETS),
        INDEXES / "vendor-index.md": render_path_index("VENDOR INDEX", VENDOR),
    }

    check_errors = []
    for path, content in generated.items():
        check_errors.extend(write_or_check(path, content, args.check))

    if check_errors:
        for error in check_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.check:
        print("Indexes are consistent")
    else:
        print("Updated MANIFEST.md and supporting indexes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
