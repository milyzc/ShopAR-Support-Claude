#!/bin/bash
# PostToolUse: formats the Python file Claude just edited or wrote.
# It runs after the tool, so it cannot block anything; it only reacts.
file=$(jq -r '.tool_input.file_path // empty')
[[ "$file" == *.py ]] || exit 0
cd "$CLAUDE_PROJECT_DIR" && uv run --quiet ruff format --quiet "$file"
