---
build_number: "001"
skill_id: "epcb.template.skill"
name: "skill-template"
description: "Base template for all skills"
trigger_keywords: "run, process, create, validate, workflow"
owner: "EPCB"
status: "draft"
created_at: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---

# Objective
Define the purpose of the skill.

# Trigger
Use this skill when the user request matches the trigger keywords and the workflow is repeatable.

# Inputs
1. Required inputs
2. Optional inputs

# Outputs
1. Expected outputs

# Support Layers
- Put long examples and source notes in `references/`.
- Put templates, images, exports, fixtures, and other artifacts in `assets/`.
- Put executable helpers in `scripts/`.
- Keep `skill.md` self-contained for core execution, but avoid bloating it with large support material.

# Procedure

1. **Step 1: Define Objective**
   1.1 Restate the problem clearly
   1.2 Confirm constraints

2. **Step 2: Process Inputs**
   2.1 Validate inputs
   2.2 Normalize data

3. **Step 3: Execute Logic**
   3.1 Apply core logic
   3.2 Handle edge cases

4. **Step 4: Output Results**
   4.1 Format output
   4.2 Validate correctness

# Decision Logic
- IF input invalid → STOP
- IF uncertainty → FAIL SAFE

# Logging
- Log input
- Log output
- Log errors

# Change Log
See CHANGELOG.md
