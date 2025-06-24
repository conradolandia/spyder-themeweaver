"""
Command-line interface for ThemeWeaver.

This module provides CLI commands for generating, exporting, and managing themes.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from themeweaver.core.exporter import ThemeExporter
from themeweaver.core.palette import create_palettes
from themeweaver.core.colorsystem import load_theme_metadata_from_yaml


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

        print(f"📋 Theme: {metadata.get('display_name', theme_name)}")
        print(f"   Name: {theme_name}")
        print(f"   Description: {metadata.get('description', 'No description')}")
        print(f"   Author: {metadata.get('author', 'Unknown')}")
        print(f"   Version: {metadata.get('version', 'Unknown')}")
        print(f"   License: {metadata.get('license', 'Unknown')}")

        if metadata.get("url"):
            print(f"   URL: {metadata['url']}")

        if metadata.get("tags"):
            print(f"   Tags: {', '.join(metadata['tags'])}")

        # Show supported variants
        print(f"   Variants: {', '.join(palettes.supported_variants)}")

    except Exception as e:
        print(f"❌ Error loading theme '{theme_name}': {e}")


def cmd_list(args):
    """List all available themes."""
    themes = list_themes()

    if not themes:
        print("No themes found.")
        return

    print(f"📚 Available themes ({len(themes)}):")
    for theme in themes:
        try:
            metadata = load_theme_metadata_from_yaml(theme)
            display_name = metadata.get("display_name", theme)
            description = metadata.get("description", "No description")
            variants = metadata.get("variants", {})
            variant_list = [v for v, enabled in variants.items() if enabled]

            print(f"  • {display_name} ({theme})")
            print(f"    {description}")
            print(f"    Variants: {', '.join(variant_list)}")

        except Exception as e:
            print(f"  • {theme} (⚠️  Error loading metadata: {e})")


def cmd_info(args):
    """Show detailed information about a theme."""
    show_theme_info(args.theme)


def cmd_export(args):
    """Export theme(s) to build directory."""

    # Determine build directory
    build_dir = Path(args.output) if args.output else None

    if args.all:
        print("🎨 Exporting all themes...")
        try:
            exported = ThemeExporter(build_dir).export_all_themes()

            print(f"✅ Successfully exported {len(exported)} themes:")
            for theme_name, variants in exported.items():
                print(f"  • {theme_name}: {', '.join(variants.keys())}")

        except Exception as e:
            print(f"❌ Export failed: {e}")
            sys.exit(1)

    else:
        # Export specific theme
        theme_name = args.theme
        variants = args.variants.split(",") if args.variants else None

        try:
            exported = ThemeExporter(build_dir).export_theme(theme_name, variants)

            print(f"✅ Successfully exported theme '{theme_name}':")
            for variant, path in exported.items():
                print(f"  • {variant}: {path}")

        except Exception as e:
            print(f"❌ Export failed: {e}")
            sys.exit(1)


def cmd_validate(args):
    """Validate theme configuration files."""
    theme_name = args.theme

    print(f"🔍 Validating theme: {theme_name}")

    try:
        # Try to load metadata
        load_theme_metadata_from_yaml(theme_name)
        print("✅ theme.yaml: Valid")

        # Try to create palettes
        palettes = create_palettes(theme_name)
        print("✅ colorsystem.yaml: Valid")
        print("✅ mappings.yaml: Valid")

        # Show supported variants
        print(f"✅ Supported variants: {', '.join(palettes.supported_variants)}")

        # Test palette instantiation
        for variant in palettes.supported_variants:
            palette_class = palettes.get_palette(variant)
            if palette_class:
                palette = palette_class()
                print(f"✅ {variant} palette: Valid ({palette.ID})")

        print(f"✅ Theme '{theme_name}' is valid!")

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
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
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
