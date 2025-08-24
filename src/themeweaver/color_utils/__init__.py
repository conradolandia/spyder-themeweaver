"""
Color utilities for themeweaver.

This module provides color conversion, analysis, and generation utilities
using LCH color space and Delta E spacing for scientifically sound palettes.
"""

from themeweaver.color_utils.color_analysis import analyze_chromatic_distances
from themeweaver.color_utils.color_generation import generate_theme_colors
from themeweaver.color_utils.color_names import (
    generate_random_adjective,
    get_color_name,
    get_color_names_from_api,
    get_palette_name_from_color,
)
from themeweaver.color_utils.color_utils import (
    adjust_lch_to_gamut,
    calculate_delta_e,
    calculate_std_dev,
    find_max_in_gamut_chroma,
    get_color_info,
    hex_to_rgb,
    hsv_to_rgb,
    is_color_dark,
    is_lch_in_gamut,
    lch_to_hex,
    rgb_to_hex,
    rgb_to_hsv,
    rgb_to_lch,
)
from themeweaver.color_utils.interpolation_methods import (
    circular_interpolate,
    cosine_interpolate,
    cubic_interpolate,
    exponential_interpolate,
    hermite_interpolate,
    linear_interpolate,
    quintic_interpolate,
    sine_interpolate,
)
from themeweaver.color_utils.palette_generators import (
    generate_lightness_gradient_from_color,
    generate_palettes_from_color,
)
from themeweaver.color_utils.palette_loaders import (
    load_color_groups_from_file,
    load_palette_from_file,
    parse_palette_from_args,
    validate_palette_data,
)
from themeweaver.color_utils.theme_generator_utils import (
    generate_theme_from_colors,
    validate_input_colors,
)

__all__ = [
    # Color utilities
    "hex_to_rgb",
    "rgb_to_hex",
    "rgb_to_hsv",
    "hsv_to_rgb",
    "lch_to_hex",
    "rgb_to_lch",
    "calculate_delta_e",
    "calculate_std_dev",
    "get_color_info",
    "is_color_dark",
    "is_lch_in_gamut",
    "find_max_in_gamut_chroma",
    "adjust_lch_to_gamut",
    # Interpolation methods
    "linear_interpolate",
    "circular_interpolate",
    "cubic_interpolate",
    "exponential_interpolate",
    "sine_interpolate",
    "cosine_interpolate",
    "hermite_interpolate",
    "quintic_interpolate",
    # Color generation
    "generate_theme_colors",
    # Color analysis
    "analyze_chromatic_distances",
    # Palette loaders
    "load_color_groups_from_file",
    "load_palette_from_file",
    "parse_palette_from_args",
    "validate_palette_data",
    # Color names
    "get_color_name",
    "get_color_names_from_api",
    "get_palette_name_from_color",
    "generate_random_adjective",
    # New palette generation
    "generate_lightness_gradient_from_color",
    "generate_palettes_from_color",
    "generate_theme_from_colors",
    "validate_input_colors",
]
