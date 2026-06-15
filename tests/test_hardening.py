"""Tests for input validation, error handling, and edge cases added during hardening."""
from __future__ import annotations

import subprocess
import sys
from unittest.mock import patch

import pytest

from mcpify.core import CmdSpec, McpifyError, run, server_code
from mcpify.cli import main


# ---------------------------------------------------------------------------
# CmdSpec validation
# ---------------------------------------------------------------------------

class TestCmdSpecValidation:
    def test_empty_name_raises(self):
        with pytest.raises(McpifyError, match="name"):
            CmdSpec("", "echo hi")

    def test_whitespace_name_raises(self):
        with pytest.raises(McpifyError, match="name"):
            CmdSpec("   ", "echo hi")

    def test_empty_command_raises(self):
        with pytest.raises(McpifyError, match="[Cc]ommand"):
            CmdSpec("mytool", "")

    def test_whitespace_command_raises(self):
        with pytest.raises(McpifyError, match="[Cc]ommand"):
            CmdSpec("mytool", "   ")

    def test_invalid_identifier_name_raises(self):
        with pytest.raises(McpifyError, match="identifier"):
            CmdSpec("123bad", "echo")

    def test_valid_spec_succeeds(self):
        spec = CmdSpec("my_tool", "echo hello")
        assert spec.name == "my_tool"
        assert spec.command == "echo hello"


# ---------------------------------------------------------------------------
# run() error handling
# ---------------------------------------------------------------------------

class TestRunErrors:
    def test_none_args_treated_as_empty(self):
        """run() must not crash when args=None is passed."""
        out = run(CmdSpec("echo", "python -c \"print('ok')\""), None)
        assert "ok" in out

    def test_nonexistent_executable_raises(self):
        with pytest.raises(McpifyError, match="not found|Executable"):
            run(CmdSpec("nope", "__no_such_binary_mcpify__"), "")

    def test_timeout_raises(self):
        """subprocess.TimeoutExpired must be converted to McpifyError."""
        with patch(
            "mcpify.core.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="slow", timeout=1),
        ):
            with pytest.raises(McpifyError, match="[Tt]imed out|timeout"):
                run(CmdSpec("slow", "slow_cmd"), "", timeout=1)


# ---------------------------------------------------------------------------
# CLI exit codes
# ---------------------------------------------------------------------------

class TestCliExitCodes:
    def test_no_subcommand_returns_zero(self):
        """Printing help on missing subcommand must exit 0, not crash."""
        assert main([]) == 0

    def test_wrap_empty_name_returns_nonzero(self):
        code = main(["wrap", "--name", "", "echo"])
        assert code != 0

    def test_run_bad_binary_returns_nonzero(self):
        code = main(["run", "__no_such_binary_mcpify__"])
        assert code != 0

    def test_wrap_valid_command_returns_zero(self):
        assert main(["wrap", "echo"]) == 0

    def test_run_valid_command_returns_zero(self):
        assert main(["run", f"{sys.executable} -c \"print(42)\""]) == 0


# ---------------------------------------------------------------------------
# server_code output sanity
# ---------------------------------------------------------------------------

class TestServerCode:
    def test_generated_code_compiles(self):
        """Generated server code must at least compile without error."""
        import py_compile
        import tempfile
        import os

        code = server_code(CmdSpec("mytool", "echo hello"))
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as fh:
            fh.write(code)
            tmp_path = fh.name
        try:
            py_compile.compile(tmp_path, doraise=True)
        finally:
            os.unlink(tmp_path)
            pyc = tmp_path + "c"
            if os.path.exists(pyc):
                os.unlink(pyc)
