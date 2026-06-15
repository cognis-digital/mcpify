"""mcpify CLI — wrap any command as an MCP server."""
import argparse
import sys

from mcpify.core import CmdSpec, McpifyError, run, server_code, TOOL_NAME, TOOL_VERSION


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="mcpify",
        description="Turn any CLI tool into an MCP server.",
    )
    ap.add_argument(
        "--version",
        action="version",
        version=f"{TOOL_NAME} {TOOL_VERSION}",
    )
    sub = ap.add_subparsers(dest="cmd")

    g = sub.add_parser("wrap", help="emit a server.py for a command")
    g.add_argument("command")
    g.add_argument("--name", default="run")

    s = sub.add_parser("serve", help="serve a command as MCP now")
    s.add_argument("command")
    s.add_argument("--name", default="run")

    r = sub.add_parser("run", help="test-run the command")
    r.add_argument("command")
    r.add_argument("args", nargs="?", default="")

    a = ap.parse_args(argv)

    if a.cmd == "wrap":
        try:
            spec = CmdSpec(a.name, a.command)
        except McpifyError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(server_code(spec))
        return 0

    if a.cmd == "serve":
        try:
            spec = CmdSpec(a.name, a.command)
            code = server_code(spec)
        except McpifyError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        try:
            ns: dict = {}
            exec(code, ns)  # noqa: S102
        except Exception as exc:
            print(f"error starting server: {exc}", file=sys.stderr)
            return 1
        return 0

    if a.cmd == "run":
        try:
            spec = CmdSpec("run", a.command)
            output = run(spec, a.args)
        except McpifyError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(output)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
