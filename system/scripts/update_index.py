from pathlib import Path

ROOT = Path(".")
SKILLS = ROOT / "skills"
REFERENCES = ROOT / "references"
ASSETS = ROOT / "assets"
VENDOR = ROOT / "vendor"
INDEXES = ROOT / "system" / "indexes"

INDEXES.mkdir(parents=True, exist_ok=True)

def read_meta(skill_file: Path):
    meta = {
        "skill_id": "",
        "name": "",
        "status": "",
        "build_number": "",
        "description": "",
    }
    if not skill_file.exists():
        return meta

    for line in skill_file.read_text().splitlines():
        if line.startswith("skill_id:"):
            meta["skill_id"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("name:"):
            meta["name"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("status:"):
            meta["status"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("build_number:"):
            meta["build_number"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("description:"):
            meta["description"] = line.split(":", 1)[1].strip().strip('"')
    return meta

# skill-master-index.md
skill_lines = [
    "# SKILL MASTER INDEX",
    "",
    "| Skill ID | Name | Build | Status | Path | Description |",
    "|----------|------|-------|--------|------|-------------|",
]

if SKILLS.exists():
    for skill_dir in sorted([p for p in SKILLS.iterdir() if p.is_dir()]):
        builds = sorted([p for p in skill_dir.iterdir() if p.is_dir() and p.name.startswith("V")])
        if not builds:
            continue
        latest = builds[-1]
        skill_file = latest / "skill.md"
        meta = read_meta(skill_file)
        skill_lines.append(
            f"| {meta['skill_id'] or skill_dir.name} | "
            f"{meta['name'] or skill_dir.name} | "
            f"{meta['build_number'] or latest.name} | "
            f"{meta['status'] or 'active'} | "
            f"{latest.as_posix()} | "
            f"{meta['description'] or ''} |"
        )

(INDEXES / "skill-master-index.md").write_text("\n".join(skill_lines) + "\n")

# reference-index.md
ref_lines = [
    "# REFERENCE INDEX",
    "",
    "| Path |",
    "|------|",
]
if REFERENCES.exists():
    for p in sorted([x for x in REFERENCES.rglob("*") if x.is_file()]):
        ref_lines.append(f"| {p.as_posix()} |")
(INDEXES / "reference-index.md").write_text("\n".join(ref_lines) + "\n")

# asset-index.md
asset_lines = [
    "# ASSET INDEX",
    "",
    "| Path |",
    "|------|",
]
if ASSETS.exists():
    for p in sorted([x for x in ASSETS.rglob("*") if x.is_file()]):
        asset_lines.append(f"| {p.as_posix()} |")
(INDEXES / "asset-index.md").write_text("\n".join(asset_lines) + "\n")

# vendor-index.md
vendor_lines = [
    "# VENDOR INDEX",
    "",
    "| Path |",
    "|------|",
]
if VENDOR.exists():
    for p in sorted([x for x in VENDOR.rglob("*") if x.is_file()]):
        vendor_lines.append(f"| {p.as_posix()} |")
(INDEXES / "vendor-index.md").write_text("\n".join(vendor_lines) + "\n")

print("Updated all indexes")