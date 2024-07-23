#!/usr/bin/env python3
from pathlib import Path
from subprocess import run


def test_cli_tool_example():

    paths = list(Path("example").resolve().glob("*.docx"))
    assert len(paths) > 0, "No documents/*.docx available for testing"

    for path in paths:
        result = run(
            ["jugmt", f"{path}", "--output", str(path.with_name("output"))],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"CLI tool failed with error: {result.stderr}"


def test_cli_tool(tmp_path):

    paths = list(Path("example").resolve().glob("*.docx"))
    assert len(paths) > 0, "No documents/*.docx available for testing"

    for path in paths:
        result = run(
            ["jugmt", f"{path}", "--output", str(tmp_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"CLI tool failed with error: {result.stderr}"


def test_cli_tool_dump_schema(tmp_path):

    paths = list(Path("example").resolve().glob("*.docx"))
    assert len(paths) > 0, "No documents/*.docx available for testing"

    for path in paths:

        result = run(
            ["jugmt", "--dump-schema", "--output", str(tmp_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"CLI tool failed with error: {result.stderr}"


def test_cli_tool_skip_validate(tmp_path):
    paths = list(Path("example").resolve().glob("*.docx"))
    assert len(paths) > 0, "No documents/*.docx available for testing"

    for path in paths:

        result = run(
            ["jugmt", f"{path}", "--skip-validate", "--output", str(tmp_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"CLI tool failed with error: {result.stderr}"


def test_cli_tool_missing_args(tmp_path):

    result = run(["jugmt"], capture_output=True, text=True)

    assert result.returncode != 0, f"Expected failure, but got: {result.stderr}"
