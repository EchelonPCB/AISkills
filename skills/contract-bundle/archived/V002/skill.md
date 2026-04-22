---
build_number: "002"
skill_id: "epcb.design1.contract_bundle_execution"
name: "Contract Bundle Execution"
description: "Unzip a contract bundle and systematically execute each contract skill to deliver all required artifacts and validation outputs."
trigger_keywords: "contract bundle, unzip, execute skills, multi-contract, deliverables"
owner: "EPCB"
status: "active"
created_at: "2026-04-21"
last_updated: "2026-04-21"
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
Define a governed workflow that unzips a bundle of contract documents and executes each corresponding contract skill (CON‑01 through CON‑04) to produce all required artifacts and validation evidence without scope creep.

# Trigger
Use this skill when a zipped file containing multiple contract documents (e.g., Cap Bank, Battery Capacity, Power Path Architecture, Simple Arbitration Logic) is provided and each contract must be processed using its dedicated AISkills definition to deliver the specified outputs.

# Do Not Use When
- The task involves only a single contract; in that case, invoke the specific contract skill directly.
- The zipped file contains documents unrelated to the defined contracts.
- Contract skills are missing or incomplete; request BoD clarification instead.
- The goal is to revise contract scopes or combine deliverables into a single artifact; each contract remains separate.

# Required Inputs
- Zipped archive of contract documents (e.g., `.zip` file with `.docx` contracts).
- Corresponding `skill.md` files for each contract (CON‑01 through CON‑04).
- Access to external sources for component specifications (vendor pages, datasheets) to satisfy contract requirements.
- Tools for calculation, diagramming, coding, and file generation (e.g., Python environment, diagram library).

# Optional Inputs
- Preferred diagramming or simulation tools (Matplotlib, Graphviz).
- Placeholder assumptions for upstream outputs when dependencies have not been completed.
- Bench hardware or simulation setups to validate arbitration logic.

# Outputs
- **PASS threshold:** A collection of deliverables satisfying each contract’s validation criteria. This includes:
  1. A calculation document for CON‑01 with derived capacitance, cell count, series/parallel arrangement, ESR considerations, and validation that bus voltage stays above 10 V.
  2. Vendor link and specification sheet for a lithium‑ion battery (12–19 V, under $200) and a candidate motor with documented peak current for CON‑02.
  3. A power path architecture diagram showing all required nodes, voltage labels, cap bank placement, and arbitration disconnect point for CON‑03.
  4. Working code or pseudocode and a decision‑flow diagram that monitors bus voltage and controls the peripheral disconnect for CON‑04.
- **Evidence items:** Each deliverable must be uploaded to the appropriate contract folder (Cap Bank, Battery Capacity, Power Path, Simple Arbitration Logic) and referenced in a handoff note.

# Support Layers
- **Contract parsing layer:** Extracts scope‑lock, in‑scope items, out‑of‑scope exclusions, and validation criteria from each contract.
- **Governance layer:** Ensures BoD‑approved boundaries are respected across all contracts.
- **Traceability layer:** Maps contract IDs and dependencies (CON‑01 through CON‑04) to the outputs and evidence artifacts.
- **Delivery layer:** Associates each deliverable with its contract folder and required format (PDF, PNG, MD, code).

# Procedure
1. **Unzip and identify documents.**
   1.1 Extract the provided archive and list all contract files.
   1.2 Match each document (e.g., `CON‑01_Cap_Bank_Sizing.docx`) with its corresponding skill file (e.g., `CON‑01_cap_bank_sizing_skill.md`).
2. **Process each contract sequentially.**
   2.1 For CON‑02 (Battery Capacity), research and select a lithium‑ion battery within the specified voltage and cost range; identify a high‑current motor; record specifications and vendor links; share outputs with the CON‑01 team.
   2.2 For CON‑01 (Cap Bank Sizing), derive transient parameters from the selected battery and motor; calculate required capacitance using \(C = I·t/ΔV\); choose appropriate supercapacitor cells; determine series/parallel configuration; compile the calculation document and specification table.
   2.3 For CON‑03 (Power Path Architecture), draw the complete power path diagram showing the main battery, UPS/BMS, Jetson compute rail, peripheral rail, cap bank, and arbitration switch; label all voltage nodes and ensure completeness.
   2.4 For CON‑04 (Simple Arbitration Logic), define disconnect and reconnect thresholds; implement voltage‑monitoring code or pseudocode; draw a decision‑flow diagram; prepare a bench or simulated demo if possible.
3. **Package and hand off.**
   3.1 Export documents, diagrams, and code in the required formats (e.g., PDF/PNG/MD).
   3.2 Upload each artifact to its respective contract folder and notify the BoD and dependent teams that the deliverable is ready.
   3.3 Record any assumptions or placeholder values used due to incomplete upstream outputs.

# Decision Logic
- If a required upstream output (battery selection, cap bank spec, power path diagram, or disconnect point) is available, use it directly and cite it.
- If an upstream output is unavailable but the contract allows placeholder assumptions, document the assumption clearly and proceed conservatively.
- If a missing dependency prevents completion of a downstream contract, stop the process for that contract and notify the BoD.
- Maintain separation of concerns: never merge deliverables from different contracts into a single artifact.

# Validation
- Confirm that each deliverable meets the exact PASS threshold stated in its contract skill.
- Ensure that all out‑of‑scope items listed in each contract are avoided.
- Verify that every validation criterion appears both in the Outputs section and in the produced evidence.
- Check that all contract IDs (CON‑01 through CON‑04) are correctly referenced and that dependencies are satisfied or explicitly assumed.
- Run a preflight over the generated skill to ensure all required headers and frontmatter keys are present and correctly ordered.

# Rules
- Do not answer the subject matter of the contracts; focus on executing the defined skills.
- Do not change scope‑lock fields or add tasks not listed in the in‑scope section.
- Do not perform procurement, physical wiring, or advanced control design; these are explicitly out of scope.
- Do not mix multiple contracts’ outputs into a single skill; deliverables must be uploaded individually to their respective folders.
- Respect identity lock: when metadata fields are supplied by the user, use them exactly as provided.
- When using external sources, cite them appropriately and ensure they are trusted and up to date.

# Failure Modes
- **Archive errors:** The zip file fails to extract or missing documents; remedy by re‑requesting the archive or reporting failure.
- **Missing skills:** A required contract skill file is absent; halt execution and request it.
- **Invalid or ambiguous contract:** Source documents lack clear scope or success criteria; raise to BoD for clarification.
- **Dependency deadlock:** An upstream contract output is unavailable and cannot be assumed; pause downstream execution and notify the BoD.

# Dependencies
- `epcb.design1.battery_capacity` (CON‑02): battery and load selection results.
- `epcb.design1.cap_bank_sizing` (CON‑01): supercapacitor sizing.
- `epcb.design1.power_path_architecture` (CON‑03): power‑path diagram and disconnect point.
- `epcb.design1.simple_arbitration_logic` (CON‑04): arbitration logic implementation.

# Assumptions
- Any metadata fields not specified in the new skill (e.g., contract location, priority, contract capacity) remain unspecified and require BoD confirmation if needed.
- Tool choice (diagramming software, coding language) is left to the contractor unless mandated by a contract.
- External research uses only publicly available and trusted sources; price and specifications may vary with time.

# Change Log
## V1.0 – 2026‑04‑21
- Initial skill created to orchestrate the execution of a zipped bundle of contracts using their respective skills and to outline deliverables, procedures, decision logic, and validation requirements.