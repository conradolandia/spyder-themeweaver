"""
Color interpolation command.
"""

import logging
from typing import Any

from themeweaver.cli.error_handling import operation_context
from themeweaver.color_utils.interpolation_analysis import analyze_interpolation
from themeweaver.color_utils.interpolation_methods import (
    interpolate_colors,
    validate_gradient_uniqueness,
)

_logger = logging.getLogger(__name__)


def cmd_interpolate(args: Any) -> None:
    """Interpolate between two colors using various methods."""
    # Suppress operation context logging when output format is specified
    quiet = args.output in ("json", "yaml", "list")

    if quiet:
        # Interpolate colors without operation context logging
        colors = interpolate_colors(
            args.start_color, args.end_color, args.steps, args.method, args.exponent
        )
    else:
        with operation_context("Color interpolation"):
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
                args.start_color, creative=not args.simple_names, quiet=True
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
                args.start_color, creative=not args.simple_names, quiet=True
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
