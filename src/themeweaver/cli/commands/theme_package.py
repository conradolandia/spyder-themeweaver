"""
Theme packaging command.

This module handles packaging of exported themes into compressed archives
with proper metadata inclusion for distribution.
"""

import logging
from pathlib import Path
from typing import Any

from themeweaver.cli.error_handling import operation_context
from themeweaver.core.theme_packager import ThemePackager

_logger = logging.getLogger(__name__)


def cmd_package(args: Any) -> None:
    """Package exported theme(s) into compressed archives with metadata."""

    # Determine output directory and format
    output_dir = Path(args.output) if args.output else None
    format_type = getattr(args, "format", "zip")

    if args.theme:
        # Package specific theme
        theme_name = args.theme
        _logger.info("📦 Packaging theme: %s (format: %s)", theme_name, format_type)

        with operation_context("Theme packaging"):
            packager = ThemePackager(output_dir)
            package_path = packager.package_theme(theme_name, format_type)

            _logger.info("✅ Successfully packaged theme '%s':", theme_name)
            _logger.info("  📁 Package: %s", package_path)

    else:
        # Package all exported themes
        _logger.info("📦 Packaging all exported themes (format: %s)...", format_type)

        with operation_context("Theme packaging"):
            packager = ThemePackager(output_dir)
            packages = packager.package_all_themes(format_type)

            _logger.info("✅ Successfully packaged %d themes:", len(packages))
            for theme_name, package_path in packages.items():
                _logger.info("  • %s: %s", theme_name, package_path)
