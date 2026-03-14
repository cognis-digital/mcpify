"""mcpify core — turn ANY command-line tool into an MCP server."""
from __future__ import annotations
import shlex, subprocess
from dataclasses import dataclass
TOOL_NAME = "mcpify"; TOOL_VERSION = "0.1.0"

@dataclass
class CmdSpec:
    name: str          # mcp tool name
    command: str       # base command, e.g. "rg" or "python script.py"

def run(spec: CmdSpec, args: str, timeout: int = 60) -> str:
    cmd = spec.command + (" " + args if args else "")
    r = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=timeout)
    return (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")

def server_code(spec: CmdSpec) -> str:
    """Emit a standalone MCP server that exposes `spec.command` as a tool."""
    return f'''#!/usr/bin/env python3
"""Auto-generated MCP server wrapping: {spec.command}"""
import shlex, subprocess
from mcp.server.fastmcp import FastMCP
app = FastMCP("{spec.name}")
@app.tool()
def {spec.name}(args: str = "") -> str:
    """Run `{spec.command} <args>` and return combined output."""
    cmd = "{spec.command}" + (" " + args if args else "")
    r = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=120)
    return (r.stdout or "") + (("\\n[stderr]\\n" + r.stderr) if r.stderr else "")
if __name__ == "__main__":
    app.run()
'''
