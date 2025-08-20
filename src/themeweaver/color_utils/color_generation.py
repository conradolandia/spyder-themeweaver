"""
Color generation algorithms for themeweaver.

This module provides perceptually uniform color generation using LCH color space
and Delta E spacing for scientifically sound color palettes.
"""

import math

from themeweaver.color_utils.color_utils import calculate_delta_e, lch_to_hex


def get_theme_parameters(theme="dark"):
    """
    Get optimized LCH parameters for a specific theme.

    Args:
        theme: 'dark' or 'light' theme

    Returns:
        dict: Theme parameters with base_lightness, base_chroma, default_start_hue
    """
    if theme == "dark":
        return {
            "base_lightness": 58,  # From Spyder Group dark palette average
            "base_chroma": 73,  # From Spyder Group dark palette average
            "default_start_hue": 37,  # Close to Spyder Group B10 hue
        }
    else:  # light theme
        return {
            "base_lightness": 65,  # From Spyder Group light palette average
            "base_chroma": 71,  # From Spyder Group light palette average
            "default_start_hue": 53,  # Close to Spyder Group B10 hue
        }


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

        # Apply Spyder Group-style adjustments
        adjusted_lch = apply_group_hue_adjustments(current_lch, theme)

        # Generate color
        color_hex = lch_to_hex(adjusted_lch[0], adjusted_lch[1], adjusted_lch[2])
        colors.append(color_hex)

    return colors


def generate_perceptual_colors(
    num_colors, start_hue, base_lightness, base_chroma, target_delta_e, theme
):
    """
    Generate colors with uniform perceptual spacing.

    Args:
        num_colors: Number of colors to generate
        start_hue: Starting hue in degrees
        base_lightness: Base lightness value
        base_chroma: Base chroma value
        target_delta_e: Target perceptual distance
        theme: Theme type for adjustments

    Returns:
        List of hex color codes
    """
    start_color_lch = [base_lightness, base_chroma, start_hue]
    colors = []
    current_lch = start_color_lch.copy()

    for i in range(num_colors):
        # Apply hue-specific adjustments for optimal visibility
        adjusted_lch = apply_group_hue_adjustments(current_lch, theme)

        # Generate current color
        color_hex = lch_to_hex(adjusted_lch[0], adjusted_lch[1], adjusted_lch[2])
        colors.append(color_hex)

        if i < num_colors - 1:  # Not the last color
            # Find next hue that achieves target Delta E
            current_lch = find_next_perceptual_color(
                current_lch, target_delta_e, base_lightness, base_chroma, theme
            )

    return colors


def generate_theme_colors(
    theme="dark",
    num_colors=12,
    target_delta_e=25,
    start_hue=None,
    uniform=False,
):
    """
    Generate color palettes using LCH color space with optional uniform or perceptual spacing.

    Updated based on Spyder Group palette analysis to include hue-specific adjustments
    for optimal visibility per theme.

    Args:
        theme: 'dark' or 'light' - determines lightness optimized for background
        num_colors: Number of colors to generate
        target_delta_e: Target perceptual distance between consecutive colors (ignored if uniform=True)
        start_hue: Starting hue in degrees (0-360) or None for default
        uniform: If True, use uniform hue steps; if False, use perceptual spacing

    Returns:
        List of hex color codes with uniform or perceptually uniform spacing
    """
    # Get theme-optimized parameters
    params = get_theme_parameters(theme)
    actual_start_hue = (
        start_hue if start_hue is not None else params["default_start_hue"]
    )

    if uniform:
        return generate_uniform_colors(
            num_colors,
            actual_start_hue,
            params["base_lightness"],
            params["base_chroma"],
            theme,
        )
    else:
        return generate_perceptual_colors(
            num_colors,
            actual_start_hue,
            params["base_lightness"],
            params["base_chroma"],
            target_delta_e,
            theme,
        )


def get_hue_range(hue):
    """
    Determine which hue range a color falls into.

    Args:
        hue: Hue value in degrees (0-360)

    Returns:
        str: Hue range identifier
    """
    hue = hue % 360

    if 0 <= hue < 60:
        return "red_yellow"
    elif 60 <= hue < 120:
        return "yellow_green"
    elif 120 <= hue < 180:
        return "green_cyan"
    elif 180 <= hue < 240:
        return "cyan_blue"
    elif 240 <= hue < 300:
        return "blue_magenta"
    else:  # 300-360
        return "magenta_red"


def get_hue_adjustments(hue_range, theme):
    """
    Get lightness and chroma adjustments for a specific hue range and theme.

    Args:
        hue_range: Hue range identifier
        theme: 'dark' or 'light' theme

    Returns:
        tuple: (lightness_adjustment, chroma_adjustment)
    """
    adjustments = {
        "red_yellow": {
            "dark": (-5, 10),  # Slightly darker, higher chroma
            "light": (10, 15),  # Brighter, higher chroma
        },
        "yellow_green": {
            "dark": (8, 5),  # Brighter, moderate chroma
            "light": (15, 20),  # Very bright, high chroma
        },
        "green_cyan": {
            "dark": (8, -10),  # Brighter, lower chroma
            "light": (8, -10),  # Same for both themes
        },
        "cyan_blue": {
            "dark": (10, -25),  # Brighter, much lower chroma
            "light": (5, -15),  # Moderate adjustments
        },
        "blue_magenta": {
            "dark": (-15, 15),  # Darker, higher chroma
            "light": (-20, 5),  # Much darker, moderate chroma
        },
        "magenta_red": {
            "dark": (-5, 0),  # Slightly darker, no chroma change
            "light": (-10, -5),  # Darker, lower chroma
        },
    }

    return adjustments[hue_range][theme]


def apply_group_hue_adjustments(lch, theme):
    """
    Apply hue-specific lightness and chroma adjustments based on Spyder Group palette analysis.
    This tries to mimic the intelligent design choices made by Isabella in the original Spyder Group palettes.
    It is not perfect, but it is a good starting point. Final manual adjustments probably should be made by the user.
    """
    lightness, chroma, hue = lch

    # Get hue range and adjustments
    hue_range = get_hue_range(hue)
    lightness_adj, chroma_adj = get_hue_adjustments(hue_range, theme)

    # Apply adjustments
    adjusted_lightness = lightness + lightness_adj
    adjusted_chroma = chroma + chroma_adj

    # Ensure valid LCH ranges
    final_lightness = max(15, min(95, adjusted_lightness))
    final_chroma = max(20, min(120, adjusted_chroma))

    return [final_lightness, final_chroma, hue]


def get_search_range(target_delta_e):
    """
    Get the appropriate search range based on target delta-e.

    Args:
        target_delta_e: Target perceptual distance

    Returns:
        range: Search range for hue increments
    """
    if target_delta_e < 15:
        return range(5, 60, 2)  # Fine search for small distances
    elif target_delta_e < 35:
        return range(10, 120, 3)  # Medium search
    else:
        return range(20, 180, 5)  # Wide search for large distances


def generate_test_candidates(adjusted_lch, target_delta_e):
    """
    Generate test LCH candidates for fine-tuning.

    Args:
        adjusted_lch: Base adjusted LCH values
        target_delta_e: Target perceptual distance

    Returns:
        list: List of LCH candidates to test
    """
    candidates = [adjusted_lch]

    # Add slight variations only if needed for fine-tuning
    if target_delta_e > 20:
        candidates.extend(
            [
                [adjusted_lch[0] + 3, adjusted_lch[1], adjusted_lch[2]],
                [adjusted_lch[0] - 3, adjusted_lch[1], adjusted_lch[2]],
                [adjusted_lch[0], adjusted_lch[1] + 5, adjusted_lch[2]],
                [adjusted_lch[0], adjusted_lch[1] - 5, adjusted_lch[2]],
            ]
        )

    return candidates


def validate_lch_bounds(lch):
    """
    Ensure LCH values are within valid bounds.

    Args:
        lch: [lightness, chroma, hue] values

    Returns:
        list: Validated LCH values
    """
    return [
        max(0, min(100, lch[0])),  # Lightness 0-100
        max(0, min(120, lch[1])),  # Chroma 0-120
        lch[2],  # Hue can wrap around
    ]


def find_next_perceptual_color(
    current_lch, target_delta_e, base_lightness, base_chroma, theme
):
    """Find the next color that achieves the target perceptual distance."""
    current_hex = lch_to_hex(current_lch[0], current_lch[1], current_lch[2])

    best_delta_e_diff = float("inf")
    best_lch = [base_lightness, base_chroma, current_lch[2]]

    # Get appropriate search range
    hue_range = get_search_range(target_delta_e)

    # Search primarily by hue, with minimal variations
    for hue_increment in hue_range:
        test_hue = (current_lch[2] + hue_increment) % 360
        test_lch = [base_lightness, base_chroma, test_hue]

        # Apply Spyder Group-style hue adjustments
        adjusted_lch = apply_group_hue_adjustments(test_lch, theme)

        # Generate test candidates
        test_candidates = generate_test_candidates(adjusted_lch, target_delta_e)

        for test_lch in test_candidates:
            # Ensure valid LCH ranges
            test_lch = validate_lch_bounds(test_lch)

            test_hex = lch_to_hex(test_lch[0], test_lch[1], test_lch[2])
            delta_e = calculate_delta_e(current_hex, test_hex)

            if delta_e is not None:
                delta_e_diff = abs(delta_e - target_delta_e)
                if delta_e_diff < best_delta_e_diff:
                    best_delta_e_diff = delta_e_diff
                    best_lch = test_lch.copy()

    return best_lch


def generate_optimal_colors(num_colors=12, theme="dark"):
    """
    Generate colors optimized for maximum distinguishability in variable explorer.

    This method is specifically designed for variable explorer tagging where
    colors need to be easily distinguishable from each other at a glance.

    Args:
        num_colors: Number of colors to generate
        theme: 'dark' or 'light' - determines lightness optimized for background

    Returns:
        List of hex color codes optimized for distinguishability
    """
    # Get theme-optimized parameters
    params = get_theme_parameters(theme)

    # For optimal distinguishability, use maximum hue separation
    hue_step = 360 / num_colors

    # Use high chroma for better visibility and distinguishability
    base_chroma = 80  # Higher than default for better distinction

    colors = []

    for i in range(num_colors):
        # Calculate hue with maximum separation
        hue = (i * hue_step) % 360

        # Use theme-appropriate lightness with some variation
        # Add slight variation to avoid monotony while maintaining distinguishability
        lightness_variation = 5 * math.sin(i * 0.7)  # Small sinusoidal variation
        lightness = params["base_lightness"] + lightness_variation

        # Ensure lightness stays within reasonable bounds
        lightness = max(20, min(80, lightness))

        # Apply hue-specific adjustments for optimal visibility
        adjusted_lch = apply_group_hue_adjustments([lightness, base_chroma, hue], theme)

        # Generate color
        color_hex = lch_to_hex(adjusted_lch[0], adjusted_lch[1], adjusted_lch[2])
        colors.append(color_hex)

    return colors
