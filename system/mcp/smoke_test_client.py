#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import anyio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "system" / "mcp" / "run_aiskills_mcp.sh"
EXPECTED_TOOLS = {
    "list_skills",
    "select_skill",
    "read_skill",
    "validate_repo",
    "list_mutations",
    "validate_mutation",
}


def first_text(result) -> str:
    if not result.content:
        return ""
    item = result.content[0]
    return item.text if hasattr(item, "text") else str(item)


def parse_json_result(result) -> dict:
    text = first_text(result)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"ok": False, "raw": text}


async def main() -> None:
    params = StdioServerParameters(
        command=str(RUNNER),
        args=[],
        cwd=str(ROOT),
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tool_names = [tool.name for tool in tools_result.tools]
            missing = sorted(EXPECTED_TOOLS.difference(tool_names))
            print("MCP tools:", ", ".join(tool_names))
            if missing:
                raise SystemExit(f"Missing expected MCP tools: {', '.join(missing)}")

            validate_result = await session.call_tool("validate_repo", {})
            validate_payload = parse_json_result(validate_result)
            print("validate_repo ok:", validate_payload.get("ok") is True)
            if validate_result.isError or validate_payload.get("ok") is not True:
                raise SystemExit(first_text(validate_result))

            route_result = await session.call_tool(
                "select_skill",
                {"query": "turn this chat into a skill", "top": 3},
            )
            route_payload = parse_json_result(route_result)
            matches = route_payload.get("matches", [])
            top_match = matches[0].get("skill_name") if matches else None
            print("select_skill top match:", top_match)
            if route_result.isError or top_match != "chat-to-skill":
                raise SystemExit(first_text(route_result))

            read_result = await session.call_tool(
                "read_skill",
                {"skill": "chat-to-skill"},
            )
            read_payload = parse_json_result(read_result)
            print("read_skill chat-to-skill ok:", read_payload.get("ok") is True)
            if read_result.isError or read_payload.get("ok") is not True:
                raise SystemExit(first_text(read_result))

    print("MCP smoke test passed")


if __name__ == "__main__":
    anyio.run(main)
