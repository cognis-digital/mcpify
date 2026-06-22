# 07 — Terraform review server (plan, never apply)

**Where this comes from.** A platform agent reviews infrastructure PRs: it should be
able to run `plan`, `validate`, and `fmt -check` so it can comment on drift and style,
but it must **never** be able to `apply`, `destroy`, or `import`. The manifest enforces
that — only read/dry-run subcommands are exposed.

**Run it.**
```bash
mcpify manifest demos/07-terraform-plan/manifest.json > tf_server.py
python tf_server.py              # run from a Terraform working directory

# Preview the exposed tools without a TF project handy:
mcpify spec demos/07-terraform-plan/manifest.json
```

**What to expect.** Tools `plan`, `validate`, `fmt_check`, `show`, `state_list`.
`plan` is dry-run by construction; nothing here changes real infrastructure. `plan` gets
a long timeout (300s) because provider refresh can be slow.

**How to act.** Wire it into PR review. The agent reports the plan diff; a human runs the
actual `terraform apply` through your normal CI gate.
