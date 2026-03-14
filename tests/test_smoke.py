from mcpify.core import CmdSpec, server_code, run
def test_codegen():
    c = server_code(CmdSpec("search", "rg"))
    assert "FastMCP" in c and "def search" in c
def test_run():
    out = run(CmdSpec("echo", "python -c \"print(123)\""), "")
    assert "123" in out
