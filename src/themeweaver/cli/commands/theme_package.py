"""
Theme packaging command.

This module handles packaging of exported themes into compressed archives
with proper metadata inclusion for distribution.
"""

import logging
from pathlib import Path
from typing import Any

from themeweaver.cli.error_handling import operation_context
from themeweaver.core.spyder_package_exporter import SpyderPackageExporter

_logger = logging.getLogger(__name__)


def cmd_python_package(args: Any) -> None:
    """Export themes as a single Spyder-compatible Python package."""

    # Parse theme names if provided
    theme_names = None
    if hasattr(args, "themes") and args.themes:
        theme_names = [t.strip() for t in args.themes.split(",")]

    # Create exporter
    exporter = SpyderPackageExporter(
        build_dir=Path(args.build_dir)
        if hasattr(args, "build_dir") and args.build_dir
        else None,
        output_dir=Path(args.output) if args.output else None,
        package_name=args.package_name
        if hasattr(args, "package_name")
        else "spyder_themes",
    )

    # Package metadata
    metadata = {
        "display_name": "Spyder Themes",
        "description": "Collection of themes for Spyder IDE",
        "author": "ThemeWeaver",
        "version": "1.0.0",
        "license": "MIT",
    }

    with operation_context("Package creation"):
        package_dir = exporter.create_package(
            theme_names=theme_names,
            metadata=metadata,
            with_pyproject=getattr(args, "with_pyproject", True),
            validate=getattr(args, "validate", True),
        )

        _logger.info("✅ Spyder package created: %s", package_dir)
