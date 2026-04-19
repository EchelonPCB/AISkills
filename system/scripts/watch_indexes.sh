#!/bin/bash
cd ~/Desktop/AISkills || exit 1
echo "Watching for changes..."
fswatch -o skills references assets vendor | while read; do
  python3 system/scripts/update_index.py
done