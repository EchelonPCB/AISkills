---
build_number: "010"
skill_id: "epcb.meta.chat_to_skill"
name: "chat-to-skill"
description: "Convert raw chats or chat summaries into structured, reusable, version-ready AISkills skill files."
trigger_keywords: "chat, classify chat, apply skill, extract skill, workflow intake, copy paste skill, epcb id, old AI chat"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-20"
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
4. Include all required sections
5. Validate compliance before output

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
- includes trigger_keywords
- includes repo action
- includes changelog
- includes support plan
- includes validation notes

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
| User asks for “single file” and receives another artifact type | Normalize the request to one governed `skill.md` file |
| Assistant answers the source chat instead of extracting | Restart in apply mode and classify first |

---

# Dependencies

- AISkills repository structure
- `MANIFEST.md` for duplicate checks when repository context is available
- `system/scripts/update_index.py` for manifest regeneration after repo edits
- `system/scripts/validate_skills.py` for validation after repo edits

---

# Assumptions

- The user wants a reusable AISkills artifact, not a summary of the source chat.
- Generated skills must be self-contained enough to run without the original chat.
- Repository-ready output includes metadata, changelog guidance, support-file planning, and validation notes.

---

# Change Log

## V010
- Added Hard Mode Contract
- Added Artifact Identity Rules
- Added No-Substitution Rule
- Added Single-File Normalization
- Added Apply Mode Lock
- Added Format Correction Rule
- Added Compliance Gate
- Strengthened Repo Transaction Output enforcement
