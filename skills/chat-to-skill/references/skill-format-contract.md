# Skill Format Contract

Generated AISkills skill files must follow this contract.

## Frontmatter

Required keys, in this order:

1. `build_number`
2. `skill_id`
3. `name`
4. `description`
5. `trigger_keywords`
6. `owner`
7. `status`
8. `created_at`
9. `last_updated`

Rules:

- `skill_id` starts with `epcb.` and uses dot-separated lowercase underscore tokens.
- `trigger_keywords` is one quoted, comma-separated line with at least three entries.
- Description is one line and should be discovery-friendly.
- Folder names use kebab-case. Frontmatter names may match the folder unless the domain already has a stronger convention.

## Required Sections

Use these level-one headings in this order:

1. `# Index`
2. `# Objective`
3. `# Trigger`
4. `# Do Not Use When`
5. `# Required Inputs`
6. `# Optional Inputs`
7. `# Outputs`
8. `# Support Layers`
9. `# Procedure`
10. `# Decision Logic`
11. `# Validation`
12. `# RALPH Loop`
13. `# Rules`
14. `# Failure Modes`
15. `# Dependencies`
16. `# Assumptions`
17. `# Change Log`

## Size

There is no fixed word or character limit. Keep the live skill body under 500 lines when practical, and never exceed the AISkills validator limit. Move detailed examples, domain tables, transcripts, command catalogs, and long procedures to support files.
