#!/bin/bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$DIR/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
  echo "AISkills MCP venv is missing." >&2
  echo "Run this once:" >&2
  echo "  cd $DIR" >&2
  echo "  ./setup_mcp_env.sh" >&2
  exit 1
fi

exec "$PYTHON" "$DIR/aiskills_server.py"
