"""
Theme generator for creating new Spyder themes.

This module provides functionality to generate complete theme definition files
using the existing color generation utilities from themeweaver.color_utils.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from themeweaver.core.palette_generator import generate_algorithmic_colorsystem
from themeweaver.core.theme_utils import (
    generate_theme_metadata,
    generate_mappings,
    write_yaml_file,
    analyze_algorithmic_palette,
)

_logger = logging.getLogger(__name__)


class ThemeGenerator:
    """Generator for creating complete Spyder theme definitions."""

    def __init__(self, themes_dir: Optional[Path] = None):
        """Initialize the theme generator.

        Args:
            themes_dir: Directory where themes are stored. If None, uses default.
        """
        if themes_dir is None:
            themes_dir = Path(__file__).parent.parent / "themes"

        self.themes_dir = Path(themes_dir)
        self.themes_dir.mkdir(exist_ok=True)

    def generate_theme_from_data(
        self,
        theme_name: str,
        theme_data: Dict,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        author: str = "ThemeWeaver",
        tags: Optional[List[str]] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """
        Generate a theme from pre-generated color data.

        Args:
            theme_name: Name for the theme (used for directory name)
            theme_data: Dictionary with colorsystem and mappings data
            display_name: Human-readable theme name
            description: Theme description
            author: Theme author
            tags: List of tags for the theme
            overwrite: Whether to overwrite existing theme

        Returns:
            Dict with paths to generated files
        """
        # Create theme directory
        theme_dir = self.themes_dir / theme_name
        if theme_dir.exists() and not overwrite:
            raise ValueError(
                f"Theme '{theme_name}' already exists. Use overwrite=True to replace."
            )

        theme_dir.mkdir(exist_ok=True)

        # Generate theme metadata
        theme_metadata = generate_theme_metadata(
            theme_name, display_name, description, author, tags
        )

        # Extract colorsystem and mappings from theme_data
        if (
            isinstance(theme_data, dict)
            and "colorsystem" in theme_data
            and "mappings" in theme_data
        ):
            # New structure with separate colorsystem and mappings
            colorsystem_data = theme_data["colorsystem"]
            mappings_data = theme_data["mappings"]
        else:
            # Legacy structure - treat theme_data as colorsystem and generate mappings
            colorsystem_data = theme_data
            mappings_data = generate_mappings(theme_data)

        # Write files
        files = {}
        files["theme.yaml"] = write_yaml_file(theme_dir / "theme.yaml", theme_metadata)
        files["colorsystem.yaml"] = write_yaml_file(
            theme_dir / "colorsystem.yaml", colorsystem_data
        )
        files["mappings.yaml"] = write_yaml_file(
            theme_dir / "mappings.yaml", mappings_data
        )

        _logger.info(f"✅ Theme '{theme_name}' generated successfully!")
        return files

    def generate_theme_from_palette(
        self,
        theme_name: str,
        palette_name: str,
        start_hue: Optional[int] = None,
        num_colors: int = 12,
        target_delta_e: float = 25,
        uniform: bool = False,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        author: str = "ThemeWeaver",
        tags: Optional[List[str]] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Generate a theme using algorithmic color generation.

        Args:
            theme_name: Name for the theme (used for directory name)
            palette_name: Name for the primary color palette
            start_hue: Starting hue for color generation (0-360)
            num_colors: Number of colors in group palettes
            target_delta_e: Target perceptual distance between colors
            uniform: Whether to use uniform hue steps instead of perceptual spacing
            display_name: Human-readable theme name
            description: Theme description
            author: Theme author
            tags: List of tags for the theme
            overwrite: Whether to overwrite existing theme

        Returns:
            Dict with paths to generated files
        """
        # Create theme directory
        theme_dir = self.themes_dir / theme_name
        if theme_dir.exists() and not overwrite:
            raise ValueError(
                f"Theme '{theme_name}' already exists. Use overwrite=True to replace."
            )

        theme_dir.mkdir(exist_ok=True)

        # Generate algorithmic color palettes
        _logger.info(
            f"🎨 Generating algorithmic color palettes for theme '{theme_name}'..."
        )
        colorsystem_data = generate_algorithmic_colorsystem(
            palette_name, start_hue, num_colors, target_delta_e, uniform
        )

        # Analyze generated colors
        analyze_algorithmic_palette(colorsystem_data, palette_name)

        # Generate theme metadata
        theme_data = generate_theme_metadata(
            theme_name, display_name, description, author, tags
        )

        # Generate color mappings
        mappings_data = generate_mappings(colorsystem_data)

        # Write files
        files = {}
        files["theme.yaml"] = write_yaml_file(theme_dir / "theme.yaml", theme_data)
        files["colorsystem.yaml"] = write_yaml_file(
            theme_dir / "colorsystem.yaml", colorsystem_data
        )
        files["mappings.yaml"] = write_yaml_file(
            theme_dir / "mappings.yaml", mappings_data
        )

        _logger.info(f"✅ Theme '{theme_name}' generated successfully!")
        return files

    def list_themes(self) -> List[str]:
        """List all available themes."""
        themes = []
        for theme_dir in self.themes_dir.iterdir():
            if theme_dir.is_dir() and not theme_dir.name.startswith("."):
                if (theme_dir / "theme.yaml").exists():
                    themes.append(theme_dir.name)
        return sorted(themes)

    def theme_exists(self, theme_name: str) -> bool:
        """Check if a theme already exists."""
        return (self.themes_dir / theme_name).exists()
