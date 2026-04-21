---
build_number: "001"
skill_id: "epcb.ssunc.multi_institution_integration"
name: "ssunc-multi-institution-integration"
description: "Define and execute a standardized multi-institution autonomous systems testbed using shared environment constraints and independent vehicle implementations."
trigger_keywords: "ssunc integration, multi school robotics, autonomy testbed setup, vehicle environment separation, rc autonomy competition"
owner: "EPCB"
status: "active"
created_at: "2026-04-20"
last_updated: "2026-04-20"
---

# Index

| Section | Description |
|--------|-------------|
| Objective | Define structured multi-institution integration model |
| Trigger | When to apply this system |
| Do Not Use When | Misuse conditions |
| Required Inputs | Core inputs needed |
| Optional Inputs | Additional context |
| Outputs | Deliverables produced |
| Support Layers | Supporting systems |
| Procedure | Execution steps |
| Decision Logic | Structural decisions |
| Validation | Correctness checks |
| Rules | Non-negotiable constraints |
| Failure Modes | Common breakdowns |
| Dependencies | External requirements |
| Assumptions | Operating assumptions |
| Change Log | Version history |

---

# Objective

Establish a scalable, repeatable framework for integrating multiple institutions into a shared autonomous systems testbed where each team develops independent vehicles and all validation occurs within a standardized, controlled environment.

This enables cross-platform validation, eliminates shared hardware dependencies, and enforces real-world systems engineering discipline.

---

# Trigger

Use this skill when:

- multiple teams or institutions are participating in a shared robotics or autonomy system
- hardware cannot be centralized or shared
- validation must be consistent across different implementations
- a project risks becoming fragmented due to unclear ownership boundaries
- a competition or testbed is being designed

---

# Do Not Use When

Do not use this skill when:

- only one team is building the system
- hardware is fully centralized and controlled by one group
- no standardized testing or evaluation is required
- the system is purely simulation-based

---

# Required Inputs

1. Defined environment (track, hazards, rules)
2. Vehicle platform options (e.g., Waveshare, custom builds)
3. Core behavior requirement (minimum autonomy loop)
4. Acceptance criteria for validation

---

# Optional Inputs

- Tiered autonomy levels
- Hardware constraints (Jetson Nano, Orin, etc.)
- Institutional roles (faculty, students, advisors)
- Documentation standards
- Logging requirements

---

# Outputs

- Defined **Vehicle vs Environment ownership model**
- Tiered **Autonomy Levels (L0–L4)**
- Standardized **Test Procedure**
- Integration-ready **Participation Model**
- Acceptance criteria for all participants

---

# Support Layers

- Architecture Layer: cross-platform autonomy stack and vehicle/environment interface boundaries
- Program Definition Layer: SSUNC participation model, poster language, and public-facing scope
- Governance Layer: faculty brief, institutional roles, and host-team responsibility boundaries
- Hazard Validation Layer: hazard state machine behavior, repeatability checks, and evidence logs

---

# Procedure

## Step 1 — Separate Ownership Domains

Define two non-overlapping domains:

**Vehicle Domain (Participants)**
- perception
- decision logic
- control
- hardware assembly

**Environment Domain (Host / ACDC)**
- hazards (traffic lights, pedestrians)
- track layout
- timing and rules
- activation interfaces

Constraint:
→ Vehicles must NOT modify the environment  
→ Environment must NOT depend on vehicle internals  

---

## Step 2 — Define Minimum Viable Autonomy

Establish **Level 1 baseline behavior**:

- forward motion under autonomy
- hazard detection or signal interpretation
- deterministic response:
  - RED → stop
  - GREEN → go
- logging of decisions

This aligns with the minimum autonomy requirement for cross-institution validation.

---

## Step 3 — Define Autonomy Levels

Level 0 — Manual + logging  
Level 1 — Hazard response (REQUIRED)  
Level 2 — Lane following  
Level 3 — Intersection handling  
Level 4 — Advanced autonomy (lane change, planning)

Rule:
→ Only Level 1 is required for participation  
→ Higher levels are optional performance tiers  

---

## Step 4 — Define Test Execution Model

For every run:

1. Environment activates hazard (external trigger)
2. Vehicle enters test zone
3. Hazard state changes deterministically
4. Vehicle must respond correctly
5. Logs are recorded and reviewed

Core behavior validated:
→ perception → decision → actuation loop

---

## Step 5 — Standardize Hazard Behavior

Hazards must follow:

enable → delay → state change → persist

Validated via:
- simulation reference
- embedded implementation

Validate against both simulation behavior and embedded hazard implementation when available.

---

## Step 6 — Enable Multi-Team Participation

Each institution must provide:

- one team
- one vehicle platform
- one faculty contact

They must:
- build independently
- test within standardized environment
- submit logs or run live tests

---

## Step 7 — Enforce Acceptance Criteria

A valid system must:

- correctly stop on RED
- correctly proceed on GREEN
- operate repeatably across runs
- produce logs of:
  - detection
  - decision
  - actuation

---

# Decision Logic

| Scenario | Action |
|----------|--------|
| team lacks advanced autonomy | assign Level 1 only |
| hardware differs across teams | allow, enforce same environment |
| compute varies (Nano vs Orin) | normalize expectations via Level system |
| environment inconsistency detected | block testing until standardized |

---

# Validation

A valid integration is achieved when:

- multiple vehicles can run in the same environment
- hazard produces identical behavior across runs
- vehicles respond consistently to identical inputs
- no team depends on another team’s hardware

---

# Rules

- Environment is the **single source of truth**
- Vehicles must be **independent**
- Minimum requirement is **Level 1 autonomy**
- No feature expansion before baseline is stable
- Repeatability > complexity
- Logs are mandatory for validation

---

# Failure Modes

| Failure | Cause | Fix |
|--------|------|-----|
| system appears too simple | poor framing | reinforce validation focus |
| teams blocked by hardware | shared dependencies | enforce independence |
| inconsistent results | environment drift | standardize hazard timing |
| over-scoping | premature complexity | lock Level 1 requirement |

---

# Dependencies

- standardized hazard system (ESP32-based)
- Jetson-based compute platforms
- modular track environment
- logging infrastructure
- documented interface contracts

---

# Assumptions

- participants have basic robotics capability
- low-cost hardware must be supported
- environment is physically deployable
- faculty oversight exists but is not execution-heavy
- program will scale across semesters

---

# Change Log

## V001
- Initial creation from Spring SSUNC integration discussions
- Formalized vehicle vs environment separation
- Introduced autonomy level hierarchy
- Defined acceptance criteria and validation model
