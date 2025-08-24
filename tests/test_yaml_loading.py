#!/usr/bin/env python3
"""
Tests for YAML loading functionality in themeweaver.

Tests the core YAML loading functions including:
- Color loading from YAML files
- Mappings loading from YAML files
- Theme metadata loading from YAML files
- Error handling for missing/invalid files

Run with: `python -m pytest tests/test_yaml_loading.py -v`
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from themeweaver.core.colorsystem import (
    load_color_mappings_from_yaml,
    load_colors_from_yaml,
    load_theme_metadata_from_yaml,
)


class TestYAMLLoading:
    """Test YAML loading functionality."""

    def test_load_colors_from_yaml_success(self) -> None:
        """Test successful loading of colors from YAML file."""
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

    def test_load_colors_from_yaml_file_not_found(self) -> None:
        """Test error handling when YAML file doesn't exist."""
        # Mock Path to point to non-existent file
        with patch("themeweaver.core.yaml_loader.Path") as mock_path:
            mock_file = Mock()
            mock_file.parent = Path("/non/existent/path")
            mock_path.return_value = mock_file

            with pytest.raises(FileNotFoundError) as exc_info:
                load_colors_from_yaml()

            assert "YAML file not found" in str(exc_info.value)

    def test_load_colors_from_yaml_nonexistent_theme(self) -> None:
        """Test error handling when theme doesn't exist."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_colors_from_yaml("nonexistent_theme")

        assert "YAML file not found" in str(exc_info.value)
        assert "nonexistent_theme" in str(exc_info.value)

    def test_load_color_mappings_from_yaml_success(self) -> None:
        """Test successful loading of mappings from YAML file."""
        mappings = load_color_mappings_from_yaml()

        assert isinstance(mappings, dict)
        # Verify expected class mappings exist
        expected_classes = [
            "Primary",
            "Secondary",
            "Success",
            "Error",
            "Warning",
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

    def test_load_color_mappings_from_yaml_nonexistent_theme(self) -> None:
        """Test error handling when mappings file doesn't exist."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_color_mappings_from_yaml("nonexistent_theme")

        assert "YAML file not found" in str(exc_info.value)
        assert "nonexistent_theme" in str(exc_info.value)

    def test_load_theme_metadata_success(self) -> None:
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

    def test_load_theme_metadata_nonexistent_theme(self) -> None:
        """Test error handling when theme metadata file doesn't exist."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_theme_metadata_from_yaml("nonexistent_theme")

        assert "YAML file not found" in str(exc_info.value)
        assert "nonexistent_theme" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
