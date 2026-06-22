# 04 — Git inspection server (read-only history)

**Where this comes from.** You want an agent to reason about a repo's history —
"who last touched this function, what changed in the last release" — without giving it
the ability to commit, push, reset, or rebase.

**Run it.**
```bash
mcpify manifest demos/04-git-inspect/manifest.json > git_server.py
python git_server.py

# Live smoke-test against this checkout:
mcpify run "git log --oneline -n 30" ""
```

**What to expect.** Tools `status`, `log`, `diff`, `blame`, `show`. All are
inspection-only git plumbing/porcelain — no write verbs (`commit`/`push`/`reset` are
absent by design).

**How to act.** The agent supplies `args` for `blame` (a path) and `show` (a sha). Run
inside the target repo; the server inherits its cwd.
