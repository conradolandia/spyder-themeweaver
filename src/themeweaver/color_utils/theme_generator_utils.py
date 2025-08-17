"""
Theme generation utilities for ThemeWeaver.

This module provides functions for generating complete themes from individual colors,
including validation and theme structure creation.
"""

import re
from themeweaver.color_utils import (
    hex_to_rgb,
    rgb_to_lch,
)
from themeweaver.color_utils.palette_generators import (
    generate_spyder_palette_from_color,
    generate_group_palettes,
)


def generate_theme_from_colors(primary_color, secondary_color, red_color, green_color, orange_color, group_initial_color, logos=None):
    """
    Generates a complete theme from individual colors.
    
    Args:
        primary_color: Hex color for the Primary palette
        secondary_color: Hex color for the Secondary palette
        red_color: Hex color for the Red palette
        green_color: Hex color for the Green palette
        orange_color: Hex color for the Orange palette
        group_initial_color: Initial color for GroupDark/GroupLight palettes
        logos: Dictionary with colors for the Logos palette (optional)
        
    Returns:
        dict: Complete theme structure with colorsystem and mappings
    """
    from themeweaver.color_utils.color_names import get_multiple_color_names, generate_random_adjective
    
    # Generate main palettes
    primary_palette = generate_spyder_palette_from_color(primary_color)
    secondary_palette = generate_spyder_palette_from_color(secondary_color)
    red_palette = generate_spyder_palette_from_color(red_color)
    green_palette = generate_spyder_palette_from_color(green_color)
    orange_palette = generate_spyder_palette_from_color(orange_color)
    
    # Get all color names in a single API call
    all_colors = [primary_color, secondary_color, red_color, green_color, orange_color, group_initial_color]
    color_names = get_multiple_color_names(all_colors)
    
    # Generate creative names for palettes using the retrieved names
    def get_creative_name(color):
        # Normalize color to match API response format (uppercase)
        normalized_color = color.upper()
        color_name = color_names.get(normalized_color)
        if color_name:
            # Clean up the color name
            clean_color_name = color_name.replace(" ", "").replace("-", "").replace("'", "")
            # Generate random adjective
            adjective = generate_random_adjective()
            return f"{adjective}{clean_color_name}"
        else:
            # Fallback to hex color if no name found
            fallback_name = color.replace("#", "")
            adjective = generate_random_adjective()
            return f"{adjective}{fallback_name}"
    
    primary_name = get_creative_name(primary_color)
    secondary_name = get_creative_name(secondary_color)
    red_name = get_creative_name(red_color)
    green_name = get_creative_name(green_color)
    orange_name = get_creative_name(orange_color)
    group_base_name = get_creative_name(group_initial_color)
    group_dark_name = group_base_name + "Dark"
    group_light_name = group_base_name + "Light"
    
    # Build colorsystem with creative names
    colorsystem = {}
    colorsystem[primary_name] = {f"B{i*10}": primary_palette[i] for i in range(16)}
    colorsystem[secondary_name] = {f"B{i*10}": secondary_palette[i] for i in range(16)}
    colorsystem[red_name] = {f"B{i*10}": red_palette[i] for i in range(16)}
    colorsystem[green_name] = {f"B{i*10}": green_palette[i] for i in range(16)}
    colorsystem[orange_name] = {f"B{i*10}": orange_palette[i] for i in range(16)}
    
    # Generate group palettes
    group_dark, group_light = generate_group_palettes(group_initial_color)
    colorsystem[group_dark_name] = group_dark
    colorsystem[group_light_name] = group_light
    
    # Add Logos palette
    if logos:
        colorsystem["Logos"] = logos
    else:
        # Default values
        colorsystem["Logos"] = {
            "B10": "#3775a9",  # Python blue
            "B20": "#ffd444",  # Python yellow
            "B30": "#414141",  # Dark gray
            "B40": "#fafafa",  # Light gray
            "B50": "#ee0000"   # Red
        }
    
    # Build mappings to connect semantic names with creative palette names
    mappings = {
        "color_classes": {
            "Primary": primary_name,
            "Secondary": secondary_name,
            "Green": green_name,
            "Red": red_name,
            "Orange": orange_name,
            "GroupDark": group_dark_name,
            "GroupLight": group_light_name,
            "Logos": "Logos"
        },
        "semantic_mappings": {
            "dark": {
                # Background colors
                "COLOR_BACKGROUND_1": "Primary.B10",
                "COLOR_BACKGROUND_2": "Primary.B20",
                "COLOR_BACKGROUND_3": "Primary.B30",
                "COLOR_BACKGROUND_4": "Primary.B20",
                "COLOR_BACKGROUND_5": "Primary.B40",
                "COLOR_BACKGROUND_6": "Primary.B50",
                
                # Text colors
                "COLOR_TEXT_1": "Primary.B130",
                "COLOR_TEXT_2": "Primary.B120",
                "COLOR_TEXT_3": "Primary.B110",
                "COLOR_TEXT_4": "Primary.B100",
                
                # Accent colors
                "COLOR_ACCENT_1": "Secondary.B10",
                "COLOR_ACCENT_2": "Secondary.B20",
                "COLOR_ACCENT_3": "Secondary.B30",
                "COLOR_ACCENT_4": "Secondary.B40",
                "COLOR_ACCENT_5": "Secondary.B50",
                
                # Disabled elements
                "COLOR_DISABLED": "Primary.B70",
                
                # Success colors
                "COLOR_SUCCESS_1": "Green.B40",
                "COLOR_SUCCESS_2": "Green.B70",
                "COLOR_SUCCESS_3": "Green.B90",
                
                # Error colors
                "COLOR_ERROR_1": "Red.B40",
                "COLOR_ERROR_2": "Red.B70",
                "COLOR_ERROR_3": "Red.B110",
                
                # Warning colors
                "COLOR_WARN_1": "Orange.B40",
                "COLOR_WARN_2": "Orange.B70",
                "COLOR_WARN_3": "Orange.B90",
                "COLOR_WARN_4": "Orange.B100",
                
                # Icon colors
                "ICON_1": "Primary.B140",
                "ICON_2": "Secondary.B80",
                "ICON_3": "Green.B80",
                "ICON_4": "Red.B70",
                "ICON_5": "Orange.B70",
                "ICON_6": "Primary.B30",
                
                # Group colors
                "GROUP_1": "GroupDark.B10",
                "GROUP_2": "GroupDark.B20",
                "GROUP_3": "GroupDark.B30",
                "GROUP_4": "GroupDark.B40",
                "GROUP_5": "GroupDark.B50",
                "GROUP_6": "GroupDark.B60",
                "GROUP_7": "GroupDark.B70",
                "GROUP_8": "GroupDark.B80",
                "GROUP_9": "GroupDark.B90",
                "GROUP_10": "GroupDark.B100",
                "GROUP_11": "GroupDark.B110",
                "GROUP_12": "GroupDark.B120",
                
                # Highlight colors
                "COLOR_HIGHLIGHT_1": "Secondary.B10",
                "COLOR_HIGHLIGHT_2": "Secondary.B20",
                "COLOR_HIGHLIGHT_3": "Secondary.B30",
                "COLOR_HIGHLIGHT_4": "Secondary.B50",
                
                # Occurrence colors
                "COLOR_OCCURRENCE_1": "Primary.B10",
                "COLOR_OCCURRENCE_2": "Primary.B20",
                "COLOR_OCCURRENCE_3": "Primary.B30",
                "COLOR_OCCURRENCE_4": "Primary.B50",
                "COLOR_OCCURRENCE_5": "Primary.B80",
                
                # Logo colors
                "PYTHON_LOGO_UP": "Logos.B10",
                "PYTHON_LOGO_DOWN": "Logos.B20",
                "SPYDER_LOGO_BACKGROUND": "Logos.B30",
                "SPYDER_LOGO_WEB": "Logos.B40",
                "SPYDER_LOGO_SNAKE": "Logos.B50",
                
                # Special tabs
                "SPECIAL_TABS_SEPARATOR": "Primary.B70",
                "SPECIAL_TABS_SELECTED": "Secondary.B20",
                
                # For the heart used to ask for donations
                "COLOR_HEART": "Secondary.B80",
                
                # For editor tooltips
                "TIP_TITLE_COLOR": "Green.B80",
                "TIP_CHAR_HIGHLIGHT_COLOR": "Orange.B90",
                
                # Tooltip opacity (numeric value, not a color reference)
                "OPACITY_TOOLTIP": 230
            },
            "light": {
                # Background colors
                "COLOR_BACKGROUND_1": "Primary.B140",
                "COLOR_BACKGROUND_2": "Primary.B130",
                "COLOR_BACKGROUND_3": "Primary.B120",
                "COLOR_BACKGROUND_4": "Primary.B130",
                "COLOR_BACKGROUND_5": "Primary.B110",
                "COLOR_BACKGROUND_6": "Primary.B100",
                
                # Text colors
                "COLOR_TEXT_1": "Primary.B20",
                "COLOR_TEXT_2": "Primary.B30",
                "COLOR_TEXT_3": "Primary.B40",
                "COLOR_TEXT_4": "Primary.B50",
                
                # Accent colors
                "COLOR_ACCENT_1": "Secondary.B140",
                "COLOR_ACCENT_2": "Secondary.B130",
                "COLOR_ACCENT_3": "Secondary.B120",
                "COLOR_ACCENT_4": "Secondary.B110",
                "COLOR_ACCENT_5": "Secondary.B100",
                
                # Disabled elements
                "COLOR_DISABLED": "Primary.B80",
                
                # Success colors
                "COLOR_SUCCESS_1": "Green.B110",
                "COLOR_SUCCESS_2": "Green.B80",
                "COLOR_SUCCESS_3": "Green.B60",
                
                # Error colors
                "COLOR_ERROR_1": "Red.B110",
                "COLOR_ERROR_2": "Red.B80",
                "COLOR_ERROR_3": "Red.B40",
                
                # Warning colors
                "COLOR_WARN_1": "Orange.B110",
                "COLOR_WARN_2": "Orange.B80",
                "COLOR_WARN_3": "Orange.B60",
                "COLOR_WARN_4": "Orange.B50",
                
                # Icon colors
                "ICON_1": "Primary.B10",
                "ICON_2": "Secondary.B70",
                "ICON_3": "Green.B70",
                "ICON_4": "Red.B80",
                "ICON_5": "Orange.B80",
                "ICON_6": "Primary.B120",
                
                # Group colors
                "GROUP_1": "GroupLight.B10",
                "GROUP_2": "GroupLight.B20",
                "GROUP_3": "GroupLight.B30",
                "GROUP_4": "GroupLight.B40",
                "GROUP_5": "GroupLight.B50",
                "GROUP_6": "GroupLight.B60",
                "GROUP_7": "GroupLight.B70",
                "GROUP_8": "GroupLight.B80",
                "GROUP_9": "GroupLight.B90",
                "GROUP_10": "GroupLight.B100",
                "GROUP_11": "GroupLight.B110",
                "GROUP_12": "GroupLight.B120",
                
                # Highlight colors
                "COLOR_HIGHLIGHT_1": "Secondary.B140",
                "COLOR_HIGHLIGHT_2": "Secondary.B130",
                "COLOR_HIGHLIGHT_3": "Secondary.B120",
                "COLOR_HIGHLIGHT_4": "Secondary.B100",
                
                # Occurrence colors
                "COLOR_OCCURRENCE_1": "Primary.B140",
                "COLOR_OCCURRENCE_2": "Primary.B130",
                "COLOR_OCCURRENCE_3": "Primary.B120",
                "COLOR_OCCURRENCE_4": "Primary.B100",
                "COLOR_OCCURRENCE_5": "Primary.B70",
                
                # Logo colors
                "PYTHON_LOGO_UP": "Logos.B10",
                "PYTHON_LOGO_DOWN": "Logos.B20",
                "SPYDER_LOGO_BACKGROUND": "Logos.B30",
                "SPYDER_LOGO_WEB": "Logos.B40",
                "SPYDER_LOGO_SNAKE": "Logos.B50",
                
                # Special tabs
                "SPECIAL_TABS_SEPARATOR": "Primary.B80",
                "SPECIAL_TABS_SELECTED": "Secondary.B130",
                
                # For the heart used to ask for donations
                "COLOR_HEART": "Red.B70",
                
                # For editor tooltips
                "TIP_TITLE_COLOR": "Green.B30",
                "TIP_CHAR_HIGHLIGHT_COLOR": "Orange.B40",
                
                # Tooltip opacity (numeric value, not a color reference)
                "OPACITY_TOOLTIP": 230
            }
        }
    }
    
    return {
        "colorsystem": colorsystem,
        "mappings": mappings
    }


def validate_input_colors(primary, secondary, red, green, orange, group):
    """
    Validates that input colors are suitable for theme generation.
    
    Args:
        primary, secondary, red, green, orange, group: Hex colors
        
    Returns:
        tuple: (is_valid, error_message)
    """
    colors = {
        "primary": primary,
        "secondary": secondary,
        "red": red,
        "green": green,
        "orange": orange,
        "group": group
    }
    
    for name, color in colors.items():
        # Check hex format
        if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
            return False, f"The {name} color ({color}) is not a valid hex format (#RRGGBB)"
        
        # Convert to LCH
        rgb = hex_to_rgb(color)
        lightness, chroma, hue = rgb_to_lch(rgb)
        
        # Check lightness and chroma
        if lightness < 10:
            return False, f"The {name} color ({color}) is too dark (L={lightness:.1f})"
        elif lightness > 90:
            return False, f"The {name} color ({color}) is too light (L={lightness:.1f})"
        # Allow low saturation colors (including grays with chroma = 0)
        # Only warn for very low saturation that might not be intentional
        elif chroma < 5 and chroma > 0:
            # This is a very low saturation color, but still valid
            # We could add a warning here if needed, but don't reject it
            pass
            
    return True, ""
