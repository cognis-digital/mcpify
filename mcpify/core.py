"""mcpify core — turn ANY command-line tool into an MCP server."""
from __future__ import annotations
import json
import re
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
TOOL_NAME = "mcpify"; TOOL_VERSION = "0.1.1"

_NAME_RE = re.compile(r"[^0-9a-zA-Z_]")


def _safe_name(name: str) -> str:
    """Coerce an arbitrary tool name into a valid python identifier / MCP tool name."""
    s = _NAME_RE.sub("_", name.strip()) or "run"
    if s[0].isdigit():
        s = "t_" + s
    return s


@dataclass
class CmdSpec:
    name: str          # mcp tool name
    command: str       # base command, e.g. "rg" or "python script.py"
    description: str = ""   # human/LLM-facing tool description
    timeout: int = 120      # per-call subprocess timeout (seconds)

    def __post_init__(self) -> None:
        self.name = _safe_name(self.name)
        if not self.description:
            self.description = f"Run `{self.command} <args>` and return combined output."


def run(spec: CmdSpec, args: str, timeout: int | None = None) -> str:
    cmd = spec.command + (" " + args if args else "")
    r = subprocess.run(shlex.split(cmd), capture_output=True, text=True,
                       timeout=timeout if timeout is not None else 60)
    return (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")


def _safe_doc(text: str) -> str:
    """Escape arbitrary text so it is safe inside a triple-quoted docstring."""
    return (text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")).strip()


def _tool_fn(spec: CmdSpec) -> str:
    """Render a single @app.tool() function body for `spec`."""
    return f'''@app.tool()
def {spec.name}(args: str = "") -> str:
    """{_safe_doc(spec.description)}"""
    cmd = {spec.command!r} + (" " + args if args else "")
    r = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout={spec.timeout})
    return (r.stdout or "") + (("\\n[stderr]\\n" + r.stderr) if r.stderr else "")
'''


def server_code(spec: CmdSpec) -> str:
    """Emit a standalone MCP server that exposes `spec.command` as a tool."""
    return server_code_multi([spec], app_name=spec.name)


def server_code_multi(specs: list[CmdSpec], app_name: str = "mcpify") -> str:
    """Emit a standalone MCP server exposing many commands as distinct tools."""
    if not specs:
        raise ValueError("server_code_multi: at least one CmdSpec is required")
    # Keep the header docstring safe regardless of quotes/newlines in commands.
    cmds = ", ".join(s.command for s in specs).replace("\\", "\\\\").replace('"', '\\"')
    cmds = cmds.replace("\n", " ")
    body = "\n".join(_tool_fn(s) for s in specs)
    return f'''#!/usr/bin/env python3
"""Auto-generated MCP server wrapping: {cmds}"""
import shlex, subprocess
from mcp.server.fastmcp import FastMCP
app = FastMCP({app_name!r})
{body}
if __name__ == "__main__":
    app.run()
'''


# ---------------------------------------------------------------------------
# Manifest: declare many tools in one JSON file and wrap them together.
# ---------------------------------------------------------------------------

@dataclass
class Manifest:
    name: str
    tools: list[CmdSpec] = field(default_factory=list)


def load_manifest(path_or_text: str | Path) -> Manifest:
    """Load a manifest from a JSON file path or a JSON string.

    Schema (all keys optional except a tool's `command`):
        {
          "name": "devbox",
          "tools": [
            {"name": "search", "command": "rg", "description": "...", "timeout": 60},
            {"name": "build",  "command": "make"}
          ]
        }
    A bare list `[{...}, ...]` is also accepted (name defaults to "mcpify").
    """
    text = path_or_text
    p = Path(str(path_or_text))
    try:
        if p.exists():
            text = p.read_text(encoding="utf-8")
    except OSError:
        pass
    data = json.loads(text)
    if isinstance(data, list):
        data = {"name": "mcpify", "tools": data}
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object or list of tools")
    raw_tools = data.get("tools") or []
    if not raw_tools:
        raise ValueError("manifest has no tools")
    specs: list[CmdSpec] = []
    seen: set[str] = set()
    for i, t in enumerate(raw_tools):
        if not isinstance(t, dict) or not t.get("command"):
            raise ValueError(f"tool #{i} is missing a 'command'")
        name = t.get("name") or f"tool_{i}"
        spec = CmdSpec(
            name=name,
            command=t["command"],
            description=t.get("description", ""),
            timeout=int(t.get("timeout", 120)),
        )
        if spec.name in seen:
            raise ValueError(f"duplicate tool name after normalization: {spec.name!r}")
        seen.add(spec.name)
        specs.append(spec)
    return Manifest(name=str(data.get("name") or "mcpify"), tools=specs)


def manifest_server_code(manifest: Manifest) -> str:
    """Emit one MCP server that exposes every tool in `manifest`."""
    return server_code_multi(manifest.tools, app_name=manifest.name)


def tools_spec(specs: list[CmdSpec], server: str = "mcpify") -> dict:
    """Emit an MCP `tools/list`-shaped spec for the given commands.

    Lets an agent discover the exposed tools (and their JSON input schema)
    *without* booting the server — handy for CI, catalogs, and interop.
    """
    return {
        "server": server,
        "protocol": "mcp",
        "tools": [
            {
                "name": s.name,
                "description": s.description,
                "command": s.command,
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "args": {
                            "type": "string",
                            "description": f"arguments appended to `{s.command}`",
                            "default": "",
                        }
                    },
                    "required": [],
                },
            }
            for s in specs
        ],
    }
