# Repo-Backed Mode

Use this mode when the AISkills repo, MCP tools, `MANIFEST.md`, or `system/indexes/skill-index.json` is available.

## Discovery

1. Prefer MCP `list_skills` or `select_skill`.
2. If MCP is unavailable, inspect `MANIFEST.md` or `system/indexes/skill-index.json`.
3. Read only the one live skill body selected for an amendment.
4. Do not scan every skill body as duplicate detection.

## Classification

Classify the source before writing:

- `new_skill`: no manifest row covers the reusable workflow.
- `amendment`: an existing skill covers the workflow but needs a behavior or structure change.
- `reference`: source is detailed background for an existing skill.
- `asset`: source is a reusable template, image, data file, or output resource.
- `script`: source is deterministic executable logic.
- `reject`: source is not reusable or conflicts with system boundaries.
- `insufficient`: missing facts block identity, runtime target, destructive scope, or validation authority.

## Writes

- For `new_skill`, run `system/scripts/new_skill.sh <folder> <domain>`.
- For `amendment`, run `system/scripts/bump_skill.sh <folder> "<reason>"` before editing.
- Never overwrite an existing live `V###/skill.md` for a material change.
- If a generated version needs correction after insertion, preserve it in `archived/V###` and apply the correction in a bumped version.

## Validation

Run these before reporting completion:

```bash
python3 system/scripts/update_index.py
python3 system/scripts/validate_skills.py
python3 system/scripts/update_index.py --check
python3 system/scripts/mcp_gateway.py validate-repo
```

Repo-backed live skills must not contain offline-only assumptions such as `Manifest unavailable; duplicate check not performed.`
