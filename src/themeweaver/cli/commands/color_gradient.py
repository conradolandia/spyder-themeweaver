"""
Color gradient generation command.

This command generates a 16-color lightness gradient from a single color,
interpolating from black to the color to white in LCH color space.
"""

import logging
from typing import Any

import yaml

from themeweaver.cli.error_handling import operation_context
from themeweaver.color_utils.interpolation_analysis import analyze_interpolation
from themeweaver.color_utils.interpolation_methods import validate_gradient_uniqueness
from themeweaver.color_utils.palette_generators import (
    generate_lightness_gradient_from_color,
)

_logger = logging.getLogger(__name__)


def cmd_gradient(args: Any) -> None:
    """Generate a 16-color lightness gradient from a single color."""
    with operation_context("Lightness gradient generation"):
        # Generate gradient
        colors = generate_lightness_gradient_from_color(args.color)

        # Output based on format
        if args.output == "list":
            print("Generated lightness gradient (16 colors):")
            for i, color in enumerate(colors):
                print(f"  B{i * 10}: {color}")

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
                    args.color, creative=not args.simple_names
                )

            # Generate B-step structure
            palette_data = {}
            for i, color in enumerate(colors):
                step = i * 10
                palette_data[f"B{step}"] = color

            data = {"palette": {palette_name: palette_data}}
            print(json.dumps(data, indent=2))

        elif args.output == "yaml":
            if args.name:
                palette_name = args.name
            else:
                from themeweaver.color_utils.color_names import (
                    get_palette_name_from_color,
                )

                palette_name = get_palette_name_from_color(
                    args.color, creative=not args.simple_names
                )

            # Create YAML structure
            data = {palette_name: {}}
            for i, color in enumerate(colors):
                step = i * 10
                data[palette_name][f"B{step}"] = color

            # Add metadata as comments
            yaml_output = f"""# Generated 16-color lightness gradient from single color
# Base color: {args.color}
# Method: LCH lightness interpolation (black -> color -> white)
# Total colors: 16

"""
            yaml_output += yaml.dump(data, default_flow_style=False, sort_keys=False)
            print(yaml_output)

        # Show analysis if requested
        if args.analyze:
            analyze_interpolation(colors, "lch-lightness")

        # Show validation if requested
        if args.validate:
            is_valid, duplicate_info = validate_gradient_uniqueness(
                colors, "lch-lightness"
            )

            _logger.info("🔍 Gradient Validation (LCH Lightness)")

            if is_valid:
                _logger.info("✅ No duplicate colors found - gradient is valid")
                _logger.info("   Total colors: %d", len(colors))
                _logger.info("   Unique colors: %d", len(colors))
            else:
                _logger.warning("❌ Duplicate colors detected!")
                _logger.warning("   Total colors: %d", duplicate_info["total_colors"])
                _logger.warning("   Unique colors: %d", duplicate_info["unique_colors"])
                _logger.warning("   Duplicate count: %d", duplicate_info["count"])
