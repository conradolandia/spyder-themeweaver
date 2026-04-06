"""In-process ThemeWeaver CLI invocation for tests (avoids subprocess startup)."""

from __future__ import annotations

import contextlib
import io
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from themeweaver.cli import main

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class CLIResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def output(self) -> str:
        return self.stdout + self.stderr


def invoke_cli(*argv: str, cwd: Path | None = None) -> CLIResult:
    """Run ``themeweaver`` CLI with the given arguments (no script name)."""
    work = cwd if cwd is not None else REPO_ROOT
    root = logging.getLogger()
    saved_handlers = list(root.handlers)
    for h in list(root.handlers):
        root.removeHandler(h)

    old_argv = sys.argv
    old_cwd = Path.cwd()
    out = io.StringIO()
    err = io.StringIO()
    code = 0
    try:
        os.chdir(work)
        sys.argv = ["themeweaver", *argv]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                main()
            except SystemExit as e:
                if e.code is None:
                    code = 0
                elif isinstance(e.code, int):
                    code = e.code
                else:
                    code = 1
    finally:
        sys.argv = old_argv
        os.chdir(old_cwd)
        for h in list(root.handlers):
            root.removeHandler(h)
        for h in saved_handlers:
            root.addHandler(h)

    return CLIResult(code, out.getvalue(), err.getvalue())
