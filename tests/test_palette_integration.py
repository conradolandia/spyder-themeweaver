#!/usr/bin/env python3
"""
Tests for palette integration and advanced functionality in themeweaver.

Tests the palette integration functionality including:
- Palette class creation from YAML
- ThemePalettes container functionality
- Error handling for theme variants
- Backward compatibility

Run with: `python -m pytest tests/test_palette_integration.py -v`
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from themeweaver.core.palette import (
    create_palettes,
    ThemePalettes,
    DarkPalette,
    LightPalette,
)


class TestPaletteIntegration:
    """Test cases for full palette integration."""

    def test_palette_classes_created_from_yaml(self):
        """Test that palette classes are properly created from YAML."""
        # Verify basic class properties
        assert DarkPalette.ID == "dark"
        assert LightPalette.ID == "light"

        # Verify some key color attributes exist and have values
        assert hasattr(DarkPalette, "COLOR_BACKGROUND_1")
        assert hasattr(DarkPalette, "COLOR_TEXT_1")
        assert hasattr(DarkPalette, "COLOR_ACCENT_1")

        assert hasattr(LightPalette, "COLOR_BACKGROUND_1")
        assert hasattr(LightPalette, "COLOR_TEXT_1")
        assert hasattr(LightPalette, "COLOR_ACCENT_1")

        # Verify they have actual color values (hex strings)
        assert isinstance(DarkPalette.COLOR_BACKGROUND_1, str)
        assert DarkPalette.COLOR_BACKGROUND_1.startswith("#")
        assert len(DarkPalette.COLOR_BACKGROUND_1) == 7

        assert isinstance(LightPalette.COLOR_BACKGROUND_1, str)
        assert LightPalette.COLOR_BACKGROUND_1.startswith("#")
        assert len(LightPalette.COLOR_BACKGROUND_1) == 7

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
            "COLOR_HIGHLIGHT_1",
            "COLOR_HIGHLIGHT_2",
            "COLOR_HIGHLIGHT_3",
            "COLOR_HIGHLIGHT_4",
            "COLOR_OCCURRENCE_1",
            "COLOR_OCCURRENCE_2",
            "COLOR_OCCURRENCE_3",
            "COLOR_OCCURRENCE_4",
            "COLOR_OCCURRENCE_5",
            "PYTHON_LOGO_UP",
            "PYTHON_LOGO_DOWN",
            "SPYDER_LOGO_BACKGROUND",
            "SPYDER_LOGO_WEB",
            "SPYDER_LOGO_SNAKE",
            "SPECIAL_TABS_SEPARATOR",
            "SPECIAL_TABS_SELECTED",
            "COLOR_HEART",
            "TIP_TITLE_COLOR",
            "TIP_CHAR_HIGHLIGHT_COLOR",
            "OPACITY_TOOLTIP",
        ]

        # Check that both palette classes have all required attributes
        for attr in required_attributes:
            assert hasattr(DarkPalette, attr), f"DarkPalette missing attribute: {attr}"
            assert hasattr(LightPalette, attr), (
                f"LightPalette missing attribute: {attr}"
            )

    def test_create_palettes_function(self):
        """Test the create_palettes function."""
        # Create palettes for default theme
        palettes = create_palettes()

        # Verify they are properly created classes
        assert palettes.dark.ID == "dark"
        assert palettes.light.ID == "light"

        # Verify they have expected attributes
        assert hasattr(palettes.dark, "COLOR_BACKGROUND_1")
        assert hasattr(palettes.light, "COLOR_BACKGROUND_1")

    def test_create_palettes_with_theme_name(self):
        """Test creating palettes with explicit theme name."""
        # Create palettes for solarized theme
        palettes = create_palettes("solarized")

        # Verify they are properly created
        assert palettes.dark.ID == "dark"
        assert palettes.light.ID == "light"

        # Verify they have expected attributes
        assert hasattr(palettes.dark, "COLOR_BACKGROUND_1")
        assert hasattr(palettes.light, "COLOR_BACKGROUND_1")


class TestEnhancedPalettes:
    """Test cases for enhanced palette functionality with theme variant support."""

    def test_create_palettes_returns_theme_palettes_object(self):
        """Test that create_palettes returns ThemePalettes object."""
        palettes = create_palettes()

        # Should return ThemePalettes object
        assert isinstance(palettes, ThemePalettes)

        # Should have both variants for solarized theme
        assert palettes.has_dark
        assert palettes.has_light
        assert palettes.supported_variants == ["dark", "light"]

    def test_theme_palettes_container_functionality(self):
        """Test ThemePalettes container functionality."""
        palettes = create_palettes()

        # Test palette access methods
        dark_palette = palettes.get_palette("dark")
        light_palette = palettes.get_palette("light")
        invalid_palette = palettes.get_palette("invalid")

        assert dark_palette is not None
        assert light_palette is not None
        assert invalid_palette is None

        # Test direct access
        assert palettes.dark is not None
        assert palettes.light is not None

        # Test IDs
        assert dark_palette.ID == "dark"
        assert light_palette.ID == "light"

    def test_palettes_respect_theme_variants(self):
        """Test that palettes are only created for supported variants."""
        # For solarized theme, both variants should be supported
        palettes = create_palettes("solarized")
        assert palettes.has_dark
        assert palettes.has_light
        assert len(palettes.supported_variants) == 2

    def test_backward_compatibility_module_level_classes(self):
        """Test that module-level DarkPalette and LightPalette still work."""
        # These should still be available for backward compatibility
        assert DarkPalette is not None
        assert LightPalette is not None
        assert DarkPalette.ID == "dark"
        assert LightPalette.ID == "light"

    def test_error_handling_no_variants_in_theme(self):
        """Test error handling when theme.yaml has no variants section."""
        # Mock theme metadata with no variants
        mock_metadata = {"name": "solarized", "description": "solarized theme"}

        with patch(
            "themeweaver.core.palette.load_theme_metadata_from_yaml",
            return_value=mock_metadata,
        ):
            with pytest.raises(ValueError, match="No variants specified for theme"):
                create_palettes("solarized")

    def test_error_handling_no_enabled_variants(self):
        """Test error handling when all variants are disabled."""
        # Mock theme metadata with all variants disabled
        mock_metadata = {
            "name": "solarized",
            "description": "solarized theme",
            "variants": {"dark": False, "light": False},
        }

        # Mock semantic mappings (won't be used but needed to avoid file load)
        mock_mappings = {"dark": {}, "light": {}}

        with patch(
            "themeweaver.core.palette.load_theme_metadata_from_yaml",
            return_value=mock_metadata,
        ):
            with patch(
                "themeweaver.core.palette.load_semantic_mappings_from_yaml",
                return_value=mock_mappings,
            ):
                with pytest.raises(ValueError, match="has no enabled variants"):
                    create_palettes("solarized")

    def test_error_handling_missing_mappings_for_enabled_variant(self):
        """Test error handling when enabled variant has no semantic mappings."""
        # Mock theme metadata with dark enabled
        mock_metadata = {
            "name": "solarized",
            "description": "solarized theme",
            "variants": {"dark": True, "light": False},
        }

        # Mock semantic mappings with no dark section
        mock_mappings = {"light": {"COLOR_BACKGROUND_1": "Primary.B10"}}

        with patch(
            "themeweaver.core.palette.load_theme_metadata_from_yaml",
            return_value=mock_metadata,
        ):
            with patch(
                "themeweaver.core.palette.load_semantic_mappings_from_yaml",
                return_value=mock_mappings,
            ):
                with pytest.raises(
                    ValueError,
                    match="supports dark variant but no dark semantic mappings found",
                ):
                    create_palettes("solarized")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
