---
build_number: "004"
skill_id: "epcb.contracts.contract_bundle_execution"
name: "Contract Bundle Execution"
description: "Organize one or more contracts with their associated contract-specific skills, then execute the bundle into traceable deliverables, evidence, and handoff records."
trigger_keywords: "contract bundle, execute contracts, associated skills, contract deliverables, bundle execution"
owner: "EPCB"
status: "active"
created_at: "2026-04-21"
last_updated: "2026-04-23"
---
# Index
| Section | Description |
|---------|-------------|
| Objective | Summarizes the high-level purpose of this skill |
| Trigger | When to apply this skill |
| Do Not Use When | Conditions where this skill is not appropriate |
| Required Inputs | Mandatory items needed to execute the process |
| Optional Inputs | Supporting inputs that aid execution |
| Outputs | What deliverables are expected to pass |
| Support Layers | Traceability and governance layers used |
| Procedure | Step-by-step workflow |
| Decision Logic | Branching and dependency decisions |
| Validation | Checks to ensure the process meets criteria |
| Rules | Non-negotiable constraints |
| Failure Modes | Recognized failure patterns and mitigation |
| Dependencies | Upstream skills or contracts required |
| Assumptions | Clarifications of unspecified fields |
| Change Log | History of revisions |

# Objective
Execute a bundle of contracts by pairing each contract with its associated contract-specific skill, planning the execution order, producing the required deliverables, and packaging evidence in a way that preserves contract scope, validation criteria, dependencies, and BoD handoff requirements.

This skill is intentionally general. It does not define the technical content of any single contract. It orchestrates contract execution using the contract documents and their associated skills.

# Trigger
Use this skill when:

- a set of one or more contracts must be executed together as a bundle
- each contract has, or needs, an associated contract-specific skill
- the task is to organize, sequence, execute, validate, and package contract deliverables
- a contract bundle contains dependencies between contracts that must be respected
- the output must include traceable evidence, assumptions, and handoff notes for each contract

# Do Not Use When
- The task is to generate the original contract document from parameters; use `contract-gen`.
- The task is to convert one contract into a new skill; use `contract-to-skill`.
- The task is to revise contract scope, success conditions, or BoD authority language.
- No contract-specific skill exists and the user has not asked to create one.
- The user wants a single standalone answer rather than governed contract execution.
- The bundle contains unrelated work that should be split into separate execution bundles.

# Required Inputs
- Contract document or contract summary for each contract in the bundle.
- Associated contract-specific skill for each contract, either as a live AISkills skill, a reference skill file, or an explicitly provided skill draft.
- Contract identifiers, titles, deadlines, tracker paths, and evidence destinations.
- PASS threshold, validation criteria, in-scope items, out-of-scope items, and interface requirements for each contract.
- Known dependency relationships between contracts, including upstream outputs needed by downstream contracts.
- Execution target: whether the goal is planning only, artifact generation, evidence packaging, or full delivery support.

# Optional Inputs
- Existing contract bundle archive, folder, or shared drive export.
- Reference skill sets, such as `references/design1-contract-skills/`, for prior bundle patterns.
- Existing artifacts, notes, vendor links, calculations, diagrams, code, photos, or videos.
- Preferred tools for documents, diagrams, calculations, code, or evidence packaging.
- Placeholder assumptions approved by BoD or explicitly allowed by the contract.
- Required notification channel or handoff format for BoD, contractors, or dependent teams.
- User preference for whether missing skills should be created now or returned as blockers.

# Outputs
- Bundle execution map listing each contract, associated skill, dependency status, deliverables, evidence items, and owner or handoff target.
- Per-contract execution notes that preserve scope, out-of-scope exclusions, assumptions, and validation criteria.
- Contract deliverables produced or specified according to each associated skill.
- Evidence package or evidence checklist for each contract, including file paths, links, demo requirements, or upload destinations.
- Dependency handoff notes showing which contract outputs unblock downstream contracts.
- Final bundle summary that states complete, blocked, assumed, and pending items.

# Support Layers
- Contract mapping layer: pairs every contract with its associated skill and required evidence.
- Governance layer: preserves scope lock, BoD validation authority, deadlines, and out-of-scope boundaries.
- Dependency layer: sequences contracts according to required upstream outputs and handoff relationships.
- Execution layer: drives each contract-specific skill without merging contract responsibilities.
- Evidence layer: packages proof-of-completion artifacts and upload or handoff instructions.
- Reference layer: keeps prior bundle-specific skill sets available as examples without making them live routed skills.

# Procedure
1. Inventory the bundle.
   1.1 List every contract document, contract ID, deliverable name, deadline, and tracker path.
   1.2 List every associated contract-specific skill and mark whether it is live, reference-only, or draft.
   1.3 Flag any contract without an associated skill before execution begins.

2. Pair contracts to skills.
   2.1 Match each contract to the skill that carries its workflow, required inputs, outputs, validation criteria, and failure modes.
   2.2 If multiple skills appear relevant, select the one that best matches the contract ID, deliverable title, scope lock, and PASS threshold.
   2.3 If no skill exists and the user explicitly wants skill creation, route to `contract-to-skill`; otherwise stop and report the missing skill as a blocker.

3. Build the execution map.
   3.1 Extract dependencies between contracts.
   3.2 Mark which contracts can run immediately and which are blocked by upstream outputs.
   3.3 Define an execution order that minimizes dependency deadlocks.
   3.4 Record any allowed placeholder assumptions before using them.
   3.5 Ask one concise question only when a missing answer changes contract pairing authority, execution target, destructive scope, or unblock strategy.

4. Execute contract-specific workflows.
   4.1 For each contract, run the associated skill's procedure against the contract's required inputs.
   4.2 Produce or specify the deliverables required by that contract only.
   4.3 Keep assumptions, external sources, calculations, code, diagrams, and evidence tied to the contract that requires them.
   4.4 Do not import extra work from neighboring contracts unless it is an explicit dependency.

5. Package evidence and handoffs.
   5.1 Build an evidence checklist for each contract.
   5.2 Link each artifact to the matching validation criterion.
   5.3 Write dependency handoff notes for downstream contract teams or BoD review.
   5.4 Record blocked items and the exact upstream output needed to unblock them.

6. Close the bundle.
   6.1 Summarize completed contracts, blocked contracts, assumptions, and pending evidence.
   6.2 Confirm every deliverable remains tied to its contract ID and tracker path.
   6.3 Provide the final bundle package or next action list.

# Decision Logic
- If a contract has a live AISkills skill, use the live skill as the authority.
- If a contract has only a reference skill, use it as an execution aid and clearly label it reference-only.
- If a contract has no associated skill and the user explicitly requests skill creation, route to `contract-to-skill`; otherwise stop and report the blocker.
- If a downstream contract depends on an upstream output that is complete, cite and use that output.
- If a downstream contract depends on an upstream output that is missing but assumptions are allowed, proceed with a labeled placeholder.
- If a missing fact changes contract pairing authority, execution target, destructive scope, or unblock strategy, ask one concise question before proceeding.
- If missing dependencies are not assumable, pause that contract and report the blocker.
- If the bundle mixes unrelated projects, split the bundle before execution.

# Validation
- Every contract in the bundle has a contract ID, deliverable name, tracker path or destination, and associated skill status.
- Every produced artifact maps to a specific contract validation criterion.
- Every assumption is labeled with the contract it affects and whether it is approved, provisional, or user-provided.
- Every dependency is either satisfied, explicitly assumed, or marked blocked.
- No deliverable crosses contract boundaries without an explicit interface requirement or dependency note.
- Reference-only skills are not treated as live routed skills unless they have been promoted into `MANIFEST.md`.
- Final output separates completed, blocked, assumed, and pending work.

# Rules
- Do not change contract scope, PASS thresholds, deadlines, tracker paths, or BoD language.
- Do not merge multiple contracts into one deliverable unless the contracts explicitly require a shared artifact.
- Do not treat reference files as live governed skills.
- Do not invent missing technical requirements to make execution easier.
- Do not perform procurement, physical installation, or irreversible operational actions unless the contract and user explicitly request them.
- Use up-to-date external sources for prices, product specs, legal requirements, or other time-sensitive facts when those details affect deliverables.
- Keep every artifact traceable to a contract ID and evidence requirement.
- Do not create or mutate contract-specific skills during bundle execution unless the user explicitly requests that step.
- Do not ask broad exploratory questions. Ask at most one concise question unless the user explicitly requests a planning workshop.
- Do not expand the bundle into adjacent contracts, new workstreams, or non-bundle artifacts unless the user explicitly requests that expansion.

# Failure Modes
- Missing associated skill: pause execution for that contract and route to `contract-to-skill` or request the missing skill.
- Ambiguous contract-skill match: present candidate skills and ask for selection or use the strongest contract ID/title match if safe.
- Stale reference skill: use the contract text as authority and mark the reference as outdated.
- Dependency deadlock: report the blocked contract, missing upstream output, and whether assumptions are allowed.
- Evidence mismatch: revise the artifact or checklist until it maps directly to the validation criterion.
- Scope creep: remove unrequested work and return to the contract's in-scope items.
- Bundle archive error: request a clean archive, folder, or contract list before proceeding.

# Dependencies
- `contract-to-skill`: creates or updates an associated contract-specific skill when none exists.
- `contract-gen`: creates the original BoD-ready contract document from validated parameters when needed.
- Contract-specific live skills or reference skill files supplied with the bundle.
- `references/design1-contract-skills/`: example reference set for a prior Design 1 contract bundle.

# Assumptions
- A contract-specific skill is the execution guide, while the contract document remains the source of authority for scope and validation.
- Reference skill files are useful examples but are not automatically live AISkills.
- Bundle execution can produce plans, artifacts, checklists, or handoff packages depending on the user's requested execution target.
- BoD or project owner approval is required for scope changes, deadline changes, and validation criteria changes.
- External facts such as product availability, pricing, and technical specifications may change and should be verified when used.

# Change Log
## V004 - 2026-04-23
- Added a CTS-style one-question clarification gate for contract pairing, execution target, destructive scope, and unblock strategy.
- Added explicit boundaries against auto-creating skills or expanding bundle scope without an explicit user request.

## V003 - 2026-04-22
- Generalized contract bundle execution from a Design 1-specific CON-01 through CON-04 workflow into a reusable contract-plus-associated-skill orchestration process.
- Clarified that Design 1 generated contract skills are reference artifacts, not live routed skills.

## V002 - 2026-04-21
- Specialized bundle workflow used for the Design 1 CON-01 through CON-04 contract set.
