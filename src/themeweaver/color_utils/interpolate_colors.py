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
)
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
from themeweaver.color_utils.interpolation_analysis import (
    analyze_interpolation,
    _get_method_description,
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
        - Duplicate colors are automatically detected and mitigated
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

    # Detect and mitigate duplicate colors
    colors = _mitigate_duplicate_colors(colors, method, start_hex, end_hex)

    return colors


def _mitigate_duplicate_colors(colors, method, start_hex, end_hex):
    """
    Detect and mitigate duplicate colors in interpolation results.

    Args:
        colors: List of hex colors from interpolation
        method: Interpolation method used
        start_hex: Starting color
        end_hex: Ending color

    Returns:
        List of colors with duplicates mitigated
    """
    if len(colors) < 3:
        return colors  # No duplicates possible with < 3 colors

    # Find duplicates (including consecutive and non-consecutive)
    duplicates = _find_duplicate_colors(colors)

    if not duplicates:
        return colors  # No duplicates found

    # Log warning about duplicates
    print(
        f"⚠️  Warning: Found {len(duplicates)} duplicate colors in {method} interpolation"
    )
    print(f"   Start: {start_hex}, End: {end_hex}, Steps: {len(colors)}")
    print(f"   Duplicate indices: {duplicates}")

    # If too many duplicates (>50% of colors), regenerate with different parameters
    if len(duplicates) > len(colors) * 0.5:
        print(
            "   Too many duplicates detected, regenerating with adjusted parameters..."
        )
        return _regenerate_gradient_without_duplicates(
            start_hex, end_hex, len(colors), method, 0
        )

    # Mitigation strategies based on method
    if method in ["linear", "lch", "hsv"]:
        # For these methods, duplicates are rare and usually due to rounding
        # Add small perturbations to break duplicates
        return _perturb_duplicates(colors, duplicates)

    elif method in ["exponential", "sine", "cosine"]:
        # These methods can have flat regions, try adjusting factors
        return _adjust_interpolation_factors(
            colors, duplicates, method, start_hex, end_hex
        )

    else:
        # For other methods, use perturbation as fallback
        return _perturb_duplicates(colors, duplicates)


def _regenerate_gradient_without_duplicates(
    start_hex, end_hex, steps, method, recursion_depth=0
):
    """
    Regenerate a gradient with different parameters to avoid duplicates.

    Args:
        start_hex: Starting color
        end_hex: Ending color
        steps: Number of steps
        method: Interpolation method
        recursion_depth: Current recursion depth to prevent infinite loops

    Returns:
        List of colors without duplicates
    """
    # Prevent infinite recursion
    if recursion_depth > 3:
        print("   ⚠️  Maximum recursion depth reached, using fallback strategy")
        return _force_unique_gradient(start_hex, end_hex, steps)

    # Check if colors are too similar to interpolate meaningfully
    if _colors_are_too_similar(start_hex, end_hex):
        print("   ⚠️  Colors are too similar, using fallback strategy")
        return _force_unique_gradient(start_hex, end_hex, steps)

    # Try different strategies based on the method
    if method == "exponential":
        # Try with a lower exponent
        for exponent in [1.5, 1.2, 1.0]:
            try:
                colors = interpolate_colors(start_hex, end_hex, steps, method, exponent)
                is_valid, _ = validate_gradient_uniqueness(colors, method)
                if is_valid:
                    print(f"   ✅ Regenerated successfully with exponent {exponent}")
                    return colors
            except (ValueError, TypeError, RuntimeError):
                continue

    elif method in ["sine", "cosine"]:
        # Try with more steps to break up flat regions
        try:
            colors = interpolate_colors(start_hex, end_hex, steps + 2, method)
            # Take every other color to maintain original step count
            result = colors[::2] if len(colors) >= steps else colors[:steps]
            is_valid, _ = validate_gradient_uniqueness(result, method)
            if is_valid:
                print(f"   ✅ Regenerated successfully with {steps + 2} steps")
                return result
        except (ValueError, TypeError, RuntimeError):
            pass

    # Fallback: use linear interpolation which is most reliable
    print("   🔄 Falling back to linear interpolation")
    try:
        colors = interpolate_colors(start_hex, end_hex, steps, "linear")
        is_valid, _ = validate_gradient_uniqueness(colors, "linear")
        if is_valid:
            return colors
    except (ValueError, TypeError, RuntimeError):
        pass

    # If linear also fails, use force strategy
    return _force_unique_gradient(start_hex, end_hex, steps)


def _colors_are_too_similar(color1, color2):
    """
    Check if two colors are too similar to interpolate meaningfully.

    Args:
        color1: First hex color
        color2: Second hex color

    Returns:
        True if colors are too similar
    """
    from themeweaver.color_utils import hex_to_rgb

    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    # Calculate Euclidean distance in RGB space
    distance = sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)) ** 0.5

    # If distance is less than 5, colors are too similar
    return distance < 5


def _force_unique_gradient(start_hex, end_hex, steps):
    """
    Force creation of a unique gradient by adding artificial variation.

    Args:
        start_hex: Starting color
        end_hex: Ending color
        steps: Number of steps

    Returns:
        List of unique colors
    """
    from themeweaver.color_utils import hex_to_rgb, rgb_to_hex

    if steps < 2:
        return [start_hex]

    rgb1 = hex_to_rgb(start_hex)
    rgb2 = hex_to_rgb(end_hex)

    colors = []
    for i in range(steps):
        factor = i / (steps - 1) if steps > 1 else 0

        # Linear interpolation with artificial variation
        r = rgb1[0] + (rgb2[0] - rgb1[0]) * factor
        g = rgb1[1] + (rgb2[1] - rgb1[1]) * factor
        b = rgb1[2] + (rgb2[2] - rgb1[2]) * factor

        # Add small artificial variation to ensure uniqueness
        variation = (i * 3) % 7  # Small cyclic variation
        r = max(0, min(255, r + variation))
        g = max(0, min(255, g + variation))
        b = max(0, min(255, b + variation))

        colors.append(rgb_to_hex((r, g, b)))

    return colors


def _find_duplicate_colors(colors):
    """
    Find all duplicate colors in a list, including non-consecutive ones.

    Args:
        colors: List of hex colors

    Returns:
        List of indices where duplicates occur (keeping the first occurrence)
    """
    seen = {}
    duplicates = []

    for i, color in enumerate(colors):
        if color in seen:
            duplicates.append(i)
        else:
            seen[color] = i

    return duplicates


def validate_gradient_uniqueness(colors, method="unknown"):
    """
    Validate that a gradient contains no duplicate colors.

    Args:
        colors: List of hex colors to validate
        method: Interpolation method used (for context)

    Returns:
        tuple: (is_valid, duplicate_info)
    """
    if len(colors) < 2:
        return True, None

    duplicates = _find_duplicate_colors(colors)

    if not duplicates:
        return True, None

    # Create detailed duplicate information
    duplicate_info = {
        "count": len(duplicates),
        "indices": duplicates,
        "method": method,
        "total_colors": len(colors),
        "unique_colors": len(colors) - len(duplicates),
    }

    return False, duplicate_info


def _perturb_duplicates(colors, duplicates):
    """
    Add small perturbations to duplicate colors to make them unique.

    Args:
        colors: List of hex colors
        duplicates: List of indices where duplicates occur

    Returns:
        List of colors with duplicates perturbed
    """
    from themeweaver.color_utils import hex_to_rgb, rgb_to_hex

    result = colors.copy()

    for dup_idx in duplicates:
        # Get the duplicate color
        dup_color = result[dup_idx]
        rgb = hex_to_rgb(dup_color)

        # Try different perturbation strategies
        perturbation_applied = False

        # Strategy 1: Small random perturbation
        import random

        for attempt in range(5):  # Try up to 5 different perturbations
            r_perturb = max(0, min(255, rgb[0] + random.randint(-3, 3)))
            g_perturb = max(0, min(255, rgb[1] + random.randint(-3, 3)))
            b_perturb = max(0, min(255, rgb[2] + random.randint(-3, 3)))

            if (r_perturb, g_perturb, b_perturb) != rgb:
                result[dup_idx] = rgb_to_hex((r_perturb, g_perturb, b_perturb))
                perturbation_applied = True
                break

        # Strategy 2: If random perturbation failed, use systematic approach
        if not perturbation_applied:
            # Add systematic perturbation based on index
            offset = (dup_idx * 7) % 15  # Use index to create variation
            r_perturb = max(0, min(255, rgb[0] + offset))
            g_perturb = max(0, min(255, rgb[1] + offset))
            b_perturb = max(0, min(255, rgb[2] + offset))

            if (r_perturb, g_perturb, b_perturb) != rgb:
                result[dup_idx] = rgb_to_hex((r_perturb, g_perturb, b_perturb))
                perturbation_applied = True

        # Strategy 3: If still no change, force a significant change
        if not perturbation_applied:
            # Force a more significant change
            r_perturb = max(0, min(255, rgb[0] + 5))
            g_perturb = max(0, min(255, rgb[1] + 5))
            b_perturb = max(0, min(255, rgb[2] + 5))
            result[dup_idx] = rgb_to_hex((r_perturb, g_perturb, b_perturb))

    return result


def _adjust_interpolation_factors(colors, duplicates, method, start_hex, end_hex):
    """
    Adjust interpolation factors to avoid duplicates in problematic methods.

    Args:
        colors: List of hex colors
        duplicates: List of indices where duplicates occur
        method: Interpolation method
        start_hex: Starting color
        end_hex: Ending color

    Returns:
        List of colors with adjusted interpolation
    """
    from themeweaver.color_utils import hex_to_rgb, rgb_to_hex
    from themeweaver.color_utils.interpolation_methods import (
        exponential_interpolate,
        sine_interpolate,
        cosine_interpolate,
    )

    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)
    steps = len(colors)

    # Recalculate with adjusted factors
    result = []
    for i in range(steps):
        factor = i / (steps - 1) if steps > 1 else 0

        # Add small offset to factor to break flat regions
        if i in duplicates:
            factor += 0.01  # Small offset to break duplicates

        # Apply the interpolation method
        if method == "exponential":
            interp_factor = exponential_interpolate(0, 1, factor, 2)
        elif method == "sine":
            interp_factor = sine_interpolate(0, 1, factor)
        elif method == "cosine":
            interp_factor = cosine_interpolate(0, 1, factor)
        else:
            interp_factor = factor

        # Interpolate RGB components
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * interp_factor
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * interp_factor
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * interp_factor

        result.append(rgb_to_hex((r, g, b)))

    return result


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
        """,
    )

    parser.add_argument("start_color", help="Starting hex color (with or without #)")

    parser.add_argument("end_color", help="Ending hex color (with or without #)")

    parser.add_argument(
        "steps",
        type=int,
        nargs="?",
        default=None,
        help="Number of interpolation steps (must be >= 2).",
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
        "--validate",
        action="store_true",
        help="Validate gradient for duplicate colors and show detailed analysis",
    )

    parser.add_argument(
        "--simple-names",
        action="store_true",
        help="Use simple color names instead of creative adjective+color combinations",
    )

    args = parser.parse_args()

    # Validate steps
    if args.steps is None:
        print(
            "Error: Number of steps is required for interpolation.",
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
            "steps": args.steps,
        }

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
            step = i * 10
            data[palette_name][f"B{step}"] = color

        # Add metadata as comments in the YAML
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

    # Show validation if requested
    if args.validate:
        is_valid, duplicate_info = validate_gradient_uniqueness(colors, args.method)

        print(f"\n=== Gradient Validation ({args.method.upper()}) ===")

        if is_valid:
            print("✅ No duplicate colors found - gradient is valid")
            print(f"   Total colors: {len(colors)}")
            print(f"   Unique colors: {len(colors)}")
        else:
            print("❌ Duplicate colors detected!")
            print(f"   Total colors: {duplicate_info['total_colors']}")
            print(f"   Unique colors: {duplicate_info['unique_colors']}")
            print(f"   Duplicate count: {duplicate_info['count']}")
            print(f"   Duplicate indices: {duplicate_info['indices']}")

            # Show which colors are duplicated
            seen_colors = {}
            for i, color in enumerate(colors):
                if color in seen_colors:
                    print(
                        f"   Color {color} appears at indices {seen_colors[color]} and {i}"
                    )
                else:
                    seen_colors[color] = i


if __name__ == "__main__":
    main()
