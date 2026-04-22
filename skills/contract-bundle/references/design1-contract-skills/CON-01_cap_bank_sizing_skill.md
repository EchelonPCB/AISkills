---
build_number: "001"
skill_id: "epcb.design1.cap_bank_sizing"
name: "Cap Bank Sizing"
description: "Calculate and specify the supercapacitor bank configuration (number of cells, capacitance, voltage rating, series/parallel arrangement) required to absorb DC bus transient events and prevent the bus from dropping below 10V during motor surge loads on the Jetson Orin Nano system."
owner: "EPCB"
status: "active"
created_at: "2026-04-21"
last_updated: "2026-04-21"
source_contract_id: "CON-01"
---

# Objective

Calculate and specify the supercapacitor bank configuration (number of cells, capacitance, voltage rating, series/parallel arrangement) required to absorb DC bus transient events and prevent the bus from dropping below 10V during motor surge loads on the Jetson Orin Nano system. Feeds into CON-03 (Power Path Architecture) for physical placement. Dependent on battery selection from CON-02 (Battery Capacity) for transient event parameters. Supercap bank connects in parallel with the main DC bus between the battery and UPS/BMS board.

# Trigger

Use this skill when the team is executing `CON-01 — Cap Bank Sizing` and needs a self-contained workflow that converts the filled contract into repeatable execution steps and proof-of-completion artifacts.

# Required Inputs

- Contract metadata: CON-01, hard deadline 5/14/26, tracker path `Design 1 > Contracts > Cap Bank`.
- Scope-lock objective: Calculate and specify the supercapacitor bank configuration (number of cells, capacitance, voltage rating, series/parallel arrangement) required to absorb DC bus transient events and prevent the bus from dropping below 10V during motor surge loads on the Jetson Orin Nano system.
- Interface context: Feeds into CON-03 (Power Path Architecture) for physical placement. Dependent on battery selection from CON-02 (Battery Capacity) for transient event parameters. Supercap bank connects in parallel with the main DC bus between the battery and UPS/BMS board.
- Battery selection from CON-02, or a clearly labeled placeholder assumption if CON-02 is not yet complete.
- Motor transient assumptions: expected current spike, event duration, and allowable voltage sag to 10 V minimum.

# Optional Inputs

- Preferred tools, diagramming software, or coding environment chosen by the contractor.
- Existing bench hardware, simulation setup, or prior team notes that reduce execution time without changing scope.
- BoD clarifications for any source fields that were left blank in the contract header.

# Outputs

- PASS threshold: PASS: A calculation document is delivered showing: (1) derived capacitance value using standard HESS/engineering equations, (2) cell count and series/parallel configuration, (3) ESR and voltage-trading considerations, and (4) minimum voltage threshold of 10V validated against expected transient draw.
- Evidence item 1: Document Upload: Calculation sheet with all equations, values, and final cap bank specification submitted to Design 1 > Contracts > Cap Bank folder.
- Evidence item 2: Review: Equations correctly reference supercap sizing formula (C = I*dt / dV) with numerical inputs sourced from motor load specs and 10V minimum threshold.
- Evidence item 3: Spec Table: Final output includes a clear table listing cell count, capacitance per cell, series/parallel arrangement, voltage rating, and ESR value.
- Evidence item 4: Dependency Sign-off: Battery capacity spec from CON-02 is referenced or assumed value is documented as a placeholder pending CON-02 output.

# Support Layers

- Contract parsing layer: preserves the issued scope-lock fields and converts them into executable steps.
- Governance layer: keeps BoD approval boundaries, evidence requirements, and anti-scope-creep constraints intact.
- Traceability layer: carries contract ID, tracker path, dependency references, and PASS criteria into the skill.
- Delivery layer: maps validation criteria to uploadable artifacts, demonstrations, or handoff evidence.

# Procedure

## 1. Establish the transient design case

1.1 Collect the RC car motor use case assumptions that define the surge event: expected current spike, event duration, and maximum allowable voltage dip.
1.2 Set the minimum bus threshold to 10 V as the non-negotiable protection floor.
1.3 If CON-02 is incomplete, document a placeholder battery assumption and mark it as provisional before continuing.

## 2. Select and apply sizing equations

2.1 Use the relevant supercapacitor sizing equations from the HES standard or project proposal report.
2.2 At minimum, evaluate the baseline relation `C = I·dt / dV` and note any additional ESR or voltage-derating checks used.
2.3 Checkpoint: confirm every variable has units and a defensible source before calculating.

## 3. Compute the bank configuration

3.1 Calculate required capacitance in farads using the transient load case.
3.2 Determine the required voltage rating and account for the series/parallel arrangement needed to satisfy the 10 V minimum bus threshold.
3.3 Estimate ESR impact and note any trade between capacitance, series count, and voltage margin.

## 4. Package the result for handoff

4.1 Create a written calculation sheet that shows equations, substitutions, assumptions, intermediate values, and final outputs.
4.2 Produce a clear final specification table listing cell count, capacitance per cell, total effective capacitance, voltage rating, arrangement, and ESR.
4.3 Prepare the result for upload to the Cap Bank contract folder.

## 5. Prepare completion evidence and notify BoD

5.1 Upload the calculation document to `Design 1 > Contracts > Cap Bank`.
5.2 Ensure the submission explicitly references CON-02 output or the placeholder assumption used.
5.3 Notify BoD that the sizing package is ready for review and await sign-off.

# Decision Logic

- If a required upstream contract output is available, use it directly and cite it in the submission artifacts.
- If an upstream output is not yet available but the contract explicitly allows an assumption path, label the placeholder assumption and continue conservatively.
- If a missing dependency changes the PASS threshold or makes the submission unverifiable, stop and escalate to BoD.
- If a contractor attempts out-of-scope expansion, reject that work from completion evidence.

# Validation

- Verify the skill can be executed without opening the original contract document.
- Verify the PASS threshold is restated exactly: PASS: A calculation document is delivered showing: (1) derived capacitance value using standard HESS/engineering equations, (2) cell count and series/parallel configuration, (3) ESR and voltage-trading considerations, and (4) minimum voltage threshold of 10V validated against expected transient draw.
- Verify every OUT OF SCOPE item appears in the Rules section.
- Verify every validation criterion appears in Outputs and in the evidence-preparation or completion steps.
- Verify every referenced contract ID appears in Dependencies.

# Rules

- Do not perform or claim completion for out-of-scope work: Physical procurement of supercapacitors — purchasing is handled after sizing is confirmed (separate BOM action).
- Do not perform or claim completion for out-of-scope work: PCB or circuit layout of the cap bank — physical integration is addressed in CON-03 (Power Path).
- Do not perform or claim completion for out-of-scope work: Arbitration logic or software — handled under CON-04 (Simple Arbitration Logic).
- Do not perform or claim completion for out-of-scope work: Battery selection or sizing — handled under CON-02 (Battery Capacity).
- Do not treat unclaimed work as an active contract.
- Do not change the scope lock without BoD approval.
- Do not count work without uploaded evidence or demonstration as complete.
- For electrical or power-path work, de-energize hardware before any physical rework, probing changes, or wiring modifications.

# Failure Modes

- If this criterion cannot be satisfied, the contract does not PASS: Document Upload: Calculation sheet with all equations, values, and final cap bank specification submitted to Design 1 > Contracts > Cap Bank folder.
- If this criterion cannot be satisfied, the contract does not PASS: Review: Equations correctly reference supercap sizing formula (C = I*dt / dV) with numerical inputs sourced from motor load specs and 10V minimum threshold.
- If this criterion cannot be satisfied, the contract does not PASS: Spec Table: Final output includes a clear table listing cell count, capacitance per cell, series/parallel arrangement, voltage rating, and ESR value.
- If this criterion cannot be satisfied, the contract does not PASS: Dependency Sign-off: Battery capacity spec from CON-02 is referenced or assumed value is documented as a placeholder pending CON-02 output.
- If dependency CON-02 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.
- If dependency CON-03 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.
- If dependency CON-04 is incomplete or unavailable, proceed only with an explicitly labeled placeholder assumption or stop and escalate to BoD when the dependency is hard-blocking.

# Dependencies

- CON-02: Battery selection, voltage window, and motor-load parameters. Hard prerequisite
- CON-03: Power-path diagram, rail split, and disconnect point definition. Hard prerequisite
- CON-04: Arbitration logic definition and disconnect-control behavior. Interface/downstream dependency

# Assumptions

- Any metadata field left blank in the source contract is preserved as `Unspecified`; deviation requires BoD confirmation.
- Tool choice is left to the contractor unless the contract names a required interface; deviation requires BoD confirmation.
- File naming and upload format may follow the team’s existing repository conventions as long as the required evidence is present; deviation requires BoD confirmation.
- The HES/HESS equation source is assumed to be the project proposal report or referenced standard available to the team; deviation requires BoD confirmation.

# Change Log

## V001
- Initial skill generated from CON-01 using the governed contract-to-skill workflow.
- Preserved blank or unspecified source fields explicitly instead of silently inventing values.

# Validation Criteria

1. Document Upload: Calculation sheet with all equations, values, and final cap bank specification submitted to Design 1 > Contracts > Cap Bank folder.
2. Review: Equations correctly reference supercap sizing formula (C = I*dt / dV) with numerical inputs sourced from motor load specs and 10V minimum threshold.
3. Spec Table: Final output includes a clear table listing cell count, capacitance per cell, series/parallel arrangement, voltage rating, and ESR value.
4. Dependency Sign-off: Battery capacity spec from CON-02 is referenced or assumed value is documented as a placeholder pending CON-02 output.

# Logging

- Contract ID: CON-01
- Skill ID: epcb.design1.cap_bank_sizing
- 4P Code: Design1
- Tracker Path: Design 1 > Contracts > Cap Bank
- Deliverable Name: Cap Bank Sizing
- Issuing BoD: Bartek Broclawik
- Issue Date: 4/20/2026
- Hard Deadline: 5/14/26
- Contract Type: Unspecified
- Priority: Unspecified
- Applicable Majors: Unspecified
- Difficulty: Unspecified
- Contract Capacity: [Contract Capacity:  [Contract Capacity:
- Source File: CON-01_Cap_Bank_Sizing.docx
