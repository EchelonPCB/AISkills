---
build_number: "008"
skill_id: "epcb.meta.chat_to_skill"
name: "chat-to-skill"
description: "Classify old AI chats and return complete, validated AISkills skill files with repo-ready metadata and support plans."
trigger_keywords: "chat, summarize, convert, workflow, extract skill, copy paste skill, epcb id, quality check, old AI chat"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-19"
---

# Index

| Field       | Detail                                                                 |
|-------------|------------------------------------------------------------------------|
| Trigger     | Old or completed AI chat may contain a reusable workflow               |
| Input       | Raw chat, chat summary, existing skills, scaffold metadata, repo context |
| Output      | Classification, complete skill.md, changelog note, support-file plan   |
| Key Steps   | Select mode -> isolate source -> extract -> generalize -> validate     |
| Fails When  | Chat lacks repeatable inputs, steps, outputs, or sufficient context    |
| Name Rule   | Folder uses kebab-case; skill_id uses epcb.<domain>.<skill_name>       |

---

# Objective

Convert completed AI conversations into governed AISkills artifacts. Determine whether each chat contains a reusable workflow, an amendment to an existing skill, a reference, an asset, a script, or insufficient material. For valid workflows, produce one complete, self-contained, copy-pastable `skill.md` file plus repo-ready metadata, a changelog note, and a support-file plan that fits the AISkills repository structure.

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
4. One complete fenced `skill.md` file when classification is new skill or amendment
5. Support-file plan listing what belongs in `references/`, `assets/`, and `scripts/`
6. Validation checklist showing whether the result is ready to add to AISkills
7. When the user asked for extraction, the proposed new or amended skill comes before any critique of this skill
8. No partial skill fragments, header-only blocks, or scattered sections when a skill file is required
9. Changelog guidance for `skills/<skill-name>/CHANGELOG.md` when a scaffold or bump command is used

# Support Layers

- Put raw chat excerpts, long examples, source notes, rubrics, and background context in `references/`.
- Put source-code excerpts, prior documents, long command output, and source notes in `references/`.
- Put templates, images, exported documents, example outputs, fixtures, and other non-code artifacts in `assets/`.
- Put executable helpers, parsers, generators, validators, or repeatable command wrappers in `scripts/`.
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
1.7 IF the user supplies this skill text plus a source chat, THEN treat this skill text as operating instructions and the source chat as the material to classify.
1.8 IF the user complains that a prior response reviewed this skill instead of extracting a skill, THEN restart in apply mode and return the missing artifact first.

## 2. Intake

2.1 Separate operating instructions from source material.
2.2 Read the source chat content from start to finish.
2.3 Identify the main thing the source chat accomplished.
2.4 Identify all artifacts produced by the source chat, including documents, scripts, prompts, decisions, files, and operating rules.
2.5 Identify the minimum inputs needed to reproduce the same kind of outcome.
2.6 Identify any explicit user constraints that shaped the process.
2.7 If the source chat is too long or mixed, segment it into candidate input -> process -> output chains.

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
5.4 Compose `skill_id` exactly as `epcb.<domain>.<skill_name>`.
5.5 Infer the domain from the subject matter, such as `meta`, `contracts`, `content`, `governance`, `ops`, `hardware`, or `data`.
5.6 Write `description` as one concise functional sentence.
5.7 Write `trigger_keywords` as comma-separated verbs, nouns, and synonyms that help an AI decide when to load the skill.
5.8 Never generate `acdc.*`, `legacy.*`, owner-specific, or tool-specific IDs for AISkills output.
5.9 If a generated ID does not start with `epcb.`, rewrite it before returning the file.
5.10 Prefer broad reusable domains over duplicated organization names in the domain segment.
5.11 If the subject is an organization-specific workflow, put the organization in the skill name when useful and keep the domain general.
5.12 Example: prefer `epcb.governance.acdc_governance_system` over `epcb.acdc_governance.acdc_governance_system`.

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
6.12 Identify whether the workflow has modes, such as baseline vs continuation, create vs update, draft vs validate, or local vs remote execution.
6.13 Preserve mode behavior in the generated skill when different inputs require different procedures.
6.14 Generalize source-chat-specific examples into reusable categories unless the specific example is essential to the skill.
6.15 Move project-specific examples, long transcripts, and detailed case history to the support-file plan instead of embedding them in `skill.md`.

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
8.7 Scan the completed frontmatter and verify `skill_id` starts with `epcb.` before output.
8.8 Verify the completed skill includes all required sections from Objective through Change Log.
8.9 If the user scaffolded the skill with `new_skill.sh`, preserve the scaffolded `skill_id` unless it violates `epcb.*`.
8.10 Remove scaffold placeholders from the generated `skill.md`; never return unfinished placeholder markers in a completed generated skill.
8.11 Add a `Change Log` section inside the generated `skill.md` that summarizes the generated version.

## 9. Output Assembly

9.1 For new skill or amendment classifications, return the generated file under a `Skill File` heading.
9.2 Under `Skill File`, output exactly one fenced markdown block containing the complete `skill.md` from frontmatter through Change Log.
9.3 Do not place only the YAML frontmatter in a code block.
9.4 Do not split the generated skill across multiple code blocks, bullet fragments, or prose sections.
9.5 Do not require the user to click, drag, stitch, or reconstruct the file from separated parts.
9.6 If the complete file cannot fit in one response, return `insufficient` with the reason `output space` and ask whether to continue in a file-writing workflow.
9.7 After the complete file block, return repo commands, `CHANGELOG.md` note, support-file plan, validation notes, and optional critique.
9.8 The `CHANGELOG.md` note must say what to replace or append in `skills/<skill-name>/CHANGELOG.md`.
9.9 If the repo scaffold changelog still says to replace TODOs, instruct the user to replace that scaffold line with the actual generated-skill summary.

## 10. Repo Action Selection

10.1 For a new skill, suggest:

```bash
./system/scripts/new_skill.sh <skill-name> <domain>
```

10.2 For an amendment, suggest:

```bash
./system/scripts/bump_skill.sh <existing-skill-folder> "<reason>"
```

10.3 For a reference, suggest adding a file under:

```text
skills/<skill-name>/references/
```

10.4 For an asset, suggest adding a file under:

```text
skills/<skill-name>/assets/
```

10.5 For a script, suggest adding a file under:

```text
skills/<skill-name>/scripts/
```

10.6 After any repo change, suggest:

```bash
python3 system/scripts/update_index.py
python3 system/scripts/validate_skills.py
python3 system/scripts/update_index.py --check
```

10.7 If the user has already scaffolded the skill, tell them to paste the complete generated file into the live `V###/skill.md`, update `CHANGELOG.md`, then run validation.
10.8 If updating an existing skill, require the bump command before editing and include the bump reason.

## 11. Validation

11.1 Verify the classification is justified by the source chat evidence.
11.2 Verify a new skill does not duplicate an existing manifest row.
11.3 Verify every generated skill has `trigger_keywords`.
11.4 Verify every generated skill includes "Use this skill when" or "Use when".
11.5 Verify the skill can be executed without the original chat.
11.6 Verify all referenced support files are listed in the support-file plan.
11.7 Verify no large raw chat transcript is placed directly in `skill.md`.
11.8 Verify apply mode was completed before any review-mode commentary when extraction was requested.
11.9 Verify new skill or amendment output contains one complete fenced `skill.md` block.
11.10 Verify the generated `skill_id` starts with `epcb.`.
11.11 Verify the generated skill does not contain source-chat-specific examples that should be generalized or moved to `references/`.
11.12 Verify support-layer guidance correctly separates references, assets, and scripts.
11.13 Verify any baseline, continuation, create/update, or validation modes discovered during extraction are represented.
11.14 Verify the companion `CHANGELOG.md` guidance will not leave scaffold TODO text behind.
11.15 If any check fails, revise before returning output.

# Decision Logic

- IF the chat contains no repeatable workflow, THEN do not create a skill.
- IF the user asks to apply this skill to a chat, THEN classify and extract before reviewing this skill.
- IF the chat improves an existing skill, THEN recommend a version bump instead of overwriting the live version.
- IF the chat contains only examples or background context, THEN recommend `references/`.
- IF the chat contains only a reusable artifact, THEN recommend `assets/`.
- IF the chat contains only executable automation, THEN recommend `scripts/`.
- IF the chat contains multiple unrelated workflows, THEN split them and classify each independently.
- IF classification is uncertain, THEN return `insufficient` and request the missing context.
- IF the generated ID does not start with `epcb.`, THEN rewrite the ID before returning output.
- IF the generated skill is split across fragments, THEN reassemble it into one complete fenced `skill.md` block before returning output.
- IF the generated skill includes source-specific examples that are not essential, THEN generalize them or move them to the support-file plan.
- IF a workflow has a first-run mode and a continuation mode, THEN include both modes explicitly.
- IF a scaffold changelog still contains placeholder text, THEN provide the replacement changelog text.

# Validation

A chat-to-skill result is valid when all checks pass:

1. Classification is one of: new skill, amendment, reference, asset, script, split, insufficient, reject.
2. New skill and amendment outputs include a complete `skill.md` draft.
3. Support material is assigned to `references/`, `assets/`, or `scripts/`.
4. New skill IDs use `epcb.<domain>.<skill_name>`.
5. Skill folder names use kebab-case.
6. The proposed repo action preserves version history.
7. `MANIFEST.md` remains the only discovery layer.
8. New skill and amendment outputs are returned as one complete fenced markdown file.
9. No generated skill uses `acdc.*` or any non-`epcb.*` ID.
10. Source-specific examples are generalized unless they are core to the skill.
11. Support-layer assignments follow AISkills references, assets, and scripts doctrine.
12. Generated repo guidance includes a changelog update when scaffold or bump commands are used.

# Rules

- Do not silently overwrite an existing live skill.
- Do not create a new skill before checking `MANIFEST.md`.
- Do not put raw chat dumps into `skill.md`.
- Do not create a second discovery system.
- Do not rename `skill.md`.
- Do not assume every useful chat should become a skill.
- Do not review or improve `chat-to-skill` instead of applying it when the user supplied chat content for extraction.
- Do not generate a skill ID that does not start with `epcb.`.
- Do not return a generated skill as scattered fragments or a header-only code block.
- Do not treat this skill's instructions as the source material when a separate source chat is supplied.
- Do not leave scaffold TODO text in either the generated `skill.md` or companion changelog guidance.
- Do not embed narrow project examples when a reusable category will preserve the same meaning.
- Do not put executable code, command wrappers, or validators in `assets/`; assign them to `scripts/`.
- Prefer classification accuracy over producing more skills.
- Keep the generated skill self-contained, but keep bulky context in support folders.

# Failure Modes

- Chat is too vague to reconstruct: return `insufficient` and ask for a structured summary.
- Assistant reviews `chat-to-skill` instead of extracting from supplied chat: restart in apply mode and return the missing classification and skill file first.
- Generated ID uses a non-`epcb.*` prefix: rewrite frontmatter and repo action before returning output.
- Generated skill appears as a header plus scattered sections: reassemble the complete file into one fenced markdown block.
- Generated skill carries source-chat-specific examples: generalize the procedure text and list the specific example as optional reference material.
- Generated skill misses baseline or continuation behavior: add mode selection and mode-specific decision logic.
- Scaffold changelog remains stale: provide replacement `CHANGELOG.md` text before validation.
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

## V008
- Added quality checks for source-specific examples, mode coverage, support-layer placement, and scaffold changelog sync.
- Added guidance to preserve scaffolded `epcb.*` IDs and prefer broad domain names.
- Added repo output requirements for companion `CHANGELOG.md` updates after scaffold or bump commands.
- Clarified references, assets, and scripts placement for generated skills.

## V007
- Added a strict one-block output contract for generated `skill.md` files.
- Added recovery behavior for assistants that review this skill instead of applying it.
- Added hard rejection and rewrite rules for non-`epcb.*` generated IDs.
- Added validation checks preventing header-only or fragmented skill output.

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
