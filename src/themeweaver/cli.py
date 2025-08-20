"""
Command-line interface for ThemeWeaver.

This module provides CLI commands for generating, exporting, and managing themes.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from themeweaver.color_utils.theme_generator_utils import (
    generate_theme_from_colors,
    validate_input_colors,
)
from themeweaver.core.colorsystem import load_theme_metadata_from_yaml
from themeweaver.core.palette import create_palettes
from themeweaver.core.theme_exporter import ThemeExporter
from themeweaver.core.theme_generator import ThemeGenerator

_logger = logging.getLogger(__name__)


def setup_logging():
    """Configure logging for the CLI application."""
    # Set up console logging with INFO level by default
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",  # Simple format for CLI output
        handlers=[logging.StreamHandler()],
    )


def list_themes(themes_dir: Optional[Path] = None) -> List[str]:
    """List all available themes.

    Args:
        themes_dir: Directory containing themes. If None, uses default.

    Returns:
        List of theme names
    """
    if themes_dir is None:
        themes_dir = Path(__file__).parent / "themes"

    themes = []
    for theme_dir in themes_dir.iterdir():
        if theme_dir.is_dir() and not theme_dir.name.startswith("."):
            # Check if it has the required files
            if (theme_dir / "theme.yaml").exists():
                themes.append(theme_dir.name)

    return sorted(themes)


def show_theme_info(theme_name: str):
    """Display information about a specific theme.

    Args:
        theme_name: Name of the theme to display info for
    """
    try:
        metadata = load_theme_metadata_from_yaml(theme_name)
        palettes = create_palettes(theme_name)

        _logger.info("📋 Theme: %s", metadata.get("display_name", theme_name))
        _logger.info("   Name: %s", theme_name)
        _logger.info(
            "   Description: %s", metadata.get("description", "No description")
        )
        _logger.info("   Author: %s", metadata.get("author", "Unknown"))
        _logger.info("   Version: %s", metadata.get("version", "Unknown"))
        _logger.info("   License: %s", metadata.get("license", "Unknown"))

        if metadata.get("url"):
            _logger.info("   URL: %s", metadata["url"])

        if metadata.get("tags"):
            _logger.info("   Tags: %s", ", ".join(metadata["tags"]))

        # Show supported variants
        _logger.info("   Variants: %s", ", ".join(palettes.supported_variants))

    except Exception as e:
        _logger.error("❌ Error loading theme '%s': %s", theme_name, e)


def cmd_list(args):
    """List all available themes."""
    themes = list_themes()

    if not themes:
        _logger.info("No themes found.")
        return

    _logger.info("📚 Available themes (%d):", len(themes))
    for theme in themes:
        try:
            metadata = load_theme_metadata_from_yaml(theme)
            display_name = metadata.get("display_name", theme)
            description = metadata.get("description", "No description")
            variants = metadata.get("variants", {})
            variant_list = [v for v, enabled in variants.items() if enabled]

            _logger.info("  • %s (%s)", display_name, theme)
            _logger.info("    %s", description)
            _logger.info("    Variants: %s", ", ".join(variant_list))

        except Exception as e:
            _logger.error("  • %s (⚠️  Error loading metadata: %s)", theme, e)


def cmd_info(args):
    """Show detailed information about a theme."""
    show_theme_info(args.theme)


def cmd_export(args):
    """Export theme(s) to build directory."""

    # Determine build directory
    build_dir = Path(args.output) if args.output else None

    if args.all:
        _logger.info("🎨 Exporting all themes...")
        try:
            exported = ThemeExporter(build_dir).export_all_themes()

            _logger.info("✅ Successfully exported %d themes:", len(exported))
            for theme_name, variants in exported.items():
                _logger.info("  • %s: %s", theme_name, ", ".join(variants.keys()))

        except Exception as e:
            _logger.error("❌ Export failed: %s", e)
            sys.exit(1)

    else:
        # Export specific theme
        theme_name = args.theme
        variants = args.variants.split(",") if args.variants else None

        try:
            exported = ThemeExporter(build_dir).export_theme(theme_name, variants)

            _logger.info("✅ Successfully exported theme '%s':", theme_name)
            for variant, path in exported.items():
                _logger.info("  • %s: %s", variant, path)

        except Exception as e:
            _logger.error("❌ Export failed: %s", e)
            sys.exit(1)


def cmd_validate(args):
    """Validate theme configuration files."""
    theme_name = args.theme

    _logger.info("🔍 Validating theme: %s", theme_name)

    try:
        # Try to load metadata
        load_theme_metadata_from_yaml(theme_name)
        _logger.info("✅ theme.yaml: Valid")

        # Try to create palettes
        palettes = create_palettes(theme_name)
        _logger.info("✅ colorsystem.yaml: Valid")
        _logger.info("✅ mappings.yaml: Valid")

        # Show supported variants
        _logger.info(
            "✅ Supported variants: %s", ", ".join(palettes.supported_variants)
        )

        # Test palette instantiation
        for variant in palettes.supported_variants:
            palette_class = palettes.get_palette(variant)
            if palette_class:
                palette = palette_class()
                _logger.info("✅ %s palette: Valid (%s)", variant, palette.ID)

        _logger.info("✅ Theme '%s' is valid!", theme_name)

    except Exception as e:
        _logger.error("❌ Validation failed: %s", e)
        sys.exit(1)


def cmd_generate(args):
    """Generate a new theme using color generation algorithms."""
    generator = ThemeGenerator()

    # Check if theme already exists
    if generator.theme_exists(args.name) and not args.overwrite:
        _logger.error(
            "❌ Theme '%s' already exists. Use --overwrite to replace it.", args.name
        )
        sys.exit(1)

    try:
        if args.colors:
            # Generate theme from single colors for each palette
            _logger.info("🎨 Generating theme from individual colors...")

            # Parse colors
            if len(args.colors) != 6:
                _logger.error(
                    "❌ When using --colors, you must provide exactly 6 colors in this order:"
                )
                _logger.error("    Primary Secondary Error Success Warning Group")
                sys.exit(1)

            # Validate colors
            is_valid, error_msg = validate_input_colors(
                args.colors[0],  # primary
                args.colors[1],  # secondary
                args.colors[2],  # error
                args.colors[3],  # success
                args.colors[4],  # warning
                args.colors[5],  # group
            )

            if not is_valid:
                _logger.error(f"❌ {error_msg}")
                sys.exit(1)

            # Generate theme structure
            theme_data = generate_theme_from_colors(
                primary_color=args.colors[0],
                secondary_color=args.colors[1],
                error_color=args.colors[2],
                success_color=args.colors[3],
                warning_color=args.colors[4],
                group_initial_color=args.colors[5],
            )

            # Generate theme files
            files = generator.generate_theme_from_data(
                theme_name=args.name,
                theme_data=theme_data,
                display_name=args.display_name,
                description=args.description,
                author=args.author,
                tags=args.tags.split(",") if args.tags else None,
                overwrite=args.overwrite,
            )

        else:
            # Generate theme using algorithmic approach
            _logger.info("🎨 Generating theme using algorithmic color generation...")

            files = generator.generate_theme_from_palette(
                theme_name=args.name,
                palette_name=args.palette_name or args.name.replace("_", " ").title(),
                start_hue=args.start_hue,
                num_colors=args.num_colors,
                target_delta_e=args.target_delta_e,
                uniform=args.uniform,
                display_name=args.display_name,
                description=args.description,
                author=args.author,
                tags=args.tags.split(",") if args.tags else None,
                overwrite=args.overwrite,
            )

        _logger.info("✅ Theme '%s' generated successfully!", args.name)
        _logger.info("📁 Files created:")
        for file_type, file_path in files.items():
            _logger.info("  • %s: %s", file_type, file_path)

        # Show detailed analysis if requested
        if args.analyze:
            _logger.info("\n📊 Performing detailed theme analysis...")
            try:
                from themeweaver.core.palette import create_palettes

                palettes = create_palettes(args.name)
                _logger.info("✅ Theme validation: All files loaded successfully")
                _logger.info(
                    f"  Supported variants: {', '.join(palettes.supported_variants)}"
                )

                # Basic palette analysis
                for variant in palettes.supported_variants:
                    palette_class = palettes.get_palette(variant)
                    if palette_class:
                        palette = palette_class()
                        _logger.info(
                            f"  {variant.title()} palette: {palette.ID} (ID: {palette.ID})"
                        )

            except Exception as e:
                _logger.warning("⚠️  Could not perform detailed analysis: %s", e)

        _logger.info("💡 You can now use: themeweaver export --theme %s", args.name)

    except Exception as e:
        _logger.error("❌ Theme generation failed: %s", e)
        sys.exit(1)


def cmd_analyze(args):
    """Analyze color palettes and find optimal generation parameters."""
    from themeweaver.color_utils.color_analysis import (
        analyze_palette_lch,
        compare_with_generated,
        find_optimal_parameters,
        generate_inspired_palette,
    )
    from themeweaver.color_utils.common_palettes import (
        COMMON_PALETTES,
        get_palette_names,
    )
    from themeweaver.color_utils.palette_loaders import (
        load_palette_from_file,
        parse_palette_from_args,
        validate_palette_data,
    )

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


def cmd_interpolate(args):
    """Interpolate between two colors using various methods."""
    from themeweaver.color_utils.interpolation_analysis import analyze_interpolation
    from themeweaver.color_utils.interpolation_methods import (
        interpolate_colors,
        validate_gradient_uniqueness,
    )

    try:
        # Interpolate colors
        colors = interpolate_colors(
            args.start_color, args.end_color, args.steps, args.method, args.exponent
        )

        # Output based on format
        if args.output == "list":
            print("Interpolated colors:")
            for i, color in enumerate(colors):
                print(f"  {i}: {color}")

        elif args.output == "json":
            import json

            # Determine palette name
            if args.name:
                palette_name = args.name
            else:
                from themeweaver.color_utils.color_names import (
                    get_palette_name_from_color,
                )

                palette_name = get_palette_name_from_color(
                    args.start_color, creative=not args.simple_names
                )

            # Generate B-step structure
            palette_data = {}
            for i, color in enumerate(colors):
                step = i * 10
                palette_data[f"B{step}"] = color

            data = {"palette": {palette_name: palette_data}}
            print(json.dumps(data, indent=2))

        elif args.output == "yaml":
            import yaml

            if args.name:
                palette_name = args.name
            else:
                from themeweaver.color_utils.color_names import (
                    get_palette_name_from_color,
                )

                palette_name = get_palette_name_from_color(
                    args.start_color, creative=not args.simple_names
                )

            # Create YAML structure
            data = {palette_name: {}}
            for i, color in enumerate(colors):
                step = i * 10
                data[palette_name][f"B{step}"] = color

            # Add metadata as comments
            yaml_output = f"""# Generated color gradient using {args.method} interpolation
# From: {args.start_color} to {args.end_color}
# Steps: {args.steps}"""

            if args.method == "exponential":
                yaml_output += f"\n# Exponent: {args.exponent}"

            yaml_output += f"\n# Method: {args.method}\n\n"
            yaml_output += yaml.dump(data, default_flow_style=False, sort_keys=False)
            print(yaml_output)

        # Show analysis if requested
        if args.analyze:
            analyze_interpolation(colors, args.method)

        # Show validation if requested
        if args.validate:
            is_valid, duplicate_info = validate_gradient_uniqueness(colors, args.method)

            _logger.info("🔍 Gradient Validation (%s)", args.method.upper())

            if is_valid:
                _logger.info("✅ No duplicate colors found - gradient is valid")
                _logger.info("   Total colors: %d", len(colors))
                _logger.info("   Unique colors: %d", len(colors))
            else:
                _logger.warning("❌ Duplicate colors detected!")
                _logger.warning("   Total colors: %d", duplicate_info["total_colors"])
                _logger.warning("   Unique colors: %d", duplicate_info["unique_colors"])
                _logger.warning("   Duplicate count: %d", duplicate_info["count"])

    except Exception as e:
        _logger.error("❌ Interpolation failed: %s", e)
        sys.exit(1)


def cmd_groups(args):
    """Generate group-style color palettes."""
    from themeweaver.color_utils.color_analysis import analyze_chromatic_distances
    from themeweaver.color_utils.color_generation import generate_theme_colors

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


def main():
    """Main CLI entry point."""
    # Set up logging for CLI output
    setup_logging()

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
