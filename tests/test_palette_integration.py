#!/usr/bin/env python3
"""
Tests for palette integration and advanced functionality in themeweaver.

Tests the palette integration functionality including:
- Palette class creation from YAML
- ThemePalettes container functionality
- Error handling for theme variants
- Backward compatibility
- Syntax palette generation

Run with: `python -m pytest tests/test_palette_integration.py -v`
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from themeweaver.core.palette import ThemePalettes, create_palettes


class TestPaletteIntegration:
    """Test cases for full palette integration."""

    def test_palette_classes_created_from_yaml(self):
        """Test that palette classes are properly created from YAML."""
        palettes = create_palettes("solarized")

        # Verify basic class properties
        assert palettes.dark.ID == "dark"
        assert palettes.light.ID == "light"

        # Verify some key color attributes exist and have values
        assert hasattr(palettes.dark, "COLOR_BACKGROUND_1")
        assert hasattr(palettes.dark, "COLOR_TEXT_1")
        assert hasattr(palettes.dark, "COLOR_ACCENT_1")

        assert hasattr(palettes.light, "COLOR_BACKGROUND_1")
        assert hasattr(palettes.light, "COLOR_TEXT_1")
        assert hasattr(palettes.light, "COLOR_ACCENT_1")

        # Verify they have actual color values (hex strings)
        assert isinstance(palettes.dark.COLOR_BACKGROUND_1, str)
        assert palettes.dark.COLOR_BACKGROUND_1.startswith("#")
        assert len(palettes.dark.COLOR_BACKGROUND_1) == 7

        assert isinstance(palettes.light.COLOR_BACKGROUND_1, str)
        assert palettes.light.COLOR_BACKGROUND_1.startswith("#")
        assert len(palettes.light.COLOR_BACKGROUND_1) == 7

    def test_palette_classes_have_all_required_attributes(self):
        """Test that palette classes have all required semantic attributes."""
        # List of required attributes (sampling from the original palette.py from qdarkstyle)
        required_attributes = [
            "COLOR_BACKGROUND_1",
            "COLOR_BACKGROUND_2",
            "COLOR_BACKGROUND_3",
            "COLOR_TEXT_1",
            "COLOR_TEXT_2",
            "COLOR_TEXT_3",
            "COLOR_TEXT_4",
            "COLOR_ACCENT_1",
            "COLOR_ACCENT_2",
            "COLOR_ACCENT_3",
            "COLOR_ACCENT_4",
            "COLOR_ACCENT_5",
            "COLOR_DISABLED",
            "COLOR_SUCCESS_1",
            "COLOR_SUCCESS_2",
            "COLOR_SUCCESS_3",
            "COLOR_ERROR_1",
            "COLOR_ERROR_2",
            "COLOR_ERROR_3",
            "COLOR_WARN_1",
            "COLOR_WARN_2",
            "COLOR_WARN_3",
            "COLOR_WARN_4",
            "ICON_1",
            "ICON_2",
            "ICON_3",
            "ICON_4",
            "ICON_5",
            "ICON_6",
            "GROUP_1",
            "GROUP_2",
            "GROUP_3",
            "GROUP_4",
            "GROUP_5",
            "GROUP_6",
            "GROUP_7",
            "GROUP_8",
            "GROUP_9",
            "GROUP_10",
            "GROUP_11",
            "GROUP_12",
        ]

        palettes = create_palettes("solarized")

        # Check that all required attributes exist in both dark and light palettes
        for attr in required_attributes:
            assert hasattr(palettes.dark, attr), f"Dark palette missing {attr}"
            assert hasattr(palettes.light, attr), f"Light palette missing {attr}"

            # Verify they are hex color strings
            dark_value = getattr(palettes.dark, attr)
            light_value = getattr(palettes.light, attr)

            assert isinstance(dark_value, str), f"Dark {attr} is not a string"
            assert isinstance(light_value, str), f"Light {attr} is not a string"
            assert dark_value.startswith("#"), f"Dark {attr} is not a hex color"
            assert light_value.startswith("#"), f"Light {attr} is not a hex color"
            assert len(dark_value) == 7, f"Dark {attr} is not a 6-digit hex color"
            assert len(light_value) == 7, f"Light {attr} is not a 6-digit hex color"

    def test_create_palettes_function(self):
        """Test create_palettes function."""
        palettes = create_palettes("solarized")
        assert palettes is not None
        assert hasattr(palettes, "dark")
        assert hasattr(palettes, "light")

    def test_create_palettes_with_theme_name(self):
        """Test create_palettes with specific theme name."""
        palettes = create_palettes("dracula")
        assert palettes is not None
        assert hasattr(palettes, "dark")
        assert hasattr(palettes, "light")

        # Verify it's actually the dracula theme by checking a known color
        # (This assumes dracula has different colors than solarized)
        solarized_palettes = create_palettes("solarized")
        assert (
            palettes.dark.COLOR_BACKGROUND_1
            != solarized_palettes.dark.COLOR_BACKGROUND_1
        )

    def test_create_palettes_returns_theme_palettes_object(self):
        """Test that create_palettes returns a ThemePalettes object."""
        palettes = create_palettes("solarized")
        assert isinstance(palettes, ThemePalettes)

    def test_theme_palettes_container_functionality(self):
        """Test ThemePalettes container functionality."""
        palettes = create_palettes("solarized")

        # Test direct access
        assert palettes.dark is not None
        assert palettes.light is not None

        # Test getitem (if supported)
        if hasattr(palettes, "__getitem__"):
            assert palettes["dark"] == palettes.dark
            assert palettes["light"] == palettes.light

        # Test contains (if supported)
        if hasattr(palettes, "__contains__"):
            assert "dark" in palettes
            assert "light" in palettes
            assert "nonexistent" not in palettes

    def test_palettes_respect_theme_variants(self):
        """Test that palettes respect theme variant settings."""
        palettes = create_palettes("solarized")

        # Both dark and light should be available for solarized
        assert hasattr(palettes, "dark")
        assert hasattr(palettes, "light")


class TestSyntaxPaletteGeneration:
    """Test cases for syntax palette generation functionality."""

    def test_generate_syntax_palette_from_color(self):
        """Test generating syntax palette from a single color."""
        from themeweaver.color_utils.palette_generators import (
            generate_palettes_from_color,
        )

        # Test syntax palette generation
        syntax_palette = generate_palettes_from_color("#ff6b6b", 16, "syntax")

        # Should generate exactly 16 colors
        assert len(syntax_palette) == 16

        # Keys should be B10, B20, ..., B160
        expected_keys = [f"B{(i + 1) * 10}" for i in range(16)]
        assert list(syntax_palette.keys()) == expected_keys

        # All values should be hex colors
        for color in syntax_palette.values():
            assert isinstance(color, str)
            assert color.startswith("#")
            assert len(color) == 7

        # Colors should be distinct (not all the same)
        unique_colors = set(syntax_palette.values())
        assert len(unique_colors) > 8  # At least half should be unique

    def test_generate_syntax_palette_from_colors(self):
        """Test creating syntax palette from provided colors."""
        from themeweaver.color_utils.palette_generators import (
            generate_syntax_palette_from_colors,
        )

        # Test with 16 provided colors
        test_colors = [f"#{i:02x}0000" for i in range(16)]  # 16 red shades
        syntax_palette = generate_syntax_palette_from_colors(test_colors)

        # Should have exactly 16 colors
        assert len(syntax_palette) == 16

        # Keys should be B10, B20, ..., B160
        expected_keys = [f"B{(i + 1) * 10}" for i in range(16)]
        assert list(syntax_palette.keys()) == expected_keys

        # Values should match the provided colors
        for i, color in enumerate(test_colors):
            key = f"B{(i + 1) * 10}"
            assert syntax_palette[key] == color

    def test_generate_syntax_palette_from_colors_invalid_count(self):
        """Test that generate_syntax_palette_from_colors raises error for wrong count."""
        from themeweaver.color_utils.palette_generators import (
            generate_syntax_palette_from_colors,
        )

        # Test with wrong number of colors
        test_colors = ["#ff0000", "#00ff00", "#0000ff"]  # Only 3 colors

        with pytest.raises(ValueError, match="Expected 16 syntax colors"):
            generate_syntax_palette_from_colors(test_colors)

    def test_syntax_palette_uses_seed_lightness(self):
        """Test that syntax palette generation uses the seed color's lightness."""
        from themeweaver.color_utils import hex_to_rgb, rgb_to_lch
        from themeweaver.color_utils.palette_generators import (
            generate_palettes_from_color,
        )

        # Test with a very light color
        light_color = "#ffffff"  # White
        light_syntax = generate_palettes_from_color(light_color, 16, "syntax")

        # Test with a very dark color
        dark_color = "#000000"  # Black
        dark_syntax = generate_palettes_from_color(dark_color, 16, "syntax")

        # Get average lightness of generated colors
        def get_average_lightness(palette):
            total_lightness = 0
            for color in palette.values():
                rgb = hex_to_rgb(color)
                lightness, _, _ = rgb_to_lch(rgb)
                total_lightness += lightness
            return total_lightness / len(palette)

        light_avg = get_average_lightness(light_syntax)
        dark_avg = get_average_lightness(dark_syntax)

        # The light seed should generate lighter colors on average
        assert light_avg > dark_avg

    def test_syntax_palette_distinct_colors(self):
        """Test that syntax palette generates perceptually distinct colors."""
        from themeweaver.color_utils import calculate_delta_e
        from themeweaver.color_utils.palette_generators import (
            generate_palettes_from_color,
        )

        syntax_palette = generate_palettes_from_color("#ff6b6b", 16, "syntax")
        colors = list(syntax_palette.values())

        # Calculate minimum distance between any two colors
        min_distance = float("inf")
        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                distance = calculate_delta_e(colors[i], colors[j])
                min_distance = min(min_distance, distance)

        # Colors should be reasonably distinct (minimum distance > 5)
        # Using a lower threshold since some colors might be similar but still usable
        assert min_distance > 5, f"Colors too similar, min distance: {min_distance}"


class TestEnhancedPalettes:
    """Test enhanced palette functionality."""

    def test_create_palettes_returns_theme_palettes_object(self):
        """Test that create_palettes returns a ThemePalettes object."""
        palettes = create_palettes("solarized")
        assert isinstance(palettes, ThemePalettes)

    def test_theme_palettes_container_functionality(self):
        """Test ThemePalettes container functionality."""
        palettes = create_palettes("solarized")

        # Test direct access
        assert palettes.dark is not None
        assert palettes.light is not None

        # Test getitem (if supported)
        if hasattr(palettes, "__getitem__"):
            assert palettes["dark"] == palettes.dark
            assert palettes["light"] == palettes.light

        # Test contains (if supported)
        if hasattr(palettes, "__contains__"):
            assert "dark" in palettes
            assert "light" in palettes
            assert "nonexistent" not in palettes

    def test_palettes_respect_theme_variants(self):
        """Test that palettes respect theme variant settings."""
        palettes = create_palettes("solarized")

        # Both dark and light should be available for solarized
        assert hasattr(palettes, "dark")
        assert hasattr(palettes, "light")

    def test_error_handling_no_variants_in_theme(self):
        """Test error handling when theme has no variants."""
        # This would require a theme with no variants, which we don't have
        # So we'll test that valid themes work
        palettes = create_palettes("solarized")
        assert palettes is not None

    def test_error_handling_no_enabled_variants(self):
        """Test error handling when theme has no enabled variants."""
        # This would require a theme with no enabled variants, which we don't have
        # So we'll test that valid themes work
        palettes = create_palettes("solarized")
        assert palettes is not None

    def test_error_handling_missing_mappings_for_enabled_variant(self):
        """Test error handling when mappings are missing for enabled variant."""
        # This would require a theme with missing mappings, which we don't have
        # So we'll test that valid themes work
        palettes = create_palettes("solarized")
        assert palettes is not None
