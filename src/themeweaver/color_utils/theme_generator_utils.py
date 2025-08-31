"""
Theme generation utilities for ThemeWeaver.

This module provides functions for generating complete themes from individual colors,
including validation and theme structure creation.
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union

from themeweaver.color_utils.color_names import (
    generate_random_adjective,
    get_color_names_from_api,
)
from themeweaver.color_utils.color_utils import hex_to_rgb, rgb_to_lch
from themeweaver.color_utils.mappings_template import (
    get_mappings_template,
)
from themeweaver.color_utils.palette_generators import (
    generate_lightness_gradient_from_color,
    generate_palettes_from_color,
    generate_syntax_palette_from_colors,
)


def generate_main_palettes(
    primary_color: str,
    secondary_color: str,
    error_color: str,
    success_color: str,
    warning_color: str,
) -> Dict[str, List[str]]:
    """Generate main color palettes from individual colors.

    Args:
        primary_color: Hex color for Primary palette
        secondary_color: Hex color for Secondary palette
        error_color: Hex color for Error palette
        success_color: Hex color for Success palette
        warning_color: Hex color for Warning palette

    Returns:
        Dictionary mapping palette types to color lists
    """
    return {
        "primary": generate_lightness_gradient_from_color(primary_color),
        "secondary": generate_lightness_gradient_from_color(secondary_color),
        "error": generate_lightness_gradient_from_color(error_color),
        "success": generate_lightness_gradient_from_color(success_color),
        "warning": generate_lightness_gradient_from_color(warning_color),
    }


def get_palette_names(colors: List[str], color_names: Dict[str, str]) -> Dict[str, str]:
    """Generate creative names for palettes using color names from API.

    Args:
        colors: List of hex colors
        color_names: Dictionary mapping hex colors to their names

    Returns:
        Dictionary mapping color types to creative palette names
    """

    def get_creative_name(color: str) -> str:
        """Generate a creative name for a color."""
        normalized_color = color.upper()
        color_name = color_names.get(normalized_color)

        if color_name:
            # Clean up the color name
            clean_color_name = (
                color_name.replace(" ", "").replace("-", "").replace("'", "")
            )
            adjective = generate_random_adjective()
            return f"{adjective}{clean_color_name}"
        else:
            # Fallback to hex color if no name found
            fallback_name = color.replace("#", "")
            adjective = generate_random_adjective()
            return f"{adjective}{fallback_name}"

    return {
        "primary": get_creative_name(colors[0]),
        "secondary": get_creative_name(colors[1]),
        "error": get_creative_name(colors[2]),
        "success": get_creative_name(colors[3]),
        "warning": get_creative_name(colors[4]),
        "group_base": get_creative_name(colors[5]),
    }


def build_colorsystem(
    palettes: Dict[str, List[str]],
    names: Dict[str, str],
    group_initial_color: str,
    syntax_colors: Optional[Union[str, List[str]]] = None,
    logos: Optional[Dict[str, str]] = None,
) -> Dict[str, Dict[str, str]]:
    """Build the complete colorsystem with all palettes.

    Args:
        palettes: Dictionary of main palettes
        names: Dictionary of palette names
        group_initial_color: Initial color for group palettes
        syntax_colors: Optional syntax colors (single or list)
        logos: Optional logos palette

    Returns:
        Complete colorsystem dictionary
    """
    colorsystem: Dict[str, Dict[str, str]] = {}

    # Add main palettes
    for palette_type, palette in palettes.items():
        name = names[palette_type]
        colorsystem[name] = {f"B{i * 10}": palette[i] for i in range(16)}

    # Generate group palettes
    group_result = generate_palettes_from_color(
        group_initial_color, palette_type="group"
    )
    group_dark, group_light = group_result
    colorsystem[names["group_base"] + "Dark"] = group_dark
    colorsystem[names["group_base"] + "Light"] = group_light

    # Generate syntax palette
    if syntax_colors:
        if isinstance(syntax_colors, str):
            # Single color - generate palette
            syntax_palette = generate_palettes_from_color(
                syntax_colors, num_colors=16, palette_type="syntax"
            )
            syntax_name = names.get("syntax", "DefaultSyntax")
        else:
            # Multiple colors - use provided colors
            syntax_palette = generate_syntax_palette_from_colors(syntax_colors)
            syntax_name = names.get("syntax", "DefaultSyntax")

        colorsystem[syntax_name] = syntax_palette
    else:
        # Default syntax palette
        default_syntax_color = "#6B7280"  # Gray
        syntax_palette = generate_palettes_from_color(
            default_syntax_color, num_colors=16, palette_type="syntax"
        )
        colorsystem["DefaultSyntax"] = syntax_palette
        syntax_name = "DefaultSyntax"

    # Add Logos palette
    if logos:
        colorsystem["Logos"] = logos
    else:
        # Default logos
        colorsystem["Logos"] = {
            "B10": "#3775a9",  # Python
            "B20": "#ffd444",  # Python
            "B30": "#414141",  # Spyder logo
            "B40": "#fafafa",  # Spyder logo
            "B50": "#ee0000",  # Spyder logo
        }

    return colorsystem


def create_mappings(names: Dict[str, str], syntax_name: str) -> Dict[str, Any]:
    """Create theme mappings connecting semantic names to palette names.

    Args:
        names: Dictionary of palette names
        syntax_name: Name of the syntax palette

    Returns:
        Complete mappings dictionary
    """
    return {
        "color_classes": {
            "Primary": names["primary"],
            "Secondary": names["secondary"],
            "Success": names["success"],
            "Error": names["error"],
            "Warning": names["warning"],
            "GroupDark": names["group_base"] + "Dark",
            "GroupLight": names["group_base"] + "Light",
            "Syntax": syntax_name,
            "Logos": "Logos",
        },
        "semantic_mappings": get_mappings_template(),
    }


def generate_theme_from_colors(
    primary_color: str,
    secondary_color: str,
    error_color: str,
    success_color: str,
    warning_color: str,
    group_initial_color: str,
    syntax_colors: Optional[Union[str, List[str]]] = None,
    logos: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Generates a complete theme from individual colors.

    Args:
        primary_color: Hex color for the Primary palette
        secondary_color: Hex color for the Secondary palette
        error_color: Hex color for the Error palette
        success_color: Hex color for the Success palette
        warning_color: Hex color for the Warning palette
        group_initial_color: Initial color for GroupDark/GroupLight palettes
        syntax_colors: Either a single hex color (for auto-generation) or list of 16 hex colors
        logos: Dictionary with colors for the Logos palette (optional)

    Returns:
        dict: Complete theme structure with colorsystem and mappings
    """
    # Generate main palettes
    palettes = generate_main_palettes(
        primary_color, secondary_color, error_color, success_color, warning_color
    )

    # Prepare colors for naming
    all_colors = [
        primary_color,
        secondary_color,
        error_color,
        success_color,
        warning_color,
        group_initial_color,
    ]

    # Add syntax colors to the list for naming
    if syntax_colors:
        if isinstance(syntax_colors, str):
            all_colors.append(syntax_colors)
        else:
            all_colors.append(syntax_colors[0])

    # Get color names from API
    color_names = get_color_names_from_api(all_colors)

    # Generate creative names for palettes
    names = get_palette_names(all_colors, color_names)

    # Add syntax name to names dict
    if syntax_colors:
        if isinstance(syntax_colors, str):
            names["syntax"] = names.get("primary", "Default") + "Syntax"
        else:
            names["syntax"] = names.get("primary", "Default") + "Syntax"
    else:
        names["syntax"] = "DefaultSyntax"

    # Build colorsystem
    colorsystem = build_colorsystem(
        palettes, names, group_initial_color, syntax_colors, logos
    )

    # Create mappings
    mappings = create_mappings(names, names["syntax"])

    return {"colorsystem": colorsystem, "mappings": mappings}


def validate_input_colors(
    primary: str,
    secondary: str,
    error: str,
    success: str,
    warning: str,
    group: str,
    syntax_colors: Optional[Union[str, List[str]]] = None,
) -> Tuple[bool, str]:
    """
    Validates that input colors are suitable for theme generation.

    Args:
        primary, secondary, error, success, warning, group: Hex colors
        syntax_colors: Either a single hex color or list of 16 hex colors (optional)

    Returns:
        tuple: (is_valid, error_message)
    """
    colors: Dict[str, str] = {
        "primary": primary,
        "secondary": secondary,
        "error": error,
        "success": success,
        "warning": warning,
        "group": group,
    }

    # Add syntax colors to validation if provided
    if syntax_colors:
        if isinstance(syntax_colors, str):
            colors["syntax_seed"] = syntax_colors
        else:
            for i, color in enumerate(syntax_colors):
                colors[f"syntax_{i + 1}"] = color

    for name, color in colors.items():
        # Check hex format
        if not re.match(r"^#[0-9A-Fa-f]{6}$", color):
            return (
                False,
                f"Rejected: The {name} color ({color}) is not a valid hex format (#RRGGBB)",
            )

        # Convert to LCH
        rgb = hex_to_rgb(color)
        lightness, chroma, hue = rgb_to_lch(rgb)

        # Check lightness and chroma
        if lightness < 10:
            return (
                False,
                f"Rejected: The {name} color ({color}) is too dark (L={lightness:.1f})",
            )
        elif lightness > 90:
            return (
                False,
                f"Rejected: The {name} color ({color}) is too light (L={lightness:.1f})",
            )
        # Allow low saturation colors (including grays with chroma = 0)
        # Only warn for very low saturation that might not be intentional
        elif 0 < chroma < 5:
            # This is a very low saturation color, but still valid
            return (
                True,
                f"Warning: The {name} color ({color}) is a very low saturation color (C={chroma:.1f})",
            )

    return True, ""
