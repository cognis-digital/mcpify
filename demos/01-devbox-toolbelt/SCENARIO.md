# 01 — Developer toolbelt as one MCP server

**Where this comes from.** A typical polyglot repo where you want your coding agent
(Claude Desktop / Cursor) to be able to search code, list files, and run read-only
quality checks — without you copy-pasting terminal output.

**Input format.** `manifest.json` is mcpify's multi-tool manifest: a `name` plus a
`tools` array where each tool has a `command` (and optional `name`/`description`/`timeout`).

**Run it.**
```bash
# Generate one MCP server that exposes all five tools:
mcpify manifest demos/01-devbox-toolbelt/manifest.json > devbox_server.py
python devbox_server.py          # needs:  pip install "cognis-mcpify[mcp]"

# Or preview the tools an agent would see, without booting anything:
mcpify spec demos/01-devbox-toolbelt/manifest.json
```

**What to expect.** `manifest` prints a standalone FastMCP server with five
`@app.tool()` functions (`search`, `find`, `tree`, `fmt`, `typecheck`). `spec` prints
the MCP `tools/list` JSON your agent uses for discovery.

**How to act.** Point your MCP client at `devbox_server.py`. The agent can now call
`search("TODO src/")` etc. Every command is read-only — nothing here mutates the repo.
