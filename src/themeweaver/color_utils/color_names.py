"""
Color names utilities for themeweaver.

This module provides utilities for working with color names using the color.pizza API.
API documentation: https://github.com/meodai/color-names

Example:
>>> from themeweaver.color_utils.color_names import get_color_name
>>> get_color_name("#000000")
'Black'
>>> get_color_name("#FF0000")
'Red'
"""

import json
import logging
import urllib.request
import urllib.parse
from typing import Optional, List, Dict

_logger = logging.getLogger(__name__)

try:
    import randomname

    RANDOMNAME_AVAILABLE = True
except ImportError:
    RANDOMNAME_AVAILABLE = False


def get_color_names_from_api(
    hex_colors: List[str], list_type: str = "bestOf"
) -> Dict[str, str]:
    """Get color names from the color.pizza API for multiple colors.

    Args:
        hex_colors: List of hex color strings (with or without #)
        list_type: API list type ('bestOf', 'wikipedia', 'ntc', etc.)

    Returns:
        Dict mapping hex colors to their names
    """
    if not hex_colors:
        return {}

    # Clean hex colors (remove # and convert to lowercase)
    clean_colors = []
    for color in hex_colors:
        clean_color = color.lstrip("#").lower()
        if len(clean_color) == 6:  # Valid hex color
            clean_colors.append(clean_color)

    if not clean_colors:
        return {}

    # Build API URL
    base_url = "https://api.color.pizza/v1/"
    params = {"values": ",".join(clean_colors), "list": list_type}

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        _logger.info("🌈 Fetching color names from API...")

        # Make API request
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        # Parse response
        color_names = {}
        if "colors" in data:
            for color_info in data["colors"]:
                # Use requestedHex if available, otherwise use hex
                requested_hex = color_info.get("requestedHex", "")
                if not requested_hex:
                    requested_hex = color_info.get("hex", "")

                # Normalize the hex value
                if requested_hex and not requested_hex.startswith("#"):
                    requested_hex = "#" + requested_hex
                hex_value = requested_hex.upper()

                name = color_info.get("name", "")
                if hex_value and name:
                    color_names[hex_value] = name

        _logger.info("✅ Retrieved %d color names", len(color_names))
        return color_names

    except Exception as e:
        _logger.error("❌ API request failed: %s", e)
        return {}


def get_color_name(hex_color: str) -> Optional[str]:
    """Get the color name for a hex color using the color.pizza API.

    Args:
        hex_color: Hex color string (e.g., "#FF0000")

    Returns:
        Color name string, or None if not found
    """
    # Normalize hex color
    if not hex_color.startswith("#"):
        hex_color = "#" + hex_color
    hex_color = hex_color.upper()

    # Get color name from API
    result = get_color_names_from_api([hex_color])
    return result.get(hex_color)


def get_multiple_color_names(hex_colors: List[str]) -> Dict[str, str]:
    """Get color names for multiple colors in a single API call.

    Args:
        hex_colors: List of hex color strings

    Returns:
        Dict mapping hex colors to their names
    """
    return get_color_names_from_api(hex_colors)


def generate_random_adjective() -> str:
    """Generate a random adjective using the randomname library.

    Returns:
        A random adjective, or "Creative" if randomname is not available
    """
    if not RANDOMNAME_AVAILABLE:
        _logger.info("ℹ️  randomname library not available, using fallback adjective")
        return "Creative"

    try:
        # Try different adjective categories for variety
        categories = ["character", "speed", "algorithms", "physics"]
        import random

        category = random.choice(categories)

        adjective = randomname.generate(f"adj/{category}")
        return adjective.title()  # Capitalize first letter

    except Exception as e:
        _logger.warning("⚠️  Failed to generate random adjective: %s", e)
        return "Creative"


def get_palette_name_from_color(hex_color: str, creative: bool = True) -> str:
    """Get a palette name based on a color, with optional creative adjective prefix.

    Args:
        hex_color: Hex color string (e.g., "#FF0000")
        creative: If True, adds a random adjective prefix (e.g., "BlaringRed")
                 If False, uses just the color name (e.g., "Red")

    Returns:
        Palette name (cleaned for use in file names)
    """
    color_name = get_color_name(hex_color)

    if color_name:
        # Clean up the color name
        clean_color_name = color_name.replace(" ", "").replace("-", "").replace("'", "")

        if creative:
            # Generate random adjective and combine
            adjective = generate_random_adjective()
            palette_name = f"{adjective}{clean_color_name}"
            _logger.info("🎨 Generated creative palette name: %s", palette_name)
        else:
            palette_name = clean_color_name

        return palette_name
    else:
        # Fallback to hex color if no name found
        fallback_name = hex_color.replace("#", "")
        if creative:
            adjective = generate_random_adjective()
            return f"{adjective}{fallback_name}"
        else:
            return fallback_name
