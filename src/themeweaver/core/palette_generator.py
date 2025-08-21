"""
Palette generation utilities for ThemeWeaver.

This module provides functions for generating different types of color palettes
used in Spyder themes, including algorithmic generation and standard palettes.
"""

from typing import Any, Dict


def generate_logos_palette() -> Dict[str, Any]:
    """Generate standard Logos palette."""
    return {
        "Logos": {
            "B10": "#3775a9",
            "B20": "#ffd444",
            "B30": "#414141",
            "B40": "#fafafa",
            "B50": "#ee0000",
        }
    }
