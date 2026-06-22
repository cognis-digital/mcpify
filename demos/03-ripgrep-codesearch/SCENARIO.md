# 03 — Code-search server (incl. a credential heuristic)

**Where this comes from.** You want an agent to navigate a large codebase the way you
would with ripgrep, plus a quick defensive sweep for accidentally-committed secrets
before a release.

**Run it.**
```bash
mcpify manifest demos/03-ripgrep-codesearch/manifest.json > codesearch_server.py
python codesearch_server.py

# Try the secret heuristic locally (expect: no real secrets in this repo):
mcpify run 'rg --line-number -e (?i)(api[_-]?key|secret|password|token)\s*[:=]' "."
```

**What to expect.** Tools `grep`, `files`, `count`, `secrets_scan`. The
`secrets_scan` pattern is a *heuristic* — it flags candidate lines, it does not prove a
leak. Treat every hit as "review by a human", never as a confirmed secret.

**How to act.** Pipe confirmed findings into the wider Cognis suite if you triage at
scale; otherwise rotate any real credential a human verifies and purge it from history.
This demo ships no real secrets — only the detector.
