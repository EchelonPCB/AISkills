# AISkills Runtime Operator

Use this prompt for any AI assistant that can read the AISkills repository.

## Core Instruction

Before doing work, route the user request through `MANIFEST.md`. Select one live skill, read only that skill's `current_path`, and execute it. If no skill applies, say so and continue normally.

When MCP tools are available, prefer the governed MCP tools over raw file reads or direct shell commands.

Preferred MCP tools:

- `list_skills`
- `select_skill`
- `read_skill`
- `validate_repo`
- `list_mutations`
- `validate_mutation`

## Minimal Runtime Algorithm

1. Read `system/indexes/skill-index.json` when available; otherwise read `MANIFEST.md`.
2. Compare the user task against each row's `skill_name`, `skill_id`, `description`, and `trigger_keywords`.
3. Pick the best match if the match is clear.
4. Read only `current_path` for that skill.
5. Follow the selected `skill.md`.
6. Load support files only when the selected skill requires them.
7. Return the task result.

If the match is weak or ambiguous, inspect top candidates or ask for clarification before loading a skill.

## Hard Rules

- `MANIFEST.md` is the canonical human-readable discovery layer.
- `system/indexes/skill-index.json` is the canonical machine-readable mirror.
- Do not scan all skill bodies before choosing.
- Do not use archived versions unless asked.
- Do not use deprecated indexes as discovery.
- Do not invent skill IDs.
- Do not overwrite live versions; bump first.
- Keep support material inside the relevant skill folder.
- Use `skill-mutation` and `workspace/mutations/` for any two-or-more-skill mutation.
- Do not promote staged mutations, archive skills, delete files, commit, or push without explicit human approval.
- Run at most two validation repair passes before reporting blockers.
- Do not create `VP###`, `production/`, or alternate production version folders.

## Useful Commands

Select likely skills:

```bash
python3 system/scripts/select_skill.py "<task>" --require-confident
```

Select and print the best live skill:

```bash
python3 system/scripts/select_skill.py "<task>" --show --require-confident
```

Regenerate and validate after changes:

```bash
python3 system/scripts/update_index.py
python3 system/scripts/validate_skills.py
python3 system/scripts/update_index.py --check
```

MCP staging gateway:

```bash
python3 system/scripts/mcp_gateway.py select-skill "<task>"
python3 system/scripts/mcp_gateway.py validate-repo
python3 system/scripts/mcp_gateway.py validate-mutation <mutation-name>
```
