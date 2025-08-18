#!/usr/bin/env python3
"""
Comprehensive test suite for themeweaver color utilities.

Run with: `python -m pytest tests/test_color_utils.py -v`
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestColorUtils:
    """Test core color utility functions."""

    def test_hex_rgb_conversion(self):
        """Test hex to RGB and RGB to hex conversion."""
        from themeweaver.color_utils import hex_to_rgb, rgb_to_hex

        # Test basic conversion
        rgb = hex_to_rgb("#ff0000")
        assert rgb == (255, 0, 0)

        # Test round trip
        hex_color = rgb_to_hex(rgb)
        assert hex_color.lower() == "#ff0000"

        # Test various formats
        assert hex_to_rgb("ff0000") == (255, 0, 0)  # Without #
        assert hex_to_rgb("#FF0000") == (255, 0, 0)  # Uppercase

    def test_hsv_conversion(self):
        """Test HSV color space conversion."""
        from themeweaver.color_utils import hsv_to_rgb, rgb_to_hsv

        # Test red color
        hsv = rgb_to_hsv((255, 0, 0))
        assert len(hsv) == 3
        assert hsv[1] > 0.9  # High saturation
        assert hsv[2] > 0.9  # High value

        # Test round trip
        rgb_back = hsv_to_rgb(hsv)
        assert all(
            abs(a - b) < 2 for a, b in zip(rgb_back, (255, 0, 0))
        )  # Allow small rounding errors

    def test_lch_conversion(self):
        """Test LCH color space conversion."""
        from themeweaver.color_utils import calculate_delta_e, lch_to_hex, rgb_to_lch

        # Test conversion
        lch = rgb_to_lch((255, 0, 0))
        assert len(lch) == 3
        assert lch[0] > 0  # Lightness should be positive

        # Test round trip
        hex_from_lch = lch_to_hex(*lch)
        assert hex_from_lch.startswith("#")

        # Test delta E calculation
        delta_e = calculate_delta_e("#ff0000", "#00ff00")
        assert isinstance(delta_e, (int, float))
        assert delta_e > 0

    def test_color_info(self):
        """Test color information retrieval."""
        from themeweaver.color_utils import get_color_info

        info = get_color_info("#ff0000")
        assert isinstance(info, dict)
        assert "hex" in info
        assert "rgb" in info
        assert info["hex"] == "#ff0000"
        assert info["rgb"] == (255, 0, 0)


class TestColorGeneration:
    """Test color generation functions."""

    def test_theme_optimized_colors(self):
        """Test theme-optimized color generation."""
        from themeweaver.color_utils import generate_theme_colors

        colors = generate_theme_colors(
            theme="dark", num_colors=5, target_delta_e=25, start_hue=30
        )

        assert isinstance(colors, list)
        assert len(colors) == 5
        assert all(c.startswith("#") for c in colors)
        assert all(len(c) == 7 for c in colors)  # All should be 6-digit hex


class TestCommonPalettes:
    """Test common palette functionality."""

    def test_palette_access(self):
        """Test accessing common palettes."""
        from themeweaver.color_utils import (
            COMMON_PALETTES,
            get_all_palettes,
            get_palette,
            get_palette_names,
        )

        # Test getting names
        names = get_palette_names()
        assert isinstance(names, list)
        assert len(names) > 0

        # Test getting specific palette
        if names:
            palette = get_palette(names[0])
            assert isinstance(palette, dict)
            assert "name" in palette
            assert "colors" in palette

        # Test getting all palettes
        all_palettes = get_all_palettes()
        assert isinstance(all_palettes, dict)
        assert len(all_palettes) == len(names)

        # Test direct access
        assert isinstance(COMMON_PALETTES, dict)


class TestPaletteLoaders:
    """Test palette loading and validation."""

    def test_palette_validation(self):
        """Test palette data validation."""
        from themeweaver.color_utils import validate_palette_data

        # Valid palette
        valid_palette = {
            "name": "Test Palette",
            "colors": {"red": "#ff0000", "blue": "#0000ff"},
        }
        assert validate_palette_data(valid_palette) is True

        # Invalid palette (missing name) - should raise ValueError
        invalid_palette = {"colors": {"red": "#ff0000"}}
        try:
            validate_palette_data(invalid_palette)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected behavior

    def test_args_parsing(self):
        """Test parsing palette from command line arguments."""
        from themeweaver.color_utils import parse_palette_from_args

        args_palette = parse_palette_from_args(["red=#ff0000", "blue=#0000ff"])
        assert isinstance(args_palette, dict)
        assert "colors" in args_palette
        assert args_palette["colors"]["red"] == "#ff0000"
        assert args_palette["colors"]["blue"] == "#0000ff"


class TestCoreModules:
    """Test core themeweaver modules."""

    def test_colorsystem_import(self):
        """Test that colorsystem classes can be imported and have expected structure."""
        from themeweaver.core.colorsystem import Success, Warning, Primary, Error, Secondary

        # Test that classes have color attributes (expect them to start with #)
        color_classes = [Primary, Secondary, Success, Error, Warning]
        for color_class in color_classes:
            attrs = [
                attr
                for attr in dir(color_class)
                if not attr.startswith("_")
                and isinstance(getattr(color_class, attr), str)
            ]
            hex_attrs = [
                getattr(color_class, attr)
                for attr in attrs
                if getattr(color_class, attr).startswith("#")
            ]
            assert len(hex_attrs) > 0, (
                f"{color_class.__name__} should have hex color attributes"
            )

    def test_theme_palette_imports(self):
        """Test that theme and palette modules can be imported."""
        from themeweaver.core.palette import Palette
        from themeweaver.core.theme import Theme

        assert Theme is not None
        assert Palette is not None


class TestColorAnalysis:
    """Test color analysis functions."""

    def test_analyze_existing_colors(self):
        """Test analysis of existing color sets."""
        from themeweaver.color_utils import analyze_existing_colors

        test_colors = ["#ff0000", "#00ff00", "#0000ff"]
        analysis = analyze_existing_colors(test_colors, "Test Group")
        assert isinstance(analysis, list)
        assert len(analysis) > 0

    def test_chromatic_distances(self):
        """Test chromatic distance analysis."""
        from themeweaver.color_utils import analyze_chromatic_distances

        test_colors = ["#ff0000", "#00ff00", "#0000ff"]
        distances = analyze_chromatic_distances(test_colors, "Test Group")
        # This function returns a list of distance dictionaries
        assert isinstance(distances, list)
        assert len(distances) == 2  # 3 colors -> 2 distance measurements
        assert all("delta_e" in d for d in distances)

    def test_palette_lch_analysis(self):
        """Test LCH palette analysis."""
        from themeweaver.color_utils import analyze_palette_lch

        test_palette = {
            "name": "Test Palette",
            "colors": {"red": "#ff0000", "green": "#00ff00", "blue": "#0000ff"},
        }

        analysis = analyze_palette_lch(test_palette)
        # This function returns a list of (name, hex, L, C, H) tuples
        assert isinstance(analysis, list)
        assert len(analysis) == 3  # 3 colors in test palette
        assert all(len(item) == 5 for item in analysis)  # Each item has 5 elements


if __name__ == "__main__":
    # Run tests with pytest
    exit_code = pytest.main([__file__, "-v"])
    sys.exit(exit_code)
