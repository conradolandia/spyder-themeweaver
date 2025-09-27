"""
Tests for CLI scripts.
"""

import subprocess
import sys
from pathlib import Path


class TestCLIScripts:
    """Test CLI scripts functionality."""

    def test_interpolate_colors_help(self) -> None:
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

    def test_interpolate_colors_basic(self) -> None:
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

    def test_generate_palette_help(self) -> None:
        """Test generate_palette help."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "palette", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "Number of colors in palettes" in result.stdout

    def test_palette_syntax_method_help(self) -> None:
        """Test that syntax method is mentioned in palette help."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "palette", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "syntax" in result.stdout
        assert "syntax highlighting optimized" in result.stdout

    def test_palette_syntax_method_basic(self) -> None:
        """Test palette syntax method basic functionality."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "palette",
                "--method",
                "syntax",
                "--from-color",
                "#ff6b6b",
                "--output-format",
                "list",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "Syntax colors:" in result.stdout
        assert "B0:" in result.stdout
        assert "B150:" in result.stdout

    def test_palette_syntax_method_json(self) -> None:
        """Test palette syntax method with JSON output."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "palette",
                "--method",
                "syntax",
                "--from-color",
                "#4a9eff",
                "--output-format",
                "json",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert '"Syntax":' in result.stdout
        assert '"B0":' in result.stdout
        assert '"B150":' in result.stdout

    def test_palette_syntax_method_class(self) -> None:
        """Test palette syntax method with class output."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "palette",
                "--method",
                "syntax",
                "--from-color",
                "#51cf66",
                "--output-format",
                "class",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "class Syntax:" in result.stdout
        assert "Syntax highlighting colors." in result.stdout
        assert "B0 = '" in result.stdout
        assert "B150 = '" in result.stdout

    def test_palette_syntax_method_no_from_color(self) -> None:
        """Test palette syntax method without --from-color (should fail)."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "palette",
                "--method",
                "syntax",
                "--output-format",
                "list",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        # The command should print error to stderr
        assert "requires --from-color argument" in result.stderr

    def test_palette_uniform_method_still_works(self) -> None:
        """Test that uniform method still works after removing deprecated flag."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "palette",
                "--method",
                "uniform",
                "--num-colors",
                "8",
                "--output-format",
                "list",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "GroupDark colors:" in result.stdout
        assert "GroupLight colors:" in result.stdout
