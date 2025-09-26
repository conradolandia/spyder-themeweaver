"""
Theme generation command.
"""

import logging
from typing import Any, List, Optional, Union

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


def cmd_generate(args: Any) -> None:
    """Generate a new theme from individual colors."""
    generator = ThemeGenerator()

    # Check if theme already exists
    validate_condition(
        not (generator.theme_exists(args.name) and not args.overwrite),
        f"Theme '{args.name}' already exists. Use --overwrite to replace it.",
    )

    with operation_context("Theme generation"):
        # Require colors for theme generation
        validate_condition(
            args.colors is not None,
            "Theme generation requires --colors argument. Please provide 6 colors: primary, secondary, error, success, warning, group.",
        )

        # Generate theme from single colors for each palette
        _logger.info("🎨 Generating theme from individual colors...")

        # Parse colors
        handle_invalid_count_error(6, len(args.colors), "colors")

        # Handle syntax colors - support for dark/light variants
        syntax_colors_dark: Optional[Union[str, List[str]]] = None
        syntax_colors_light: Optional[Union[str, List[str]]] = None

        # Check for new variant-specific parameters first
        if hasattr(args, "syntax_colors_dark") and args.syntax_colors_dark:
            if len(args.syntax_colors_dark) == 1:
                syntax_colors_dark = args.syntax_colors_dark[0]
            elif len(args.syntax_colors_dark) == 16:
                syntax_colors_dark = args.syntax_colors_dark
            else:
                raise ValueError(
                    f"Syntax colors dark must be either 1 color (for auto-generation) or 16 colors (for custom palette), got {len(args.syntax_colors_dark)}"
                )

        if hasattr(args, "syntax_colors_light") and args.syntax_colors_light:
            if len(args.syntax_colors_light) == 1:
                syntax_colors_light = args.syntax_colors_light[0]
            elif len(args.syntax_colors_light) == 16:
                syntax_colors_light = args.syntax_colors_light
            else:
                raise ValueError(
                    f"Syntax colors light must be either 1 color (for auto-generation) or 16 colors (for custom palette), got {len(args.syntax_colors_light)}"
                )

        # Legacy support: if --syntax-colors is provided and no variant-specific colors, use for dark
        if args.syntax_colors and not syntax_colors_dark and not syntax_colors_light:
            if len(args.syntax_colors) == 1:
                syntax_colors_dark = args.syntax_colors[0]
            elif len(args.syntax_colors) == 16:
                syntax_colors_dark = args.syntax_colors
            else:
                raise ValueError(
                    f"Syntax colors must be either 1 color (for auto-generation) or 16 colors (for custom palette), got {len(args.syntax_colors)}"
                )

        # Validate colors - validate both syntax color variants if provided
        is_valid, error_msg = True, ""

        # Validate main colors
        is_valid, error_msg = validate_input_colors(
            args.colors[0],  # primary
            args.colors[1],  # secondary
            args.colors[2],  # error
            args.colors[3],  # success
            args.colors[4],  # warning
            args.colors[5],  # group
        )

        # Validate syntax colors if provided
        if is_valid and syntax_colors_dark:
            is_valid, error_msg = validate_input_colors(
                args.colors[0],
                args.colors[1],
                args.colors[2],
                args.colors[3],
                args.colors[4],
                args.colors[5],
                syntax_colors=syntax_colors_dark,
            )

        if is_valid and syntax_colors_light:
            is_valid, error_msg = validate_input_colors(
                args.colors[0],
                args.colors[1],
                args.colors[2],
                args.colors[3],
                args.colors[4],
                args.colors[5],
                syntax_colors=syntax_colors_light,
            )

        validate_condition(is_valid, error_msg)

        # Handle variants parameter
        requested_variants = getattr(args, "variants", None)
        if requested_variants is None:
            # Default: generate both variants
            variants_to_generate = ["dark", "light"]
        else:
            # Use requested variants
            variants_to_generate = requested_variants

        # Determine if legacy syntax_colors was used
        legacy_syntax_colors = None
        was_legacy = (
            args.syntax_colors
            and not (hasattr(args, "syntax_colors_dark") and args.syntax_colors_dark)
            and not (hasattr(args, "syntax_colors_light") and args.syntax_colors_light)
        )
        if was_legacy:
            # This was originally legacy, but we converted it to syntax_colors_dark
            legacy_syntax_colors = args.syntax_colors
            # Don't pass syntax_colors_dark when using legacy
            syntax_colors_dark = None

        # Generate theme structure
        theme_data = generate_theme_from_colors(
            primary_color=args.colors[0],
            secondary_color=args.colors[1],
            error_color=args.colors[2],
            success_color=args.colors[3],
            warning_color=args.colors[4],
            group_initial_color=args.colors[5],
            syntax_colors=legacy_syntax_colors,
            syntax_colors_dark=syntax_colors_dark,
            syntax_colors_light=syntax_colors_light,
            syntax_format=getattr(args, "syntax_format", None),
            variants=variants_to_generate,
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
