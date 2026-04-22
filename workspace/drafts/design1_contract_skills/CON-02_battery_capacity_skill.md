---
build_number: "001"
skill_id: "epcb.design1.battery_capacity"
name: "Battery Capacity"
description: "Select and size a lithium-ion main battery (12-19V operating range, under $200) that can supply sufficient transient current to cause measurable DC bus voltage dips during motor load events, enabling controlled brownout induction for prototype testing."
owner: "EPCB"
status: "active"
created_at: "2026-04-21"
last_updated: "2026-04-21"
source_contract_id: "CON-02"
---

# Objective

Select and size a lithium-ion main battery (12-19V operating range, under $200) that can supply sufficient transient current to cause measurable DC bus voltage dips during motor load events, enabling controlled brownout induction for prototype testing. Main battery feeds the UPS/BMS board (15-19V charging input) and the external peripheral rail. Battery specs are a required input for CON-01 (Cap Bank Sizing). External peripheral motor selection informs CON-03 (Power Path Architecture).

# Trigger

Use this skill when the team is executing `CON-02 — Battery Capacity` and needs a self-contained workflow that converts the filled contract into repeatable execution steps and proof-of-completion artifacts.

# Required Inputs

- Contract metadata: CON-02, hard deadline 5/14/26, tracker path `Design 1 > Contracts > Battery Capacity`.
- Scope-lock objective: Select and size a lithium-ion main battery (12-19V operating range, under $200) that can supply sufficient transient current to cause measurable DC bus voltage dips during motor load events, enabling controlled brownout induction for prototype testing.
- Interface context: Main battery feeds the UPS/BMS board (15-19V charging input) and the external peripheral rail. Battery specs are a required input for CON-01 (Cap Bank Sizing). External peripheral motor selection informs CON-03 (Power Path Architecture).
- Vendor-accessible product listings for lithium-ion batteries in the 12–19 V range under $200.
- Candidate external peripheral load options with estimated peak current draw.

# Optional Inputs

- Preferred tools, diagramming software, or coding environment chosen by the contractor.
- Existing bench hardware, simulation setup, or prior team notes that reduce execution time without changing scope.
- BoD clarifications for any source fields that were left blank in the contract header.

# Outputs

- PASS threshold: PASS: An Amazon (or equivalent vendor) product link is provided for a lithium-ion battery within 12-19V range and under $200, with documented specs (voltage, amp-hours, C-rate). An external peripheral (motor) candidate is also identified that will create sufficient current draw to dip the bus voltage measurably.
- Evidence item 1: Amazon/Vendor Link: Direct product link to the selected lithium-ion battery posted to Design 1 > Contracts > Battery Capacity folder.
- Evidence item 2: Spec Sheet: Document listing nominal voltage, amp-hours, max continuous and peak discharge current, and weight — confirming compatibility with 12-19V operating window.
- Evidence item 3: Motor Candidate: At least one external peripheral (motor) identified with estimated peak current draw (Amps) documented; sufficient to cause measurable bus voltage dip.
- Evidence item 4: Dependency Handoff: Battery specs shared with Bart/Christian (CON-01 team) via Discord or document upload confirming unblock of cap bank sizing.

# Support Layers

- Contract parsing layer: preserves the issued scope-lock fields and converts them into executable steps.
- Governance layer: keeps BoD approval boundaries, evidence requirements, and anti-scope-creep constraints intact.
- Traceability layer: carries contract ID, tracker path, dependency references, and PASS criteria into the skill.
- Delivery layer: maps validation criteria to uploadable artifacts, demonstrations, or handoff evidence.

# Procedure

## 1. Research the battery candidates

1.1 Search for lithium-ion battery options whose output voltage falls within 12–19 V and whose listed price is under $200.
1.2 Screen for enough discharge capability to support transient motor loads rather than only steady-state consumption.
1.3 Checkpoint: reject any candidate lacking published voltage or discharge information.

## 2. Select the main battery

2.1 Choose the candidate that best fits the voltage window, discharge needs, and budget constraint.
2.2 Capture the direct Amazon or equivalent vendor link.
2.3 Record nominal voltage, amp-hour rating, max discharge current or C-rate, dimensions, and weight.

## 3. Select the external peripheral load

3.1 Identify at least one motor or other peripheral expected to create intermittent high-current draws on the bus.
3.2 Estimate or document its expected peak current draw in amps.
3.3 Tie the load choice back to the goal of producing a measurable bus-voltage dip.

## 4. Write the rationale and dependency handoff

4.1 Summarize why the chosen battery and motor pair are adequate for induced-brownout testing.
4.2 Share the battery sizing rationale with Bart/Christian so CON-01 can proceed.
4.3 Checkpoint: confirm the shared handoff includes voltage, capacity, discharge, and load-current information.

## 5. Prepare completion evidence and notify BoD

5.1 Upload the vendor link and spec sheet to `Design 1 > Contracts > Battery Capacity`.
5.2 Document the selected motor candidate and expected peak current.
5.3 Notify BoD that the dependency handoff to CON-01 is complete and await sign-off.

# Decision Logic

- If a required upstream contract output is available, use it directly and cite it in the submission artifacts.
- If an upstream output is not yet available but the contract explicitly allows an assumption path, label the placeholder assumption and continue conservatively.
- If a missing dependency changes the PASS threshold or makes the submission unverifiable, stop and escalate to BoD.
- If a contractor attempts out-of-scope expansion, reject that work from completion evidence.

# Validation

- Verify the skill can be executed without opening the original contract document.
- Verify the PASS threshold is restated exactly: PASS: An Amazon (or equivalent vendor) product link is provided for a lithium-ion battery within 12-19V range and under $200, with documented specs (voltage, amp-hours, C-rate). An external peripheral (motor) candidate is also identified that will create sufficient current draw to dip the bus voltage measurably.
- Verify every OUT OF SCOPE item appears in the Rules section.
- Verify every validation criterion appears in Outputs and in the evidence-preparation or completion steps.
- Verify every referenced contract ID appears in Dependencies.

# Rules

- Do not perform or claim completion for out-of-scope work: Cap bank sizing or supercapacitor calculations — handled under CON-01.
- Do not perform or claim completion for out-of-scope work: Physical wiring or integration of the battery into the prototype circuit — addressed in CON-03.
- Do not perform or claim completion for out-of-scope work: Arbitration firmware or software — handled under CON-04.
- Do not perform or claim completion for out-of-scope work: Procurement approval or ordering — submit specs to BoD; ordering is a separate action.
- Do not treat unclaimed work as an active contract.
- Do not change the scope lock without BoD approval.
- Do not count work without uploaded evidence or demonstration as complete.
- For electrical or power-path work, de-energize hardware before any physical rework, probing changes, or wiring modifications.

# Failure Modes

- If this criterion cannot be satisfied, the contract does not PASS: Amazon/Vendor Link: Direct product link to the selected lithium-ion battery posted to Design 1 > Contracts > Battery Capacity folder.
- If this criterion cannot be satisfied, the contract does not PASS: Spec Sheet: Document listing nominal voltage, amp-hours, max continuous and peak discharge current, and weight — confirming compatibility with 12-19V operating window.
- If this criterion cannot be satisfied, the contract does not PASS: Motor Candidate: At least one external peripheral (motor) identified with estimated peak current draw (Amps) documented; sufficient to cause measurable bus voltage dip.
- If this criterion cannot be satisfied, the contract does not PASS: Dependency Handoff: Battery specs shared with Bart/Christian (CON-01 team) via Discord or document upload confirming unblock of cap bank sizing.
- If dependency CON-01 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.
- If dependency CON-03 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.
- If dependency CON-04 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.

# Dependencies

- CON-01: Cap bank specification and transient-energy sizing outputs. Interface/downstream dependency
- CON-03: Power-path diagram, rail split, and disconnect point definition. Interface/downstream dependency
- CON-04: Arbitration logic definition and disconnect-control behavior. Interface/downstream dependency

# Assumptions

- Any metadata field left blank in the source contract is preserved as `Unspecified`; deviation requires BoD confirmation.
- Tool choice is left to the contractor unless the contract names a required interface; deviation requires BoD confirmation.
- File naming and upload format may follow the team’s existing repository conventions as long as the required evidence is present; deviation requires BoD confirmation.

# Change Log

## V001
- Initial skill generated from CON-02 using the governed contract-to-skill workflow.
- Preserved blank or unspecified source fields explicitly instead of silently inventing values.

# Validation Criteria

1. Amazon/Vendor Link: Direct product link to the selected lithium-ion battery posted to Design 1 > Contracts > Battery Capacity folder.
2. Spec Sheet: Document listing nominal voltage, amp-hours, max continuous and peak discharge current, and weight — confirming compatibility with 12-19V operating window.
3. Motor Candidate: At least one external peripheral (motor) identified with estimated peak current draw (Amps) documented; sufficient to cause measurable bus voltage dip.
4. Dependency Handoff: Battery specs shared with Bart/Christian (CON-01 team) via Discord or document upload confirming unblock of cap bank sizing.

# Logging

- Contract ID: CON-02
- Skill ID: epcb.design1.battery_capacity
- 4P Code: Design1
- Tracker Path: Design 1 > Contracts > Battery Capacity
- Deliverable Name: Battery Capacity
- Issuing BoD: Bartek Broclawik
- Issue Date: 4/20/2026
- Hard Deadline: 5/14/26
- Contract Type: Unspecified
- Priority: Unspecified
- Applicable Majors: Unspecified
- Difficulty: Unspecified
- Contract Capacity: Contract Capacity:  Contract Capacity:
- Source File: CON-02_Battery_Capacity.docx
