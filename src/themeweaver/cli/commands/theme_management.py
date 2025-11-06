"""
Theme management commands: list, info, validate.
"""

import logging
from pathlib import Path
from typing import Any

from themeweaver.cli.error_handling import operation_context
from themeweaver.cli.utils import list_themes, show_theme_info
from themeweaver.core.colorsystem import load_theme_metadata_from_yaml
from themeweaver.core.palette import create_palettes

_logger = logging.getLogger(__name__)


def cmd_list(args: Any) -> None:
    """List all available themes."""
    themes_dir = (
        Path(args.theme_dir) if hasattr(args, "theme_dir") and args.theme_dir else None
    )
    themes = list_themes(themes_dir=themes_dir)

    if not themes:
        _logger.info("No themes found.")
        return

    _logger.info("📚 Available themes (%d):", len(themes))
    for theme in themes:
        try:
            metadata = load_theme_metadata_from_yaml(theme, themes_dir=themes_dir)
            display_name = metadata.get("display_name", theme)
            description = metadata.get("description", "No description")
            variants = metadata.get("variants", {})
            variant_list = [v for v, enabled in variants.items() if enabled]

            _logger.info("  • %s (%s)", display_name, theme)
            _logger.info("    %s", description)
            _logger.info("    Variants: %s", ", ".join(variant_list))

        except Exception as e:
            _logger.error("  • %s (⚠️  Error loading metadata: %s)", theme, e)


def cmd_info(args: Any) -> None:
    """Show detailed information about a theme."""
    themes_dir = (
        Path(args.theme_dir) if hasattr(args, "theme_dir") and args.theme_dir else None
    )
    show_theme_info(args.theme, themes_dir=themes_dir)


def cmd_validate(args: Any) -> None:
    """Validate theme configuration files."""
    theme_name = args.theme
    themes_dir = (
        Path(args.theme_dir) if hasattr(args, "theme_dir") and args.theme_dir else None
    )

    _logger.info("🔍 Validating theme: %s", theme_name)

    with operation_context("Theme validation"):
        # Try to load metadata
        load_theme_metadata_from_yaml(theme_name, themes_dir=themes_dir)
        _logger.info("✅ theme.yaml: Valid")

        # Try to create palettes
        palettes = create_palettes(theme_name, themes_dir=themes_dir)
        _logger.info("✅ colorsystem.yaml: Valid")
        _logger.info("✅ mappings.yaml: Valid")

        # Show supported variants
        _logger.info(
            "✅ Supported variants: %s", ", ".join(palettes.supported_variants)
        )

        # Test palette instantiation
        for variant in palettes.supported_variants:
            palette_class = palettes.get_palette(variant)
            if palette_class:
                palette = palette_class()
                _logger.info("✅ %s palette: Valid (%s)", variant, palette.ID)

        _logger.info("✅ Theme '%s' is valid!", theme_name)
