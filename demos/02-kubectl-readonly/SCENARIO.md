# 02 — Read-only kubectl triage server

**Where this comes from.** On-call: a pod is crash-looping and you want the agent to
investigate, but you do NOT want it able to `delete`, `scale`, or `apply` anything.
Every command in this manifest is read-only — there is no mutate verb anywhere.

**Run it.**
```bash
mcpify manifest demos/02-kubectl-readonly/manifest.json > k8s_server.py
python k8s_server.py             # agent connects over MCP

# Smoke-test a single tool live against your current kube-context:
mcpify run "kubectl get pods -o wide" ""
```

**What to expect.** Five tools: `get_pods`, `describe`, `logs`, `top_pods`,
`get_events`. The agent can chain them — e.g. `get_pods` → spot a `CrashLoopBackOff`
→ `logs my-pod` → `get_events`.

**How to act.** Run with a kube-context scoped to a read-only ServiceAccount /
RBAC role for defence in depth; the manifest is the second layer (no write verbs).
`describe`/`logs` take the resource as `args` from the agent.
