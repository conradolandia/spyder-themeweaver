"""
Color generation command.
"""

import json
import logging
from typing import Any, List, Optional, Tuple

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

PaletteTriplet = Tuple[List[str], List[str], str]


def _palette_triplet(args: Any) -> Optional[PaletteTriplet]:
    """Compute dark/light color lists and a short method description. None on user error."""
    if args.method == "syntax":
        if not args.from_color:
            _logger.error("❌ Syntax method requires --from-color argument")
            return None

        syntax_palette = generate_palettes_from_color(
            args.from_color, SYNTAX_PALETTE_SIZE, palette_type="syntax"
        )
        syntax_colors = list(syntax_palette.values())
        method_info = f"Syntax highlighting from {args.from_color}"
        return syntax_colors, syntax_colors, method_info

    if args.from_color:
        group_dark, group_light = generate_palettes_from_color(
            args.from_color, args.num_colors
        )
        dark_colors = list(group_dark.values())
        light_colors = list(group_light.values())
        method_info = f"Golden ratio from {args.from_color}"
        return dark_colors, light_colors, method_info

    if args.method == "optimal":
        dark_colors = generate_optimal_colors(args.num_colors, "dark", args.start_hue)
        light_colors = generate_optimal_colors(args.num_colors, "light", args.start_hue)
        method_info = "Optimal distinguishability"
        return dark_colors, light_colors, method_info

    if args.method == "uniform":
        dark_colors = generate_theme_colors("dark", args.num_colors, uniform=True)
        light_colors = generate_theme_colors("light", args.num_colors, uniform=True)
        method_info = "Uniform (30° hue steps)"
        return dark_colors, light_colors, method_info

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
    return dark_colors, light_colors, method_info


def _log_palette_header(args: Any, method_info: str) -> None:
    _logger.info("🎨 Generated using %s", method_info)
    if args.from_color:
        _logger.info("🎯 Starting color: %s", args.from_color)
    else:
        _logger.info("🎯 Start hue: %s", args.start_hue or "auto (37° dark, 53° light)")
    _logger.info("📊 Colors: %d", args.num_colors)


def _emit_palette_output(
    args: Any, dark_colors: List[str], light_colors: List[str]
) -> None:
    if args.output_format == "class":
        if args.method == "syntax":
            print("class Syntax:")
            print('    """')
            print("    Syntax highlighting colors.")
            print('    """')
            print()

            for i, color in enumerate(dark_colors):
                step = (i + 1) * 10
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
        if args.method == "syntax":
            result = {
                "Syntax": {
                    f"B{(i + 1) * 10}": color for i, color in enumerate(dark_colors)
                }
            }
        else:
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
        if args.method == "syntax":
            print("Syntax colors:")
            for i, color in enumerate(dark_colors):
                step = (i + 1) * 10
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


def _run_analysis_if_needed(
    args: Any, dark_colors: List[str], light_colors: List[str]
) -> None:
    if args.no_analysis:
        return
    _logger.info("📊 PERCEPTUAL DISTANCE ANALYSIS")
    if args.method == "syntax":
        analyze_chromatic_distances(dark_colors, "Syntax Palette")
    else:
        analyze_chromatic_distances(dark_colors, "Dark Palette")
        analyze_chromatic_distances(light_colors, "Light Palette")


def cmd_palette(args: Any) -> None:
    """Generate color palettes."""
    quiet = args.output_format in ("class", "json", "list")

    if quiet:
        triplet = _palette_triplet(args)
        if triplet is None:
            return
        dark_colors, light_colors, method_info = triplet
    else:
        with operation_context("Palette generation"):
            triplet = _palette_triplet(args)
        if triplet is None:
            return
        dark_colors, light_colors, method_info = triplet
        _log_palette_header(args, method_info)

    _emit_palette_output(args, dark_colors, light_colors)
    _run_analysis_if_needed(args, dark_colors, light_colors)
