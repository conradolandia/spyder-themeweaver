"""
Theme generation utilities for ThemeWeaver.

This module provides functions for generating complete themes from individual colors,
including validation and theme structure creation.
"""

import re

from themeweaver.color_utils import hex_to_rgb, rgb_to_lch
from themeweaver.color_utils.color_names import (
    generate_random_adjective,
    get_multiple_color_names,
)
from themeweaver.color_utils.palette_generators import (
    generate_palettes_from_color,
    generate_spyder_palette_from_color,
    generate_syntax_palette_from_colors,
)
from themeweaver.color_utils.semantic_mappings_template import (
    get_semantic_mappings_template,
)


def generate_theme_from_colors(
    primary_color,
    secondary_color,
    error_color,
    success_color,
    warning_color,
    group_initial_color,
    syntax_colors=None,
    logos=None,
):
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
    primary_palette = generate_spyder_palette_from_color(primary_color)
    secondary_palette = generate_spyder_palette_from_color(secondary_color)
    error_palette = generate_spyder_palette_from_color(error_color)
    success_palette = generate_spyder_palette_from_color(success_color)
    warning_palette = generate_spyder_palette_from_color(warning_color)

    # Get all color names in a single API call
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
            # Single color - add to naming list
            all_colors.append(syntax_colors)
        else:
            # Multiple colors - add the first one for naming
            all_colors.append(syntax_colors[0])

    color_names = get_multiple_color_names(all_colors)

    # Generate creative names for palettes using the retrieved names
    def get_creative_name(color):
        # Normalize color to match API response format (uppercase)
        normalized_color = color.upper()
        color_name = color_names.get(normalized_color)
        if color_name:
            # Clean up the color name
            clean_color_name = (
                color_name.replace(" ", "").replace("-", "").replace("'", "")
            )
            # Generate random adjective
            adjective = generate_random_adjective()
            return f"{adjective}{clean_color_name}"
        else:
            # Fallback to hex color if no name found
            fallback_name = color.replace("#", "")
            adjective = generate_random_adjective()
            return f"{adjective}{fallback_name}"

    primary_name = get_creative_name(primary_color)
    secondary_name = get_creative_name(secondary_color)
    error_name = get_creative_name(error_color)
    success_name = get_creative_name(success_color)
    warning_name = get_creative_name(warning_color)
    group_base_name = get_creative_name(group_initial_color)
    group_dark_name = group_base_name + "Dark"
    group_light_name = group_base_name + "Light"

    # Build colorsystem with creative names
    colorsystem = {}
    colorsystem[primary_name] = {f"B{i * 10}": primary_palette[i] for i in range(16)}
    colorsystem[secondary_name] = {
        f"B{i * 10}": secondary_palette[i] for i in range(16)
    }
    colorsystem[error_name] = {f"B{i * 10}": error_palette[i] for i in range(16)}
    colorsystem[success_name] = {f"B{i * 10}": success_palette[i] for i in range(16)}
    colorsystem[warning_name] = {f"B{i * 10}": warning_palette[i] for i in range(16)}

    # Generate group palettes
    group_result = generate_palettes_from_color(
        group_initial_color, palette_type="group"
    )
    group_dark, group_light = group_result
    colorsystem[group_dark_name] = group_dark
    colorsystem[group_light_name] = group_light

    # Generate syntax palette
    if syntax_colors:
        if isinstance(syntax_colors, str):
            # Single color - generate palette using the existing function
            syntax_palette = generate_palettes_from_color(
                syntax_colors, num_colors=16, palette_type="syntax"
            )
            syntax_name = get_creative_name(syntax_colors) + "Syntax"
        else:
            # Multiple colors - use provided colors
            syntax_palette = generate_syntax_palette_from_colors(syntax_colors)
            syntax_name = get_creative_name(syntax_colors[0]) + "Syntax"

        colorsystem[syntax_name] = syntax_palette
    else:
        # Default syntax palette using a neutral color
        default_syntax_color = "#6B7280"  # Gray
        syntax_palette = generate_palettes_from_color(
            default_syntax_color, num_colors=16, palette_type="syntax"
        )
        syntax_name = "DefaultSyntax"
        colorsystem[syntax_name] = syntax_palette

    # Add Logos palette
    if logos:
        colorsystem["Logos"] = logos
    else:
        # Default values
        colorsystem["Logos"] = {
            "B10": "#3775a9",  # Python
            "B20": "#ffd444",  # Python
            "B30": "#414141",  # Spyder logo
            "B40": "#fafafa",  # Spyder logo
            "B50": "#ee0000",  # Spyder logo
        }

    # Build mappings to connect semantic names with creative palette names
    mappings = {
        "color_classes": {
            "Primary": primary_name,
            "Secondary": secondary_name,
            "Success": success_name,
            "Error": error_name,
            "Warning": warning_name,
            "GroupDark": group_dark_name,
            "GroupLight": group_light_name,
            "Syntax": syntax_name,
            "Logos": "Logos",
        },
        "semantic_mappings": get_semantic_mappings_template(),
    }

    return {"colorsystem": colorsystem, "mappings": mappings}


def validate_input_colors(
    primary, secondary, error, success, warning, group, syntax_colors=None
):
    """
    Validates that input colors are suitable for theme generation.

    Args:
        primary, secondary, error, success, warning, group: Hex colors
        syntax_colors: Either a single hex color or list of 16 hex colors (optional)

    Returns:
        tuple: (is_valid, error_message)
    """
    colors = {
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
                f"The {name} color ({color}) is not a valid hex format (#RRGGBB)",
            )

        # Convert to LCH
        rgb = hex_to_rgb(color)
        lightness, chroma, hue = rgb_to_lch(rgb)

        # Check lightness and chroma
        if lightness < 10:
            return False, f"The {name} color ({color}) is too dark (L={lightness:.1f})"
        elif lightness > 90:
            return False, f"The {name} color ({color}) is too light (L={lightness:.1f})"
        # Allow low saturation colors (including grays with chroma = 0)
        # Only warn for very low saturation that might not be intentional
        elif chroma < 5 and chroma > 0:
            # This is a very low saturation color, but still valid
            # We could add a warning here if needed, but don't reject it
            pass

    return True, ""
