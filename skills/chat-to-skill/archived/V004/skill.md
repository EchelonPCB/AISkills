---
build_number: "004"
skill_id: "epcb.meta.chat_to_skill"
name: "chat-to-skill"
description: "Classify old AI chats and extract repeatable workflows into governed AISkills skill files."
trigger_keywords: "chat, summarize, convert, workflow, extract skill, skill intake, old AI chat"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-20"
---

# Index

| Field       | Detail                                                                 |
|-------------|------------------------------------------------------------------------|
| Trigger     | Old or completed AI chat may contain a reusable workflow               |
| Input       | Raw chat, chat summary, existing skill names, repo context             |
| Output      | Classification, skill draft, support-file plan, repo action            |
| Key Steps   | Select mode -> intake -> compare -> extract -> structure -> validate   |
| Fails When  | Chat lacks repeatable inputs, steps, outputs, or sufficient context    |
| Name Rule   | Folder uses kebab-case; skill_id uses epcb.<domain>.<skill_name>       |

---

# Objective

Convert completed AI conversations into governed AISkills artifacts. Determine whether each chat contains a reusable workflow, an amendment to an existing skill, a reference, an asset, a script, or insufficient material. For valid workflows, produce a self-contained `skill.md` draft plus a support-file plan that fits the AISkills repository structure.

# Trigger

Use this skill when:

- Reviewing old AI chats for reusable systems, workflows, or repeatable operating procedures
- Converting a solved conversation into a durable AISkills skill
- Deciding whether chat material should become a new skill, a new version of an existing skill, a reference, an asset, or a script
- Extracting a clean process from a messy conversation while preserving context in skill-local support folders

# Do Not Use When

- The user only needs a summary of a chat and does not want a reusable repo artifact
- The chat is purely brainstorming with no repeatable procedure
- The chat contains only a standalone file, template, image, or code snippet with no operating workflow
- The chat is still in progress and has not reached a stable checkpoint
- Required context is missing and cannot be reconstructed from the chat

# Required Inputs

1. Chat content: raw transcript or structured summary
2. Intended repo action: evaluate only, create new skill, update existing skill, or decide during intake
3. AISkills repository context: current `MANIFEST.md` and relevant existing skill folder, when available

# Optional Inputs

1. Proposed skill name
2. Proposed domain for `skill_id`
3. Existing skill candidate to compare against
4. Raw files, screenshots, prompts, generated outputs, or examples from the chat
5. User constraints, naming preferences, or ownership metadata

# Outputs

1. Classification: new skill, amendment, reference, asset, script, split, insufficient, or reject
2. Rationale: one concise reason for the classification
3. Repo action: scaffold, bump, add reference, add asset, add script, defer, or reject
4. Complete `skill.md` draft when classification is new skill or amendment
5. Support-file plan listing what belongs in `references/`, `assets/`, and `scripts/`
6. Validation checklist showing whether the result is ready to add to AISkills
7. When the user asked for extraction, the proposed new or amended skill comes before any critique of this skill

# Support Layers

- Put raw chat excerpts, long examples, source notes, rubrics, and background context in `references/`.
- Put templates, images, exported documents, example outputs, fixtures, and non-code artifacts in `assets/`.
- Put executable helpers, parsers, generators, or validation utilities in `scripts/`.
- Keep `skill.md` focused on activation, inputs, outputs, procedure, decision logic, validation, dependencies, and failure modes.
- Do not add skill-specific support material to top-level `references/` or `assets/`.

---

# Procedure

## 1. Mode Selection

1.1 Determine whether the user is asking to **apply** this skill to chat content or **review/improve** this skill itself.
1.2 IF the user provides chat history, says "use this chat to skill", asks to extract a skill, or asks what skill comes from the chat, THEN choose **apply mode**.
1.3 IF the user explicitly asks to review, rate, amend, or improve `chat-to-skill`, THEN choose **review mode**.
1.4 IF both are requested, THEN perform apply mode first and review mode second.
1.5 In apply mode, do not critique or improve `chat-to-skill` until after returning the classification and proposed skill artifact.
1.6 In review mode, do not create a new skill unless the user also supplied chat content and asked for extraction.

## 2. Intake

2.1 Read the chat content from start to finish.
2.2 Identify the main thing the chat accomplished.
2.3 Identify all artifacts produced by the chat, including documents, scripts, prompts, decisions, files, and operating rules.
2.4 Identify the minimum inputs needed to reproduce the same kind of outcome.
2.5 Identify any explicit user constraints that shaped the process.
2.6 If the chat is too long or mixed, segment it into candidate input -> process -> output chains.

## 3. Existing Skill Check

3.1 Read `MANIFEST.md` before proposing a new skill.
3.2 Compare the candidate workflow against existing `skill_name`, `skill_id`, `description`, and `trigger_keywords`.
3.3 If one existing skill clearly covers the same workflow, classify the chat as an amendment.
3.4 If the chat adds examples or source material but no new procedure, classify it as a reference for the existing skill.
3.5 If the chat adds an executable helper but no new workflow, classify it as a script for the existing skill.
3.6 If no existing skill covers the workflow, continue as a new skill candidate.

## 4. Classification

4.1 Classify as **new skill** only when all conditions are true:

- The workflow is repeatable across different instances of the same problem.
- Inputs are identifiable.
- Outputs are identifiable.
- Procedure steps can be written without relying on the original chat.
- Failure modes or validation checks can be stated.

4.2 Classify as **amendment** when the chat materially improves an existing skill's procedure, validation, scope, trigger, or support layers.
4.3 Classify as **reference** when the chat contains useful context, examples, decisions, or notes but no new repeatable procedure.
4.4 Classify as **asset** when the main artifact is a template, image, exported file, fixture, or reusable non-code artifact.
4.5 Classify as **script** when the main artifact is executable code or automation with no broader workflow.
4.6 Classify as **split** when the chat contains multiple unrelated workflows; create one classification per workflow.
4.7 Classify as **insufficient** when the workflow cannot be reconstructed.
4.8 Classify as **reject** when the material is one-off, obsolete, unsafe, or not useful to preserve.
4.9 Include confidence as `high`, `medium`, or `low` with one reason.

## 5. Naming and Metadata

5.1 Name the skill after what it does, not after the chat, user, organization, or tool.
5.2 Use kebab-case for the folder and `name` field.
5.3 Use underscore form for the final `skill_id` segment.
5.4 Compose `skill_id` as `epcb.<domain>.<skill_name>`.
5.5 Infer the domain from the subject matter, such as `meta`, `contracts`, `content`, `governance`, `ops`, `hardware`, or `data`.
5.6 Write `description` as one concise functional sentence.
5.7 Write `trigger_keywords` as comma-separated verbs, nouns, and synonyms that help an AI decide when to load the skill.

## 6. Extraction

6.1 Extract the objective as one paragraph that states what the workflow does and what output it produces.
6.2 Extract required inputs as concrete objects, files, fields, or decisions.
6.3 Extract optional inputs only when defaults or fallbacks exist.
6.4 Extract outputs as specific artifacts or decisions.
6.5 Extract procedure steps in the order needed for repeatable execution, not necessarily the order the chat wandered through.
6.6 Convert implicit decisions into explicit IF/THEN logic.
6.7 Extract rules as hard constraints.
6.8 Extract failure modes and pair each with a recovery action.
6.9 Extract dependencies, including other skills, files, scripts, tools, APIs, and source materials.
6.10 Extract assumptions that would surprise a first-time executor.
6.11 If the procedure exceeds 15 major steps, evaluate whether the workflow should be split.

## 7. Progressive Disclosure Plan

7.1 Keep only core execution logic in `skill.md`.
7.2 Move raw chat snippets, detailed examples, and lengthy explanations to `references/`.
7.3 Move templates, sample outputs, images, screenshots, and exported files to `assets/`.
7.4 Move reusable code or command helpers to `scripts/`.
7.5 In `skill.md`, reference supplied support files by relative path only after those files exist.
7.6 Do not create support files unless their contents are known or supplied.

## 8. Skill Draft Construction

8.1 Build frontmatter with these required fields:

```yaml
---
build_number: "001"
skill_id: "epcb.<domain>.<skill_name>"
name: "<kebab-case-name>"
description: "<one-line functional summary>"
trigger_keywords: "<comma-separated activation terms>"
owner: "EPCB"
status: "active"
created_at: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---
```

8.2 Add an Index table immediately after frontmatter.
8.3 Add these sections in order:

1. Objective
2. Trigger
3. Do Not Use When
4. Required Inputs
5. Optional Inputs
6. Outputs
7. Support Layers
8. Procedure
9. Decision Logic
10. Validation
11. Rules
12. Failure Modes
13. Dependencies
14. Assumptions
15. Change Log

8.4 Write procedure steps in imperative form.
8.5 Avoid references to "the chat", "above", "earlier", or "as discussed" inside the generated skill body.
8.6 Keep examples short inside `skill.md`; move long examples to support files.

## 9. Repo Action Selection

9.1 For a new skill, suggest:

```bash
./system/scripts/new_skill.sh <skill-name> <domain>
```

9.2 For an amendment, suggest:

```bash
./system/scripts/bump_skill.sh <existing-skill-folder>
```

9.3 For a reference, suggest adding a file under:

```text
skills/<skill-name>/references/
```

9.4 For an asset, suggest adding a file under:

```text
skills/<skill-name>/assets/
```

9.5 For a script, suggest adding a file under:

```text
skills/<skill-name>/scripts/
```

9.6 After any repo change, suggest:

```bash
python3 system/scripts/update_index.py
python3 system/scripts/validate_skills.py
python3 system/scripts/update_index.py --check
```

## 10. Validation

10.1 Verify the classification is justified by the chat evidence.
10.2 Verify a new skill does not duplicate an existing manifest row.
10.3 Verify every generated skill has `trigger_keywords`.
10.4 Verify every generated skill includes "Use this skill when" or "Use when".
10.5 Verify the skill can be executed without the original chat.
10.6 Verify all referenced support files are listed in the support-file plan.
10.7 Verify no large raw chat transcript is placed directly in `skill.md`.
10.8 Verify apply mode was completed before any review-mode commentary when extraction was requested.
10.9 If any check fails, revise before returning output.

# Decision Logic

- IF the chat contains no repeatable workflow, THEN do not create a skill.
- IF the user asks to apply this skill to a chat, THEN classify and extract before reviewing this skill.
- IF the chat improves an existing skill, THEN recommend a version bump instead of overwriting the live version.
- IF the chat contains only examples or background context, THEN recommend `references/`.
- IF the chat contains only a reusable artifact, THEN recommend `assets/`.
- IF the chat contains only executable automation, THEN recommend `scripts/`.
- IF the chat contains multiple unrelated workflows, THEN split them and classify each independently.
- IF classification is uncertain, THEN return `insufficient` and request the missing context.

# Validation

A chat-to-skill result is valid when all checks pass:

1. Classification is one of: new skill, amendment, reference, asset, script, split, insufficient, reject.
2. New skill and amendment outputs include a complete `skill.md` draft.
3. Support material is assigned to `references/`, `assets/`, or `scripts/`.
4. New skill IDs use `epcb.<domain>.<skill_name>`.
5. Skill folder names use kebab-case.
6. The proposed repo action preserves version history.
7. `MANIFEST.md` remains the only discovery layer.

# Rules

- Do not silently overwrite an existing live skill.
- Do not create a new skill before checking `MANIFEST.md`.
- Do not put raw chat dumps into `skill.md`.
- Do not create a second discovery system.
- Do not rename `skill.md`.
- Do not assume every useful chat should become a skill.
- Do not review or improve `chat-to-skill` instead of applying it when the user supplied chat content for extraction.
- Prefer classification accuracy over producing more skills.
- Keep the generated skill self-contained, but keep bulky context in support folders.

# Failure Modes

- Chat is too vague to reconstruct: return `insufficient` and ask for a structured summary.
- Chat contains multiple workflows: return `split` and list each candidate workflow.
- Existing skill already covers the workflow: return `amendment` and name the skill folder to bump.
- Support artifact is referenced but not supplied: list it in the support-file plan without inventing contents.
- Proposed skill name is too broad: rename using the main output or action.
- Generated skill depends on original chat context: rewrite the affected section.

# Dependencies

- `MANIFEST.md`: required for existing skill comparison
- AISkills folder convention: required for repo action selection
- `system/scripts/new_skill.sh`: used to scaffold new skills
- `system/scripts/bump_skill.sh`: used to amend existing skills
- `system/scripts/update_index.py`: used to regenerate `MANIFEST.md`
- `system/scripts/validate_skills.py`: used to validate governed skills

# Assumptions

- The chat has ended or reached a stable checkpoint.
- The user wants durable repo knowledge, not just a prose summary.
- AISkills keeps `MANIFEST.md` as the only discovery layer.
- Support material should live inside the individual skill folder unless it is truly global.

# Change Log

## V004
- Added explicit old-chat intake workflow for new skill, amendment, reference, asset, script, split, insufficient, and reject classifications.
- Added mode-selection guardrails so extraction requests produce skill artifacts before review commentary.
- Updated naming rules to use kebab-case folders and underscore `epcb.<domain>.<skill_name>` IDs.
- Added progressive disclosure guidance for skill-local `references/`, `assets/`, and `scripts/`.
- Added repo action selection for scaffold, bump, and support-file additions.
- Added validation checks aligned with AISkills manifest-only discovery and support-folder doctrine.

## V003
- Added mandatory Index Window section.
- Changed naming rule: plain descriptive names, no org prefixes.
- Added cold-execution validation checklist.
- Clarified classification rules with concrete examples.
- Aligned output format to match contract-to-skill and other ACDC skills.
- Removed explicit reference to chat-context in procedure steps.
