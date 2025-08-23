"""
Color generation command.
"""

import logging

from themeweaver.cli.error_handling import operation_context
from themeweaver.color_utils.color_analysis import analyze_chromatic_distances
from themeweaver.color_utils.color_generation import (
    generate_optimal_colors,
    generate_theme_colors,
)
from themeweaver.color_utils.palette_generators import (
    SYNTAX_PALETTE_SIZE,
    generate_palettes_from_color,
)

_logger = logging.getLogger(__name__)


def cmd_palette(args):
    """Generate color palettes."""
    with operation_context("Palette generation"):
        # Generate colors based on method
        if args.method == "syntax":
            # Syntax highlighting palette generation
            if not args.from_color:
                _logger.error("❌ Syntax method requires --from-color argument")
                return

            # Generate single syntax palette (16 colors)
            syntax_palette = generate_palettes_from_color(
                args.from_color, SYNTAX_PALETTE_SIZE, palette_type="syntax"
            )
            syntax_colors = list(syntax_palette.values())
            method_info = f"Syntax highlighting from {args.from_color}"

            # For syntax, we only have one palette
            dark_colors = syntax_colors
            light_colors = syntax_colors

        elif args.from_color:
            # Color-based generation using golden ratio method
            group_dark, group_light = generate_palettes_from_color(
                args.from_color, args.num_colors
            )
            dark_colors = list(group_dark.values())
            light_colors = list(group_light.values())
            method_info = f"Golden ratio from {args.from_color}"
        elif args.method == "optimal":
            # Optimal distinguishability method
            dark_colors = generate_optimal_colors(
                args.num_colors, "dark", args.start_hue
            )
            light_colors = generate_optimal_colors(
                args.num_colors, "light", args.start_hue
            )
            method_info = "Optimal distinguishability"
        elif args.method == "uniform":
            # Uniform hue steps method
            dark_colors = generate_theme_colors("dark", args.num_colors, uniform=True)
            light_colors = generate_theme_colors("light", args.num_colors, uniform=True)
            method_info = "Uniform (30° hue steps)"
        else:
            # Perceptual spacing method (default)
            dark_colors = generate_theme_colors(
                theme="dark",
                start_hue=args.start_hue,
                num_colors=args.num_colors,
            )
            light_colors = generate_theme_colors(
                theme="light",
                start_hue=args.start_hue,
                num_colors=args.num_colors,
            )
            method_info = "Golden ratio distribution"

        # Print header
        _logger.info("🎨 Generated using %s", method_info)
        if args.from_color:
            _logger.info("🎯 Starting color: %s", args.from_color)
        else:
            _logger.info(
                "🎯 Start hue: %s", args.start_hue or "auto (37° dark, 53° light)"
            )
        _logger.info("📊 Colors: %d", args.num_colors)

        # Output based on format
        if args.output_format == "class":
            if args.method == "syntax":
                print("class Syntax:")
                print('    """')
                print("    Syntax highlighting colors.")
                print('    """')
                print()

                for i, color in enumerate(dark_colors):
                    step = i * 10
                    print(f"    B{step} = '{color}'")
            else:
                print("class GroupDark:")
                print('    """')
                print("    Group Colors for the dark palette.")
                print('    """')
                print()

                for i, color in enumerate(dark_colors):
                    step = (i + 1) * 10
                    print(f"    B{step} = '{color}'")

                print("\n")

                print("class GroupLight:")
                print('    """')
                print("    Group Colors for the light palette.")
                print('    """')
                print()

                for i, color in enumerate(light_colors):
                    step = (i + 1) * 10
                    print(f"    B{step} = '{color}'")

        elif args.output_format == "json":
            import json

            if args.method == "syntax":
                result = {
                    "Syntax": {
                        f"B{i * 10}": color for i, color in enumerate(dark_colors)
                    }
                }
            else:
                result = {
                    "GroupDark": {
                        f"B{(i + 1) * 10}": color for i, color in enumerate(dark_colors)
                    },
                    "GroupLight": {
                        f"B{(i + 1) * 10}": color
                        for i, color in enumerate(light_colors)
                    },
                }
            print(json.dumps(result, indent=2))

        elif args.output_format == "list":
            if args.method == "syntax":
                print("Syntax colors:")
                for i, color in enumerate(dark_colors):
                    step = i * 10
                    print(f"  B{step}: {color}")
            else:
                print("GroupDark colors:")
                for i, color in enumerate(dark_colors):
                    step = (i + 1) * 10
                    print(f"  B{step}: {color}")

                print("\nGroupLight colors:")
                for i, color in enumerate(light_colors):
                    step = (i + 1) * 10
                    print(f"  B{step}: {color}")

        # Add analysis unless disabled
        if not args.no_analysis:
            _logger.info("📊 PERCEPTUAL DISTANCE ANALYSIS")
            if args.method == "syntax":
                analyze_chromatic_distances(dark_colors, "Syntax Palette")
            else:
                analyze_chromatic_distances(dark_colors, "Dark Palette")
                analyze_chromatic_distances(light_colors, "Light Palette")
