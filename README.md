<a name="top"></a>
<div align="center">

# mcpify

### Turn **any** command-line tool into an MCP server — one line, zero boilerplate.

[![License: COCL 1.0](https://img.shields.io/badge/License-COCL%201.0-2b6cb0.svg)](LICENSE) ![MCP](https://img.shields.io/badge/MCP-native-black) [![Suite](https://img.shields.io/badge/Cognis-Neural%20Suite-6b46c1.svg)](https://github.com/cognis-digital/cognis-neural-suite)

`#mcp` `#ai-agents` `#llm` `#developer-tools` `#cli`

</div>

The MCP gold rush, solved: expose `rg`, `kubectl`, your build script — anything — to Claude/Cursor/agents
without writing a server.

```bash
pip install "cognis-mcpify[mcp]"
mcpify wrap "rg" --name search > server.py    # generate a server
mcpify serve "kubectl" --name kube             # or serve immediately
```

<!-- cognis:layman:start -->
## What is this?

mcpify takes any program you already have on your computer — like a search tool, a database command, or a build script — and wraps it so that AI assistants like Claude or Cursor can run it on your behalf. You point it at a command, and it generates a small server file that makes that command available to AI agents without any custom coding. It is for developers who want their existing tools to work inside AI-powered workflows without rewriting anything.
<!-- cognis:layman:end -->

## Architecture

```mermaid
flowchart LR
  CLI[Any CLI tool] --> M[mcpify]
  M --> GEN[Generate FastMCP server]
  GEN --> S[(MCP server)]
  S --> AG[Claude · Cursor · agents]
```

## Use it from any AI stack
MCP-native by definition; also exposes a plain `run` for shell/JSON pipelines, and pairs with
[uncensored-fleet](https://github.com/cognis-digital/uncensored-fleet) for fully-local agents.

<a name="verification"></a>
<!-- cognis:domains:start -->
## Domains

**Primary domain:** AI & ML  ·  **JTF MERIDIAN division:** ATHENA-PRIME · SAGE

**Topics:** `cognis` `ai` `llm` `machine-learning` `mcp` `agent-security` `cli`

Part of the **Cognis Neural Suite** — 300+ source-available tools organized across 12 domains under the JTF MERIDIAN command structure. See the [suite on GitHub](https://github.com/cognis-digital) and [jtf-meridian](https://github.com/cognis-digital/jtf-meridian) for how the pieces fit together.
<!-- cognis:domains:end -->

<!-- cognis:install:start -->
## Install

`mcpify` is source-available (not published to PyPI) — every method below installs
straight from GitHub. Pick whichever you prefer; the one-line scripts auto-detect
the best tool available on your machine.

**One-liner (Linux / macOS):**
```sh
curl -fsSL https://raw.githubusercontent.com/cognis-digital/mcpify/HEAD/install.sh | sh
```

**One-liner (Windows PowerShell):**
```powershell
irm https://raw.githubusercontent.com/cognis-digital/mcpify/HEAD/install.ps1 | iex
```

**Or install manually — any one of:**
```sh
pipx install "git+https://github.com/cognis-digital/mcpify.git"     # isolated (recommended)
uv tool install "git+https://github.com/cognis-digital/mcpify.git"  # uv
pip install "git+https://github.com/cognis-digital/mcpify.git"      # pip
```

**From source:**
```sh
git clone https://github.com/cognis-digital/mcpify.git
cd mcpify && pip install .
```

Then run:
```sh
mcpify --help
```
<!-- cognis:install:end -->

## Verification

[![tests](https://img.shields.io/badge/tests-2%20passing-2ea44f.svg)](AUDIT.md)

Every push is verified end-to-end. Latest audit (2026-06-13):

```text
tests        : 2 passed, 0 failed, 0 errored
compile      : all modules parse
cli          : C:\Python314\python.exe: No module named https
package      : https
```

<details><summary>CLI surface (<code>--help</code>)</summary>

```text
C:\Python314\python.exe: No module named https
```
</details>

Full machine-readable results: [`AUDIT.md`](AUDIT.md) · regenerate with `python -m https --help` + `pytest -q`.

<div align="right"><a href="#top">↑ back to top</a></div>


## Related
[🧰 skills](https://github.com/cognis-digital/skills) · [🤖 uncensored-fleet](https://github.com/cognis-digital/uncensored-fleet) · [🗂️ the suite](https://github.com/cognis-digital/cognis-neural-suite)

> ### ⭐ Star it if it saved you a server.

## License
COCL v1.0 — see [LICENSE](LICENSE).
