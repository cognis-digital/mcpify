"""mcpify CLI — wrap any command as an MCP server."""
import argparse, sys
from mcpify.core import CmdSpec, run, server_code, TOOL_NAME, TOOL_VERSION
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="mcpify", description="Turn any CLI tool into an MCP server.")
    ap.add_argument("--version", action="version", version=f"{TOOL_NAME} {TOOL_VERSION}")
    sub = ap.add_subparsers(dest="cmd")
    g = sub.add_parser("wrap", help="emit a server.py for a command"); g.add_argument("command"); g.add_argument("--name", default="run")
    s = sub.add_parser("serve", help="serve a command as MCP now"); s.add_argument("command"); s.add_argument("--name", default="run")
    r = sub.add_parser("run", help="test-run the command"); r.add_argument("command"); r.add_argument("args", nargs="?", default="")
    a = ap.parse_args(argv)
    if a.cmd == "wrap":
        print(server_code(CmdSpec(a.name, a.command))); return 0
    if a.cmd == "serve":
        ns = {}; exec(server_code(CmdSpec(a.name, a.command)), ns); return 0
    if a.cmd == "run":
        print(run(CmdSpec("run", a.command), a.args)); return 0
    ap.print_help(); return 0
if __name__ == "__main__":
    sys.exit(main())
