"""
Color generation algorithms for themeweaver.

This module provides perceptually uniform color generation using LCH color space
and Delta E spacing for scientifically sound color palettes.
"""

from .color_utils import lch_to_hex, calculate_delta_e


def generate_theme_optimized_colors(
    theme="dark",
    num_colors=12,
    target_delta_e=25,
    start_hue=None,
):
    """
    Generate perceptually uniform color progressions using LCH color space.

    Updated based on Spyder Group palette analysis to include hue-specific adjustments
    for optimal visibility per theme.

    Args:
        theme: 'dark' or 'light' - determines lightness optimized for background
        num_colors: Number of colors to generate
        target_delta_e: Target perceptual distance between consecutive colors
        start_hue: Starting hue in degrees (0-360) or None for default

    Returns:
        List of hex color codes with perceptually uniform spacing
    """

    # Theme-optimized LCH parameters based on Spyder Group palette analysis
    if theme == "dark":
        base_lightness = 58  # From Spyder Group dark palette average (was 70)
        base_chroma = 73  # From Spyder Group dark palette average (was 75)
        default_start_hue = 37  # Close to Spyder Group B10 hue (was 20)
    else:  # light theme
        base_lightness = 65  # From Spyder Group light palette average (was 55)
        base_chroma = 71  # From Spyder Group light palette average (was 80)
        default_start_hue = 53  # Close to Spyder Group B10 hue (was 15)

    actual_start_hue = start_hue if start_hue is not None else default_start_hue
    start_color_lch = [base_lightness, base_chroma, actual_start_hue]

    # Generate colors with uniform perceptual spacing
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


def apply_group_hue_adjustments(lch, theme):
    """
    Apply hue-specific lightness and chroma adjustments based on Spyder Group palette analysis.

    This mimics the intelligent design choices in the original Spyder Group palettes.
    """
    lightness, chroma, hue = lch
    hue = hue % 360

    # Hue-specific adjustments based on Spyder Group palette patterns
    if 0 <= hue < 60:  # Red to Yellow range (like Spyder Group B10, B20)
        if theme == "dark":
            # Spyder Group pattern: high chroma for warm colors on dark backgrounds
            chroma_adj = chroma + 10
            lightness_adj = lightness - 5  # Slightly darker for warmth
        else:
            # Light theme: brighter warm colors
            chroma_adj = chroma + 15
            lightness_adj = lightness + 10

    elif 60 <= hue < 120:  # Yellow to Green range (like Spyder Group B30, B40)
        if theme == "dark":
            chroma_adj = chroma + 5
            lightness_adj = lightness + 8  # Brighter greens/yellows
        else:
            # Very bright yellows for light theme (like Spyder Group B30: L=90.7)
            chroma_adj = chroma + 20
            lightness_adj = lightness + 15

    elif 120 <= hue < 180:  # Green to Cyan range (like Spyder Group B120)
        # Teals/cyans generally brighter with moderate chroma
        chroma_adj = chroma - 10
        lightness_adj = lightness + 8

    elif 180 <= hue < 240:  # Cyan to Blue range (like Spyder Group B50, B60)
        if theme == "dark":
            # Spyder Group pattern: much lower chroma for blues (B50: C=38.4)
            chroma_adj = chroma - 25
            lightness_adj = lightness + 10
        else:
            chroma_adj = chroma - 15
            lightness_adj = lightness + 5

    elif 240 <= hue < 300:  # Blue to Magenta range (like Spyder Group B70, B80)
        if theme == "dark":
            # Spyder Group pattern: darker blues/purples with high chroma
            chroma_adj = chroma + 15
            lightness_adj = lightness - 15
        else:
            # Much darker for light theme (Spyder Group B70: L=39.8)
            chroma_adj = chroma + 5
            lightness_adj = lightness - 20

    else:  # 300-360: Magenta to Red range (like Spyder Group B100, B110)
        if theme == "dark":
            chroma_adj = chroma
            lightness_adj = lightness - 5
        else:
            chroma_adj = chroma - 5
            lightness_adj = lightness - 10

    # Ensure valid LCH ranges
    final_lightness = max(15, min(95, lightness_adj))
    final_chroma = max(20, min(120, chroma_adj))

    return [final_lightness, final_chroma, hue]


def find_next_perceptual_color(
    current_lch, target_delta_e, base_lightness, base_chroma, theme
):
    """Find the next color that achieves the target perceptual distance."""
    current_hex = lch_to_hex(current_lch[0], current_lch[1], current_lch[2])

    best_delta_e_diff = float("inf")
    best_lch = [base_lightness, base_chroma, current_lch[2]]

    # Adaptive search range based on target delta-e
    if target_delta_e < 15:
        hue_range = range(5, 60, 2)  # Fine search for small distances
    elif target_delta_e < 35:
        hue_range = range(10, 120, 3)  # Medium search
    else:
        hue_range = range(20, 180, 5)  # Wide search for large distances

    # Search primarily by hue, with minimal variations
    for hue_increment in hue_range:
        test_hue = (current_lch[2] + hue_increment) % 360
        test_lch = [base_lightness, base_chroma, test_hue]

        # Apply Spyder Group-style hue adjustments
        adjusted_lch = apply_group_hue_adjustments(test_lch, theme)

        # Try the adjusted values first
        test_lch_candidates = [adjusted_lch]

        # Add slight variations only if needed for fine-tuning
        if target_delta_e > 20:
            test_lch_candidates.extend(
                [
                    [adjusted_lch[0] + 3, adjusted_lch[1], adjusted_lch[2]],
                    [adjusted_lch[0] - 3, adjusted_lch[1], adjusted_lch[2]],
                    [adjusted_lch[0], adjusted_lch[1] + 5, adjusted_lch[2]],
                    [adjusted_lch[0], adjusted_lch[1] - 5, adjusted_lch[2]],
                ]
            )

        for test_lch in test_lch_candidates:
            # Ensure valid LCH ranges
            test_lch[0] = max(0, min(100, test_lch[0]))  # Lightness 0-100
            test_lch[1] = max(0, min(120, test_lch[1]))  # Chroma 0-120

            test_hex = lch_to_hex(test_lch[0], test_lch[1], test_lch[2])
            delta_e = calculate_delta_e(current_hex, test_hex)

            if delta_e is not None:
                delta_e_diff = abs(delta_e - target_delta_e)
                if delta_e_diff < best_delta_e_diff:
                    best_delta_e_diff = delta_e_diff
                    best_lch = test_lch.copy()

    return best_lch


def generate_group_uniform_palette(theme="dark", num_colors=12):
    """
    Generate a palette with uniform 30° hue steps, mimicking Spyder Group palette structure
    but with regular progression.

    This provides a good balance between Spyder Group's design principles and mathematical uniformity.
    """

    # Use Spyder Group palette characteristics
    if theme == "dark":
        base_lightness = 58
        base_chroma = 73
        start_hue = 37
    else:
        base_lightness = 65
        base_chroma = 71
        start_hue = 53

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
