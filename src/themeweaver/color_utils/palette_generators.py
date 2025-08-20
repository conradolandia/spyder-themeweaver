"""
Palette generation utilities for ThemeWeaver.

This module provides functions for generating different types of color palettes
used in Spyder themes, including Spyder-compatible palettes and group palettes.
"""

import math

from themeweaver.color_utils import (
    adjust_lch_to_gamut,
    hex_to_rgb,
    is_lch_in_gamut,
    lch_to_hex,
    rgb_to_lch,
)


def generate_spyder_palette_from_color(color_hex):
    """
    Generates a complete 16-color Spyder palette from a single color,
    placing the color in its natural position based on its lightness.

    Args:
        color_hex: Input hex color

    Returns:
        list: List of 16 hex colors
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


def generate_group_palettes_from_color(initial_color_hex, num_colors=12):
    """
    Generates GroupDark and GroupLight palettes from an initial color.

    This function is designed for generating palettes when you have a specific
    color that should be the base (B10) of both GroupDark and GroupLight palettes.
    It's commonly used in theme generation from user-provided colors.

    Args:
        initial_color_hex: Initial hex color (B10 of both palettes)
        num_colors: Number of colors in each palette (default: 12)

    Returns:
        tuple: (group_dark_colors, group_light_colors) as dictionaries
    """
    # Convert to LCH
    rgb = hex_to_rgb(initial_color_hex)
    lightness, chroma, hue = rgb_to_lch(rgb)

    # Define ranges for each palette
    dark_l_range = (40, 75)  # Lightness range for GroupDark
    light_l_range = (60, 95)  # Lightness range for GroupLight

    # Distribute hues uniformly with sufficient separation
    # Using golden ratio for optimal distribution
    golden_ratio = 0.618033988749895

    group_dark = {}
    group_light = {}

    # First color is the user-provided one
    group_dark["B10"] = initial_color_hex

    # For GroupLight, adjust the lightness of the initial color
    light_lightness = min(max(lightness + 20, light_l_range[0]), light_l_range[1])
    if not is_lch_in_gamut(light_lightness, chroma, hue):
        _, chroma_adjusted, _ = adjust_lch_to_gamut(light_lightness, chroma, hue)
        group_light["B10"] = lch_to_hex(light_lightness, chroma_adjusted, hue)
    else:
        group_light["B10"] = lch_to_hex(light_lightness, chroma, hue)

    # Generate remaining colors
    for i in range(1, num_colors):
        # Calculate new hue using golden ratio for optimal distribution
        h_offset = (hue + i * 360 * golden_ratio) % 360

        # Vary lightness and chroma for each color
        # Use sinusoidal functions to create natural variation
        dark_l_i = dark_l_range[0] + (dark_l_range[1] - dark_l_range[0]) * (
            0.5 + 0.4 * math.sin(i * 1.8)
        )
        light_l_i = light_l_range[0] + (light_l_range[1] - light_l_range[0]) * (
            0.5 + 0.4 * math.sin(i * 1.8)
        )

        # Vary chroma to increase distinction
        # More chroma for hues that are typically less saturated
        h_factor = 1.0
        if 60 <= h_offset <= 180:  # Greens/cyan typically need more chroma
            h_factor = 1.2
        elif 180 <= h_offset <= 240:  # Blues
            h_factor = 1.1

        dark_c_i = min(100, chroma * h_factor * (0.8 + 0.4 * math.cos(i * 0.9)))
        light_c_i = min(100, chroma * h_factor * (0.7 + 0.5 * math.cos(i * 0.9)))

        # Check and adjust gamut
        if not is_lch_in_gamut(dark_l_i, dark_c_i, h_offset):
            _, dark_c_i, _ = adjust_lch_to_gamut(dark_l_i, dark_c_i, h_offset)

        if not is_lch_in_gamut(light_l_i, light_c_i, h_offset):
            _, light_c_i, _ = adjust_lch_to_gamut(light_l_i, light_c_i, h_offset)

        # Add to palettes
        group_dark[f"B{(i + 1) * 10}"] = lch_to_hex(dark_l_i, dark_c_i, h_offset)
        group_light[f"B{(i + 1) * 10}"] = lch_to_hex(light_l_i, light_c_i, h_offset)

    return group_dark, group_light
