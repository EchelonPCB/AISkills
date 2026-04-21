---
build_number: "001"
skill_id: "epcb.meta.skill_mutation"
name: "skill-mutation"
description: "Stage and validate a higher-risk mutated skill by combining two or more parent skills with parent mapping, conflict analysis, RALPH checks, and promotion gates."
trigger_keywords: "mutation, combine, mutate skill, combine skills, skill mutation, merge workflows, staged skill validation, parent skill map"
owner: "EPCB"
status: "active"
created_at: "2026-04-20"
last_updated: "2026-04-20"
---

# Index

| Section | Description |
|--------|-------------|
| Objective | Define mutation staging purpose |
| Trigger | When to apply this skill |
| Do Not Use When | Conditions where mutation is inappropriate |
| Required Inputs | Parent skills and mutation goal |
| Optional Inputs | Helpful validation context |
| Outputs | Staging package and promotion recommendation |
| Support Layers | Parent, conflict, staging, and validation surfaces |
| Procedure | Mutation workflow |
| Decision Logic | Mutation classification and gates |
| Validation | Candidate correctness checks |
| Rules | Non-negotiable mutation constraints |
| Failure Modes | Common mutation breakdowns |
| Dependencies | Required repo files and scripts |
| Assumptions | Operating assumptions |
| Change Log | Version history |

---

# Objective

Create a controlled staging workflow for combining two or more existing skills into a new mutated skill. The mutation must preserve parent traceability, resolve conflicts explicitly, satisfy AISkills formatting rules, and remain staged until validation and human approval support promotion into `skills/<skill-name>/V001/skill.md`.

---

# Trigger

Use this skill when:

- the user wants to combine two or more skills into one new reusable workflow
- parent skills overlap but neither fully covers the target workflow
- a generated skill needs staged validation before it becomes live repo knowledge
- the mutation introduces higher risk than a normal skill amendment
- the user asks for a synthesis, hybrid, merged, evolved, or mutated skill

---

# Do Not Use When

- only one existing skill needs a normal update → use `chat-to-skill` amendment flow or bump the skill directly
- the request only needs runtime execution of multiple skills, not a new durable skill
- parent skill text, versions, or manifest rows are unavailable and cannot be supplied
- the proposed mutation has no new reusable behavior beyond bundling existing instructions
- the output is a reference, asset, or script rather than a skill

---

# Required Inputs

1. Two or more parent skill identities, including folder name and version when available
2. Current parent `skill.md` text or access to the parent `current_path`
3. Mutation goal stated as the new behavior the combined skill should provide
4. Target skill name or permission to infer one
5. Validation mode: staged only, staged plus promotion plan, or promote after explicit approval

---

# Optional Inputs

- Current `MANIFEST.md`
- Example tasks the mutated skill should handle
- Example tasks the mutated skill should reject
- Known conflicts between parent skills
- Human-in-the-loop threshold
- Existing staging folder under `workspace/mutations/`

---

# Outputs

Create a staged mutation package under:

```text
workspace/mutations/<mutation-name>/
```

The package should contain:

1. `candidate.skill.md` — the complete candidate skill file
2. `parent-map.md` — keep / modify / discard / conflict mapping for each parent skill
3. `conflict-matrix.md` — explicit trigger, rule, input, output, dependency, and validation conflicts
4. `validation-plan.md` — tests, RALPH checks, and promotion gates
5. `validation-results.md` — pass/fail result, unresolved blockers, and promotion recommendation

Only after approval, promote the candidate into:

```text
skills/<mutation-name>/V001/skill.md
```

---

# Support Layers

- Parent layer: selected live parent skill files and their manifest metadata
- Traceability layer: parent-map showing what was kept, modified, discarded, or conflicted
- Conflict layer: matrix of incompatible rules, triggers, inputs, outputs, dependencies, and validation gates
- Candidate layer: one complete AISkills-formatted `candidate.skill.md`
- RALPH layer: bounded requirements reaffirmation before promotion
- Promotion layer: repo validation, index update, and human approval boundary

---

# Procedure

## 1. Confirm Mutation Scope

1.1 List all parent skills and versions.
1.2 State the mutation goal in one sentence.
1.3 Confirm the target output is a new skill, not a reference, asset, script, or normal amendment.
1.4 If fewer than two parent skills are available, stop and request the missing parent material.

## 2. Build Parent Map

2.1 For each parent skill, identify:
- objective
- trigger
- required inputs
- outputs
- procedure steps
- decision logic
- validation gates
- rules
- failure modes
- dependencies

2.2 Mark each component as:
- `keep`
- `modify`
- `discard`
- `conflict`
- `move to reference`

2.3 Write the result to `parent-map.md`.

## 3. Build Conflict Matrix

3.1 Compare parent triggers, inputs, outputs, rules, and validation requirements.
3.2 Identify contradictions or duplicate responsibilities.
3.3 Resolve each conflict with one of:
- parent A wins
- parent B wins
- synthesize new rule
- require human decision
- exclude from mutation

3.4 Write the result to `conflict-matrix.md`.

## 4. Draft Candidate Skill

4.1 Generate one complete `candidate.skill.md`.
4.2 Use standard frontmatter and required AISkills sections.
4.3 Do not concatenate parent skills.
4.4 Preserve only instructions that serve the mutation goal.
4.5 Generalize parent-specific examples unless they are essential.
4.6 Add a `# Change Log` with `## V001` describing the mutation.

## 5. Run RALPH

Run at most two RALPH passes:

- **R — Reaffirm Requirements:** all required AISkills fields and sections are present.
- **A — Audit Alignment:** candidate satisfies mutation goal and parent scope.
- **L — Lock Layout and Lineage:** formatting, naming, parent traceability, and versioning are correct.
- **P — Purge Provenance Problems:** no copied citation artifacts, scaffold placeholders, or hidden-context dependencies remain.
- **H — Halt or Hand Off:** pass, conditional pass, or stop with blockers.

Do not run a third RALPH pass.

## 6. Write Validation Plan

Define:

1. Structural validation checks
2. Parent traceability checks
3. Conflict resolution checks
4. Trigger-positive example tasks
5. Trigger-negative example tasks
6. Promotion criteria
7. Human approval criteria

Write this to `validation-plan.md`.

## 7. Record Validation Results

Record:

- RALPH result
- unresolved conflicts
- repo validation result if available
- index consistency result if available
- recommendation: promote, revise, reject, or request human decision

Write this to `validation-results.md`.

## 8. Promote Only After Approval

8.1 If recommendation is `promote` and human approval is explicit, scaffold the skill with `new_skill.sh`.
8.2 Paste or write `candidate.skill.md` into `skills/<mutation-name>/V001/skill.md`.
8.3 Update the new skill changelog.
8.4 Run:

```bash
python3 system/scripts/update_index.py
python3 system/scripts/validate_skills.py
python3 system/scripts/update_index.py --check
```

---

# Decision Logic

| Condition | Action |
|----------|--------|
| fewer than two parent skills are available | stop and request parent material |
| parent skills conflict on rules or outputs | document in conflict matrix before drafting |
| mutation only bundles existing skills | reject as no new skill |
| conflict requires policy judgment | mark human decision required |
| RALPH fails after two passes | hand off blockers |
| candidate passes staging but lacks approval | keep staged, do not promote |
| candidate passes staging and approval is explicit | promote through normal skill scaffold flow |

---

# Validation

A staged mutation is valid when:

1. Parent skills and versions are listed.
2. Parent-map exists and covers every parent skill.
3. Conflict matrix exists and has no unresolved silent conflicts.
4. Candidate skill is complete and AISkills-formatted.
5. RALPH exits with PASS or CONDITIONAL PASS within two passes.
6. Validation plan includes positive and negative trigger examples.
7. Validation results state promote, revise, reject, or human decision required.
8. No live skill is created before promotion approval.

---

# Rules

- Never mutate by concatenating parent skill bodies.
- Never promote a mutated skill directly without staging.
- Never hide parent conflicts.
- Never overwrite an existing live skill version.
- Never create `VP###`, `production/`, or alternate production folders.
- Always use existing `V###`, `CURRENT`, and `MANIFEST.md` flow.
- Always keep mutation evidence in `workspace/mutations/<mutation-name>/` until promoted or rejected.
- Human approval is required before promotion.

---

# Failure Modes

| Failure | Recovery |
|--------|----------|
| parent skill text is missing | request parent skill text or manifest access |
| mutation goal is vague | ask for the new behavior the mutation must provide |
| parent rules conflict | document and require resolution before candidate finalization |
| candidate becomes too broad | split into smaller mutation candidates |
| RALPH loops without convergence | stop after two passes and return blockers |
| staged candidate passes but approval is absent | keep in `workspace/mutations/` |
| validation fails after promotion attempt | leave candidate staged and fix before retrying promotion |

---

# Dependencies

- Two or more parent AISkills skill files
- `MANIFEST.md` when repo access is available
- `workspace/mutations/` staging area
- `system/scripts/new_skill.sh` for promotion
- `system/scripts/update_index.py` for manifest/index regeneration
- `system/scripts/validate_skills.py` for repo validation

---

# Assumptions

- Mutations are higher risk than normal skill amendments.
- Parent skills may conflict, duplicate responsibilities, or encode incompatible assumptions.
- Staging is safer than direct promotion.
- Human approval remains required for promotion even when validation passes.

---

# Change Log

## V001
- Created governed skill mutation workflow with parent mapping, conflict matrix, staged candidate generation, RALPH validation, and approval-gated promotion.
