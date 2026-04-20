from pathlib import Path
import re
import sys

from update_index import collect_skills

ROOT = Path(".")
SKILLS = ROOT / "skills"
TOP_LEVEL_SUPPORT_DIRS = ("references", "assets")
MAX_SKILL_LINES = 800
MIN_DESCRIPTION_CHARS = 20
REQUIRED_PHRASES = ("Use when", "Use this skill when")
PLACEHOLDER_SNIPPETS = (
    'description: "Base template for all skills"',
    'trigger_keywords: "run, process, create, validate, workflow"',
    "TODO:",
    "Define the purpose of the skill.",
    "1. Required inputs",
    "2. Optional inputs",
    "1. Expected outputs",
    "Step 1: Define Objective",
    "Step 2: Process Inputs",
    "Step 3: Execute Logic",
    "Step 4: Output Results",
)


def meaningful_files(path: Path):
    if not path.exists():
        return []
    return sorted(
        p
        for p in path.rglob("*")
        if p.is_file() and p.name not in {".DS_Store", ".gitkeep"}
    )


def skill_text(path: Path):
    return path.read_text()


def frontmatter_value(text: str, key: str):
    prefix = f"{key}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def validate_trigger_keywords(record):
    errors = []
    keywords = [item.strip() for item in record.trigger_keywords.split(",") if item.strip()]

    if len(keywords) < 3:
        errors.append(
            f"{record.current_path.as_posix()} trigger_keywords must contain at least 3 comma-separated entries"
        )
    if record.trigger_keywords.strip() == record.name:
        errors.append(
            f"{record.current_path.as_posix()} trigger_keywords must not only repeat the skill name"
        )
    if not any(keyword.split()[0].endswith(("e", "y", "t")) or " " in keyword for keyword in keywords):
        errors.append(
            f"{record.current_path.as_posix()} trigger_keywords should include task verbs or action phrases"
        )
    return errors


def validate_skill_file(record):
    errors = []
    text = skill_text(record.current_path)
    description = record.description.strip()

    for snippet in PLACEHOLDER_SNIPPETS:
        if snippet in text:
            errors.append(
                f"{record.current_path.as_posix()} still contains template placeholder text: {snippet!r}"
            )

    if len(description) < MIN_DESCRIPTION_CHARS:
        errors.append(
            f"{record.current_path.as_posix()} description is too short for reliable discovery"
        )
    if "\n" in description:
        errors.append(f"{record.current_path.as_posix()} description must be one line")
    if len(text.splitlines()) > MAX_SKILL_LINES:
        errors.append(
            f"{record.current_path.as_posix()} is over {MAX_SKILL_LINES} lines; move examples to references/ or assets/"
        )
    if not any(phrase in text for phrase in REQUIRED_PHRASES):
        errors.append(
            f"{record.current_path.as_posix()} must include a 'Use when' or 'Use this skill when' section"
        )
    if "# Failure Modes" not in text:
        errors.append(f"{record.current_path.as_posix()} must include # Failure Modes")
    if "# Dependencies" not in text:
        errors.append(f"{record.current_path.as_posix()} must include # Dependencies")
    if "# Assumptions" not in text:
        errors.append(f"{record.current_path.as_posix()} must include # Assumptions")
    return errors


def validate_support_links(record):
    errors = []
    text = skill_text(record.current_path)
    skill_dir = record.current_path.parents[1]

    for match in re.finditer(r"(?<!system/)(?<!skills/[A-Za-z0-9_-]/)\b(?:references|assets|scripts)/[A-Za-z0-9_./-]+", text):
        rel = match.group(0).rstrip(").,")
        target = skill_dir / rel
        if not target.exists():
            errors.append(
                f"{record.current_path.as_posix()} references missing support file {target.as_posix()}"
            )
    return errors


def validate_top_level_support():
    errors = []
    for dirname in TOP_LEVEL_SUPPORT_DIRS:
        path = ROOT / dirname
        files = meaningful_files(path)
        if files:
            joined = ", ".join(p.as_posix() for p in files)
            errors.append(
                f"Top-level {dirname}/ contains support files ({joined}); move skill-specific support into skills/<skill>/{dirname}/"
            )
    return errors


def main():
    records, errors = collect_skills()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    errors.extend(validate_top_level_support())

    for record in records:
        errors.extend(validate_trigger_keywords(record))
        errors.extend(validate_skill_file(record))
        errors.extend(validate_support_links(record))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Skills are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
