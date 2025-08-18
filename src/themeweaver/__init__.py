"""
ThemeWeaver - Generate and export Spyder themes.

This package provides utilities for creating, managing, and exporting
Spyder-compatible themes with QDarkStyle integration.
"""

__version__ = "1.0.0"
__author__ = "Spyder Team"

# Core functionality exports
from themeweaver.core.theme import Theme
from themeweaver.core.palette import create_palettes, ThemePalettes
from themeweaver.core.exporter import ThemeExporter
from themeweaver.core.yaml_loader import (
    load_theme_metadata_from_yaml,
    load_colors_from_yaml,
    load_color_mappings_from_yaml,
    load_semantic_mappings_from_yaml,
)

# Color generation utilities
from themeweaver.color_utils.color_generation import (
    generate_theme_colors,
)

__all__ = [
    # Core classes
    "Theme",
    "ThemePalettes",
    "ThemeExporter",
    # Main functions
    "create_palettes",
    # YAML loaders
    "load_theme_metadata_from_yaml",
    "load_colors_from_yaml",
    "load_color_mappings_from_yaml",
    "load_semantic_mappings_from_yaml",
    # Color generation
    "generate_theme_colors",
    # Version info
    "__version__",
    "__author__",
]
