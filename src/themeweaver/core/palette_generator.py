"""
Palette generation utilities for ThemeWeaver.

This module provides functions for generating different types of color palettes
used in Spyder themes, including algorithmic generation and standard palettes.
"""

from typing import Dict


def generate_logos_palette() -> Dict[str, Dict[str, str]]:
    """Generate standard Logos palette.

    Returns:
        Dictionary containing the Logos color palette with hex color values.
    """
    return {
        "Logos": {
            "B10": "#3775a9",
            "B20": "#ffd444",
            "B30": "#414141",
            "B40": "#fafafa",
            "B50": "#ee0000",
        }
    }
