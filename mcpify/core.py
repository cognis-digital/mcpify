"""mcpify core — turn ANY command-line tool into an MCP server."""
from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass

TOOL_NAME = "mcpify"
TOOL_VERSION = "0.1.0"


class McpifyError(Exception):
    """Base error for mcpify failures."""


@dataclass
class CmdSpec:
    name: str       # mcp tool name
    command: str    # base command, e.g. "rg" or "python script.py"

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise McpifyError("Tool name must not be empty.")
        if not self.command or not self.command.strip():
            raise McpifyError("Command must not be empty.")
        # MCP tool names must be valid Python identifiers
        if not self.name.replace("-", "_").isidentifier():
            raise McpifyError(
                f"Tool name {self.name!r} is not a valid identifier."
            )


def _split_cmd(cmd: str) -> list[str]:
    """Split a shell command string into a list of tokens.

    On Windows, shlex with posix=True corrupts backslash-separated paths
    (e.g. C:\\foo\\bar.exe becomes C:foobar.exe).  We therefore pass the
    command as a plain string on Windows so that CreateProcess handles it
    directly, returning a single-element list.
    """
    if os.name == "nt":
        # Let Windows CreateProcess tokenise natively; return as-is.
        return [cmd]
    try:
        return shlex.split(cmd)
    except ValueError as exc:
        raise McpifyError(f"Could not parse command {cmd!r}: {exc}") from exc


def run(spec: CmdSpec, args: str, timeout: int = 60) -> str:
    """Execute spec.command with args and return combined output.

    Raises McpifyError on subprocess failures so callers get a clean message.
    """
    if args is None:
        args = ""
    cmd = spec.command + (" " + args if args else "")

    parts = _split_cmd(cmd)
    # On Windows parts is a 1-element list containing the full string;
    # subprocess.run accepts a string on Windows and passes it to CreateProcess.
    cmd_arg: list[str] | str = parts[0] if (os.name == "nt" and len(parts) == 1) else parts

    if not cmd_arg:
        raise McpifyError("Command is empty after shell tokenisation.")

    try:
        r = subprocess.run(
            cmd_arg,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        exe = parts[0].split()[0] if parts else cmd
        raise McpifyError(
            f"Executable not found: {exe!r}. Is it installed and on PATH?"
        )
    except PermissionError:
        exe = parts[0].split()[0] if parts else cmd
        raise McpifyError(f"Permission denied when running {exe!r}.")
    except subprocess.TimeoutExpired:
        raise McpifyError(
            f"Command timed out after {timeout}s: {cmd!r}"
        )
    except OSError as exc:
        raise McpifyError(f"OS error running command: {exc}") from exc

    return (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")


def server_code(spec: CmdSpec) -> str:
    """Emit a standalone MCP server that exposes `spec.command` as a tool."""
    return f'''#!/usr/bin/env python3
"""Auto-generated MCP server wrapping: {spec.command}"""
import shlex
import subprocess

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
