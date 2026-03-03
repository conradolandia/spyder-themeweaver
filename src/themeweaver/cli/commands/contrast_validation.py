"""Contrast validation CLI command."""

import logging
from pathlib import Path
from typing import Any, List

from themeweaver.cli.error_handling import operation_context
from themeweaver.contrast import validate_theme

_logger = logging.getLogger(__name__)


def _get_themes_to_validate(args: Any) -> List[str]:
    """Return list of theme names to validate."""
    if getattr(args, "all", False):
        themes_dir = Path(args.theme_dir) if getattr(args, "theme_dir", None) else None
        if themes_dir is None:
            themes_dir = Path.cwd() / "themes"
        if not themes_dir.exists():
            _logger.error("Theme directory not found: %s", themes_dir)
            return []
        return sorted(
            d.name
            for d in themes_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
    theme_name = getattr(args, "theme", None)
    return [theme_name] if theme_name else []


def cmd_validate_contrast(args: Any) -> None:
    """Validate theme color contrast against Spyder UI rules."""
    themes = _get_themes_to_validate(args)
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

    if not themes:
        _logger.error("No themes to validate")
        return

    with operation_context("Contrast validation"):
        grand_total_passed = 0
        grand_total_failed = 0

        for theme_name in themes:
            _logger.info("Contrast validation for theme: %s", theme_name)
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
                        line = (
                            f"    [{symbol}] {r.rule_id}: {r.message or r.actual_ratio}"
                        )
                        if r.suggestion:
                            line += f"\n        Suggestion: {r.suggestion}"
                        _logger.info(line)

            _logger.info(
                "  Total: %d passed, %d failed",
                total_passed,
                total_failed,
            )
            grand_total_passed += total_passed
            grand_total_failed += total_failed

        if len(themes) > 1:
            _logger.info(
                "Grand total: %d passed, %d failed",
                grand_total_passed,
                grand_total_failed,
            )
