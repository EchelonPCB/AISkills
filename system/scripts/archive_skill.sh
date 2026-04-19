#!/bin/bash

set -e

SKILL_FOLDER=$1

if [ -z "$SKILL_FOLDER" ]; then
  echo "Usage: ./system/scripts/archive_skill.sh <skill-folder>"
  exit 1
fi

SRC="skills/$SKILL_FOLDER"
DEST="vendor/archived-skills"

if [ ! -d "$SRC" ]; then
  echo "Skill folder not found: $SRC"
  exit 1
fi

mkdir -p "$DEST"
mv "$SRC" "$DEST/"

echo "Archived full skill to $DEST/$SKILL_FOLDER"