"""
Color gradient generation command.

This command generates a 16-color lightness gradient from a single color,
interpolating from black to the color to white using various methods.
"""

import logging
from typing import Any, List

import yaml

from themeweaver.cli.error_handling import operation_context
from themeweaver.color_utils.interpolation_analysis import analyze_interpolation
from themeweaver.color_utils.interpolation_methods import (
    interpolate_colors,
    validate_gradient_uniqueness,
)
from themeweaver.color_utils.palette_generators import (
    generate_lightness_gradient_from_color,
)

_logger = logging.getLogger(__name__)


def _generate_gradient_with_method(
    color: str, method: str, exponent: float = 2
) -> List[str]:
    """
    Generate a 16-color gradient from black to color to white using the specified method.

    Args:
        color: Base hex color
        method: Interpolation method
        exponent: Exponent for exponential interpolation

    Returns:
        List of 16 hex colors
    """
    # Normalize color to include # prefix if missing
    normalized_color = color.upper() if color.startswith("#") else f"#{color.upper()}"

    # Use existing LCH lightness method for backward compatibility
    if method == "lch-lightness":
        return generate_lightness_gradient_from_color(normalized_color)

    # For other methods, interpolate from black to color to white
    # We need exactly 16 colors: black + 7 intermediate + color + 7 intermediate + white
    # Split into two segments with 9 steps each to get enough colors

    # Interpolate from black to color (9 steps: black + 7 intermediate + color)
    black_to_color = interpolate_colors(
        "#000000", normalized_color, 9, method, exponent
    )

    # Interpolate from color to white (9 steps: color + 7 intermediate + white)
    color_to_white = interpolate_colors(
        normalized_color, "#FFFFFF", 9, method, exponent
    )

    # Combine to get exactly 16 colors:
    # - Take first 8 from black->color: black + 7 intermediate (8 colors)
    # - Add the base color itself (1 color)
    # - Take last 7 from color->white: 6 intermediate + white (7 colors, skip duplicate color at position 0)
    colors = black_to_color[:8]  # black + 7 intermediate (8 colors)
    colors.append(normalized_color)  # the base color (1 color)
    colors.extend(
        color_to_white[1:8]
    )  # 6 intermediate + white (7 colors, skip duplicate color)

    # Ensure we have exactly 16 colors
    if len(colors) != 16:
        # If we have more, trim; if less, we need to adjust
        if len(colors) > 16:
            colors = colors[:16]
        else:
            # Pad if needed (shouldn't happen, but safety check)
            while len(colors) < 16:
                colors.append(colors[-1])

    # Ensure first is black and last is white
    colors[0] = "#000000"
    colors[15] = "#FFFFFF"

    return colors


def cmd_gradient(args: Any) -> None:
    """Generate a 16-color gradient from a single color using various methods."""
    # Suppress operation context logging when output format is specified
    quiet = args.output in ("json", "yaml", "list")

    if quiet:
        # Generate gradient without operation context logging
        colors = _generate_gradient_with_method(args.color, args.method, args.exponent)
    else:
        with operation_context("Gradient generation"):
            # Generate gradient
            colors = _generate_gradient_with_method(
                args.color, args.method, args.exponent
            )

    # Determine method description for output
    method_descriptions = {
        "lch-lightness": "LCH lightness interpolation (black -> color -> white)",
        "linear": "Linear interpolation",
        "cubic": "Cubic interpolation (smoothstep)",
        "exponential": f"Exponential interpolation (exponent: {args.exponent})",
        "sine": "Sine-based interpolation",
        "cosine": "Cosine-based interpolation",
        "hermite": "Hermite polynomial interpolation",
        "quintic": "Quintic polynomial interpolation",
        "hsv": "HSV color space interpolation",
        "lch": "LCH color space interpolation",
    }
    method_desc = method_descriptions.get(args.method, args.method)

    # Output based on format
    if args.output == "list":
        print(f"Generated gradient (16 colors) using {args.method}:")
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
                args.color, creative=not args.simple_names, quiet=True
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
                args.color, creative=not args.simple_names, quiet=True
            )

        # Normalize base color for comparison
        normalized_base_color = (
            args.color.upper()
            if args.color.startswith("#")
            else f"#{args.color.upper()}"
        )

        # Find the position of the base color in the gradient
        base_color_position = None
        for i, color in enumerate(colors):
            if color.upper() == normalized_base_color:
                base_color_position = i
                break

        # Create YAML structure
        data = {palette_name: {}}
        for i, color in enumerate(colors):
            step = i * 10
            data[palette_name][f"B{step}"] = color

        # Add metadata as comments
        yaml_output = f"""# Generated 16-color gradient from single color
# Base color: {args.color}
# Base color position: {base_color_position if base_color_position is not None else "N/A"} (0-15)
# Method: {method_desc}
# Total colors: 16
"""

        if args.method == "exponential":
            yaml_output += f"# Exponent: {args.exponent}\n"

        yaml_output += "\n"
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
