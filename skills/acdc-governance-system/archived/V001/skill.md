---
build_number: "001"
skill_id: "acdc.governance.acdc_governance_system"
name: "acdc-governance-system"
description: "Execute, enforce, and manage ACDC governance including membership, voting, 4Ps lifecycle, and Board authority."
trigger_keywords: "acdc governance, membership enforcement, 4Ps approval, board voting, club operations, committee structure, status management"
owner: "ACDC"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-19"
---
Index
Field	Detail
Trigger	Need to run ACDC operations, enforce membership, approve 4Ps
Input	Member actions, proposals, status data, governance decisions
Output	Decisions, status updates, approvals, enforcement actions
Core System	4Ps lifecycle + membership tiers + BoD authority
Failure	Lack of enforcement, unclear authority, inactive members
Objective

Operate ACDC as a structured governance system, ensuring all activities (Projects, Programs, Proposals, Presentations) are executed through enforceable rules, validated participation, and Board-controlled decision-making.

Trigger

Use this skill when:

Running ACDC meetings (BoD or GBM)
Evaluating member status (RM, RAM, ERAM)
Approving or rejecting 4Ps
Assigning committees or roles
Enforcing inactivity or demotions
Making governance decisions (votes, amendments, impeachment)
Do Not Use When
Casual discussion without execution
Brainstorming without defined outputs
Non-ACDC related orgs or governance systems
Required Inputs
Member status data (RM / RAM / ERAM)
Proposed 4P (Proposal, Program, Project, Presentation)
Deliverable tracking (completed / active progress)
Committee assignments
BoD availability for vote
Optional Inputs
Exception requests (for inactivity)
Advisor input
External collaboration proposals
AI usage reports (if applicable)
Outputs
Approved / Rejected 4Ps
Member promotions / demotions
Committee assignments
Voting outcomes
Enforcement actions (inactive status, removal)
Governance records (logged decisions)
Support Layers
references/ → Constitution + Bylaws
assets/ → Templates (Quad Charts, Proposals)
scripts/ → Voting tools, tracking systems (future)
Procedure
1. Intake Governance Action
Identify request type:
4P submission
Membership evaluation
Committee assignment
Governance vote
Enforcement action
2. Validate Membership Authority

IF member is:

RM → no voting, cannot lead
RAM → can vote, propose, lead
ERAM → can vote + operate committees
BoD → full authority

Reject actions outside authority.

3. Execute 4P Lifecycle
3.1 Proposal Intake

Require:

Problem statement
Deliverables
Resource needs
Quad chart (or equivalent)
3.2 Voting Structure
RAM → feasibility / participation
ERAM → technical evaluation
BoD → final authority

Decision = BoD controlled

4. Membership Enforcement
4.1 Evaluate Deliverables
RM → ≥1 deliverable or active progress
RAM → ≥2 deliverables OR 1 + active progress
ERAM → RAM requirements + committee participation
4.2 Mid-Semester Review (Week 8)

IF requirements NOT met AND no exception:

→ Reclassify as Inactive

5. Inactive Enforcement

Immediate effects:

Remove voting rights
Remove committee roles
Remove leadership ability

Reactivation requires:

Written request
Plan to contribute
BoD approval
6. Committee Execution

Assign:

BoD → 2 committees minimum
ERAM → 1 committee required
RAM → ≥1 committee

Each committee must:

Maintain Plan of Action
Track deliverables (Gantt or equivalent)
Report monthly
7. Voting Execution
Voting Types:
Simple majority (>50%)
Two-thirds (≥66.7%)
Used for:
Promotions
4P approvals
Amendments
Removal / impeachment
8. AI Governance Enforcement

If AI used:

Require AI Summary Report:
prompts
outputs
decisions
metadata

Reject work if:

Misrepresented as fully original
No disclosure
9. Board Authority Execution

BoD can:

Approve/reject all 4Ps
Override member votes (except elections/impeachment)
Assign roles and committees
Enforce status changes
Approve exceptions

Chairperson can override decisions (with limits).

Decision Logic
IF member lacks authority → reject action
IF 4P lacks structure → return for revision
IF deliverables unmet → inactive status
IF no BoD vote → no approval
IF AI used without disclosure → invalid output
Validation

System is valid if:

All actions map to membership tier authority
All 4Ps go through BoD
Deliverables are tracked
Mid-semester enforcement occurs
All decisions are recorded
Rules
No participation without deliverables
No voting without RAM+ status
No 4P execution without approval
No committee without accountability
No AI use without disclosure
Failure Modes
1. Passive Members

→ Fix: enforce deliverables + Week 8 review

2. Scope Creep

→ Fix: BoD approval gate

3. Authority Confusion

→ Fix: strict tier-based permissions

4. Fake Participation

→ Fix: require documented progress

5. Governance Drift

→ Fix: BoD enforcement + monthly reporting

Dependencies
ACDC Constitution & Bylaws
4P Templates (Quad Charts, etc.)
Tracking system (Gantt / task board)
Communication platform (Discord / Drive)
Assumptions
BoD is active and responsive
Deliverables are trackable
Members operate within defined roles
Governance > popularity