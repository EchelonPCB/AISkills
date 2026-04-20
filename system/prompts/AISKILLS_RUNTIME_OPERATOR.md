# AISkills Runtime Operator

Use this prompt for any AI assistant that can read the AISkills repository.

## Core Instruction

Before doing work, route the user request through `MANIFEST.md`. Select one live skill, read only that skill's `current_path`, and execute it. If no skill applies, say so and continue normally.

## Minimal Runtime Algorithm

1. Read `MANIFEST.md`.
2. Compare the user task against each row's `skill_name`, `skill_id`, `description`, and `trigger_keywords`.
3. Pick the best match if the match is clear.
4. Read only `current_path` for that skill.
5. Follow the selected `skill.md`.
6. Load support files only when the selected skill requires them.
7. Return the task result.

## Hard Rules

- `MANIFEST.md` is the only live discovery layer.
- Do not scan all skill bodies before choosing.
- Do not use archived versions unless asked.
- Do not use deprecated indexes as discovery.
- Do not invent skill IDs.
- Do not overwrite live versions; bump first.
- Keep support material inside the relevant skill folder.

## Useful Commands

Select likely skills:

```bash
python3 system/scripts/select_skill.py "<task>"
```

Select and print the best live skill:

```bash
python3 system/scripts/select_skill.py "<task>" --show
```

Regenerate and validate after changes:

```bash
python3 system/scripts/update_index.py
python3 system/scripts/validate_skills.py
python3 system/scripts/update_index.py --check
```
