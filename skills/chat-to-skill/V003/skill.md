---
build_number: "003"
skill_id: "epcb.meta.chat_to_skill"
name: "chat-to-skill"
description: "Scan a conversation for repeatable workflows and produce a complete, self-contained skill.md file with a simple descriptive name."
trigger_keywords: "chat, summarize, convert, workflow, extract skill, create skill"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-19"
---

# Index

| Field       | Detail                                                                 |
|-------------|------------------------------------------------------------------------|
| Trigger     | End of a conversation that solved a repeatable problem                 |
| Input       | Chat history (raw or summarized)                                       |
| Output      | One or more complete `skill.md` files, or a classification decision    |
| Key Steps   | Qualify → Name → Extract → Expand → Validate → Output                 |
| Fails When  | Conversation is vague, one-off, or purely informational                |
| Name Rule   | Short, lowercase, plain English noun or verb phrase — no org prefixes  |

---

# Objective

At the end of a conversation, determine whether the workflow demonstrated qualifies as a reusable skill. If it does, extract the core process, give it a plain descriptive name, and produce a complete `skill.md` file that can be executed by anyone without access to the original conversation.

# Trigger

Use this skill when a conversation:

- Solved a problem using a repeatable, multi-step process
- Produced a defined output from defined inputs
- Could be handed to a new person or AI and run again from scratch
- Involved system integration, document generation, data processing, or structured decision-making

# Do Not Use When

- The conversation was exploratory or brainstorming only → classify as **reference**
- The output was a one-off answer with no repeatable steps → do not produce a skill
- The only artifact is code with no surrounding workflow → classify as **script**
- The output is a standalone template or form → classify as **asset**
- There is not enough context to define inputs and outputs → request clarification

# Required Inputs

1. Full conversation history OR a structured summary of what was done

# Optional Inputs

1. Desired skill name (if user specifies)
2. Skill ID prefix (default: infer from domain)
3. Owner override (default: EPCB)
4. Known constraints from the conversation

# Outputs

1. Classification decision (skill / reference / script / asset / insufficient)
2. One complete `skill.md` per identified skill workflow
3. List of assumptions made during extraction
4. Suggested repo action (add / split / defer)

---

# Procedure

## 1. Conversation Scan

1.1 Read the full conversation history from start to finish.
1.2 Identify the core thing that was accomplished — the primary output.
1.3 Identify what inputs were needed to produce that output.
1.4 Identify the steps taken in sequence between input and output.
1.5 Ask: could someone new follow these steps and get the same result? 
    - YES → proceed to Step 2
    - NO  → classify and stop (see Step 2.3)

1.6 Check whether multiple independent workflows were performed.
    IF multiple distinct input→output chains exist:
    → plan to produce one skill per workflow

## 2. Classification

2.1 A valid skill requires ALL three:
    - Repeatable: same steps work across different instances of the same problem
    - Defined steps: clear sequence with decision points
    - Consistent output: same type of result each time

2.2 IF valid skill → continue to Step 3.

2.3 IF NOT a skill:

    Conversation was exploratory or informational → classify: reference
    Output was only code, no surrounding workflow → classify: script
    Output was a blank form or template → classify: asset
    Steps are too context-specific to repeat → do not produce a skill

    Return classification + one-sentence reasoning. STOP.

## 3. Naming

3.1 Name the skill after what it DOES, not who owns it or what system it lives in.
3.2 Use a short, plain English noun or verb phrase:
    - GOOD: "contract-gen", "lane-detection", "udp-receiver", "enclosure-design"
    - BAD:  "legacy.meta.contract-to-skill", "epcb_workflow_v2", "process_handler"
3.3 If the conversation covered multiple skills, name each independently.
3.4 Convert to kebab-case for the skill name field.
3.5 Compose skill_id as: `{prefix}.{domain}.{name}`
    - Infer domain from the subject matter (e.g., hardware, v2i, pid, meta, ops)
    - Use owner prefix if specified; default to EPCB

## 4. Extraction

4.1 Extract the **Objective**: one paragraph stating what the skill accomplishes and what the output looks like.

4.2 Extract **Required Inputs**: everything that must exist before the skill can start.

4.3 Extract **Optional Inputs**: things that were used in the conversation but have valid defaults.

4.4 Extract **Outputs**: every artifact produced — files, decisions, states, confirmations.

4.5 Extract the **Procedure**:
    - Reproduce steps in the order they were actually performed
    - Expand each high-level action into 2–5 numbered substeps
    - Preserve all decision logic as explicit IF/THEN blocks
    - Identify and mark any checkpoints where a gate or approval was required

4.6 Extract **Rules** from:
    - Explicit constraints stated in the conversation
    - Things that were explicitly excluded or avoided
    - Safety or quality gates that were applied

4.7 Extract **Failure Modes** from:
    - Problems encountered during the conversation
    - Edge cases mentioned or implied
    - Steps that could silently fail without detection

4.8 Extract **Dependencies** from:
    - External tools, files, or systems required
    - Other skills or processes that must complete first

4.9 Extract **Assumptions** from:
    - Anything that was implied but not stated
    - Choices made without full justification
    - Values or conventions used without definition

## 5. Normalization

5.1 Rewrite all steps in imperative form ("Do X", "Confirm Y", "Upload Z").
5.2 Remove all conversational language, hedging, and filler.
5.3 Replace any reference to "the conversation" or "as discussed" with explicit facts.
5.4 Ensure every step can be executed without reading the original chat.

## 6. Index Window Construction

6.1 Build the Index table at the top of the file (below frontmatter, above Objective):

    | Field     | Detail                          |
    |-----------|----------------------------------|
    | Trigger   | One-line description             |
    | Input     | Key inputs, comma-separated      |
    | Output    | Key outputs, comma-separated     |
    | Key Steps | Verb phrase summary of procedure |
    | Fails When| Primary failure condition        |
    | Name Rule | Any naming convention used       |

6.2 The Index must be scannable in under 10 seconds — no sentences longer than one line.

## 7. Metadata Construction

7.1 Generate YAML frontmatter:

    build_number: "001"          ← always 001 for new skills
    skill_id: {prefix}.{domain}.{skill_name}
    name: {kebab-case name}
    description: {one-line functional summary, no org jargon}
    owner: EPCB                  ← unless overridden
    status: active
    created_at: {today's date}
    last_updated: {today's date}

## 8. Validation

8.1 Before outputting, verify the skill passes ALL checks:

    [ ] Objective states what the skill does without referencing the chat
    [ ] All inputs are named and typed
    [ ] Every output is listed
    [ ] Every procedure step is imperative and actionable
    [ ] Every rule says "Do not..." or states a hard constraint
    [ ] Every failure mode has a named recovery action
    [ ] Index table is complete and accurate
    [ ] Skill can be executed cold by someone who never saw the conversation

8.2 IF any check fails → revise the relevant section. Do not output a partial file.

## 9. Output

9.1 Return:
    1. Classification result
    2. Complete `skill.md` file(s)
    3. Assumptions list
    4. Suggested repo action

9.2 Do NOT output the skill name prefixed with organization or system names unless that is the descriptive name.
9.3 Do NOT leave any section blank.

---

# Rules

- Name skills after what they do — never after the org, system, or conversation they came from
- Never produce a partial skill file — all sections required
- Never reference the source conversation inside the skill body
- Split workflows that have more than one distinct input→output chain
- The Index table is mandatory — it is the first thing a reader sees
- Prefer explicit and verbose over concise and ambiguous

# Failure Modes

- Conversation too vague to extract steps → return classification: insufficient; request structured summary
- Multiple unrelated workflows in one chat → split into separate skills; do not merge
- Skill name is too long or org-specific → rename using plain descriptive noun/verb
- Procedure references chat context → rewrite section to be self-contained
- Index table is missing → add before outputting

# Dependencies

- Conversation history: must be available in full or summarized form
- AISkills repository standard: defines the `skill.md` file structure this skill outputs to

# Assumptions

- The conversation has concluded or reached a stable checkpoint before this skill is applied
- "Repeatable" means the same process applies to a different instance of the same type of problem — not just re-running the same inputs
- Skill names are chosen for clarity to a first-time reader, not for system routing

# Change Log

## v003
- Added mandatory Index Window section
- Changed naming rule: plain descriptive names, no org prefixes
- Added cold-execution validation checklist
- Clarified classification rules with concrete examples
- Aligned output format to match contract-to-skill and other ACDC skills
- Removed explicit reference to chat-context in procedure steps
