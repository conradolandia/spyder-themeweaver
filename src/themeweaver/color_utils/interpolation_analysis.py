"""
Interpolation analysis utilities for ThemeWeaver.

This module provides functions for analyzing color interpolation results,
including perceptual metrics and quality assessment.
"""

from typing import List

from themeweaver.color_utils import calculate_delta_e, get_color_info


def analyze_interpolation(colors: List[str], method: str = "unknown") -> None:
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
