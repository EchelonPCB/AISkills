---
build_number: "001"
skill_id: "epcb.mutated.chat_to_contracts"
name: "chat-to-contracts"
description: "Staged mutation skill for Use a chat to create an actionable contract, seeded from chat-to-skill V013, contract-to-skill V002."
trigger_keywords: "mutate skill, combine skills, chat to contracts, Use a chat to create an actionable contract"
owner: "EPCB"
status: "draft"
created_at: "2026-04-20"
last_updated: "2026-04-20"
---

# Index

| Section | Description |
|--------|-------------|
| Index | Index guidance |
| Objective | Objective guidance |
| Trigger | Trigger guidance |
| Do Not Use When | Do Not Use When guidance |
| Required Inputs | Required Inputs guidance |
| Optional Inputs | Optional Inputs guidance |
| Outputs | Outputs guidance |
| Support Layers | Support Layers guidance |
| Procedure | Procedure guidance |
| Decision Logic | Decision Logic guidance |
| Validation | Validation guidance |
| Rules | Rules guidance |
| Failure Modes | Failure Modes guidance |
| Dependencies | Dependencies guidance |
| Assumptions | Assumptions guidance |
| Change Log | Change Log guidance |

---

# Objective

Create a reusable workflow for Use a chat to create an actionable contract.

SYNTHESIS_REQUIRED: This staged candidate is seeded from parent skill signals. A connected AI must rewrite this file so the promoted version describes the mutated runtime behavior directly, not the staging process.

Parent objective signals:

- `chat-to-skill` `V013`: Convert a raw chat log or structured chat summary into one or more complete, reusable `skill.md` files that conform to the AISkills repository standard. ---
- `contract-to-skill` `V002`: Given one or more ACDC MVP Deliverable Contract documents, extract the structured content from each contract's fields and produce a complete, reusable `skill.md` file per contract. The output skill must be executable without reference to the original contract document.

---

# Trigger

Use this skill when:

- a user needs a repeatable workflow for Use a chat to create an actionable contract
- the task requires capabilities from more than one parent skill
- the output must be converted into one self-contained AISkills `skill.md`

Parent trigger signals:

- `chat-to-skill` `V013`: Use this skill when a conversation contains: - repeatable workflows - system integration logic - procedural steps with clear execution order - defined inputs and outputs - reusable engineering, business, or AI processes ---
- `contract-to-skill` `V002`: Use this skill when: - A member or BoD has issued one or more ACDC MVP Deliverable Contract `.docx` files - The goal is to make those contracts accessible as executable, AI-readable skill files - The contracts contain defined scope, validation criteria, in-scope steps, and a clear deliverable

---

# Do Not Use When

- one parent skill can handle the task without synthesis
- the desired output is only a note, asset, checklist, or reference file
- parent rules conflict and no human decision has resolved the conflict
- the mutation goal is not reusable beyond one isolated request

Parent exclusion signals:

- `chat-to-skill` `V013`: Do not use this skill when the content is: - purely informational → classify as **reference** - only code → classify as **script** - a standalone file/template → classify as **asset** - vague or exploratory → request clarification ---
- `contract-to-skill` `V002`: - The contract is blank or has no Scope Lock filled in — classify as **asset** (template), not skill - The deliverable is purely informational (e.g., a report) with no repeatable execution steps — classify as **reference** - The contract has conflicting or undefined success conditions — request BoD clarification before proceeding

---

# Required Inputs

1. Source material needed to perform: Use a chat to create an actionable contract
2. Parent snapshots listed in the Dependencies section
3. Mutation brief at `references/mutation-brief.md`
4. Parent mapping at `references/parent-map.md`
5. Merge notes at `references/merge-notes.md`

Parent input signals:

- `chat-to-skill` `V013`: 1. Raw chat log OR structured summary ---
- `contract-to-skill` `V002`: 1. One or more ACDC MVP Deliverable Contract `.docx` files (BoD page must be filled) 2. ACDC Club Constitution and Bylaws (for enforcement language and membership rules)

---

# Optional Inputs

- Example source chats, contracts, or task records relevant to Use a chat to create an actionable contract
- Naming, domain, owner, or skill ID overrides
- Acceptance criteria supplied by a human reviewer
- Existing support files that should become references, assets, or scripts

---

# Outputs

1. One complete mutated `skill.md` that performs Use a chat to create an actionable contract
2. Updated `references/parent-map.md` explaining which parent components were kept, modified, discarded, or conflicted
3. Updated `references/merge-notes.md` resolving rule, trigger, input, output, dependency, and validation conflicts
4. Updated `references/promotion-checklist.md` with the final recommendation

Parent output signals:

- `chat-to-skill` `V013`: - Classification block - One complete formatted `skill.md` for `new skill` or `amendment` - Repo command block - CHANGELOG entry - Support file plan - Validation notes ---
- `contract-to-skill` `V002`: One complete `skill.md` file per contract, containing: 1. YAML frontmatter with skill metadata 2. Objective — what the contract deliverable accomplishes 3. Trigger — when to use this skill 4. Required Inputs — mapped from Interface Requirements + IN SCOPE prerequisites 5. Optional Inputs — inferred from contractor discretion fields 6. Outputs — mapped from Validation Criteria evidence items 7. Procedure — derived from IN SCOPE steps, expanded into numbered substeps 8. Rules — derived from OUT OF SCOPE items + Enfor

---

# Support Layers

- Parent snapshot layer: immutable parent skills under `parents/<skill>/<V###>/skill.md`
- Mutation brief layer: target behavior and AI work order in `references/mutation-brief.md`
- Parent map layer: explicit component mapping in `references/parent-map.md`
- Merge notes layer: conflict resolution in `references/merge-notes.md`
- Promotion layer: approval gate in `references/promotion-checklist.md`

---

# Procedure

## 1. Read Parent Evidence

1.1 Read `references/mutation-brief.md` first.
1.2 Read each parent snapshot listed in Dependencies.
1.3 Identify the parent behavior that directly supports Use a chat to create an actionable contract.
1.4 Ignore parent content that only serves the parent skill's original artifact type.

## 2. Synthesize The Mutated Skill

2.1 Rewrite this `skill.md` so the Objective states the new runtime behavior directly.
2.2 Convert parent triggers into a single non-overlapping trigger set.
2.3 Merge required inputs into the minimum inputs needed for the mutated workflow.
2.4 Merge outputs into one clear deliverable contract.
2.5 Convert parent procedures into one ordered workflow.
2.6 Resolve parent conflicts in `references/merge-notes.md` before promotion.

## 3. Run Bounded RALPH

3.1 Reaffirm every required AISkills frontmatter field and section.
3.2 Audit alignment with the mutation goal.
3.3 Lock layout, lineage, and versioning.
3.4 Purge scaffold markers, hidden context, copied citation artifacts, and staging-only text.
3.5 Halt after two passes with PASS, CONDITIONAL PASS, REVISE, or REJECT.

---

# Decision Logic

| Condition | Action |
|----------|--------|
| one parent fully covers the task | reject mutation and use that parent skill |
| source material is missing | request the missing material |
| parent instructions conflict | resolve in `references/merge-notes.md` before editing the candidate |
| candidate still contains synthesis-required markers | keep staged and do not promote |
| promotion checklist says revise or reject | keep staged and continue editing |
| promotion checklist says promote and human approval is explicit | run `promote_mutation.py <mutation-name> --approve` |

---

# Validation

A promotion-ready mutated skill must:

1. State Use a chat to create an actionable contract as a self-contained runtime behavior.
2. Preserve only parent instructions that serve the mutation goal.
3. Remove staging-only language, including this synthesis-required notice.
4. Include all required AISkills frontmatter fields and sections.
5. Include at least three useful trigger keywords.
6. Pass `python3 system/scripts/validate_skills.py` after promotion.
7. Have `references/promotion-checklist.md` set to `Recommendation: promote`.

Parent validation signals:

- `chat-to-skill` `V013`: A generated chat-to-skill result is valid only when: - the classification block is first - new skill or amendment output contains one complete fenced `skill.md` - generated frontmatter includes `trigger_keywords` - generated level-one headers match the Required Skill Formatter exactly - generated skill has no placeholders or partial sections - generated skill has no source-citation artifacts - generated changelog guidance has no scaffold leftovers - RALPH exits with PASS or CONDITIONAL PASS - manifest-unavailable o
- `contract-to-skill` `V002`: The generated skill is valid when: 1. It can be executed without the original contract document. 2. All required AISkills sections are present. 3. PASS threshold matches the contract's Success Condition. 4. OUT OF SCOPE items are represented as Rules. 5. Contract IDs and dependencies are traceable. ---

---

# Rules

- Do not concatenate parent skill bodies.
- Do not preserve parent content that does not serve Use a chat to create an actionable contract.
- Do not promote while synthesis-required or staging-only language remains.
- Do not bypass human approval.
- Do not create `VP###`, `production/`, or alternate production folders.

Parent rule signals:

- `chat-to-skill` `V013`: - Do not return a generated skill until the Required Skill Formatter passes. - Do not use body-only trigger keywords as a substitute for YAML `trigger_keywords`. - Do not rename required generated headers. - Do not copy AI chat citation markers into generated skills. - Do not leave scaffold changelog text in companion changelog guidance. - Do not run RALPH more than two passes. - Do not treat missing manifest access as proof that no duplicate skill exists. - Do not recommend `VP###`, `production/`, or separate prod
- `contract-to-skill` `V002`: - Do not produce a skill file for a contract with an unfilled Scope Lock. - Do not omit any of the 13 required output sections. - Do not reference "the contract" inside the skill body — the skill must be self-contained. - Do not modify or interpret the Success Condition — restate it exactly as the PASS threshold. - Do not infer OUT OF SCOPE items — only include items explicitly listed in the contract. - Produce one skill file per contract — do not merge multiple contracts into one skill. - All safety-critical steps

---

# Failure Modes

| Failure | Recovery |
|--------|----------|
| mutation remains a parent bundle | rewrite into one runtime workflow |
| parent conflict is unresolved | stop and request a human decision |
| candidate fails formatter requirements | revise before promotion |
| RALPH does not converge after two passes | halt and record blockers in the promotion checklist |

---

# Dependencies

Parent skill snapshots:

- `parents/chat-to-skill/V013/skill.md`
- `parents/contract-to-skill/V002/skill.md`

Mutation references:

- `references/mutation-brief.md`
- `references/parent-map.md`
- `references/merge-notes.md`
- `references/promotion-checklist.md`

---

# Assumptions

- Parent snapshots represent the exact versions selected for mutation.
- The connected AI can read the parent folder and rewrite this staged file before promotion.
- The promoted skill should be self-contained and should not require reading the mutation workspace at runtime.

---

# Change Log

## V001
- Created staged mutation candidate from chat-to-skill V013, contract-to-skill V002 for Use a chat to create an actionable contract.
