"""
Themeweaver utilities package.

This package provides color manipulation, generation, and analysis utilities
for the themeweaver project, with a focus on perceptually uniform color generation
using LCH color space and Delta E spacing for scientifically sound palettes.
"""

from .color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsv,
    hsv_to_rgb,
    lch_to_hex,
    rgb_to_lch,
    calculate_delta_e,
    get_color_info,
    linear_interpolate,
    HAS_LCH,
)

from .color_generation import (
    generate_theme_optimized_colors,
)

from .color_analysis import (
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

from .famous_palettes import (
    FAMOUS_PALETTES,
    get_palette_names,
    get_palette,
    get_all_palettes,
)

from .palette_loaders import (
    load_palette_from_file,
    parse_palette_from_args,
    validate_palette_data,
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
    "linear_interpolate",
    "HAS_LCH",
    # Color generation
    "generate_theme_optimized_colors",
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
    # Famous palettes
    "FAMOUS_PALETTES",
    "get_palette_names",
    "get_palette",
    "get_all_palettes",
    # Palette loaders
    "load_palette_from_file",
    "parse_palette_from_args",
    "validate_palette_data",
]
