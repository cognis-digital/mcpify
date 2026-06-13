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

## Usage — step by step

1. Install the CLI (console-script: `mcpify`):
   ```bash
   pipx install "git+https://github.com/cognis-digital/mcpify.git"
   mcpify --version
   ```
2. Test-run the command you want to expose, to confirm it behaves:
   ```bash
   mcpify run "ripgrep" "TODO ./src"
   ```
3. Serve that command as an MCP server right now (tool name defaults to `run`):
   ```bash
   mcpify serve "ripgrep" --name search
   ```
4. Or emit a standalone `server.py` you can commit and run later:
   ```bash
   mcpify wrap "ripgrep" --name search > server.py
   python server.py
   ```
5. In CI, generate the server file as a build artifact for your agent stack:
   ```bash
   mcpify wrap "mytool --flag" --name mytool > dist/server.py
   ```

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

## Related
[🧰 skills](https://github.com/cognis-digital/skills) · [🤖 uncensored-fleet](https://github.com/cognis-digital/uncensored-fleet) · [🗂️ the suite](https://github.com/cognis-digital/cognis-neural-suite)

> ### ⭐ Star it if it saved you a server.

## License
COCL v1.0 — see [LICENSE](LICENSE).
