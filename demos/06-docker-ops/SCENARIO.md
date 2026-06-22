# 06 — Docker observability server (no lifecycle control)

**Where this comes from.** A container is eating memory on a host and you want an agent
to diagnose it. It should be able to *observe* (ps/logs/inspect/stats) but never
`run`, `stop`, `rm`, or `exec` — so those verbs are simply not in the manifest.

**Run it.**
```bash
mcpify manifest demos/06-docker-ops/manifest.json > docker_server.py
python docker_server.py

# Live smoke-test (returns JSON lines of running containers):
mcpify run "docker ps --format json" ""
```

**What to expect.** Tools `ps`, `images`, `logs`, `inspect`, `stats`, all emitting
JSON so the agent can parse rather than scrape. A typical flow: `stats` → spot the hog →
`logs <id>` → `inspect <id>`.

**How to act.** Because the manifest excludes lifecycle verbs, the agent can investigate
freely; a human still performs any remediation (restart/redeploy).
