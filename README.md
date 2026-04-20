# AI Skills System

## Purpose
Centralized modular skill system for EPCB.

## Skill Discovery
`MANIFEST.md` is the only skill discovery file.

Do not use `system/indexes/skill-master-index.md`; it is deprecated and should not be regenerated.

## Skill Structure
Every skill uses this governed folder layout:

```text
skills/<skill-name>/
  CURRENT
  V###/skill.md
  archived/
  references/
  assets/
  scripts/
  CHANGELOG.md
```

Folder names use hyphens. Skill IDs use `epcb.*` with underscores, for example:

```text
epcb.meta.chat_to_skill
```

Support material belongs inside the individual skill folder:

- `references/` for examples, long notes, rubrics, source material, and non-core documentation
- `assets/` for templates, images, exports, fixtures, and other non-code artifacts
- `scripts/` for executable helpers used by that skill

Top-level `references/` and `assets/` are legacy holding areas only. New skill-specific support files should not be added there.

## Rules
- `CURRENT` points to the live `V###` version.
- `MANIFEST.md` contains one row per live skill.
- Archived versions stay inside each skill's `archived/` folder.
- Do not overwrite old live versions.
- Material skill changes use the next version folder.
- Meaningful skill changes should be described in `CHANGELOG.md`.
- Keep `skill.md` focused on activation, inputs, outputs, procedure, and validation.
- Move large examples or support material into the skill-local support folders.

## Commands
Create a skill:

```bash
./system/scripts/new_skill.sh lead-scorer business
```

Bump a skill:

```bash
./system/scripts/bump_skill.sh lead-scorer "Tightened validation rules"
```

Regenerate manifest and supporting file indexes:

```bash
python3 system/scripts/update_index.py
```

Validate governed skill structure and quality:

```bash
python3 system/scripts/validate_skills.py
```

Check generated files without writing:

```bash
python3 system/scripts/update_index.py --check
```

## Version History
`CHANGELOG.md` is the skill's required version history.

- It should say what changed in each `V###` and why that version exists.
- Git history records operational audit details.
- Per-skill `logs/` folders are not required.

For skill version changes, use `bump_skill.sh` with a reason so the changelog stays useful:

```bash
./system/scripts/bump_skill.sh chat-to-skill "Added apply-mode guardrails for old chat extraction"
```

Do not put routine validation or index regeneration into `CHANGELOG.md`; record only meaningful skill changes.

Archive a full skill:

```bash
./system/scripts/archive_skill.sh lead-scorer
```

Enable automatic consistency before commits:

```bash
git config core.hooksPath .githooks
```

## Preserved Command Reference
The section below preserves the original README command notes. Some entries may be historical. When this section conflicts with the current doctrine above, prefer the current doctrine.

Historical entries mentioning `sklog`, `log_run.py`, or `skills/<skill>/logs` are obsolete. Use `CHANGELOG.md` plus git history instead.

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

AISkills Command Reference (Categorized)
System Initialization & Bring-Up
Command	When to Run	Purpose
cd ~/Desktop/AISkills	Start of every session	Enter repo root so all scripts work
source ~/.zshrc	New terminal / after edits	Reload aliases (sk* commands)
chmod +x system/scripts/*.sh	First setup / after clone	Ensure scripts are executable
python3 system/scripts/update_index.py	After pull / startup	Rebuild all indexes
./system/scripts/watch_indexes.sh	Optional (background)	Auto-update indexes on file changes
code .	Start of work session	Open repo in VS Code
Skill Lifecycle (Core Usage)

Command	When to Run	Purpose
sknew <folder> <skill_id> <name>	Creating a new skill	Scaffold a new skill with structure
skbump <skill>	Updating a skill	Create new version, archive old, update changelog
skarch <skill>	Retiring a skill	Move entire skill to vendor archive
sklog <skill> "message"	Any meaningful action	Log actions to skill logs
skindex	After structural changes	Rebuild indexes (manual trigger)

Validation & Testing Command	When to Run	Purpose
tree -L 2	After changes	Inspect folder structure
ls skills/<skill>/logs	After logging	Confirm logs are written
cat skills/<skill>/CHANGELOG.md	After bump	Verify changelog updated
git status	Before commit	Check working tree
python3 system/scripts/log_run.py <skill> "test"	Debugging	Verify logging system

Git Operations Command	When to Run	Purpose
git pull origin main	Start of session	Sync latest changes
git status	Before commit	Review changes
git add .	Before commit	Stage changes
git commit -m "message"	After changes	Save snapshot
git push origin main	After commit	Push to remote
git add system/indexes/*.md	After index rebuild	Stage updated indexes

Automation Controls Command	When to Run	Purpose
./system/scripts/watch_indexes.sh	During active work	Auto-refresh indexes
.git/hooks/post-commit (auto)	On every commit	Rebuild indexes automatically
./system/scripts/bringup.sh	Returning after long gap	Full system initialization
One-Time Setup / Maintenance
Command	When to Run	Purpose
brew install fswatch	Initial setup	Enable file watcher
chmod +x .git/hooks/post-commit	After creating hook	Activate git automation
code ~/.zshrc	Updating aliases	Edit command shortcuts
Recommended Daily Workflow
Step	Command
Enter repo	cd ~/Desktop/AISkills
Sync repo	git pull origin main
Start watcher	./system/scripts/watch_indexes.sh
Open workspace	code .
Work	sknew / skbump / sklog
Rebuild index (if needed)	skindex
Commit	git add . && git commit -m "..."
Push	git push origin main
Recommended “Return After Months” Workflow
Step	Command
Enter repo	cd ~/Desktop/AISkills
Reload shell	source ~/.zshrc
Fix permissions	chmod +x system/scripts/*.sh
Pull latest	git pull origin main
Rebuild indexes	python3 system/scripts/update_index.py
Start watcher	./system/scripts/watch_indexes.sh
Open workspace	code .
Command Categories Summary
Category	Scope
System	Repo health, indexes, scripts
Skills	Create, update, archive, log
Git	Version control and sharing
Terminal	Environment setup
Controls	Automation and watchers
Validation	Debugging and verification

Minimal Workflow Summary
git pull
sknew / skbump / sklog
skindex
git add .
git commit -m "..."
git push

# Stage everything in current directory
git add .
# Stage one specific file
git add README.md
# Stage multiple specific files
git add README.md system/scripts/new_skill.sh
# Stage an entire folder
git add skills/infographic-generator/
# Stage only Python files
git add *.py
# Stage changes interactively (pick parts)
git add -p
# Stage all changes including deletions (alternative)
git add -A
# Stage only modified/deleted (not new files)
git add -u

git pull
Fetch and merge latest changes from remote into your current branch.

sknew <folder> <id> <name>
Create a new skill scaffold (V001) with structure.

skbump <skill>
Create next version, archive previous, update metadata and changelog.

sklog <skill> "msg"
Write a timestamped log entry for that skill.

skindex
Rebuild all system indexes to reflect current repo state.

git commit -m "msg"
Save staged changes as a new commit with a message.

git push
Upload local commits to the remote repository.
