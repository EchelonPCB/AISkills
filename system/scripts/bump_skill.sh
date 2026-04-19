#!/bin/bash
set -e

SKILL_FOLDER=$1
TODAY=$(date +%F)
BASE="skills/$SKILL_FOLDER"

if [ -z "$SKILL_FOLDER" ]; then
  echo "Usage: ./system/scripts/bump_skill.sh <skill-folder>"
  exit 1
fi

if [ ! -d "$BASE" ]; then
  echo "Skill folder not found: $BASE"
  exit 1
fi

LATEST=$(find "$BASE" -maxdepth 1 -type d -name 'V*' | sed 's|.*/||' | sort -V | tail -n 1)
LATEST_NUM=${LATEST#V}
NEXT_NUM=$(printf "%03d" $((10#$LATEST_NUM + 1)))
NEXT="V$NEXT_NUM"

mkdir -p "$BASE/$NEXT"
cp "$BASE/$LATEST/skill.md" "$BASE/$NEXT/skill.md"

python3 - <<PY
from pathlib import Path
import re
p = Path("$BASE/$NEXT/skill.md")
text = p.read_text()
text = re.sub(r'build_number:\s*"\d+"', 'build_number: "$NEXT_NUM"', text, count=1)
text = re.sub(r'last_updated:\s*"[^"]*"', 'last_updated: "$TODAY"', text, count=1)
p.write_text(text)
PY

mkdir -p "$BASE/archived"
for d in "$BASE"/V*; do
  name=$(basename "$d")
  if [ "$name" != "$NEXT" ]; then
    rm -rf "$BASE/archived/$name"
    mv "$d" "$BASE/archived/$name"
  fi
done

cat >> "$BASE/CHANGELOG.md" <<EOF
## $NEXT
- Bumped from $LATEST on $TODAY
- [Add change summary here]

EOF

python3 system/scripts/update_index.py
python3 system/scripts/log_run.py "$SKILL_FOLDER" "Bumped from $LATEST to $NEXT"

echo "Bumped $SKILL_FOLDER to $NEXT"