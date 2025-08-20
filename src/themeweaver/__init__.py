"""
ThemeWeaver - Generate and export Spyder themes.

This package provides utilities for creating, managing, and exporting
Spyder-compatible themes with QDarkStyle integration.
"""

__version__ = "1.0.0"
__author__ = "Andres Conrado Montoya Acosta (@conradolandia)"

from themeweaver.core.exporter import ThemeExporter
from themeweaver.core.palette import ThemePalettes, create_palettes

# Core functionality exports
from themeweaver.core.theme import Theme
from themeweaver.core.yaml_loader import (
    load_color_mappings_from_yaml,
    load_colors_from_yaml,
    load_semantic_mappings_from_yaml,
    load_theme_metadata_from_yaml,
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
    # Version info
    "__version__",
    "__author__",
]
