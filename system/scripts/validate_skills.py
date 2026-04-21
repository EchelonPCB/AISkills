from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from update_index import collect_skills

ROOT = Path(".")
SKILLS = ROOT / "skills"
TOP_LEVEL_SUPPORT_DIRS = ("references", "assets")
MAX_SKILL_LINES = 800
MIN_DESCRIPTION_CHARS = 20
REQUIRED_PHRASES = ("Use when", "Use this skill when")
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
FORBIDDEN_ARTIFACTS = (
    ":contentReference",
    "oaicite",
    "[Add change summary here]",
    "Initial governed skill scaffold; replace TODOs",
    "replace TODOs before validation",
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


def frontmatter_lines(text: str):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return []
    try:
        end = lines.index("---", 1)
    except ValueError:
        return []
    return lines[1:end]


def top_level_heading_lines(text: str):
    return [
        (index, line.strip())
        for index, line in enumerate(text.splitlines(), start=1)
        if line.startswith("# ")
    ]


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
    documents_forbidden_artifacts = record.name == "chat-to-skill"

    for snippet in PLACEHOLDER_SNIPPETS:
        if snippet in text:
            errors.append(
                f"{record.current_path.as_posix()} still contains template placeholder text: {snippet!r}"
            )

    for artifact in FORBIDDEN_ARTIFACTS:
        if artifact in text and not documents_forbidden_artifacts:
            errors.append(
                f"{record.current_path.as_posix()} contains forbidden source/scaffold artifact: {artifact!r}"
            )

    frontmatter = frontmatter_lines(text)
    if not frontmatter:
        errors.append(f"{record.current_path.as_posix()} must start with YAML frontmatter")
    else:
        present_keys = [
            line.split(":", 1)[0].strip()
            for line in frontmatter
            if ":" in line and not line.lstrip().startswith("#")
        ]
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in present_keys:
                errors.append(f"{record.current_path.as_posix()} frontmatter is missing {key}")
        required_positions = [
            present_keys.index(key)
            for key in REQUIRED_FRONTMATTER_KEYS
            if key in present_keys
        ]
        if required_positions != sorted(required_positions):
            errors.append(
                f"{record.current_path.as_posix()} frontmatter keys must keep required metadata order"
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

    headings = top_level_heading_lines(text)
    heading_positions = {heading: line_no for line_no, heading in headings}
    last_position = 0
    for section in REQUIRED_SECTIONS:
        position = heading_positions.get(section)
        if position is None:
            errors.append(f"{record.current_path.as_posix()} must include {section}")
            continue
        if position < last_position:
            errors.append(
                f"{record.current_path.as_posix()} has {section} out of required section order"
            )
        last_position = max(last_position, position)
    return errors


def validate_changelog(record):
    errors = []
    skill_dir = record.current_path.parents[1]
    changelog = skill_dir / "CHANGELOG.md"
    documents_forbidden_artifacts = record.name == "chat-to-skill"
    if not changelog.exists():
        return [f"{skill_dir.as_posix()} is missing CHANGELOG.md"]

    text = changelog.read_text()
    if f"## {record.current_version}" not in text:
        errors.append(
            f"{changelog.as_posix()} must include an entry for {record.current_version}"
        )
    for artifact in FORBIDDEN_ARTIFACTS:
        if artifact in text and not documents_forbidden_artifacts:
            errors.append(
                f"{changelog.as_posix()} contains forbidden source/scaffold artifact: {artifact!r}"
            )
    return errors


def validate_manifest_overlap(records):
    errors = []
    seen_names = {}
    seen_keyword_sets = {}

    for record in records:
        normalized_name = record.name.replace("-", "_")
        if normalized_name in seen_names:
            errors.append(
                f"{record.current_path.as_posix()} has near-duplicate skill name with {seen_names[normalized_name]}"
            )
        seen_names[normalized_name] = record.current_path.as_posix()

        keywords = frozenset(
            keyword.strip().lower()
            for keyword in record.trigger_keywords.split(",")
            if keyword.strip()
        )
        if keywords and keywords in seen_keyword_sets:
            errors.append(
                f"{record.current_path.as_posix()} duplicates trigger_keywords from {seen_keyword_sets[keywords]}"
            )
        seen_keyword_sets[keywords] = record.current_path.as_posix()
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
    errors.extend(validate_manifest_overlap(records))

    for record in records:
        errors.extend(validate_trigger_keywords(record))
        errors.extend(validate_skill_file(record))
        errors.extend(validate_support_links(record))
        errors.extend(validate_changelog(record))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Skills are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
