#!/usr/bin/env python3
"""
Generic color palette analyzer for themeweaver.

This module can analyze any color palette to understand its characteristics
and determine optimal generation settings to recreate similar aesthetics.
"""

import argparse
import sys

# Local imports from reorganized modules
from .common_palettes import COMMON_PALETTES, get_palette_names
from .palette_loaders import (
    load_palette_from_file,
    parse_palette_from_args,
    validate_palette_data,
)
from .color_analysis import (
    analyze_palette_lch,
    find_optimal_parameters,
    compare_with_generated,
    generate_inspired_palette,
)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze any color palette and find optimal generation parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s solarized                           # Analyze Solarized palette
  %(prog)s --file colors.py                    # Analyze palette from file
  %(prog)s --colors red=#ff0000 blue=#0000ff   # Analyze custom colors
  %(prog)s material --compare                  # Analyze Material Design and compare
  %(prog)s --file palette.json --generate      # Analyze and generate inspired palette
        """,
    )

    # Input sources
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "common",
        nargs="?",
        choices=get_palette_names(),
        help="Analyze a common palette",
    )
    group.add_argument("--file", "-f", help="Load palette from file (Python/JSON)")
    group.add_argument(
        "--colors",
        "-c",
        nargs="+",
        help="Define colors directly (name=hex or just hex)",
    )

    # Analysis options
    parser.add_argument(
        "--compare", action="store_true", help="Compare with current generation"
    )
    parser.add_argument(
        "--generate", action="store_true", help="Generate inspired palette"
    )
    parser.add_argument(
        "--theme",
        choices=["dark", "light"],
        default="dark",
        help="Theme for generation/comparison (default: dark)",
    )
    parser.add_argument(
        "--max-colors", type=int, help="Limit number of colors for parameter testing"
    )

    args = parser.parse_args()

    try:
        # Load the palette
        palette_data = None
        if args.common:
            palette_data = COMMON_PALETTES[args.common]
        elif args.file:
            palette_data = load_palette_from_file(args.file)
        elif args.colors:
            palette_data = parse_palette_from_args(args.colors)

        # Validate palette data
        if not palette_data:
            print("ERROR: No palette data loaded", file=sys.stderr)
            sys.exit(1)

        validate_palette_data(palette_data)

        # Analyze the palette
        palette_lch = analyze_palette_lch(palette_data)
        if not palette_lch:
            return

        # Find optimal parameters
        best_params, best_distance = find_optimal_parameters(
            palette_data, args.max_colors
        )
        if best_params:
            print(f"\nBEST PARAMETERS for {palette_data['name']}-like palette:")
            print(f"  {best_params}")
            print(f"  Average distance: {best_distance:.1f}")

        # Optional comparisons and generation
        if args.compare:
            compare_with_generated(palette_data, args.theme)

        if args.generate:
            generate_inspired_palette(palette_data, args.theme)

        # Show recommendations
        if best_params:
            print("\n=== RECOMMENDATIONS ===")
            print(f"To recreate {palette_data['name']} aesthetic, try:")
            delta_e = best_params["target_delta_e"]
            start_hue = best_params["start_hue"]
            print(
                f"  python -m themeweaver.color_utils.generate_groups --target-delta-e {delta_e} --start-hue {start_hue}"
            )

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
