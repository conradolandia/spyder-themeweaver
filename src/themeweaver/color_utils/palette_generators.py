"""
Palette generation utilities for ThemeWeaver.

This module provides functions for generating different types of color palettes
used in Spyder themes, including Spyder-compatible palettes and group palettes.
"""

import math
from typing import Dict, List, Tuple, Union

from themeweaver.color_utils import (
    adjust_lch_to_gamut,
    hex_to_rgb,
    is_lch_in_gamut,
    lch_to_hex,
    rgb_to_lch,
)

# Constants
GOLDEN_RATIO = 0.618033988749895
SYNTAX_PALETTE_SIZE = 16
DEFAULT_GROUP_PALETTE_SIZE = 12

# Lightness and chroma ranges for different palette types
SYNTAX_LIGHTNESS_RANGE = (40, 80)  # Good readability range
SYNTAX_CHROMA_RANGE = (40, 90)  # Moderate to high saturation for distinction
GROUP_DARK_LIGHTNESS_RANGE = (40, 75)
GROUP_LIGHT_LIGHTNESS_RANGE = (30, 60)

# Hue-specific chroma adjustment factors for better distinguishability
HUE_CHROMA_FACTORS = {
    # (start_hue, end_hue): factor
    (60, 180): 1.3,  # Greens/cyan typically need more chroma
    (180, 240): 1.2,  # Blues
    (240, 300): 1.1,  # Magentas
}

# Variation parameters for natural color distribution
LIGHTNESS_VARIATION_PARAMS = {
    "base": 0.5,
    "amplitude": 0.4,
    "frequency": 1.8,
}

CHROMA_VARIATION_PARAMS = {
    "base": 0.7,
    "amplitude": 0.5,
    "frequency": 0.9,
}


def _get_hue_chroma_factor(hue: float) -> float:
    """
    Get chroma adjustment factor based on hue for better distinguishability.

    Args:
        hue: Hue value in degrees (0-360)

    Returns:
        float: Chroma adjustment factor
    """
    for (start_hue, end_hue), factor in HUE_CHROMA_FACTORS.items():
        if start_hue <= hue <= end_hue:
            return factor
    return 1.0


def _calculate_color_variation(index: int, variation_params: Dict[str, float]) -> float:
    """
    Calculate variation value using sinusoidal function for natural distribution.

    Args:
        index: Color index in the palette
        variation_params: Dictionary with 'base', 'amplitude', and 'frequency' keys

    Returns:
        float: Variation value between 0 and 1
    """
    return variation_params["base"] + variation_params["amplitude"] * math.sin(
        index * variation_params["frequency"]
    )


def generate_lightness_gradient_from_color(color_hex: str) -> List[str]:
    """
    Generates a complete 16-color lightness gradient from a single color,
    placing the color in its natural position based on its lightness.

    Args:
        color_hex: Input hex color

    Returns:
        list: List of 16 hex colors forming a lightness gradient
    """
    # Convert to LCH
    rgb = hex_to_rgb(color_hex)
    lightness, chroma, hue = rgb_to_lch(rgb)

    # Check if in gamut and adjust if necessary
    if not is_lch_in_gamut(lightness, chroma, hue):
        lightness, chroma, hue = adjust_lch_to_gamut(lightness, chroma, hue)

    # Determine the natural position of the color in the gradient (0-15)
    # Map lightness (0-100) to position (0-15)
    natural_position = round((lightness / 100) * 15)

    # Ensure we're not at the extremes (avoid division by zero)
    natural_position = max(1, min(14, natural_position))

    # Calculate lightness steps
    lightness_values = []

    # Generate lightness values for the complete gradient
    for i in range(16):
        if i < natural_position:
            # Interpolate between black (L=0) and user color
            factor = i / natural_position
            lightness_values.append(lightness * factor)
        elif i > natural_position:
            # Interpolate between user color and white (L=100)
            factor = (i - natural_position) / (15 - natural_position)
            lightness_values.append(lightness + (100 - lightness) * factor)
        else:
            # Position of the original color
            lightness_values.append(lightness)

    # Calculate chroma values
    chroma_values = []
    for i in range(16):
        if i < natural_position:
            # Scale chroma proportionally to lightness
            # This avoids saturated but very dark colors that would be hard to distinguish
            factor = lightness_values[i] / lightness if lightness > 0 else 0
            chroma_values.append(chroma * factor)
        elif i > natural_position:
            # Gradually reduce chroma towards white
            factor = (
                1 - (lightness_values[i] - lightness) / (100 - lightness)
                if lightness < 100
                else 0
            )
            chroma_values.append(chroma * factor)
        else:
            chroma_values.append(chroma)

    # Generate final colors
    colors = []
    for i in range(16):
        # Check and adjust if outside gamut
        if not is_lch_in_gamut(lightness_values[i], chroma_values[i], hue):
            _, chroma_values[i], _ = adjust_lch_to_gamut(
                lightness_values[i], chroma_values[i], hue
            )

        colors.append(lch_to_hex(lightness_values[i], chroma_values[i], hue))

    # Ensure first color is black and last is white
    colors[0] = "#000000"
    colors[15] = "#FFFFFF"

    # Ensure the original color is in the palette at its natural position
    colors[natural_position] = color_hex

    return colors


def generate_palettes_from_color(
    initial_color_hex: str,
    num_colors: int = DEFAULT_GROUP_PALETTE_SIZE,
    palette_type: str = "group",
) -> Union[Tuple[Dict[str, str], Dict[str, str]], Dict[str, str]]:
    """
    Generates color palettes from an initial color.

    This function can generate different types of palettes:
    - "group": GroupDark and GroupLight palettes (default)
    - "syntax": Single syntax highlighting palette with 16 distinct colors

    Args:
        initial_color_hex: Initial hex color to base the palette on
        num_colors: Number of colors in each palette (default: 12, 16 for syntax)
        palette_type: Type of palette to generate ("group" or "syntax")

    Returns:
        For "group": tuple (group_dark_colors, group_light_colors) as dictionaries
        For "syntax": dict with B0-B150 keys containing 16 hex colors
    """
    # Convert to LCH
    rgb = hex_to_rgb(initial_color_hex)
    lightness, chroma, hue = rgb_to_lch(rgb)

    if palette_type == "syntax":
        return _generate_syntax_palette(lightness, chroma, hue)

    else:
        # Original group palette logic
        return _generate_group_palettes(
            initial_color_hex, lightness, chroma, hue, num_colors
        )


def _generate_syntax_palette(
    seed_lightness: float, seed_chroma: float, seed_hue: float
) -> Dict[str, str]:
    """
    Generate a syntax highlighting palette with 16 distinct colors.

    Args:
        seed_lightness: Base lightness from the seed color
        seed_chroma: Base chroma from the seed color
        seed_hue: Base hue from the seed color

    Returns:
        dict: Dictionary with B0-B150 keys containing 16 hex colors
    """
    syntax_palette = {}

    # Generate 16 colors (B0 to B150)
    for i in range(SYNTAX_PALETTE_SIZE):
        # Calculate hue using golden ratio for optimal distribution
        h_offset = (seed_hue + i * 360 * GOLDEN_RATIO) % 360

        # Vary lightness using sinusoidal function for natural distribution
        # Center the variation around the seed lightness
        lightness_variation = _calculate_color_variation(i, LIGHTNESS_VARIATION_PARAMS)

        # Map variation to a range around the seed lightness
        # This ensures the generated colors are more consistent with the seed color
        lightness_range = max(
            20, min(40, seed_lightness * 0.3)
        )  # Dynamic range based on seed
        lightness_i = seed_lightness + (lightness_variation - 0.5) * lightness_range

        # Clamp to our target range for syntax highlighting
        lightness_i = max(
            SYNTAX_LIGHTNESS_RANGE[0], min(SYNTAX_LIGHTNESS_RANGE[1], lightness_i)
        )

        # Get hue-specific chroma adjustment factor
        h_factor = _get_hue_chroma_factor(h_offset)

        # Dynamic chroma variation using cosine function
        chroma_variation = _calculate_color_variation(i, CHROMA_VARIATION_PARAMS)
        chroma_i = min(100, seed_chroma * h_factor * chroma_variation)

        # Ensure chroma is within our target range
        chroma_i = max(SYNTAX_CHROMA_RANGE[0], min(SYNTAX_CHROMA_RANGE[1], chroma_i))

        # Check and adjust gamut
        if not is_lch_in_gamut(lightness_i, chroma_i, h_offset):
            _, chroma_i, _ = adjust_lch_to_gamut(lightness_i, chroma_i, h_offset)

        # Add to palette
        syntax_palette[f"B{(i + 1) * 10}"] = lch_to_hex(lightness_i, chroma_i, h_offset)

    return syntax_palette


def _generate_group_palettes(
    initial_color_hex: str, lightness: float, chroma: float, hue: float, num_colors: int
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Generate GroupDark and GroupLight palettes.

    Args:
        initial_color_hex: Original color hex string
        lightness: Base lightness value
        chroma: Base chroma value
        hue: Base hue value
        num_colors: Number of colors in each palette

    Returns:
        tuple: (group_dark_colors, group_light_colors) as dictionaries
    """
    group_dark = {}
    group_light = {}

    # First color is the user-provided one
    group_dark["B10"] = initial_color_hex

    # For GroupLight, adjust the lightness of the initial color
    light_lightness = min(
        max(lightness + 20, GROUP_LIGHT_LIGHTNESS_RANGE[0]),
        GROUP_LIGHT_LIGHTNESS_RANGE[1],
    )
    if not is_lch_in_gamut(light_lightness, chroma, hue):
        _, chroma_adjusted, _ = adjust_lch_to_gamut(light_lightness, chroma, hue)
        group_light["B10"] = lch_to_hex(light_lightness, chroma_adjusted, hue)
    else:
        group_light["B10"] = lch_to_hex(light_lightness, chroma, hue)

    # Generate remaining colors
    for i in range(1, num_colors):
        # Calculate new hue using golden ratio for optimal distribution
        h_offset = (hue + i * 360 * GOLDEN_RATIO) % 360

        # Vary lightness and chroma for each color using sinusoidal functions
        dark_l_variation = _calculate_color_variation(i, LIGHTNESS_VARIATION_PARAMS)
        light_l_variation = _calculate_color_variation(i, LIGHTNESS_VARIATION_PARAMS)

        dark_l_i = (
            GROUP_DARK_LIGHTNESS_RANGE[0]
            + (GROUP_DARK_LIGHTNESS_RANGE[1] - GROUP_DARK_LIGHTNESS_RANGE[0])
            * dark_l_variation
        )
        light_l_i = (
            GROUP_LIGHT_LIGHTNESS_RANGE[0]
            + (GROUP_LIGHT_LIGHTNESS_RANGE[1] - GROUP_LIGHT_LIGHTNESS_RANGE[0])
            * light_l_variation
        )

        # Get hue-specific chroma adjustment factor
        h_factor = _get_hue_chroma_factor(h_offset)

        # Calculate chroma variations with different base values for dark/light
        dark_c_i = min(
            100,
            chroma
            * h_factor
            * (0.8 + 0.4 * math.cos(i * CHROMA_VARIATION_PARAMS["frequency"])),
        )
        light_c_i = min(
            100,
            chroma
            * h_factor
            * (0.7 + 0.5 * math.cos(i * CHROMA_VARIATION_PARAMS["frequency"])),
        )

        # Check and adjust gamut
        if not is_lch_in_gamut(dark_l_i, dark_c_i, h_offset):
            _, dark_c_i, _ = adjust_lch_to_gamut(dark_l_i, dark_c_i, h_offset)

        if not is_lch_in_gamut(light_l_i, light_c_i, h_offset):
            _, light_c_i, _ = adjust_lch_to_gamut(light_l_i, light_c_i, h_offset)

        # Add to palettes
        group_dark[f"B{(i + 1) * 10}"] = lch_to_hex(dark_l_i, dark_c_i, h_offset)
        group_light[f"B{(i + 1) * 10}"] = lch_to_hex(light_l_i, light_c_i, h_offset)

    return group_dark, group_light


def generate_syntax_palette_from_colors(syntax_colors: List[str]) -> Dict[str, str]:
    """
    Creates a syntax palette from a list of provided colors.

    Args:
        syntax_colors: List of hex colors for syntax highlighting

    Returns:
        dict: Dictionary with B0-B150 keys containing the provided colors

    Raises:
        ValueError: If not exactly SYNTAX_PALETTE_SIZE colors are provided
    """
    if len(syntax_colors) != SYNTAX_PALETTE_SIZE:
        raise ValueError(
            f"Expected {SYNTAX_PALETTE_SIZE} syntax colors, got {len(syntax_colors)}"
        )

    return {f"B{(i + 1) * 10}": color for i, color in enumerate(syntax_colors)}


def generate_syntax_from_group_colors(
    group_dark_colors: Dict[str, str], group_light_colors: Dict[str, str]
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Generate syntax highlighting palettes based on GroupDark and GroupLight colors.

    This function analyzes the group colors and generates syntax palettes that
    harmonize with the theme while maintaining good contrast and distinguishability.

    Args:
        group_dark_colors: Dictionary of GroupDark colors (B10-B120)
        group_light_colors: Dictionary of GroupLight colors (B10-B120)

    Returns:
        tuple: (syntax_dark_palette, syntax_light_palette) as dictionaries
    """
    # Extract color values from group palettes
    dark_values = list(group_dark_colors.values())
    light_values = list(group_light_colors.values())

    # Analyze the color characteristics of each group
    dark_analysis = _analyze_group_colors(dark_values)
    light_analysis = _analyze_group_colors(light_values)

    # Generate syntax palettes based on the analysis
    syntax_dark = _generate_syntax_from_analysis(dark_analysis, "dark")
    syntax_light = _generate_syntax_from_analysis(light_analysis, "light")

    return syntax_dark, syntax_light


def _analyze_group_colors(colors: List[str]) -> Dict[str, float]:
    """
    Analyze a list of group colors to extract characteristics for syntax generation.

    Args:
        colors: List of hex color strings

    Returns:
        dict: Analysis results with average lightness, chroma, hue distribution, etc.
    """
    lch_values = []
    for color in colors:
        rgb = hex_to_rgb(color)
        lch = rgb_to_lch(rgb)
        lch_values.append(lch)

    # Calculate averages and ranges
    lightnesses = [lch[0] for lch in lch_values]
    chromas = [lch[1] for lch in lch_values]
    hues = [lch[2] for lch in lch_values]

    # Calculate hue distribution (handle circular nature of hue)
    hue_distribution = _calculate_hue_distribution(hues)

    return {
        "avg_lightness": sum(lightnesses) / len(lightnesses),
        "avg_chroma": sum(chromas) / len(chromas),
        "lightness_range": max(lightnesses) - min(lightnesses),
        "chroma_range": max(chromas) - min(chromas),
        "hue_distribution": hue_distribution,
        "dominant_hues": _find_dominant_hues(hues),
        "color_count": len(colors),
    }


def _calculate_hue_distribution(hues: List[float]) -> Dict[str, float]:
    """Calculate the distribution of hues in the color palette."""
    # Group hues into sectors (0-60, 60-120, 120-180, etc.)
    sectors = [0] * 6
    for hue in hues:
        sector = int(hue // 60) % 6
        sectors[sector] += 1

    total = len(hues)
    return {
        "red_yellow": sectors[0] / total,
        "yellow_green": sectors[1] / total,
        "green_cyan": sectors[2] / total,
        "cyan_blue": sectors[3] / total,
        "blue_magenta": sectors[4] / total,
        "magenta_red": sectors[5] / total,
    }


def _find_dominant_hues(hues: List[float]) -> List[float]:
    """Find the most dominant hues in the palette."""
    # Group similar hues together (within 30 degrees)
    hue_groups = []
    for hue in hues:
        added_to_group = False
        for group in hue_groups:
            if any(abs(hue - group_hue) <= 30 for group_hue in group):
                group.append(hue)
                added_to_group = True
                break
        if not added_to_group:
            hue_groups.append([hue])

    # Find the largest groups
    hue_groups.sort(key=len, reverse=True)
    dominant_hues = []
    for group in hue_groups[:3]:  # Top 3 dominant hue groups
        if len(group) > 1:
            dominant_hues.append(sum(group) / len(group))
        else:
            dominant_hues.append(group[0])

    return dominant_hues


def _generate_syntax_from_analysis(
    analysis: Dict[str, float], variant: str
) -> Dict[str, str]:
    """
    Generate a syntax palette based on group color analysis.

    Args:
        analysis: Results from _analyze_group_colors
        variant: "dark" or "light" to adjust for theme variant

    Returns:
        dict: Syntax palette with B10-B160 keys
    """
    syntax_palette = {}

    # Base parameters from analysis
    base_lightness = analysis["avg_lightness"]
    base_chroma = analysis["avg_chroma"]
    dominant_hues = analysis["dominant_hues"]

    # Adjust for variant
    if variant == "dark":
        # For dark themes, syntax colors should be lighter and more saturated
        target_lightness = min(75, base_lightness + 15)
        target_chroma = min(90, base_chroma + 10)
    else:
        # For light themes, syntax colors should be darker and less saturated
        target_lightness = max(25, base_lightness - 15)
        target_chroma = min(80, base_chroma + 5)

    # Generate 16 colors using the dominant hues and adjusted parameters
    for i in range(SYNTAX_PALETTE_SIZE):
        # Cycle through dominant hues
        if dominant_hues:
            base_hue = dominant_hues[i % len(dominant_hues)]
        else:
            base_hue = (i * 360 / SYNTAX_PALETTE_SIZE) % 360

        # Add variation to hue for better distinguishability
        hue_variation = (i * 30) % 60 - 30  # ±30 degrees variation
        hue = (base_hue + hue_variation) % 360

        # Vary lightness around target
        lightness_variation = (i * 10) % 20 - 10  # ±10 lightness variation
        lightness = max(20, min(85, target_lightness + lightness_variation))

        # Vary chroma around target
        chroma_variation = (i * 5) % 15 - 7.5  # ±7.5 chroma variation
        chroma = max(30, min(100, target_chroma + chroma_variation))

        # Ensure color is in gamut
        if not is_lch_in_gamut(lightness, chroma, hue):
            lightness, chroma, hue = adjust_lch_to_gamut(lightness, chroma, hue)

        # Convert to hex
        color_hex = lch_to_hex(lightness, chroma, hue)
        syntax_palette[f"B{(i + 1) * 10}"] = color_hex

    return syntax_palette
