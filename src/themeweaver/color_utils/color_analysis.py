"""
Color analysis utilities for themeweaver.

This module provides functions for analyzing color palettes,
specifically chromatic distance analysis for perceptual quality assessment.
"""

from themeweaver.color_utils.color_utils import calculate_delta_e, calculate_std_dev


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
