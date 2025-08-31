"""
Command-line interface for ThemeWeaver.

This module provides CLI commands for generating, exporting, and managing themes.
"""

import argparse
import logging
import sys

from themeweaver.cli.commands import (
    cmd_export,
    cmd_generate,
    cmd_info,
    cmd_interpolate,
    cmd_list,
    cmd_package,
    cmd_palette,
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
        "generate", help="Generate a new theme from individual colors"
    )
    generate_parser.add_argument("name", help="Theme name (used for directory name)")

    # Colors argument (required)
    generate_parser.add_argument(
        "--colors",
        nargs=6,
        required=True,
        metavar=("PRIMARY", "SECONDARY", "ERROR", "SUCCESS", "WARNING", "GROUP"),
        help="Generate theme from single colors for each palette (6 hex colors required in this order: Primary, Secondary, Error, Success, Warning, Group)",
    )

    generate_parser.add_argument(
        "--syntax-colors",
        nargs="+",
        metavar="COLOR",
        help="Syntax highlighting colors. Provide either 1 color (for seeded auto-generation) or 16 colors (for custom palette). If not provided, uses default auto-generated palette.",
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

    # Palette command
    palette_parser = subparsers.add_parser("palette", help="Generate color palettes")
    palette_parser.add_argument(
        "--method",
        choices=["perceptual", "optimal", "uniform", "syntax"],
        default="perceptual",
        help="Generation method: perceptual (Delta E), optimal (max distinguishability), uniform (30° steps), syntax (syntax highlighting optimized) (default: perceptual)",
    )
    palette_parser.add_argument(
        "--from-color",
        help="Generate palette variations from a specific color (uses golden ratio method)",
    )
    palette_parser.add_argument(
        "--start-hue",
        type=int,
        help="Starting hue for generation (0-360) (used with optimal and uniform methods)",
    )
    palette_parser.add_argument(
        "--num-colors",
        type=int,
        default=12,
        help="Number of colors in palettes (default: 12)",
    )

    palette_parser.add_argument(
        "--output-format",
        choices=["class", "json", "list"],
        default="list",
        help="Output format (default: list)",
    )
    palette_parser.add_argument(
        "--no-analysis",
        action="store_true",
        help="Skip chromatic distance analysis output",
    )
    palette_parser.set_defaults(func=cmd_palette)

    # Package command
    package_parser = subparsers.add_parser(
        "package", help="Package exported themes into compressed archives"
    )
    package_parser.add_argument(
        "--theme",
        help="Theme name to package (if not provided, packages all exported themes)",
    )
    package_parser.add_argument(
        "--output",
        "-o",
        help="Output directory for the packaged themes (default: workspace/packages)",
    )
    package_parser.add_argument(
        "--format",
        choices=["zip", "tar.gz", "folder"],
        default="zip",
        help="Archive format or 'folder' for uncompressed directory (default: zip)",
    )
    package_parser.set_defaults(func=cmd_package)

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
