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

## AI Runtime Usage
AISkills becomes a runtime when an AI uses `MANIFEST.md` as a routing table instead of reading the whole repository.

Runtime order:

1. Read `MANIFEST.md`.
2. Select one relevant live skill by `description` and `trigger_keywords`.
3. Read only the selected row's `current_path`.
4. Execute that `skill.md`.
5. Load skill-local `references/`, `assets/`, or `scripts/` only when needed.
6. If no skill applies, say no AISkills skill applies and proceed normally.

Do not ask an AI to read the entire repo as its first step. That wastes tokens and increases the chance it will use archived or deprecated material.

### Claude Project / Cowork Setup
Use this short repo entrypoint when Claude supports project files or repo guidance:

```text
CLAUDE.md
```

Use this fuller prompt as Claude project or cowork instructions:

```text
system/prompts/AISKILLS_CLAUDE_OPERATOR.md
```

The Claude operator prompt tells Claude to:

- treat `MANIFEST.md` as the only discovery layer
- load only one live `skill.md` by default
- avoid archived versions unless explicitly asked
- use skill-local support files only after selecting a skill
- run index and validation commands after repo changes when shell access is available

If Claude cannot run shell commands, it should still follow the same routing logic manually by reading `MANIFEST.md` and then the selected `current_path`.

### Runtime Selector
Use the selector to route tasks without scanning every skill body:

```bash
python3 system/scripts/select_skill.py "turn this lab chat into a formal engineering record"
```

To print the best matching live skill after selection:

```bash
python3 system/scripts/select_skill.py "turn this lab chat into a formal engineering record" --show
```

For machine-readable output:

```bash
python3 system/scripts/select_skill.py "turn this lab chat into a formal engineering record" --json
```

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

Stage a higher-risk mutated skill from two or more parent skills:

```bash
python3 system/scripts/stage_mutation.py chat-to-skill skill-mutation --name chat-mutation-lab --goal "combine skill drafting with mutation validation"
```

Promote an approved staged mutation into the live `skills/` folder:

```bash
python3 system/scripts/promote_mutation.py chat-mutation-lab --approve
```

The matching shell aliases are `m` for staging and `mup` for promotion when your `.zshrc` shortcuts are installed.

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

## Templates
Templates live in `system/templates/` and are starting points, not live skills.

- `SKILL_TEMPLATE.md`: copied by `new_skill.sh` into `skills/<skill>/V001/skill.md`. It intentionally contains `TODO:` markers, so a new scaffold must be authored before `validate_skills.py` passes.
- `CHANGELOG_TEMPLATE.md`: reference shape for skill changelogs. The scripts generate real changelogs automatically.
- `REFERENCE_TEMPLATE.md`: starting point for files placed in a skill-local `references/` folder.
- `MASTER_PROMPT_OPTIMIZER_SKILL.MD`: legacy/template prompt-optimization skill shape. Use it as reference material unless it is promoted into `skills/` as a governed skill.

Do not treat templates as discoverable skills. Only `MANIFEST.md` controls live skill discovery.

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

## Current Alias And Command Quick Reference

This section reflects the current `.zshrc` shortcuts and the current script argument formats. Prefer this section when it conflicts with older preserved command notes above.

### Start A Skill Session

Expected shell setup:

```bash
source ~/.zshrc
skroot
```

Expected result:

```text
Terminal is in ~/Desktop/AISkills and the sk* aliases are available.
```

### Create A New Skill

Full command format:

```bash
./system/scripts/new_skill.sh <skill-name> [domain]
```

Alias format:

```bash
sknew <skill-name> [domain]
n <skill-name> [domain]
```

Example:

```bash
sknew donor-intake triage
```

Expected generated format:

```text
skills/donor-intake/
  CURRENT
  V001/skill.md
  archived/.gitkeep
  references/.gitkeep
  assets/.gitkeep
  scripts/.gitkeep
  CHANGELOG.md
```

Expected generated frontmatter pattern:

```yaml
skill_id: "epcb.triage.donor_intake"
name: "donor-intake"
```

After creating a new skill, edit `skills/<skill-name>/V001/skill.md` to replace scaffold content, then run:

```bash
skhealth
```

### Stage A Skill Mutation

Use mutation staging when combining two or more existing skills into a higher-risk candidate skill.

Full command format:

```bash
python3 system/scripts/stage_mutation.py <parent-skill-1> <parent-skill-2> [parent-skill-3] --name <mutation-name> --goal "one sentence goal"
```

Alias format:

```bash
skmutate <parent-skill-1> <parent-skill-2> --name <mutation-name> --goal "one sentence goal"
m <parent-skill-1> <parent-skill-2> --name <mutation-name> --goal "one sentence goal"
```

Example:

```bash
m chat-to-skill skill-mutation --name cts-mutation-lab --goal "combine skill drafting with mutation validation"
```

Expected generated format:

```text
workspace/mutations/cts-mutation-lab/
  CURRENT
  V001/skill.md
  parents/<parent-skill>/<V###>/skill.md
  references/mutation-brief.md
  references/parent-map.md
  references/merge-notes.md
  references/promotion-checklist.md
  archived/
  assets/
  scripts/
  CHANGELOG.md
```

Use dry run when you only want to confirm parent resolution:

```bash
m chat-to-skill skill-mutation --name cts-mutation-lab --goal "combine skill drafting with mutation validation" --dry-run
```

### Promote An Approved Mutation

Promotion moves a staged mutation into the live `skills/` folder only after the staged package is complete.

Before promotion, `workspace/mutations/<mutation-name>/references/promotion-checklist.md` must include:

```text
Recommendation: promote
```

Full command format:

```bash
python3 system/scripts/promote_mutation.py <mutation-name> --approve
```

Alias format:

```bash
skpromotemutation <mutation-name> --approve
mup <mutation-name> --approve
```

Example:

```bash
mup cts-mutation-lab --approve
```

Expected promoted format:

```text
skills/cts-mutation-lab/
  CURRENT
  V001/skill.md
  archived/.gitkeep
  references/.gitkeep
  assets/.gitkeep
  scripts/.gitkeep
  CHANGELOG.md
```

Promotion also runs:

```bash
python3 system/scripts/update_index.py
python3 system/scripts/validate_skills.py
python3 system/scripts/update_index.py --check
```

Bump a staged mutation version when you want to preserve the current candidate and keep iterating:

```bash
python3 system/scripts/bump_mutation.py <mutation-name> "reason for the staged version bump"
```

### Alias Categories

Repo navigation:

```bash
skroot='cd ~/Desktop/AISkills'
skcode='code .'
```

Skill lifecycle:

```bash
sknew='./system/scripts/new_skill.sh'
skbump='./system/scripts/bump_skill.sh'
skarch='./system/scripts/archive_skill.sh'
```

Mutation staging and promotion:

```bash
skmutate='python3 ~/Desktop/AISkills/system/scripts/stage_mutation.py'
skpromotemutation='python3 ~/Desktop/AISkills/system/scripts/promote_mutation.py'
```

Indexing and validation:

```bash
skindex='python3 ./system/scripts/update_index.py'
skcheck='python3 ./system/scripts/update_index.py --check'
skvalidate='python3 ./system/scripts/validate_skills.py'
skhealth='python3 ./system/scripts/update_index.py && python3 ./system/scripts/validate_skills.py && python3 ./system/scripts/update_index.py --check'
```

Automation:

```bash
skwatch='./system/scripts/watch_indexes.sh'
```

Short forms:

```bash
n='sknew'
b='skbump'
i='skindex'
c='skcheck'
v='skvalidate'
h='skhealth'
a='skarch'
m='skmutate'
mup='skpromotemutation'
```
