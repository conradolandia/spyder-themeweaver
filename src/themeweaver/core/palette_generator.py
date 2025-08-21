"""
Palette generation utilities for ThemeWeaver.

This module provides functions for generating different types of color palettes
used in Spyder themes, including algorithmic generation and standard palettes.
"""

from typing import Dict, Optional, Tuple

from themeweaver.color_utils import hex_to_rgb, lch_to_hex, rgb_to_lch
from themeweaver.color_utils.color_generation import generate_theme_colors
from themeweaver.color_utils.palette_generators import (
    generate_spyder_palette_from_color,
)


def generate_algorithmic_colorsystem(
    palette_name: str,
    start_hue: Optional[int],
    num_colors: int,
    uniform: bool,
) -> Dict:
    """Generate colorsystem using algorithmic color generation."""
    colorsystem = {}

    # Generate primary palette using algorithmic approach
    if uniform:
        # For uniform generation, get colors for dark endpoints
        dark_colors = generate_theme_colors(
            "dark", 4, uniform=True
        )  # Get 4 colors to have options

        # Use first and second darkest colors for primary and secondary palettes
        primary_dark = dark_colors[0]
        secondary_dark = dark_colors[1] if len(dark_colors) > 1 else dark_colors[0]
    else:
        # For optimized generation, create colors suitable for Spyder endpoints
        dark_colors = generate_theme_colors(
            theme="dark",
            start_hue=start_hue,
            num_colors=4,
        )

        # Use first and middle colors for primary and secondary palettes
        primary_dark = dark_colors[0]
        secondary_dark = dark_colors[1] if len(dark_colors) > 1 else dark_colors[0]

    # Generate Spyder-compliant palettes
    # For algorithmic generation, we'll use the first color as the base
    primary_palette = generate_spyder_palette_from_color(primary_dark)
    secondary_palette = generate_spyder_palette_from_color(secondary_dark)

    # Add primary palette with proper B-step format
    colorsystem[palette_name] = {}
    for i, color in enumerate(primary_palette):
        step = i * 10
        colorsystem[palette_name][f"B{step}"] = color

    # Create secondary palette name and add it
    secondary_name = f"{palette_name}Light"
    colorsystem[secondary_name] = {}
    for i, color in enumerate(secondary_palette):
        step = i * 10
        colorsystem[secondary_name][f"B{step}"] = color

    # Add standard palettes
    colorsystem.update(generate_standard_palettes())

    # Add Group palettes
    colorsystem.update(
        generate_group_palettes_algorithmic(start_hue, num_colors, uniform)
    )

    # Add Logos palette
    colorsystem.update(generate_logos_palette())

    # Store palette names for mappings
    colorsystem["_palette_names"] = {
        "primary": palette_name,
        "secondary": secondary_name,
    }

    return colorsystem


def generate_standard_palettes(
    primary_colors: Optional[Tuple[str, str]] = None, method: str = "lch"
) -> Dict:
    """Generate standard Success, Error, Warning palettes using dynamic color generation.

    Args:
        primary_colors: Tuple of (dark_color, light_color) for primary palette (if available)
                      If provided, uses the dark color's characteristics for harmonization
        method: Interpolation method for color generation

    Returns:
        Dict with Success, Error, Warning palettes
    """
    # Define color wheel regions
    SUCCESS_HUE = 120  # Success region
    ERROR_HUE = 0  # Error region
    WARNING_HUE = 30  # Warning region

    # Determine base characteristics for harmonization
    if primary_colors:
        # Extract characteristics from user-provided dark color for harmonization
        # Get LCH characteristics from primary dark color to harmonize standard palettes
        primary_dark_lch = rgb_to_lch(hex_to_rgb(primary_colors[0]))

        # Use lightness and chroma characteristics from dark color for harmonization
        base_lightness_dark = primary_dark_lch[0]
        base_chroma = primary_dark_lch[1]

        # Generate harmonized colors using user color characteristics
        success_dark = lch_to_hex(base_lightness_dark, base_chroma, SUCCESS_HUE)
        error_dark = lch_to_hex(base_lightness_dark, base_chroma, ERROR_HUE)
        warning_dark = lch_to_hex(base_lightness_dark, base_chroma, WARNING_HUE)

    else:
        # Use algorithmic generation with specific hue regions
        # For standard palettes, generate more subdued colors that work well with black/white endpoints
        # Use moderate lightness and chroma values to avoid jarring transitions

        # Define more conservative LCH values for smooth gradients
        DARK_LIGHTNESS = 15  # Dark enough to transition smoothly from black
        MODERATE_CHROMA = 50  # Moderate saturation to avoid harsh jumps

        # Generate harmonized colors using conservative LCH values
        success_dark = lch_to_hex(DARK_LIGHTNESS, MODERATE_CHROMA, SUCCESS_HUE)
        error_dark = lch_to_hex(DARK_LIGHTNESS, MODERATE_CHROMA, ERROR_HUE)
        warning_dark = lch_to_hex(DARK_LIGHTNESS, MODERATE_CHROMA, WARNING_HUE)

    # Generate full 16-color palettes using the new single-color approach
    success_palette = generate_spyder_palette_from_color(success_dark)
    error_palette = generate_spyder_palette_from_color(error_dark)
    warning_palette = generate_spyder_palette_from_color(warning_dark)

    # Convert to B-step format
    standard_palettes = {}

    # Add Success palette
    standard_palettes["Success"] = {}
    for i, color in enumerate(success_palette):
        step = i * 10
        standard_palettes["Success"][f"B{step}"] = color

    # Add Error palette
    standard_palettes["Error"] = {}
    for i, color in enumerate(error_palette):
        step = i * 10
        standard_palettes["Error"][f"B{step}"] = color

    # Add Warning palette
    standard_palettes["Warning"] = {}
    for i, color in enumerate(warning_palette):
        step = i * 10
        standard_palettes["Warning"][f"B{step}"] = color

    return standard_palettes


def generate_group_palettes_algorithmic(
    start_hue: Optional[int] = None,
    num_colors: int = 12,
    uniform: bool = False,
) -> Dict:
    """
    Generate GroupDark and GroupLight palettes using algorithmic methods.
    """
    if uniform:
        dark_colors = generate_theme_colors("dark", num_colors, uniform=True)
        light_colors = generate_theme_colors("light", num_colors, uniform=True)
    else:
        dark_colors = generate_theme_colors(
            theme="dark",
            start_hue=start_hue,
            num_colors=num_colors,
        )
        light_colors = generate_theme_colors(
            theme="light",
            start_hue=start_hue,
            num_colors=num_colors,
        )

    group_palettes = {"GroupDark": {}, "GroupLight": {}}

    # Add GroupDark colors
    for i, color in enumerate(dark_colors):
        step = (i + 1) * 10
        group_palettes["GroupDark"][f"B{step}"] = color

    # Add GroupLight colors
    for i, color in enumerate(light_colors):
        step = (i + 1) * 10
        group_palettes["GroupLight"][f"B{step}"] = color

    return group_palettes


def generate_logos_palette() -> Dict:
    """Generate standard Logos palette."""
    return {
        "Logos": {
            "B10": "#3775a9",
            "B20": "#ffd444",
            "B30": "#414141",
            "B40": "#fafafa",
            "B50": "#ee0000",
        }
    }
