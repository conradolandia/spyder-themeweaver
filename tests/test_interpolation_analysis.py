#!/usr/bin/env python3
"""
Tests for interpolation analysis in themeweaver.

Tests the interpolation analysis functionality including:
- Perceptual analysis of color gradients
- Analysis output formatting
- Method-specific analysis

Run with: `python -m pytest tests/test_interpolation_analysis.py -v`
"""

import sys
from io import StringIO
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from themeweaver.color_utils.interpolation_analysis import (
    analyze_interpolation,
)


class TestInterpolationAnalysis:
    """Test interpolation analysis functionality."""

    def test_analyze_interpolation_basic(self) -> None:
        """Test basic interpolation analysis."""
        colors = ["#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00"]

        # Capture stdout to test the output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_interpolation(colors, "linear")
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Check that analysis output was generated
        assert "Interpolation Analysis (LINEAR)" in output
        assert "Perceptual Distance Analysis" in output
        assert "Perceptual Statistics" in output
        assert "Average ΔE" in output

    def test_analyze_interpolation_single_color(self) -> None:
        """Test interpolation analysis with single color."""
        colors = ["#FF0000"]

        # Capture stdout to test the output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_interpolation(colors, "linear")
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Should return early for single color
        assert output == ""

    def test_analyze_interpolation_two_colors(self) -> None:
        """Test interpolation analysis with two colors."""
        colors = ["#FF0000", "#0000FF"]

        # Capture stdout to test the output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_interpolation(colors, "cubic")
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Check that analysis output was generated
        assert "Interpolation Analysis (CUBIC)" in output
        assert "Perceptual Distance Analysis" in output
        assert "Step 1 → 2: ΔE =" in output

    def test_analyze_interpolation_lch_method(self) -> None:
        """Test interpolation analysis with LCH method."""
        colors = ["#FF0000", "#00FF00", "#0000FF"]

        # Capture stdout to test the output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_interpolation(colors, "lch")
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Check that LCH-specific analysis was generated
        assert "Interpolation Analysis (LCH)" in output
        assert "LCH interpolation optimizes for perceptual uniformity" in output
        assert "Perceptual Distance Analysis" in output

    def test_analyze_interpolation_hsv_method(self) -> None:
        """Test interpolation analysis with HSV method."""
        colors = ["#FF0000", "#00FF00", "#0000FF"]

        # Capture stdout to test the output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_interpolation(colors, "hsv")
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Check that HSV-specific analysis was generated
        assert "Interpolation Analysis (HSV)" in output
        assert "HSV interpolation avoids 'muddy colors'" in output
        assert "Perceptual Distance Analysis" in output

    def test_analyze_interpolation_rgb_methods(self) -> None:
        """Test interpolation analysis with RGB-based methods."""
        colors = ["#FF0000", "#00FF00", "#0000FF"]

        for method in [
            "linear",
            "cubic",
            "exponential",
            "sine",
            "cosine",
            "hermite",
            "quintic",
        ]:
            # Capture stdout to test the output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                analyze_interpolation(colors, method)
                output = captured_output.getvalue()
            finally:
                sys.stdout = sys.__stdout__

            # Check that RGB-specific analysis was generated
            assert f"Interpolation Analysis ({method.upper()})" in output
            assert (
                "RGB-based interpolation may show perceptual non-uniformity" in output
            )
            assert "Perceptual Distance Analysis" in output

    def test_analyze_interpolation_unknown_method(self) -> None:
        """Test interpolation analysis with unknown method."""
        colors = ["#FF0000", "#00FF00", "#0000FF"]

        # Capture stdout to test the output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_interpolation(colors, "unknown")
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Check that analysis was generated without method-specific notes
        assert "Interpolation Analysis (UNKNOWN)" in output
        assert "Perceptual Distance Analysis" in output
        # Should not have method-specific notes
        assert "LCH interpolation optimizes" not in output
        assert "HSV interpolation avoids" not in output
        assert "RGB-based interpolation may show" not in output

    def test_analyze_interpolation_empty_list(self) -> None:
        """Test interpolation analysis with empty list."""
        colors = []

        # Capture stdout to test the output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_interpolation(colors, "linear")
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Should return early for empty list
        assert output == ""

    def test_analyze_interpolation_color_info_formatting(self) -> None:
        """Test that color information is properly formatted in output."""
        colors = ["#FF0000", "#00FF00"]

        # Capture stdout to test the output
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            analyze_interpolation(colors, "linear")
            output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Check that color information is formatted correctly
        assert "Step  1:" in output
        assert "Step  2:" in output
        assert "#FF0000" in output
        assert "#00FF00" in output
        assert "HSV(" in output


if __name__ == "__main__":
    # Run tests with pytest
    exit_code = pytest.main([__file__, "-v"])
    sys.exit(exit_code)
