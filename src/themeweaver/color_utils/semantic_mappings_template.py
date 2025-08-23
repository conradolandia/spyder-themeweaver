"""
Semantic mappings template for ThemeWeaver.

This module contains the template for semantic UI mappings used in theme generation.
The template uses generic palette names (Primary, Secondary, etc.) that get resolved
to actual palette names during theme generation.
"""


def get_semantic_mappings_template():
    """
    Returns the semantic mappings template for both dark and light variants.

    Returns:
        dict: Template with semantic mappings using generic palette names
    """
    return {
        "dark": {
            # Background colors
            "COLOR_BACKGROUND_1": "Primary.B10",
            "COLOR_BACKGROUND_2": "Primary.B20",
            "COLOR_BACKGROUND_3": "Primary.B30",
            "COLOR_BACKGROUND_4": "Primary.B40",
            "COLOR_BACKGROUND_5": "Primary.B50",
            "COLOR_BACKGROUND_6": "Primary.B60",
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
            "COLOR_SUCCESS_1": "Success.B40",
            "COLOR_SUCCESS_2": "Success.B70",
            "COLOR_SUCCESS_3": "Success.B90",
            # Error colors
            "COLOR_ERROR_1": "Error.B40",
            "COLOR_ERROR_2": "Error.B70",
            "COLOR_ERROR_3": "Error.B110",
            # Warning colors
            "COLOR_WARN_1": "Warning.B40",
            "COLOR_WARN_2": "Warning.B70",
            "COLOR_WARN_3": "Warning.B90",
            "COLOR_WARN_4": "Warning.B100",
            # Icon colors
            "ICON_1": "Primary.B140",
            "ICON_2": "Secondary.B80",
            "ICON_3": "Success.B80",
            "ICON_4": "Error.B70",
            "ICON_5": "Warning.B70",
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
            # Syntax highlighting colors
            "EDITOR_BACKGROUND": "Syntax.B0",
            "EDITOR_CURRENTLINE": "Syntax.B0",
            "EDITOR_CURRENTCELL": "Syntax.B10",
            "EDITOR_OCCURRENCE": "Syntax.B20",
            "EDITOR_CTRLCLICK": "Syntax.B30",
            "EDITOR_SIDEAREAS": "Syntax.B40",
            "EDITOR_MATCHED_P": "Syntax.B50",
            "EDITOR_UNMATCHED_P": "Syntax.B60",
            "EDITOR_NORMAL": "Syntax.B70",
            "EDITOR_KEYWORD": "Syntax.B80",
            "EDITOR_MAGIC": "Syntax.B90",
            "EDITOR_BUILTIN": "Syntax.B100",
            "EDITOR_DEFINITION": "Syntax.B110",
            "EDITOR_COMMENT": "Syntax.B120",
            "EDITOR_STRING": "Syntax.B130",
            "EDITOR_NUMBER": "Syntax.B140",
            "EDITOR_INSTANCE": "Syntax.B150",
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
            "TIP_TITLE_COLOR": "Success.B80",
            "TIP_CHAR_HIGHLIGHT_COLOR": "Warning.B90",
            # Tooltip opacity (numeric value, not a color reference)
            "OPACITY_TOOLTIP": 230,
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
            "COLOR_SUCCESS_1": "Success.B110",
            "COLOR_SUCCESS_2": "Success.B80",
            "COLOR_SUCCESS_3": "Success.B60",
            # Error colors
            "COLOR_ERROR_1": "Error.B110",
            "COLOR_ERROR_2": "Error.B80",
            "COLOR_ERROR_3": "Error.B40",
            # Warning colors
            "COLOR_WARN_1": "Warning.B110",
            "COLOR_WARN_2": "Warning.B80",
            "COLOR_WARN_3": "Warning.B60",
            "COLOR_WARN_4": "Warning.B50",
            # Icon colors
            "ICON_1": "Primary.B10",
            "ICON_2": "Secondary.B70",
            "ICON_3": "Success.B70",
            "ICON_4": "Error.B80",
            "ICON_5": "Warning.B80",
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
            # Syntax highlighting colors
            "EDITOR_BACKGROUND": "Syntax.B0",
            "EDITOR_CURRENTLINE": "Syntax.B0",
            "EDITOR_CURRENTCELL": "Syntax.B10",
            "EDITOR_OCCURRENCE": "Syntax.B20",
            "EDITOR_CTRLCLICK": "Syntax.B30",
            "EDITOR_SIDEAREAS": "Syntax.B40",
            "EDITOR_MATCHED_P": "Syntax.B50",
            "EDITOR_UNMATCHED_P": "Syntax.B60",
            "EDITOR_NORMAL": "Syntax.B70",
            "EDITOR_KEYWORD": "Syntax.B80",
            "EDITOR_MAGIC": "Syntax.B90",
            "EDITOR_BUILTIN": "Syntax.B100",
            "EDITOR_DEFINITION": "Syntax.B110",
            "EDITOR_COMMENT": "Syntax.B120",
            "EDITOR_STRING": "Syntax.B130",
            "EDITOR_NUMBER": "Syntax.B140",
            "EDITOR_INSTANCE": "Syntax.B150",
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
            "COLOR_HEART": "Error.B70",
            # For editor tooltips
            "TIP_TITLE_COLOR": "Success.B30",
            "TIP_CHAR_HIGHLIGHT_COLOR": "Warning.B40",
            # Tooltip opacity (numeric value, not a color reference)
            "OPACITY_TOOLTIP": 230,
        },
    }
