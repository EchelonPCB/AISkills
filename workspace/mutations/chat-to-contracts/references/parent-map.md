# Parent Map: chat-to-contracts

Mutation goal: Use a chat to create an actionable contract

| Parent | Version | Snapshot | Primary Contribution | Keep / Modify / Discard / Conflict |
|--------|---------|----------|----------------------|------------------------------------|
| chat-to-skill | V013 | parents/chat-to-skill/V013/skill.md | Convert a raw chat log or structured chat summary into one or more complete, reusable `skill.md` files that conform to the AISkills repository standard. --- | SYNTHESIS_REQUIRED |
| contract-to-skill | V002 | parents/contract-to-skill/V002/skill.md | Given one or more ACDC MVP Deliverable Contract documents, extract the structured content from each contract's fields and produce a complete, reusable `skill.md` file per contract. | SYNTHESIS_REQUIRED |

## Component Mapping

### chat-to-skill V013

- Objective signal: Convert a raw chat log or structured chat summary into one or more complete, reusable `skill.md` files that conform to the AISkills repository standard. ---
- Trigger signal: Use this skill when a conversation contains: - repeatable workflows - system integration logic - procedural steps with clear execution order - defined inputs and outputs - reusable engineering, business, or AI processes ---
- Required input signal: 1. Raw chat log OR structured summary ---
- Output signal: - Classification block - One complete formatted `skill.md` for `new skill` or `amendment` - Repo command block - CHANGELOG entry - Support file plan - Validation notes ---
- Validation signal: A generated chat-to-skill result is valid only when: - the classification block is first - new skill or amendment output contains one complete fenced `skill.md` - generated frontmatter includes `trigger_keywords` - generated level-one headers match the Required Skill Formatter exactly - generated skill has no placeholders or partial sections - generated skill has no source-citation artifacts - generated changelog guidance has no scaffold leftovers - RALPH exits with PASS or CONDITIONAL PASS - manifest-unavailable o
- Keep: SYNTHESIS_REQUIRED
- Modify: SYNTHESIS_REQUIRED
- Discard: SYNTHESIS_REQUIRED
- Conflicts: SYNTHESIS_REQUIRED

### contract-to-skill V002

- Objective signal: Given one or more ACDC MVP Deliverable Contract documents, extract the structured content from each contract's fields and produce a complete, reusable `skill.md` file per contract. The output skill must be executable without reference to the original contract document.
- Trigger signal: Use this skill when: - A member or BoD has issued one or more ACDC MVP Deliverable Contract `.docx` files - The goal is to make those contracts accessible as executable, AI-readable skill files - The contracts contain defined scope, validation criteria, in-scope steps, and a clear deliverable
- Required input signal: 1. One or more ACDC MVP Deliverable Contract `.docx` files (BoD page must be filled) 2. ACDC Club Constitution and Bylaws (for enforcement language and membership rules)
- Output signal: One complete `skill.md` file per contract, containing: 1. YAML frontmatter with skill metadata 2. Objective — what the contract deliverable accomplishes 3. Trigger — when to use this skill 4. Required Inputs — mapped from Interface Requirements + IN SCOPE prerequisites 5. Optional Inputs — inferred from contractor discretion fields 6. Outputs — mapped from Validation Criteria evidence items 7. Procedure — derived from IN SCOPE steps, expanded into numbered substeps 8. Rules — derived from OUT OF SCOPE items + Enfor
- Validation signal: The generated skill is valid when: 1. It can be executed without the original contract document. 2. All required AISkills sections are present. 3. PASS threshold matches the contract's Success Condition. 4. OUT OF SCOPE items are represented as Rules. 5. Contract IDs and dependencies are traceable. ---
- Keep: SYNTHESIS_REQUIRED
- Modify: SYNTHESIS_REQUIRED
- Discard: SYNTHESIS_REQUIRED
- Conflicts: SYNTHESIS_REQUIRED
