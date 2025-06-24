#!/usr/bin/env python3
"""
Generate color group palettes using perceptually uniform LCH color space.

This module provides group-style color generation with intelligent hue-specific
adjustments for optimal visibility on dark and light backgrounds.
"""

import argparse
import sys


from themeweaver.color_utils.color_analysis import (
    load_color_groups_from_file,
    print_color_analysis,
    analyze_chromatic_distances,
)
from themeweaver.color_utils.color_generation import (
    generate_theme_optimized_colors,
    generate_group_uniform_palette,
)


def generate_group_palettes(
    output_format="class",
    start_hue=None,
    num_colors=12,
    target_delta_e=25,
    uniform=False,
):
    """Generate group-style color palettes for dark and light themes."""

    # Choose generation method
    if uniform:
        # Uniform 30° hue steps with group adjustments
        dark_colors = generate_group_uniform_palette("dark", num_colors)
        light_colors = generate_group_uniform_palette("light", num_colors)
        method_info = "group Uniform (30° hue steps)"
    else:
        # Perceptually uniform with group adjustments (RECOMMENDED)
        dark_colors = generate_theme_optimized_colors(
            theme="dark",
            start_hue=start_hue,
            num_colors=num_colors,
            target_delta_e=target_delta_e,
        )
        light_colors = generate_theme_optimized_colors(
            theme="light",
            start_hue=start_hue,
            num_colors=num_colors,
            target_delta_e=target_delta_e,
        )
        method_info = f"Group Optimized (ΔE ≈ {target_delta_e})"

    # Print header
    print(f"# Generated using {method_info}")
    print(f"# Start hue: {start_hue or 'auto (37° dark, 53° light)'}")
    print(f"# Colors: {num_colors}")
    print()

    if output_format == "class":
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

    elif output_format == "json":
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

    elif output_format == "list":
        print("Dark theme colors:")
        for i, color in enumerate(dark_colors):
            print(f"B{(i + 1) * 10}: {color}")

        print("\nLight theme colors:")
        for i, color in enumerate(light_colors):
            print(f"B{(i + 1) * 10}: {color}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate group-style color palettes with intelligent hue adjustments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Generate default group-style palettes
  %(prog)s --uniform                          # Use uniform 30° hue steps
  %(prog)s --target-delta-e 30                # Increase color spacing
  %(prog)s --start-hue 0 --num-colors 8       # Custom red start with 8 colors
  %(prog)s --output-format json               # JSON output
  %(prog)s analyze --file colors.py           # Analyze existing palettes
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command (default) - add arguments to main parser
    parser.add_argument(
        "--start-hue",
        type=int,
        default=None,
        help="Starting hue in degrees (0-360). Auto-selects optimal hue if not specified.",
    )
    parser.add_argument(
        "--num-colors",
        type=int,
        default=12,
        help="Number of colors to generate (default: 12)",
    )
    parser.add_argument(
        "--target-delta-e",
        type=float,
        default=25,
        help="Target perceptual distance between colors (default: 25)",
    )
    parser.add_argument(
        "--uniform",
        action="store_true",
        help="Use uniform 30° hue steps instead of perceptual spacing",
    )
    parser.add_argument(
        "--output-format",
        choices=["class", "json", "list"],
        default="class",
        help="Output format (default: class)",
    )
    parser.add_argument(
        "--no-analysis",
        action="store_true",
        help="Skip chromatic distance analysis output",
    )

    # Analyze command (optional)
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze existing color groups"
    )
    analyze_parser.add_argument(
        "--file",
        "-f",
        default="src/themeweaver/colorsystem.py",
        help="Path to color system file (default: src/themeweaver/colorsystem.py)",
    )
    analyze_parser.add_argument(
        "--groups",
        "-g",
        nargs="*",
        help="Specific groups to analyze (default: all groups)",
    )

    args = parser.parse_args()

    try:
        if args.command == "analyze":
            # Load and analyze color groups from file
            color_groups = load_color_groups_from_file(args.file)
            if not color_groups:
                print(f"No color groups found in {args.file}")
                return

            print(f"Loaded {len(color_groups)} color groups from {args.file}")
            print_color_analysis(color_groups, args.groups)

        else:
            # Default: generate group-style palettes
            generate_group_palettes(
                args.output_format,
                args.start_hue,
                args.num_colors,
                args.target_delta_e,
                args.uniform,
            )

            # Add analysis unless disabled
            if not args.no_analysis:
                print("\n" + "=" * 60)
                print("PERCEPTUAL DISTANCE ANALYSIS")
                print("=" * 60)

                # Generate colors again for analysis
                if args.uniform:
                    dark_colors = generate_group_uniform_palette(
                        "dark", args.num_colors
                    )
                    light_colors = generate_group_uniform_palette(
                        "light", args.num_colors
                    )
                else:
                    dark_colors = generate_theme_optimized_colors(
                        theme="dark",
                        start_hue=args.start_hue,
                        num_colors=args.num_colors,
                        target_delta_e=args.target_delta_e,
                    )
                    light_colors = generate_theme_optimized_colors(
                        theme="light",
                        start_hue=args.start_hue,
                        num_colors=args.num_colors,
                        target_delta_e=args.target_delta_e,
                    )

                analyze_chromatic_distances(dark_colors, "Dark Palette")
                analyze_chromatic_distances(light_colors, "Light Palette")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
