#!/usr/bin/env python3
"""
Tests for dynamic color class creation in themeweaver.

Tests the dynamic color class creation functionality including:
- Color class creation from YAML data
- Color attribute access and validation
- Integration with YAML data
- Error handling

Run with: `python -m pytest tests/test_color_classes.py -v`
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from themeweaver.core.colorsystem import (
    Error,
    GroupDark,
    GroupLight,
    Logos,
    Primary,
    Secondary,
    Success,
    Warning,
    _create_color_class,
    load_color_mappings_from_yaml,
    load_colors_from_yaml,
)


class TestColorClassCreation:
    """Test dynamic color class creation."""

    def test_create_color_class(self):
        """Test dynamic color class creation."""
        test_colors = {
            "B0": "#000000",
            "B10": "#111111",
            "B20": "#222222",
            "B150": "#FFFFFF",
        }

        TestColor = _create_color_class("TestColor", test_colors)

        # Test class creation
        assert TestColor.__name__ == "TestColor"

        # Test color attributes
        assert hasattr(TestColor, "B0")
        assert hasattr(TestColor, "B10")
        assert hasattr(TestColor, "B20")
        assert hasattr(TestColor, "B150")

        # Test color values
        assert TestColor.B0 == "#000000"
        assert TestColor.B10 == "#111111"
        assert TestColor.B20 == "#222222"
        assert TestColor.B150 == "#FFFFFF"

    def test_create_color_class_empty_colors(self):
        """Test creating color class with empty color dictionary."""
        EmptyColor = _create_color_class("EmptyColor", {})
        assert EmptyColor.__name__ == "EmptyColor"

        # Should not have any color attributes except built-in ones
        color_attrs = [attr for attr in dir(EmptyColor) if not attr.startswith("_")]
        assert len(color_attrs) == 0


class TestColorClasses:
    """Test the dynamically created color system classes."""

    def test_all_color_classes_exist(self):
        """Test that all expected color classes exist and have basic structure."""
        color_classes = [
            Primary,
            Secondary,
            Success,
            Error,
            Warning,
            GroupDark,
            GroupLight,
            Logos,
        ]

        for color_class in color_classes:
            assert color_class is not None
            assert hasattr(color_class, "__name__")

            # Each class should have color attributes
            color_attrs = self._get_color_attributes(color_class)
            assert len(color_attrs) > 0, (
                f"{color_class.__name__} should have color attributes"
            )

    def test_color_classes_have_expected_attributes(self):
        """Test that color classes have expected basic attributes."""
        # Test Primary (maps to Gunmetal)
        assert hasattr(Primary, "B0")
        assert hasattr(Primary, "B150")
        assert Primary.B0 == "#000000"
        assert Primary.B150 == "#FFFFFF"

        # Test Secondary (maps to Midnight)
        assert hasattr(Secondary, "B0")
        assert hasattr(Secondary, "B150")
        assert Secondary.B0 == "#000000"
        assert Secondary.B150 == "#FFFFFF"

        # Test GroupDark (starts from B10)
        assert hasattr(GroupDark, "B10")
        assert hasattr(GroupDark, "B120")
        assert GroupDark.B10 == "#EE3432"

        # Test GroupLight (starts from B10)
        assert hasattr(GroupLight, "B10")
        assert hasattr(GroupLight, "B120")
        assert GroupLight.B10 == "#FF7564"

        # Test Logos (has fewer colors B10-B50)
        assert hasattr(Logos, "B10")
        assert hasattr(Logos, "B50")
        assert Logos.B10 == "#3775a9"
        assert Logos.B50 == "#ee0000"

    def test_color_value_formats(self):
        """Test that all color values are in expected hex format."""
        color_classes = [
            Primary,
            Secondary,
            Success,
            Error,
            Warning,
            GroupDark,
            GroupLight,
            Logos,
        ]

        for color_class in color_classes:
            color_attrs = self._get_color_attributes(color_class)
            for attr in color_attrs:
                color_value = getattr(color_class, attr)
                # Should start with # (or ## for the typos in YAML)
                assert color_value.startswith("#"), (
                    f"{color_class.__name__}.{attr} = {color_value} should start with #"
                )
                # Should be valid hex after removing #
                hex_part = color_value.lstrip("#")
                assert len(hex_part) == 6, (
                    f"{color_class.__name__}.{attr} = {color_value} should be 6-digit hex"
                )
                # Should be valid hex characters
                try:
                    int(hex_part, 16)
                except ValueError:
                    pytest.fail(
                        f"{color_class.__name__}.{attr} = {color_value} contains invalid hex characters"
                    )

    def test_yaml_data_consistency(self):
        """Test that the loaded YAML data matches the created classes."""
        colors = load_colors_from_yaml()

        # Primary should match Gunmetal from YAML
        gunmetal_colors = colors["Gunmetal"]
        for key, value in gunmetal_colors.items():
            assert hasattr(Primary, key), f"Primary missing attribute {key}"
            assert getattr(Primary, key) == value, f"Primary.{key} != {value}"

    def test_mappings_integration(self):
        """Test that mappings correctly link color classes to palettes."""
        colors = load_colors_from_yaml()
        mappings = load_color_mappings_from_yaml()

        # Verify Primary maps to the correct palette
        primary_palette = mappings["Primary"]
        assert primary_palette in colors, (
            f"Primary maps to '{primary_palette}' but it's not in colorsystem.yaml"
        )

        # Verify that Primary class has the colors from the mapped palette
        mapped_colors = colors[primary_palette]
        for key, value in mapped_colors.items():
            assert hasattr(Primary, key), (
                f"Primary missing attribute {key} from {primary_palette}"
            )
            assert getattr(Primary, key) == value, f"Primary.{key} != {value}"

        # Same test for Secondary
        secondary_palette = mappings["Secondary"]
        assert secondary_palette in colors, (
            f"Secondary maps to '{secondary_palette}' but it's not in colorsystem.yaml"
        )

        mapped_colors = colors[secondary_palette]
        for key, value in mapped_colors.items():
            assert hasattr(Secondary, key), (
                f"Secondary missing attribute {key} from {secondary_palette}"
            )
            assert getattr(Secondary, key) == value, f"Secondary.{key} != {value}"

    def test_all_classes_exported(self):
        """Test that all expected classes and functions are exported in __all__."""
        from themeweaver.core import colorsystem

        expected_exports = [
            "load_colors_from_yaml",
            "load_color_mappings_from_yaml",
            "Primary",
            "Secondary",
            "Success",
            "Error",
            "Warning",
            "GroupDark",
            "GroupLight",
            "Logos",
        ]

        assert hasattr(colorsystem, "__all__")
        assert isinstance(colorsystem.__all__, list)

        for export_name in expected_exports:
            assert export_name in colorsystem.__all__, f"{export_name} not in __all__"
            assert hasattr(colorsystem, export_name), f"{export_name} not accessible"

    def _get_color_attributes(self, color_class):
        """Helper method to get color attributes from a class."""
        return [
            attr
            for attr in dir(color_class)
            if not attr.startswith("_")
            and isinstance(getattr(color_class, attr), str)
            and (
                getattr(color_class, attr).startswith("#")
                or getattr(color_class, attr).startswith("##")
            )
        ]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
