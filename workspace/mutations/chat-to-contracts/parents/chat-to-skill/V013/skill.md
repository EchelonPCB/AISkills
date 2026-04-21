---
build_number: "013"
skill_id: "epcb.meta.chat_to_skill"
name: "chat-to-skill"
description: "Convert raw chats or chat summaries into structured, reusable, version-ready AISkills skill files."
trigger_keywords: "chat, classify chat, apply skill, extract skill, workflow intake, copy paste skill, epcb id, old AI chat"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-20"
---

# Index

| Section | Description |
|--------|-------------|
| Objective | Define the governed extraction purpose |
| Hard Mode Contract | Prevent non-skill substitutes |
| Artifact Identity Rules | Define the only valid skill artifact |
| Required Skill Formatter | Enforce repo-valid generated skill structure |
| Source Artifact Sanitation | Remove invalid source and scaffold leftovers |
| RALPH Validation Loop | Bound requirements reaffirmation and exit conditions |
| Offline Copy-Paste Mode | Operate when manifest and repo context are unavailable |
| Trigger | When to apply the skill |
| Do Not Use When | Misuse conditions |
| Required Inputs | Mandatory source material |
| Optional Inputs | Helpful repo and naming context |
| Outputs | Expected governed deliverables |
| Support Layers | Repo surfaces used during extraction |
| Procedure | Execution order |
| Decision Logic | Classification and formatting decisions |
| Validation | Output correctness checks |
| Rules | Non-negotiable constraints |
| Repo Transaction Output | Required response order |
| Skill File Requirements | Required generated skill sections |
| Compliance Gate | Blocking validation checks |
| Failure Modes | Recoverable breakdowns |
| Dependencies | External repo requirements |
| Assumptions | Operating assumptions |
| Change Log | Version history |

---

# Objective

Convert a raw chat log or structured chat summary into one or more complete, reusable `skill.md` files that conform to the AISkills repository standard.

---

# Hard Mode Contract

When this skill is invoked in apply mode, it supersedes normal assistant helpfulness behavior.

The assistant must NOT:
- answer the source chat’s subject matter
- generate PDFs, DOCX files, slide decks, or summaries
- produce lightweight markdown notes
- provide partial skill drafts or skeletons
- output multiple fragmented artifacts

The assistant MUST:
- classify first
- return the governed skill extraction output
- treat “use this chat to skill” as a repo transaction request

---

# Artifact Identity Rules

For `new skill` and `amendment` classifications, the ONLY valid artifact is:

→ one complete AISkills `skill.md` file

A valid skill file is:
- a single fenced markdown block
- frontmatter through Change Log
- fully self-contained
- repo-ready

INVALID substitutes:
- summaries
- study guides
- PDFs
- partial markdown
- split blocks
- explanatory prose without a full skill file

---

# Required Skill Formatter

Before returning any generated `skill.md`, the assistant MUST format it through this gate.

Frontmatter requirements:
- Frontmatter starts on line 1 with `---` and closes with `---`.
- Include these keys in this order: `build_number`, `skill_id`, `name`, `description`, `trigger_keywords`, `owner`, `status`, `created_at`, `last_updated`.
- `description` is one line.
- `trigger_keywords` is one quoted, comma-separated line with at least three entries.
- `trigger_keywords` belongs in YAML frontmatter, not only inside the body `# Trigger` section.
- `skill_id` starts with `epcb.` and uses dot-separated lowercase underscore tokens.

Required header formatter:
- Use level-one headings exactly as written here.
- Do not rename, pluralize, merge, or decorate these headers.
- Do not substitute nearby labels such as `# Trigger Words`, `# Preconditions`, `# Risks`, or `# Notes`.
- The generated skill MUST contain these sections in this order:
  1. `# Index`
  2. `# Objective`
  3. `# Trigger`
  4. `# Do Not Use When`
  5. `# Required Inputs`
  6. `# Optional Inputs`
  7. `# Outputs`
  8. `# Support Layers`
  9. `# Procedure`
  10. `# Decision Logic`
  11. `# Validation`
  12. `# Rules`
  13. `# Failure Modes`
  14. `# Dependencies`
  15. `# Assumptions`
  16. `# Change Log`

Hard validation constraint:
- If any required frontmatter key or header is missing, misspelled, or placed only as body prose, revise the generated skill before output.
- If the generated skill would fail `system/scripts/validate_skills.py`, revise before output.
- If the assistant cannot validate the structure confidently, return the classification and ask for permission to write the skill into the repo for validation instead of returning a possibly invalid file.

---

# Source Artifact Sanitation

Before returning any generated `skill.md`, companion CHANGELOG entry, or support-file plan, the assistant MUST scan for and remove source artifacts that are not valid repo content.

Forbidden source-citation artifacts:
- `:contentReference`
- `oaicite`
- `turn0`
- dangling citation placeholders without a real local support file
- bracketed source handles copied from an AI chat instead of converted into plain evidence language

Forbidden scaffold leftovers:
- `TODO`
- `[Add change summary here]`
- `Initial governed skill scaffold; replace TODOs`
- `replace TODOs before validation`
- placeholder changelog language that describes scaffolding instead of the actual skill content

Sanitation rules:
- Replace citation placeholders with plain descriptions of the support layer, evidence type, or validation source.
- If a source file actually exists, reference it as a real skill-local path such as `references/<file>.md`.
- If no source file exists, describe the evidence category without inventing a file path.
- The companion `skills/<skill-name>/CHANGELOG.md` entry must describe the completed skill, not the scaffold.
- If sanitation changes the generated skill materially, re-run the Required Skill Formatter afterward.

Hard sanitation constraint:
- If any forbidden source-citation artifact or scaffold leftover remains, revise before output.
- If the artifact appears only in the source chat, do not copy it into the generated skill.
- Treat clean changelog guidance as part of validation, not optional polish.

---

# RALPH Validation Loop

Run RALPH after drafting, formatting, and sanitation. RALPH is a bounded quality gate based on requirements traceability, acceptance criteria, format control, provenance review, and explicit stop criteria.

RALPH means:

- **R — Reaffirm Requirements:** Confirm the generated skill satisfies all required skill fields: frontmatter keys, `trigger_keywords`, Index, Objective, Trigger, Do Not Use When, Required Inputs, Optional Inputs, Outputs, Support Layers, Procedure, Decision Logic, Validation, Rules, Failure Modes, Dependencies, Assumptions, and Change Log.
- **A — Audit Alignment:** Confirm the generated skill matches the source workflow, does not answer the source chat directly, and separates `Use this skill when` from `Do Not Use When`.
- **L — Lock Layout and Lineage:** Confirm exact header text and order, `epcb.*` skill ID format, kebab-case skill name, support-file plan, changelog guidance, and standard `V###` / `CURRENT` / `MANIFEST.md` versioning. Do not propose `VP###` or separate production folders.
- **P — Purge Provenance Problems:** Confirm no copied AI citation markers, hidden-context dependencies, scaffold placeholders, invented support paths, or stale changelog text remain.
- **H — Halt or Hand Off:** Exit the loop when all checks pass, or stop after the maximum allowed passes and return the unresolved blockers.

Loop limit:
- Run at most **two RALPH passes**.
- Pass 1 may identify and repair defects.
- Pass 2 may only confirm the repair or stop with blockers.
- Do not start a third pass.
- Do not recursively regenerate forever.

Exit conditions:
- **PASS:** all RALPH checks pass; return the governed output.
- **CONDITIONAL PASS:** repo-only checks cannot be completed because `MANIFEST.md` or existing skill files are unavailable, but the generated skill is structurally valid. Return the governed output and state in Validation Notes: `Manifest unavailable; duplicate check not performed.`
- **HAND OFF:** after two passes, any blocking requirement, formatter, sanitation, or structure issue remains. Do not return a possibly invalid skill as final; return the classification, blockers, and the exact missing information or repo validation action needed.

---

# Offline Copy-Paste Mode

Use this mode when the assistant has the CTS file and source chat, but does not have access to the AISkills repository, `MANIFEST.md`, or existing skill folders.

Offline behavior:
- Continue generating one complete paste-ready `skill.md` when the source qualifies as `new skill`.
- Do not require manifest access before producing a candidate skill.
- Do not claim duplicate checks were completed.
- Include a Validation Notes line that says: `Manifest unavailable; duplicate check not performed.`
- Recommend that the user paste the generated file into `skills/<skill-name>/V001/skill.md`, update the skill changelog, then run repo validation locally.

Offline amendment behavior:
- If the user asks for an amendment but no existing skill text is supplied, classify as `insufficient`.
- Ask for the current skill file or produce an amendment plan only.
- Do not invent changes to an unseen skill.

Versioning doctrine:
- Use existing `V###`, `CURRENT`, and `MANIFEST.md` flow.
- Treat the current live version as the production-ready version.
- Do not create or recommend `VP###`, `production/`, or separate production-version folders.

---

# Single-File Normalization Rule

If the user says:
- "single file"
- "combine everything"
- "one .md"
- "one .mp"
- "make downloadable"

Interpret this as:

→ return one complete governed `skill.md`

DO NOT change artifact type.

---

# Trigger

Use this skill when a conversation contains:

- repeatable workflows
- system integration logic
- procedural steps with clear execution order
- defined inputs and outputs
- reusable engineering, business, or AI processes

---

# Do Not Use When

Do not use this skill when the content is:

- purely informational → classify as **reference**
- only code → classify as **script**
- a standalone file/template → classify as **asset**
- vague or exploratory → request clarification

---

# Required Inputs

1. Raw chat log OR structured summary

---

# Optional Inputs

- Existing skill folder to amend
- Existing skill text, when amendment is requested without repo access
- Proposed skill name or domain
- Current `MANIFEST.md`
- Repo validation output
- User preference for tone, strictness, or support-file depth

---

# Outputs

- Classification block
- One complete formatted `skill.md` for `new skill` or `amendment`
- Repo command block
- CHANGELOG entry
- Support file plan
- Validation notes

---

# Support Layers

- Manifest layer: compare against `MANIFEST.md` before proposing new skills.
- Formatter layer: normalize generated skill frontmatter and headers before output.
- Sanitation layer: remove source citation artifacts and scaffold leftovers before output.
- RALPH layer: run bounded requirements reaffirmation before output.
- Offline layer: mark unavailable manifest checks without blocking structurally valid new-skill output.
- Validation layer: use repo validation rules as blocking constraints.
- Support-file layer: route long examples, assets, and scripts into skill-local support folders.

---

# Mode Selection

If the user provides raw chat content → APPLY MODE  
If the user asks about how to use this skill → ADVISORY MODE  

---

## Apply Mode Lock

When in apply mode:

- all advisory behavior is suspended
- no summaries or alternate artifacts allowed
- no PDFs, DOCX, or study guides
- only governed extraction output is valid

---

# First Response Contract

When invoked, the assistant MUST begin with:

Classification: <new skill | amendment | reference | script | asset>  
Confidence: <high | medium | low>  

Rationale:
- <bullet 1>
- <bullet 2>
- <bullet 3>

Repo Action:
- <create / update / none>

---

# No-Substitution Rule

If classification is `new skill` or `amendment`, the assistant MUST NOT substitute:

- summaries
- study guides
- PDFs
- lightweight markdown
- partial drafts

If anything other than a full `skill.md` is returned → NON-COMPLIANT

---

# Format Correction Rule

If the user says:

- "use this chat to skill"
- "follow the CTS"
- "this is not the right format"
- "include everything"
- "single file"

The assistant MUST:

→ discard previous output  
→ regenerate fully compliant CTS output  

DO NOT revise lightweight artifacts.

---

# Procedure

1. Classify the content
2. Determine skill boundaries
3. Generate full skill file
4. Apply the Required Skill Formatter
5. Apply Source Artifact Sanitation
6. Run the RALPH Validation Loop
7. Include all exact required headers and frontmatter keys
8. Validate compliance before output

---

# Decision Logic

| Condition | Action |
|----------|--------|
| source contains repeatable workflow | classify as `new skill` or `amendment` |
| existing manifest row covers workflow | classify as `amendment` |
| source is useful context but not procedure | classify as `reference` |
| generated headers drift from formatter | revise before output |
| generated text contains `:contentReference` or `oaicite` | replace with plain evidence language before output |
| changelog guidance contains scaffold text | replace with actual completed-skill summary |
| manifest is unavailable for a new skill | continue in Offline Copy-Paste Mode and mark duplicate check unavailable |
| manifest is unavailable for an amendment | require existing skill text or return `insufficient` |
| RALPH pass 1 finds defects | repair once and run pass 2 |
| RALPH pass 2 still finds blockers | stop and hand off blockers |
| validation confidence is low | move to repo-writing validation workflow |

---

# Validation

A generated chat-to-skill result is valid only when:

- the classification block is first
- new skill or amendment output contains one complete fenced `skill.md`
- generated frontmatter includes `trigger_keywords`
- generated level-one headers match the Required Skill Formatter exactly
- generated skill has no placeholders or partial sections
- generated skill has no source-citation artifacts
- generated changelog guidance has no scaffold leftovers
- RALPH exits with PASS or CONDITIONAL PASS
- manifest-unavailable outputs disclose that duplicate checks were not performed
- repo action, changelog entry, support plan, and validation notes are present

---

# Rules

- Do not return a generated skill until the Required Skill Formatter passes.
- Do not use body-only trigger keywords as a substitute for YAML `trigger_keywords`.
- Do not rename required generated headers.
- Do not copy AI chat citation markers into generated skills.
- Do not leave scaffold changelog text in companion changelog guidance.
- Do not run RALPH more than two passes.
- Do not treat missing manifest access as proof that no duplicate skill exists.
- Do not recommend `VP###`, `production/`, or separate production version folders.
- Do not soften the V010 hard constraints.
- Treat repo validation failure as a blocking defect, not a warning.

---

# Repo Transaction Output

The assistant MUST return in this exact order:

1. Classification block  
2. Skill File heading  
3. ONE complete fenced `skill.md`  
4. Repo command block  
5. CHANGELOG entry  
6. Support file plan  
7. Validation notes  

---

# Skill File Requirements

Each skill MUST include:

- YAML frontmatter
- Index table
- Objective
- Trigger
- Do Not Use When
- Required Inputs
- Optional Inputs
- Outputs
- Support Layers
- Procedure
- Decision Logic
- Validation
- Rules
- Failure Modes
- Dependencies
- Assumptions
- Change Log

---

# Compliance Gate

Before returning output, verify:

- classification block present
- confidence + rationale included
- exactly ONE fenced markdown block
- full `skill.md` present
- no partial fragments
- includes all required sections
- includes exact Required Skill Formatter headers
- includes frontmatter `trigger_keywords`
- includes no forbidden citation artifacts
- includes no scaffold changelog leftovers
- includes RALPH result in validation notes
- includes repo action
- includes changelog
- includes support plan
- includes validation notes
- would pass repo validation without header-text repair

---

# Core Principle

“Use this chat to skill” means:

→ perform governed skill extraction  
→ not summarize  
→ not explain  
→ not generate alternate artifacts  

---

# Failure Modes

| Failure | Recovery |
|--------|----------|
| Missing classification block | Restart output with the required classification contract |
| Generated artifact is not a complete `skill.md` | Discard the partial artifact and regenerate one complete fenced file |
| `trigger_keywords` omitted from generated frontmatter | Add comma-separated activation terms before returning output |
| Generated skill uses alternate header text | Reformat with the exact Required Skill Formatter headings |
| Source citation marker appears in generated skill | Replace it with plain evidence language or a real support-file path |
| Scaffold changelog text remains | Replace it with an actual completed-skill changelog entry |
| RALPH loop repeats without convergence | stop after two passes and return blockers |
| Manifest unavailable in copy-paste workflow | produce structurally valid output and disclose duplicate-check limitation |
| Amendment requested without existing skill text | return `insufficient` and request the current skill file |
| Generated skill would fail repo validation | Revise before output or move into repo-writing validation workflow |
| User asks for “single file” and receives another artifact type | Normalize the request to one governed `skill.md` file |
| Assistant answers the source chat instead of extracting | Restart in apply mode and classify first |

---

# Dependencies

- AISkills repository structure when available
- `MANIFEST.md` for duplicate checks when repository context is available
- `system/scripts/update_index.py` for manifest regeneration after repo edits
- `system/scripts/validate_skills.py` for validation after repo edits

---

# Assumptions

- The user wants a reusable AISkills artifact, not a summary of the source chat.
- Generated skills must be self-contained enough to run without the original chat.
- Repository-ready output includes metadata, changelog guidance, support-file planning, and validation notes.
- In offline copy-paste mode, the assistant may not have access to `MANIFEST.md` or existing skills.
- `CURRENT` plus `MANIFEST.md` is the production path; separate production folders are intentionally avoided.

---

# Change Log

## V013
- Added bounded RALPH validation loop with a two-pass maximum and explicit PASS, CONDITIONAL PASS, and HAND OFF exits.
- Added Offline Copy-Paste Mode for assistants that receive CTS without repository or manifest access.
- Added manifest-unavailable disclosure requirements for validation notes.
- Rejected `VP###` and separate production-folder versioning in favor of existing `V###`, `CURRENT`, and `MANIFEST.md` flow.

## V012
- Added Source Artifact Sanitation as a blocking pre-output gate.
- Added explicit rejection of AI citation markers such as `:contentReference` and `oaicite`.
- Added changelog sanitation rules to prevent scaffold leftover text in generated skill folders.
- Required sanitation before final validation and output.

## V011
- Added Required Skill Formatter as a blocking pre-output gate.
- Added exact frontmatter and level-one header requirements for generated skills.
- Added hard validation constraint requiring revision before output when repo validation would fail.
- Preserved V010 hard constraints while tightening generated skill validity.

## V010
- Added Hard Mode Contract
- Added Artifact Identity Rules
- Added No-Substitution Rule
- Added Single-File Normalization
- Added Apply Mode Lock
- Added Format Correction Rule
- Added Compliance Gate
- Strengthened Repo Transaction Output enforcement
