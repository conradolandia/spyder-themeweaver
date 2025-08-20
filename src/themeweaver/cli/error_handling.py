"""
Centralized error handling for CLI commands.

This module provides common error handling patterns used across CLI commands
to reduce code duplication and ensure consistent error reporting.
"""

import logging
import sys
from contextlib import contextmanager
from typing import Any, Callable

_logger = logging.getLogger(__name__)


def handle_operation_error(
    operation_name: str, error: Exception, exit_on_error: bool = True
) -> None:
    """
    Handle operation errors with consistent logging and optional exit.

    Args:
        operation_name: Name of the operation that failed
        error: The exception that occurred
        exit_on_error: Whether to exit with code 1 on error
    """
    _logger.error("❌ %s failed: %s", operation_name, error)
    if exit_on_error:
        sys.exit(1)


def handle_validation_error(message: str, exit_on_error: bool = True) -> None:
    """
    Handle validation errors with consistent logging and optional exit.

    Args:
        message: Error message to display
        exit_on_error: Whether to exit with code 1 on error
    """
    _logger.error("❌ %s", message)
    if exit_on_error:
        sys.exit(1)


def handle_missing_data_error(
    data_type: str, details: str = "", exit_on_error: bool = True
) -> None:
    """
    Handle missing data errors with consistent logging and optional exit.

    Args:
        data_type: Type of data that is missing
        details: Additional details about the missing data
        exit_on_error: Whether to exit with code 1 on error
    """
    message = f"No {data_type} data loaded"
    if details:
        message += f": {details}"
    handle_validation_error(message, exit_on_error)


def handle_unknown_option_error(
    option_name: str, available_options: list, exit_on_error: bool = True
) -> None:
    """
    Handle unknown option errors with consistent logging and optional exit.

    Args:
        option_name: The unknown option that was provided
        available_options: List of valid options
        exit_on_error: Whether to exit with code 1 on error
    """
    message = f"Unknown {option_name}: {option_name}. Available: {', '.join(available_options)}"
    handle_validation_error(message, exit_on_error)


def handle_invalid_count_error(
    expected: int, actual: int, item_type: str, exit_on_error: bool = True
) -> None:
    """
    Handle invalid count errors with consistent logging and optional exit.

    Args:
        expected: Expected number of items
        actual: Actual number of items provided
        item_type: Type of items being counted
        exit_on_error: Whether to exit with code 1 on error
    """
    message = f"Expected {expected} {item_type}, but got {actual}"
    handle_validation_error(message, exit_on_error)


@contextmanager
def operation_context(operation_name: str, exit_on_error: bool = True):
    """
    Context manager for wrapping operations with consistent error handling.

    Args:
        operation_name: Name of the operation being performed
        exit_on_error: Whether to exit with code 1 on error

    Yields:
        None

    Raises:
        Exception: Re-raises the original exception if exit_on_error is False
    """
    try:
        yield
    except Exception as e:
        handle_operation_error(operation_name, e, exit_on_error)
        if not exit_on_error:
            raise


def safe_operation(operation_name: str, operation: Callable, *args, **kwargs) -> Any:
    """
    Safely execute an operation with consistent error handling.

    Args:
        operation_name: Name of the operation being performed
        operation: Function to execute
        *args: Arguments to pass to the operation
        **kwargs: Keyword arguments to pass to the operation

    Returns:
        Result of the operation

    Raises:
        Exception: Re-raises the original exception
    """
    try:
        return operation(*args, **kwargs)
    except Exception as e:
        handle_operation_error(operation_name, e, exit_on_error=False)
        raise


def validate_required_args(
    args: dict, required_args: list, exit_on_error: bool = True
) -> None:
    """
    Validate that required arguments are provided.

    Args:
        args: Dictionary of arguments to validate
        required_args: List of required argument names
        exit_on_error: Whether to exit with code 1 on error
    """
    missing = [arg for arg in required_args if not args.get(arg)]
    if missing:
        message = f"Missing required arguments: {', '.join(missing)}"
        handle_validation_error(message, exit_on_error)


def validate_condition(
    condition: bool, message: str, exit_on_error: bool = True
) -> None:
    """
    Validate a condition and handle failure consistently.

    Args:
        condition: Condition to validate
        message: Error message if condition is False
        exit_on_error: Whether to exit with code 1 on error
    """
    if not condition:
        handle_validation_error(message, exit_on_error)
