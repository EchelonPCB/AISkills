---
build_number: "002"
skill_id: "epcb.ops.jetson_multinode_devops"
name: "jetson-multinode-devops"
description: "Set up and operate an SSH/SCP-based multi-node Jetson development and deployment workflow."
trigger_keywords: "jetson, ssh, scp, deploy, push, pull, zshrc, multi-node, hotspot, usb networking"
owner: "EPCB"
status: "active"
created_at: "2026-04-19"
last_updated: "2026-04-19"
---

# Index

| Field       | Detail                                                            |
|-------------|-------------------------------------------------------------------|
| Trigger     | Need repeatable file sync and deployment across Jetson nodes      |
| Input       | Host labels, users, IPs, local paths, remote paths, SSH access    |
| Output      | Working push, pull, deploy, and host-selection command layer      |
| Key Steps   | Map hosts -> configure SSH -> define paths -> add commands -> test |
| Fails When  | Network, SSH keys, permissions, or path resolution are wrong      |
| Name Rule   | Use for Jetson or Linux-node SSH/SCP devops workflows             |

---

# Objective

Create a repeatable multi-node development workflow for Jetson-based systems using SSH, SCP, shell aliases, and path-resolution functions. The output is a local command layer that can push files, pull files or directories, deploy code, and target one or more remote nodes without repeatedly writing raw SSH/SCP commands.

# Trigger

Use this skill when:

- Developing on a Jetson or Linux-based embedded node from a local workstation
- Managing more than one SSH target, such as a Jetson and a secondary desktop or compute node
- Replacing repeated `scp` commands with reusable `push`, `pull`, or `deploy` helpers
- Switching between USB networking, hotspot networking, or multiple known host addresses
- Building a fast edit-transfer-run loop for hardware or robotics development

# Do Not Use When

- The work is entirely local and does not require SSH or SCP
- Remote hosts are not reachable on the network
- The user needs fleet orchestration, containers, Kubernetes, or CI/CD rather than shell-level development helpers
- The remote system cannot accept SSH keys or password-based SSH login
- The workflow requires secure production deployment rather than development convenience

# Required Inputs

1. Local workstation shell: usually `zsh` or another shell that can define aliases/functions
2. Remote host inventory: label, username, hostname or IP, and preferred connection route for each node
3. Remote home or project directory for each host
4. Local project files or directories to transfer
5. SSH access to each remote host

# Optional Inputs

1. Preferred host priority, such as USB before hotspot
2. Passwordless SSH key setup
3. Remote run command, such as `python3 -u main.py`
4. Process cleanup command for deploy loops
5. Verbose/debug mode for SSH or SCP troubleshooting

# Outputs

1. Host mapping for Jetson and related nodes
2. Shell functions or aliases for `push`, `pull`, and `deploy`
3. Path-resolution behavior for absolute and relative remote paths
4. Validation checks for SSH, file transfer, and multi-host targeting
5. Failure-mode playbook for common SSH/SCP/network issues

# Support Layers

- Put full `.zshrc` examples or host-specific command snippets in `references/`.
- Put network diagrams, screenshots, exported configs, or fixture files in `assets/`.
- Put reusable shell helpers or generated scripts in `scripts/`.
- Keep machine-specific IPs, usernames, and private paths out of the generic `skill.md` unless they are examples clearly marked as replaceable.

# Procedure

## 1. Define the Node Inventory

1.1 List each target node with a short label, such as `jetson`, `desktop`, or `car`.
1.2 For each node, record:

- SSH username
- preferred hostname or IP
- backup hostname or IP
- remote home directory
- remote project directory

1.3 Mark which connection route each address represents, such as USB, hotspot, LAN, or static Ethernet.
1.4 Do not assume all nodes share the same username or home directory.

## 2. Verify Network Reachability

2.1 On the local workstation, test each known address with `ping` when ICMP is available.
2.2 Test SSH manually before writing helper functions:

```bash
ssh <user>@<host>
```

2.3 On the remote node, inspect addresses when needed:

```bash
ip a
hostname -I
```

2.4 If using Wi-Fi or hotspot routing, confirm the local workstation and remote node are on the same network.
2.5 Record which address is most reliable for repeated development.

## 3. Configure SSH Keys

3.1 Generate an SSH key if the workstation does not already have one.
3.2 Install the public key on each remote host:

```bash
ssh-copy-id <user>@<host>
```

3.3 Re-test login and confirm it no longer requires a password.
3.4 If passwordless SSH is not allowed, keep the helper functions but expect interactive password prompts.

## 4. Define Shell Configuration

4.1 Open the local shell configuration file, such as `~/.zshrc`.
4.2 Define one variable per host label, username, and remote directory.
4.3 Define a host selector that maps labels to `user@host`.
4.4 Define a remote path resolver:

- IF the remote path starts with `/`, treat it as absolute.
- IF the remote path is relative, resolve it under the host's configured remote project directory or home directory.

4.5 Keep host identity logic separate from path logic.
4.6 Reload the shell configuration after edits:

```bash
source ~/.zshrc
```

## 5. Implement Push Commands

5.1 Create a `push` helper for the default Jetson target.
5.2 Create named variants only when useful, such as `pushjetson` or `pushdesktop`.
5.3 Support both files and directories:

- IF source is a file, use `scp`.
- IF source is a directory, use `scp -r`.

5.4 Preserve the original filename when no destination filename is provided.
5.5 Print the resolved destination before transfer so wrong-path errors are visible.

## 6. Implement Pull Commands

6.1 Create a `pull` helper that resolves a remote path and downloads it locally.
6.2 Support both files and directories:

- IF remote source is a file, use `scp`.
- IF remote source is a directory, use `scp -r`.

6.3 Accept absolute remote paths without modifying them.
6.4 Resolve relative paths under the configured remote base directory.
6.5 Print the resolved remote path before transfer.

## 7. Implement Deploy Loop

7.1 Define the deploy command as a development convenience, not a production deployment system.
7.2 Upload the target file or project directory.
7.3 Optionally stop the prior remote process if a safe process name is known.
7.4 Start the remote command over SSH only when remote execution is intended.
7.5 For hardware safety, document whether the process should be stopped locally, over SSH, or physically on the device.

## 8. Validate End to End

8.1 Confirm SSH works for each host label.
8.2 Push one small test file to each target.
8.3 Pull the same test file back from each target.
8.4 Push and pull one test directory to confirm recursive handling.
8.5 Test absolute and relative remote paths.
8.6 Test the deploy helper with a harmless command before using live hardware code.
8.7 Remove test files after validation.

# Decision Logic

- IF more than one address is available for a host, THEN prefer the most reliable route and keep backups explicit.
- IF USB networking is available and stable, THEN prefer it for direct Jetson development.
- IF hotspot networking is used, THEN verify both devices are on the hotspot subnet.
- IF a path starts with `/`, THEN treat it as absolute and do not prepend a remote base path.
- IF a path is relative, THEN resolve it under the configured remote base path.
- IF transferring a directory, THEN use recursive SCP.
- IF process control affects physical hardware, THEN prefer explicit remote or physical shutdown instructions over blind local interrupts.

# Validation

The workflow is valid when:

1. Each configured host connects through SSH.
2. Host labels resolve to the correct `user@host`.
3. `push` works for at least one file.
4. `pull` works for at least one file.
5. Directory transfer uses recursive SCP.
6. Absolute remote paths are not rewritten.
7. Relative remote paths resolve predictably.
8. Deploy behavior is tested with a harmless command before hardware use.

# Rules

- Do not hardcode one home directory for every host.
- Do not mix host-selection logic with path-resolution logic.
- Do not assume local interrupts safely stop remote hardware behavior.
- Do not hide resolved paths; print them before transfer.
- Do not treat this skill as production deployment security guidance.
- Do not store private keys, passwords, or secrets in skill files, references, assets, or scripts.

# Failure Modes

- SSH permission denied: install or repair SSH keys with `ssh-copy-id`, or verify username and host.
- Host unreachable: check subnet, cable, hotspot, IP address, and whether SSH is enabled.
- SCP reports "not a regular file": retry with recursive SCP for directories.
- Remote file not found: print and verify the resolved remote path with `ssh <host> 'ls -la <path>'`.
- Transfer hangs: retry with verbose SSH/SCP flags and verify network stability.
- Wrong host receives files: inspect host selector variables and print `user@host` before transfer.
- Hardware process keeps running: stop it on the remote node or use the documented physical shutdown path.

# Dependencies

- SSH client on the local workstation
- SSH server on each remote node
- SCP or compatible file-transfer tool
- Shell configuration file such as `~/.zshrc`
- Network route between workstation and remote nodes
- Optional: SSH keys for passwordless login

# Assumptions

- Remote nodes are Linux-based and reachable by SSH.
- The workflow is for development iteration, not hardened production deployment.
- The user can edit local shell configuration.
- The user has permission to transfer files to the remote target directories.
- Host-specific examples should be stored in `references/` rather than embedded in this generic skill.

# Change Log

See CHANGELOG.md
