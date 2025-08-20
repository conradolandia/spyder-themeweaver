"""
Shared utilities for CLI commands.
"""

import logging
from pathlib import Path
from typing import List, Optional

from themeweaver.core.colorsystem import load_theme_metadata_from_yaml
from themeweaver.core.palette import create_palettes

_logger = logging.getLogger(__name__)


def setup_logging():
    """Configure logging for the CLI application."""
    # Set up console logging with INFO level by default
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",  # Simple format for CLI output
        handlers=[logging.StreamHandler()],
    )


def list_themes(themes_dir: Optional[Path] = None) -> List[str]:
    """List all available themes.

    Args:
        themes_dir: Directory containing themes. If None, uses default.

    Returns:
        List of theme names
    """
    if themes_dir is None:
        themes_dir = Path(__file__).parent.parent / "themes"

    themes = []
    for theme_dir in themes_dir.iterdir():
        if theme_dir.is_dir() and not theme_dir.name.startswith("."):
            # Check if it has the required files
            if (theme_dir / "theme.yaml").exists():
                themes.append(theme_dir.name)

    return sorted(themes)


def show_theme_info(theme_name: str):
    """Display information about a specific theme.

    Args:
        theme_name: Name of the theme to display info for
    """
    try:
        metadata = load_theme_metadata_from_yaml(theme_name)
        palettes = create_palettes(theme_name)

        _logger.info("📋 Theme: %s", metadata.get("display_name", theme_name))
        _logger.info("   Name: %s", theme_name)
        _logger.info(
            "   Description: %s", metadata.get("description", "No description")
        )
        _logger.info("   Author: %s", metadata.get("author", "Unknown"))
        _logger.info("   Version: %s", metadata.get("version", "Unknown"))
        _logger.info("   License: %s", metadata.get("license", "Unknown"))

        if metadata.get("url"):
            _logger.info("   URL: %s", metadata["url"])

        if metadata.get("tags"):
            _logger.info("   Tags: %s", ", ".join(metadata["tags"]))

        # Show supported variants
        _logger.info("   Variants: %s", ", ".join(palettes.supported_variants))

    except Exception as e:
        _logger.error("❌ Error loading theme '%s': %s", theme_name, e)
