"""
Tests for CLI scripts (palette, interpolate help paths).
"""

from cli_invoke import invoke_cli


class TestCLIScripts:
    """Exercise CLI subcommands in-process."""

    def test_interpolate_colors_help(self) -> None:
        """Test interpolate help."""
        r = invoke_cli("interpolate", "--help")
        assert r.returncode == 0
        assert "Starting hex color" in r.stdout

    def test_interpolate_colors_basic(self) -> None:
        """Test interpolate basic run."""
        r = invoke_cli("interpolate", "#FF0000", "#0000FF", "3")
        assert r.returncode == 0
        assert "#FF0000" in r.stdout
        assert "#0000FF" in r.stdout

    def test_generate_palette_help(self) -> None:
        """Test palette help."""
        r = invoke_cli("palette", "--help")
        assert r.returncode == 0
        assert "Number of colors in palettes" in r.stdout

    def test_palette_syntax_method_help(self) -> None:
        """Test that syntax method is mentioned in palette help."""
        r = invoke_cli("palette", "--help")
        assert r.returncode == 0
        assert "syntax" in r.stdout
        assert "syntax highlighting optimized" in r.stdout

    def test_palette_syntax_method_basic(self) -> None:
        """Test palette syntax method (list output)."""
        r = invoke_cli(
            "palette",
            "--method",
            "syntax",
            "--from-color",
            "#ff6b6b",
            "--output-format",
            "list",
        )
        assert r.returncode == 0
        assert "Syntax colors:" in r.stdout
        assert "B10:" in r.stdout
        assert "B170:" in r.stdout

    def test_palette_syntax_method_json(self) -> None:
        """Test palette syntax method with JSON output."""
        r = invoke_cli(
            "palette",
            "--method",
            "syntax",
            "--from-color",
            "#4a9eff",
            "--output-format",
            "json",
        )
        assert r.returncode == 0
        assert '"Syntax":' in r.stdout
        assert '"B10":' in r.stdout
        assert '"B170":' in r.stdout

    def test_palette_syntax_method_class(self) -> None:
        """Test palette syntax method with class output."""
        r = invoke_cli(
            "palette",
            "--method",
            "syntax",
            "--from-color",
            "#51cf66",
            "--output-format",
            "class",
        )
        assert r.returncode == 0
        assert "class Syntax:" in r.stdout
        assert "Syntax highlighting colors." in r.stdout
        assert "B10 = '" in r.stdout
        assert "B170 = '" in r.stdout

    def test_palette_syntax_method_no_from_color(self) -> None:
        """Syntax method without --from-color should log an error."""
        r = invoke_cli(
            "palette",
            "--method",
            "syntax",
            "--output-format",
            "list",
        )
        assert "requires --from-color argument" in r.stderr

    def test_palette_uniform_method_still_works(self) -> None:
        """Uniform palette method (list output)."""
        r = invoke_cli(
            "palette",
            "--method",
            "uniform",
            "--num-colors",
            "8",
            "--output-format",
            "list",
        )
        assert r.returncode == 0
        assert "GroupDark colors:" in r.stdout
        assert "GroupLight colors:" in r.stdout
