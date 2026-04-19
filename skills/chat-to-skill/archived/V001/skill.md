---
build_number: "001"
skill_id: "epcb.meta.chat_to_skill"
name: "chat-to-skill"
description: "Convert chat summaries or raw chat logs into structured, version-ready AISkills skill files"
owner: "EPCB"
status: "active"
created_at: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---

# Objective

Convert a raw chat or chat summary into a reusable, structured skill file compatible with the AISkills system.

# Trigger

Use this skill when:
- a chat contains repeatable logic
- a workflow appears more than once
- a process has clear inputs and outputs
- a conversation produced a useful system or method

# Required Inputs

1. Chat summary OR raw chat content
2. Intended use case (optional but recommended)

# Optional Inputs

1. Desired skill name
2. Known inputs/outputs
3. Known constraints
4. Target domain (engineering, business, AI, etc.)

# Output

A complete `skill.md` file including:
- YAML frontmatter
- structured sections
- numbered procedure
- reusable logic
- version-ready format

# Procedure

## 1. Intake

1.1 Accept raw chat or summary  
1.2 If raw chat is provided, compress into a structured summary  
1.3 Identify core objective of the workflow  

## 2. Classification

2.1 Determine if content qualifies as a skill  
2.2 If not, recommend:
- reference
- asset
- script

2.3 If skill, continue  

## 3. Extraction

3.1 Extract:
- purpose
- trigger
- required inputs
- optional inputs
- outputs

3.2 Extract step-by-step logic  

3.3 Extract:
- decision points
- edge cases
- failure modes  

## 4. Normalization

4.1 Convert into standardized structure:

- Objective  
- Trigger  
- Inputs  
- Outputs  
- Procedure  
- Rules  
- Failure Modes  
- Logging  

4.2 Ensure no hidden assumptions  

## 5. Structuring

5.1 Build numbered procedure:

1. Main steps  
1.1 Substeps  

5.2 Ensure logical flow and determinism  

## 6. Dependency Identification

6.1 Identify if skill requires:
- reference files  
- assets  
- scripts  

6.2 If needed, list them explicitly  

## 7. Output Generation

7.1 Generate full `skill.md` file  
7.2 Include YAML frontmatter:

- build_number  
- skill_id  
- name  
- description  
- status  
- created_at  
- last_updated  

7.3 Ensure compatibility with AISkills repo structure  

## 8. Validation

8.1 Check:
- reusability  
- clarity  
- independence from chat context  

8.2 If weak:
- refine structure  
- expand steps  

## 9. Review Gate

9.1 Ask user:
- approve  
- refine  
- reject  

## 10. Logging

10.1 Log:
- input summary  
- classification result  
- generated skill name  
- completeness level  

# Rules

- Do not convert one-off chats into skills  
- Do not include conversational fluff  
- Do not rely on hidden context  
- Prefer explicit structure over brevity  
- Ensure steps are executable, not descriptive  
- Always produce a complete file, not fragments  

# Failure Modes

- Chat too vague → request clarification  
- No repeatable logic → classify as reference  
- Missing inputs → infer but label assumptions  
- Overly broad scope → split into multiple skills  

# Output Format

Return:

1. Skill Name  
2. Classification Result  
3. Full `skill.md` file  
4. Suggested repo action:
   - create skill  
   - refine before commit  
   - classify as reference  

# Logging

- store input summary  
- store classification decision  
- store generated output status  

# Change Log

See CHANGELOG.md
