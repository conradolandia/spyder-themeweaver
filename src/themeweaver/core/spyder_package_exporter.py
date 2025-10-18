"""
Spyder package exporter module for ThemeWeaver.

Exports all themes into a single Python package structure suitable
for installation as a Spyder theme package.
"""

import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

_logger = logging.getLogger(__name__)


class SpyderPackageExporter:
    """Exports multiple themes into a single Spyder-compatible Python package."""

    def __init__(
        self,
        build_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None,
        package_name: str = "spyder_themes",
    ) -> None:
        """Initialize the package exporter.

        Args:
            build_dir: Directory containing built themes
            output_dir: Directory to create package in
            package_name: Name of the Python package
        """
        self.workspace_root = Path(__file__).parent.parent.parent.parent
        self.build_dir = build_dir or self.workspace_root / "build"
        self.output_dir = output_dir or self.workspace_root / "dist"
        self.package_name = package_name

    def create_package(
        self,
        theme_names: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        with_pyproject: bool = True,
        validate: bool = True,
    ) -> Path:
        """Create a complete Spyder theme package.

        Args:
            theme_names: List of themes to include (None = all)
            metadata: Package metadata
            with_pyproject: Generate pyproject.toml
            validate: Validate structure before packaging

        Returns:
            Path to created package directory
        """
        # Determine themes to include
        if theme_names is None:
            theme_names = self._discover_themes()

        _logger.info(
            "Creating package '%s' with %d themes", self.package_name, len(theme_names)
        )

        # Create package directory structure
        package_dir = self.output_dir / self.package_name
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir(parents=True)

        # Create the actual Python package directory inside the package directory
        python_package_dir = package_dir / self.package_name
        python_package_dir.mkdir(parents=True)

        # Validate and copy each theme
        valid_themes = []
        for theme_name in theme_names:
            theme_src = self.build_dir / theme_name

            if validate and not self._validate_theme(theme_src):
                _logger.warning("Skipping invalid theme: %s", theme_name)
                continue

            theme_dst = python_package_dir / theme_name
            shutil.copytree(theme_src, theme_dst)
            valid_themes.append(theme_name)
            _logger.info("  • Added theme: %s", theme_name)

        # Generate package __init__.py inside the Python package directory
        self._generate_root_init(python_package_dir, valid_themes, metadata)

        # Generate pyproject.toml if requested (in the outer package directory)
        if with_pyproject:
            self._generate_pyproject(package_dir, metadata)

        _logger.info("✅ Package created: %s", package_dir)
        return package_dir

    def _discover_themes(self) -> List[str]:
        """Discover all themes in build directory."""
        themes = []
        for item in self.build_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                # Check if it has required files
                if (item / "colorsystem.py").exists() and (
                    item / "palette.py"
                ).exists():
                    themes.append(item.name)
        return sorted(themes)

    def _validate_theme(self, theme_path: Path) -> bool:
        """Validate theme has required structure."""
        required_files = ["__init__.py", "colorsystem.py", "palette.py"]

        for filename in required_files:
            if not (theme_path / filename).exists():
                _logger.error("Missing %s in %s", filename, theme_path.name)
                return False

        # Check at least one variant exists
        has_dark = (theme_path / "dark").exists()
        has_light = (theme_path / "light").exists()

        if not (has_dark or has_light):
            _logger.error("No dark/ or light/ directory in %s", theme_path.name)
            return False

        return True

    def _generate_root_init(
        self,
        package_dir: Path,
        theme_names: List[str],
        metadata: Optional[Dict[str, Any]],
    ) -> None:
        """Generate root __init__.py for package."""
        metadata = metadata or {}

        content = f'''# -*- coding: utf-8 -*-
"""
{metadata.get("display_name", "Spyder Theme Package")}

{metadata.get("description", "Collection of themes for Spyder IDE")}

Author: {metadata.get("author", "ThemeWeaver")}
Version: {metadata.get("version", "1.0.0")}
"""

import importlib

# List of available themes
THEMES = {theme_names!r}

def get_theme_module(theme_name):
    """Get theme module by name.

    Args:
        theme_name: Name of the theme to load

    Returns:
        Theme module with THEME_ID and palette classes

    Raises:
        ValueError: If theme not found
    """
    if theme_name not in THEMES:
        raise ValueError(f"Theme '{{theme_name}}' not found. Available: {{THEMES}}")
    return importlib.import_module(f'.{{theme_name}}', package=__name__)

__all__ = ['THEMES', 'get_theme_module']
'''

        init_path = package_dir / "__init__.py"
        init_path.write_text(content, encoding="utf-8")
        _logger.info("  • Generated: __init__.py")

    def _generate_pyproject(
        self,
        package_dir: Path,
        metadata: Optional[Dict[str, Any]],
    ) -> None:
        """Generate pyproject.toml for pip installation."""
        metadata = metadata or {}

        content = f'''[project]
name = "{self.package_name}"
version = "{metadata.get("version", "1.0.0")}"
description = "{metadata.get("description", "Spyder IDE theme package")}"
authors = [
    {{name = "{metadata.get("author", "ThemeWeaver")}"}}
]
license = "{metadata.get("license", "MIT")}"
requires-python = ">=3.8"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: User Interfaces",
    "Programming Language :: Python :: 3",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["{self.package_name}*"]

[tool.setuptools.package-data]
"*" = ["**/*.qss", "**/*.qrc", "**/*.py", "**/*.png", "**/*.svg"]
'''

        pyproject_path = package_dir / "pyproject.toml"
        pyproject_path.write_text(content, encoding="utf-8")
        _logger.info("  • Generated: pyproject.toml")
