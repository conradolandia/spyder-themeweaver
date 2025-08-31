"""
Tests for ThemePackager functionality.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from themeweaver.core.theme_packager import ThemePackager


class TestThemePackager:
    """Test ThemePackager functionality."""

    def setup_method(self) -> None:
        """Setup test environment with temporary directories."""
        self.temp_dir = tempfile.mkdtemp()
        self.build_dir = Path(self.temp_dir) / "build"
        self.packages_dir = Path(self.temp_dir) / "packages"
        self.themes_dir = Path(self.temp_dir) / "themes"

        # Create test directories
        self.build_dir.mkdir(parents=True)
        self.packages_dir.mkdir(parents=True)
        self.themes_dir.mkdir(parents=True)

    def teardown_method(self) -> None:
        """Cleanup test environment."""
        if hasattr(self, "temp_dir") and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_packager_initialization(self) -> None:
        """Test that packager initializes correctly."""
        packager = ThemePackager(self.packages_dir)
        assert packager.output_dir == self.packages_dir
        assert packager.build_dir.name == "build"
        assert packager.themes_dir.name == "themes"

    def test_package_theme_not_found(self) -> None:
        """Test packaging a theme that doesn't exist in build directory."""
        packager = ThemePackager(self.packages_dir)

        with pytest.raises(FileNotFoundError, match="Theme 'nonexistent' not found"):
            packager.package_theme("nonexistent")

    def test_package_theme_success(self) -> None:
        """Test successful packaging of a theme."""
        # Create mock theme in build directory
        theme_name = "test_theme"
        theme_build_dir = self.build_dir / theme_name
        theme_build_dir.mkdir()

        # Create some mock files
        (theme_build_dir / "colorsystem.py").write_text("# Test colorsystem")
        (theme_build_dir / "palette.py").write_text("# Test palette")
        (theme_build_dir / "dark").mkdir()
        (theme_build_dir / "dark" / "darkstyle.qss").write_text("/* Test QSS */")

        # Create mock theme.yaml
        theme_yaml_dir = self.themes_dir / theme_name
        theme_yaml_dir.mkdir()
        theme_yaml = theme_yaml_dir / "theme.yaml"
        theme_yaml.write_text("""
name: test_theme
display_name: Test Theme
description: A test theme
author: Test Author
version: 1.0.0
license: MIT
tags: [test, dark]
variants:
  dark: true
  light: false
""")

        # Create packager and manually set the paths
        packager = ThemePackager(self.packages_dir)
        packager.workspace_root = self.temp_dir
        packager.build_dir = self.build_dir
        packager.themes_dir = self.themes_dir

        package_path = packager.package_theme(theme_name)

        assert package_path.exists()
        assert package_path.name == f"{theme_name}-1.0.0.zip"
        assert package_path.parent == self.packages_dir

    def test_package_all_themes_empty_build(self) -> None:
        """Test packaging all themes when build directory is empty."""
        packager = ThemePackager(self.packages_dir)
        packager.workspace_root = self.temp_dir
        packager.build_dir = self.build_dir
        packager.themes_dir = self.themes_dir

        packages = packager.package_all_themes()
        assert packages == {}

    def test_package_all_themes_with_themes(self) -> None:
        """Test packaging all themes when themes exist."""
        # Create mock themes
        theme_names = ["theme1", "theme2"]
        for theme_name in theme_names:
            theme_build_dir = self.build_dir / theme_name
            theme_build_dir.mkdir()
            (theme_build_dir / "colorsystem.py").write_text("# Test")

            theme_yaml_dir = self.themes_dir / theme_name
            theme_yaml_dir.mkdir()
            theme_yaml = theme_yaml_dir / "theme.yaml"
            theme_yaml.write_text(f"""
name: {theme_name}
display_name: {theme_name.title()}
version: 1.0.0
variants:
  dark: true
""")

        packager = ThemePackager(self.packages_dir)
        packager.workspace_root = self.temp_dir
        packager.build_dir = self.build_dir
        packager.themes_dir = self.themes_dir

        packages = packager.package_all_themes()

        assert len(packages) == 2
        for theme_name in theme_names:
            assert theme_name in packages
            assert packages[theme_name].exists()

    def test_package_theme_tar_gz_format(self) -> None:
        """Test packaging theme in TAR.GZ format."""
        # Create mock theme
        theme_name = "test_theme"
        theme_build_dir = self.build_dir / theme_name
        theme_build_dir.mkdir()
        (theme_build_dir / "colorsystem.py").write_text("# Test")

        theme_yaml_dir = self.themes_dir / theme_name
        theme_yaml_dir.mkdir()
        theme_yaml = theme_yaml_dir / "theme.yaml"
        theme_yaml.write_text("""
name: test_theme
version: 1.0.0
variants:
  dark: true
""")

        packager = ThemePackager(self.packages_dir)
        packager.workspace_root = self.temp_dir
        packager.build_dir = self.build_dir
        packager.themes_dir = self.themes_dir

        package_path = packager.package_theme(theme_name, "tar.gz")

        assert package_path.exists()
        assert package_path.name == f"{theme_name}-1.0.0.tar.gz"

    def test_package_theme_invalid_format(self) -> None:
        """Test packaging with invalid format."""
        # Create mock theme
        theme_name = "test_theme"
        theme_build_dir = self.build_dir / theme_name
        theme_build_dir.mkdir()
        (theme_build_dir / "colorsystem.py").write_text("# Test")

        theme_yaml_dir = self.themes_dir / theme_name
        theme_yaml_dir.mkdir()
        theme_yaml = theme_yaml_dir / "theme.yaml"
        theme_yaml.write_text("""
name: test_theme
version: 1.0.0
variants:
  dark: true
""")

        packager = ThemePackager(self.packages_dir)
        packager.workspace_root = self.temp_dir
        packager.build_dir = self.build_dir
        packager.themes_dir = self.themes_dir

        with pytest.raises(ValueError, match="Unsupported format: invalid"):
            packager.package_theme(theme_name, "invalid")

    def test_package_theme_missing_metadata(self) -> None:
        """Test packaging theme with missing metadata file."""
        # Create mock theme without theme.yaml
        theme_name = "test_theme"
        theme_build_dir = self.build_dir / theme_name
        theme_build_dir.mkdir()
        (theme_build_dir / "colorsystem.py").write_text("# Test")

        packager = ThemePackager(self.packages_dir)
        packager.workspace_root = self.temp_dir
        packager.build_dir = self.build_dir
        packager.themes_dir = self.themes_dir

        package_path = packager.package_theme(theme_name)

        # Should still work with fallback metadata
        assert package_path.exists()
        assert package_path.name == f"{theme_name}-1.0.0.zip"
