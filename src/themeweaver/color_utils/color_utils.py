"""
Core color utilities for themeweaver.

This module provides fundamental color conversion functions and utilities
that can be shared across different themeweaver tools.

CIELab vs CIELCh Usage:
    CIELab [L*, a*, b*] - Cartesian coordinates:
        • Used for: Delta E color difference calculations
        • Why: Mathematical distance formulas require a*, b* components
        • Functions: calculate_delta_e()

    CIELCh [L*, C*, h*] - Cylindrical coordinates:
        • Used for: Human-friendly color manipulation and analysis
        • Why: Intuitive control of lightness, chroma, and hue independently
        • Functions: rgb_to_lch(), lch_to_hex(), is_color_dark()

    Both represent identical colors in different coordinate systems,
    optimized for their respective use cases.
"""

import colorsys
from typing import List, Optional, Tuple

import colorspacious


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex to RGB (0-255)."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: #{hex_color}. Must be 6 characters.")
    try:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(
            f"Invalid hex color: #{hex_color}. Must contain only hex digits."
        )


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB to hex."""
    return "#{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    """Convert RGB (0-255) to HSV (0-1)."""
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)


def hsv_to_rgb(hsv: Tuple[float, float, float]) -> Tuple[int, int, int]:
    """Convert HSV (0-1) to RGB (0-255)."""
    r, g, b = colorsys.hsv_to_rgb(*hsv)
    return tuple(int(x * 255) for x in (r, g, b))


def lch_to_hex(lightness: float, chroma: float, hue: float) -> str:
    """Convert LCH to hex color."""

    # Convert LCH to sRGB
    try:
        rgb = colorspacious.cspace_convert([lightness, chroma, hue], "CIELCh", "sRGB1")
        # Clamp RGB values to valid range
        rgb = [max(0, min(1, component)) for component in rgb]
        return rgb_to_hex(tuple(int(c * 255) for c in rgb))
    except (ValueError, TypeError, OverflowError):
        # Fallback for out-of-gamut colors or invalid inputs
        return "#808080"  # Gray fallback


def rgb_to_lch(rgb: Tuple[int, int, int]) -> List[float]:
    """Convert RGB (0-255) to LCH."""

    # Normalize RGB to 0-1 range
    rgb_norm = [c / 255.0 for c in rgb]
    try:
        return colorspacious.cspace_convert(rgb_norm, "sRGB1", "CIELCh")
    except (ValueError, TypeError, OverflowError):
        return [50, 0, 0]  # Fallback to neutral gray


def calculate_delta_e(color1_hex: str, color2_hex: str) -> Optional[float]:
    """
    Calculate perceptual color difference (Delta E) between two hex colors.

    Delta E interpretation:
    - < 1: Not perceptible by human eyes
    - 1-2: Perceptible through close observation
    - 2-10: Perceptible at a glance
    - 11-49: Colors are more similar than opposite
    - > 50: Colors are exact opposite
    """

    try:
        rgb1 = [c / 255.0 for c in hex_to_rgb(color1_hex)]
        rgb2 = [c / 255.0 for c in hex_to_rgb(color2_hex)]

        lab1 = colorspacious.cspace_convert(rgb1, "sRGB1", "CIELab")
        lab2 = colorspacious.cspace_convert(rgb2, "sRGB1", "CIELab")

        # Calculate Delta E CIE 2000 (most accurate)
        delta_e = colorspacious.deltaE(lab1, lab2, input_space="CIELab")
        return delta_e
    except (ValueError, TypeError, OverflowError):
        return None


def get_color_info(hex_color: str) -> dict:
    """
    Get color information for a hex color.

    Returns:
        dict: Color information including RGB, HSV, and LCH values
    """
    rgb = hex_to_rgb(hex_color)
    hsv = rgb_to_hsv(rgb)

    info = {
        "hex": hex_color,
        "rgb": rgb,
        "hsv": hsv,
        "hsv_degrees": (hsv[0] * 360, hsv[1], hsv[2]),
    }

    try:
        lightness, chroma, hue_lch = rgb_to_lch(rgb)
        info.update(
            {
                "lch": (lightness, chroma, hue_lch),
                "lch_lightness": lightness,
                "lch_chroma": chroma,
                "lch_hue": hue_lch,
            }
        )
    except (ValueError, TypeError, OverflowError):
        info.update(
            {
                "lch": None,
                "lch_lightness": None,
                "lch_chroma": None,
                "lch_hue": None,
            }
        )

    return info


def is_color_dark(hex_color: str, threshold: float = 35.0) -> bool:
    """
    Determine if a color is considered "dark" or "light" using LCh lightness.

    Uses the perceptually uniform LCh color space where the lightness component
    directly corresponds to how light or dark a color appears to human vision.

    Args:
        hex_color (str): Hex color string (e.g., "#FF0000")
        threshold (float): Lightness threshold (0-100). Colors below this are dark.
                          Default is 35.0

    Returns:
        bool: True if the color is dark, False if it's light

    Raises:
        ValueError: If the hex color is invalid

    Examples:
        >>> is_color_dark("#000000")  # Black, L=0
        True
        >>> is_color_dark("#FFFFFF")  # White, L=100
        False
        >>> is_color_dark("#808080")  # Medium gray, L≈54
        False
        >>> is_color_dark("#404040")  # Dark gray, L≈27
        True
        >>> is_color_dark("#FF0000", threshold=50.0)  # Custom threshold
        True
    """
    try:
        rgb = hex_to_rgb(hex_color)
        lightness, _, _ = rgb_to_lch(rgb)
        return bool(lightness < threshold)
    except (ValueError, TypeError, OverflowError):
        # Fallback: if LCh conversion fails, use RGB luminance approximation
        rgb = hex_to_rgb(hex_color)  # This will raise ValueError for invalid hex
        # Calculate relative luminance (ITU-R BT.709)
        r, g, b = [c / 255.0 for c in rgb]
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        # Convert to approximate LCh lightness scale (0-100)
        approx_lightness = luminance * 100
        return bool(approx_lightness < threshold)


def is_lch_in_gamut(lightness: float, chroma: float, hue: float) -> bool:
    """
    Determines if an LCH color is within the sRGB gamut.

    Args:
        lightness: L* value (0-100)
        chroma: C* value (0+)
        hue: h° value (0-360)

    Returns:
        bool: True if color is within sRGB gamut, False if outside
    """
    # Special case for pure black and white (avoid conversion issues at extremes)
    if chroma == 0 and (lightness == 0 or lightness == 100):
        return True

    try:
        rgb = colorspacious.cspace_convert([lightness, chroma, hue], "CIELCh", "sRGB1")
        return all(0 <= component <= 1 for component in rgb)
    except (ValueError, TypeError, OverflowError):
        return False


def find_max_in_gamut_chroma(
    lightness: float, hue: float, precision: float = 0.5
) -> float:
    """
    Finds the maximum chroma value that keeps the color within sRGB gamut.

    Args:
        lightness: L* value (0-100)
        hue: h° value (0-360)
        precision: Precision of the binary search

    Returns:
        float: Maximum chroma value that keeps the color in gamut
    """
    low = 0
    high = 150  # Reasonable starting maximum

    # If maximum is in gamut, increase until we find the limit
    if is_lch_in_gamut(lightness, high, hue):
        while is_lch_in_gamut(lightness, high, hue):
            high *= 2

    # Binary search for the maximum value
    while high - low > precision:
        mid = (low + high) / 2
        if is_lch_in_gamut(lightness, mid, hue):
            low = mid
        else:
            high = mid

    return low


def adjust_lch_to_gamut(
    lightness: float, chroma: float, hue: float, preserve: str = "lightness"
) -> Tuple[float, float, float]:
    """
    Adjusts an LCH color to be within the sRGB gamut.

    Args:
        lightness: L* value (0-100)
        chroma: C* value (0+)
        hue: h° value (0-360)
        preserve: What to preserve ("lightness", "chroma", or "both")

    Returns:
        tuple: (lightness, chroma, hue) adjusted to be within gamut
    """
    if is_lch_in_gamut(lightness, chroma, hue):
        return (lightness, chroma, hue)

    if preserve == "lightness":
        # Reduce chroma until in gamut
        return (lightness, find_max_in_gamut_chroma(lightness, hue), hue)
    elif preserve == "chroma":
        # Adjust lightness (simplified implementation)
        # Look for nearby L that allows the given chroma
        for l_offset in range(1, 50):
            for direction in [1, -1]:
                new_l = lightness + l_offset * direction
                if 0 <= new_l <= 100 and is_lch_in_gamut(new_l, chroma, hue):
                    return (new_l, chroma, hue)
        # If we can't find one, fall back to preserving lightness
        return (lightness, find_max_in_gamut_chroma(lightness, hue), hue)
    else:  # "both" - try to adjust both minimally
        # Simplified implementation
        return (lightness, find_max_in_gamut_chroma(lightness, hue), hue)


def calculate_std_dev(values: List[float]) -> float:
    """Calculate standard deviation of a list of values."""
    if not values:
        return 0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance**0.5
