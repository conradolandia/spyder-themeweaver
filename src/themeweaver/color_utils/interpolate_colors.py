"""
Color interpolation CLI tool with multiple methods and color spaces.

This script interpolates between two hex colors using various mathematical interpolation
methods and color spaces. Different methods operate in different color spaces:

- RGB-based methods (linear, cubic, exponential, sine, cosine, hermite, quintic):
  Interpolate directly in RGB space using mathematical curves

- Color space methods (hsv, lch):
  Convert to respective color space, interpolate, then convert back

- Perceptual methods (lch):
  Use LCH color space for perceptually uniform color transitions

The analysis feature always shows perceptual metrics (Delta E) regardless of
interpolation method, allowing comparison of perceptual uniformity across methods.

For Spyder themes, use the --spyder flag to generate 16-color palettes with
B0 (black) and B150 (white) endpoints, with user colors at B10 (dark) and B140 (light).
"""

import argparse
import sys

from themeweaver.color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsv,
    hsv_to_rgb,
    lch_to_hex,
    rgb_to_lch,
    calculate_delta_e,
    get_color_info,
    classify_color_lightness,
    is_color_suitable_for_theme,
)

# color_names import moved to where it's used to avoid import issues
from themeweaver.color_utils.interpolation_methods import (
    linear_interpolate,
    circular_interpolate,
    cubic_interpolate,
    exponential_interpolate,
    sine_interpolate,
    cosine_interpolate,
    hermite_interpolate,
    quintic_interpolate,
)


def interpolate_colors(start_hex, end_hex, steps, method="linear", exponent=2):
    """
    Interpolate between two hex colors using various methods and color spaces.

    Args:
        start_hex: Starting hex color (e.g., '#FF0000')
        end_hex: Ending hex color (e.g., '#0000FF')
        steps: Number of interpolation steps (including start and end)
        method: Interpolation method - see below for details
        exponent: Exponent for exponential interpolation (default: 2)

    Methods:
        RGB-based (operate directly in RGB color space):
            - linear: Simple linear interpolation
            - cubic: Smooth acceleration/deceleration (smoothstep)
            - exponential: Exponential curve with configurable exponent
            - sine: Sine-based easing curve
            - cosine: Cosine-based easing curve
            - hermite: Hermite polynomial interpolation
            - quintic: Very smooth 5th-degree polynomial

        Color space methods (convert to color space, interpolate, convert back):
            - hsv: Interpolate in HSV space (good for natural color transitions)
            - lch: Interpolate in LCH space (perceptually uniform)

    Returns:
        List of hex color strings with interpolated colors

    Note:
        - LCH method provides the most perceptually uniform results
        - HSV method avoids the "muddy colors" problem of RGB interpolation
        - RGB methods are fastest but may produce less natural color transitions
    """
    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)

    colors = []

    if method == "hsv":
        # Convert to HSV for more natural color transitions
        start_hsv = rgb_to_hsv(start_rgb)
        end_hsv = rgb_to_hsv(end_rgb)

        for i in range(steps):
            factor = i / (steps - 1) if steps > 1 else 0

            # Interpolate in HSV space with proper hue wrapping
            h = circular_interpolate(start_hsv[0] * 360, end_hsv[0] * 360, factor) / 360
            s = linear_interpolate(start_hsv[1], end_hsv[1], factor)
            v = linear_interpolate(start_hsv[2], end_hsv[2], factor)

            # Convert back to RGB
            rgb = hsv_to_rgb((h, s, v))
            colors.append(rgb_to_hex(rgb))

    elif method == "lch":
        # LCH interpolation for perceptually uniform colors

        start_lch = rgb_to_lch(start_rgb)
        end_lch = rgb_to_lch(end_rgb)

        for i in range(steps):
            factor = i / (steps - 1) if steps > 1 else 0

            # Interpolate in LCH space with proper hue wrapping
            lightness = linear_interpolate(start_lch[0], end_lch[0], factor)
            chroma = linear_interpolate(start_lch[1], end_lch[1], factor)
            hue = circular_interpolate(start_lch[2], end_lch[2], factor)

            color_hex = lch_to_hex(lightness, chroma, hue)
            colors.append(color_hex)

    else:
        # RGB-based interpolation methods
        for i in range(steps):
            factor = i / (steps - 1) if steps > 1 else 0

            # Apply the chosen interpolation method
            if method == "cubic":
                interp_factor = cubic_interpolate(0, 1, factor)
            elif method == "exponential":
                interp_factor = exponential_interpolate(0, 1, factor, exponent)
            elif method == "sine":
                interp_factor = sine_interpolate(0, 1, factor)
            elif method == "cosine":
                interp_factor = cosine_interpolate(0, 1, factor)
            elif method == "hermite":
                interp_factor = hermite_interpolate(0, 1, factor)
            elif method == "quintic":
                interp_factor = quintic_interpolate(0, 1, factor)
            else:
                interp_factor = factor  # fallback to linear

            # Interpolate each RGB component
            r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * interp_factor
            g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * interp_factor
            b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * interp_factor

            colors.append(rgb_to_hex((r, g, b)))

    return colors


def interpolate_colors_spyder(dark_color, light_color, method="linear", exponent=2):
    """
    Generate a 16-color Spyder-compatible palette.

    Spyder palettes have specific requirements:
    - B0 must be black (#000000)
    - B150 must be white (#FFFFFF)
    - User's dark color goes to B10
    - User's light color goes to B140
    - B20-B130 are interpolated between the user colors (12 intermediate steps)

    Args:
        dark_color: Dark hex color (will be placed at B10)
        light_color: Light hex color (will be placed at B140)
        method: Interpolation method for intermediate colors
        exponent: Exponent for exponential interpolation

    Returns:
        List of 16 hex colors for B0, B10, B20, ..., B140, B150
    """
    # Fixed endpoints
    black = "#000000"
    white = "#FFFFFF"

    # Interpolate 14 colors from user's dark to user's light color
    # This will give us: dark_color, 12 intermediate colors, light_color (14 total)
    intermediate_colors = interpolate_colors(
        dark_color, light_color, 14, method, exponent
    )

    # Build the full 16-color palette
    # B0 = black, B10-B140 = user colors + interpolated (14 colors), B150 = white
    spyder_palette = [black]  # B0
    spyder_palette.extend(intermediate_colors)  # B10-B140 (14 colors)
    spyder_palette.append(white)  # B150

    return spyder_palette


def validate_spyder_colors(dark_color, light_color):
    """
    Validate that colors are appropriate for Spyder theme generation.

    Uses robust three-stage classification to ensure colors are clearly
    distinguishable and suitable for theme generation. Rejects ambiguous
    "medium" colors that could cause readability issues.

    Args:
        dark_color: Should be a clearly dark color (L < 35)
        light_color: Should be a clearly light color (L > 65)

    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Check if colors are valid hex
        hex_to_rgb(dark_color)
        hex_to_rgb(light_color)

        # Classify colors using the robust three-stage system
        dark_classification = classify_color_lightness(dark_color)
        light_classification = classify_color_lightness(light_color)

        # Check for clearly inappropriate classifications
        if dark_classification == "light" and light_classification == "dark":
            return (
                False,
                f"Colors appear to be swapped: '{dark_color}' is light (L > 65) but '{light_color}' is dark (L < 35). Please swap them.",
            )

        # Check if dark color is suitable
        if not is_color_suitable_for_theme(dark_color, "dark"):
            if dark_classification == "medium":
                return (
                    False,
                    f"Dark color '{dark_color}' is too ambiguous (medium lightness). Use a clearly dark color (L < 35).",
                )
            else:  # must be "light"
                return (
                    False,
                    f"Dark color '{dark_color}' is actually light (L > 65). Use a dark color (L < 35).",
                )

        # Check if light color is suitable
        if not is_color_suitable_for_theme(light_color, "light"):
            if light_classification == "medium":
                return (
                    False,
                    f"Light color '{light_color}' is too ambiguous (medium lightness). Use a clearly light color (L > 65).",
                )
            else:  # must be "dark"
                return (
                    False,
                    f"Light color '{light_color}' is actually dark (L < 35). Use a light color (L > 65).",
                )

        return True, ""

    except ValueError as e:
        return False, str(e)


def analyze_interpolation(colors, method="unknown"):
    """
    Analyze the color interpolation for perceptual quality.

    This analysis shows perceptual metrics (Delta E) regardless of the interpolation
    method used, allowing comparison of how different methods affect perceptual uniformity.

    Args:
        colors: List of hex color strings to analyze
        method: The interpolation method used (for context in output)
    """
    if len(colors) < 2:
        return

    print(f"\n=== Interpolation Analysis ({method.upper()}) ===")

    # Add method-specific context
    if method == "lch":
        print("Note: LCH interpolation optimizes for perceptual uniformity")
    elif method == "hsv":
        print(
            "Note: HSV interpolation avoids 'muddy colors' but may not be perceptually uniform"
        )
    elif method in [
        "linear",
        "cubic",
        "exponential",
        "sine",
        "cosine",
        "hermite",
        "quintic",
    ]:
        print("Note: RGB-based interpolation may show perceptual non-uniformity")

    for i, color in enumerate(colors):
        info = get_color_info(color)
        hsv_deg = info["hsv_degrees"]

        analysis_str = f"Step {i + 1:2d}: {color} | HSV({hsv_deg[0]:6.1f}°, {hsv_deg[1]:.2f}, {hsv_deg[2]:.2f})"

        if info.get("lch"):
            lch = info["lch"]
            analysis_str += f" | LCH({lch[0]:.1f}, {lch[1]:.1f}, {lch[2]:.1f}°)"

        print(analysis_str)

    # Delta E analysis
    if len(colors) > 1:
        print("\n=== Perceptual Distance Analysis ===")

        delta_es = []
        for i in range(len(colors) - 1):
            delta_e = calculate_delta_e(colors[i], colors[i + 1])
            if delta_e is not None:
                delta_es.append(delta_e)
                print(f"Step {i + 1} → {i + 2}: ΔE = {delta_e:.1f}")

        if delta_es:
            avg_delta_e = sum(delta_es) / len(delta_es)
            min_delta_e = min(delta_es)
            max_delta_e = max(delta_es)

            # Calculate standard deviation
            variance = sum((x - avg_delta_e) ** 2 for x in delta_es) / len(delta_es)
            std_dev = variance**0.5

            print("\nPerceptual Statistics:")
            print(f"  Average ΔE: {avg_delta_e:.1f}")
            print(f"  Min ΔE: {min_delta_e:.1f}")
            print(f"  Max ΔE: {max_delta_e:.1f}")
            print(f"  Std Dev: {std_dev:.1f}")

            # Quality assessment with method-specific interpretation
            if std_dev < 3:
                print("  ✅ Very uniform perceptual spacing")
                if method != "lch":
                    print("     (Excellent result for non-LCH method!)")
            elif std_dev < 5:
                print("  ✅ Good perceptual spacing")
                if method == "lch":
                    print("     (Expected for LCH method)")
                else:
                    print("     (Good result for RGB/HSV method)")
            else:
                print("  ⚠️  Uneven perceptual spacing")
                if method == "lch":
                    print("     (Unexpected - LCH should be more uniform)")
                elif method == "hsv":
                    print("     (Consider LCH method for perceptual uniformity)")
                else:
                    print("     (Consider LCH or HSV methods for better uniformity)")


def _get_method_description(method):
    """Get a brief description of the interpolation method."""
    descriptions = {
        "linear": "simple linear interpolation",
        "cubic": "smooth acceleration/deceleration",
        "exponential": "exponential curve",
        "sine": "sine-based easing curve",
        "cosine": "cosine-based easing curve",
        "hermite": "hermite polynomial interpolation",
        "quintic": "very smooth 5th-degree polynomial",
        "hsv": "HSV color space interpolation",
        "lch": "perceptually uniform LCH color space",
    }
    return descriptions.get(method, "unknown method")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Interpolate between two hex colors with various interpolation methods.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s '#93A1A1' '#EEE8D5' 8                                    # Basic linear interpolation
  %(prog)s '#FF0000' '#0000FF' 10 --method hsv                      # HSV color space (natural transitions)
  %(prog)s '#FF0000' '#0000FF' 8 --method lch --analyze             # LCH color space (perceptually uniform)
  %(prog)s '#93A1A1' '#EEE8D5' 5 --method cubic                     # Smooth RGB curves
  %(prog)s '#FF0000' '#00FF00' 8 --method exponential --exponent 3  # Exponential RGB curves
  %(prog)s '#FF0000' '#0000FF' 8 --method quintic                   # Very smooth RGB curves
  %(prog)s '#FF0000' '#0000FF' 5 --method hermite --format both     # Hermite interpolation with RGB output
  %(prog)s '#93A1A1' '#EEE8D5' 8 --output yaml --method lch         # Generate YAML palette (creative automatic naming: "RigidSilentFilm")
  %(prog)s '#93A1A1' '#EEE8D5' 8 --output yaml --name "MyPalette"   # Generate YAML palette with custom name
  %(prog)s '#93A1A1' '#EEE8D5' 8 --output yaml --simple-names       # Generate YAML palette with simple color names
  %(prog)s '#002B36' '#EEE8D5' --spyder --method lch                # Generate 16-color Spyder palette
        """,
    )

    parser.add_argument("start_color", help="Starting hex color (with or without #)")

    parser.add_argument("end_color", help="Ending hex color (with or without #)")

    parser.add_argument(
        "steps",
        type=int,
        nargs="?",
        default=None,
        help="Number of interpolation steps (must be >= 2). Not used with --spyder.",
    )

    parser.add_argument(
        "-m",
        "--method",
        choices=[
            "linear",
            "cubic",
            "exponential",
            "sine",
            "cosine",
            "hermite",
            "quintic",  # RGB-based
            "hsv",
            "lch",  # Color space methods
        ],
        default="linear",
        help="Interpolation method: RGB-based (linear, cubic, exponential, sine, cosine, hermite, quintic) or color space (hsv, lch) (default: linear)",
    )

    parser.add_argument(
        "-e",
        "--exponent",
        type=float,
        default=2.0,
        help="Exponent for exponential interpolation (default: 2.0)",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["hex", "rgb", "both"],
        default="hex",
        help="Output format (default: hex)",
    )

    parser.add_argument(
        "-o",
        "--output",
        choices=["list", "json", "yaml"],
        default="list",
        help="Output style (default: list)",
    )

    parser.add_argument(
        "--spyder",
        action="store_true",
        help="Generate 16-color Spyder-compatible palette (B0=black, B150=white, user colors at B10/B140)",
    )

    parser.add_argument(
        "--name",
        type=str,
        default="",
        help="Name of the palette",
    )

    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Show detailed color analysis including perceptual metrics",
    )

    parser.add_argument(
        "--simple-names",
        action="store_true",
        help="Use simple color names instead of creative adjective+color combinations",
    )

    args = parser.parse_args()

    # Handle Spyder mode
    if args.spyder:
        # Validate colors for Spyder mode
        is_valid, error_msg = validate_spyder_colors(args.start_color, args.end_color)
        if not is_valid:
            print(f"Error: {error_msg}", file=sys.stderr)
            print(
                "Tip: Use a dark color (like #002B36) as the first color and a light color (like #EEE8D5) as the second.",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            colors = interpolate_colors_spyder(
                args.start_color, args.end_color, args.method, args.exponent
            )
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Regular mode - validate steps
        if args.steps is None:
            print(
                "Error: Number of steps is required for regular interpolation (not using --spyder).",
                file=sys.stderr,
            )
            sys.exit(1)

        if args.steps < 2:
            print("Error: Number of steps must be at least 2.", file=sys.stderr)
            sys.exit(1)

        # Validate exponent for exponential method
        if args.method == "exponential" and args.exponent <= 0:
            print(
                "Error: Exponent must be positive for exponential interpolation.",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            colors = interpolate_colors(
                args.start_color, args.end_color, args.steps, args.method, args.exponent
            )
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Output colors in requested format
    if args.output == "list":
        for i, color in enumerate(colors):
            if args.format == "hex":
                print(color)
            elif args.format == "rgb":
                rgb = hex_to_rgb(color)
                print(f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
            elif args.format == "both":
                rgb = hex_to_rgb(color)
                print(f"{color} | rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")

    elif args.output == "json":
        import json

        data = {
            "start_color": args.start_color,
            "end_color": args.end_color,
            "method": args.method,
        }

        if args.spyder:
            data["spyder_mode"] = True
            data["total_colors"] = 16
        else:
            data["steps"] = args.steps

        if args.method == "exponential":
            data["exponent"] = args.exponent

        # Generate palette name
        if args.name:
            palette_name = args.name
        else:
            if args.simple_names:
                from themeweaver.color_utils.color_names import (
                    get_palette_name_from_color,
                )

                palette_name = get_palette_name_from_color(
                    args.start_color, creative=False
                )
            else:
                from themeweaver.color_utils.color_names import (
                    get_palette_name_from_color,
                )

                palette_name = get_palette_name_from_color(
                    args.start_color, creative=True
                )

        # Generate B-step structure
        palette_data = {}
        for i, color in enumerate(colors):
            if args.spyder:
                # Spyder uses B0, B10, B20, ..., B140, B150
                step = i * 10
            else:
                # Regular mode uses sequential B0, B10, B20, etc.
                step = i * 10

            palette_data[f"B{step}"] = color

        data["palette"] = {palette_name: palette_data}
        print(json.dumps(data, indent=2))

    elif args.output == "yaml":
        import yaml

        if args.name:
            palette_name = args.name
        else:
            if args.simple_names:
                from themeweaver.color_utils.color_names import (
                    get_palette_name_from_color,
                )

                palette_name = get_palette_name_from_color(
                    args.start_color, creative=False
                )
            else:
                from themeweaver.color_utils.color_names import (
                    get_palette_name_from_color,
                )

                palette_name = get_palette_name_from_color(
                    args.start_color, creative=True
                )

        # Create YAML structure compatible with ThemeWeaver colorsystem.yaml
        data = {palette_name: {}}

        # Generate B-step naming
        for i, color in enumerate(colors):
            if args.spyder:
                # Spyder uses B0, B10, B20, ..., B140, B150 (16 colors)
                step = i * 10
            else:
                # Regular mode uses sequential B0, B10, B20, etc.
                step = i * 10

            data[palette_name][f"B{step}"] = color

        # Add metadata as comments in the YAML
        if args.spyder:
            yaml_output = f"""# Generated Spyder-compatible palette using {args.method} interpolation
# Darkest color (B10): {args.start_color}
# Lightest color (B140): {args.end_color}
# B0 = black, B150 = white (Spyder requirement)"""
        else:
            yaml_output = f"""# Generated color gradient using {args.method} interpolation
# From: {args.start_color} to {args.end_color}
# Steps: {args.steps}"""

        if args.method == "exponential":
            yaml_output += f"\n# Exponent: {args.exponent}"

        yaml_output += (
            f"\n# Method: {args.method} ({_get_method_description(args.method)})\n\n"
        )

        yaml_output += yaml.dump(data, default_flow_style=False, sort_keys=False)
        print(yaml_output)

    # Show analysis if requested
    if args.analyze:
        analyze_interpolation(colors, args.method)


if __name__ == "__main__":
    main()
