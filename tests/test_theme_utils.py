"""
Tests for theme utility functions.
"""

from pathlib import Path

from themeweaver.core.theme_utils import (
    generate_mappings,
    generate_theme_metadata,
    write_yaml_file,
)


class TestThemeUtils:
    """Test theme utility functions."""

    def test_generate_theme_metadata(self) -> None:
        """Test theme metadata generation."""
        metadata = generate_theme_metadata(
            theme_name="test_theme",
            display_name="Test Theme",
            description="A test theme",
            author="Test Author",
            tags=["test", "demo"],
        )

        assert metadata["name"] == "test_theme"
        assert metadata["display_name"] == "Test Theme"
        assert metadata["description"] == "A test theme"
        assert metadata["author"] == "Test Author"
        assert metadata["tags"] == ["test", "demo"]
        assert metadata["variants"]["dark"] is True
        assert metadata["variants"]["light"] is True

    def test_generate_theme_metadata_defaults(self) -> None:
        """Test theme metadata generation with defaults."""
        metadata = generate_theme_metadata(
            theme_name="test_theme",
            display_name=None,
            description=None,
            author="Test Author",
            tags=None,
        )

        assert metadata["display_name"] == "Test Theme"
        assert metadata["description"] == "Generated theme: test_theme"
        assert metadata["tags"] == ["dark", "light"]

    def test_generate_mappings(self) -> None:
        """Test mappings generation."""
        colorsystem_data = {
            "_palette_names": {
                "primary": "CustomPrimary",
                "secondary": "CustomSecondary",
            }
        }

        mappings = generate_mappings(colorsystem_data)

        assert mappings["color_classes"]["Primary"] == "CustomPrimary"
        assert mappings["color_classes"]["Secondary"] == "CustomSecondary"
        assert "semantic_mappings" in mappings
        assert "dark" in mappings["semantic_mappings"]
        assert "light" in mappings["semantic_mappings"]

    def test_write_yaml_file(self, tmp_path: Path) -> None:
        """Test YAML file writing."""
        data = {"test": "value", "number": 42}
        file_path = tmp_path / "test.yaml"

        result = write_yaml_file(file_path, data)

        assert result == str(file_path)
        assert file_path.exists()

        # Read back and verify
        with open(file_path, "r") as f:
            content = f.read()
            assert "test: value" in content
            assert "number: 42" in content
