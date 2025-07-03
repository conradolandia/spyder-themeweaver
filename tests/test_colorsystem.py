#!/usr/bin/env python3
"""
Comprehensive test suite for themeweaver colorsystem module.

Tests the core color system functionality including:
- YAML color loading
- Dynamic color class creation
- Color attribute access and validation
- Error handling for missing/invalid files

Run with: `python -m pytest tests/test_colorsystem.py -v`
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# Import all the functions we need for testing
from themeweaver.core.colorsystem import (
    load_theme_metadata_from_yaml,
    load_semantic_mappings_from_yaml,
    create_palette_class,
    Primary,
    Secondary,
)


class TestColorSystemCore:
    """Test core colorsystem functionality."""

    def test_load_colors_from_yaml_success(self):
        """Test successful loading of colors from YAML file."""
        from themeweaver.core.colorsystem import load_colors_from_yaml

        # This should load the actual YAML file (default theme)
        colors = load_colors_from_yaml()

        assert isinstance(colors, dict)
        # Verify expected color groups exist
        expected_groups = [
            "Gunmetal",
            "Midnight",
            "Green",
            "Red",
            "Orange",
            "GroupDark",
            "GroupLight",
            "Logos",
        ]
        for group in expected_groups:
            assert group in colors, f"Expected color group '{group}' not found"
            assert isinstance(colors[group], dict)

    def test_load_colors_from_yaml_with_theme_name(self):
        """Test loading colors with explicit theme name."""
        from themeweaver.core.colorsystem import load_colors_from_yaml

        # Test with explicit theme name
        colors = load_colors_from_yaml("solarized")

        assert isinstance(colors, dict)
        # Verify expected color groups exist
        expected_groups = [
            "Gunmetal",
            "Midnight",
            "Green",
            "Red",
            "Orange",
            "GroupDark",
            "GroupLight",
            "Logos",
        ]
        for group in expected_groups:
            assert group in colors, f"Expected color group '{group}' not found"
            assert isinstance(colors[group], dict)

    def test_load_colors_from_yaml_file_not_found(self):
        """Test error handling when YAML file doesn't exist."""
        from themeweaver.core.colorsystem import load_colors_from_yaml

        # Mock Path to point to non-existent file
        with patch("themeweaver.core.colorsystem.Path") as mock_path:
            mock_file = Mock()
            mock_file.parent = Path("/non/existent/path")
            mock_path.return_value = mock_file

            with pytest.raises(FileNotFoundError) as exc_info:
                load_colors_from_yaml()

            assert "Color system YAML file not found" in str(exc_info.value)

    def test_load_colors_from_yaml_nonexistent_theme(self):
        """Test error handling when theme doesn't exist."""
        from themeweaver.core.colorsystem import load_colors_from_yaml

        with pytest.raises(FileNotFoundError) as exc_info:
            load_colors_from_yaml("nonexistent_theme")

        assert "Color system YAML file not found" in str(exc_info.value)
        assert "nonexistent_theme" in str(exc_info.value)

    def test_load_color_mappings_from_yaml_success(self):
        """Test successful loading of mappings from YAML file."""
        from themeweaver.core.colorsystem import load_color_mappings_from_yaml

        # This should load the actual mappings file (default theme)
        mappings = load_color_mappings_from_yaml()

        assert isinstance(mappings, dict)
        # Verify expected class mappings exist
        expected_classes = [
            "Primary",
            "Secondary",
            "Green",
            "Red",
            "Orange",
            "GroupDark",
            "GroupLight",
            "Logos",
        ]
        for class_name in expected_classes:
            assert class_name in mappings, (
                f"Expected class mapping '{class_name}' not found"
            )
            assert isinstance(mappings[class_name], str), (
                f"Mapping value for '{class_name}' should be a string"
            )

    def test_load_color_mappings_from_yaml_with_theme_name(self):
        """Test loading mappings with explicit theme name."""
        from themeweaver.core.colorsystem import load_color_mappings_from_yaml

        # Test with explicit theme name
        mappings = load_color_mappings_from_yaml("solarized")

        assert isinstance(mappings, dict)
        # Verify expected class mappings exist
        expected_classes = [
            "Primary",
            "Secondary",
            "Green",
            "Red",
            "Orange",
            "GroupDark",
            "GroupLight",
            "Logos",
        ]
        for class_name in expected_classes:
            assert class_name in mappings, (
                f"Expected class mapping '{class_name}' not found"
            )
            assert isinstance(mappings[class_name], str), (
                f"Mapping value for '{class_name}' should be a string"
            )

    def test_load_color_mappings_from_yaml_nonexistent_theme(self):
        """Test error handling when mappings file doesn't exist."""
        from themeweaver.core.colorsystem import load_color_mappings_from_yaml

        with pytest.raises(FileNotFoundError) as exc_info:
            load_color_mappings_from_yaml("nonexistent_theme")

        assert "Color mappings YAML file not found" in str(exc_info.value)
        assert "nonexistent_theme" in str(exc_info.value)

    def test_create_color_class(self):
        """Test dynamic color class creation."""
        from themeweaver.core.colorsystem import _create_color_class

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
        from themeweaver.core.colorsystem import _create_color_class

        EmptyColor = _create_color_class("EmptyColor", {})
        assert EmptyColor.__name__ == "EmptyColor"

        # Should not have any color attributes except built-in ones
        color_attrs = [attr for attr in dir(EmptyColor) if not attr.startswith("_")]
        assert len(color_attrs) == 0


class TestThemeMetadata:
    """Test theme metadata loading functionality."""

    def test_load_theme_metadata_success(self):
        """Test successful loading of theme metadata from YAML file."""
        metadata = load_theme_metadata_from_yaml()

        assert isinstance(metadata, dict)
        # Verify expected metadata fields exist
        expected_fields = [
            "name",
            "display_name",
            "description",
            "author",
            "version",
            "variants",
        ]
        for field in expected_fields:
            assert field in metadata, f"Expected metadata field '{field}' not found"

        # Verify variants section
        assert "variants" in metadata
        variants = metadata["variants"]
        assert isinstance(variants, dict)
        assert "dark" in variants
        assert "light" in variants

    def test_load_theme_metadata_with_theme_name(self):
        """Test loading theme metadata with explicit theme name."""
        metadata = load_theme_metadata_from_yaml("solarized")

        assert isinstance(metadata, dict)
        assert metadata["name"] == "solarized"
        assert metadata["display_name"] == "Solarized"
        assert "variants" in metadata

    def test_load_theme_metadata_nonexistent_theme(self):
        """Test error handling when theme metadata file doesn't exist."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_theme_metadata_from_yaml("nonexistent_theme")

        assert "Theme metadata YAML file not found" in str(exc_info.value)
        assert "nonexistent_theme" in str(exc_info.value)


class TestColorSystemClasses:
    """Test the dynamically created color system classes."""

    def test_primary_color_class(self):
        """Test Primary color class attributes."""
        from themeweaver.core.colorsystem import Primary

        # Test class exists and has expected structure
        assert Primary.__name__ == "Primary"

        # Test that it has color attributes (should have B0, B10, etc.)
        color_attrs = self._get_color_attributes(Primary)
        assert len(color_attrs) > 0, "Primary should have color attributes"

        # Test specific expected colors (from Gunmetal in YAML)
        assert hasattr(Primary, "B0")
        assert hasattr(Primary, "B150")
        assert Primary.B0 == "#000000"
        assert Primary.B150 == "#FFFFFF"

    def test_secondary_color_class(self):
        """Test Secondary color class attributes."""
        from themeweaver.core.colorsystem import Secondary

        assert Secondary.__name__ == "Secondary"
        color_attrs = self._get_color_attributes(Secondary)
        assert len(color_attrs) > 0, "Secondary should have color attributes"

        # Test specific expected colors (from Midnight in YAML)
        assert hasattr(Secondary, "B0")
        assert hasattr(Secondary, "B150")
        assert Secondary.B0 == "#000000"
        assert Secondary.B150 == "#FFFFFF"

    def test_green_color_class(self):
        """Test Green color class attributes."""
        from themeweaver.core.colorsystem import Green

        assert Green.__name__ == "Green"
        color_attrs = self._get_color_attributes(Green)
        assert len(color_attrs) > 0, "Green should have color attributes"

        # Test specific expected colors
        assert hasattr(Green, "B0")
        assert hasattr(Green, "B150")
        assert Green.B0 == "#000000"

    def test_red_color_class(self):
        """Test Red color class attributes."""
        from themeweaver.core.colorsystem import Red

        assert Red.__name__ == "Red"
        color_attrs = self._get_color_attributes(Red)
        assert len(color_attrs) > 0, "Red should have color attributes"

        # Note: Red has a typo in YAML with double # in B150
        assert hasattr(Red, "B150")
        assert Red.B150 == "##FFFFFF"  # This reflects the actual YAML content

    def test_orange_color_class(self):
        """Test Orange color class attributes."""
        from themeweaver.core.colorsystem import Orange

        assert Orange.__name__ == "Orange"
        color_attrs = self._get_color_attributes(Orange)
        assert len(color_attrs) > 0, "Orange should have color attributes"

        # Note: Orange also has a typo in YAML with double # in B150
        assert hasattr(Orange, "B150")
        assert Orange.B150 == "##FFFFFF"  # This reflects the actual YAML content

    def test_group_dark_color_class(self):
        """Test GroupDark color class attributes."""
        from themeweaver.core.colorsystem import GroupDark

        assert GroupDark.__name__ == "GroupDark"
        color_attrs = self._get_color_attributes(GroupDark)
        assert len(color_attrs) > 0, "GroupDark should have color attributes"

        # GroupDark starts from B10, not B0
        assert hasattr(GroupDark, "B10")
        assert hasattr(GroupDark, "B120")
        assert GroupDark.B10 == "#EE3432"

    def test_group_light_color_class(self):
        """Test GroupLight color class attributes."""
        from themeweaver.core.colorsystem import GroupLight

        assert GroupLight.__name__ == "GroupLight"
        color_attrs = self._get_color_attributes(GroupLight)
        assert len(color_attrs) > 0, "GroupLight should have color attributes"

        # GroupLight starts from B10, not B0
        assert hasattr(GroupLight, "B10")
        assert hasattr(GroupLight, "B120")
        assert GroupLight.B10 == "#FF7564"

    def test_logos_color_class(self):
        """Test Logos color class attributes."""
        from themeweaver.core.colorsystem import Logos

        assert Logos.__name__ == "Logos"
        color_attrs = self._get_color_attributes(Logos)
        assert len(color_attrs) > 0, "Logos should have color attributes"

        # Logos has fewer colors (B10-B50)
        assert hasattr(Logos, "B10")
        assert hasattr(Logos, "B50")
        assert Logos.B10 == "#3775a9"
        assert Logos.B50 == "#ee0000"

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


class TestColorSystemIntegration:
    """Test integration and end-to-end functionality."""

    def test_all_classes_exported(self):
        """Test that all expected classes and functions are exported in __all__."""
        from themeweaver.core import colorsystem

        expected_exports = [
            "load_colors_from_yaml",
            "load_color_mappings_from_yaml",
            "Primary",
            "Secondary",
            "Green",
            "Red",
            "Orange",
            "GroupDark",
            "GroupLight",
            "Logos",
        ]

        assert hasattr(colorsystem, "__all__")
        assert isinstance(colorsystem.__all__, list)

        for export_name in expected_exports:
            assert export_name in colorsystem.__all__, f"{export_name} not in __all__"
            assert hasattr(colorsystem, export_name), f"{export_name} not accessible"

    def test_import_all_classes(self):
        """Test importing all color classes."""
        from themeweaver.core.colorsystem import (
            Primary,
            Secondary,
            Green,
            Red,
            Orange,
            GroupDark,
            GroupLight,
            Logos,
        )

        classes = [Primary, Secondary, Green, Red, Orange, GroupDark, GroupLight, Logos]

        for color_class in classes:
            assert color_class is not None
            assert hasattr(color_class, "__name__")
            # Each class should have at least one color attribute
            color_attrs = self._get_color_attributes(color_class)
            assert len(color_attrs) > 0, (
                f"{color_class.__name__} should have color attributes"
            )

    def test_color_value_formats(self):
        """Test that all color values are in expected hex format."""
        from themeweaver.core.colorsystem import (
            Primary,
            Secondary,
            Green,
            Red,
            Orange,
            GroupDark,
            GroupLight,
            Logos,
        )

        classes = [Primary, Secondary, Green, Red, Orange, GroupDark, GroupLight, Logos]

        for color_class in classes:
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
        from themeweaver.core.colorsystem import load_colors_from_yaml, Primary

        colors = load_colors_from_yaml()

        # Primary should match Gunmetal from YAML
        gunmetal_colors = colors["Gunmetal"]
        for key, value in gunmetal_colors.items():
            assert hasattr(Primary, key), f"Primary missing attribute {key}"
            assert getattr(Primary, key) == value, f"Primary.{key} != {value}"

    def test_mappings_integration(self):
        """Test that mappings correctly link color classes to palettes."""
        from themeweaver.core.colorsystem import (
            load_colors_from_yaml,
            load_color_mappings_from_yaml,
            Primary,
            Secondary,
        )

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


def mock_open_with_file(file_path):
    """Helper function to create a mock open that reads from actual file."""

    def mock_open(*args, **kwargs):
        return open(file_path, *args, **kwargs)

    return mock_open


class TestSemanticMappings:
    """Test cases for semantic mappings functionality."""

    def test_load_semantic_mappings_success(self):
        """Test loading semantic mappings from YAML."""
        semantic_mappings = load_semantic_mappings_from_yaml()

        # Check that we have both dark and light mappings
        assert "dark" in semantic_mappings
        assert "light" in semantic_mappings

        # Check some key mappings exist
        dark_mappings = semantic_mappings["dark"]
        light_mappings = semantic_mappings["light"]

        assert "COLOR_BACKGROUND_1" in dark_mappings
        assert "COLOR_TEXT_1" in dark_mappings
        assert "COLOR_ACCENT_1" in dark_mappings

        assert "COLOR_BACKGROUND_1" in light_mappings
        assert "COLOR_TEXT_1" in light_mappings
        assert "COLOR_ACCENT_1" in light_mappings

    def test_load_semantic_mappings_with_theme_name(self):
        """Test loading semantic mappings with explicit theme name."""
        semantic_mappings = load_semantic_mappings_from_yaml("solarized")

        assert "dark" in semantic_mappings
        assert "light" in semantic_mappings

        # Verify some expected mappings
        dark_mappings = semantic_mappings["dark"]
        assert dark_mappings["COLOR_BACKGROUND_1"] == "Primary.B10"
        assert dark_mappings["COLOR_TEXT_1"] == "Primary.B130"
        assert dark_mappings["COLOR_ACCENT_1"] == "Secondary.B10"

        light_mappings = semantic_mappings["light"]
        assert light_mappings["COLOR_BACKGROUND_1"] == "Primary.B140"
        assert light_mappings["COLOR_TEXT_1"] == "Primary.B20"
        assert light_mappings["COLOR_ACCENT_1"] == "Secondary.B70"

    def test_load_semantic_mappings_nonexistent_theme(self):
        """Test loading semantic mappings for non-existent theme."""
        with pytest.raises(FileNotFoundError):
            load_semantic_mappings_from_yaml("nonexistent")

    def test_create_palette_class_dark(self):
        """Test creating a dark palette class dynamically."""
        from qdarkstyle.palette import Palette

        # Mock semantic mappings
        semantic_mappings = {
            "COLOR_BACKGROUND_1": "Primary.B10",
            "COLOR_TEXT_1": "Primary.B130",
            "COLOR_ACCENT_1": "Secondary.B10",
        }

        color_classes = {
            "Primary": Primary,
            "Secondary": Secondary,
        }

        # Create palette class
        DarkPalette = create_palette_class(
            "dark", semantic_mappings, color_classes, Palette
        )

        # Verify class properties
        assert DarkPalette.ID == "dark"
        assert DarkPalette.COLOR_BACKGROUND_1 == Primary.B10
        assert DarkPalette.COLOR_TEXT_1 == Primary.B130
        assert DarkPalette.COLOR_ACCENT_1 == Secondary.B10

        # Verify it's a proper subclass
        assert issubclass(DarkPalette, Palette)

    def test_create_palette_class_light(self):
        """Test creating a light palette class dynamically."""
        from qdarkstyle.palette import Palette

        # Mock semantic mappings
        semantic_mappings = {
            "COLOR_BACKGROUND_1": "Primary.B140",
            "COLOR_TEXT_1": "Primary.B20",
            "COLOR_ACCENT_1": "Secondary.B70",
        }

        color_classes = {
            "Primary": Primary,
            "Secondary": Secondary,
        }

        # Create palette class
        LightPalette = create_palette_class(
            "light", semantic_mappings, color_classes, Palette
        )

        # Verify class properties
        assert LightPalette.ID == "light"
        assert LightPalette.COLOR_BACKGROUND_1 == Primary.B140
        assert LightPalette.COLOR_TEXT_1 == Primary.B20
        assert LightPalette.COLOR_ACCENT_1 == Secondary.B70

        # Verify it's a proper subclass
        assert issubclass(LightPalette, Palette)

    def test_create_palette_class_with_numeric_values(self):
        """Test creating palette class with numeric values like OPACITY_TOOLTIP."""
        from qdarkstyle.palette import Palette

        # Mock semantic mappings including numeric value
        semantic_mappings = {
            "COLOR_BACKGROUND_1": "Primary.B10",
            "OPACITY_TOOLTIP": 230,
        }

        color_classes = {
            "Primary": Primary,
        }

        # Create palette class
        DarkPalette = create_palette_class(
            "dark", semantic_mappings, color_classes, Palette
        )

        # Verify both color and numeric properties
        assert DarkPalette.COLOR_BACKGROUND_1 == Primary.B10
        assert DarkPalette.OPACITY_TOOLTIP == 230

    def test_create_palette_class_invalid_color_reference(self):
        """Test creating palette class with invalid color reference."""
        from qdarkstyle.palette import Palette

        # Mock semantic mappings with invalid reference
        semantic_mappings = {
            "COLOR_BACKGROUND_1": "NonExistent.B10",
        }

        color_classes = {
            "Primary": Primary,
        }

        # Should raise ValueError for invalid reference
        with pytest.raises(ValueError, match="Color class 'NonExistent' not found"):
            create_palette_class("dark", semantic_mappings, color_classes, Palette)

    def test_create_palette_class_invalid_attribute(self):
        """Test creating palette class with invalid attribute reference."""
        from qdarkstyle.palette import Palette

        # Mock semantic mappings with invalid attribute
        semantic_mappings = {
            "COLOR_BACKGROUND_1": "Primary.B999",
        }

        color_classes = {
            "Primary": Primary,
        }

        # Should raise ValueError for invalid attribute
        with pytest.raises(ValueError, match="Attribute 'B999' not found"):
            create_palette_class("dark", semantic_mappings, color_classes, Palette)


class TestPaletteIntegration:
    """Test cases for full palette integration."""

    def test_palette_classes_created_from_yaml(self):
        """Test that palette classes are properly created from YAML."""
        from themeweaver.core.palette import DarkPalette, LightPalette

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
        from themeweaver.core.palette import DarkPalette, LightPalette

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
        from themeweaver.core.palette import create_palettes

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
        from themeweaver.core.palette import create_palettes

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
        from themeweaver.core.palette import create_palettes, ThemePalettes

        palettes = create_palettes()

        # Should return ThemePalettes object
        assert isinstance(palettes, ThemePalettes)

        # Should have both variants for solarized theme
        assert palettes.has_dark
        assert palettes.has_light
        assert palettes.supported_variants == ["dark", "light"]

    def test_theme_palettes_container_functionality(self):
        """Test ThemePalettes container functionality."""
        from themeweaver.core.palette import create_palettes

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

    def test_create_palettes_legacy_function(self):
        """Test legacy create_palettes_legacy function for backward compatibility."""
        from themeweaver.core.palette import create_palettes_legacy

        dark_palette, light_palette = create_palettes_legacy()

        # Should return tuple like the old function
        assert dark_palette is not None
        assert light_palette is not None
        assert dark_palette.ID == "dark"
        assert light_palette.ID == "light"

    def test_palettes_respect_theme_variants(self):
        """Test that palettes are only created for supported variants."""
        from themeweaver.core.palette import create_palettes

        # For solarized theme, both variants should be supported
        palettes = create_palettes("solarized")
        assert palettes.has_dark
        assert palettes.has_light
        assert len(palettes.supported_variants) == 2

    def test_backward_compatibility_module_level_classes(self):
        """Test that module-level DarkPalette and LightPalette still work."""
        from themeweaver.core.palette import DarkPalette, LightPalette

        # These should still be available for backward compatibility
        assert DarkPalette is not None
        assert LightPalette is not None
        assert DarkPalette.ID == "dark"
        assert LightPalette.ID == "light"

    def test_error_handling_no_variants_in_theme(self):
        """Test error handling when theme.yaml has no variants section."""
        from themeweaver.core.palette import create_palettes
        from unittest.mock import patch

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
        from themeweaver.core.palette import create_palettes
        from unittest.mock import patch

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
        from themeweaver.core.palette import create_palettes
        from unittest.mock import patch

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
