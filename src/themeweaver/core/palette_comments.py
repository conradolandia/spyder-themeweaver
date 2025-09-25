"""
Palette comments for ThemeWeaver.

This module provides the comments for palette attributes to be used in generated palette.py files.
"""

# Define comment groups for palette attributes
PALETTE_COMMENT_GROUPS = {
    # Background colors
    "COLOR_BACKGROUND_": "# Background colors",
    # Text colors
    "COLOR_TEXT_": "# Text colors",
    # Accent colors
    "COLOR_ACCENT_": "# Accent colors",
    # Disabled elements
    "COLOR_DISABLED": "# Disabled elements",
    # Success colors
    "COLOR_SUCCESS_": "# Success colors",
    # Error colors
    "COLOR_ERROR_": "# Error colors",
    # Warning colors
    "COLOR_WARN_": "# Warning colors",
    # Icon colors
    "ICON_": "# Icon colors",
    # Group colors
    "GROUP_": "# Group colors",
    # Highlight colors
    "COLOR_HIGHLIGHT_": "# Highlight colors",
    # Occurrence colors
    "COLOR_OCCURRENCE_": "# Occurrence colors",
    # Syntax highlighting colors
    "EDITOR_": "# Syntax highlighting colors",
    # Logo colors
    "PYTHON_LOGO_": "# Logo colors",
    "SPYDER_LOGO_": "# Logo colors",
    # Special tabs
    "SPECIAL_TABS_": "# Special tabs",
    # For the heart used to ask for donations
    "COLOR_HEART": "# For the heart used to ask for donations",
    # For editor tooltips
    "TIP_": "# For editor tooltips",
    # Tooltip opacity
    "OPACITY_TOOLTIP": "# Tooltip opacity (numeric value, not a color reference)",
    # Border radius
    "SIZE_": "# Border radius",
    # Borders
    "BORDER_": "# Borders",
    "BORDER_SELECTION_": "# Border selections",
    # Widget specific variables
    "W_": "# Widget specific variables",
    # Paths
    "PATH_": "# Paths",
}


def get_comment_for_attribute(attr_name):
    """
    Get the comment for a given attribute name.

    Args:
        attr_name: The attribute name to get the comment for

    Returns:
        str: The comment for the attribute, or None if not found
    """
    for prefix, comment in PALETTE_COMMENT_GROUPS.items():
        if attr_name.startswith(prefix):
            return comment
    return None
