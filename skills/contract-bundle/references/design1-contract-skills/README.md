# Design 1 Contract Skill References

These files are reference artifacts for `Contract Bundle Execution`.

## Provenance

- Created from Chat-to-Skill (CTS) based on chat-to-contract output.
- Used alongside the Design 1 contract bundle to execute CON-01 through CON-04.
- Preserved here as reference inputs and examples, not as live routed AISkills.

## Reference Set

| Contract | File | Purpose |
|----------|------|---------|
| CON-01 | `CON-01_cap_bank_sizing_skill.md` | Cap bank sizing workflow and evidence requirements |
| CON-02 | `CON-02_battery_capacity_skill.md` | Battery capacity workflow and evidence requirements |
| CON-03 | `CON-03_power_path_architecture_skill.md` | Power path architecture workflow and evidence requirements |
| CON-04 | `CON-04_simple_arbitration_logic_skill.md` | Simple arbitration logic workflow and evidence requirements |

## Use

When executing a Design 1 contract bundle, use the live `Contract Bundle Execution` skill as the orchestrator and these files as the contract-specific reference workflows.

Do not add these files to `MANIFEST.md` unless the Design 1 contract workflows are intentionally promoted into governed live skills.
