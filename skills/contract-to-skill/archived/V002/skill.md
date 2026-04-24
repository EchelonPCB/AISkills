---
build_number: "002"
skill_id: "epcb.meta.contract_to_skill"
name: "contract-to-skill"
description: "Convert an ACDC MVP Deliverable Contract document into a complete, reusable skill.md file by mapping contract fields to the AISkills standard structure."
trigger_keywords: "contract, convert contract, extract workflow, create skill, skill intake"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-20"
---

# Index

| Section | Description |
|--------|-------------|
| Objective | Define contract-to-skill conversion purpose |
| Trigger | When to apply the skill |
| Do Not Use When | Misuse conditions |
| Required Inputs | Contract and governance inputs |
| Optional Inputs | Metadata overrides and context |
| Outputs | Generated skill file expectations |
| Support Layers | Source and formatting layers |
| Procedure | Conversion process |
| Decision Logic | Branches and classification decisions |
| Validation | Output correctness checks |
| Rules | Non-negotiable constraints |
| Failure Modes | Common breakdowns |
| Dependencies | Required source materials |
| Assumptions | Operating assumptions |
| Change Log | Version history |

---

# Objective

Given one or more ACDC MVP Deliverable Contract documents, extract the structured content from each contract's fields and produce a complete, reusable `skill.md` file per contract. The output skill must be executable without reference to the original contract document.

# Trigger

Use this skill when:

- A member or BoD has issued one or more ACDC MVP Deliverable Contract `.docx` files
- The goal is to make those contracts accessible as executable, AI-readable skill files
- The contracts contain defined scope, validation criteria, in-scope steps, and a clear deliverable

# Do Not Use When

- The contract is blank or has no Scope Lock filled in — classify as **asset** (template), not skill
- The deliverable is purely informational (e.g., a report) with no repeatable execution steps — classify as **reference**
- The contract has conflicting or undefined success conditions — request BoD clarification before proceeding

# Required Inputs

1. One or more ACDC MVP Deliverable Contract `.docx` files (BoD page must be filled)
2. ACDC Club Constitution and Bylaws (for enforcement language and membership rules)

# Optional Inputs

1. Skill ID prefix override (default: `epcb.{project_domain}.{skill_name}`)
2. Owner override (default: `EPCB`)
3. Additional context from the project tracker or 4P documentation

# Outputs

One complete `skill.md` file per contract, containing:

1. YAML frontmatter with skill metadata
2. Objective — what the contract deliverable accomplishes
3. Trigger — when to use this skill
4. Required Inputs — mapped from Interface Requirements + IN SCOPE prerequisites
5. Optional Inputs — inferred from contractor discretion fields
6. Outputs — mapped from Validation Criteria evidence items
7. Procedure — derived from IN SCOPE steps, expanded into numbered substeps
8. Rules — derived from OUT OF SCOPE items + Enforcement & Conditions clause
9. Failure Modes — inferred from success conditions, out-of-scope exclusions, and edge cases
10. Dependencies — extracted from Interface Requirements and Contract ID cross-references
11. Assumptions — explicit statements covering anything the contract leaves to contractor discretion
12. Validation Criteria — exact PASS threshold from the contract's Validation Criteria section
13. Logging block — Contract ID, 4P Code, Tracker Path, Deadline, Type, Priority, Majors, Capacity

---

# Support Layers

- Contract parsing layer: reads filled BoD page fields from ACDC MVP Deliverable Contract documents.
- Governance layer: preserves enforcement language and BoD authority boundaries.
- Skill formatting layer: maps extracted fields into AISkills governed section structure.
- Traceability layer: carries Contract ID, 4P Code, Tracker Path, and deadline into the generated skill.

---

# Procedure

## 1. Intake and Field Extraction

1.1 Open each contract document and locate the BoD page (Page 1).
1.2 Confirm the Scope Lock section is filled in — if blank, stop and classify as asset.
1.3 Extract the following fields verbatim:

    - Contract ID
    - 4P Code
    - Deliverable name
    - Type (Micro / Macro)
    - Hard Deadline
    - Tracker Path
    - Contract Type (Technical / Operations / Marketing / Events)
    - Priority (Critical / Standard / Low)
    - Applicable Majors
    - Difficulty
    - Contract Capacity
    - MVP Function
    - Success Condition
    - Interface Requirement
    - IN SCOPE items (all checked boxes)
    - OUT OF SCOPE items (all checked boxes)
    - Validation Criteria items (#1–#4)

## 2. Skill ID Generation

2.1 Map the contract's project domain to a skill ID prefix using the Tracker Path:

    - "ASVP-Hardware" → epcb.asvp
    - "V2I-Integration" → epcb.v2i
    - "ASVP-PID"       → epcb.pid
    - Other            → epcb.{tracker-subfolder-name}

2.2 Convert the Deliverable name to snake_case for the skill ID name:
    e.g., "Traffic Light Enclosure Design" → "enclosure-design"

2.3 Compose skill_id: `{prefix}.{snake_case_deliverable}`

## 3. Objective Construction

3.1 Write the Objective by combining:
    - MVP Function (what the task does)
    - Success Condition (what a completed result looks like)
    - Interface Requirement (what it connects to)

3.2 The Objective must be executable without the contract document — do not reference "the contract."

## 4. Procedure Expansion

4.1 Take each IN SCOPE item and expand it into 2–5 numbered substeps.
4.2 For any step involving a safety or quality gate (e.g., resistor verification, BoD approval), add an explicit checkpoint before proceeding.
4.3 Add an evidence preparation section at the end mapping each Validation Criteria item to a file upload or live demo action.
4.4 Add a completion step: notify BoD, request review, await sign-off.

4.5 Apply decision logic where IN SCOPE items contain conditional actions:

    IF [condition]:
    → [action]

## 5. Rules Derivation

5.1 Convert each OUT OF SCOPE item into a prohibition rule using "Do not..." language.
5.2 Extract universal enforcement rules from the Enforcement & Conditions clause:
    - Work without evidence does not qualify as completion.
    - Scope changes require BoD approval.
    - Unclaimed contracts are not active.
5.3 Add any safety rules implied by the domain (e.g., power-off before rework for electrical contracts).

## 6. Failure Modes Derivation

6.1 For each Validation Criteria item, define what happens if it cannot be satisfied.
6.2 For each IN SCOPE step involving hardware, define a recovery action on failure.
6.3 For each dependency on a prior contract, define the failure mode if that contract is incomplete.

## 7. Dependencies Extraction

7.1 Identify all contract cross-references in the OUT OF SCOPE and Interface Requirement fields.
7.2 For each cross-referenced Contract ID, create a dependency entry stating:
    - What the dependency provides
    - Whether it is a hard prerequisite (cannot start without it) or a downstream dependency

## 8. Assumptions Derivation

8.1 For each field left to contractor discretion (e.g., tool choice, material selection), write an explicit assumption.
8.2 For each implied constraint not stated in the contract (e.g., measurement conventions, unit definitions), write an explicit assumption.
8.3 Flag all assumptions with the phrase "deviation requires BoD confirmation."

## 9. Logging Block Construction

9.1 Populate the Logging block with all extracted metadata fields verbatim from the contract header.

## 10. Validation

10.1 Verify the generated skill.md:
    - Can be executed without the original contract document
    - Contains no fields left blank
    - All Validation Criteria are restated exactly as PASS conditions
    - All OUT OF SCOPE items appear as Rules
    - All cross-referenced Contract IDs appear in Dependencies

10.2 If any section is missing or incomplete: refine before output — do not produce partial files.

---

# Decision Logic

| Condition | Action |
|----------|--------|
| Scope Lock is blank | classify as asset and stop |
| contract is informational only | classify as reference |
| success condition conflicts with scope | request BoD clarification |
| multiple contracts are supplied | generate one skill per contract |
| all contract fields are complete | produce governed `skill.md` output |

---

# Validation

The generated skill is valid when:

1. It can be executed without the original contract document.
2. All required AISkills sections are present.
3. PASS threshold matches the contract's Success Condition.
4. OUT OF SCOPE items are represented as Rules.
5. Contract IDs and dependencies are traceable.

---

# Rules

- Do not produce a skill file for a contract with an unfilled Scope Lock.
- Do not omit any of the 13 required output sections.
- Do not reference "the contract" inside the skill body — the skill must be self-contained.
- Do not modify or interpret the Success Condition — restate it exactly as the PASS threshold.
- Do not infer OUT OF SCOPE items — only include items explicitly listed in the contract.
- Produce one skill file per contract — do not merge multiple contracts into one skill.
- All safety-critical steps (electrical power-on, mechanical fit, BoD approval gates) must appear as explicit checkpoints in the Procedure.

# Failure Modes

- Contract Scope Lock is blank: Stop — classify document as asset (unfilled template). Do not generate a skill.
- Validation Criteria fields are empty: Request BoD to complete the contract before proceeding.
- Cross-referenced Contract ID is unknown: Flag as an unresolved dependency in the skill file; do not silently omit.
- IN SCOPE items are ambiguous: Expand to the most conservative interpretation and mark as assumption.
- Conflicting OUT OF SCOPE and IN SCOPE items: Flag conflict; do not resolve independently — raise to BoD.

# Dependencies

- ACDC Club Constitution and Bylaws: Required for accurate enforcement language in the Rules section (Article IV §4.8–§4.9).
- ACDC MVP Deliverable Contract template: Defines the field structure this skill reads from.
- AISkills `chat-to-skill` skill (`epcb.meta.chat_to_skill`): Provides the standard `skill.md` output format this skill conforms to.

# Assumptions

- The BoD page of each contract is fully filled in before this skill is applied.
- Tracker Path values in the contract are current and accessible.
- "Micro" contracts (<2h) produce shorter Procedure sections than "Macro" contracts (>2h) but the same required sections.
- Contract ID cross-references use the format CON-YYYYMMDD-NN and can be resolved from the project tracker.
- The skill_id prefix mapping (Tracker Path → domain) is maintained by the DRAM and updated when new project folders are created.

# Change Log

## V002
- Added governed Index, Support Layers, Decision Logic, Validation, and Change Log sections for autonomous validation compatibility.
- Preserved V001 contract extraction behavior and output mapping.

# Validation Criteria (Skill Self-Check)

A generated skill.md is valid when ALL of the following are true:

1. All 13 output sections are present and non-empty.
2. PASS threshold matches the contract's Success Condition verbatim.
3. Every OUT OF SCOPE item appears as a Rule.
4. Every Validation Criteria item appears in the Outputs and Procedure evidence steps.
5. Every cross-referenced Contract ID appears in Dependencies.
6. The skill can be read and executed without access to the original contract document.

# Logging

- Skill ID: epcb.meta.contract_to_skill
- Source: Derived from ACDC MVP Deliverable Contract processing session (2026-04-19)
- Skills generated in originating session: 7
- Contracts processed: CON-20260415-03 through CON-20260415-09
- Completeness status: All sections present in all outputs
