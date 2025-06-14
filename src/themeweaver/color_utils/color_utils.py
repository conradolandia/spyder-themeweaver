"""
Core color utilities for themeweaver.

This module provides fundamental color conversion functions and utilities
that can be shared across different themeweaver tools.
"""

import colorsys

try:
    import colorspacious

    HAS_LCH = True
except ImportError:
    HAS_LCH = False


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
    if not HAS_LCH:
        raise ImportError("colorspacious required for LCH color model")

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
    if not HAS_LCH:
        raise ImportError("colorspacious required for LCH color model")

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
    if not HAS_LCH:
        return None

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


def linear_interpolate(start, end, factor):
    """Linear interpolation between two values."""
    return start + (end - start) * factor


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

    if HAS_LCH:
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
        except (ValueError, TypeError, OverflowError, ImportError):
            info.update(
                {
                    "lch": None,
                    "lch_lightness": None,
                    "lch_chroma": None,
                    "lch_hue": None,
                }
            )

    return info
