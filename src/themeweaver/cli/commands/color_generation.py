"""
Color generation command.
"""

import logging
import sys

from themeweaver.color_utils.color_analysis import analyze_chromatic_distances
from themeweaver.color_utils.color_generation import generate_theme_colors

_logger = logging.getLogger(__name__)


def cmd_groups(args):
    """Generate group-style color palettes."""
    try:
        # Generate colors
        if args.uniform:
            dark_colors = generate_theme_colors("dark", args.num_colors, uniform=True)
            light_colors = generate_theme_colors("light", args.num_colors, uniform=True)
            method_info = "group Uniform (30° hue steps)"
        else:
            dark_colors = generate_theme_colors(
                theme="dark",
                start_hue=args.start_hue,
                num_colors=args.num_colors,
                target_delta_e=args.target_delta_e,
            )
            light_colors = generate_theme_colors(
                theme="light",
                start_hue=args.start_hue,
                num_colors=args.num_colors,
                target_delta_e=args.target_delta_e,
            )
            method_info = f"Group Optimized (ΔE ≈ {args.target_delta_e})"

        # Print header
        _logger.info("🎨 Generated using %s", method_info)
        _logger.info("🎯 Start hue: %s", args.start_hue or "auto (37° dark, 53° light)")
        _logger.info("📊 Colors: %d", args.num_colors)

        # Output based on format
        if args.output_format == "class":
            print("class GroupDark:")
            print('    """')
            print("    Group colors for the dark palette.")
            print('    """')
            print()

            for i, color in enumerate(dark_colors):
                step = (i + 1) * 10
                print(f"    B{step} = '{color}'")

            print("\n")

            print("class GroupLight:")
            print('    """')
            print("    Group colors for the light palette.")
            print('    """')
            print()

            for i, color in enumerate(light_colors):
                step = (i + 1) * 10
                print(f"    B{step} = '{color}'")

        elif args.output_format == "json":
            import json

            result = {
                "GroupDark": {
                    f"B{(i + 1) * 10}": color for i, color in enumerate(dark_colors)
                },
                "GroupLight": {
                    f"B{(i + 1) * 10}": color for i, color in enumerate(light_colors)
                },
            }
            print(json.dumps(result, indent=2))

        elif args.output_format == "list":
            print("Dark theme colors:")
            for i, color in enumerate(dark_colors):
                step = (i + 1) * 10
                print(f"  B{step}: {color}")

            print("\nLight theme colors:")
            for i, color in enumerate(light_colors):
                step = (i + 1) * 10
                print(f"  B{step}: {color}")

        # Add analysis unless disabled
        if not args.no_analysis:
            _logger.info("📊 PERCEPTUAL DISTANCE ANALYSIS")
            analyze_chromatic_distances(dark_colors, "Dark Palette")
            analyze_chromatic_distances(light_colors, "Light Palette")

    except Exception as e:
        _logger.error("❌ Group generation failed: %s", e)
        sys.exit(1)
