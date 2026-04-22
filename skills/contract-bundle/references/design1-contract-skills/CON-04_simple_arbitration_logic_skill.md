---
build_number: "001"
skill_id: "epcb.design1.simple_arbitration_logic"
name: "Simple Arbitration Logic"
description: "Design and implement software/firmware arbitration logic that monitors DC bus voltage health and commands the peripheral rail disconnect when voltage drops toward the brownout threshold — protecting the Jetson Orin Nano from crashing while the supercap bank is depleted under extended motor load."
owner: "EPCB"
status: "active"
created_at: "2026-04-21"
last_updated: "2026-04-21"
source_contract_id: "CON-04"
---

# Objective

Design and implement software/firmware arbitration logic that monitors DC bus voltage health and commands the peripheral rail disconnect when voltage drops toward the brownout threshold — protecting the Jetson Orin Nano from crashing while the supercap bank is depleted under extended motor load. Interfaces with the power path defined in CON-03 — controls the switch/disconnect on the external peripheral rail. Runs on the Jetson Orin Nano or a dedicated microcontroller (Arduino/STM32). Requires voltage monitoring input (ADC or I2C voltage monitor). Arbitration output is the final stage of the three-test-scenario demonstration.

# Trigger

Use this skill when the team is executing `CON-04 — Simple Arbitration Logic` and needs a self-contained workflow that converts the filled contract into repeatable execution steps and proof-of-completion artifacts.

# Required Inputs

- Contract metadata: CON-04, hard deadline 5/14/26, tracker path `Design 1 > Contracts > Simple Arbitration Logic`.
- Scope-lock objective: Design and implement software/firmware arbitration logic that monitors DC bus voltage health and commands the peripheral rail disconnect when voltage drops toward the brownout threshold — protecting the Jetson Orin Nano from crashing while the supercap bank is depleted under extended motor load.
- Interface context: Interfaces with the power path defined in CON-03 — controls the switch/disconnect on the external peripheral rail. Runs on the Jetson Orin Nano or a dedicated microcontroller (Arduino/STM32). Requires voltage monitoring input (ADC or I2C voltage monitor). Arbitration output is the final stage of the three-test-scenario demonstration.
- Disconnect point from CON-03.
- Voltage monitoring source (ADC, I2C monitor, or UPS monitoring pins).
- Execution target: Jetson Orin Nano or dedicated microcontroller.

# Optional Inputs

- Preferred tools, diagramming software, or coding environment chosen by the contractor.
- Existing bench hardware, simulation setup, or prior team notes that reduce execution time without changing scope.
- BoD clarifications for any source fields that were left blank in the contract header.

# Outputs

- PASS threshold: PASS: Working code or pseudocode is delivered that: (1) reads or simulates bus voltage input, (2) triggers a shutoff/disconnect signal when voltage drops to or below a defined threshold (target ~10V), and (3) is demonstrated on a bench test or simulation showing the peripheral rail being disconnected before the Jetson browns out.
- Evidence item 1: Code/Logic Upload: Arbitration code or pseudocode uploaded to Design 1 > Contracts > Simple Arbitration Logic folder (GitHub link or file accepted).
- Evidence item 2: Decision Flow: A simple diagram or flowchart showing the monitoring loop, threshold check, and shutoff action is included with the submission.
- Evidence item 3: Bench Demo or Simulation: Video or live demonstration showing the arbitration logic triggering a peripheral disconnect when voltage drops to the defined threshold — can be simulated with a voltage divider or variable bench supply standing in for the bus.
- Evidence item 4: Threshold Documentation: Threshold voltage values (disconnect and reconnect) are clearly stated in code comments or accompanying doc, with justification tied to Jetson Orin Nano operating range.

# Support Layers

- Contract parsing layer: preserves the issued scope-lock fields and converts them into executable steps.
- Governance layer: keeps BoD approval boundaries, evidence requirements, and anti-scope-creep constraints intact.
- Traceability layer: carries contract ID, tracker path, dependency references, and PASS criteria into the skill.
- Delivery layer: maps validation criteria to uploadable artifacts, demonstrations, or handoff evidence.

# Procedure

## 1. Define arbitration thresholds

1.1 Set the disconnect threshold and hysteresis/reconnect threshold, targeting a brownout-protection trigger near 10 V.
1.2 Tie the chosen values to the Jetson Orin Nano operating range and document the justification.
1.3 Checkpoint: thresholds must be written into code comments or accompanying documentation before demo.

## 2. Implement voltage monitoring

2.1 Build the monitoring loop that reads bus voltage from an ADC, I2C voltage monitor, or UPS monitoring pins.
2.2 Choose a polling rate sufficient to observe the relevant transient event.
2.3 If the input is simulated rather than physical, document how the simulation maps to bus-voltage behavior.

## 3. Implement the disconnect action

3.1 Generate the shutoff/disconnect command using the switch point defined in CON-03.
3.2 Support execution on the Jetson Orin Nano or a dedicated microcontroller such as Arduino or STM32.
3.3 Apply simple threshold-based on/off arbitration only; do not expand into advanced control.

## 4. Document the control logic

4.1 Produce a decision flow diagram showing voltage read, threshold comparison, disconnect decision, and reconnect logic.
4.2 Document the code or pseudocode structure well enough for team review.
4.3 Checkpoint: confirm the logic diagram matches the actual implementation or pseudocode submitted.

## 5. Prepare completion evidence and notify BoD

5.1 Upload the code or pseudocode to `Design 1 > Contracts > Simple Arbitration Logic`.
5.2 Run a bench demo or simulation proving the peripheral rail disconnect occurs before Jetson brownout.
5.3 Notify BoD that the arbitration package is ready for review and await sign-off.

# Decision Logic

- If a required upstream contract output is available, use it directly and cite it in the submission artifacts.
- If an upstream output is not yet available but the contract explicitly allows an assumption path, label the placeholder assumption and continue conservatively.
- If a missing dependency changes the PASS threshold or makes the submission unverifiable, stop and escalate to BoD.
- If a contractor attempts out-of-scope expansion, reject that work from completion evidence.

# Validation

- Verify the skill can be executed without opening the original contract document.
- Verify the PASS threshold is restated exactly: PASS: Working code or pseudocode is delivered that: (1) reads or simulates bus voltage input, (2) triggers a shutoff/disconnect signal when voltage drops to or below a defined threshold (target ~10V), and (3) is demonstrated on a bench test or simulation showing the peripheral rail being disconnected before the Jetson browns out.
- Verify every OUT OF SCOPE item appears in the Rules section.
- Verify every validation criterion appears in Outputs and in the evidence-preparation or completion steps.
- Verify every referenced contract ID appears in Dependencies.

# Rules

- Do not perform or claim completion for out-of-scope work: Physical switching hardware or relay circuit design — hardware implementation is a follow-on assembly task after contract completion.
- Do not perform or claim completion for out-of-scope work: Cap bank sizing or power path routing — handled under CON-01 and CON-03 respectively.
- Do not perform or claim completion for out-of-scope work: UI dashboard, data logging, or oscilloscope integration — out of scope for MVP; collect voltage data through existing UPS board monitoring if needed.
- Do not perform or claim completion for out-of-scope work: Full closed-loop PID or advanced control — arbitration is a simple threshold-based on/off switch for MVP.
- Do not treat unclaimed work as an active contract.
- Do not change the scope lock without BoD approval.
- Do not count work without uploaded evidence or demonstration as complete.
- For electrical or power-path work, de-energize hardware before any physical rework, probing changes, or wiring modifications.

# Failure Modes

- If this criterion cannot be satisfied, the contract does not PASS: Code/Logic Upload: Arbitration code or pseudocode uploaded to Design 1 > Contracts > Simple Arbitration Logic folder (GitHub link or file accepted).
- If this criterion cannot be satisfied, the contract does not PASS: Decision Flow: A simple diagram or flowchart showing the monitoring loop, threshold check, and shutoff action is included with the submission.
- If this criterion cannot be satisfied, the contract does not PASS: Bench Demo or Simulation: Video or live demonstration showing the arbitration logic triggering a peripheral disconnect when voltage drops to the defined threshold — can be simulated with a voltage divider or variable bench supply standing in for the bus.
- If this criterion cannot be satisfied, the contract does not PASS: Threshold Documentation: Threshold voltage values (disconnect and reconnect) are clearly stated in code comments or accompanying doc, with justification tied to Jetson Orin Nano operating range.
- If dependency CON-01 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.
- If dependency CON-03 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.

# Dependencies

- CON-01: Cap bank specification and transient-energy sizing outputs. Interface/downstream dependency
- CON-03: Power-path diagram, rail split, and disconnect point definition. Hard prerequisite

# Assumptions

- Any metadata field left blank in the source contract is preserved as `Unspecified`; deviation requires BoD confirmation.
- Tool choice is left to the contractor unless the contract names a required interface; deviation requires BoD confirmation.
- File naming and upload format may follow the team’s existing repository conventions as long as the required evidence is present; deviation requires BoD confirmation.

# Change Log

## V001
- Initial skill generated from CON-04 using the governed contract-to-skill workflow.
- Preserved blank or unspecified source fields explicitly instead of silently inventing values.

# Validation Criteria

1. Code/Logic Upload: Arbitration code or pseudocode uploaded to Design 1 > Contracts > Simple Arbitration Logic folder (GitHub link or file accepted).
2. Decision Flow: A simple diagram or flowchart showing the monitoring loop, threshold check, and shutoff action is included with the submission.
3. Bench Demo or Simulation: Video or live demonstration showing the arbitration logic triggering a peripheral disconnect when voltage drops to the defined threshold — can be simulated with a voltage divider or variable bench supply standing in for the bus.
4. Threshold Documentation: Threshold voltage values (disconnect and reconnect) are clearly stated in code comments or accompanying doc, with justification tied to Jetson Orin Nano operating range.

# Logging

- Contract ID: CON-04
- Skill ID: epcb.design1.simple_arbitration_logic
- 4P Code: Design1
- Tracker Path: Design 1 > Contracts > Simple Arbitration Logic
- Deliverable Name: Simple Arbitration Logic
- Issuing BoD: Bartek Broclawik
- Issue Date: 4/20/2026
- Hard Deadline: 5/14/26
- Contract Type: Unspecified
- Priority: Unspecified
- Applicable Majors: CS [ ]  CE [ ]  EE [ ]  ME [ ]  Other(s): —
- Difficulty: Easy [ ]  Intermediate [ ]  Advanced [ ]
- Contract Capacity: Applicable Major(s): CS [ ]  CE [ ]  EE [ ]  ME [ ]  Other(s): —          Difficulty: Easy [ ]  Intermediate [ ]  Advanced [ ]  Contract Capacity:  Applicable Major(s): CS [ ]  CE [ ]  EE [ ]  ME [ ]  Other(s): —          Difficulty: Easy [ ]  Intermediate [ ]  Advanced [ ]  Contract Capacity:
- Source File: CON-04_Simple_Arbitration_Logic.docx
