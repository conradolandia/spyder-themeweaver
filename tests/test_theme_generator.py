"""
Tests for theme generation functionality.
"""

from pathlib import Path

import pytest

from themeweaver.core.theme_generator import ThemeGenerator


class TestThemeGenerator:
    """Test theme generation functionality."""

    def test_theme_generator_init(self) -> None:
        """Test ThemeGenerator initialization."""
        generator = ThemeGenerator()
        assert generator is not None
        assert hasattr(generator, "themes_dir")

    def test_theme_exists(self) -> None:
        """Test theme existence check."""
        generator = ThemeGenerator()

        # Test with existing theme
        assert generator.theme_exists("dracula") is True
        assert generator.theme_exists("solarized") is True

        # Test with non-existing theme
        assert generator.theme_exists("nonexistent_theme") is False

    def test_list_themes(self) -> None:
        """Test theme listing."""
        generator = ThemeGenerator()

        themes = generator.list_themes()
        assert isinstance(themes, list)
        assert len(themes) > 0
        assert "dracula" in themes
        assert "solarized" in themes

    def test_generate_theme_from_data(self, tmp_path: Path) -> None:
        """Test theme generation from data."""
        themes_dir = tmp_path / "themes"
        themes_dir.mkdir()
        generator = ThemeGenerator(themes_dir=themes_dir)

        theme_data = {
            "colorsystem": {
                "palettes": {
                    "Primary": {
                        "B10": "#000000",
                        "B20": "#111111",
                    }
                }
            },
            "mappings": {
                "color_classes": {
                    "Primary": "Primary",
                    "Secondary": "Secondary",
                }
            },
        }

        files = generator.generate_theme_from_data(
            theme_name="test_theme_data",
            theme_data=theme_data,
            display_name="Test Theme",
            description="A test theme",
            author="Test Author",
            tags=["test", "demo"],
            overwrite=True,
        )

        assert isinstance(files, dict)
        assert "theme.yaml" in files
        assert "colorsystem.yaml" in files
        assert "mappings.yaml" in files

    def test_generate_theme_existing_no_overwrite(self) -> None:
        """Test theme generation with existing theme and no overwrite."""
        generator = ThemeGenerator()

        with pytest.raises(ValueError):
            generator.generate_theme_from_data(
                theme_name="dracula",  # Existing theme
                theme_data={},
                overwrite=False,
            )
