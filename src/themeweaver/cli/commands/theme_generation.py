"""
Theme generation command.
"""

import logging

from themeweaver.cli.error_handling import (
    handle_invalid_count_error,
    operation_context,
    validate_condition,
)
from themeweaver.color_utils.theme_generator_utils import (
    generate_theme_from_colors,
    validate_input_colors,
)
from themeweaver.core.theme_generator import ThemeGenerator

_logger = logging.getLogger(__name__)


def cmd_generate(args):
    """Generate a new theme using color generation algorithms."""
    generator = ThemeGenerator()

    # Check if theme already exists
    validate_condition(
        not (generator.theme_exists(args.name) and not args.overwrite),
        f"Theme '{args.name}' already exists. Use --overwrite to replace it.",
    )

    with operation_context("Theme generation"):
        if args.colors:
            # Generate theme from single colors for each palette
            _logger.info("🎨 Generating theme from individual colors...")

            # Parse colors
            handle_invalid_count_error(6, len(args.colors), "colors")

            # Validate colors
            is_valid, error_msg = validate_input_colors(
                args.colors[0],  # primary
                args.colors[1],  # secondary
                args.colors[2],  # error
                args.colors[3],  # success
                args.colors[4],  # warning
                args.colors[5],  # group
            )

            validate_condition(is_valid, error_msg)

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
