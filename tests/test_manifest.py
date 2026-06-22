"""Tests for the manifest / multi-tool / spec features."""
from __future__ import annotations

import ast
import json

import pytest

from mcpify import cli
from mcpify.core import (
    CmdSpec,
    load_manifest,
    manifest_server_code,
    server_code,
    server_code_multi,
    tools_spec,
    TOOL_VERSION,
)


def test_version_matches_pyproject():
    assert TOOL_VERSION == "0.1.1"


def test_name_normalization():
    # leading digit and illegal chars become a valid identifier
    assert CmdSpec("7-build", "make").name == "t_7_build"
    assert CmdSpec("my tool!", "rg").name == "my_tool_"


def test_default_description():
    assert CmdSpec("search", "rg").description == "Run `rg <args>` and return combined output."


def test_load_manifest_object():
    man = load_manifest(json.dumps({
        "name": "devbox",
        "tools": [
            {"name": "search", "command": "rg", "description": "code search", "timeout": 30},
            {"name": "build", "command": "make"},
        ],
    }))
    assert man.name == "devbox"
    assert [t.name for t in man.tools] == ["search", "build"]
    assert man.tools[0].timeout == 30
    assert man.tools[0].description == "code search"


def test_load_manifest_bare_list():
    man = load_manifest('[{"command": "ls"}]')
    assert man.name == "mcpify"
    assert man.tools[0].name == "tool_0"


def test_load_manifest_rejects_missing_command():
    with pytest.raises(ValueError):
        load_manifest('{"tools": [{"name": "x"}]}')


def test_load_manifest_rejects_empty():
    with pytest.raises(ValueError):
        load_manifest('{"tools": []}')


def test_load_manifest_rejects_duplicate_names():
    with pytest.raises(ValueError):
        load_manifest('{"tools": [{"name": "a b", "command": "ls"}, {"name": "a-b", "command": "pwd"}]}')


def test_manifest_server_code_is_valid_python():
    man = load_manifest('{"name": "x", "tools": [{"name": "a", "command": "ls"}, {"name": "b", "command": "pwd"}]}')
    code = manifest_server_code(man)
    ast.parse(code)
    assert "def a(" in code and "def b(" in code and 'FastMCP(\'x\')' in code


def test_server_code_survives_quotes_in_command():
    # the original f-string header crashed on a quote; this must not.
    ast.parse(server_code(CmdSpec("x", 'echo "hi"')))
    ast.parse(server_code_multi([CmdSpec("a", 'grep --include=*.py foo')]))


def test_server_code_survives_quotes_in_description():
    spec = CmdSpec("d", "psql -c", description='describe, e.g. args="\\d+ orders"')
    ast.parse(server_code(spec))


def test_tools_spec_shape():
    spec = tools_spec([CmdSpec("search", "rg", description="code search")], server="devbox")
    assert spec["server"] == "devbox" and spec["protocol"] == "mcp"
    t = spec["tools"][0]
    assert t["name"] == "search" and t["command"] == "rg"
    assert t["inputSchema"]["properties"]["args"]["type"] == "string"


def test_cli_manifest(tmp_path, capsys):
    p = tmp_path / "m.json"
    p.write_text('{"name": "n", "tools": [{"name": "a", "command": "ls"}]}', encoding="utf-8")
    rc = cli.main(["manifest", str(p)])
    out = capsys.readouterr().out
    assert rc == 0 and "FastMCP('n')" in out and "def a(" in out


def test_cli_spec_from_command(capsys):
    rc = cli.main(["spec", "rg", "--name", "search"])
    out = capsys.readouterr().out
    assert rc == 0
    data = json.loads(out)
    assert data["tools"][0]["name"] == "search"


def test_cli_spec_from_manifest(tmp_path, capsys):
    p = tmp_path / "m.json"
    p.write_text('{"name": "devbox", "tools": [{"name": "a", "command": "ls"}, {"name": "b", "command": "pwd"}]}', encoding="utf-8")
    rc = cli.main(["spec", str(p)])
    out = capsys.readouterr().out
    assert rc == 0
    data = json.loads(out)
    assert data["server"] == "devbox" and len(data["tools"]) == 2
