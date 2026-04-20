# CLAUDE.md

Claude should operate this repository through AISkills runtime routing.

## Start Here

1. Read `MANIFEST.md`.
2. Select the best matching live skill by `description` and `trigger_keywords`.
3. Read only the selected row's `current_path`.
4. Execute that `skill.md`.
5. Load support files only when the selected skill requires them.

For full Claude project instructions, read:

```text
system/prompts/AISKILLS_CLAUDE_OPERATOR.md
```

## Fast Selector

When shell access is available:

```bash
python3 system/scripts/select_skill.py "<user task>"
```

To print the selected live skill:

```bash
python3 system/scripts/select_skill.py "<user task>" --show
```

## Hard Rules

- `MANIFEST.md` is the only skill discovery layer.
- Do not read all skill files before choosing.
- Do not use archived versions unless asked.
- Do not use deprecated discovery files.
- Do not create non-`epcb.*` skill IDs.
- Do not overwrite live skill versions; bump first.
- After repo changes, run index and validation checks.
