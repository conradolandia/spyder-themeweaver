#!/usr/bin/env python3
"""
Tests for interpolation methods in themeweaver.

Tests the various interpolation algorithms including:
- Linear interpolation
- Circular interpolation
- Cubic interpolation
- Exponential interpolation
- Sine/Cosine interpolation
- Hermite interpolation
- Quintic interpolation
- Color interpolation with different methods

Run with: `python -m pytest tests/test_interpolation_methods.py -v`
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from themeweaver.color_utils.interpolation_methods import (
    circular_interpolate,
    cosine_interpolate,
    cubic_interpolate,
    exponential_interpolate,
    hermite_interpolate,
    interpolate_colors,
    linear_interpolate,
    quintic_interpolate,
    sine_interpolate,
)


class TestBasicInterpolationMethods:
    """Test basic interpolation methods."""

    def test_linear_interpolate(self) -> None:
        """Test linear interpolation."""
        # Test basic linear interpolation
        result = linear_interpolate(0, 100, 0.5)
        assert result == 50.0

        # Test edge cases
        assert linear_interpolate(0, 100, 0) == 0.0
        assert linear_interpolate(0, 100, 1) == 100.0

        # Test negative values
        result = linear_interpolate(-10, 10, 0.5)
        assert result == 0.0

        # Test floating point
        result = linear_interpolate(1.5, 3.5, 0.25)
        assert result == 2.0

    def test_circular_interpolate(self) -> None:
        """Test circular interpolation between angles."""
        # Test normal case
        result = circular_interpolate(0, 180, 0.5)
        assert result == 90.0

        # Test crossing 0/360 boundary
        result = circular_interpolate(350, 10, 0.5)
        assert result == 0.0

        # Test the other way around
        result = circular_interpolate(10, 350, 0.5)
        assert result == 0.0

        # Test edge cases
        assert (
            circular_interpolate(0, 360, 0.5) == 0.0
        )  # 360 becomes 0 after normalization

        # Test negative angles - the function normalizes angles, so -90 becomes 270
        result = circular_interpolate(-90, 90, 0.5)
        # The shortest path from 270 to 90 degrees is 180 degrees
        assert result == 180.0

    def test_cubic_interpolate(self) -> None:
        """Test cubic interpolation."""
        # Test basic cubic interpolation
        result = cubic_interpolate(0, 100, 0.5)
        assert result == 50.0  # At 0.5, smoothstep should be 0.5

        # Test edge cases
        assert cubic_interpolate(0, 100, 0) == 0.0
        assert cubic_interpolate(0, 100, 1) == 100.0

        # Test that it's different from linear at other points
        linear_result = linear_interpolate(0, 100, 0.25)
        cubic_result = cubic_interpolate(0, 100, 0.25)
        assert cubic_result != linear_result

    def test_exponential_interpolate(self) -> None:
        """Test exponential interpolation."""
        # Test basic exponential interpolation
        result = exponential_interpolate(0, 100, 0.5, 2)
        assert result == 25.0  # 0.5^2 = 0.25

        # Test with different exponents
        result = exponential_interpolate(0, 100, 0.5, 3)
        assert result == 12.5  # 0.5^3 = 0.125

        # Test edge cases
        assert exponential_interpolate(0, 100, 0, 2) == 0.0
        assert exponential_interpolate(0, 100, 1, 2) == 100.0

        # Test with exponent 1 (should be linear)
        result = exponential_interpolate(0, 100, 0.5, 1)
        assert result == 50.0

    def test_sine_interpolate(self) -> None:
        """Test sine interpolation."""
        # Test basic sine interpolation
        result = sine_interpolate(0, 100, 0.5)
        assert abs(result - 50.0) < 0.01  # Allow small floating point errors

        # Test edge cases
        assert sine_interpolate(0, 100, 0) == 0.0
        assert sine_interpolate(0, 100, 1) == 100.0

        # Test that it's different from linear
        linear_result = linear_interpolate(0, 100, 0.25)
        sine_result = sine_interpolate(0, 100, 0.25)
        assert sine_result != linear_result

    def test_cosine_interpolate(self) -> None:
        """Test cosine interpolation."""
        # Test basic cosine interpolation
        result = cosine_interpolate(0, 100, 0.5)
        assert abs(result - 50.0) < 0.01  # Allow small floating point errors

        # Test edge cases
        assert cosine_interpolate(0, 100, 0) == 0.0
        assert cosine_interpolate(0, 100, 1) == 100.0

        # Test that it's different from linear
        linear_result = linear_interpolate(0, 100, 0.25)
        cosine_result = cosine_interpolate(0, 100, 0.25)
        assert cosine_result != linear_result

    def test_hermite_interpolate(self) -> None:
        """Test Hermite interpolation."""
        # Test basic Hermite interpolation
        result = hermite_interpolate(0, 100, 0.5)
        assert result == 50.0  # At 0.5, Hermite should be 0.5

        # Test edge cases
        assert hermite_interpolate(0, 100, 0) == 0.0
        assert hermite_interpolate(0, 100, 1) == 100.0

        # Test that it's different from linear
        linear_result = linear_interpolate(0, 100, 0.25)
        hermite_result = hermite_interpolate(0, 100, 0.25)
        assert hermite_result != linear_result

    def test_quintic_interpolate(self) -> None:
        """Test quintic interpolation."""
        # Test basic quintic interpolation
        result = quintic_interpolate(0, 100, 0.5)
        assert result == 50.0  # At 0.5, quintic should be 0.5

        # Test edge cases
        assert quintic_interpolate(0, 100, 0) == 0.0
        assert quintic_interpolate(0, 100, 1) == 100.0

        # Test that it's different from linear
        linear_result = linear_interpolate(0, 100, 0.25)
        quintic_result = quintic_interpolate(0, 100, 0.25)
        assert quintic_result != linear_result


class TestColorInterpolation:
    """Test color interpolation functionality."""

    def test_interpolate_colors_linear(self) -> None:
        """Test color interpolation with linear method."""
        colors = interpolate_colors("#FF0000", "#0000FF", 3, method="linear")

        assert len(colors) == 3
        assert colors[0] == "#FF0000"  # Start color
        assert colors[2] == "#0000FF"  # End color
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_cubic(self) -> None:
        """Test color interpolation with cubic method."""
        colors = interpolate_colors("#FF0000", "#0000FF", 5, method="cubic")

        assert len(colors) == 5
        assert colors[0] == "#FF0000"
        assert colors[4] == "#0000FF"
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_exponential(self) -> None:
        """Test color interpolation with exponential method."""
        colors = interpolate_colors(
            "#FF0000", "#0000FF", 4, method="exponential", exponent=3
        )

        assert len(colors) == 4
        assert colors[0] == "#FF0000"
        assert colors[3] == "#0000FF"
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_sine(self) -> None:
        """Test color interpolation with sine method."""
        colors = interpolate_colors("#FF0000", "#0000FF", 3, method="sine")

        assert len(colors) == 3
        assert colors[0] == "#FF0000"
        assert colors[2] == "#0000FF"
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_cosine(self) -> None:
        """Test color interpolation with cosine method."""
        colors = interpolate_colors("#FF0000", "#0000FF", 3, method="cosine")

        assert len(colors) == 3
        assert colors[0] == "#FF0000"
        assert colors[2] == "#0000FF"
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_hermite(self) -> None:
        """Test color interpolation with Hermite method."""
        colors = interpolate_colors("#FF0000", "#0000FF", 3, method="hermite")

        assert len(colors) == 3
        assert colors[0] == "#FF0000"
        assert colors[2] == "#0000FF"
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_quintic(self) -> None:
        """Test color interpolation with quintic method."""
        colors = interpolate_colors("#FF0000", "#0000FF", 3, method="quintic")

        assert len(colors) == 3
        assert colors[0] == "#FF0000"
        assert colors[2] == "#0000FF"
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_hsv(self) -> None:
        """Test color interpolation with HSV method."""
        colors = interpolate_colors("#FF0000", "#0000FF", 3, method="hsv")

        assert len(colors) == 3
        assert colors[0] == "#FF0000"
        assert colors[2] == "#0000FF"
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_lch(self) -> None:
        """Test color interpolation with LCH method."""
        colors = interpolate_colors("#FF0000", "#0000FF", 3, method="lch")

        assert len(colors) == 3
        assert colors[0].startswith("#")  # Should be a hex color
        assert colors[2].startswith("#")  # Should be a hex color
        assert all(color.startswith("#") for color in colors)

    def test_interpolate_colors_different_steps(self) -> None:
        """Test color interpolation with different step counts."""
        # Test with 2 steps (just start and end)
        colors_2 = interpolate_colors("#FF0000", "#0000FF", 2, method="linear")
        assert len(colors_2) == 2
        assert colors_2[0] == "#FF0000"
        assert colors_2[1] == "#0000FF"

        # Test with 10 steps
        colors_10 = interpolate_colors("#FF0000", "#0000FF", 10, method="linear")
        assert len(colors_10) == 10
        assert colors_10[0] == "#FF0000"
        assert colors_10[9] == "#0000FF"

    def test_interpolate_colors_edge_cases(self) -> None:
        """Test color interpolation edge cases."""
        # Test same color
        colors = interpolate_colors("#FF0000", "#FF0000", 3, method="linear")
        assert len(colors) == 3
        assert all(color == "#FF0000" for color in colors)

        # Test with black and white
        colors = interpolate_colors("#000000", "#FFFFFF", 3, method="linear")
        assert len(colors) == 3
        assert colors[0] == "#000000"
        assert colors[2] == "#FFFFFF"

    def test_interpolate_colors_invalid_method(self) -> None:
        """Test color interpolation with invalid method."""
        with pytest.raises(ValueError):
            interpolate_colors("#FF0000", "#0000FF", 3, method="invalid_method")


if __name__ == "__main__":
    # Run tests with pytest
    exit_code = pytest.main([__file__, "-v"])
    sys.exit(exit_code)
