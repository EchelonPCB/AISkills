# AISkills MCP Staging

This folder stages a local MCP server for AISkills.

The server is intentionally narrow. It exposes routing and validation tools first, not autonomous write/promotion tools.

## What Lives Where

```text
system/mcp/
  aiskills_server.py
  pyproject.toml
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

## Install MCP Runtime

Install `uv` if needed, then run:

```bash
cd /Users/polaszwaczka/Desktop/AISkills/system/mcp
uv sync
uv run aiskills_server.py
```

The server uses stdio transport. When run directly, it waits for an MCP client to speak JSON-RPC over stdin/stdout.

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

## Claude Code / SDK Connection

Use `.mcp.example.json` as the project-root starting point. Copy it to `.mcp.json` only when you want the repo to auto-advertise the local AISkills MCP server to compatible clients.

```bash
cp .mcp.example.json .mcp.json
```

Do not commit a machine-specific `.mcp.json` unless the path and launch command are intentionally portable.

## Connection Model

1. Claude launches `uv --directory /Users/polaszwaczka/Desktop/AISkills/system/mcp run aiskills_server.py`.
2. `aiskills_server.py` exposes MCP tools.
3. Tool calls delegate to `system/scripts/mcp_gateway.py`.
4. The gateway returns compact JSON.
5. The AI reads a single selected skill only after routing.

## Failure Points

- `uv` is not installed or not on PATH.
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
