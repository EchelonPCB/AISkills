---
build_number: "002"
skill_id: "epcb.governance.acdc_governance_system"
name: "acdc-governance-system"
description: "Execute ACDC governance decisions for membership, voting, 4P approval, committees, and Board authority."
trigger_keywords: "acdc governance, membership enforcement, 4P approval, board voting, committee structure, status management"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-19"
---

# Index

| Field       | Detail                                                              |
|-------------|---------------------------------------------------------------------|
| Trigger     | Need to run or validate an ACDC governance action                   |
| Input       | Member status, 4P proposal, vote context, committee data            |
| Output      | Governance decision, status update, approval, rejection, next step  |
| Key Steps   | Classify action -> check authority -> validate rules -> decide      |
| Fails When  | Authority, evidence, vote, or required governance input is missing  |
| Name Rule   | Use for ACDC governance execution and enforcement                   |

---

# Objective

Execute and validate ACDC governance actions through repeatable rules for membership tiers, 4P lifecycle decisions, committee responsibility, voting, Board authority, inactivity enforcement, and AI-use disclosure.

# Trigger

Use this skill when:

- Running or preparing an ACDC Board or general body governance decision
- Evaluating member status, voting rights, or activity requirements
- Reviewing, approving, rejecting, or routing a 4P submission
- Assigning committees, roles, or leadership responsibility
- Enforcing inactivity, demotion, removal, or exception handling
- Checking whether AI-assisted work was disclosed and governed correctly

# Do Not Use When

- The request is a casual discussion with no governance action
- The organization is not ACDC or does not follow this governance model
- The user needs a contract document rather than governance enforcement
- Required facts such as member status, proposal scope, or voting context are missing

# Required Inputs

1. Governance action type: membership, 4P, committee, vote, enforcement, exception, or AI disclosure
2. Member or body involved
3. Current member status when relevant: RM, RAM, ERAM, BoD, inactive, or unknown
4. Proposal or decision text when relevant
5. Evidence of deliverables, participation, or active progress when relevant
6. Voting body and threshold when a vote is required

# Optional Inputs

1. Advisor input
2. Exception request
3. Committee assignment history
4. Tracker, Gantt, Drive, or Discord reference
5. AI summary report or disclosure package
6. Prior related governance decisions

# Outputs

1. Governance classification
2. Required authority level
3. Decision: approve, reject, revise, escalate, enforce, or request missing information
4. Rationale tied to the relevant governance rule
5. Required follow-up action
6. Recordkeeping note for the relevant tracker or meeting record

# Support Layers

- Put constitution, bylaws, policy excerpts, and meeting-rule references in `references/`.
- Put proposal templates, quad charts, or forms in `assets/`.
- Put vote tally helpers or tracker automation in `scripts/`.
- Keep private member records out of `skill.md`; reference where records should be checked instead.

# Procedure

## 1. Classify the Governance Action

1.1 Identify whether the request concerns membership, 4P review, committee execution, voting, enforcement, exception handling, or AI disclosure.
1.2 Identify the affected member, committee, proposal, or decision body.
1.3 Identify the requested output, such as approval, status change, vote result, or required revision.
1.4 If the action type is unclear, request clarification before applying rules.

## 2. Verify Authority

2.1 Determine the member or body authority level.
2.2 Apply the tier model:

- RM: limited participation; no voting or leadership authority
- RAM: voting, proposal, and leadership eligibility when requirements are met
- ERAM: RAM authority plus committee operation responsibility
- BoD: final governance authority within the rules

2.3 Reject or escalate actions that exceed the actor's authority.
2.4 If authority is unknown, request status evidence before deciding.

## 3. Evaluate 4P Actions

3.1 Confirm the 4P type: Project, Program, Proposal, or Presentation.
3.2 Confirm the submission includes problem statement, deliverables, resource needs, and review artifact such as a quad chart when required.
3.3 Route review through the correct bodies:

- RAM: feasibility or participation signal when applicable
- ERAM: technical or committee evaluation when applicable
- BoD: final approval authority

3.4 Return incomplete 4Ps for revision with missing items named explicitly.
3.5 Approve execution only after required authority and review gates are satisfied.

## 4. Evaluate Membership Status

4.1 Review deliverables, active progress, committee participation, and documented exceptions.
4.2 Apply the current membership criteria for RM, RAM, ERAM, and inactive status.
4.3 At review checkpoints, identify members who have not met requirements.
4.4 If requirements are unmet and no exception applies, recommend inactive status or another defined enforcement action.
4.5 For reactivation, require written request, contribution plan, and required approval.

## 5. Execute Committee Governance

5.1 Verify committee assignment requirements for BoD, ERAM, and RAM participants.
5.2 Confirm each committee has a plan of action and trackable deliverables.
5.3 Confirm committees report progress on the required cadence.
5.4 Escalate missing accountability to the responsible authority.

## 6. Execute Voting

6.1 Identify the voting body and threshold.
6.2 Confirm quorum or participation requirements when specified.
6.3 Classify the vote as simple majority, two-thirds, or another defined threshold.
6.4 Record the vote result and whether the motion passes.
6.5 If the Board has final authority, record whether the Board accepts, rejects, or overrides the recommendation.

## 7. Enforce AI Governance

7.1 Determine whether AI-assisted work was used.
7.2 Require disclosure when AI materially contributed to output, decisions, or evidence.
7.3 Check for an AI summary report when required, including prompts, outputs, decisions, and metadata.
7.4 Mark undisclosed or misrepresented AI-assisted work as invalid until corrected.

# Decision Logic

- IF the actor lacks authority, THEN reject or escalate the action.
- IF a 4P lacks required structure, THEN return it for revision.
- IF required deliverables are unmet and no exception applies, THEN recommend inactive or reduced status.
- IF no required vote or Board decision exists, THEN do not mark the action approved.
- IF AI-assisted work lacks required disclosure, THEN mark the output invalid until disclosure is supplied.
- IF governance facts are missing, THEN request the missing facts before deciding.

# Validation

The governance result is valid when:

1. The action type is identified.
2. The relevant authority level is named.
3. Required inputs are present or explicitly requested.
4. The decision maps to a stated membership, 4P, committee, vote, enforcement, or AI-disclosure rule.
5. Follow-up actions and recordkeeping requirements are stated.

# Rules

- Do not approve actions outside the actor's authority.
- Do not execute a 4P without required review and approval.
- Do not treat popularity or informal agreement as governance approval.
- Do not invent missing member status, vote results, deliverables, or exceptions.
- Do not accept undisclosed AI-assisted work when disclosure is required.
- Keep private records in their source system; do not copy sensitive member data into this skill.

# Failure Modes

- Missing member status: request status record before deciding.
- Vague 4P submission: return for revision with missing fields listed.
- Authority confusion: map the action to RM, RAM, ERAM, or BoD authority before proceeding.
- Fake or passive participation: require documented deliverables or active progress.
- Governance drift: require written decision records and Board confirmation when needed.
- Undisclosed AI use: require disclosure package before accepting the work.

# Dependencies

- ACDC Constitution and Bylaws
- Current membership roster or status tracker
- 4P templates and review artifacts
- Committee plans of action or tracker
- Voting records or meeting minutes
- AI disclosure policy and reports when AI was used

# Assumptions

- ACDC governance records exist outside this skill and can be consulted.
- Board authority and membership tiers are defined by current ACDC governing documents.
- This skill assists decision execution; it does not replace formal Board judgment.
- Sensitive member information should remain in approved record systems.

# Change Log

See CHANGELOG.md
