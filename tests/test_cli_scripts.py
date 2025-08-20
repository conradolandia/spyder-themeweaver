"""
Tests for CLI scripts.
"""

import subprocess
import sys
from pathlib import Path

import pytest


class TestCLIScripts:
    """Test CLI scripts functionality."""

    def test_analyze_palette_help(self):
        """Test analyze_palette help."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.color_utils.analyze_palette", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "Analyze any color palette" in result.stdout

    def test_analyze_palette_solarized(self):
        """Test analyze_palette with solarized."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.color_utils.analyze_palette",
                "solarized",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "solarized" in result.stdout.lower()

    def test_interpolate_colors_help(self):
        """Test interpolate_colors help."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.color_utils.interpolate_colors",
                "--help",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "Interpolate between two hex colors" in result.stdout

    def test_interpolate_colors_basic(self):
        """Test interpolate_colors basic functionality."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.color_utils.interpolate_colors",
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

    def test_generate_groups_help(self):
        """Test generate_groups help."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.color_utils.generate_groups", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "Generate group-style color palettes" in result.stdout

    def test_generate_groups_module_import(self):
        """Test that generate_groups module can be imported."""
        # This tests that the module can be imported without errors
        try:
            import themeweaver.color_utils.generate_groups

            _ = themeweaver.color_utils.generate_groups
            assert True
        except ImportError:
            pytest.fail("generate_groups module should be importable")
