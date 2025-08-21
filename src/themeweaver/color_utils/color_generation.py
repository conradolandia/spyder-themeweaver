"""
Color generation algorithms for themeweaver.

This module provides color generation using LCH color space with different strategies:
- Uniform hue steps for simple, predictable palettes
- Golden ratio distribution for optimal distinguishability
"""

import math

from themeweaver.color_utils.color_utils import lch_to_hex


def generate_uniform_colors(num_colors, start_hue, base_lightness, base_chroma, theme):
    """
    Generate colors with uniform hue steps.

    Args:
        num_colors: Number of colors to generate
        start_hue: Starting hue in degrees
        base_lightness: Base lightness value
        base_chroma: Base chroma value
        theme: Theme type for adjustments

    Returns:
        List of hex color codes
    """
    colors = []
    hue_step = 360 / num_colors  # Uniform steps

    for i in range(num_colors):
        current_hue = (start_hue + i * hue_step) % 360
        current_lch = [base_lightness, base_chroma, current_hue]

        # Apply theme-specific adjustments
        adjusted_lch = apply_theme_adjustments(current_lch, theme)

        # Generate color
        color_hex = lch_to_hex(adjusted_lch[0], adjusted_lch[1], adjusted_lch[2])
        colors.append(color_hex)

    return colors


def apply_theme_adjustments(lch, theme):
    """
    Apply simple theme-specific adjustments to LCH values.

    Args:
        lch: [lightness, chroma, hue] values
        theme: 'dark' or 'light' theme

    Returns:
        list: Adjusted LCH values
    """
    lightness, chroma, hue = lch

    # Simple adjustments based on theme
    if theme == "dark":
        # Dark theme: slightly darker, higher chroma for visibility
        adjusted_lightness = max(15, lightness - 5)
        adjusted_chroma = min(120, chroma + 10)
    else:
        # Light theme: slightly brighter, moderate chroma
        adjusted_lightness = min(95, lightness + 8)
        adjusted_chroma = min(120, chroma + 5)

    return [adjusted_lightness, adjusted_chroma, hue]


def generate_theme_colors(
    theme="dark",
    num_colors=12,
    start_hue=None,
    uniform=False,
):
    """
    Generate color palettes using LCH color space.

    Args:
        theme: 'dark' or 'light' - determines lightness optimized for background
        num_colors: Number of colors to generate
        start_hue: Starting hue in degrees (0-360) or None for default
        uniform: If True, use uniform hue steps; if False, use golden ratio

    Returns:
        List of hex color codes
    """
    # Get theme-optimized parameters
    if theme == "dark":
        base_lightness = 58  # From Spyder Group dark palette average
        base_chroma = 73  # From Spyder Group dark palette average
        default_start_hue = 37  # Close to Spyder Group B10 hue
    else:  # light theme
        base_lightness = 65  # From Spyder Group light palette average
        base_chroma = 71  # From Spyder Group light palette average
        default_start_hue = 53  # Close to Spyder Group B10 hue

    actual_start_hue = start_hue if start_hue is not None else default_start_hue

    if uniform:
        return generate_uniform_colors(
            num_colors,
            actual_start_hue,
            base_lightness,
            base_chroma,
            theme,
        )
    else:
        # Use golden ratio distribution for better distinguishability
        return generate_golden_ratio_colors(
            num_colors,
            actual_start_hue,
            base_lightness,
            base_chroma,
            theme,
        )


def generate_golden_ratio_colors(
    num_colors, start_hue, base_lightness, base_chroma, theme
):
    """
    Generate colors using golden ratio distribution for optimal distinguishability.

    Args:
        num_colors: Number of colors to generate
        start_hue: Starting hue in degrees
        base_lightness: Base lightness value
        base_chroma: Base chroma value
        theme: Theme type for adjustments

    Returns:
        List of hex color codes
    """
    colors = []
    golden_ratio = 0.618033988749895

    for i in range(num_colors):
        # Use golden ratio for hue distribution
        hue = (start_hue + (i * 360 * golden_ratio)) % 360

        # Vary lightness slightly for better distinguishability
        lightness_variation = 0.5 + 0.3 * math.sin(i * 1.5)
        lightness = base_lightness + (lightness_variation - 0.5) * 20

        # Vary chroma slightly
        chroma_variation = 0.8 + 0.4 * math.cos(i * 0.8)
        chroma = base_chroma * chroma_variation

        current_lch = [lightness, chroma, hue]
        adjusted_lch = apply_theme_adjustments(current_lch, theme)

        # Generate color
        color_hex = lch_to_hex(adjusted_lch[0], adjusted_lch[1], adjusted_lch[2])
        colors.append(color_hex)

    return colors


def generate_optimal_colors(num_colors=12, theme="dark", start_hue=None):
    """
    Generate colors optimized for maximum distinguishability in variable explorer.

    This method is specifically designed for variable explorer tagging where
    colors need to be easily distinguishable from each other at a glance.

    Args:
        num_colors: Number of colors to generate
        theme: 'dark' or 'light' - determines lightness optimized for background
        start_hue: Starting hue in degrees (0-360). If None, uses default distribution.

    Returns:
        List of hex color codes optimized for distinguishability
    """
    # Use golden ratio for wider hue distribution
    golden_ratio = 0.618033988749895

    # Define lightness ranges for better variation
    if theme == "dark":
        lightness_range = (40, 75)  # Good range for dark backgrounds
    else:
        lightness_range = (60, 90)  # Good range for light backgrounds

    # Base chroma - start high for better distinguishability
    base_chroma = 85

    colors = []

    for i in range(num_colors):
        if start_hue is not None:
            # Use start_hue as the first color, then distribute from there
            if i == 0:
                hue = start_hue
            else:
                # Continue golden ratio distribution from start_hue
                hue = (start_hue + (i * 360 * golden_ratio)) % 360
        else:
            # Calculate hue using golden ratio for optimal distribution
            hue = (i * 360 * golden_ratio) % 360

        # Vary lightness using sinusoidal function for natural distribution
        lightness_variation = 0.5 + 0.4 * math.sin(i * 1.8)
        lightness = (
            lightness_range[0]
            + (lightness_range[1] - lightness_range[0]) * lightness_variation
        )

        # Vary chroma based on hue for better distinguishability
        # More chroma for hues that are typically less saturated
        h_factor = 1.0
        if 60 <= hue <= 180:  # Greens/cyan typically need more chroma
            h_factor = 1.3
        elif 180 <= hue <= 240:  # Blues
            h_factor = 1.2
        elif 240 <= hue <= 300:  # Magentas
            h_factor = 1.1

        # Dynamic chroma variation
        chroma_variation = 0.8 + 0.4 * math.cos(i * 0.9)
        chroma = min(120, base_chroma * h_factor * chroma_variation)

        # Generate color
        color_hex = lch_to_hex(lightness, chroma, hue)
        colors.append(color_hex)

    return colors
