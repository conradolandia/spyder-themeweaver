"""
Tests for theme generation functionality.
"""

import pytest

from themeweaver.core.theme_generator import ThemeGenerator


class TestThemeGenerator:
    """Test theme generation functionality."""

    def test_theme_generator_init(self):
        """Test ThemeGenerator initialization."""
        generator = ThemeGenerator()
        assert generator is not None
        assert hasattr(generator, "themes_dir")

    def test_theme_exists(self):
        """Test theme existence check."""
        generator = ThemeGenerator()

        # Test with existing theme
        assert generator.theme_exists("dracula") is True
        assert generator.theme_exists("solarized") is True

        # Test with non-existing theme
        assert generator.theme_exists("nonexistent_theme") is False

    def test_list_themes(self):
        """Test theme listing."""
        generator = ThemeGenerator()

        themes = generator.list_themes()
        assert isinstance(themes, list)
        assert len(themes) > 0
        assert "dracula" in themes
        assert "solarized" in themes

    def test_generate_theme_from_data(self, tmp_path):
        """Test theme generation from data using temporary directory."""
        # Use temporary directory for test
        test_themes_dir = tmp_path / "test_themes"
        generator = ThemeGenerator(themes_dir=test_themes_dir)

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

        # Verify files were created in temporary directory
        theme_dir = test_themes_dir / "test_theme_data"
        assert theme_dir.exists()
        assert (theme_dir / "theme.yaml").exists()
        assert (theme_dir / "colorsystem.yaml").exists()
        assert (theme_dir / "mappings.yaml").exists()

    def test_generate_theme_existing_no_overwrite(self, tmp_path):
        """Test theme generation with existing theme and no overwrite."""
        # Use temporary directory for test
        test_themes_dir = tmp_path / "test_themes"
        generator = ThemeGenerator(themes_dir=test_themes_dir)

        # First create a theme
        theme_data = {"colorsystem": {}, "mappings": {}}
        generator.generate_theme_from_data(
            theme_name="test_existing_theme",
            theme_data=theme_data,
            overwrite=True,
        )

        # Try to create the same theme without overwrite
        with pytest.raises(ValueError):
            generator.generate_theme_from_data(
                theme_name="test_existing_theme",  # Existing theme
                theme_data={},
                overwrite=False,
            )

    def test_generate_theme_from_palette(self, tmp_path):
        """Test theme generation from palette using temporary directory."""
        # Use temporary directory for test
        test_themes_dir = tmp_path / "test_themes"
        generator = ThemeGenerator(themes_dir=test_themes_dir)

        files = generator.generate_theme_from_palette(
            theme_name="test_palette_theme",
            palette_name="TestPalette",
            start_hue=30,
            num_colors=8,
            target_delta_e=25,
            display_name="Test Palette Theme",
            description="A test theme generated from palette",
            author="Test Author",
            tags=["test", "palette"],
            overwrite=True,
        )

        assert isinstance(files, dict)
        assert "theme.yaml" in files
        assert "colorsystem.yaml" in files
        assert "mappings.yaml" in files

        # Verify files were created in temporary directory
        theme_dir = test_themes_dir / "test_palette_theme"
        assert theme_dir.exists()
        assert (theme_dir / "theme.yaml").exists()
        assert (theme_dir / "colorsystem.yaml").exists()
        assert (theme_dir / "mappings.yaml").exists()
