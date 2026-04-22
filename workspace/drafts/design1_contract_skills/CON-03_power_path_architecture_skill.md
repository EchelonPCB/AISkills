---
build_number: "001"
skill_id: "epcb.design1.power_path_architecture"
name: "Power Path Architecture"
description: "Define and document the complete power delivery path from the main battery through the UPS/BMS board to the Jetson Orin Nano compute rail and external peripheral rail, including the supercapacitor injection point and bus voltage node labels — producing the architecture diagram used for all subsequent prototype integration."
owner: "EPCB"
status: "active"
created_at: "2026-04-21"
last_updated: "2026-04-21"
source_contract_id: "CON-03"
---

# Objective

Define and document the complete power delivery path from the main battery through the UPS/BMS board to the Jetson Orin Nano compute rail and external peripheral rail, including the supercapacitor injection point and bus voltage node labels — producing the architecture diagram used for all subsequent prototype integration. Consumes outputs from CON-01 (cap bank spec) and CON-02 (battery selection). Diagram feeds directly into CON-04 (Arbitration Logic) to define where the switch/disconnect is placed. Serves as the build blueprint for prototype assembly.

# Trigger

Use this skill when the team is executing `CON-03 — Power Path Architecture` and needs a self-contained workflow that converts the filled contract into repeatable execution steps and proof-of-completion artifacts.

# Required Inputs

- Contract metadata: CON-03, hard deadline 5/14/26, tracker path `Design 1 > Contracts > Power Path`.
- Scope-lock objective: Define and document the complete power delivery path from the main battery through the UPS/BMS board to the Jetson Orin Nano compute rail and external peripheral rail, including the supercapacitor injection point and bus voltage node labels — producing the architecture diagram used for all subsequent prototype integration.
- Interface context: Consumes outputs from CON-01 (cap bank spec) and CON-02 (battery selection). Diagram feeds directly into CON-04 (Arbitration Logic) to define where the switch/disconnect is placed. Serves as the build blueprint for prototype assembly.
- Cap bank output from CON-01 or an explicit placeholder if still pending.
- Battery output from CON-02 or an explicit placeholder if still pending.
- Known UPS/BMS and Jetson rail voltage ranges used by the team.

# Optional Inputs

- Preferred tools, diagramming software, or coding environment chosen by the contractor.
- Existing bench hardware, simulation setup, or prior team notes that reduce execution time without changing scope.
- BoD clarifications for any source fields that were left blank in the contract header.

# Outputs

- PASS threshold: PASS: A finalized power path architecture diagram is delivered showing: main battery, UPS/BMS board, Jetson Orin Nano compute rail, external peripheral rail, supercap bank placement, and labeled voltage nodes (nominal, min 10V). Diagram must be clear enough to serve as the build reference for the team.
- Evidence item 1: Diagram Upload: Final power path architecture diagram (PNG, PDF, or draw.io export) uploaded to Design 1 > Contracts > Power Path folder.
- Evidence item 2: Completeness Check: Diagram includes all required nodes — main battery, UPS/BMS, compute rail, peripheral rail, cap bank, arbitration disconnect point, and voltage labels.
- Evidence item 3: Voltage Labels: All critical voltage nodes are labeled on the diagram (nominal battery voltage, 10V minimum threshold, UPS output range 9-12.6V, peripheral rail).
- Evidence item 4: Arbitration Handoff: Arbitration switch/disconnect point is clearly marked and documented for CON-04 team — confirmed via diagram annotation or written note.

# Support Layers

- Contract parsing layer: preserves the issued scope-lock fields and converts them into executable steps.
- Governance layer: keeps BoD approval boundaries, evidence requirements, and anti-scope-creep constraints intact.
- Traceability layer: carries contract ID, tracker path, dependency references, and PASS criteria into the skill.
- Delivery layer: maps validation criteria to uploadable artifacts, demonstrations, or handoff evidence.

# Procedure

## 1. Draft the baseline architecture diagram

1.1 Create the initial power path diagram covering the main battery, UPS/BMS board, Jetson Orin Nano compute rail, external peripheral rail, and supercap bank.
1.2 Because the first IN SCOPE row is blank in the source contract, treat the baseline diagram-creation step as a conservative assumption; deviation requires BoD confirmation.
1.3 Checkpoint: do not invent extra subsystems beyond what the contract and known hardware require.

## 2. Label voltage nodes and conversion stages

2.1 Label battery nominal voltage, UPS output range, compute rail, peripheral rail, and the 10 V minimum bus threshold.
2.2 Mark any buck converters or regulators required along the path.
2.3 Ensure the node labels are readable enough to serve as a build reference.

## 3. Place the cap bank

3.1 Identify the physical placement of the cap bank relative to the UPS board and peripheral rail split.
3.2 State whether the cap bank sits before or after the BMS based on the chosen architecture.
3.3 Tie the placement back to the outputs of CON-01 and CON-02.

## 4. Define the arbitration interface

4.1 Mark the peripheral-rail disconnect point where CON-04 arbitration logic will take control.
4.2 Annotate the switch/disconnect point clearly enough that the control team can implement against it without reinterpretation.
4.3 Checkpoint: verify the disconnect point is shown on the same diagram as the voltage nodes.

## 5. Prepare completion evidence and notify BoD

5.1 Export the finalized diagram as PNG, PDF, or draw.io output and upload it to `Design 1 > Contracts > Power Path`.
5.2 Include a short written note if needed to clarify the arbitration handoff to CON-04.
5.3 Notify BoD that the architecture diagram is ready for review and await sign-off.

# Decision Logic

- If a required upstream contract output is available, use it directly and cite it in the submission artifacts.
- If an upstream output is not yet available but the contract explicitly allows an assumption path, label the placeholder assumption and continue conservatively.
- If a missing dependency changes the PASS threshold or makes the submission unverifiable, stop and escalate to BoD.
- If a contractor attempts out-of-scope expansion, reject that work from completion evidence.

# Validation

- Verify the skill can be executed without opening the original contract document.
- Verify the PASS threshold is restated exactly: PASS: A finalized power path architecture diagram is delivered showing: main battery, UPS/BMS board, Jetson Orin Nano compute rail, external peripheral rail, supercap bank placement, and labeled voltage nodes (nominal, min 10V). Diagram must be clear enough to serve as the build reference for the team.
- Verify every OUT OF SCOPE item appears in the Rules section.
- Verify every validation criterion appears in Outputs and in the evidence-preparation or completion steps.
- Verify every referenced contract ID appears in Dependencies.

# Rules

- Do not perform or claim completion for out-of-scope work: Arbitration firmware or monitoring logic — handled under CON-04 (Simple Arbitration Logic).
- Do not perform or claim completion for out-of-scope work: Cap bank sizing calculations — handled under CON-01; diagram uses CON-01 output as input.
- Do not perform or claim completion for out-of-scope work: Battery selection — handled under CON-02; diagram uses CON-02 output as input.
- Do not perform or claim completion for out-of-scope work: Physical prototype assembly or wiring — diagram is the blueprint; assembly is a follow-on task after all 4 contracts complete.
- Do not treat unclaimed work as an active contract.
- Do not change the scope lock without BoD approval.
- Do not count work without uploaded evidence or demonstration as complete.
- For electrical or power-path work, de-energize hardware before any physical rework, probing changes, or wiring modifications.

# Failure Modes

- The first IN SCOPE row in the source contract is blank. Recovery: preserve this as an assumption, keep the procedure conservative, and raise to BoD if a more specific task definition is needed.
- If this criterion cannot be satisfied, the contract does not PASS: Diagram Upload: Final power path architecture diagram (PNG, PDF, or draw.io export) uploaded to Design 1 > Contracts > Power Path folder.
- If this criterion cannot be satisfied, the contract does not PASS: Completeness Check: Diagram includes all required nodes — main battery, UPS/BMS, compute rail, peripheral rail, cap bank, arbitration disconnect point, and voltage labels.
- If this criterion cannot be satisfied, the contract does not PASS: Voltage Labels: All critical voltage nodes are labeled on the diagram (nominal battery voltage, 10V minimum threshold, UPS output range 9-12.6V, peripheral rail).
- If this criterion cannot be satisfied, the contract does not PASS: Arbitration Handoff: Arbitration switch/disconnect point is clearly marked and documented for CON-04 team — confirmed via diagram annotation or written note.
- If dependency CON-01 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.
- If dependency CON-02 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.
- If dependency CON-04 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.

# Dependencies

- CON-01: Cap bank specification and transient-energy sizing outputs. Hard prerequisite
- CON-02: Battery selection, voltage window, and motor-load parameters. Hard prerequisite
- CON-04: Arbitration logic definition and disconnect-control behavior. Hard prerequisite

# Assumptions

- Any metadata field left blank in the source contract is preserved as `Unspecified`; deviation requires BoD confirmation.
- Tool choice is left to the contractor unless the contract names a required interface; deviation requires BoD confirmation.
- File naming and upload format may follow the team’s existing repository conventions as long as the required evidence is present; deviation requires BoD confirmation.
- The blank first IN SCOPE row is interpreted conservatively as the baseline task of drafting the architecture diagram itself; deviation requires BoD confirmation.

# Change Log

## V001
- Initial skill generated from CON-03 using the governed contract-to-skill workflow.
- Preserved blank or unspecified source fields explicitly instead of silently inventing values.

# Validation Criteria

1. Diagram Upload: Final power path architecture diagram (PNG, PDF, or draw.io export) uploaded to Design 1 > Contracts > Power Path folder.
2. Completeness Check: Diagram includes all required nodes — main battery, UPS/BMS, compute rail, peripheral rail, cap bank, arbitration disconnect point, and voltage labels.
3. Voltage Labels: All critical voltage nodes are labeled on the diagram (nominal battery voltage, 10V minimum threshold, UPS output range 9-12.6V, peripheral rail).
4. Arbitration Handoff: Arbitration switch/disconnect point is clearly marked and documented for CON-04 team — confirmed via diagram annotation or written note.

# Logging

- Contract ID: CON-03
- Skill ID: epcb.design1.power_path_architecture
- 4P Code: Design1
- Tracker Path: Design 1 > Contracts > Power Path
- Deliverable Name: Power Path Architecture
- Issuing BoD: Bartek Broclawik
- Issue Date: 4/20/2026
- Hard Deadline: 5/14/26
- Contract Type: Unspecified
- Priority: Unspecified
- Applicable Majors: Unspecified
- Difficulty: Unspecified
- Contract Capacity: Contract Capacity:  Contract Capacity:
- Source File: CON-03_Power_Path_Architecture.docx
