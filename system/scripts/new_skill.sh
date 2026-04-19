#!/bin/bash
set -e

RAW_NAME=$1
RAW_DOMAIN=${2:-general}
TODAY=$(date +%F)

if [ -z "$RAW_NAME" ]; then
  echo "Usage: ./system/scripts/new_skill.sh <skill-name> [domain]"
  exit 1
fi

# normalize
SKILL_FOLDER=$(echo "$RAW_NAME" | tr '[:upper:]' '[:lower:]' | tr ' _' '--' | sed -E 's/[^a-z0-9-]+/-/g; s/-+/-/g; s/^-|-$//g')
DOMAIN=$(echo "$RAW_DOMAIN" | tr '[:upper:]' '[:lower:]' | tr ' -' '__' | sed -E 's/[^a-z0-9_]+/_/g; s/_+/_/g; s/^_|_$//g')
NAME="$SKILL_FOLDER"
SKILL_ID_NAME=$(echo "$SKILL_FOLDER" | tr '-' '_')
SKILL_ID="epcb.$DOMAIN.$SKILL_ID_NAME"

if [ -z "$SKILL_FOLDER" ] || [ -z "$DOMAIN" ]; then
  echo "Skill name and domain must contain at least one letter or number"
  exit 1
fi

BASE="skills/$SKILL_FOLDER"
VERSION="V001"

if [ -d "$BASE" ]; then
  echo "Skill already exists: $BASE"
  exit 1
fi

mkdir -p "$BASE/$VERSION" "$BASE"/{archived,logs,references,assets,scripts}
echo "$VERSION" > "$BASE/CURRENT"
touch "$BASE/scripts/.gitkeep"

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

text = text.replace('skill_id: "epcb.template.skill"', 'skill_id: "$SKILL_ID"', 1)
text = text.replace('name: "skill-template"', 'name: "$NAME"', 1)
text = text.replace('created_at: "YYYY-MM-DD"', 'created_at: "$TODAY"', 1)
text = text.replace('last_updated: "YYYY-MM-DD"', 'last_updated: "$TODAY"', 1)

p.write_text(text)
PY

python3 system/scripts/update_index.py
python3 system/scripts/log_run.py "$SKILL_FOLDER" "Created $VERSION"

echo "Created $SKILL_FOLDER with ID $SKILL_ID"
