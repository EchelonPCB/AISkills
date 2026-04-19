# AI Skills System

## Purpose
Centralized modular skill system for ACDC.

## Structure
- templates/
- scripts/
- archived/
- skill folders

## Rules
- Every update increments build_number
- No overwriting versions
- All changes logged

Key commands from now on

Create a skill:

./system/scripts/new_skill.sh lead-scorer acdc.business.lead_scoring lead-scorer

Bump version:

./system/scripts/bump_skill.sh lead-scorer

Update master index:

python3 ./system/scripts/update_index.py

Log a run:

python3 ./system/scripts/log_run.py lead-scorer "Created initial V001 structure"

Archive full skill:

./system/scripts/archive_skill.sh lead-scorer

Open in VS Code:

code .