---
build_number: "002"
skill_id: "epcb.ops.engineering_work_record_generation"
name: "engineering-work-record-generation"
description: "Generate baseline or continuation engineering work records from session context without duplicating prior documentation."
trigger_keywords: "engineering record, work log, lab session, document progress, generate report, continuation record, baseline record, technical summary"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-19"
---

# Index

| Field       | Detail                                                               |
|-------------|----------------------------------------------------------------------|
| Trigger     | Need to convert a technical session into an engineering work record  |
| Input       | Session context, session date, project context, prior records        |
| Output      | Structured baseline or continuation engineering work record          |
| Key Steps   | Select mode -> extract work -> remove overlap -> structure -> verify |
| Fails When  | Session context, timeline, or required project facts are unclear     |
| Name Rule   | Folder uses kebab-case; skill_id uses epcb.ops.engineering_work_record_generation |

---

# Objective

Generate a complete engineering work record from a chat transcript, session notes, or structured summary. Produce either a baseline record for a first documented session or a continuation record that preserves chronological continuity and avoids repeating prior documented work.

# Trigger

Use this skill when:

- A technical work session needs to become a formal engineering record
- A chat history or session summary contains implementation, testing, debugging, validation, or design decisions
- Prior records exist and the new record must continue the history without restating old work
- No prior record exists but the user needs a first baseline record for the project
- The user wants a durable technical document rather than a casual chat summary

# Do Not Use When

- The user only wants a short summary or status update
- The session is purely brainstorming with no concrete technical work, decision, or result
- The requested output is a contract, governance decision, or reusable skill file
- Required session facts are missing and cannot be inferred safely

# Required Inputs

1. Current session context: chat transcript, notes, or structured summary
2. Session date or date range
3. Project or system name
4. Intended record mode: baseline, continuation, or infer from context

# Optional Inputs

1. Prior engineering work records for continuation mode
2. Desired audience: internal team, advisor, reviewer, sponsor, or archive
3. Desired tone: formal, narrative, concise, or technical
4. Supporting artifacts: code excerpts, test outputs, images, datasets, diagrams, or command output
5. Required document template or section headings

# Outputs

1. Complete engineering work record document
2. Mode label: baseline or continuation
3. Chronological account of new technical work
4. Clearly separated sections for objective, context, work performed, observations, decisions, current state, and next steps
5. List of missing facts or assumptions when the record cannot be completed with confidence

# Support Layers

- Put prior work records, source summaries, long command output, code excerpts, and technical notes in `references/`.
- Put document templates, screenshots, diagrams, exported reports, and sample output files in `assets/`.
- Put repeatable record generators, parsers, formatters, or validation helpers in `scripts/`.
- Do not copy full raw chat logs into `skill.md`; preserve only the process required to generate the record.

# Procedure

## 1. Select Record Mode

1.1 Read the current session context and identify whether it is the first documented session or a continuation.
1.2 If prior records are supplied, select continuation mode.
1.3 If no prior records are supplied and the user needs documentation, select baseline mode.
1.4 If the mode cannot be determined, ask whether the output should begin a new record chain or continue an existing one.

## 2. Establish Session Scope

2.1 Identify the project, subsystem, date, participants if supplied, and main technical objective.
2.2 Identify what kind of work occurred: design, implementation, debugging, testing, validation, integration, analysis, or planning.
2.3 Separate concrete work from speculation, side comments, and unresolved ideas.
2.4 Flag missing facts that would change the technical record.

## 3. Analyze Continuity

3.1 In continuation mode, compare the current session against prior records.
3.2 Mark repeated background, already validated systems, and previously documented debugging as prior context.
3.3 Extract only new progress, new failures, new decisions, new evidence, and changed understanding.
3.4 In baseline mode, include enough background to make the first record self-contained without over-explaining the project.

## 4. Extract Engineering Content

4.1 Extract actions performed during the session.
4.2 Extract observations and evidence, including test results, error states, measurements, screenshots, or behavior changes.
4.3 Extract engineering reasoning as cause-action-result chains.
4.4 Extract decisions and the rationale for each decision.
4.5 Extract current state and remaining blockers.

## 5. Structure the Record

5.1 Build the document with this default structure unless the user provides another template:

1. Title
2. Session Date
3. Mode
4. Objective
5. Background Context
6. Work Performed
7. Observations and Evidence
8. Decisions Made
9. Current State
10. Next Steps
11. Assumptions or Missing Information

5.2 Use parallel work streams when the session covers independent subsystems.
5.3 Keep chronology clear inside each section.
5.4 Keep background shorter in continuation mode than in baseline mode.

## 6. Enforce De-Duplication

6.1 Do not restate prior work as if it happened in the current session.
6.2 Do not repeat earlier explanations unless they are required to understand a new result.
6.3 Refer to prior records briefly when continuity matters.
6.4 If most of the session repeats prior work, produce a short delta record focused on what changed.

## 7. Draft the Work Record

7.1 Write in a formal engineering tone.
7.2 Use precise subsystem names, file names, measurements, commands, and observed states when supplied.
7.3 Avoid vague phrases such as "worked on things" or "made progress" without details.
7.4 Preserve uncertainty as uncertainty; do not invent results, causes, dates, or decisions.
7.5 End with concrete next steps that follow from the current state.

## 8. Verify the Record

8.1 Confirm the record is readable without the original chat.
8.2 Confirm the record does not duplicate prior sessions.
8.3 Confirm each major claim traces back to session context or a supplied artifact.
8.4 Confirm missing information is listed instead of invented.
8.5 Confirm the output format matches the user's requested template when one is supplied.

# Decision Logic

- IF prior records are supplied, THEN use continuation mode.
- IF no prior records are supplied and documentation is still needed, THEN use baseline mode.
- IF overlap with prior records is found, THEN summarize it as prior context and focus on new deltas.
- IF the session includes multiple independent subsystems, THEN separate them into work streams.
- IF technical evidence is missing for a major claim, THEN mark the claim as unresolved or request clarification.
- IF the user supplies a document template, THEN preserve the required headings unless they conflict with the record's accuracy.

# Validation

A valid work record must:

1. Identify whether it is baseline or continuation mode.
2. State the session date or date range.
3. Describe the session objective and scope.
4. Separate prior context from current-session progress.
5. Include actions, observations, decisions, current state, and next steps.
6. Avoid duplicating prior records except for brief continuity references.
7. List assumptions or missing facts when source material is incomplete.
8. Read as a standalone engineering document.

# Rules

- Do not invent technical results, causes, measurements, dates, participants, or decisions.
- Do not collapse multiple sessions into one timeline unless the user explicitly requests a combined record.
- Do not paste full raw chat transcripts into the final record.
- Do not treat brainstormed ideas as completed work.
- Do not store executable code examples in `assets/`; use `references/` for source excerpts and `scripts/` for runnable helpers.
- Keep the final document focused on engineering evidence, reasoning, and next action.

# Failure Modes

- Missing session date: ask for the date or label the date as unknown.
- Missing prior records in continuation mode: switch to baseline mode or request the prior records.
- Excessive overlap with prior records: write a short delta record focused on new developments.
- Vague session content: request clarification for objective, actions, evidence, and outcome.
- Mixed timelines: split the content into separate dated records.
- Unsupported technical claim: mark the claim as unverified and list the needed evidence.

# Dependencies

- Current session transcript, notes, or structured summary
- Prior engineering records when continuation mode is required
- Project context, subsystem names, and relevant artifact references
- Optional document template or reporting standard

# Assumptions

- The user wants a formal engineering record, not just a conversational summary.
- Prior records, when supplied, are already accepted as documented history.
- The output may be used for internal project continuity or external review.
- The `ops` domain is retained for this skill because it supports engineering operations and recordkeeping workflows.

# Change Log

## V002
- Added baseline mode for first engineering records when no prior record exists.
- Generalized source-specific examples into reusable engineering documentation rules.
- Clarified support-layer placement for references, assets, and scripts.
- Reworked failure modes into explicit recovery actions.

## V001
- Initial extraction from SSUNC / ASVP lab workflow.
- Captured continuation-based engineering documentation process.
