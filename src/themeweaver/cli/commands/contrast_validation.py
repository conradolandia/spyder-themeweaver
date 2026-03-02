"""Contrast validation CLI command."""

import logging
from pathlib import Path
from typing import Any

from themeweaver.cli.error_handling import operation_context
from themeweaver.contrast import validate_theme

_logger = logging.getLogger(__name__)


def cmd_validate_contrast(args: Any) -> None:
    """Validate theme color contrast against Spyder UI rules."""
    theme_name = args.theme
    themes_dir = (
        Path(args.theme_dir) if hasattr(args, "theme_dir") and args.theme_dir else None
    )
    rules_dir = (
        Path(args.rules_dir) if hasattr(args, "rules_dir") and args.rules_dir else None
    )
    variants = getattr(args, "variant", "both")
    if variants == "both":
        variants = ["dark", "light"]
    else:
        variants = [variants]
    verbose = getattr(args, "verbose", False)

    _logger.info("Contrast validation for theme: %s", theme_name)

    with operation_context("Contrast validation"):
        total_passed = 0
        total_failed = 0

        for variant in variants:
            try:
                result = validate_theme(
                    theme_name=theme_name,
                    variant=variant,
                    themes_dir=themes_dir,
                    rules_dir=rules_dir,
                    include_suggestions=True,
                )
            except (ValueError, FileNotFoundError) as e:
                _logger.error("%s (%s): %s", variant, theme_name, e)
                continue

            total_passed += result.passed_count
            total_failed += result.failed_count

            status = "PASS" if result.all_passed else "FAIL"
            _logger.info(
                "  %s: %s (%d passed, %d failed)",
                variant,
                status,
                result.passed_count,
                result.failed_count,
            )

            if verbose or not result.all_passed:
                for r in result.results:
                    if r.passed and not verbose:
                        continue
                    symbol = "P" if r.passed else "F"
                    line = f"    [{symbol}] {r.rule_id}: {r.message or r.actual_ratio}"
                    if r.suggestion:
                        line += f"\n        Suggestion: {r.suggestion}"
                    _logger.info(line)

        _logger.info(
            "Total: %d passed, %d failed",
            total_passed,
            total_failed,
        )
