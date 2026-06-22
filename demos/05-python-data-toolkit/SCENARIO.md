# 05 — JSON/CSV data toolkit for an analyst agent

**Where this comes from.** An analytics agent needs to poke at local JSON/CSV dumps —
a service's daily metrics, an export from a dashboard — and answer questions about them.
`sample.json` is a small, synthetic checkout-API metrics rollup included so the demo runs
end-to-end with no external data.

**Run it.**
```bash
mcpify manifest demos/05-python-data-toolkit/manifest.json > datakit_server.py
python datakit_server.py

# Verify two tools end-to-end against the bundled sample:
mcpify run "python -m json.tool" "demos/05-python-data-toolkit/sample.json"
mcpify run 'jq' ".by_route[] | {route, p99_ms}  demos/05-python-data-toolkit/sample.json"
```

**What to expect.** Tools `jq`, `csvstat`, `csvgrep`, `head`, `validate`. `validate`
pretty-prints `sample.json`; `jq` projects each route's p99 (the `/pay` route at 980ms is
the obvious latency outlier to flag).

**How to act.** The agent passes the filter + file as `args`. All tools are read-only and
operate on local files; nothing is written or sent off-box.
