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
import re
import unicodedata
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

_logger = logging.getLogger(__name__)


def normalize_color_name_to_safe_ascii(name: str) -> str:
    """Strip API color names down to ASCII letters and digits (valid in Python identifiers).

    Accented letters become their closest ASCII base letters; spaces, punctuation,
    apostrophes, and symbols are removed. Empty input or all-non-ASCII names
    produce an empty string (callers should fall back).
    """
    if not name or not str(name).strip():
        return ""
    nfkd = unicodedata.normalize("NFKD", str(name).strip())
    ascii_only = nfkd.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^A-Za-z0-9]", "", ascii_only)


def _http_user_agent() -> str:
    """Identify this app; api.color.pizza returns 403 for urllib's default User-Agent (Cloudflare)."""
    ver = "0"
    try:
        from importlib.metadata import version

        ver = version("themeweaver")
    except Exception:
        pass
    return f"Themeweaver/{ver} (color names; +https://github.com/conradolandia/spyder-themeweaver)"


try:
    import randomname

    RANDOMNAME_AVAILABLE = True
except ImportError:
    RANDOMNAME_AVAILABLE = False


def get_color_names_from_api(
    hex_colors: List[str], list_type: str = "bestOf", quiet: bool = False
) -> Dict[str, str]:
    """Get color names from the color.pizza API for multiple colors.

    Args:
        hex_colors: List of hex color strings (with or without #)
        list_type: API list type ('bestOf', 'wikipedia', 'ntc', etc.)
        quiet: If True, suppress informational logging

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
        if not quiet:
            _logger.info("🌈 Fetching color names from API...")

        # Make API request (must set User-Agent: default urllib UA is blocked with 403 by Cloudflare)
        request = urllib.request.Request(
            url,
            headers={"User-Agent": _http_user_agent()},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
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

                raw_name = color_info.get("name", "")
                if not hex_value or not raw_name:
                    continue
                safe_name = normalize_color_name_to_safe_ascii(raw_name)
                if not safe_name:
                    # e.g. name was only non-Latin script; keep a deterministic ASCII label
                    hex_digits = hex_value.lstrip("#").upper()
                    safe_name = f"Color{hex_digits}"
                color_names[hex_value] = safe_name

        if not quiet:
            _logger.info("✅ Retrieved %d color names", len(color_names))
        return color_names

    except Exception as e:
        _logger.error("❌ API request failed: %s", e)
        return {}


def get_color_name(hex_color: str, quiet: bool = False) -> Optional[str]:
    """Get the color name for a hex color using the color.pizza API.

    Args:
        hex_color: Hex color string (e.g., "#FF0000")
        quiet: If True, suppress informational logging

    Returns:
        Color name string, or None if not found
    """
    # Normalize hex color
    if not hex_color.startswith("#"):
        hex_color = "#" + hex_color
    hex_color = hex_color.upper()

    # Get color name from API
    result = get_color_names_from_api([hex_color], quiet=quiet)
    return result.get(hex_color)


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


def get_palette_name_from_color(
    hex_color: str, creative: bool = True, quiet: bool = False
) -> str:
    """Get a palette name based on a color, with optional creative adjective prefix.

    Args:
        hex_color: Hex color string (e.g., "#FF0000")
        creative: If True, adds a random adjective prefix (e.g., "BlaringRed")
                 If False, uses just the color name (e.g., "Red")
        quiet: If True, suppress informational logging

    Returns:
        Palette name (cleaned for use in file names)
    """
    color_name = get_color_name(hex_color, quiet=quiet)

    if color_name:
        clean_color_name = normalize_color_name_to_safe_ascii(color_name)
        if not clean_color_name:
            clean_color_name = f"Color{hex_color.replace('#', '').upper()}"

        if creative:
            # Generate random adjective and combine
            adjective = generate_random_adjective()
            palette_name = f"{adjective}{clean_color_name}"
            if not quiet:
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
