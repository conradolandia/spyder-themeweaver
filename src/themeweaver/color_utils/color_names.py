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
import urllib.request
import urllib.parse
from typing import Optional, List, Dict

try:
    import randomname
    RANDOMNAME_AVAILABLE = True
except ImportError:
    RANDOMNAME_AVAILABLE = False


def get_color_names_from_api(hex_colors: List[str], list_type: str = "bestOf") -> Dict[str, str]:
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
    params = {
        "values": ",".join(clean_colors),
        "list": list_type
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        print(f"🌈 Fetching color names from API...")
        
        # Make API request
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        # Parse response
        color_names = {}
        if "colors" in data:
            for color_info in data["colors"]:
                # Use requestedHex if available, otherwise use hex
                requested_hex = color_info.get('requestedHex', '')
                if not requested_hex:
                    requested_hex = color_info.get('hex', '')
                
                # Normalize the hex value
                if requested_hex and not requested_hex.startswith('#'):
                    requested_hex = '#' + requested_hex
                hex_value = requested_hex.upper()
                
                name = color_info.get('name', '')
                if hex_value and name:
                    color_names[hex_value] = name
        
        print(f"✅ Retrieved {len(color_names)} color names")
        return color_names
        
    except Exception as e:
        print(f"❌ API request failed: {e}")
        return {}


def get_color_name(hex_color: str, exact_match_only: bool = False) -> Optional[str]:
    """Get the color name for a hex color using the color.pizza API.
    
    Args:
        hex_color: Hex color string (e.g., "#FF0000")
        exact_match_only: If True, only returns exact matches. 
                         If False, returns closest match (API handles this).
        
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
        print("ℹ️  randomname library not available, using fallback adjective")
        return "Creative"
    
    try:
        # Try different adjective categories for variety
        categories = ['character', 'speed', 'algorithms', 'physics']
        import random
        category = random.choice(categories)
        
        adjective = randomname.generate(f'adj/{category}')
        return adjective.title()  # Capitalize first letter
        
    except Exception as e:
        print(f"⚠️  Failed to generate random adjective: {e}")
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
    color_name = get_color_name(hex_color, exact_match_only=False)
    
    if color_name:
        # Clean up the color name
        clean_color_name = color_name.replace(" ", "").replace("-", "").replace("'", "")
        
        if creative:
            # Generate random adjective and combine
            adjective = generate_random_adjective()
            palette_name = f"{adjective}{clean_color_name}"
            print(f"🎨 Generated creative palette name: {palette_name}")
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


def get_enhanced_palette_name_from_color(hex_color: str) -> str:
    """Get an enhanced palette name with random adjective prefix.
    
    This is a convenience function that always generates creative names.
    
    Args:
        hex_color: Hex color string (e.g., "#FF0000")
        
    Returns:
        Creative palette name like "BlaringRed" or "QuietHaiti"
    """
    return get_palette_name_from_color(hex_color, creative=True)


def calculate_color_distance(hex1: str, hex2: str) -> float:
    """Calculate the Euclidean distance between two hex colors in RGB space.
    
    Args:
        hex1: First hex color (e.g., "#FF0000")
        hex2: Second hex color (e.g., "#00FF00")
        
    Returns:
        Distance between the colors (lower = more similar)
    """
    # Import here to avoid circular imports
    from themeweaver.color_utils import hex_to_rgb
    
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    
    # Calculate Euclidean distance in RGB space
    distance = ((rgb1[0] - rgb2[0]) ** 2 + 
                (rgb1[1] - rgb2[1]) ** 2 + 
                (rgb1[2] - rgb2[2]) ** 2) ** 0.5
    
    return distance


# Legacy functions for backward compatibility
def download_color_names(filename="colornames.yaml"):
    """Legacy function - now uses API instead of file download.
    
    Args:
        filename: Ignored, kept for compatibility
    """
    print("ℹ️  Note: Color names are now fetched from API, no file download needed")


def check_color_names_file(filename="colornames.yaml"):
    """Legacy function - now uses API instead of file checking.
    
    Args:
        filename: Ignored, kept for compatibility
    """
    # No-op since we use API now
    pass
