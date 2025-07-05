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


def is_color_dark(hex_color, threshold=35.0):
    """
    Determine if a color is considered "dark" or "light" using LCh lightness.

    Uses the perceptually uniform LCh color space where the lightness component
    directly corresponds to how light or dark a color appears to human vision.

    This function provides a simple binary classification with customizable threshold.
    For more robust theme generation, consider using classify_color_lightness()
    which provides a three-stage classification (dark/medium/light).

    Args:
        hex_color (str): Hex color string (e.g., "#FF0000")
        threshold (float): Lightness threshold (0-100). Colors below this are dark.
                          Default is 35.0 (aligned with enhanced classification)

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


def classify_color_lightness(hex_color, dark_threshold=35.0, light_threshold=65.0):
    """
    Classify a color as dark, medium, or light using LCh lightness.

    This provides more robust classification for theme generation where we need
    clearly distinguishable dark and light colors.

    Args:
        hex_color (str): Hex color string (e.g., "#FF0000")
        dark_threshold (float): Upper bound for dark colors (0-100). Default 35.0
        light_threshold (float): Lower bound for light colors (0-100). Default 65.0

    Returns:
        str: "dark", "medium", or "light"

    Raises:
        ValueError: If the hex color is invalid or thresholds are invalid

    Examples:
        >>> classify_color_lightness("#000000")  # Black, L=0
        'dark'
        >>> classify_color_lightness("#FFFFFF")  # White, L=100
        'light'
        >>> classify_color_lightness("#808080")  # Medium gray, L≈53
        'medium'
        >>> classify_color_lightness("#002B36")  # Dark blue, L≈15
        'dark'
        >>> classify_color_lightness("#EEE8D5")  # Light beige, L≈90
        'light'
    """
    # Validate thresholds
    if not 0 <= dark_threshold <= 100:
        raise ValueError(f"dark_threshold must be 0-100, got {dark_threshold}")
    if not 0 <= light_threshold <= 100:
        raise ValueError(f"light_threshold must be 0-100, got {light_threshold}")
    if dark_threshold >= light_threshold:
        raise ValueError(
            f"dark_threshold ({dark_threshold}) must be < light_threshold ({light_threshold})"
        )

    # Validate hex_color
    if not isinstance(hex_color, str):
        raise ValueError(f"Hex color must be a string, got {type(hex_color)}")
    if not hex_color.startswith("#"):
        raise ValueError(f"Hex color must start with '#', got: {hex_color}")

    try:
        rgb = hex_to_rgb(hex_color)
        lightness, _, _ = rgb_to_lch(rgb)

        if lightness < dark_threshold:
            return "dark"
        elif lightness > light_threshold:
            return "light"
        else:
            return "medium"

    except (ValueError, TypeError, OverflowError):
        # Fallback: if LCh conversion fails, use RGB luminance approximation
        rgb = hex_to_rgb(hex_color)  # This will raise ValueError for invalid hex
        # Calculate relative luminance (ITU-R BT.709)
        r, g, b = [c / 255.0 for c in rgb]
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        # Convert to approximate LCh lightness scale (0-100)
        approx_lightness = luminance * 100

        if approx_lightness < dark_threshold:
            return "dark"
        elif approx_lightness > light_threshold:
            return "light"
        else:
            return "medium"


def is_color_suitable_for_theme(hex_color, role="dark"):
    """
    Check if a color is suitable for a specific role in theme generation.

    This is more strict than simple dark/light classification, ensuring colors
    are clearly distinguishable and will work well in theme contexts.

    Args:
        hex_color (str): Hex color string (e.g., "#FF0000")
        role (str): Expected role - "dark" or "light"

    Returns:
        bool: True if the color is suitable for the specified role

    Raises:
        ValueError: If the hex color is invalid or role is not recognized

    Examples:
        >>> is_color_suitable_for_theme("#000000", "dark")  # Black
        True
        >>> is_color_suitable_for_theme("#808080", "dark")  # Medium gray
        False
        >>> is_color_suitable_for_theme("#FFFFFF", "light")  # White
        True
        >>> is_color_suitable_for_theme("#808080", "light")  # Medium gray
        False
    """
    if role not in ("dark", "light"):
        raise ValueError(f"Role must be 'dark' or 'light', got: {role}")

    classification = classify_color_lightness(hex_color)
    return classification == role


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
