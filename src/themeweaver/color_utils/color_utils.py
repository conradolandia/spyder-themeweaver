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
import colorspacious


def hex_to_rgb(hex_color):
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


def rgb_to_hex(rgb):
    """Convert RGB to hex."""
    return "#{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def hsv_to_hex(hue, saturation, value):
    """Convert HSV to hex color."""
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return rgb_to_hex(tuple(int(c * 255) for c in rgb))


def rgb_to_hsv(rgb):
    """Convert RGB (0-255) to HSV (0-1)."""
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)


def hsv_to_rgb(hsv):
    """Convert HSV (0-1) to RGB (0-255)."""
    r, g, b = colorsys.hsv_to_rgb(*hsv)
    return tuple(int(x * 255) for x in (r, g, b))


def lch_to_hex(lightness, chroma, hue):
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


def rgb_to_lch(rgb):
    """Convert RGB (0-255) to LCH."""

    # Normalize RGB to 0-1 range
    rgb_norm = [c / 255.0 for c in rgb]
    try:
        return colorspacious.cspace_convert(rgb_norm, "sRGB1", "CIELCh")
    except (ValueError, TypeError, OverflowError):
        return [50, 0, 0]  # Fallback to neutral gray


def calculate_delta_e(color1_hex, color2_hex):
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


def get_color_info(hex_color):
    """
    Get comprehensive color information for a hex color.

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


def is_color_dark(hex_color, threshold=50.0):
    """
    Determine if a color is considered "dark" or "light" using LCh lightness.

    Uses the perceptually uniform LCh color space where the lightness component
    directly corresponds to how light or dark a color appears to human vision.

    Args:
        hex_color (str): Hex color string (e.g., "#FF0000")
        threshold (float): Lightness threshold (0-100). Colors below this are dark.
                          Default is 50.0 (middle lightness)

    Returns:
        bool: True if the color is dark, False if it's light

    Raises:
        ValueError: If the hex color is invalid

    Examples:
        >>> is_color_dark("#000000")  # Black
        True
        >>> is_color_dark("#FFFFFF")  # White
        False
        >>> is_color_dark("#FF0000")  # Red (depends on threshold)
        True
        >>> is_color_dark("#FF0000", threshold=30.0)  # Lower threshold
        False
    """
    # Validate hex_color first to ensure proper error handling
    if not isinstance(hex_color, str):
        raise ValueError(f"Hex color must be a string, got {type(hex_color)}")

    if not hex_color.startswith("#"):
        raise ValueError(f"Hex color must start with '#', got: {hex_color}")

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


def get_color_brightness_info(hex_color):
    """
    Get detailed brightness information for a color using multiple methods.

    Args:
        hex_color (str): Hex color string (e.g., "#FF0000")

    Returns:
        dict: Brightness information including:
            - lch_lightness: LCh lightness (0-100, perceptually uniform)
            - rgb_luminance: RGB relative luminance (0-1, ITU-R BT.709)
            - hsv_value: HSV value component (0-1)
            - is_dark_lch: Whether color is dark using LCh (threshold 50)
            - is_dark_luminance: Whether color is dark using RGB luminance (threshold 0.5)

    Example:
        >>> info = get_color_brightness_info("#FF0000")
        >>> print(f"Red lightness: {info['lch_lightness']:.1f}")
        >>> print(f"Is dark: {info['is_dark_lch']}")
    """
    rgb = hex_to_rgb(hex_color)
    hsv = rgb_to_hsv(rgb)

    # Calculate LCh lightness
    try:
        lightness, _, _ = rgb_to_lch(rgb)
    except (ValueError, TypeError, OverflowError):
        lightness = None

    # Calculate RGB relative luminance (ITU-R BT.709)
    r, g, b = [c / 255.0 for c in rgb]
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    return {
        "hex": hex_color,
        "lch_lightness": lightness,
        "rgb_luminance": luminance,
        "hsv_value": hsv[2],
        "is_dark_lch": bool(is_color_dark(hex_color, threshold=50.0))
        if lightness is not None
        else None,
        "is_dark_luminance": bool(luminance < 0.5),
        "is_dark_hsv": bool(hsv[2] < 0.5),
    }
