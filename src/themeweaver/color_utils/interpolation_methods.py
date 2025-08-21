"""
Pure mathematical interpolation methods.

This module contains various interpolation algorithms that can be used
for any numerical interpolation, including colors, animations, and other
mathematical applications.
"""

import math


def linear_interpolate(start, end, factor):
    """
    Linear interpolation between two values.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value
    """
    return start + (end - start) * factor


def circular_interpolate(start_angle, end_angle, factor):
    """
    Interpolate between two angles (in degrees) taking the shortest circular path.

    Args:
        start_angle: Starting angle in degrees
        end_angle: Ending angle in degrees
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated angle in degrees
    """
    # Normalize angles to 0-360
    start_angle = start_angle % 360
    end_angle = end_angle % 360

    # Calculate the difference
    diff = end_angle - start_angle

    # Take the shortest path around the circle
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360

    # Interpolate and normalize result
    result = (start_angle + diff * factor) % 360
    return result


def cubic_interpolate(start, end, factor):
    """
    Cubic (smooth) interpolation between two values using smoothstep function.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value with smooth acceleration/deceleration
    """
    # Using smoothstep function: 3t² - 2t³
    smooth_factor = factor * factor * (3 - 2 * factor)
    return start + (end - start) * smooth_factor


def exponential_interpolate(start, end, factor, exponent=2):
    """
    Exponential interpolation between two values.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)
        exponent: Exponential power (default: 2)

    Returns:
        Interpolated value with exponential curve
    """
    exp_factor = factor**exponent
    return start + (end - start) * exp_factor


def sine_interpolate(start, end, factor):
    """
    Sine-based interpolation between two values for smooth easing.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value with sine curve easing
    """
    sine_factor = (1 - math.cos(factor * math.pi)) / 2
    return start + (end - start) * sine_factor


def cosine_interpolate(start, end, factor):
    """
    Cosine-based interpolation between two values.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value with cosine curve
    """
    cosine_factor = (1 - math.cos(factor * math.pi)) / 2
    return start + (end - start) * cosine_factor


def hermite_interpolate(start, end, factor):
    """
    Hermite interpolation for smooth curves.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value using Hermite polynomial
    """
    # Hermite basis functions
    h1 = 2 * factor**3 - 3 * factor**2 + 1
    h2 = -2 * factor**3 + 3 * factor**2

    return h1 * start + h2 * end


def quintic_interpolate(start, end, factor):
    """
    Quintic (5th degree polynomial) interpolation for very smooth curves.

    Args:
        start: Starting value
        end: Ending value
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated value with quintic smoothing
    """
    # Quintic smoothstep: 6t⁵ - 15t⁴ + 10t³
    smooth_factor = factor**3 * (factor * (factor * 6 - 15) + 10)
    return start + (end - start) * smooth_factor


def interpolate_colors(start_hex, end_hex, steps, method="linear", exponent=2):
    """
    Interpolate between two hex colors using various methods and color spaces.

    Args:
        start_hex: Starting hex color (e.g., '#FF0000')
        end_hex: Ending hex color (e.g., '#0000FF')
        steps: Number of interpolation steps (including start and end)
        method: Interpolation method - see below for details
        exponent: Exponent for exponential interpolation (default: 2)

    Methods:
        RGB-based (operate directly in RGB color space):
            - linear: Simple linear interpolation
            - cubic: Smooth acceleration/deceleration (smoothstep)
            - exponential: Exponential curve with configurable exponent
            - sine: Sine-based easing curve
            - cosine: Cosine-based easing curve
            - hermite: Hermite polynomial interpolation
            - quintic: Very smooth 5th-degree polynomial

        Color space methods (convert to color space, interpolate, convert back):
            - hsv: Interpolate in HSV space (good for natural color transitions)
            - lch: Interpolate in LCH space (perceptually uniform)

    Returns:
        List of hex color strings with interpolated colors
    """
    from themeweaver.color_utils import (
        hex_to_rgb,
        hsv_to_rgb,
        lch_to_hex,
        rgb_to_hex,
        rgb_to_hsv,
        rgb_to_lch,
    )

    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)

    colors = []

    if method == "hsv":
        # Convert to HSV for more natural color transitions
        start_hsv = rgb_to_hsv(start_rgb)
        end_hsv = rgb_to_hsv(end_rgb)

        for i in range(steps):
            factor = i / (steps - 1) if steps > 1 else 0

            # Interpolate in HSV space with proper hue wrapping
            h = circular_interpolate(start_hsv[0] * 360, end_hsv[0] * 360, factor) / 360
            s = linear_interpolate(start_hsv[1], end_hsv[1], factor)
            v = linear_interpolate(start_hsv[2], end_hsv[2], factor)

            # Convert back to RGB
            rgb = hsv_to_rgb((h, s, v))
            colors.append(rgb_to_hex(rgb))

    elif method == "lch":
        # Convert to LCH for perceptually uniform interpolation
        start_lch = rgb_to_lch(start_rgb)
        end_lch = rgb_to_lch(end_rgb)

        for i in range(steps):
            factor = i / (steps - 1) if steps > 1 else 0

            # Interpolate in LCH space with proper hue wrapping
            lightness = linear_interpolate(start_lch[0], end_lch[0], factor)
            chroma = linear_interpolate(start_lch[1], end_lch[1], factor)
            hue = circular_interpolate(start_lch[2], end_lch[2], factor)

            # Convert back to hex
            colors.append(lch_to_hex(lightness, chroma, hue))

    else:
        # RGB-based methods
        for i in range(steps):
            factor = i / (steps - 1) if steps > 1 else 0

            if method == "linear":
                r = linear_interpolate(start_rgb[0], end_rgb[0], factor)
                g = linear_interpolate(start_rgb[1], end_rgb[1], factor)
                b = linear_interpolate(start_rgb[2], end_rgb[2], factor)
            elif method == "cubic":
                r = cubic_interpolate(start_rgb[0], end_rgb[0], factor)
                g = cubic_interpolate(start_rgb[1], end_rgb[1], factor)
                b = cubic_interpolate(start_rgb[2], end_rgb[2], factor)
            elif method == "exponential":
                r = exponential_interpolate(start_rgb[0], end_rgb[0], factor, exponent)
                g = exponential_interpolate(start_rgb[1], end_rgb[1], factor, exponent)
                b = exponential_interpolate(start_rgb[2], end_rgb[2], factor, exponent)
            elif method == "sine":
                r = sine_interpolate(start_rgb[0], end_rgb[0], factor)
                g = sine_interpolate(start_rgb[1], end_rgb[1], factor)
                b = sine_interpolate(start_rgb[2], end_rgb[2], factor)
            elif method == "cosine":
                r = cosine_interpolate(start_rgb[0], end_rgb[0], factor)
                g = cosine_interpolate(start_rgb[1], end_rgb[1], factor)
                b = cosine_interpolate(start_rgb[2], end_rgb[2], factor)
            elif method == "hermite":
                r = hermite_interpolate(start_rgb[0], end_rgb[0], factor)
                g = hermite_interpolate(start_rgb[1], end_rgb[1], factor)
                b = hermite_interpolate(start_rgb[2], end_rgb[2], factor)
            elif method == "quintic":
                r = quintic_interpolate(start_rgb[0], end_rgb[0], factor)
                g = quintic_interpolate(start_rgb[1], end_rgb[1], factor)
                b = quintic_interpolate(start_rgb[2], end_rgb[2], factor)
            else:
                raise ValueError(f"Unknown interpolation method: {method}")

            colors.append(rgb_to_hex((int(r), int(g), int(b))))

    return colors


def validate_gradient_uniqueness(colors, method="unknown"):
    """
    Validate that a color gradient has no duplicate colors.

    Args:
        colors: List of hex color strings
        method: Interpolation method used (for reporting)

    Returns:
        Tuple of (is_valid, duplicate_info)
    """
    unique_colors = set(colors)
    total_colors = len(colors)
    unique_count = len(unique_colors)

    if unique_count == total_colors:
        return True, {
            "total_colors": total_colors,
            "unique_colors": unique_count,
            "count": 0,
            "indices": [],
        }
    else:
        # Find duplicate indices
        seen = {}
        duplicates = []
        for i, color in enumerate(colors):
            if color in seen:
                duplicates.append((seen[color], i))
            else:
                seen[color] = i

        return False, {
            "total_colors": total_colors,
            "unique_colors": unique_count,
            "count": total_colors - unique_count,
            "indices": duplicates,
        }
