"""
Spyder Python file generator module for ThemeWeaver.

This module handles the generation of Spyder-compatible Python files:
- colorsystem.py with color class definitions
- palette.py with palette class definitions and semantic mappings
"""

import logging
from pathlib import Path
from typing import Dict

from themeweaver.core.palette import create_palettes
from themeweaver.core.colorsystem import (
    load_colors_from_yaml,
    load_color_mappings_from_yaml,
    load_semantic_mappings_from_yaml,
)

_logger = logging.getLogger(__name__)


class SpyderFileGenerator:
    """Generates Spyder-compatible Python files from ThemeWeaver themes."""

    def generate_files(self, theme_name: str, theme_metadata: Dict, export_dir: Path):
        """Generate all Spyder-compatible Python files.

        Args:
            theme_name: Name of the theme
            theme_metadata: Theme metadata from theme.yaml
            export_dir: Export directory
        """
        _logger.info("🐍 Generating Spyder Python files...")

        # Generate colorsystem.py
        colorsystem_path = export_dir / "colorsystem.py"
        self.generate_colorsystem_file(theme_name, theme_metadata, colorsystem_path)

        # Generate palette.py
        palette_path = export_dir / "palette.py"
        self.generate_palette_file(theme_name, theme_metadata, palette_path)

        _logger.info("📄 Generated: %s, %s", colorsystem_path.name, palette_path.name)

    def generate_colorsystem_file(
        self, theme_name: str, theme_metadata: Dict, output_path: Path
    ):
        """Generate colorsystem.py file compatible with Spyder's expectations."""

        # Load color definitions
        colors_data = load_colors_from_yaml(theme_name)
        color_mappings = load_color_mappings_from_yaml(theme_name)

        # Template for colorsystem.py
        template = '''# -*- coding: utf-8 -*-
#
# Generated by ThemeWeaver
# Theme: {theme_display_name}
# Description: {description}
# Author: {author}
# Version: {version}

"""
Extra colors used for the {theme_display_name} theme in Spyder.
"""

{color_classes}
'''

        # Generate color class definitions
        color_classes = []

        for class_name, palette_name in color_mappings.items():
            if palette_name in colors_data:
                colors = colors_data[palette_name]

                # Generate class definition
                class_def = f"class {class_name}:\n"
                for color_key, color_value in colors.items():
                    # Clean up any malformed hex values (like "##FFFFFF")
                    if isinstance(color_value, str) and color_value.startswith("##"):
                        color_value = color_value[1:]  # Remove extra #
                    class_def += f"    {color_key} = '{color_value}'\n"

                color_classes.append(class_def)

        # Format the template
        content = template.format(
            theme_display_name=theme_metadata.get("display_name", theme_name.title()),
            description=theme_metadata.get("description", ""),
            author=theme_metadata.get("author", "Unknown"),
            version=theme_metadata.get("version", "1.0.0"),
            color_classes="\n\n".join(color_classes),
        )

        # Write file
        output_path.write_text(content, encoding="utf-8")

    def generate_palette_file(
        self, theme_name: str, theme_metadata: Dict, output_path: Path
    ):
        """Generate palette.py file compatible with Spyder's expectations."""

        # Template for palette.py
        template = '''# -*- coding: utf-8 -*-
#
# Generated by ThemeWeaver  
# Theme: {theme_display_name}
# Description: {description}
# Author: {author}
# Version: {version}

"""
Palettes for {theme_display_name} theme used in Spyder.
"""

# Local imports  
from spyder.config.gui import is_dark_interface
from .colorsystem import {color_imports}

# =============================================================================
# ---- {theme_display_name} palettes
# =============================================================================

{palette_classes}

# =============================================================================
# ---- Exported classes
# =============================================================================
if is_dark_interface():
    SpyderPalette = SpyderPaletteDark
else:
    SpyderPalette = SpyderPaletteLight
'''

        # Load color mappings and semantic mappings
        color_mappings = load_color_mappings_from_yaml(theme_name)
        semantic_mappings = load_semantic_mappings_from_yaml(theme_name)
        color_imports = ", ".join(color_mappings.keys())

        # Load palettes to generate class definitions
        palettes = create_palettes(theme_name)

        palette_classes = []

        # Generate dark palette class if supported
        if palettes.has_dark:
            dark_attrs = []
            dark_semantic = semantic_mappings.get("dark", {})

            # Add ID attribute first
            dark_attrs.append('    ID = "dark"')

            for attr_name, color_ref in dark_semantic.items():
                # Handle numeric values (like OPACITY_TOOLTIP)
                if isinstance(color_ref, (int, float)):
                    dark_attrs.append(f"    {attr_name} = {color_ref}")
                else:
                    # Use colorsystem reference (e.g., "Primary.B10")
                    dark_attrs.append(f"    {attr_name} = {color_ref}")

            dark_class = f'''class SpyderPaletteDark:
    """Dark palette for {theme_metadata.get("display_name", theme_name)}."""

{chr(10).join(dark_attrs)}'''
            palette_classes.append(dark_class)

        # Generate light palette class if supported
        if palettes.has_light:
            light_attrs = []
            light_semantic = semantic_mappings.get("light", {})

            # Add ID attribute first
            light_attrs.append('    ID = "light"')

            for attr_name, color_ref in light_semantic.items():
                # Handle numeric values (like OPACITY_TOOLTIP)
                if isinstance(color_ref, (int, float)):
                    light_attrs.append(f"    {attr_name} = {color_ref}")
                else:
                    # Use colorsystem reference (e.g., "Primary.B140")
                    light_attrs.append(f"    {attr_name} = {color_ref}")

            light_class = f'''class SpyderPaletteLight:
    """Light palette for {theme_metadata.get("display_name", theme_name)}."""

{chr(10).join(light_attrs)}'''
            palette_classes.append(light_class)

        # Format the template
        content = template.format(
            theme_display_name=theme_metadata.get("display_name", theme_name.title()),
            description=theme_metadata.get("description", ""),
            author=theme_metadata.get("author", "Unknown"),
            version=theme_metadata.get("version", "1.0.0"),
            color_imports=color_imports,
            palette_classes="\n\n".join(palette_classes),
        )

        # Write file
        output_path.write_text(content, encoding="utf-8")
