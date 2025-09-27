"""
Theme export command.
"""

import logging
from pathlib import Path
from typing import Any

from themeweaver.cli.error_handling import operation_context
from themeweaver.core.theme_exporter import ThemeExporter

_logger = logging.getLogger(__name__)


def cmd_export(args: Any) -> None:
    """Export theme(s) to build directory."""

    # Determine build directory
    build_dir = Path(args.output) if args.output else None

    # Determine themes directory
    themes_dir = (
        Path(args.theme_dir) if hasattr(args, "theme_dir") and args.theme_dir else None
    )

    # Create exporter with custom directories
    exporter = ThemeExporter(build_dir=build_dir, themes_dir=themes_dir)

    if args.all:
        _logger.info("🎨 Exporting all themes...")
        with operation_context("Theme export"):
            exported = exporter.export_all_themes()

            _logger.info("✅ Successfully exported %d themes:", len(exported))
            for theme_name, variants in exported.items():
                _logger.info("  • %s: %s", theme_name, ", ".join(variants.keys()))

    else:
        # Export specific theme
        theme_name = args.theme
        variants = args.variants.split(",") if args.variants else None

        with operation_context("Theme export"):
            exported = exporter.export_theme(theme_name, variants)

            _logger.info("✅ Successfully exported theme '%s':", theme_name)
            for variant, path in exported.items():
                _logger.info("  • %s: %s", variant, path)
