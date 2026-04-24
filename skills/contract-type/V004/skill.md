---
build_number: "004"
skill_id: "epcb.contracts.contract_type"
name: "contract-type"
description: "Classify and validate contract parameters before downstream contract generation."
trigger_keywords: "contract, classify contract, contract type, validate parameters, scope"
owner: "EPCB"
status: "draft"
created_at: "2026-04-19"
last_updated: "2026-04-23"
---

# Index

| Section | Description |
|--------|-------------|
| Objective | Define contract intake validation purpose |
| Trigger | When to apply the skill |
| Do Not Use When | Misuse conditions |
| Required Inputs | Minimum contract intake fields |
| Optional Inputs | Helpful metadata and context |
| Outputs | Classification and handoff results |
| Support Layers | Contract intake support surfaces |
| Procedure | Validation process |
| Decision Logic | Intake branches |
| Validation | Output correctness checks |
| Rules | Non-negotiable constraints |
| Failure Modes | Common breakdowns |
| Dependencies | Downstream contract generation needs |
| Assumptions | Operating assumptions |
| Change Log | Version history |

---

# Objective

Classify a proposed contract request and verify that the minimum fields needed for downstream contract generation are present, coherent, and ready to pass to `contract-gen`.

# Trigger

Use this skill when a contract needs to be classified, scoped, or validated before downstream contract generation.

# Do Not Use When

- The user only needs the final contract document and already has a validated parameter set.
- The request has no defined deliverable, owner, or scope.
- The work is not contract-like and should be treated as a general task or reference.

# Required Inputs

1. Deliverable name
2. Contract purpose or project context
3. In-scope work items
4. Out-of-scope exclusions
5. Success condition or validation criteria
6. Deadline or timing constraint
7. Responsible owner or issuing body

# Optional Inputs

1. Priority
2. Difficulty
3. Capacity or contributor count
4. Required evidence type
5. Tracker path
6. Reissue or revision context
7. User preference for interactive clarification versus blocker-only output

# Outputs

1. Contract classification
2. Validated parameter set for `contract-gen`
3. Missing-field list when input is incomplete
4. Scope-risk notes when requirements are ambiguous
5. One concise clarification question when a missing answer changes contract identity, issuing authority, destructive scope, or PASS semantics

# Support Layers

- Put example parameter sets in `references/`.
- Put blank contract templates or exported forms in `assets/`.
- Put parsers or formatters for contract intake data in `scripts/`.

# Procedure

1. **Identify Contract Type**
   1.1 Read the proposed deliverable and project context.
   1.2 Determine whether the request is new work, revision, reissue, validation, or administrative support.
   1.3 Record the classification in plain language.

2. **Validate Required Fields**
   2.1 Confirm the deliverable name is specific.
   2.2 Confirm in-scope items are observable actions or outputs.
   2.3 Confirm out-of-scope exclusions are explicit.
   2.4 Confirm the success condition can be verified.
   2.5 Confirm deadline and owner are present.

3. **Normalize Parameters**
   3.1 Rewrite vague scope items into concrete deliverables.
   3.2 Convert validation language into evidence-oriented criteria.
   3.3 Preserve user-provided constraints without inventing missing commitments.

4. **Produce Handoff**
   4.1 Return a complete parameter set when all required fields are valid.
   4.2 Return a missing-field list when fields are absent.
   4.3 Return scope-risk notes when ambiguity remains.

# Decision Logic

- IF required fields are missing, THEN return missing-field list and stop.
- IF scope is vague, THEN request clarification before contract generation.
- IF success criteria are not observable, THEN rewrite them as evidence requirements or request user confirmation.
- IF a missing answer changes contract identity, issuing authority, destructive scope, or PASS semantics, THEN ask one concise question before proceeding.
- IF all required fields are valid, THEN produce a parameter set for `contract-gen`.

# Validation

The output is valid when:

1. Contract type is stated.
2. Required fields are either complete or listed as missing.
3. In-scope work items are concrete.
4. Success criteria are observable.
5. The handoff can be consumed by `contract-gen`.

# Rules

- Do not generate the final contract document.
- Do not silently invent missing scope, owner, deadline, or success criteria.
- Do not pass vague success criteria to `contract-gen`.
- Keep validation notes separate from final parameter values.
- Do not ask broad exploratory questions. Ask at most one concise question unless the user explicitly requests a deeper intake.
- Do not expand the request into contract drafting, skill generation, or bundle execution unless the user explicitly requests that next step.
- Do not bury a required clarification inside a returned parameter set or risk note. Ask or stop first.

# Failure Modes

- Missing deliverable: request a specific deliverable name.
- Vague scope: ask for observable in-scope items.
- Unverifiable success condition: request evidence-based validation criteria.
- Conflicting requirements: identify the conflict and request resolution.

# Dependencies

- `contract-gen`: consumes the validated parameter set.
- Contract template or policy references when available.

# Assumptions

- The user wants contract intake validation, not final document generation.
- `contract-gen` remains responsible for producing the finished contract artifact.
- Contract requirements should be explicit enough for another person to execute and verify.

# Change Log

## V004
- Added a CTS-style one-question clarification gate for contract identity, authority, destructive scope, and PASS semantics.
- Added explicit boundaries against auto-expanding intake work into drafting, skill generation, or bundle execution.

## V003
- Added governed Index section for autonomous validation compatibility.
- Preserved V002 contract intake validation behavior.
