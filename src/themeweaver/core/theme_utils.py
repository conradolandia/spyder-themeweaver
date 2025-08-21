"""
Theme utilities for ThemeWeaver.

This module provides utility functions for theme generation, including
metadata generation, mappings creation, file writing, and analysis.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from themeweaver.color_utils import calculate_delta_e
from themeweaver.color_utils.color_names import get_multiple_color_names

_logger = logging.getLogger(__name__)


def generate_theme_metadata(
    theme_name: str,
    display_name: Optional[str],
    description: Optional[str],
    author: str,
    tags: Optional[List[str]],
) -> Dict[str, Any]:
    """Generate theme.yaml content."""
    return {
        "name": theme_name,
        "display_name": display_name or theme_name.replace("_", " ").title(),
        "description": description or f"Generated theme: {theme_name}",
        "author": author,
        "version": "1.0.0",
        "license": "MIT",
        "tags": tags or ["dark", "light", "generated"],
        "variants": {"dark": True, "light": True},
    }


def generate_mappings(colorsystem_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate mappings.yaml content."""
    # Extract palette names
    palette_names = colorsystem_data.pop(
        "_palette_names", {"primary": "Primary", "secondary": "Secondary"}
    )

    primary_name = palette_names["primary"]
    secondary_name = palette_names["secondary"]

    return {
        "color_classes": {
            "Primary": primary_name,
            "Secondary": secondary_name,
            "Success": "Success",
            "Error": "Error",
            "Warning": "Warning",
            "GroupDark": "GroupDark",
            "GroupLight": "GroupLight",
            "Logos": "Logos",
        },
        "semantic_mappings": {
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
                "COLOR_TEXT_2": "Primary.B110",
                "COLOR_TEXT_3": "Primary.B90",
                "COLOR_TEXT_4": "Primary.B80",
                # Accent colors
                "COLOR_ACCENT_1": "Secondary.B20",
                "COLOR_ACCENT_2": "Secondary.B40",
                "COLOR_ACCENT_3": "Secondary.B50",
                "COLOR_ACCENT_4": "Secondary.B70",
                "COLOR_ACCENT_5": "Secondary.B80",
                # Disabled elements
                "COLOR_DISABLED": "Primary.B70",
                # Colors for information and feedback in dialogs
                "COLOR_SUCCESS_1": "Success.B40",
                "COLOR_SUCCESS_2": "Success.B70",
                "COLOR_SUCCESS_3": "Success.B90",
                "COLOR_ERROR_1": "Error.B40",
                "COLOR_ERROR_2": "Error.B70",
                "COLOR_ERROR_3": "Error.B110",
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
                # Colors for icons and variable explorer
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
                # Colors for highlight in editor
                "COLOR_HIGHLIGHT_1": "Secondary.B10",
                "COLOR_HIGHLIGHT_2": "Secondary.B20",
                "COLOR_HIGHLIGHT_3": "Secondary.B30",
                "COLOR_HIGHLIGHT_4": "Secondary.B50",
                # Colors for occurrences from find widget
                "COLOR_OCCURRENCE_1": "Primary.B10",
                "COLOR_OCCURRENCE_2": "Primary.B20",
                "COLOR_OCCURRENCE_3": "Primary.B30",
                "COLOR_OCCURRENCE_4": "Primary.B50",
                "COLOR_OCCURRENCE_5": "Primary.B80",
                # Colors for Spyder and Python logos
                "PYTHON_LOGO_UP": "Logos.B10",
                "PYTHON_LOGO_DOWN": "Logos.B20",
                "SPYDER_LOGO_BACKGROUND": "Logos.B30",
                "SPYDER_LOGO_WEB": "Logos.B40",
                "SPYDER_LOGO_SNAKE": "Logos.B50",
                # For special tabs
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
                "COLOR_BACKGROUND_4": "Primary.B110",
                "COLOR_BACKGROUND_5": "Primary.B100",
                "COLOR_BACKGROUND_6": "Primary.B90",
                # Text colors
                "COLOR_TEXT_1": "Primary.B10",
                "COLOR_TEXT_2": "Primary.B20",
                "COLOR_TEXT_3": "Primary.B50",
                "COLOR_TEXT_4": "Primary.B70",
                # Accent colors
                "COLOR_ACCENT_1": "Secondary.B130",
                "COLOR_ACCENT_2": "Secondary.B100",
                "COLOR_ACCENT_3": "Secondary.B90",
                "COLOR_ACCENT_4": "Secondary.B80",
                "COLOR_ACCENT_5": "Secondary.B70",
                # Disabled elements
                "COLOR_DISABLED": "Primary.B80",
                # Colors for information and feedback in dialogs
                "COLOR_SUCCESS_1": "Success.B40",
                "COLOR_SUCCESS_2": "Success.B70",
                "COLOR_SUCCESS_3": "Success.B30",
                "COLOR_ERROR_1": "Error.B40",
                "COLOR_ERROR_2": "Error.B70",
                "COLOR_ERROR_3": "Error.B110",
                "COLOR_WARN_1": "Warning.B40",
                "COLOR_WARN_2": "Warning.B70",
                "COLOR_WARN_3": "Warning.B50",
                "COLOR_WARN_4": "Warning.B40",
                # Icon colors
                "ICON_1": "Primary.B30",
                "ICON_2": "Secondary.B50",
                "ICON_3": "Success.B30",
                "ICON_4": "Error.B70",
                "ICON_5": "Warning.B70",
                "ICON_6": "Primary.B140",
                # Colors for icons and variable explorer
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
                # Colors for highlight in editor
                "COLOR_HIGHLIGHT_1": "Secondary.B140",
                "COLOR_HIGHLIGHT_2": "Secondary.B130",
                "COLOR_HIGHLIGHT_3": "Secondary.B120",
                "COLOR_HIGHLIGHT_4": "Secondary.B110",
                # Colors for occurrences from find widget
                "COLOR_OCCURRENCE_1": "Primary.B120",
                "COLOR_OCCURRENCE_2": "Primary.B110",
                "COLOR_OCCURRENCE_3": "Primary.B100",
                "COLOR_OCCURRENCE_4": "Primary.B90",
                "COLOR_OCCURRENCE_5": "Primary.B60",
                # Colors for Spyder and Python logos
                "PYTHON_LOGO_UP": "Logos.B10",
                "PYTHON_LOGO_DOWN": "Logos.B20",
                "SPYDER_LOGO_BACKGROUND": "Logos.B30",
                "SPYDER_LOGO_WEB": "Logos.B40",
                "SPYDER_LOGO_SNAKE": "Logos.B50",
                # For special tabs
                "SPECIAL_TABS_SEPARATOR": "Primary.B70",
                "SPECIAL_TABS_SELECTED": "Secondary.B70",
                # For the heart used to ask for donations
                "COLOR_HEART": "Error.B70",
                # For editor tooltips
                "TIP_TITLE_COLOR": "Success.B20",
                "TIP_CHAR_HIGHLIGHT_COLOR": "Warning.B30",
                # Tooltip opacity (numeric value, not a color reference)
                "OPACITY_TOOLTIP": 230,
            },
        },
    }


def write_yaml_file(file_path: Path, data: Dict[str, Any]) -> str:
    """Write data to a YAML file."""
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(
            data, f, default_flow_style=False, sort_keys=False, allow_unicode=True
        )

    _logger.info(f"📝 Created: {file_path}")
    return str(file_path)


def analyze_algorithmic_palette(
    colorsystem_data: Dict[str, Any], palette_name: str
) -> None:
    """Analyze and log information about algorithmically generated palettes."""
    if palette_name in colorsystem_data:
        palette = colorsystem_data[palette_name]

        # Get a sample of colors for analysis (e.g., B10, B50, B100, B140)
        sample_colors = []
        for step in [10, 50, 100, 140]:
            key = f"B{step}"
            if key in palette:
                sample_colors.append(palette[key])

        if sample_colors:
            # Get color names for sample colors
            color_names = get_multiple_color_names(sample_colors)

            _logger.info(f"🎨 Algorithmic Palette Analysis for '{palette_name}':")
            for i, color in enumerate(sample_colors):
                step = [10, 50, 100, 140][i]
                name = color_names.get(color, "Unknown")
                _logger.info(f"  B{step}: {color} → {name}")

            # Calculate perceptual color distances (Delta E) within palette
            if len(sample_colors) >= 2:
                distances = []
                for i in range(len(sample_colors) - 1):
                    delta_e = calculate_delta_e(sample_colors[i], sample_colors[i + 1])
                    if delta_e is not None:
                        distances.append(delta_e)

                avg_distance = sum(distances) / len(distances)
                _logger.info(f"  Average ΔE: {avg_distance:.1f}")

                # Delta E guideline thresholds
                if avg_distance < 5:
                    _logger.warning("⚠️  Colors in palette may be too similar (ΔE < 5)")
                elif avg_distance > 30:
                    _logger.warning(
                        "⚠️  Colors in palette may be too contrasting (ΔE > 30)"
                    )
                else:
                    _logger.info("✅ Good perceptual distribution in palette")
