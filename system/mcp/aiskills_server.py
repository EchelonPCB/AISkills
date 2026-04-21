#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError as exc:
    print(
        "Missing MCP Python SDK. Run `./setup_mcp_env.sh` from system/mcp "
        "or install `mcp[cli]>=1.2.0` into the Python environment launching this server.",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


ROOT = Path(__file__).resolve().parents[2]
GATEWAY = ROOT / "system" / "scripts" / "mcp_gateway.py"

mcp = FastMCP("aiskills")


def run_gateway(*args: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(GATEWAY), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        payload = {
            "ok": False,
            "errors": ["gateway returned invalid JSON"],
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    payload.setdefault("ok", result.returncode == 0)
    payload.setdefault("returncode", result.returncode)
    return payload


@mcp.tool()
def list_skills() -> dict:
    """List live AISkills records without reading skill bodies."""
    return run_gateway("list-skills")


@mcp.tool()
def select_skill(query: str, top: int = 3) -> dict:
    """Select candidate AISkills for a user task using manifest metadata only."""
    return run_gateway("select-skill", query, "--top", str(top))


@mcp.tool()
def read_skill(skill: str) -> dict:
    """Read one live skill by folder, name, skill_id, or current_path."""
    return run_gateway("read-skill", skill)


@mcp.tool()
def validate_repo() -> dict:
    """Run read-only repo consistency checks for live AISkills."""
    return run_gateway("validate-repo")


@mcp.tool()
def list_mutations() -> dict:
    """List staged mutation workspaces without promoting them."""
    return run_gateway("list-mutations")


@mcp.tool()
def validate_mutation(mutation: str, promotable: bool = False) -> dict:
    """Validate a staged mutation workspace. Set promotable to true for promotion gates."""
    args = ["validate-mutation", mutation]
    if promotable:
        args.append("--promotable")
    return run_gateway(*args)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
