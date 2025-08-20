"""
Command-line interface for ThemeWeaver.

This module provides CLI commands for generating, exporting, and managing themes.
"""

import argparse
import logging
import sys

from themeweaver.cli.commands import (
    cmd_analyze,
    cmd_export,
    cmd_generate,
    cmd_groups,
    cmd_info,
    cmd_interpolate,
    cmd_list,
    cmd_validate,
)
from themeweaver.cli.utils import setup_logging

_logger = logging.getLogger(__name__)


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="themeweaver",
        description="ThemeWeaver - Generate and export Spyder themes",
    )

    # Add version argument
    parser.add_argument("--version", action="version", version="ThemeWeaver 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List all available themes")
    list_parser.set_defaults(func=cmd_list)

    # Info command
    info_parser = subparsers.add_parser("info", help="Show detailed theme information")
    info_parser.add_argument("theme", help="Theme name to show info for")
    info_parser.set_defaults(func=cmd_info)

    # Export command
    export_parser = subparsers.add_parser(
        "export", help="Export theme(s) to build directory"
    )
    export_group = export_parser.add_mutually_exclusive_group(required=True)
    export_group.add_argument("--theme", help="Theme name to export")
    export_group.add_argument("--all", action="store_true", help="Export all themes")

    export_parser.add_argument(
        "--variants",
        help="Comma-separated list of variants to export (e.g., 'dark,light')",
    )
    export_parser.add_argument(
        "--output", "-o", help="Output directory (default: workspace/build)"
    )
    export_parser.set_defaults(func=cmd_export)

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate theme configuration"
    )
    validate_parser.add_argument("theme", help="Theme name to validate")
    validate_parser.set_defaults(func=cmd_validate)

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate a new theme using color algorithms"
    )
    generate_parser.add_argument("name", help="Theme name (used for directory name)")

    # Generation methods - mutually exclusive
    generation_group = generate_parser.add_mutually_exclusive_group()

    generation_group.add_argument(
        "--colors",
        nargs=6,
        metavar=("PRIMARY", "SECONDARY", "ERROR", "SUCCESS", "WARNING", "GROUP"),
        help="Generate theme from single colors for each palette (6 hex colors required in this order: Primary, Secondary, Error, Success, Warning, Group)",
    )
    generation_group.add_argument(
        "--palette-name",
        help="Name for the primary palette (used with algorithmic generation)",
    )

    # Algorithmic generation options
    generate_parser.add_argument(
        "--start-hue", type=int, help="Starting hue for algorithmic generation (0-360)"
    )
    generate_parser.add_argument(
        "--num-colors",
        type=int,
        default=12,
        help="Number of colors in group palettes (default: 12)",
    )
    generate_parser.add_argument(
        "--target-delta-e",
        type=float,
        default=25,
        help="Target perceptual distance between colors (default: 25)",
    )
    generate_parser.add_argument(
        "--uniform",
        action="store_true",
        help="Use uniform hue steps instead of perceptual spacing",
    )

    # Color interpolation method
    generate_parser.add_argument(
        "--method",
        choices=[
            "linear",
            "cubic",
            "exponential",
            "sine",
            "cosine",
            "hermite",
            "quintic",
            "hsv",
            "lch",
        ],
        default="lch",
        help="Color interpolation method (default: lch)",
    )

    # Theme metadata options
    generate_parser.add_argument("--display-name", help="Human-readable theme name")
    generate_parser.add_argument("--description", help="Theme description")
    generate_parser.add_argument(
        "--author", default="ThemeWeaver", help="Theme author (default: ThemeWeaver)"
    )
    generate_parser.add_argument("--tags", help="Comma-separated list of tags")

    # Options
    generate_parser.add_argument(
        "--simple-names",
        action="store_true",
        help="Use simple color names instead of creative names",
    )
    generate_parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing theme if it exists"
    )
    generate_parser.add_argument(
        "--analyze",
        action="store_true",
        help="Show detailed color analysis of generated theme",
    )

    generate_parser.set_defaults(func=cmd_generate)

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze color palettes and find optimal generation parameters"
    )

    # Input sources - mutually exclusive
    analyze_group = analyze_parser.add_mutually_exclusive_group(required=True)
    analyze_group.add_argument(
        "common",
        nargs="?",
        help="Analyze a common palette (e.g., solarized, material)",
    )
    analyze_group.add_argument(
        "--file", "-f", help="Load palette from file (Python/JSON)"
    )
    analyze_group.add_argument(
        "--colors",
        "-c",
        nargs="+",
        help="Define colors directly (name=hex or just hex)",
    )

    # Analysis options
    analyze_parser.add_argument(
        "--compare", action="store_true", help="Compare with current generation"
    )
    analyze_parser.add_argument(
        "--generate", action="store_true", help="Generate inspired palette"
    )
    analyze_parser.add_argument(
        "--theme",
        choices=["dark", "light"],
        default="dark",
        help="Theme for generation/comparison (default: dark)",
    )
    analyze_parser.add_argument(
        "--max-colors", type=int, help="Limit number of colors for parameter testing"
    )
    analyze_parser.set_defaults(func=cmd_analyze)

    # Interpolate command
    interpolate_parser = subparsers.add_parser(
        "interpolate", help="Interpolate between two colors using various methods"
    )
    interpolate_parser.add_argument(
        "start_color", help="Starting hex color (e.g., #FF0000)"
    )
    interpolate_parser.add_argument(
        "end_color", help="Ending hex color (e.g., #0000FF)"
    )
    interpolate_parser.add_argument(
        "steps",
        type=int,
        default=8,
        nargs="?",
        help="Number of interpolation steps (default: 8)",
    )
    interpolate_parser.add_argument(
        "--method",
        choices=[
            "linear",
            "cubic",
            "exponential",
            "sine",
            "cosine",
            "hermite",
            "quintic",
            "hsv",
            "lch",
        ],
        default="linear",
        help="Interpolation method (default: linear)",
    )
    interpolate_parser.add_argument(
        "--exponent",
        type=float,
        default=2,
        help="Exponent for exponential interpolation (default: 2)",
    )
    interpolate_parser.add_argument(
        "--output",
        choices=["list", "json", "yaml"],
        default="list",
        help="Output format (default: list)",
    )
    interpolate_parser.add_argument("--name", help="Name for the generated palette")
    interpolate_parser.add_argument(
        "--simple-names", action="store_true", help="Use simple color names"
    )
    interpolate_parser.add_argument(
        "--analyze", action="store_true", help="Show perceptual analysis"
    )
    interpolate_parser.add_argument(
        "--validate", action="store_true", help="Validate gradient uniqueness"
    )
    interpolate_parser.set_defaults(func=cmd_interpolate)

    # Groups command
    groups_parser = subparsers.add_parser(
        "groups", help="Generate group-style color palettes"
    )
    groups_parser.add_argument(
        "--start-hue",
        type=int,
        help="Starting hue for generation (0-360)",
    )
    groups_parser.add_argument(
        "--num-colors",
        type=int,
        default=12,
        help="Number of colors in palettes (default: 12)",
    )
    groups_parser.add_argument(
        "--target-delta-e",
        type=float,
        default=25,
        help="Target perceptual distance between colors (default: 25)",
    )
    groups_parser.add_argument(
        "--uniform",
        action="store_true",
        help="Use uniform 30° hue steps instead of perceptual spacing",
    )
    groups_parser.add_argument(
        "--output-format",
        choices=["class", "json", "list"],
        default="class",
        help="Output format (default: class)",
    )
    groups_parser.add_argument(
        "--no-analysis",
        action="store_true",
        help="Skip chromatic distance analysis output",
    )
    groups_parser.set_defaults(func=cmd_groups)

    return parser


def main():
    """Main CLI entry point."""
    # Set up logging for CLI output
    setup_logging()

    parser = create_parser()

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command specified
    if not args.command:
        parser.print_help()
        return

    # Run the specified command
    try:
        args.func(args)
    except KeyboardInterrupt:
        _logger.warning("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        _logger.error("❌ Unexpected error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
