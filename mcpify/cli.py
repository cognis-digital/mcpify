"""mcpify CLI — wrap any command as an MCP server."""
import argparse, json, sys
from mcpify.core import (
    CmdSpec, run, server_code, load_manifest, manifest_server_code,
    tools_spec, TOOL_NAME, TOOL_VERSION,
)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="mcpify", description="Turn any CLI tool into an MCP server.")
    ap.add_argument("--version", action="version", version=f"{TOOL_NAME} {TOOL_VERSION}")
    sub = ap.add_subparsers(dest="cmd")
    g = sub.add_parser("wrap", help="emit a server.py for a command"); g.add_argument("command"); g.add_argument("--name", default="run")
    s = sub.add_parser("serve", help="serve a command as MCP now"); s.add_argument("command"); s.add_argument("--name", default="run")
    r = sub.add_parser("run", help="test-run the command"); r.add_argument("command"); r.add_argument("args", nargs="?", default="")
    m = sub.add_parser("manifest", help="emit a multi-tool server.py from a JSON manifest"); m.add_argument("path")
    p = sub.add_parser("spec", help="emit the MCP tools/list spec (JSON) without booting a server")
    p.add_argument("source", help="a command string, or a path to a JSON manifest")
    p.add_argument("--name", default="run", help="tool name when SOURCE is a single command")
    a = ap.parse_args(argv)
    if a.cmd == "wrap":
        print(server_code(CmdSpec(a.name, a.command))); return 0
    if a.cmd == "serve":
        ns = {}; exec(server_code(CmdSpec(a.name, a.command)), ns); return 0
    if a.cmd == "run":
        print(run(CmdSpec("run", a.command), a.args)); return 0
    if a.cmd == "manifest":
        print(manifest_server_code(load_manifest(a.path))); return 0
    if a.cmd == "spec":
        try:
            man = load_manifest(a.source)
            print(json.dumps(tools_spec(man.tools, server=man.name), indent=2))
        except (ValueError, json.JSONDecodeError):
            spec = CmdSpec(a.name, a.source)
            print(json.dumps(tools_spec([spec], server=spec.name), indent=2))
        return 0
    ap.print_help(); return 0


if __name__ == "__main__":
    sys.exit(main())
