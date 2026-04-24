---
build_number: "001"
skill_id: "epcb.pid.pid_steering_controller"
name: "pid-steering-controller"
description: "Implement and tune a PID/PI steering controller for the JPA JetRacer Pro RC car using lane offset input from the perception pipeline and PWM output to the PCA9685 servo."
trigger_keywords: "pid steering, pid controller, lane offset, servo steering, rc car steering, pid tuning, steer control, pid loop, jetracer steer, pid gains"
owner: "EPCB"
status: "active"
created_at: "2026-04-23"
last_updated: "2026-04-23"
source_contract: "CON-10"
---

# Index

| Field       | Detail                                                                              |
|-------------|-------------------------------------------------------------------------------------|
| Trigger     | RC car needs closed-loop steering from lane center offset to PWM servo command     |
| Input       | Lane center offset (pixels), camera frame, PCA9685 bus                             |
| Output      | Steering PWM ticks sent to servo; lap completion without manual intervention       |
| Key Steps   | Read offset → compute PID → clamp → convert to ticks → send to PCA9685            |
| Fails When  | Lane offset is unavailable, PCA9685 bus fails, or gains are uncalibrated           |
| PASS        | Vehicle completes one full lap staying between lane boundaries with no manual steering input |
| Name Rule   | Folder uses kebab-case; skill_id uses epcb.pid.pid_steering_controller             |

---

# Objective

Implement a PID (or PI) steering controller that receives a pixel offset from the lane center detector and outputs a PWM steering command to the JetRacer Pro servo via PCA9685. The controller must keep the car between the lane boundary lines through a full lap without any manual steering input. Speed control, V2I integration, and navigation are explicitly out of scope.

---

# Trigger

Use this skill when:

- The RC car needs closed-loop steering from a lane detection offset
- A PID controller needs to be wired into the main perception loop
- PID gains need to be tuned on the real track
- The steering module is being ported or integrated into a new demoday script
- The `pid_steer.py` file needs to be created, modified, or debugged

---

# Do Not Use When

- V2I integration or speed control is the goal (use jpa-module-integration)
- The task is lane detection algorithm development (the input offset is assumed to be provided)
- Hardware changes to the PCA9685 or servo wiring are needed
- Navigation or path planning beyond lane centering is needed

---

# Required Inputs

1. Lane center offset in pixels (positive = car is right of center, negative = left of center)
2. PCA9685 I2C bus and channel number for the steering servo
3. Hardware constants: STEER_CENTER, STEER_RIGHT_LIMIT, STEER_LEFT_LIMIT (in ticks)

---

# Optional Inputs

1. Initial PID gains (Kp, Ki, Kd) — defaults: Kp=0.8, Ki=0.01, Kd=0.3
2. Integral windup cap
3. Dead-band threshold (offset below which no correction is applied)
4. Log file path for per-frame steering telemetry

---

# Outputs

1. `pid_steer.py` — PID controller class with `compute(offset)` method returning steering ticks
2. Steering telemetry column in the session CSV: `steer_ticks`, `pid_offset`
3. Tuning guide (inline comments) for Kp, Ki, Kd adjustment on real track
4. PASS evidence: one full lap CSV log with no manual input and lane boundary compliance

---

# Out of Scope

- V2I integration (no `v2i_remaining`, no RUSH/LATE_STOP logic)
- Speed control or throttle decisions
- Navigation, waypoints, or path planning
- Hardware changes to the PCA9685, servo wiring, or car chassis
- Traffic light detection or traffic light state decisions

---

# Hardware Constants

| Constant          | Value (ticks) | Notes                                    |
|-------------------|---------------|------------------------------------------|
| STEER_CENTER      | 320           | Neutral / straight-ahead position        |
| STEER_RIGHT_LIMIT | 280           | Maximum right turn (lower tick = right)  |
| STEER_LEFT_LIMIT  | 370           | Maximum left turn (higher tick = left)   |

Unit conversion: `ticks = round(microseconds × 4096 / 20000)`

---

# Support Layers

- Put PID tuning worksheets, gain calibration logs, and track geometry notes in `references/`.
- Put sample CSV logs and steering telemetry plots in `assets/`.
- Put repeatable gain-sweep scripts or log analyzers in `scripts/`.

---

# Procedure

## 1. Confirm Input Interface

The PID controller receives one float per frame:
- `offset` — signed pixel distance of detected lane center from image center column
- Positive offset: car is to the right of lane center → steer left (increase ticks toward STEER_LEFT_LIMIT)
- Negative offset: car is to the left of lane center → steer right (decrease ticks toward STEER_RIGHT_LIMIT)
- `None` — lane not detected; controller returns STEER_CENTER and resets integral

## 2. Implement PID Controller

```python
from typing import Optional
import time

class PIDSteering:
    """PID steering controller.  Input: lane offset px.  Output: PCA9685 ticks."""

    # ── Tuning ────────────────────────────────────────────────────────────────
    # TUNING_GUIDE:
    #   Kp  – dominant gain; raise until oscillation starts, then back off ~20 %
    #   Ki  – reduce steady-state drift; start very small (0.005–0.02)
    #   Kd  – damps oscillation; raise until wobble smooths, stop before chatter
    #   Start with Kd=0 until Kp/Ki converge, then add Kd.
    # ─────────────────────────────────────────────────────────────────────────

    STEER_CENTER      = 320
    STEER_RIGHT_LIMIT = 280
    STEER_LEFT_LIMIT  = 370

    def __init__(self,
                 kp: float = 0.8,
                 ki: float = 0.01,
                 kd: float = 0.3,
                 windup_cap: float = 50.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.windup_cap = windup_cap
        self._integral   = 0.0
        self._prev_error = 0.0
        self._prev_time  = time.monotonic()

    # ── Unit conversion ───────────────────────────────────────────────────────
    @staticmethod
    def us_to_ticks(us: float) -> int:
        """Convert microseconds to PCA9685 12-bit ticks (20 ms period)."""
        return round(us * 4096 / 20000)

    # ── Main compute ──────────────────────────────────────────────────────────
    def compute(self, offset: Optional[float]) -> int:
        """
        Compute steering ticks from lane center offset.

        Parameters
        ----------
        offset : float | None
            Signed pixel offset (positive = car right of center → steer left).
            Pass None when lane is not detected.

        Returns
        -------
        int  PCA9685 tick value clamped to [STEER_RIGHT_LIMIT, STEER_LEFT_LIMIT]
        """
        if offset is None:
            self.reset()
            return self.STEER_CENTER

        now = time.monotonic()
        dt  = max(now - self._prev_time, 1e-3)

        # PID terms
        error          = float(offset)
        self._integral = max(-self.windup_cap,
                             min(self.windup_cap, self._integral + error * dt))
        derivative     = (error - self._prev_error) / dt

        correction_us  = (self.kp * error +
                          self.ki * self._integral +
                          self.kd * derivative)

        self._prev_error = error
        self._prev_time  = now

        # Positive offset → steer left → add correction
        steer_ticks = self.STEER_CENTER + int(correction_us)
        return max(self.STEER_RIGHT_LIMIT,
                   min(self.STEER_LEFT_LIMIT, steer_ticks))

    def reset(self) -> None:
        """Reset integrator and derivative state (call on RED / stop events)."""
        self._integral   = 0.0
        self._prev_error = 0.0
        self._prev_time  = time.monotonic()
```

## 3. Wire Into Main Loop

```python
from perception.pid_steer import PIDSteering

pid = PIDSteering(kp=0.8, ki=0.01, kd=0.3)

# Inside frame loop:
offset = lane_detector.get_offset(frame)   # float or None
steer_ticks = pid.compute(offset)
pca.channels[STEER_CHANNEL].duty_cycle = steer_ticks   # or equivalent PWM write
```

On any stop/RED event: call `pid.reset()` before the next GO window to prevent integral wind-up carry-over.

## 4. Tune Gains on Real Track

Follow the TUNING_GUIDE inline comments in `PIDSteering`. Sequence:
1. Zero Ki and Kd. Raise Kp until the car oscillates, then reduce ~20%.
2. Add Ki in small increments (0.005 steps) until steady-state drift disappears.
3. Add Kd to damp remaining oscillation without introducing high-frequency chatter.
4. Log `steer_ticks` and `pid_offset` in CSV each frame for post-session analysis.

## 5. PASS Verification

Run one full lap under camera-only control with no manual input. The lap log CSV must show:
- `steer_ticks` column present and non-constant throughout the run
- No manual override events in the log
- Car stayed between yellow (left) and white (right) lane boundaries — observable from video or observer confirmation

---

# Decision Logic

| Condition | Action |
|-----------|--------|
| lane offset is `None` | return `STEER_CENTER` and call `reset()` |
| computed output exceeds hardware limits | clamp to `[STEER_RIGHT_LIMIT, STEER_LEFT_LIMIT]` before write |
| stop or RED state occurs upstream | reset PID state before the next GO window |
| tuning changes are proposed without track evidence | require a logged real-track verification pass |

---

# Validation

The skill output is valid when:

1. `PIDSteering.compute(offset)` returns a clamped steering command for numeric offsets.
2. `PIDSteering.compute(None)` returns `STEER_CENTER` and clears controller state.
3. Steering output respects the published soft-stop hardware constants.
4. The integration path logs `steer_ticks` and `pid_offset` or equivalent steering telemetry.
5. PASS evidence includes a full real-track lap with no manual steering input.

---

# Rules

- Do not integrate V2I data, RUSH/LATE_STOP logic, or speed control decisions into this module.
- The controller operates on lane offset only. Traffic light state is handled upstream.
- Do not modify PCA9685 address or channel mapping without updating hardware constants in this file.
- `compute(None)` must always return STEER_CENTER and reset state — never hold a stale correction.
- All steering output must be clamped within [STEER_RIGHT_LIMIT, STEER_LEFT_LIMIT] before sending to hardware.

---

# Failure Modes

- Lane offset unavailable: return `STEER_CENTER`, reset controller state, and surface the missing-lane condition to the caller.
- Gains too aggressive: the vehicle oscillates or chatters; reduce `Kp`, then retune `Ki` and `Kd` using logged runs.
- Integral wind-up: steering remains biased after recovery; lower `Ki`, lower the windup cap, and confirm `reset()` is called on stop events.
- Steering polarity reversed: positive offset steers the car farther right instead of left; reverse the correction sign before further tuning.
- Hardware limit mismatch: controller saturates at one side too early; verify `STEER_CENTER`, `STEER_RIGHT_LIMIT`, and `STEER_LEFT_LIMIT` against the current servo calibration.

---

# Dependencies

- Lane detection output that provides a signed center offset each frame.
- PCA9685 steering output path and the correct steering channel mapping.
- Real-track validation context for final PID gain tuning and PASS evidence.
- Upstream integration logic that calls `reset()` on stop or failsafe events.

---

# Assumptions

- Lane offset sign follows the convention documented in `# Procedure`: positive means the car is right of center and must steer left.
- Steering constants remain `STEER_CENTER=320`, `STEER_RIGHT_LIMIT=280`, and `STEER_LEFT_LIMIT=370` unless new hardware calibration supersedes them.
- Final gain tuning authority comes from real-track behavior, not simulation or static reasoning alone.
- This skill owns steering correction only; throttle, V2I, and traffic-light decisions remain outside the controller.

---

# Change Log

## V001
- Added the initial governed PID steering controller skill for JPA lane-centering control.
- Documented implementation pattern, tuning sequence, validation expectations, and steering-only boundaries.
