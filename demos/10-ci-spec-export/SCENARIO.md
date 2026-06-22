# 10 — Export the MCP tool spec as a CI artifact

**Where this comes from.** You maintain a fleet of agents that share a catalog of MCP
servers. Rather than boot every server to discover its tools, you generate each server's
`tools/list` spec in CI and publish it as an artifact (or diff it to catch breaking
changes to a tool's surface).

**Run it.**
```bash
# Emit the discovery spec — no server process required:
mcpify spec demos/10-ci-spec-export/manifest.json > release-tools.mcp.json

# Also produce the runnable server in the same pipeline:
mcpify manifest demos/10-ci-spec-export/manifest.json > release_server.py
```

**What to expect.** `mcpify spec` prints a JSON document:
`{"server": "release-tools", "protocol": "mcp", "tools": [ {name, description, command,
inputSchema}, ... ]}`. It is deterministic, so committing it lets `git diff` flag any
change to the exposed tool surface in review.

**How to act.** In CI, fail the job if `release-tools.mcp.json` changed without a
corresponding manifest change, so tool-surface drift can't sneak in unreviewed.
