# AISkills MCP Staging

This folder stages a local MCP server for AISkills.

The server is intentionally narrow. It exposes routing and validation tools first, not autonomous write/promotion tools.

## What Lives Where

```text
system/mcp/
  aiskills_server.py
  pyproject.toml
  requirements.txt
  setup_mcp_env.sh
  run_aiskills_mcp.sh
  claude_desktop_config.example.json

system/scripts/
  mcp_gateway.py
  validate_mutation.py
  select_skill.py
  update_index.py
  validate_skills.py

system/indexes/
  skill-index.json
```

Use `system/scripts/` directly for local testing. Use `system/mcp/aiskills_server.py` when connecting an MCP host.

## Exposed MCP Tools

Read-only and staging-safe tools:

- `list_skills`: list live skills without reading skill bodies
- `select_skill`: route a user task using manifest metadata only
- `read_skill`: read one selected live skill
- `validate_repo`: run index and skill validation checks
- `list_mutations`: list staged mutation workspaces
- `validate_mutation`: validate a staged mutation workspace

Promotion, archive, deletion, commit, and push are intentionally not exposed as MCP tools yet.

## Local CLI Smoke Tests

From the repo root:

```bash
python3 system/scripts/mcp_gateway.py list-skills
python3 system/scripts/mcp_gateway.py select-skill "turn this chat into a skill"
python3 system/scripts/mcp_gateway.py read-skill chat-to-skill
python3 system/scripts/mcp_gateway.py validate-repo
python3 system/scripts/mcp_gateway.py list-mutations
python3 system/scripts/mcp_gateway.py validate-mutation chat-to-contracts
```

## Install MCP Runtime Without uv

Use the venv setup path on macOS when `uv` is not installed:

```bash
cd /Users/polaszwaczka/Desktop/AISkills/system/mcp
chmod +x setup_mcp_env.sh run_aiskills_mcp.sh
./setup_mcp_env.sh
```

The server uses stdio transport. When run directly, it waits for an MCP client to speak JSON-RPC over stdin/stdout.
Use `system/mcp/smoke_test_client.py` from the repo root for manual protocol testing.

## Optional uv Runtime

If you later install `uv`, this also works:

```bash
cd /Users/polaszwaczka/Desktop/AISkills/system/mcp
uv sync
uv run aiskills_server.py
```

## Claude Desktop Connection

Claude Desktop reads MCP server configuration from:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Copy the contents of:

```text
system/mcp/claude_desktop_config.example.json
```

into that file, then fully restart Claude Desktop.

The current Claude Desktop example launches Python directly instead of executing `run_aiskills_mcp.sh`. This avoids macOS blocking Claude Desktop from executing shell scripts inside protected folders such as `Desktop`.

## Claude Code / SDK Connection

Use `.mcp.example.json` as the project-root starting point. Copy it to `.mcp.json` only when you want the repo to auto-advertise the local AISkills MCP server to compatible clients.

```bash
cp .mcp.example.json .mcp.json
```

Do not commit a machine-specific `.mcp.json` unless the path and launch command are intentionally portable.

## Connection Model

1. Claude launches `/usr/local/opt/python@3.14/bin/python3.14 /Users/polaszwaczka/Desktop/AISkills/system/mcp/aiskills_server.py`.
2. `aiskills_server.py` exposes MCP tools.
3. Tool calls delegate to `system/scripts/mcp_gateway.py`.
4. The gateway returns compact JSON.
5. The AI reads a single selected skill only after routing.

## Sync, Async, Or Hybrid

Current choice: hybrid, with synchronous tool calls at the repo boundary.

- MCP host/server protocol: stdio, event-driven by the client.
- MCP tool functions: synchronous wrappers.
- Repo operations: synchronous subprocess calls.
- Future path: async wrappers only if multiple long-running tools need parallel execution.

Why this is intentional:

- The repo is local and small.
- Routing and validation commands are fast.
- Synchronous subprocess calls are easier to audit and safer for write gates.
- Async would add complexity before there is real latency pressure.

Do not expose parallel write tools until transaction safety is stronger.

## Failure Points

- MCP venv was not created with `setup_mcp_env.sh`.
- MCP SDK dependency is not installed.
- Claude config JSON has invalid syntax.
- Config path is relative instead of absolute.
- Server logs to stdout instead of stderr.
- `MANIFEST.md` or `system/indexes/skill-index.json` is stale.
- The AI scans archived skills or mutation workspaces as live skills.

Run this before blaming MCP:

```bash
python3 system/scripts/mcp_gateway.py validate-repo
```
