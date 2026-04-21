---
build_number: "003"
skill_id: "epcb.contracts.contract_gen"
name: "contract-gen"
description: "Generate a complete, BoD-ready ACDC MVP Deliverable Contract document from a validated parameter set, with all fields filled and enforcement language included."
trigger_keywords: "contract, generate contract, deliverable contract, fill document, bod contract"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-20"
---

# Index

| Field      | Detail                                                                   |
|------------|--------------------------------------------------------------------------|
| Trigger    | Validated parameter set is ready from `contract-type`                    |
| Input      | 12-field parameter set + Contract ID + Issue Date + BoD name             |
| Output     | Filled ACDC MVP Deliverable Contract `.docx`, ready for BoD signature    |
| Key Steps  | Assign ID → fill BoD page → fill enforcement → fill contractor page → export |
| Fails When | Any required parameter is missing or success condition is not binary      |
| Requires   | `contract-type` output (epcb.contracts.contract_type)                    |

---

# Objective

Given a complete parameter set (from `contract-type` or provided directly by the BoD), generate a fully filled ACDC MVP Deliverable Contract document. The output document is print-ready and signature-ready for the BoD page. The contractor copy is pre-populated with identifiers. No fields on the BoD page should be left blank.

# Trigger

Use this skill when:

- A parameter set has been validated by `contract-type` and is ready for document production
- The BoD has provided all required fields manually and needs a formatted contract document
- A prior contract is being reissued with revised scope (requires updated Contract ID)

# Do Not Use When

- The parameter set has any field marked [ASSUMED] that has not been confirmed by BoD → resolve assumptions first
- The deliverable scope has not been defined (in-scope items missing) → run `contract-type` first
- The contract is being reissued identically to a prior failed contract → reissuance requires scope revision per Article IV §4.8

# Required Inputs

1. Complete 12-field parameter set from `contract-type`:
   - contract_type, priority, type, difficulty, capacity
   - applicable_majors, supporting_majors
   - mvp_function, success_condition, interface_requirement
   - in_scope (up to 4 items), out_of_scope (up to 4 items)
2. Contract ID (format: CON-YYYYMMDD-NN, e.g., CON-20260415-05)
3. 4P Code (format: 4P-YYYYMMDD-TAG, e.g., 4P-20260415-WIRE)
4. Deliverable name (short title)
5. Hard Deadline (date)
6. Tracker Path (BoD > Projects > {folder} > {Contract ID})
7. Location (lab room, e.g., CKB 110 Triple Door Entry)
8. Issue Date
9. Issuing BoD member name

# Optional Inputs

1. Validation Criteria overrides (if BoD wants non-standard evidence items)
2. Special accommodation note
3. Reissuance flag (TRUE/FALSE) — if TRUE, old Contract ID must be referenced in notes

# Outputs

1. Filled ACDC MVP Deliverable Contract `.docx` file — BoD page complete, contractor copy pre-populated
2. Contract ID logged to tracker
3. Summary confirmation block (Contract ID, Deliverable, Deadline, Tracker Path)

---

# Support Layers

- Intake layer: consumes validated parameter sets from `contract-type` or equivalent BoD-approved inputs.
- Template layer: fills the fixed ACDC MVP Deliverable Contract document structure.
- Enforcement layer: preserves required contract enforcement language and signature boundaries.
- Tracker layer: returns IDs, tracker path, and output status for downstream records.

---

# Procedure

## 1. Input Validation

1.1 Confirm all 9 required inputs are present and non-empty.
1.2 Confirm the parameter set has no unresolved [ASSUMED] flags.
1.3 Confirm the success_condition begins with "PASS:" and contains at least one binary, observable criterion.
1.4 Confirm in_scope contains 1–4 items; out_of_scope contains 1–4 items.
1.5 Confirm Contract ID follows format CON-YYYYMMDD-NN.

IF any check fails:
→ List the failing fields and stop. Do not generate a partial document.

## 2. Assign Validation Criteria

2.1 Map each in_scope item to a corresponding validation criterion (#1–#4):
    - Each validation criterion must be a specific, verifiable evidence item
    - Format: "[Evidence type] — [specific observable result]"
    - Evidence types: Live demo, Photo, File upload, Video, Verbal confirmation, Written note

2.2 Default mapping rules:
    - Last in_scope item (evidence upload) → File upload criterion
    - Any in_scope item involving hardware function → Live demo criterion
    - Any in_scope item involving a diagram or photo → Photo/upload criterion
    - Any in_scope item involving verbal verification → Verbal confirmation criterion

2.3 IF BoD provided validation criteria overrides → use those instead of the defaults.

## 3. Fill the BoD Page (Page 1)

3.1 Fill the contract header block:

    4P Code:         {4p_code}
    Contract ID:     {contract_id}
    Deliverable:     {deliverable_name}
    Type:            {type}
    Hard Deadline:   {hard_deadline}
    Tracker Path:    {tracker_path}
    Location:        {location}
    Issued By (BoD): {issuing_bod_member}
    Issue Date:      {issue_date}

3.2 Fill the contract type and priority checkboxes:

    Contract Type:   [X] in the {contract_type} box
    Priority:        [X] in the {priority} box

3.3 Fill applicable and supporting majors.

3.4 Fill difficulty and capacity checkboxes.

3.5 Fill Scope Lock section:

    MVP Function:          {mvp_function}
    Success Condition:     {success_condition}
    Interface Requirement: {interface_requirement}

3.6 Fill IN SCOPE checkboxes — one item per row, in execution order.

3.7 Fill OUT OF SCOPE checkboxes — one item per row.

3.8 Fill Validation Criteria rows #1–#4 from Step 2.

3.9 Insert standard Enforcement & Conditions clause verbatim:

    "This contract constitutes formal assignment to a deliverable within an approved 4P. A contract becomes active only upon contractor claim and signature. Active progress requires a claimed contract, inclusion in the official tracker, and demonstrable work evidenced by partial or complete fulfillment of in-scope requirements. Membership status is evaluated in Week 8 relative to the start of a given semester. Inactive members may not participate in 4Ps (Art. IV §4.9.1). Only completed and BoD-verified contracts count toward membership advancement, while active claimed contracts prior to the declared deadline count toward membership preservation. Unclaimed, expired, or failed contracts revert to the issuing BoD member for completion or reissuance at their discretion. Reissued contracts must include revised scope or criteria; identical reissuance is not permitted. A contract is considered expired once the hard deadline has passed, and failed if all in-scope requirements defined on the BoD page are not completed. Contracts with no observable progress may be revoked at BoD discretion. In cases of ambiguity, the BoD determines whether success conditions are satisfied. Work without evidence does not qualify as completion, the BoD holds final authority on verification and contract closure in accordance with Article IV (§4.8–§4.9)."

3.10 Leave BoD Signature and Date fields blank — for physical or digital signature at issuance.

## 4. Fill the Contractor Copy (Page 2)

4.1 Pre-populate the contractor copy header:

    Contract ID:   {contract_id}
    4P Code:       {4p_code}
    Deliverable:   {deliverable_name}

4.2 Leave all contractor-fill sections blank:
    - Contractor Commitment Claim (name, role, UCID, hours, type, signature, date)
    - Materials & Procurement
    - Evidence Submission (#1–#4)
    - Verification (BoD only)

4.3 Add return instruction header: "Return to BoD when all required evidence submissions are filled in."

## 5. Export and Log

5.1 Export the document as a `.docx` file.
5.2 Name the file: `ACDC_{contract_id}_{deliverable_tag}.docx`
    - deliverable_tag = short uppercase label from 4P Code (e.g., WIRE, ENCL-D, UDP)
5.3 Upload or place the file at the tracker path: {tracker_path}.
5.4 Return a confirmation summary block:

    Contract ID:    {contract_id}
    Deliverable:    {deliverable_name}
    Hard Deadline:  {hard_deadline}
    Tracker Path:   {tracker_path}
    Status:         Ready for BoD signature

---

# Decision Logic

| Condition | Action |
|----------|--------|
| required field is missing | stop and list missing fields |
| unresolved `[ASSUMED]` flag exists | return to BoD for confirmation |
| validation criteria override exists | use BoD-provided criteria |
| reissue is identical to failed prior contract | reject until scope or criteria changes |
| all inputs pass checks | generate BoD page and contractor copy |

---

# Validation

The generated contract package is valid when:

1. All BoD page fields are filled except signature/date lines.
2. Contractor copy identifiers are pre-populated.
3. Contractor-only fields remain blank.
4. Validation criteria are specific and evidence-based.
5. Confirmation summary includes Contract ID, Deliverable, Deadline, Tracker Path, and Status.

---

# Rules

- Do not generate a contract with any BoD page field left blank — all fields must be filled before output
- Do not modify the Enforcement & Conditions clause — it must be reproduced verbatim from Step 3.9
- Do not pre-fill the contractor copy sections — those are contractor-only fields
- Do not reissue a contract with identical scope — reissuance requires at least one change to in-scope items or success condition (Article IV §4.8)
- Validation Criteria must be specific and verifiable — reject vague items like "contractor demonstrates understanding"
- The BoD Signature line must be left blank — do not pre-sign or auto-fill

# Failure Modes

- Missing required input: List the missing field(s); stop generation. Do not produce a partial contract.
- Unresolved [ASSUMED] flags: Return the flagged fields to the BoD for confirmation before proceeding.
- Success condition is not binary: Rewrite using `contract-type` before generating — do not produce a vague success condition.
- More than 4 in-scope items: Signal that the deliverable must be split. Stop and refer to `contract-type`.
- Identical reissuance attempted: Flag the violation (Article IV §4.8); require scope or criteria change before proceeding.
- Validation Criteria cannot be derived from in-scope items: Request BoD to specify evidence items manually.

# Dependencies

- `contract-type` (epcb.contracts.contract_type): Produces the parameter set this skill consumes. Can be bypassed if BoD provides all inputs directly.
- ACDC MVP Deliverable Contract template: The `.docx` base document this skill fills. Must be accessible in the shared drive.
- ACDC Club Constitution Article IV §4.8–§4.9: Governs enforcement language; reproduced verbatim in Step 3.9.
- 4P tracker: Destination for the output file.

# Assumptions

- The contract template structure is fixed — field positions and section order do not change between contracts.
- The Enforcement & Conditions clause is a static text block managed by the BoD — this skill does not interpret or modify it.
- "Ready for BoD signature" means the issuing BoD member reviews and physically or digitally signs Page 1 before distributing to contractors.
- File naming convention uses the short tag from the 4P Code — BoD is responsible for defining the tag at 4P creation time.
- Reissuance is flagged by the BoD; this skill does not automatically detect prior contracts with the same deliverable name.

# Change Log

## V003
- Added governed Support Layers, Decision Logic, Validation, and Change Log sections for autonomous validation compatibility.
- Preserved V002 contract generation procedure and enforcement constraints.
