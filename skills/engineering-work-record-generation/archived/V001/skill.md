---
build_number: "001"
skill_id: "epcb.ops.engineering_work_record_generation"
name: "engineering-work-record-generation"
description: "Generate structured, chronological engineering work records from chat context while avoiding duplication with prior documented sessions."
trigger_keywords: "work log, engineering record, lab session, generate report, chronological session, continuation doc, avoid repetition, technical report"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-19"
---

# Index

| Field       | Detail                                                                 |
|-------------|------------------------------------------------------------------------|
| Trigger     | Need to convert a chat or session into a formal engineering work record |
| Input       | Chat context, prior work records, session date                         |
| Output      | Complete structured engineering work record document                   |
| Key Steps   | Context analysis -> overlap filtering -> structuring -> drafting       |
| Fails When  | Prior records missing or session context unclear                       |
| Name Rule   | Folder uses kebab-case; skill_id uses epcb.ops.engineering_work_record_generation |

---

# Objective

Generate a complete, structured engineering work record from a chat or session context that aligns with existing documentation, avoids duplication, and reflects true chronological progression of technical work.

---

# Trigger

Use this skill when:

- A lab session or engineering work needs to be formally documented
- Chat history represents a completed work session
- Prior work records already exist and continuity must be preserved
- The user requests a chronological continuation of previous engineering documentation

---

# Do Not Use When

- The user only wants a summary of a chat
- There are no prior work records and no need for continuity
- The session is incomplete or still exploratory
- The content is purely theoretical without execution

---

# Required Inputs

1. Current session chat context
2. Date of the session
3. At least one prior engineering work record

---

# Optional Inputs

1. Desired tone (formal vs narrative)
2. Emphasis preference (hardware vs software vs balanced)
3. Supporting artifacts (code, logs, screenshots)

---

# Outputs

1. Complete engineering work record document
2. Chronological continuation aligned with prior sessions
3. Clearly separated sections:
   - Objective
   - Background
   - Process
   - Observations
   - Outcomes
   - Next Steps

---

# Support Layers

- Store prior work records in `references/`
- Store code artifacts in `assets/`
- Store automation scripts in `scripts/`

---

# Procedure

## 1. Intake

1.1 Read the full chat context  
1.2 Read all prior work records  
1.3 Identify the session date and scope  

---

## 2. Overlap Analysis

2.1 Compare chat content against prior records  
2.2 Identify overlapping topics (I2C debugging, perception validation, etc.)  
2.3 Mark all repeated content as “do not restate”  
2.4 Extract only new developments  

---

## 3. Session Framing

3.1 Define what makes this session distinct  
3.2 Identify:
- New failures
- New implementations
- New decisions
- New system-level understanding  

3.3 Establish session identity (e.g., regression, integration, validation phase)

---

## 4. Content Extraction

4.1 Extract technical progress  
4.2 Extract debugging logic  
4.3 Extract engineering decisions  
4.4 Extract system behavior observations  

---

## 5. Structuring

5.1 Build document in this order:

- Objective  
- Background Context  
- Primary Work Streams  
- Observations  
- Decisions  
- Current State  
- Outcomes  
- Next Steps  

---

## 6. De-duplication Enforcement

6.1 Do NOT:
- Re-explain previously validated systems  
- Repeat earlier debugging steps  
- Re-describe already proven architectures  

6.2 Instead:
- Reference prior validation implicitly  
- Focus only on progression  

---

## 7. Technical Depth

7.1 Maintain system-level reasoning  
7.2 Include cause → action → result chains  
7.3 Avoid vague summaries  
7.4 Preserve engineering language and precision  

---

## 8. Output Drafting

8.1 Write in formal engineering tone  
8.2 Ensure logical flow between sections  
8.3 Maintain consistency with prior records  
8.4 Ensure readability and structure  

---

# Decision Logic

- IF prior records exist → enforce continuation mode  
- IF overlap detected → remove redundancy  
- IF new failure present → center session around it  
- IF subsystem progresses independently → separate it explicitly  
- IF chat includes multiple domains → structure into parallel work streams  

---

# Validation

A valid work record must:

1. Not duplicate prior sessions  
2. Clearly represent new progress  
3. Maintain chronological continuity  
4. Include structured sections  
5. Be readable as a standalone document  

---

# Rules

- Do not restate previously documented work  
- Do not collapse multiple sessions into one narrative  
- Do not omit key engineering reasoning  
- Do not write informal summaries  
- Always maintain structured format  

---

# Failure Modes

### Missing prior context
→ Ask for previous work records

### Excessive overlap
→ Reduce content to only new developments

### Vague session content
→ Request clarification before writing

### Mixed session timelines
→ Separate into distinct records

---

# Dependencies

- Prior engineering work records
- Chat session logs
- Project context (hardware/software system)

---

# Assumptions

- Prior sessions are already documented
- The user wants continuity, not repetition
- The chat represents a completed session
- The output is intended for formal documentation

---

# Change Log

## V001
- Initial extraction from SSUNC / ASVP lab workflow
- Captures continuation-based engineering documentation process