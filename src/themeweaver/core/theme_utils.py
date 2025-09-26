"""
Theme utilities for ThemeWeaver.

This module provides utility functions for theme generation, including
metadata generation, mappings creation, file writing, and analysis.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from themeweaver.color_utils.mappings_template import get_mappings_template

_logger = logging.getLogger(__name__)


def generate_theme_metadata(
    theme_name: str,
    display_name: Optional[str],
    description: Optional[str],
    author: str,
    tags: Optional[List[str]],
) -> Dict[str, Any]:
    """Generate theme.yaml content.

    Args:
        theme_name: Name of the theme
        display_name: Human-readable display name
        description: Theme description
        author: Theme author
        tags: List of theme tags

    Returns:
        Dictionary containing theme metadata
    """
    return {
        "name": theme_name,
        "display_name": display_name or theme_name.replace("_", " ").title(),
        "description": description or f"Generated theme: {theme_name}",
        "author": author,
        "version": "1.0.0",
        "license": "MIT",
        "tags": tags or ["dark", "light"],
        "variants": {"dark": True, "light": True},
    }


def generate_mappings(colorsystem_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate mappings.yaml content.

    Args:
        colorsystem_data: Color system data dictionary

    Returns:
        Dictionary containing color class and semantic mappings
    """
    # Extract palette names
    palette_names = colorsystem_data.pop(
        "_palette_names", {"primary": "Primary", "secondary": "Secondary"}
    )

    primary_name = palette_names["primary"]
    secondary_name = palette_names["secondary"]

    # Get the complete template mappings
    template_mappings = get_mappings_template()

    # Apply palette name substitutions to the template
    # This maps
    def substitute_palette_names(mappings_dict):
        """Recursively substitute palette names in mappings."""
        result = {}
        for key, value in mappings_dict.items():
            if isinstance(value, dict):
                result[key] = substitute_palette_names(value)
            elif isinstance(value, str):
                # Replace generic palette names with actual names
                if value.startswith("Primary."):
                    result[key] = value.replace("Primary", primary_name)
                elif value.startswith("Secondary."):
                    result[key] = value.replace("Secondary", secondary_name)
                else:
                    result[key] = value
            elif isinstance(value, list):
                # Handle syntax formatting lists [color, bold, italic]
                if len(value) == 3 and isinstance(value[0], str):
                    color_ref = value[0]
                    if color_ref.startswith("Primary."):
                        color_ref = color_ref.replace("Primary", primary_name)
                    elif color_ref.startswith("Secondary."):
                        color_ref = color_ref.replace("Secondary", secondary_name)
                    result[key] = [color_ref, value[1], value[2]]
                else:
                    result[key] = value
            else:
                result[key] = value
        return result

    return {
        "color_classes": {
            "Primary": primary_name,
            "Secondary": secondary_name,
            "Success": "Success",
            "Error": "Error",
            "Warning": "Warning",
            "GroupDark": "GroupDark",
            "GroupLight": "GroupLight",
            "Syntax": "Syntax",
            "Logos": "Logos",
        },
        "semantic_mappings": substitute_palette_names(template_mappings),
    }


def write_yaml_file(file_path: Path, data: Dict[str, Any]) -> str:
    """Write data to a YAML file (supports inline lists).

    Args:
        file_path: Path to the YAML file to write
        data: Dictionary data to write to the file

    Returns:
        String representation of the file path
    """

    class InlineListDumper(yaml.SafeDumper):
        def write_line_break(self, data=None):
            super().write_line_break(data)
            if len(self.indents) == 1:
                super().write_line_break()

        def represent_list(self, data):
            # Use inline format for lists with 6 or less elements
            if len(data) <= 6:
                return self.represent_sequence(
                    "tag:yaml.org,2002:seq", data, flow_style=True
                )
            return self.represent_sequence(
                "tag:yaml.org,2002:seq", data, flow_style=False
            )

    InlineListDumper.add_representer(list, InlineListDumper.represent_list)

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, Dumper=InlineListDumper, sort_keys=False, allow_unicode=True)

    _logger.info(f"📝 Created: {file_path}")
    return str(file_path)
