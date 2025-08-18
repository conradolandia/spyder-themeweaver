"""
Color analysis utilities for themeweaver.

This module provides functions for analyzing color palettes,
including chromatic distance analysis, color statistics,
and data loading utilities.
"""

import importlib.util
import inspect
from pathlib import Path

from themeweaver.color_utils.color_utils import calculate_delta_e, get_color_info


def load_color_groups_from_file(file_path):
    """
    Load color group classes from a Python file.

    Args:
        file_path: Path to the Python file containing color group classes

    Returns:
        Dictionary of {class_name: {attribute_name: color_value}}
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("colorsystem", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    color_groups = {}

    # Find all classes in the module
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Check if this looks like a color group class
        color_attrs = {}
        for attr_name in dir(obj):
            if not attr_name.startswith("_"):  # Skip private attributes
                attr_value = getattr(obj, attr_name)
                if isinstance(attr_value, str) and attr_value.startswith("#"):
                    color_attrs[attr_name] = attr_value

        if color_attrs:  # Only include classes that have color attributes
            color_groups[name] = color_attrs

    return color_groups


def extract_colors_from_group(color_group_dict):
    """
    Extract color values from a color group dictionary, sorted by attribute name.

    Args:
        color_group_dict: Dictionary of {attribute_name: color_value}

    Returns:
        List of hex color strings
    """
    # Sort by attribute name (B10, B20, etc.)
    sorted_items = sorted(color_group_dict.items(), key=lambda x: x[0])
    return [color for _, color in sorted_items]


def analyze_existing_colors(colors, group_name=""):
    """Analyze a list of hex colors to understand their HSV and LCH characteristics."""
    analysis = []
    for i, color in enumerate(colors):
        info = get_color_info(color)
        item = {
            "index": i,
            "hex": color,
            "hue": info["hsv"][0],
            "saturation": info["hsv"][1],
            "brightness": info["hsv"][2],
            "hue_degrees": info["hsv_degrees"][0],
        }

        # Add LCH analysis if available
        if info.get("lch") is not None:
            item.update(
                {
                    "lch_lightness": info["lch_lightness"],
                    "lch_chroma": info["lch_chroma"],
                    "lch_hue": info["lch_hue"],
                }
            )
        else:
            item.update(
                {
                    "lch_lightness": None,
                    "lch_chroma": None,
                    "lch_hue": None,
                }
            )

        analysis.append(item)

    if group_name:
        print(f"=== Analysis of {group_name} Colors ===")

    for item in analysis:
        step = (item["index"] + 1) * 10
        hsv_info = (
            f"B{step:3d}: {item['hex']} | "
            f"HSV H: {item['hue_degrees']:6.1f}° | "
            f"S: {item['saturation']:.2f} | "
            f"V: {item['brightness']:.2f}"
        )

        if item["lch_lightness"] is not None:
            lch_info = (
                f" | LCH L: {item['lch_lightness']:.1f} | "
                f"C: {item['lch_chroma']:.1f} | "
                f"H: {item['lch_hue']:.1f}°"
            )
            print(hsv_info + lch_info)
        else:
            print(hsv_info)

    avg_sat = sum(item["saturation"] for item in analysis) / len(analysis)
    avg_bright = sum(item["brightness"] for item in analysis) / len(analysis)

    print(f"\nHSV Averages - Saturation: {avg_sat:.2f}, Brightness: {avg_bright:.2f}")

    valid_lch = [item for item in analysis if item.get("lch_lightness") is not None]
    if valid_lch:
        avg_lightness = sum(item["lch_lightness"] for item in valid_lch) / len(
            valid_lch
        )
        avg_chroma = sum(item["lch_chroma"] for item in valid_lch) / len(valid_lch)
        print(
            f"LCH Averages - Lightness: {avg_lightness:.1f}, Chroma: {avg_chroma:.1f}"
        )

    # Show hue progression for both models
    hues_hsv = [item["hue_degrees"] for item in analysis]
    print(f"HSV Hue progression: {[round(h, 1) for h in hues_hsv]}")

    hues_lch = [item["lch_hue"] for item in analysis if item.get("lch_hue") is not None]
    if hues_lch:
        print(f"LCH Hue progression: {[round(h, 1) for h in hues_lch]}")

    print()

    return analysis


def analyze_chromatic_distances(colors, group_name=""):
    """Analyze chromatic distances between consecutive colors in a palette."""

    if len(colors) < 2:
        return None

    distances = []
    for i in range(len(colors) - 1):
        delta_e = calculate_delta_e(colors[i], colors[i + 1])
        if delta_e is not None:
            distances.append(
                {
                    "from_color": colors[i],
                    "to_color": colors[i + 1],
                    "delta_e": delta_e,
                    "step": f"B{(i + 1) * 10} -> B{(i + 2) * 10}",
                }
            )

    if group_name:
        print(f"\n=== Chromatic Distance Analysis: {group_name} ===")

    total_delta_e = 0
    for dist in distances:
        print(
            f"{dist['step']}: ΔE = {dist['delta_e']:.1f} ({dist['from_color']} -> {dist['to_color']})"
        )
        total_delta_e += dist["delta_e"]

    avg_delta_e = total_delta_e / len(distances) if distances else 0
    min_delta_e = min(d["delta_e"] for d in distances) if distances else 0
    max_delta_e = max(d["delta_e"] for d in distances) if distances else 0

    print("\nDistance Statistics:")
    print(f"  Average ΔE: {avg_delta_e:.1f}")
    print(f"  Min ΔE: {min_delta_e:.1f}")
    print(f"  Max ΔE: {max_delta_e:.1f}")
    print(
        f"  Consistency (std dev): {calculate_std_dev([d['delta_e'] for d in distances]):.1f}"
    )

    # Perceptual quality assessment
    print("\nPerceptual Quality Assessment:")
    if avg_delta_e < 10:
        print("  ⚠️  Colors may be too similar - low contrast")
    elif avg_delta_e > 50:
        print("  ⚠️  Colors may be too different - jarring transitions")
    else:
        print("  ✅ Good perceptual spacing")

    if max_delta_e - min_delta_e > 20:
        print("  ⚠️  Inconsistent spacing - some jumps too large")
    else:
        print("  ✅ Consistent spacing")

    return distances


def calculate_std_dev(values):
    """Calculate standard deviation of a list of values."""
    if not values:
        return 0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance**0.5


def print_color_analysis(color_groups, group_names=None):
    """Analyze color groups from loaded data."""
    if group_names is None:
        group_names = list(color_groups.keys())

    for group_name in group_names:
        if group_name in color_groups:
            colors = extract_colors_from_group(color_groups[group_name])
            analyze_existing_colors(colors, group_name)

            # Add chromatic distance analysis
            analyze_chromatic_distances(colors, group_name)
        else:
            print(f"Warning: Group '{group_name}' not found in loaded color groups.")


def analyze_palette_lch(palette_data):
    """Analyze a color palette in LCH space."""
    from themeweaver.color_utils import hex_to_rgb, rgb_to_lch

    name = palette_data["name"]
    colors = palette_data["colors"]

    print(f"=== {name.upper()} ANALYSIS ===\n")

    palette_lch = []
    print(f"{'Color':<12} {'Hex':<8} {'L':<6} {'C':<6} {'H':<6}")
    print("-" * 50)

    for color_name, hex_color in colors.items():
        if not hex_color.startswith("#"):
            hex_color = "#" + hex_color
        try:
            rgb = hex_to_rgb(hex_color)
            lightness, chroma, hue = rgb_to_lch(rgb)
            palette_lch.append((color_name, hex_color, lightness, chroma, hue))
            print(
                f"{color_name:<12} {hex_color:<8} {lightness:.1f}  {chroma:.1f}  {hue:.1f}"
            )
        except ValueError as e:
            print(f"{color_name:<12} {hex_color:<8} ERROR: Invalid color format - {e}")
        except (TypeError, IndexError) as e:
            print(
                f"{color_name:<12} {hex_color:<8} ERROR: Color conversion failed - {e}"
            )
        except Exception as e:
            print(
                f"{color_name:<12} {hex_color:<8} ERROR: Unexpected error - {type(e).__name__}: {e}"
            )

    if not palette_lch:
        print("No valid colors found in palette!")
        return None

    # Analyze overall characteristics
    lightness_values = [lightness for _, _, lightness, _, _ in palette_lch]
    chroma_values = [chroma for _, _, _, chroma, _ in palette_lch]
    hue_values = [hue for _, _, _, _, hue in palette_lch]

    print(f"\n--- {name.upper()} CHARACTERISTICS ---")
    print(f"Colors: {len(palette_lch)}")
    print(
        f"Lightness: min={min(lightness_values):.1f}, max={max(lightness_values):.1f}, avg={sum(lightness_values) / len(lightness_values):.1f}"
    )
    print(
        f"Chroma: min={min(chroma_values):.1f}, max={max(chroma_values):.1f}, avg={sum(chroma_values) / len(chroma_values):.1f}"
    )
    print(f"Hue range: {min(hue_values):.1f}° to {max(hue_values):.1f}°")

    # Sort by hue to see progression
    palette_lch.sort(key=lambda x: x[4])  # Sort by hue
    print("\n--- HUE PROGRESSION (sorted) ---")
    print(f"{'Color':<12} {'Hue':<6} {'L':<6} {'C':<6}")
    print("-" * 38)

    for color_name, hex_color, lightness, chroma, hue in palette_lch:
        print(f"{color_name:<12} {hue:.1f}°  {lightness:.1f}  {chroma:.1f}")

    return palette_lch


def find_optimal_parameters(target_palette_data, max_colors=None):
    """Find what parameters would generate colors closest to the target palette."""
    from themeweaver.color_utils import calculate_delta_e
    from themeweaver.color_utils.color_generation import generate_theme_colors

    print("\n=== FINDING OPTIMAL PARAMETERS ===\n")

    target_lch = analyze_palette_lch(target_palette_data)
    if not target_lch:
        return None, None

    # Extract average characteristics
    avg_lightness = sum(lightness for _, _, lightness, _, _ in target_lch) / len(
        target_lch
    )
    avg_chroma = sum(chroma for _, _, _, chroma, _ in target_lch) / len(target_lch)

    # Find the starting hue (first color in hue progression)
    target_hues = sorted([hue for _, _, _, _, hue in target_lch])
    start_hue = target_hues[0]

    print("TARGET PALETTE AVERAGES:")
    print(f"  Lightness: {avg_lightness:.1f}")
    print(f"  Chroma: {avg_chroma:.1f}")
    print(f"  Start hue: {start_hue:.1f}°")

    # Test different parameters
    test_cases = [
        {"target_delta_e": 15, "start_hue": int(start_hue)},
        {"target_delta_e": 20, "start_hue": int(start_hue)},
        {"target_delta_e": 25, "start_hue": int(start_hue)},
        {"target_delta_e": 30, "start_hue": int(start_hue)},
        {"target_delta_e": 35, "start_hue": int(start_hue)},
    ]

    print("\n--- TESTING PARAMETERS ---")

    best_match = None
    best_distance = float("inf")
    num_colors = max_colors or len(target_lch)

    for params in test_cases:
        try:
            # Generate with these parameters
            generated_colors = generate_theme_colors(
                theme="dark",  # Use dark as reference
                num_colors=num_colors,
                **params,
            )

            # Calculate total distance to target colors
            total_distance = 0
            target_hex_colors = [hex_color for _, hex_color, _, _, _ in target_lch]
            comparison_count = 0

            for i, gen_color in enumerate(generated_colors):
                if i < len(target_hex_colors):
                    distance = calculate_delta_e(gen_color, target_hex_colors[i])
                    # Fix: Check specifically for None, not just truthiness
                    if distance is not None:
                        total_distance += distance
                        comparison_count += 1

            # Fix: Prevent division by zero
            if comparison_count > 0:
                avg_distance = total_distance / comparison_count
                print(
                    f"ΔE={params['target_delta_e']}, start_hue={params['start_hue']}° → avg distance: {avg_distance:.1f}"
                )

                if avg_distance < best_distance:
                    best_distance = avg_distance
                    best_match = params
            else:
                print(
                    f"ΔE={params['target_delta_e']}, start_hue={params['start_hue']}° → no valid comparisons"
                )
        except Exception as e:
            print(
                f"ΔE={params['target_delta_e']}, start_hue={params['start_hue']}° → error: {e}"
            )

    return best_match, best_distance


def compare_with_generated(target_palette_data, theme="dark"):
    """Compare target palette with generated colors using current defaults."""
    from themeweaver.color_utils import hex_to_rgb, rgb_to_lch
    from themeweaver.color_utils.color_generation import generate_theme_colors

    print("\n=== COMPARISON WITH GENERATED COLORS ===\n")

    target_lch = analyze_palette_lch(target_palette_data)
    if not target_lch:
        return

    try:
        # Generate with current defaults
        generated_colors = generate_theme_colors(
            theme=theme, num_colors=len(target_lch)
        )

        # Fix: Check for empty generated_colors
        if not generated_colors:
            print(f"ERROR: No colors generated for theme '{theme}'")
            return

        print(f"GENERATED {theme.upper()} COLORS:")
        for i, color in enumerate(generated_colors):
            rgb = hex_to_rgb(color)
            lightness, chroma, hue = rgb_to_lch(rgb)
            print(
                f"  B{(i + 1) * 10}: {color} → L={lightness:.1f}, C={chroma:.1f}, H={hue:.1f}°"
            )

        # Calculate average characteristics
        generated_lch = [rgb_to_lch(hex_to_rgb(c)) for c in generated_colors]
        generated_avg_l = sum(lch[0] for lch in generated_lch) / len(generated_lch)
        generated_avg_c = sum(lch[1] for lch in generated_lch) / len(generated_lch)

        target_avg_l = sum(lightness for _, _, lightness, _, _ in target_lch) / len(
            target_lch
        )
        target_avg_c = sum(chroma for _, _, _, chroma, _ in target_lch) / len(
            target_lch
        )

        print("\nCOMPARISON:")
        print(
            f"  Target Lightness: {target_avg_l:.1f} | Generated: {generated_avg_l:.1f} | Diff: {generated_avg_l - target_avg_l:+.1f}"
        )
        print(
            f"  Target Chroma: {target_avg_c:.1f} | Generated: {generated_avg_c:.1f} | Diff: {generated_avg_c - target_avg_c:+.1f}"
        )
    except Exception as e:
        print(f"ERROR: Failed to compare with generated colors: {e}")


def generate_inspired_palette(target_palette_data, theme="dark"):
    """Generate a palette inspired by the target palette."""
    from themeweaver.color_utils.color_generation import generate_theme_colors

    target_name = target_palette_data["name"]
    print(f"\n=== {target_name.upper()}-INSPIRED PALETTE ===\n")

    target_lch = analyze_palette_lch(target_palette_data)
    if not target_lch:
        return None

    try:
        # Use target-like parameters
        target_hues = sorted([hue for _, _, _, _, hue in target_lch])
        start_hue = int(target_hues[0])

        # Generate inspired palette
        inspired_colors = generate_theme_colors(
            theme=theme,
            num_colors=len(target_lch),
            target_delta_e=25,  # Good default
            start_hue=start_hue,
        )

        print(f"{target_name.upper()}-INSPIRED {theme.upper()}:")
        for i, color in enumerate(inspired_colors):
            print(f"  B{(i + 1) * 10} = '{color}'")

        return inspired_colors
    except Exception as e:
        print(f"ERROR: Failed to generate inspired palette: {e}")
        return None
