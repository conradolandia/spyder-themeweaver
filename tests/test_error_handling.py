"""Tests for CLI error handling helpers."""

import pytest

from themeweaver.cli import error_handling as eh


def test_handle_missing_data_error_with_details_no_exit() -> None:
    with pytest.raises(SystemExit):
        eh.handle_missing_data_error("palette", "theme=dracula")


def test_handle_unknown_option_error_no_exit() -> None:
    eh.handle_unknown_option_error("foo", ["a", "b"], exit_on_error=False)


def test_handle_invalid_count_error_triggers_exit() -> None:
    with pytest.raises(SystemExit):
        eh.handle_invalid_count_error(3, 2, "colors")


def test_operation_context_reraises_when_exit_disabled() -> None:
    with pytest.raises(ValueError, match="boom"):
        with eh.operation_context("Op", exit_on_error=False):
            raise ValueError("boom")


def test_safe_operation_success() -> None:
    def add(a: int, b: int) -> int:
        return a + b

    assert eh.safe_operation("add", add, 2, 3) == 5


def test_safe_operation_failure_reraises() -> None:
    def fail() -> None:
        raise RuntimeError("bad")

    with pytest.raises(RuntimeError, match="bad"):
        eh.safe_operation("fail", fail)


def test_validate_required_args_missing_no_exit() -> None:
    eh.validate_required_args(
        {"theme": "dracula", "variants": ""},
        ["theme", "variants"],
        exit_on_error=False,
    )
