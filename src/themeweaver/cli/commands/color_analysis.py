"""
Color analysis command.
"""

import logging
import sys

from themeweaver.color_utils.color_analysis import (
    analyze_palette_lch,
    compare_with_generated,
    find_optimal_parameters,
    generate_inspired_palette,
)
from themeweaver.color_utils.common_palettes import COMMON_PALETTES, get_palette_names
from themeweaver.color_utils.palette_loaders import (
    load_palette_from_file,
    parse_palette_from_args,
    validate_palette_data,
)

_logger = logging.getLogger(__name__)


def cmd_analyze(args):
    """Analyze color palettes and find optimal generation parameters."""
    try:
        # Load the palette
        palette_data = None
        if args.common:
            if args.common not in get_palette_names():
                _logger.error(
                    "❌ Unknown palette: %s. Available: %s",
                    args.common,
                    ", ".join(get_palette_names()),
                )
                sys.exit(1)
            palette_data = COMMON_PALETTES[args.common]
        elif args.file:
            palette_data = load_palette_from_file(args.file)
        elif args.colors:
            palette_data = parse_palette_from_args(args.colors)

        # Validate palette data
        if not palette_data:
            _logger.error("❌ No palette data loaded")
            sys.exit(1)

        validate_palette_data(palette_data)

        # Analyze the palette
        palette_lch = analyze_palette_lch(palette_data)
        if not palette_lch:
            _logger.error("❌ Failed to analyze palette")
            sys.exit(1)

        # Find optimal parameters
        best_params, best_distance = find_optimal_parameters(
            palette_data, args.max_colors
        )
        if best_params:
            _logger.info(
                "🎯 BEST PARAMETERS for %s-like palette:", palette_data["name"]
            )
            _logger.info("   %s", best_params)
            _logger.info("   Average distance: %.1f", best_distance)

        # Optional comparisons and generation
        if args.compare:
            compare_with_generated(palette_data, args.theme)

        if args.generate:
            generate_inspired_palette(palette_data, args.theme)

        # Show recommendations
        if best_params:
            _logger.info("📋 RECOMMENDATIONS")
            _logger.info("To recreate %s aesthetic, try:", palette_data["name"])
            delta_e = best_params["target_delta_e"]
            start_hue = best_params["start_hue"]
            _logger.info(
                "  themeweaver groups --target-delta-e %s --start-hue %s",
                delta_e,
                start_hue,
            )

    except Exception as e:
        _logger.error("❌ Analysis failed: %s", e)
        sys.exit(1)
