---
build_number: "001"
skill_id: "epcb.domain.skill_id"
name: "skill-name"
description: "Use when this governed workflow should turn inputs into reliable outputs."
trigger_keywords: "use workflow, create output, validate process"
owner: "EPCB"
status: "active"
created_at: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---

# Index

| Field | Detail |
|-------|--------|
| Trigger | Concise activation condition |
| Input | Required source material |
| Output | Governed deliverable |
| Key Steps | Read, decide, execute, validate |

---

# Objective

Define the reusable purpose.

---

# Trigger

Use this skill when:

- The workflow condition is present.

---

# Do Not Use When

- The request belongs to another skill or is not reusable.

---

# Required Inputs

1. Required input.

---

# Optional Inputs

1. Optional input.

---

# Outputs

1. Expected output.

---

# Support Layers

- Put detailed references in `references/`.
- Put deterministic helpers in `scripts/`.
- Put reusable output resources in `assets/`.

---

# Procedure

1. Read inputs.
2. Apply decision rules.
3. Produce outputs.
4. Validate.

---

# Decision Logic

| Condition | Action |
|-----------|--------|
| Required fact is missing | Ask one concise question or document assumption |

---

# Validation

1. Output satisfies the objective.
2. Required inputs are accounted for.
3. Failure modes are handled.

---

# RALPH Loop

Run at most two passes: reaffirm requirements, audit alignment, lock layout, purge provenance problems, then halt or hand off.

---

# Rules

- Keep the skill concise.
- Move detailed examples to support files.

---

# Failure Modes

| Failure | Recovery |
|---------|----------|
| Source is insufficient | Ask one targeted question |

---

# Dependencies

- AISkills validation scripts.

---

# Assumptions

- Repo-backed mode is preferred when available.

---

# Change Log

## V001
- Initial governed skill version.
