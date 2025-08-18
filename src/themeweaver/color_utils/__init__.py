"""
Themeweaver utilities package.

This package provides color manipulation, generation, and analysis utilities
for the themeweaver project, with a focus on perceptually uniform color generation
using LCH color space and Delta E spacing for scientifically sound palettes.
"""

from themeweaver.color_utils.color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsv,
    hsv_to_rgb,
    lch_to_hex,
    rgb_to_lch,
    calculate_delta_e,
    get_color_info,
    is_color_dark,
    classify_color_lightness,
    is_color_suitable_for_theme,
    get_color_brightness_info,
    is_lch_in_gamut,
    find_max_in_gamut_chroma,
    adjust_lch_to_gamut,
)

from themeweaver.color_utils.interpolation_methods import (
    linear_interpolate,
    circular_interpolate,
    cubic_interpolate,
    exponential_interpolate,
    sine_interpolate,
    cosine_interpolate,
    hermite_interpolate,
    quintic_interpolate,
)

from themeweaver.color_utils.palette_generators import (
    generate_spyder_palette_from_color,
    generate_group_palettes_from_color,
)
from themeweaver.color_utils.theme_generator_utils import (
    generate_theme_from_colors,
    validate_input_colors,
)

from themeweaver.color_utils.color_generation import (
    generate_theme_colors,
)

from themeweaver.color_utils.color_analysis import (
    load_color_groups_from_file,
    extract_colors_from_group,
    analyze_existing_colors,
    analyze_chromatic_distances,
    calculate_std_dev,
    print_color_analysis,
    analyze_palette_lch,
    find_optimal_parameters,
    compare_with_generated,
    generate_inspired_palette,
)

from themeweaver.color_utils.common_palettes import (
    COMMON_PALETTES,
    get_palette_names,
    get_palette,
    get_all_palettes,
)

from themeweaver.color_utils.palette_loaders import (
    load_palette_from_file,
    parse_palette_from_args,
    validate_palette_data,
)

from themeweaver.color_utils.color_names import (
    get_color_name,
    get_multiple_color_names,
    get_palette_name_from_color,
    generate_random_adjective,
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
    "get_color_info",
    "is_color_dark",
    "classify_color_lightness",
    "is_color_suitable_for_theme",
    "get_color_brightness_info",
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
    "load_color_groups_from_file",
    "extract_colors_from_group",
    "analyze_existing_colors",
    "analyze_chromatic_distances",
    "calculate_std_dev",
    "print_color_analysis",
    "analyze_palette_lch",
    "find_optimal_parameters",
    "compare_with_generated",
    "generate_inspired_palette",
    # Common palettes
    "COMMON_PALETTES",
    "get_palette_names",
    "get_palette",
    "get_all_palettes",
    # Palette loaders
    "load_palette_from_file",
    "parse_palette_from_args",
    "validate_palette_data",
    # Color names
    "get_color_name",
    "get_multiple_color_names",
    "get_palette_name_from_color",
    "generate_random_adjective",
    # New palette generation
    "generate_spyder_palette_from_color",
    "generate_group_palettes_from_color",
    "generate_theme_from_colors",
    "validate_input_colors",
]
