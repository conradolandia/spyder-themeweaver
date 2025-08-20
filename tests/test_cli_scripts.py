"""
Tests for CLI scripts.
"""

import subprocess
import sys
from pathlib import Path

import pytest


class TestCLIScripts:
    """Test CLI scripts functionality."""

    def test_interpolate_colors_help(self):
        """Test interpolate_colors help."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "interpolate",
                "--help",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "Starting hex color" in result.stdout

    def test_interpolate_colors_basic(self):
        """Test interpolate_colors basic functionality."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "interpolate",
                "#FF0000",
                "#0000FF",
                "3",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "#FF0000" in result.stdout
        assert "#0000FF" in result.stdout

    def test_generate_palette_help(self):
        """Test generate_palette help."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "palette", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "Number of colors in palettes" in result.stdout

    def test_generate_groups_module_import(self):
        """Test that groups functionality can be imported."""
        # This tests that the groups functionality can be imported without errors
        try:
            from themeweaver.color_utils.color_generation import generate_theme_colors

            if generate_theme_colors:
                assert True
            else:
                pytest.fail("groups functionality should be importable")
        except ImportError:
            pytest.fail("groups functionality should be importable")
