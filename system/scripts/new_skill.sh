#!/bin/bash
set -e

SKILL_FOLDER=$1
SKILL_ID=$2
NAME=$3
TODAY=$(date +%F)
BASE="skills/$SKILL_FOLDER"
VERSION="V001"

if [ -z "$SKILL_FOLDER" ] || [ -z "$SKILL_ID" ] || [ -z "$NAME" ]; then
  echo "Usage: ./system/scripts/new_skill.sh <folder> <skill_id> <name>"
  exit 1
fi

if [ -d "$BASE" ]; then
  echo "Skill already exists: $BASE"
  exit 1
fi

mkdir -p "$BASE/$VERSION" "$BASE"/{archived,logs,references,assets}

cp system/templates/SKILL_TEMPLATE.md "$BASE/$VERSION/skill.md"

cat > "$BASE/CHANGELOG.md" <<EOF
# CHANGELOG

## V001
- Created on $TODAY
- Initial skill scaffold

EOF

python3 - <<PY
from pathlib import Path
p = Path("$BASE/$VERSION/skill.md")
text = p.read_text()
text = text.replace('skill_id: "acdc.template.skill"', 'skill_id: "$SKILL_ID"', 1)
text = text.replace('name: "skill-template"', 'name: "$NAME"', 1)
text = text.replace('created_at: "YYYY-MM-DD"', 'created_at: "$TODAY"', 1)
text = text.replace('last_updated: "YYYY-MM-DD"', 'last_updated: "$TODAY"', 1)
p.write_text(text)
PY

python3 system/scripts/update_index.py
python3 system/scripts/log_run.py "$SKILL_FOLDER" "Created $VERSION"

echo "Created $SKILL_FOLDER"