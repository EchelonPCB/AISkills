---
build_number: "002"
skill_id: "epcb.meta.chat_to_skill"
name: "chat-to-skill"
description: "Convert raw chats or chat summaries into structured, reusable, version-ready AISkills skill files."
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-19"
---

# Objective

Convert a raw chat log or structured chat summary into one or more complete, reusable `skill.md` files that conform to the AISkills repository standard.

# Trigger

Use this skill when a conversation contains:

- repeatable workflows
- system integration logic
- procedural steps with clear execution order
- defined inputs and outputs
- reusable engineering, business, or AI processes

# Do Not Use When

Do not use this skill when the content is:

- purely informational → classify as **reference**
- only code → classify as **script**
- a standalone file/template → classify as **asset**
- vague or exploratory → request clarification

# Required Inputs

1. Raw chat log OR structured summary

# Optional Inputs

1. Intended use case  
2. Desired skill name  
3. Known inputs/outputs  
4. Known constraints  
5. Domain classification  
6. Skill ID prefix  
7. Owner override  

# Outputs

The system MUST return ALL of the following:

1. Skill Name  
2. Classification Result  
3. One or more complete `skill.md` files  
4. Assumptions made during extraction  
5. Suggested repo action  

# Procedure

## 1. Intake

1.1 Accept raw chat or summary  
1.2 If raw chat, compress into structured summary  
1.3 Identify core objective(s)  
1.4 Detect if multiple independent workflows exist  

IF multiple workflows exist:
→ split into multiple skills  

## 2. Classification

2.1 Evaluate if content is a skill:

A valid skill must:
- be repeatable
- have defined steps
- produce consistent outputs

2.2 If NOT a skill:

Return:
- classification (reference / script / asset)
- reasoning

STOP execution

2.3 If skill:
→ continue

## 3. Skill Boundary Definition

3.1 Define scope of the skill  
3.2 Remove unrelated content  
3.3 Ensure single responsibility per skill  

IF scope is too broad:
→ split into multiple skills  

## 4. Extraction

4.1 Extract:
- objective
- trigger
- required inputs
- optional inputs
- outputs

4.2 Extract:
- step-by-step procedure
- decision logic
- arbitration rules (if any)
- control mappings (if any)

4.3 Extract:
- constraints
- assumptions
- failure modes

## 5. Normalization

5.1 Convert all content to:

- explicit
- deterministic
- executable steps

5.2 Remove:
- conversational language
- ambiguity
- hidden dependencies

5.3 Replace implicit knowledge with explicit assumptions

## 6. Structuring

6.1 Build standardized sections:

- Objective  
- Trigger  
- Inputs  
- Outputs  
- Procedure  
- Rules  
- Failure Modes  
- Dependencies  
- Assumptions  
- Logging (if applicable)

6.2 Enforce numbered hierarchy:

- 1
- 1.1
- 1.2

## 7. Metadata Construction

7.1 Generate YAML frontmatter:

- build_number = "001" (for new skills)
- skill_id = {prefix}.{domain}.{skill_name}
- name = kebab-case version
- description = one-line functional summary
- owner = EPCB (default unless overridden)
- status = active
- created_at = current date
- last_updated = current date

7.2 Ensure uniqueness of skill_id

## 8. Output Generation

8.1 Generate complete `skill.md` file(s)

8.2 Do NOT output partial files  
8.3 Do NOT omit sections  

## 9. Validation

9.1 Verify:

- skill is reusable without chat context
- steps are executable
- no missing inputs
- no hidden dependencies

9.2 If invalid:
→ refine before output

## 10. Output Formatting

Return in this exact structure:

1. Skill Name  
2. Classification Result  
3. Full `skill.md` file(s)  
4. Assumptions  
5. Suggested Repo Action  

# Rules

- Never produce partial skill files  
- Never rely on chat context outside the skill  
- Prefer explicit over concise  
- Split large workflows into multiple skills  
- Maintain deterministic logic  
- Enforce safety and failure handling where applicable  

# Failure Modes

- Chat too vague → request clarification  
- No repeatable logic → classify as reference  
- Missing inputs → infer and label assumptions  
- Overly complex workflow → split into multiple skills  
- Conflicting logic → prioritize safety and determinism  

# Logging

Store:

- input summary  
- classification decision  
- number of skills generated  
- skill_id(s) created  
- completeness status  

# Change Log

## v002
- Enforced strict output contract
- Added multi-skill detection and splitting
- Separated classification from generation
- Standardized metadata generation
- Removed conversational review step from execution
- Added deterministic validation requirements
