"""
Theme exporter module for ThemeWeaver - Backward Compatibility Interface.

This module maintains backward compatibility by re-exporting functionality from the
new modular structure:
- theme_exporter.py: Main orchestrator
- qdarkstyle_exporter.py: QDarkStyle asset generation
- spyder_generator.py: Spyder Python file generation

For new code, prefer importing directly from the specific modules.
"""

# Re-export the main classes and functions for backward compatibility
from themeweaver.core.theme_exporter import ThemeExporter
from themeweaver.core.qdarkstyle_exporter import QDarkStyleAssetExporter
from themeweaver.core.spyder_generator import SpyderFileGenerator

# Make the main exports available at module level
__all__ = [
    "ThemeExporter",
    "QDarkStyleAssetExporter",
    "SpyderFileGenerator",
]
