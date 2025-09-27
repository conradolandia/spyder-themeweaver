"""
Theme generation command.
"""

import logging
from pathlib import Path
from typing import Any, List, Optional, Union

import yaml

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
from themeweaver.core.yaml_theme_loader import (
    load_theme_from_yaml,
    parse_theme_definition,
)

_logger = logging.getLogger(__name__)


def cmd_generate(args: Any) -> None:
    """Generate a new theme from individual colors or YAML definition."""
    # Use custom output directory if provided
    output_dir = (
        args.output_dir if hasattr(args, "output_dir") and args.output_dir else None
    )
    generator = ThemeGenerator(themes_dir=output_dir)

    # Check if we're using a YAML file for theme definition
    if hasattr(args, "from_yaml") and args.from_yaml:
        return _generate_from_yaml(args, generator)
    else:
        return _generate_from_colors(args, generator)


def _generate_from_yaml(args: Any, generator: ThemeGenerator) -> None:
    """Generate a theme from a YAML definition file."""
    yaml_path = Path(args.from_yaml)
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {yaml_path}")

    with operation_context("Theme generation from YAML"):
        _logger.info("🎨 Generating theme from YAML definition: %s", yaml_path)

        # Load and parse the YAML file
        try:
            theme_data = load_theme_from_yaml(yaml_path)
            parsed_data = parse_theme_definition(theme_data)
        except FileNotFoundError as e:
            raise ValueError(f"YAML file not found: {e}")
        except ValueError as e:
            raise ValueError(f"YAML validation error: {e}")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parsing error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error parsing YAML file: {e}")

        # Override theme name if specified in command line
        theme_name = args.name

        # Warn if YAML theme name differs from command line name
        yaml_theme_name = parsed_data.get("name")
        if yaml_theme_name and yaml_theme_name != theme_name:
            _logger.warning(
                f"⚠️  Theme name in YAML ('{yaml_theme_name}') differs from command line name ('{theme_name}'). "
                f"Using command line name: '{theme_name}'"
            )

        # Check if theme already exists
        validate_condition(
            not (
                generator.theme_exists(theme_name)
                and not parsed_data.get("overwrite", False)
            ),
            f"Theme '{theme_name}' already exists. Set 'overwrite: true' in YAML or use --overwrite.",
        )

        # Extract theme data
        colors = parsed_data["colors"]
        syntax_colors_dark = parsed_data.get("syntax_colors_dark")
        syntax_colors_light = parsed_data.get("syntax_colors_light")
        syntax_format = parsed_data.get("syntax_format")
        variants = parsed_data.get("variants", ["dark", "light"])
        display_name = parsed_data.get("display_name")
        description = parsed_data.get("description")
        author = parsed_data.get("author", "ThemeWeaver")
        tags = parsed_data.get("tags")
        overwrite = parsed_data.get("overwrite", False)

        # Validate colors
        is_valid, error_msg = validate_input_colors(
            colors[0],  # primary
            colors[1],  # secondary
            colors[2],  # error
            colors[3],  # success
            colors[4],  # warning
            colors[5],  # group
        )
        validate_condition(is_valid, error_msg)

        # Generate theme structure
        theme_data = generate_theme_from_colors(
            primary_color=colors[0],
            secondary_color=colors[1],
            error_color=colors[2],
            success_color=colors[3],
            warning_color=colors[4],
            group_initial_color=colors[5],
            syntax_colors_dark=syntax_colors_dark,
            syntax_colors_light=syntax_colors_light,
            syntax_format=syntax_format,
            variants=variants,
        )

        # Generate theme files
        files = generator.generate_theme_from_data(
            theme_name=theme_name,
            theme_data=theme_data,
            display_name=display_name,
            description=description,
            author=author,
            tags=tags,
            overwrite=overwrite,
        )

        _logger.info(
            "✅ Theme [%s] generated successfully from YAML definition!", theme_name
        )
        _logger.info("📁 Files created:")
        for file_type, _file_path in files.items():
            _logger.info("   -> %s", file_type)

        # Show the output directory information
        output_path = generator.themes_dir / theme_name
        _logger.info(
            "📁 [%s]: yaml theme ready at -> %s",
            theme_name,
            str(output_path.resolve()),
        )

        # Show export command hint
        custom_dir = hasattr(args, "output_dir") and args.output_dir
        if custom_dir:
            _logger.info(
                "💡 You can now use: themeweaver export --theme %s --theme-dir %s",
                theme_name,
                str(generator.themes_dir.resolve()),
            )
        else:
            _logger.info(
                "💡 You can now use: themeweaver export --theme %s",
                theme_name,
            )


def _generate_from_colors(args: Any, generator: ThemeGenerator) -> None:
    """Generate a theme from individual colors."""
    # Check if theme already exists
    validate_condition(
        not (generator.theme_exists(args.name) and not args.overwrite),
        f"Theme '{args.name}' already exists. Use --overwrite to replace it.",
    )

    with operation_context("Theme generation from colors"):
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

        # Generate theme structure
        theme_data = generate_theme_from_colors(
            primary_color=args.colors[0],
            secondary_color=args.colors[1],
            error_color=args.colors[2],
            success_color=args.colors[3],
            warning_color=args.colors[4],
            group_initial_color=args.colors[5],
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

        _logger.info("✅ Theme [%s] generated successfully!", args.name)
        _logger.info("📁 Files created:")
        for file_type, _file_path in files.items():
            _logger.info("   -> %s", file_type)

        # Show the output directory information
        output_path = generator.themes_dir / args.name
        _logger.info(
            "📁 [%s]: yaml theme ready at -> %s",
            args.name,
            str(output_path.resolve()),
        )

        # Show export command hint
        custom_dir = hasattr(args, "output_dir") and args.output_dir
        if custom_dir:
            _logger.info(
                "💡 You can now use: themeweaver export --theme %s --theme-dir %s",
                args.name,
                str(generator.themes_dir.resolve()),
            )
        else:
            _logger.info(
                "💡 You can now use: themeweaver export --theme %s",
                args.name,
            )
