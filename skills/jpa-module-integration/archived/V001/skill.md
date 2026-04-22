---
build_number: "001"
skill_id: "epcb.ops.jpa_module_integration"
name: "jpa-module-integration"
description: "Integrate new contract deliverable modules into the JPA RC car stack, restructure the repo for runtime, and rewrite the integration loop with updated fusion doctrine and PID steering."
trigger_keywords: "jpa, jetracer, demoday, contract integration, rc car, lane detect, pid steer, v2i fusion, ssunc, module wiring, deploy jetson"
owner: "EPCB"
status: "active"
created_at: "2026-04-22"
last_updated: "2026-04-22"
---

# Index

| Field     | Detail                                                                           |
|-----------|----------------------------------------------------------------------------------|
| Trigger   | New contract deliverables need wiring into the JPA RC car main loop             |
| Input     | Frozen 0409 base files, contract .py deliverables, project context files        |
| Output    | Updated demoday.py, restructured ssunc_perception/, SCP deploy commands         |
| Key Steps | Read base → read contracts → analyze stack → restructure → rewrite → verify → deploy |
| Fails When | Contract return signatures, unit mismatch, or fusion doctrine are unresolved   |
| Name Rule | Folder uses kebab-case; skill_id uses epcb.ops.jpa_module_integration          |

---

# Objective

Take a set of frozen validated base modules and newly delivered contract Python files, analyze how they connect in the full sensing and control stack, restructure the repository so the entry point runs cleanly, and rewrite the integration loop with the correct fusion doctrine, PID steering, and hardware constants. Produce a syntax-verified, import-chain-verified demoday.py and the SCP commands needed to deploy it to the Jetson.

---

# Trigger

Use this skill when:

- New contract deliverables (lane detection, PID steering, signal state machine, or similar) are ready and need to be wired into the existing JPA demoday loop.
- The repo structure needs to change so that a single entry point can find all modules at a consistent relative path.
- The fusion doctrine needs to be updated, such as switching from camera-priority fallback to an AGREE-first doctrine where both V2I and camera must confirm GO.
- Hardware constants change, such as removing a steer_center.txt file dependency and hardcoding the value.
- The Jetson deploy path or module layout changes and SCP commands need updating.

---

# Do Not Use When

- The frozen base files need to be changed. Those are validated and locked.
- The task is purely adding a new AISkills domain skill unrelated to JPA hardware integration.
- The request is a code review only with no restructuring or rewrite needed.
- No contract deliverables exist yet and nothing is ready to wire in.

---

# Required Inputs

1. Frozen base files: `3led_detector.py`, `3led_v2i.py`, `3led_demoday.py` (or equivalent 0409 originals).
2. Contract deliverable files: one or more of `lane_detect.py`, `pid_steer.py`, `yellow_fallback.py`.
3. Project context: `CLAUDE.md` and `PROJECT.md` from the JPA workspace.
4. Confirmation of fusion doctrine from the user: AGREE-first (both sensors required) or camera-priority fallback.
5. Confirmed STEER_CENTER tick value from the hardware constants table.

---

# Optional Inputs

1. Jetson IP address and confirmed remote path layout for SCP commands.
2. Existing `.zshrc` aliases to determine whether `jpush` or `jpa_deploy` helpers already exist.
3. Prior engineering work records to avoid duplicating documented history.
4. Run log CSV files from prior sessions for stack behavior context.
5. TRACK_WIDTH_PX measurement from a real camera frame on the ASVP track.

---

# Outputs

1. `demoday.py` at the repo root — the single entry point that imports all four modules, enforces the fusion doctrine, runs PID steering when GO, and resets the PID integrator on every STOP.
2. `ssunc_perception/` folder containing all four runtime modules: `traffic_light_detector.py`, `v2i_receiver.py`, `lane_detect.py`, `pid_steer.py`.
3. Syntax verification result across all six Python files.
4. Import chain verification confirming all four imports resolve and core logic checks pass.
5. SCP deploy commands matched to the confirmed Jetson path layout.
6. Optional: `.zshrc` alias block with `jpush`, `jpa_deploy`, and `jetson` shortcuts.

---

# Support Layers

- Put prior engineering work records, run log CSVs, and annotated frame screenshots in `references/`.
- Put hardware constant tables, wiring diagrams, and track photos in `assets/`.
- Put standalone test harnesses and calibration scripts in `scripts/`.
- Do not edit frozen 0409 base files; keep them in `0409/Dev/` as the verified archive.

---

# Procedure

## 1. Select the Skill

1.1 Use AISkills MCP `select_skill` with a query covering the task domain before reading any skill body.
1.2 Read only the selected skill body. Load skill-local references only if needed.

## 2. Read the Frozen Base Files

2.1 Read `3led_detector.py` and record: ROI coordinates, HSV thresholds, confidence gate, return type.
2.2 Read `3led_v2i.py` and record: UDP port, timeout value, `get_latest()` return signature, `is_live` property.
2.3 Read `3led_demoday.py` and record: all hardware constants, existing fusion branches, steering behavior, CSV log columns, sys.path setup.

## 3. Read the Contract Deliverable Files

3.1 Read each contract file and record: class name, public method signatures and return types, internal units (µs vs ticks), hardware constants, any `steer_center.txt` or file dependencies.
3.2 For `lane_detect.py`: confirm slope-sign classifier is present, confirm return signature is `(offset, left_x, right_x, yellow_x)`, note `ROI_TOP` value and `TRACK_WIDTH_PX` constant.
3.3 For `pid_steer.py`: confirm `STEER_CENTER_US` value, confirm `PWM_MIN` and `PWM_MAX` match hardware soft stops, confirm `reset()` method exists, confirm output unit is µs.
3.4 For `yellow_fallback.py`: confirm it is a standalone contract test harness only and is NOT imported into demoday.py.

## 4. Read Project Context

4.1 Read `CLAUDE.md` and `PROJECT.md` for workspace boundaries and engine relationship rules.
4.2 Confirm that AIGST, AISkills, and GSD are not to be edited unless explicitly requested.

## 5. Analyze the Full Integration Stack

5.1 Map all six modules into three layers: sensor modules, integration loop, control.
5.2 Confirm the two ROI regions do not conflict: traffic light detector uses upper frame, lane detector uses bottom 45%.
5.3 Verify the unit bridge: `us_to_ticks(us) = round(us × 4096 / 20000)`. Check center (1563µs → 320 ticks), right limit (1367µs → 280 ticks), left limit (1807µs → 370 ticks).
5.4 Check for V2I timeout mismatch: `V2IReceiver.TIMEOUT_S` vs `yellow_fallback.PACKET_TIMEOUT_S`. Document discrepancy if present.
5.5 Confirm `TRACK_WIDTH_PX` is documented as requiring physical measurement before the first run.
5.6 Identify any file dependencies (steer_center.txt, legacy paths) that must be removed.

## 6. Clarify Fusion Doctrine with User

6.1 Confirm whether the target doctrine is AGREE-first (both V2I and camera must confirm GREEN for GO) or camera-priority.
6.2 Confirm V2I-offline fallback behavior: camera-only authority when V2I packet age exceeds timeout.
6.3 Document the confirmed doctrine before writing any code.

## 7. Restructure the Repository

7.1 Copy each contract deliverable file into `ssunc_perception/`. Do not move or rename frozen 0409 base files.
7.2 Place `demoday.py` at the repo root.
7.3 Confirm the final layout: `demoday.py` at root, `ssunc_perception/` containing all four runtime modules, `0409/Dev/` as frozen archive, `logs/` auto-created at runtime, `Debug/` unchanged.

## 8. Rewrite demoday.py

8.1 Replace the hardcoded absolute `sys.path` with a relative path derived from `__file__`:
    `sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssunc_perception'))`
8.2 Add imports: `from lane_detect import LaneDetector` and `from pid_steer import PIDSteering, STEER_CENTER_US`.
8.3 Remove all `steer_center.txt` file-read logic. Set `STEER_CENTER = 320` as a named constant.
8.4 Add `us_to_ticks()` helper.
8.5 Implement the confirmed fusion doctrine in a `fuse()` function with named `decision_source` labels for every branch.
8.6 In `main()`: instantiate `LaneDetector` and `PIDSteering(steer_center=STEER_CENTER_US)`.
8.7 Move log file creation inside `main()` or guard with `if __name__ == '__main__'`.
8.8 In the main loop, call `lane_det.get_offset(frame)` every tick regardless of state.
8.9 When `final_state == GREEN`: call `pid.compute(lane_offset)`, apply `us_to_ticks()`, clamp to `[STEER_RIGHT_LIMIT, STEER_LEFT_LIMIT]`, write to `CH_STEER`.
8.10 When `final_state != GREEN`: call `pid.reset()`, write `STEER_CENTER` to `CH_STEER`.
8.11 Add a consecutive camera-failure counter. After `CAM_FAIL_LIMIT` consecutive failures, call `safe_stop()`.
8.12 Expand `annotate_frame()` to use `lane_det._last_debug` as the base frame so the lane overlay is visible in the MJPEG stream.
8.13 Expand CSV log columns to include `lane_offset` and `steer_ticks`.
8.14 Set `PRINT_EVERY_N_LOOPS = 30` for approximately one heartbeat print per second at 30fps.

## 9. Verify

9.1 Run `ast.parse()` on all six Python files. All must pass with no syntax errors.
9.2 Run an import chain check: insert `ssunc_perception/` into `sys.path`, import all four modules, instantiate each class, verify `STEER_CENTER_US == 1563`, verify `us_to_ticks()` for center and both limits, verify `pid.compute(0.0) == 1563`, verify `pid.compute(None) == 1563`, verify `restrictive()` for all key cases.
9.3 If any check fails, fix the defect before proceeding.

## 10. Prepare Jetson Deploy Commands

10.1 Confirm Jetson username, IP address, and whether `ssunc_perception/` exists at `/home/jetson/` or inside `/home/jetson/jetson/`.
10.2 If the deploy path has changed, confirm the user wants to establish the new layout before transferring.
10.3 Write SCP commands for: `demoday.py`, `lane_detect.py`, `pid_steer.py`. Note that frozen files (`traffic_light_detector.py`, `v2i_receiver.py`) should already be present.
10.4 If `.zshrc` aliases exist for Jetson transfer, read them and provide updated `jpa_deploy` function matching the new file set. If they do not exist, provide a `.zshrc` block the user can add.
10.5 Provide the remote run command: `cd ~ && python3 -u demoday.py`.

---

# Decision Logic

| Condition | Action |
|-----------|--------|
| User confirms AGREE-first doctrine | Both sensors must return GREEN; any mismatch picks the more restrictive state |
| V2I is offline (packet age > timeout) | Camera is sole authority; UNKNOWN camera → FAILSAFE RED |
| Only one white border visible in lane detect | Use TRACK_WIDTH_PX single-border fallback; flag value as requiring physical measurement |
| Slope-sign classifier not in lane_detect.py | Block integration; x-midpoint classifier causes track departure on drift |
| PID output unit is µs | Apply us_to_ticks() before writing to PCA9685; do not write µs values as ticks |
| steer_center.txt file dependency found | Remove it; hardcode STEER_CENTER as 320 ticks |
| V2I timeout mismatch between modules | Document discrepancy; the deployed V2IReceiver timeout governs real behavior |
| Contract return signature is float or None | Update to 4-tuple before integration; old signature breaks the call site |
| yellow_fallback.py present in repo | Keep as standalone contract test harness; do not import into demoday.py |
| Jetson path layout unclear | Ask user to confirm before writing SCP commands |
| Existing .zshrc aliases found | Read them and update jpa_deploy to match new file set |
| No .zshrc aliases found | Provide alias block for jpush, jpa_deploy, and jetson shortcut |

---

# Validation

A valid integration is complete when:

1. All six Python files parse without syntax errors.
2. All four module imports resolve from the relative ssunc_perception/ path.
3. `us_to_ticks(1563) == 320`, `us_to_ticks(1367) == 280`, `us_to_ticks(1807) == 370`.
4. `pid.compute(0.0) == 1563` and `pid.compute(None) == 1563`.
5. `restrictive('GREEN', 'RED') == 'RED'` and `restrictive('UNKNOWN', 'RED') == 'RED'`.
6. No reference to `steer_center.txt` remains in `demoday.py`.
7. `sys.path` uses a relative path from `__file__`, not a hardcoded absolute Jetson path.
8. Fusion doctrine matches the user-confirmed behavior: AGREE-first when V2I is live, camera fallback when offline.
9. `pid.reset()` is called on every non-GREEN state.
10. CSV log columns include `lane_offset` and `steer_ticks`.

---

# Rules

- Do not modify frozen 0409 base files under any circumstances.
- Do not import `yellow_fallback.py` into `demoday.py`; its behaviors are enforced directly in the fusion logic.
- Do not write µs values directly to `set_pwm()`; always convert with `us_to_ticks()` first.
- Do not leave any `steer_center.txt` file reads or fallback logic in `demoday.py`.
- Do not use the absolute Jetson path `/home/jetson/jetson/ssunc_perception` in `sys.path`; use the relative path from `__file__`.
- Do not mark a PID output as correct without verifying the servo direction on real hardware.
- Do not transfer frozen files unless the user confirms the Jetson's existing copies need updating.
- Do not skip the import chain verification step before declaring the integration complete.

---

# Failure Modes

| Failure | Recovery |
|---------|----------|
| lane_detect returns float or None instead of 4-tuple | Update call site to unpack (offset, left_x, right_x, yellow_x) or update module |
| PID writes µs ticks directly to PCA9685 | Add us_to_ticks() at the call site; verify with hardware constant table |
| steer_center.txt missing on Jetson at startup | Hardcode STEER_CENTER = 320; remove all file-read logic |
| Camera drops mid-run and loops forever | Add consecutive-failure counter; call safe_stop() after CAM_FAIL_LIMIT failures |
| Fusion allows camera-only GO when V2I is live | Re-examine fuse() branches; AGREE branch must be the only path to GREEN when V2I is live |
| Slope-sign classifier reverses on tight curves | Single-border fallback activates; verify TRACK_WIDTH_PX is measured, not estimated |
| Jetson cannot find ssunc_perception/ modules | Confirm demoday.py is at the same level as ssunc_perception/; verify relative path resolves |
| V2I timeout mismatch causes unexpected early stop | Document the effective timeout; if 2.0s is too tight, align V2IReceiver.TIMEOUT_S to contract spec |
| PID steers wrong direction on hardware | Negate correction in pid_steer.py or reverse polarity in the steer PWM write |

---

# Dependencies

- Python 3.8+ with `cv2`, `numpy`, `smbus2` installed on the Jetson.
- `traffic_light_detector.py` and `v2i_receiver.py` present and validated in `ssunc_perception/`.
- `lane_detect.py` with slope-sign classifier and 4-tuple return from `get_offset()`.
- `pid_steer.py` with `STEER_CENTER_US = 1563`, hardware-matched PWM limits, and `reset()` method.
- PCA9685 on I²C bus 1 at address 0x40, prescale 121, 50Hz.
- ESP32 V2I transmitter sending JSON UDP packets to port 5005.
- SSH access to Jetson for SCP deployment.

---

# Assumptions

- The frozen 0409 base files are validated and correct; no changes to their logic are needed.
- STEER_CENTER is 320 ticks (1563µs) based on the hardware constants table in the ACDC procedure document.
- The JPA track has two white border lines, optional yellow center line, and dark floor, consistent with the lane_detect.py tuning.
- TRACK_WIDTH_PX = 300 is an estimate; physical measurement is required before the first run.
- The servo wiring on this JetRacer Pro produces left turns at higher tick values; verify if uncertain.
- Manifest unavailable; duplicate check not performed.

---

# Change Log

## V001
- Created governed JPA module integration skill capturing the AGREE-first fusion doctrine, contract module wiring procedure, repo restructuring for demoday.py runtime, unit bridge verification, and Jetson deploy preparation workflow.
