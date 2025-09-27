"""
YAML theme definition loader.

This module provides functionality for loading theme definitions from YAML files.
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, Union

import yaml

_logger = logging.getLogger(__name__)


def load_theme_from_yaml(yaml_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a theme definition from a YAML file.

    Args:
        yaml_path: Path to the YAML file

    Returns:
        Dictionary with theme definition data
    """
    yaml_path = Path(yaml_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"Theme definition file not found: {yaml_path}")

    with open(yaml_path, "r") as f:
        yaml_data = yaml.safe_load(f)

    if not yaml_data:
        raise ValueError(f"Empty or invalid YAML file: {yaml_path}")

    # The YAML file should have a single top-level key which is the theme name
    # The value is the theme definition
    if len(yaml_data) != 1:
        raise ValueError(
            f"YAML file should have a single top-level key (theme name): {yaml_path}"
        )

    theme_name = list(yaml_data.keys())[0]
    theme_data = yaml_data[theme_name]

    # Add the theme name to the data
    theme_data["name"] = theme_name

    return theme_data


def parse_theme_definition(theme_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the theme definition data and convert it to the format expected by generate_theme_from_colors.

    Args:
        theme_data: Dictionary with theme definition data

    Returns:
        Dictionary with parsed theme data ready for theme generation
    """
    # Extract required fields
    theme_name = theme_data.get("name")
    if not theme_name:
        raise ValueError("Theme name is required")

    # Extract colors
    colors = theme_data.get("colors")
    if not colors or len(colors) != 6:
        raise ValueError("Theme colors are required and must contain exactly 6 colors")

    # Validate color format
    _validate_colors(colors)

    # Extract optional fields
    display_name = theme_data.get("display-name")
    description = theme_data.get("description")
    author = theme_data.get("author")
    tags = theme_data.get("tags", [])
    overwrite = theme_data.get("overwrite", False)

    # Extract variants
    variants = theme_data.get("variants", ["dark", "light"])

    # Extract syntax format
    syntax_format = None
    if "syntax-format" in theme_data:
        format_data = theme_data["syntax-format"]
        if format_data:
            # Convert the dictionary to the format expected by the CLI
            # e.g., "normal:none,keyword:bold,comment:italic"
            syntax_format = ",".join(
                f"{key}:{value}" for key, value in format_data.items()
            )

    # Extract syntax colors
    syntax_colors_dark = None
    syntax_colors_light = None

    if "syntax-colors" in theme_data:
        syntax_colors = theme_data["syntax-colors"]

        if "dark" in syntax_colors:
            dark_colors = syntax_colors["dark"]
            _validate_syntax_colors(dark_colors, "dark")
            if len(dark_colors) == 1:
                syntax_colors_dark = dark_colors[0]
            elif len(dark_colors) == 16:
                syntax_colors_dark = dark_colors

        if "light" in syntax_colors:
            light_colors = syntax_colors["light"]
            _validate_syntax_colors(light_colors, "light")
            if len(light_colors) == 1:
                syntax_colors_light = light_colors[0]
            elif len(light_colors) == 16:
                syntax_colors_light = light_colors

    # Prepare the result
    result = {
        "name": theme_name,
        "colors": colors,
        "display_name": display_name,
        "description": description,
        "author": author,
        "tags": tags,
        "overwrite": overwrite,
        "variants": variants,
        "syntax_format": syntax_format,
        "syntax_colors_dark": syntax_colors_dark,
        "syntax_colors_light": syntax_colors_light,
    }

    return result


def _validate_colors(colors: list) -> None:
    """
    Validate that colors are in proper hex format.

    Args:
        colors: List of color strings to validate

    Raises:
        ValueError: If any color is not in valid hex format
    """
    hex_pattern = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

    for i, color in enumerate(colors):
        if not isinstance(color, str):
            raise ValueError(
                f"Color {i + 1} must be a string, got {type(color).__name__}"
            )

        if not hex_pattern.match(color):
            raise ValueError(
                f"Color {i + 1} '{color}' is not a valid hex color. Expected format: #RRGGBB or #RGB"
            )


def _validate_syntax_colors(syntax_colors: list, variant: str) -> None:
    """
    Validate syntax colors format.

    Args:
        syntax_colors: List of syntax colors to validate
        variant: Variant name (dark/light) for error messages

    Raises:
        ValueError: If syntax colors are not valid
    """
    if not syntax_colors:
        return

    if len(syntax_colors) not in [1, 16]:
        raise ValueError(
            f"Syntax colors for {variant} variant must be either 1 color (for auto-generation) "
            f"or 16 colors (for custom palette), got {len(syntax_colors)}"
        )

    # Validate color format for syntax colors
    hex_pattern = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

    for i, color in enumerate(syntax_colors):
        if not isinstance(color, str):
            raise ValueError(
                f"Syntax color {i + 1} for {variant} variant must be a string, got {type(color).__name__}"
            )

        if not hex_pattern.match(color):
            raise ValueError(
                f"Syntax color {i + 1} for {variant} variant '{color}' is not a valid hex color. Expected format: #RRGGBB or #RGB"
            )
