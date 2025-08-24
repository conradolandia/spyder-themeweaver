#!/usr/bin/env python3
"""
Test suite for color gamut handling and palette generation functions.

Tests the new functionality for:
- Detecting colors outside sRGB gamut
- Adjusting out-of-gamut colors
- Generating palettes from single colors
- Generating group palettes

Run with: `python -m pytest tests/test_gamut_handling.py -v`
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestGamutHandling:
    """Test gamut detection and adjustment functions."""

    def test_is_lch_in_gamut(self) -> None:
        """Test detection of colors within and outside the sRGB gamut."""
        from themeweaver.color_utils import is_lch_in_gamut

        # Known in-gamut colors
        assert is_lch_in_gamut(50, 30, 0)  # Medium red
        assert is_lch_in_gamut(50, 30, 90)  # Medium yellow-green
        assert is_lch_in_gamut(50, 0, 0)  # Medium gray (no chroma)
        assert is_lch_in_gamut(0, 0, 0)  # Black
        assert is_lch_in_gamut(100, 0, 0)  # White

        # Known out-of-gamut colors (very high chroma)
        assert not is_lch_in_gamut(50, 150, 270)  # Super saturated blue
        assert not is_lch_in_gamut(80, 150, 0)  # Super saturated light red

        # Edge cases
        assert is_lch_in_gamut(50, 0, 400)  # Hue > 360 is fine if chroma is 0
        assert not is_lch_in_gamut(-10, 30, 0)  # Negative lightness is invalid

    def test_find_max_in_gamut_chroma(self) -> None:
        """Test finding maximum in-gamut chroma for a given lightness and hue."""
        from themeweaver.color_utils import find_max_in_gamut_chroma, is_lch_in_gamut

        # Test for various lightness/hue combinations
        test_cases = [
            (50, 0),  # Medium red
            (50, 90),  # Medium yellow-green
            (50, 180),  # Medium cyan
            (50, 270),  # Medium blue
            (20, 0),  # Dark red
            (80, 0),  # Light red
        ]

        for lightness, hue in test_cases:
            max_chroma = find_max_in_gamut_chroma(lightness, hue)

            # The max chroma should be in gamut
            assert is_lch_in_gamut(lightness, max_chroma, hue)

            # A slightly higher chroma should be out of gamut
            assert not is_lch_in_gamut(lightness, max_chroma + 1.0, hue)

    def test_adjust_lch_to_gamut(self) -> None:
        """Test adjusting out-of-gamut colors."""
        from themeweaver.color_utils import adjust_lch_to_gamut, is_lch_in_gamut

        # Test with a color that's out of gamut
        lightness = 50
        chroma = 150  # Very high, likely out of gamut
        hue = 270  # Blue

        # Default mode (preserve lightness)
        adjusted_l, adjusted_c, adjusted_h = adjust_lch_to_gamut(lightness, chroma, hue)
        assert adjusted_l == lightness  # Lightness should be preserved
        assert adjusted_c < chroma  # Chroma should be reduced
        assert adjusted_h == hue  # Hue should be preserved
        assert is_lch_in_gamut(
            adjusted_l, adjusted_c, adjusted_h
        )  # Should be in gamut now

        # Preserve chroma mode
        adjusted_l, adjusted_c, adjusted_h = adjust_lch_to_gamut(
            lightness, chroma, hue, preserve="chroma"
        )
        # Either lightness changed or we fell back to preserving lightness
        assert adjusted_l != lightness or adjusted_c < chroma
        assert is_lch_in_gamut(
            adjusted_l, adjusted_c, adjusted_h
        )  # Should be in gamut now

        # Both mode
        adjusted_l, adjusted_c, adjusted_h = adjust_lch_to_gamut(
            lightness, chroma, hue, preserve="both"
        )
        assert is_lch_in_gamut(
            adjusted_l, adjusted_c, adjusted_h
        )  # Should be in gamut now

    def test_already_in_gamut_color(self) -> None:
        """Test that in-gamut colors are not modified."""
        from themeweaver.color_utils import adjust_lch_to_gamut

        # Use a color that's definitely in gamut
        lightness = 50
        chroma = 20
        hue = 0

        adjusted_l, adjusted_c, adjusted_h = adjust_lch_to_gamut(lightness, chroma, hue)
        assert adjusted_l == lightness
        assert adjusted_c == chroma
        assert adjusted_h == hue


class TestPaletteGeneration:
    """Test palette generation from single colors."""

    def test_generate_lightness_gradient_from_color(self) -> None:
        """Test generating a complete lightness gradient from a single color."""
        from themeweaver.color_utils.palette_generators import (
            generate_lightness_gradient_from_color,
        )

        # Test with a medium blue color
        palette = generate_lightness_gradient_from_color("#1A72BB")

        # Should generate 16 colors
        assert len(palette) == 16

        # First color should be black, last should be white
        assert palette[0] == "#000000"
        assert palette[15] == "#FFFFFF"

        # The original color should be somewhere in the middle
        # (not testing exact position as it depends on the algorithm)
        assert "#1A72BB" in palette or any(
            color.lower() == "#1a72bb" for color in palette
        )

        # Colors should form a gradient (each color should be different from neighbors)
        for i in range(len(palette) - 1):
            assert palette[i] != palette[i + 1]

    def test_natural_position_calculation(self) -> None:
        """Test that colors are positioned correctly based on lightness."""
        from themeweaver.color_utils import hex_to_rgb, rgb_to_lch
        from themeweaver.color_utils.palette_generators import (
            generate_lightness_gradient_from_color,
        )

        # Test with a dark color
        dark_color = "#1A1A1A"  # Very dark gray
        dark_palette = generate_lightness_gradient_from_color(dark_color)

        # Should be positioned near the beginning of the palette
        dark_pos = dark_palette.index(dark_color) if dark_color in dark_palette else -1
        if dark_pos == -1:  # If exact color not found due to gamut adjustment
            dark_l = rgb_to_lch(hex_to_rgb(dark_color))[0]
            # Find closest color by lightness
            closest_pos = 0
            closest_diff = 100
            for i, color in enumerate(dark_palette):
                lightness = rgb_to_lch(hex_to_rgb(color))[0]
                diff = abs(lightness - dark_l)
                if diff < closest_diff:
                    closest_diff = diff
                    closest_pos = i
            dark_pos = closest_pos

        assert 1 <= dark_pos <= 4  # Should be in the first few positions

        # Test with a light color
        light_color = "#E0E0E0"  # Very light gray
        light_palette = generate_lightness_gradient_from_color(light_color)

        # Should be positioned near the end of the palette
        light_pos = (
            light_palette.index(light_color) if light_color in light_palette else -1
        )
        if light_pos == -1:  # If exact color not found due to gamut adjustment
            light_l = rgb_to_lch(hex_to_rgb(light_color))[0]
            # Find closest color by lightness
            closest_pos = 0
            closest_diff = 100
            for i, color in enumerate(light_palette):
                lightness = rgb_to_lch(hex_to_rgb(color))[0]
                diff = abs(lightness - light_l)
                if diff < closest_diff:
                    closest_diff = diff
                    closest_pos = i
            light_pos = closest_pos

        assert 11 <= light_pos <= 14  # Should be in the last few positions

    def test_generate_group_palettes(self) -> None:
        """Test generating GroupDark and GroupLight palettes."""
        from themeweaver.color_utils.palette_generators import (
            generate_palettes_from_color,
        )

        # Test with a red color
        group_dark, group_light = generate_palettes_from_color("#E11C1C")

        # Should generate 12 colors for each palette
        assert len(group_dark) == 12
        assert len(group_light) == 12

        # Keys should be B10, B20, etc.
        for i in range(1, 13):
            key = f"B{i * 10}"
            assert key in group_dark
            assert key in group_light

        # First color in GroupDark should be the provided color
        assert group_dark["B10"] == "#E11C1C"

        # First color in GroupLight should be lighter than the provided color
        from themeweaver.color_utils import hex_to_rgb, rgb_to_lch

        dark_l = rgb_to_lch(hex_to_rgb("#E11C1C"))[0]
        light_l = rgb_to_lch(hex_to_rgb(group_light["B10"]))[0]

        assert light_l > dark_l  # Light version should have higher lightness

        # Colors should be distributed around the color wheel (different hues)
        dark_hues = []
        for color in group_dark.values():
            _, _, hue = rgb_to_lch(hex_to_rgb(color))
            dark_hues.append(hue)

        # Check that hues are distributed (not all the same)
        assert len(set([round(h / 30) for h in dark_hues])) > 3

    def test_generate_theme_from_colors(self) -> None:
        """Test generating a complete theme from individual colors."""
        from themeweaver.color_utils.theme_generator_utils import (
            generate_theme_from_colors,
        )

        # Generate a theme with test colors
        theme = generate_theme_from_colors(
            primary_color="#1A72BB",
            secondary_color="#FF5500",
            error_color="#E11C1C",
            success_color="#00AA55",
            warning_color="#FF9900",
            group_initial_color="#8844EE",
        )

        # Should contain colorsystem and mappings
        assert "colorsystem" in theme
        assert "mappings" in theme

        colorsystem = theme["colorsystem"]
        mappings = theme["mappings"]

        # Should contain all required palettes in colorsystem
        assert len(colorsystem) >= 8  # At least 7 palettes + Logos

        # Check that mappings contain the semantic names
        assert "color_classes" in mappings
        color_classes = mappings["color_classes"]
        assert "Primary" in color_classes
        assert "Secondary" in color_classes
        assert "Error" in color_classes
        assert "Success" in color_classes
        assert "Warning" in color_classes
        assert "GroupDark" in color_classes
        assert "GroupLight" in color_classes
        assert "Logos" in color_classes

        # Check that the mapped palette names exist in colorsystem
        for semantic_name, palette_name in color_classes.items():
            assert palette_name in colorsystem

        # Check that main palettes have the expected structure
        for semantic_name in ["Primary", "Secondary", "Error", "Success", "Warning"]:
            palette_name = color_classes[semantic_name]
            palette = colorsystem[palette_name]
            assert "B0" in palette
            assert "B150" in palette
            assert len(palette) == 16  # B0 to B150 in steps of 10

        # Check group palettes
        group_dark_name = color_classes["GroupDark"]
        group_light_name = color_classes["GroupLight"]
        assert len(colorsystem[group_dark_name]) == 12
        assert len(colorsystem[group_light_name]) == 12
        assert "B10" in colorsystem[group_dark_name]
        assert "B10" in colorsystem[group_light_name]

        # Check logos palette
        assert len(colorsystem["Logos"]) == 5
        assert "B10" in colorsystem["Logos"]
        assert "B50" in colorsystem["Logos"]

        # Check that colors are properly formatted
        for palette_name, palette in colorsystem.items():
            for key, color in palette.items():
                assert color.startswith("#")
                assert len(color) == 7  # #RRGGBB format


class TestInputValidation:
    """Test input validation for color generation."""

    def test_validate_input_colors(self) -> None:
        """Test validation of input colors."""
        from themeweaver.color_utils.theme_generator_utils import validate_input_colors

        # Valid colors
        is_valid, _ = validate_input_colors(
            "#1A72BB", "#FF5500", "#E11C1C", "#00AA55", "#FF9900", "#8844EE"
        )
        assert is_valid

        # Invalid hex format
        is_valid, error = validate_input_colors(
            "1A72BB", "#FF5500", "#E11C1C", "#00AA55", "#FF9900", "#8844EE"
        )
        assert not is_valid
        assert "not a valid hex format" in error

        # Too dark
        is_valid, error = validate_input_colors(
            "#000000", "#FF5500", "#E11C1C", "#00AA55", "#FF9900", "#8844EE"
        )
        assert not is_valid
        assert "too dark" in error

        # Too light
        is_valid, error = validate_input_colors(
            "#1A72BB", "#FFFFFF", "#E11C1C", "#00AA55", "#FF9900", "#8844EE"
        )
        assert not is_valid
        assert "too light" in error

        # Very low saturation (but still valid now)
        is_valid, error = validate_input_colors(
            "#1A72BB", "#FF5500", "#E11C1C", "#808080", "#FF9900", "#8844EE"
        )
        assert is_valid  # Should be valid now

        # Pure gray colors (chroma = 0) should be valid
        is_valid, error = validate_input_colors(
            "#3f3f3f", "#1A72BB", "#bd6e76", "#688060", "#dfaf8f", "#cc9393"
        )
        assert is_valid, f"Gray colors should be valid: {error}"


if __name__ == "__main__":
    # Run tests with pytest
    exit_code = pytest.main([__file__, "-v"])
    sys.exit(exit_code)
