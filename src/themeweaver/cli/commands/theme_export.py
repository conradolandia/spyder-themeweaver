"""
Theme export command.
"""

import logging
from pathlib import Path

from themeweaver.cli.error_handling import operation_context
from themeweaver.core.theme_exporter import ThemeExporter

_logger = logging.getLogger(__name__)


def cmd_export(args):
    """Export theme(s) to build directory."""

    # Determine build directory
    build_dir = Path(args.output) if args.output else None

    if args.all:
        _logger.info("🎨 Exporting all themes...")
        with operation_context("Theme export"):
            exported = ThemeExporter(build_dir).export_all_themes()

            _logger.info("✅ Successfully exported %d themes:", len(exported))
            for theme_name, variants in exported.items():
                _logger.info("  • %s: %s", theme_name, ", ".join(variants.keys()))

    else:
        # Export specific theme
        theme_name = args.theme
        variants = args.variants.split(",") if args.variants else None

        with operation_context("Theme export"):
            exported = ThemeExporter(build_dir).export_theme(theme_name, variants)

            _logger.info("✅ Successfully exported theme '%s':", theme_name)
            for variant, path in exported.items():
                _logger.info("  • %s: %s", variant, path)
