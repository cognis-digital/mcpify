# 08 — Read-only Postgres query server

**Where this comes from.** An analytics agent answers "how many orders shipped
yesterday?" against a production replica. The single hard rule: it must not be able to
mutate data. mcpify is the *second* line of defence; the **first** is connecting `psql`
with a role that only has `SELECT` (see below).

**Run it.**
```bash
# Connection string comes from the environment, never hardcoded in the manifest:
export PGHOST=replica.internal PGDATABASE=shop PGUSER=analyst_ro
mcpify manifest demos/08-db-query-readonly/manifest.json > pg_server.py
python pg_server.py

# Preview the tool schema offline:
mcpify spec demos/08-db-query-readonly/manifest.json
```

**What to expect.** Tools `query`, `tables`, `describe`, `explain`. The agent passes
the SQL as `args`.

**How to act — defence in depth.**
1. Grant the DB role only `SELECT` (`GRANT SELECT ... TO analyst_ro;`). This is the real
   guarantee, not the tool list.
2. Optionally set the role's default transaction to read-only:
   `ALTER ROLE analyst_ro SET default_transaction_read_only = on;`
3. Run against a *replica*, never the primary.

The manifest carries no credentials — `psql` reads `PG*` env vars / `~/.pgpass`.
