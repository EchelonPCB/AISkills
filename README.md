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
  logs/
  CHANGELOG.md
```

Folder names use hyphens. Skill IDs use `epcb.*` with underscores, for example:

```text
epcb.meta.chat_to_skill
```

## Rules
- `CURRENT` points to the live `V###` version.
- `MANIFEST.md` contains one row per live skill.
- Archived versions stay inside each skill's `archived/` folder.
- Do not overwrite old live versions.
- Material skill changes use the next version folder.
- Meaningful actions should be logged.

## Commands
Create a skill:

```bash
./system/scripts/new_skill.sh lead-scorer business
```

Bump a skill:

```bash
./system/scripts/bump_skill.sh lead-scorer
```

Regenerate manifest and supporting file indexes:

```bash
python3 system/scripts/update_index.py
```

Check generated files without writing:

```bash
python3 system/scripts/update_index.py --check
```

Log a run:

```bash
python3 system/scripts/log_run.py lead-scorer "Created initial V001 structure"
```

Archive a full skill:

```bash
./system/scripts/archive_skill.sh lead-scorer
```

Enable automatic consistency before commits:

```bash
git config core.hooksPath .githooks
```
