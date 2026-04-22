---
build_number: "016"
skill_id: "epcb.meta.chat_to_skill"
name: "chat-to-skill"
description: "Convert raw chats or chat summaries into structured, reusable, version-ready AISkills skill files."
trigger_keywords: "chat, classify chat, apply skill, extract skill, workflow intake, copy paste skill, epcb id, old AI chat"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-22"
---

# Index

| Need | Load |
|------|------|
| Repo-backed create or bump | `references/repo-backed-mode.md` |
| Offline single-file answer | `references/offline-copy-paste-mode.md` |
| Required generated skill shape | `references/skill-format-contract.md` and `assets/governed-skill-template.md` |
| Hardware, Jetson, remote runtime | `references/runtime-target-validation.md` |
| Output cleanup and anti-contamination | `references/output-contracts.md` |
| Final quality gate | `references/ralph-gate.md` |

Default path: classify first, ask only when blocked, then use the minimum reference set for the selected mode.

---

# Objective

Turn a raw chat, chat summary, or workflow note into a governed AISkills skill without contaminating the live repo with stale assumptions, unvalidated hardware claims, duplicate skill bodies, or copy-paste wrapper text.

This skill has no fixed word or character limit. The effective limits are repo validation and token economy: keep generated live skill bodies under 500 lines when practical, never exceed the AISkills validator limit, and move examples, long procedures, templates, and domain specifics into `references/`, `scripts/`, or `assets/`.

---

# Trigger

Use this skill when:

- A conversation needs to become a reusable AISkills `skill.md`.
- A generated skill needs to be classified as new, amendment, reference, asset, script, reject, or insufficient.
- A repo-backed skill write must be done through `new_skill.sh` or `bump_skill.sh`.
- A copy-paste-only assistant must return exactly one governed `skill.md` block.
- A hardware or remote-runtime skill needs separate development-host and target-runtime validation gates.

---

# Do Not Use When

- The user is asking to execute an existing domain workflow rather than create or update a skill.
- The task is only a normal code edit, repo cleanup, or git operation.
- The source material is exploratory and cannot be converted into a reusable procedure without at least one targeted clarification.
- The user asks for a reference file, script, or asset only; classify it that way and do not force it into a skill.

---

# Required Inputs

1. Source chat, summary, or workflow description.
2. Desired mode if stated: repo-backed write, offline copy-paste, advisory, or classification only.
3. Skill identity if supplied: folder name, frontmatter `name`, `skill_id`, owner, status, dates, and intended domain.
4. Runtime target when relevant: local host, remote host, Jetson or other physical hardware, cloud service, or mixed environment.

---

# Optional Inputs

1. Existing `MANIFEST.md`, `system/indexes/skill-index.json`, or MCP `list_skills` output.
2. Existing skill body when the request is an amendment.
3. User preference for whether to ask one clarifying question before generation.
4. Related references, scripts, assets, contracts, logs, or validation output.

---

# Outputs

1. Classification: `new_skill`, `amendment`, `reference`, `asset`, `script`, `reject`, or `insufficient`.
2. In repo-backed mode: a new or bumped live skill plus updated indexes and validation summary.
3. In offline copy-paste mode: exactly one fenced `skill.md` block, with no extra prose inside the block.
4. If blocked: one concise question or a short blocker list, not a speculative full skill.

---

# Support Layers

- Use `references/repo-backed-mode.md` only when the assistant can see the AISkills repo.
- Use `references/offline-copy-paste-mode.md` only when the assistant cannot use repo files or MCP.
- Use `references/skill-format-contract.md` for generated skill section rules.
- Use `references/runtime-target-validation.md` for hardware, Jetson, remote, and mixed-runtime gates.
- Use `references/output-contracts.md` before returning or writing any artifact.
- Use `references/ralph-gate.md` as the final bounded quality loop.
- Use `assets/governed-skill-template.md` as the skeleton for a new governed skill.

---

# Procedure

1. Classify the request before drafting.
2. If repo context exists, inspect `MANIFEST.md`, `system/indexes/skill-index.json`, or MCP `list_skills` before reading any skill body.
3. If a matching live skill exists and the user wants a change, classify as `amendment`; run `system/scripts/bump_skill.sh <folder> "<reason>"` before editing.
4. If no matching skill exists, classify as `new_skill`; use `system/scripts/new_skill.sh <folder> <domain>` when writing in the repo.
5. Ask one targeted question only when the missing answer would change identity, target runtime, destructive scope, or validation authority. Otherwise proceed with explicit assumptions.
6. Load only the reference files needed for the selected mode.
7. Generate or update the skill using the required frontmatter and section order.
8. For hardware or remote-runtime skills, separate development-host checks from target-runtime checks before marking validation complete.
9. Run RALPH once, repair concrete defects, and run one final pass if needed.
10. In repo-backed mode, run index update and skill validation before reporting completion.

---

# Decision Logic

| Condition | Action |
|-----------|--------|
| Manifest or index is visible | Use repo-backed mode; do not include offline manifest-unavailable assumptions |
| No repo/index/MCP context is visible | Use offline copy-paste mode and disclose duplicate-check limits only inside `# Assumptions` |
| Existing skill covers the workflow | Bump the skill; do not overwrite the current live version |
| User-supplied folder and frontmatter name conflict | Ask which identity is authoritative |
| Missing fact affects runtime safety or repo identity | Ask one concise question before generating |
| Missing fact is minor and recoverable | Proceed with an explicit assumption |
| Target is Jetson or physical hardware | Require target-runtime validation for dependencies, devices, interfaces, and failsafe behavior |
| Dependency is missing only on the development host | Record environment mismatch; do not label it a code defect |
| Source is only reference material | Produce or stage a reference, not a skill |
| Source is only reusable code | Produce or stage a script or asset, not a skill |

---

# Validation

A valid CTS run satisfies all of these checks:

1. Classification is stated before generation or repo mutation.
2. Repo-backed mode uses manifest/index/MCP discovery before reading skill bodies.
3. Material amendments are made in a bumped version, never by overwriting an existing live `V###/skill.md`.
4. Generated skills contain required AISkills frontmatter keys in order.
5. Generated skills include the required top-level sections in the validator order.
6. `trigger_keywords` is present in YAML frontmatter and contains at least three comma-separated entries.
7. No source artifacts remain: AI citation markers, scaffold placeholders, TODO text, stale changelog instructions, or markdown wrappers inside saved skill files.
8. Hardware or remote-runtime skills identify development-host checks separately from target-runtime checks.
9. Jetson skills require real target checks for imports, camera, I2C/PCA9685, network bind, and safe-stop behavior before motion.
10. Repo-backed output has no text such as `Manifest unavailable; duplicate check not performed.`
11. Offline output is exactly one fenced `skill.md` block unless the user requested a different artifact.

---

# Rules

- Do not scan every skill body to find duplicates; use manifest, index, MCP, or selected live skill first.
- Do not create a new skill when a targeted bump of an existing skill is the correct action.
- Do not include companion files in a single-file copy-paste response unless the user explicitly asked for those files.
- Do not bury a required clarification inside a generated skill. Ask the question before generation.
- Do not ask broad exploratory questions. Ask at most one concise question unless the user requested a design interview.
- Do not treat missing Jetson-only packages on macOS as a failed Jetson integration.
- Do not mark hardware validation complete without target-runtime evidence.
- Do not carry offline-only assumptions into repo-backed live skills.

---

# Failure Modes

| Failure | Recovery |
|---------|----------|
| Generated skill duplicates an existing manifest row | Reclassify as amendment and bump the existing skill |
| Live `V###` was edited directly | Preserve that version as historical state, bump, and apply corrections in the new current version |
| Output includes wrapper prose inside the fenced skill | Regenerate the single fenced block cleanly |
| Skill body grows near the validator line limit | Move details into references, scripts, or assets and link them from `# Support Layers` |
| Hardware validation mixes host and target checks | Split checks and require target evidence before PASS |
| RALPH does not converge after two passes | Stop and hand off concrete blockers |

---

# Dependencies

- AISkills repo with `MANIFEST.md`, `system/indexes/skill-index.json`, and validation scripts for repo-backed mode.
- `system/scripts/new_skill.sh`, `system/scripts/bump_skill.sh`, `system/scripts/update_index.py`, and `system/scripts/validate_skills.py`.
- AISkills MCP tools when available: `list_skills`, `select_skill`, `read_skill`, and `validate_repo`.
- Skill-local references and template listed in `# Support Layers`.

---

# Assumptions

- Repo-backed mode is preferred whenever AISkills files or MCP tools are available.
- Offline copy-paste mode exists for assistants that cannot access the repo; it is not the default inside AIGST.
- The user benefits from one targeted question when the answer prevents a wrong skill identity, wrong runtime target, or unsafe hardware validation claim.
- Token savings come mainly from smaller live skill bodies, compact discovery outputs, and avoiding broad log or skill-body scans.

---

# Change Log

## V016
- Compressed the live CTS body from the near-limit V015 into a progressive-disclosure router.
- Moved detailed repo-backed, offline, formatting, runtime, output, and RALPH rules into references.
- Added an optional one-question clarification gate for identity, target runtime, destructive scope, and validation authority.
- Clarified that CTS has no fixed word or character limit; practical limits are validator line count and token economy.

## V015
- Added repo-backed mode, runtime target gating, and required generated `# RALPH Loop` sections.
