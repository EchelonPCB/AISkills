---
build_number: "003"
skill_id: "epcb.meta.skill_mutation"
name: "skill-mutation"
description: "Stage, synthesize, version, and promotion-gate a mutated skill from two or more parent skills using a skill-like workspace."
trigger_keywords: "mutation, combine, mutate skill, combine skills, skill mutation, merge workflows, staged skill validation, parent skill map, m command, promote mutation, mutation workspace"
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

Create a controlled staging workflow for combining two or more existing skills into a new mutated skill. The mutation workspace must resemble a regular skill folder, preserve parent traceability, hold a real `V###/skill.md` candidate, and remain staged until synthesis, checklist approval, repo validation, and human approval support promotion into `skills/<skill-name>/V001/skill.md`.

Prefer the command path when repo access is available:

```bash
python3 system/scripts/stage_mutation.py <parent-skill-1> <parent-skill-2> --name <mutation-name> --goal "one sentence goal"
python3 system/scripts/promote_mutation.py <mutation-name> --approve
```

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
  CURRENT
  V001/skill.md
  parents/<parent-skill>/<V###>/skill.md
  <references folder>/mutation-brief.md
  <references folder>/parent-map.md
  <references folder>/merge-notes.md
  <references folder>/promotion-checklist.md
  archived/
  assets/
  scripts/
  CHANGELOG.md
```

The package should contain:

1. `CURRENT` — staged current candidate version, initially `V001`
2. `V001/skill.md` — the candidate mutated skill, using the same filename as regular skills
3. `parents/<parent-skill>/<V###>/skill.md` — immutable parent snapshots used for synthesis
4. `mutation-brief.md` in the references folder — goal, parent list, and AI work order
5. `parent-map.md` in the references folder — keep / modify / discard / conflict mapping
6. `merge-notes.md` in the references folder — explicit trigger, input, output, rule, dependency, and validation conflicts
7. `promotion-checklist.md` in the references folder — RALPH result, blockers, and promotion recommendation
8. `CHANGELOG.md` — staged mutation history

Only after approval, promote the candidate into:

```text
skills/<mutation-name>/V001/skill.md
```

---

# Support Layers

- Parent layer: selected live parent skill files and their manifest metadata
- Traceability layer: `parent-map.md` in the references folder showing what was kept, modified, discarded, or conflicted
- Conflict layer: `merge-notes.md` in the references folder showing incompatible rules, triggers, inputs, outputs, dependencies, and validation gates
- Candidate layer: one complete AISkills-formatted `V###/skill.md`
- RALPH layer: bounded requirements reaffirmation before promotion
- Promotion layer: repo validation, index update, and human approval boundary

---

# Procedure

## 1. Confirm Mutation Scope

When shell access is available, create the staging structure with:

```bash
python3 system/scripts/stage_mutation.py <parent-skill-1> <parent-skill-2> --name <mutation-name> --goal "one sentence goal"
```

The short alias may be used when installed:

```bash
m <parent-skill-1> <parent-skill-2> --name <mutation-name> --goal "one sentence goal"
```

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

2.3 Write the result to `parent-map.md` in the mutation references folder.

## 3. Build Conflict Matrix

3.1 Compare parent triggers, inputs, outputs, rules, and validation requirements.
3.2 Identify contradictions or duplicate responsibilities.
3.3 Resolve each conflict with one of:
- parent A wins
- parent B wins
- synthesize new rule
- require human decision
- exclude from mutation

3.4 Write the result to `merge-notes.md` in the mutation references folder.

## 4. Draft Candidate Skill

4.1 Generate one complete `V001/skill.md`.
4.2 Use standard frontmatter and required AISkills sections.
4.3 Do not concatenate parent skills.
4.4 Preserve only instructions that serve the mutation goal.
4.5 Seed the candidate with parent objective, trigger, output, validation, and rule signals so a connected AI has real synthesis material.
4.6 Mark the seeded file with a clear synthesis-required note until an AI rewrites it into a self-contained mutated skill.
4.7 Add a `# Change Log` with `## V001` describing the mutation.

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

Write this to `promotion-checklist.md` in the mutation references folder.

## 7. Record Validation Results

Record:

- RALPH result
- unresolved conflicts
- repo validation result if available
- index consistency result if available
- recommendation: promote, revise, reject, or request human decision

Write this to `promotion-checklist.md` in the mutation references folder.

## 8. Promote Only After Approval

8.1 If recommendation is `promote` and human approval is explicit, run:

```bash
python3 system/scripts/promote_mutation.py <mutation-name> --approve
```

8.2 The promotion script must:
- read the staged candidate from `CURRENT` → `V###/skill.md`
- refuse promotion unless `promotion-checklist.md` in the mutation references folder says `Recommendation: promote`
- refuse promotion while the candidate or promotion checklist contains unresolved synthesis markers
- create the normal `skills/<skill-name>/V001/skill.md` structure
- regenerate indexes
- run repo validation
- roll back the new live skill if validation fails

8.3 If aliases are installed, the shorter form is:

```bash
mup <mutation-name> --approve
```

8.4 Manual fallback is allowed only when the promotion script is unavailable:

```bash
./system/scripts/new_skill.sh <mutation-name> mutated
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
| candidate passes staging and approval is explicit | promote through `promote_mutation.py --approve` |

---

# Validation

A staged mutation is valid when:

1. Parent skills and versions are listed.
2. Parent snapshots exist under `parents/<parent-skill>/<V###>/skill.md`.
3. `parent-map.md` in the references folder covers every parent skill.
4. `merge-notes.md` in the references folder has no unresolved silent conflicts.
5. Candidate skill is complete and AISkills-formatted at `CURRENT` → `V###/skill.md`.
6. Candidate no longer describes the staging process; it describes the mutated runtime behavior.
7. RALPH exits with PASS or CONDITIONAL PASS within two passes.
8. Promotion checklist includes positive and negative trigger examples.
9. Promotion checklist states promote, revise, reject, or human decision required.
10. No live skill is created before promotion approval.
11. Promotion command completes repo validation after moving the candidate into `skills/`.

---

# Rules

- Never mutate by concatenating parent skill bodies.
- Never promote a mutated skill directly without staging.
- Never hide parent conflicts.
- Never overwrite an existing live skill version.
- Never create `VP###`, `production/`, or alternate production folders.
- Always use existing `V###`, `CURRENT`, and `MANIFEST.md` flow.
- In mutation workspaces, use `V###/skill.md`; do not use `candidate.skill.md`.
- Do not require `mutation.json`; lineage must be readable from parent folders, mutation brief, and changelog.
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
| validation fails after promotion attempt | rely on promotion rollback, leave candidate staged, and fix before retrying promotion |
| workspace has loose root markdown files | migrate to `CURRENT`, `V###/skill.md`, the references folder, and `CHANGELOG.md` |

---

# Dependencies

- Two or more parent AISkills skill files
- `MANIFEST.md` when repo access is available
- `workspace/mutations/` staging area
- `system/scripts/stage_mutation.py` for command-generated staging packages
- `system/scripts/promote_mutation.py` for approval-gated promotion
- `system/scripts/bump_mutation.py` for staged mutation version increments when available
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

## V003
- Replaced loose root mutation artifacts with a staged-skill workspace structure.
- Standardized candidate files as `CURRENT` → `V###/skill.md`.
- Replaced separate validation plan/results files with one promotion checklist in the references folder.
- Made parent snapshots first-class folders under `parents/<parent-skill>/<V###>/`.

## V002
- Added command-first mutation staging through `stage_mutation.py`.
- Added approval-gated promotion through `promote_mutation.py`.
- Added required machine-readable mutation metadata and parent snapshots to staged packages.

## V001
- Created governed skill mutation workflow with parent mapping, conflict matrix, staged candidate generation, RALPH validation, and approval-gated promotion.
