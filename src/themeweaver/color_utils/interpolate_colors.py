"""
Color interpolation CLI tool.

This script interpolates between two hex colors with a specified number of steps
using various interpolation methods, including LCH color space and perceptual
uniformity features.
"""

import argparse
import sys
import math

from .color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsv,
    hsv_to_rgb,
    lch_to_hex,
    rgb_to_lch,
    calculate_delta_e,
    get_color_info,
    linear_interpolate,
    HAS_LCH,
)


def circular_interpolate(start_angle, end_angle, factor):
    """
    Interpolate between two angles (in degrees) taking the shortest circular path.

    Args:
        start_angle: Starting angle in degrees
        end_angle: Ending angle in degrees
        factor: Interpolation factor (0-1)

    Returns:
        Interpolated angle in degrees
    """
    # Normalize angles to 0-360
    start_angle = start_angle % 360
    end_angle = end_angle % 360

    # Calculate the difference
    diff = end_angle - start_angle

    # Take the shortest path around the circle
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360

    # Interpolate and normalize result
    result = (start_angle + diff * factor) % 360
    return result


def cubic_interpolate(start, end, factor):
    """Cubic (smooth) interpolation between two values."""
    # Using smoothstep function: 3t² - 2t³
    smooth_factor = factor * factor * (3 - 2 * factor)
    return start + (end - start) * smooth_factor


def exponential_interpolate(start, end, factor, exponent=2):
    """Exponential interpolation between two values."""
    exp_factor = factor**exponent
    return start + (end - start) * exp_factor


def sine_interpolate(start, end, factor):
    """Sine-based interpolation between two values."""
    sine_factor = (1 - math.cos(factor * math.pi)) / 2
    return start + (end - start) * sine_factor


def interpolate_colors(start_hex, end_hex, steps, method="linear", exponent=2):
    """Interpolate between two hex colors with given number of steps and method."""
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
        if not HAS_LCH:
            raise ImportError("LCH interpolation requires colorspacious library")

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
            if method == "linear":
                interp_factor = factor
            elif method == "cubic":
                interp_factor = cubic_interpolate(0, 1, factor)
            elif method == "exponential":
                interp_factor = exponential_interpolate(0, 1, factor, exponent)
            elif method == "sine":
                interp_factor = sine_interpolate(0, 1, factor)
            else:
                interp_factor = factor  # fallback to linear

            # Interpolate each RGB component
            r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * interp_factor
            g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * interp_factor
            b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * interp_factor

            colors.append(rgb_to_hex((r, g, b)))

    return colors


def analyze_interpolation(colors):
    """Analyze the color interpolation for perceptual quality."""
    if len(colors) < 2:
        return

    print("\n=== Interpolation Analysis ===")

    for i, color in enumerate(colors):
        info = get_color_info(color)
        hsv_deg = info["hsv_degrees"]

        analysis_str = f"Step {i + 1:2d}: {color} | HSV({hsv_deg[0]:6.1f}°, {hsv_deg[1]:.2f}, {hsv_deg[2]:.2f})"

        if HAS_LCH and info.get("lch"):
            lch = info["lch"]
            analysis_str += f" | LCH({lch[0]:.1f}, {lch[1]:.1f}, {lch[2]:.1f}°)"

        print(analysis_str)

    # Delta E analysis if available
    if HAS_LCH and len(colors) > 1:
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

            # Quality assessment
            if std_dev < 3:
                print("  ✅ Very uniform perceptual spacing")
            elif std_dev < 5:
                print("  ✅ Good perceptual spacing")
            else:
                print("  ⚠️  Uneven perceptual spacing")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Interpolate between two hex colors with various interpolation methods.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s '#93A1A1' '#EEE8D5' 8
  %(prog)s '#FF0000' '#0000FF' 10 --method hsv
  %(prog)s '#93A1A1' '#EEE8D5' 5 --method cubic
  %(prog)s '#FF0000' '#00FF00' 8 --method exponential --exponent 3
  %(prog)s '#FF0000' '#0000FF' 8 --method lch --analyze
        """,
    )

    parser.add_argument("start_color", help="Starting hex color (with or without #)")

    parser.add_argument("end_color", help="Ending hex color (with or without #)")

    parser.add_argument(
        "steps", type=int, help="Number of interpolation steps (must be >= 2)"
    )

    parser.add_argument(
        "-m",
        "--method",
        choices=["linear", "cubic", "exponential", "sine", "hsv", "lch"],
        default="linear",
        help="Interpolation method (default: linear)",
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
        choices=["list", "class", "json"],
        default="list",
        help="Output style (default: list)",
    )

    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Show detailed color analysis including perceptual metrics",
    )

    args = parser.parse_args()

    # Validate steps
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

    # Validate LCH requirements
    if args.method == "lch" and not HAS_LCH:
        print(
            "Error: LCH interpolation requires colorspacious library.", file=sys.stderr
        )
        sys.exit(1)

    try:
        colors = interpolate_colors(
            args.start_color, args.end_color, args.steps, args.method, args.exponent
        )

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

        elif args.output == "class":
            method_name = args.method.title()
            print(f"# Generated color interpolation ({method_name} method)")
            for i, color in enumerate(colors):
                step = i * (140 - 10) // (args.steps - 1) + 10 if args.steps > 1 else 10
                print(f"    B{step} = '{color}'")

        elif args.output == "json":
            import json

            data = {
                "start_color": args.start_color,
                "end_color": args.end_color,
                "steps": args.steps,
                "method": args.method,
            }

            if args.method == "exponential":
                data["exponent"] = args.exponent

            if args.format == "hex":
                data["colors"] = colors
            elif args.format == "rgb":
                data["colors"] = [list(hex_to_rgb(color)) for color in colors]
            else:  # both
                data["colors"] = [
                    {"hex": color, "rgb": list(hex_to_rgb(color))} for color in colors
                ]

            print(json.dumps(data, indent=2))

        # Show analysis if requested
        if args.analyze:
            analyze_interpolation(colors)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
