---
build_number: "001"
skill_id: "epcb.template.skill"
name: "skill-template"
description: "TODO: Replace with a one-line functional summary of what this skill does."
trigger_keywords: "TODO: replace, with, comma-separated, trigger terms"
owner: "EPCB"
status: "draft"
created_at: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---

# Index

| Field       | Detail                                                     |
|-------------|------------------------------------------------------------|
| Trigger     | TODO: one-line condition for loading this skill            |
| Input       | TODO: key inputs, comma-separated                          |
| Output      | TODO: key outputs, comma-separated                         |
| Key Steps   | TODO: short verb phrase sequence                           |
| Fails When  | TODO: primary failure condition                            |
| Name Rule   | Folder uses kebab-case; skill_id uses epcb.<domain>.<name> |

---

# Objective

TODO: State what this skill accomplishes, when it is useful, and what output it produces. This paragraph must be executable without reading the source chat or any hidden context.

# Trigger

Use this skill when:

- TODO: Name the first concrete situation where this skill applies.
- TODO: Name the second concrete situation where this skill applies.
- TODO: Name the repeatable workflow signal that should trigger this skill.

# Do Not Use When

- TODO: Name a nearby request that should not use this skill.
- TODO: Name a missing-input or wrong-scope condition.

# Required Inputs

1. TODO: Required input with type or source.
2. TODO: Required input with type or source.

# Optional Inputs

1. TODO: Optional input with default or fallback.

# Outputs

1. TODO: Primary output artifact or decision.
2. TODO: Secondary output artifact or decision.

# Support Layers

- Put long examples, source notes, rubrics, and background context in `references/`.
- Put templates, images, exports, fixtures, and other non-code artifacts in `assets/`.
- Put executable helpers, parsers, generators, or validation utilities in `scripts/`.
- Keep `skill.md` focused on activation, inputs, outputs, procedure, validation, dependencies, and failure modes.

# Procedure

## 1. TODO: First Major Step

1.1 TODO: Write an imperative action.
1.2 TODO: Validate the result of the action.

## 2. TODO: Second Major Step

2.1 TODO: Write an imperative action.
2.2 TODO: Handle the main branch or decision point.

## 3. TODO: Produce Output

3.1 TODO: Format the final output.
3.2 TODO: Confirm the output satisfies validation.

# Decision Logic

- IF TODO condition is true, THEN TODO action.
- IF required input is missing, THEN request it before continuing.

# Validation

The result is valid when:

1. TODO: Concrete validation condition.
2. TODO: Concrete validation condition.
3. All referenced support files exist or are listed as planned support files.

# Rules

- TODO: Hard rule or constraint.
- Do not rely on hidden chat context.
- Do not put large raw examples directly in `skill.md`.

# Failure Modes

- TODO failure mode: TODO recovery action.
- Missing required input: request the missing input and stop.

# Dependencies

- TODO: Required tool, file, skill, or external system.
- None if this skill has no external dependencies.

# Assumptions

- TODO: State any assumption a first-time executor must know.

# Change Log

See CHANGELOG.md
