# Runtime Target Validation

Use this reference when a generated skill targets physical hardware, a remote machine, a cloud runtime, or a mixed environment.

## Target Gate

Before finalizing, identify the execution target:

- local development host
- remote host
- physical hardware
- cloud service
- mixed environment

Then separate checks into:

- development-host checks: syntax, static analysis, path shape, pure logic, mocked imports
- target-runtime checks: real imports, device access, network binds, credentials, hardware interfaces, service permissions, safety behavior

Missing target-only dependencies on the development host are environment mismatches, not code defects.

## Jetson Hardware Minimum

For Jetson robotics skills, require target verification on the Jetson for:

1. real imports for `cv2`, `numpy`, `smbus2`, and project modules
2. camera open through the selected capture pipeline
3. PCA9685 visible on I2C bus 1 at address `0x40`
4. UDP or V2I bind on the expected port
5. safe-stop or failsafe behavior before any motion command

Do not mark the skill PASS until the target-runtime evidence exists, or clearly hand off the exact target checks the user must run on hardware.
