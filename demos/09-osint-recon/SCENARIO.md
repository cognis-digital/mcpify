# 09 — Passive recon server (authorized footprinting only)

**Where this comes from.** During an **authorized** security assessment of assets you own
or are explicitly engaged to test, you want an agent to gather passive footprint data —
WHOIS, DNS, TLS cert metadata, HTTP headers — to feed a report.

> **Authorized use only.** Every tool here is passive (lookups against public records and
> a single TLS handshake / HEAD request). There is no scanning, brute-forcing, or
> exploitation. Only run it against targets you are permitted to assess.

**Run it.**
```bash
mcpify manifest demos/09-osint-recon/manifest.json > recon_server.py
python recon_server.py

# Live smoke-test against the IANA reserved example domain:
mcpify run "dig +noall +answer" "example.com A"
```

**What to expect.** Tools `whois`, `dns`, `rdns`, `cert`, `headers`. `example.com`
is the IANA-reserved documentation domain — safe to query in any environment.

**How to act.** Forward structured findings to the Cognis suite (`cognis-connect` →
STIX/MISP/Splunk) for correlation. Keep scope to the engagement's authorized asset list.
