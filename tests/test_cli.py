"""
Tests for CLI functionality.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, patch

from themeweaver.cli.commands.theme_management import cmd_list
from themeweaver.cli.utils import list_themes, setup_logging, show_theme_info


class TestCLI:
    """Test CLI functionality."""

    def test_setup_logging(self) -> None:
        """Test logging setup."""
        setup_logging()
        # Should not raise any exceptions

    def test_list_themes(self) -> None:
        """Test theme listing."""
        themes = list_themes()
        assert isinstance(themes, list)
        assert len(themes) > 0
        # Should include known themes
        assert "dracula" in themes
        assert "solarized" in themes

    def test_list_themes_with_custom_dir(self, tmp_path: Path) -> None:
        """Test theme listing with custom directory."""
        # Create a mock theme directory
        theme_dir = tmp_path / "test_theme"
        theme_dir.mkdir()
        (theme_dir / "theme.yaml").touch()

        themes = list_themes(tmp_path)
        assert "test_theme" in themes

    @patch("themeweaver.cli.utils._logger")
    def test_show_theme_info(self, mock_logger: Mock) -> None:
        """Test theme info display."""
        show_theme_info("dracula")
        # Should call logger methods
        assert mock_logger.info.called

    @patch("themeweaver.cli.utils._logger")
    def test_show_theme_info_invalid(self, mock_logger: Mock) -> None:
        """Test theme info with invalid theme."""
        show_theme_info("nonexistent_theme")
        # Should log error
        assert mock_logger.error.called

    @patch("themeweaver.cli.commands.theme_management._logger")
    def test_cmd_list(self, mock_logger: Mock) -> None:
        """Test list command."""
        args = Mock()
        cmd_list(args)
        # Should call logger
        assert mock_logger.info.called


class TestCLICommands:
    """Test CLI commands via subprocess."""

    def test_cli_help(self) -> None:
        """Test CLI help output."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "ThemeWeaver" in result.stdout

    def test_cli_list(self) -> None:
        """Test CLI list command."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "list"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "Available themes" in output or "dracula" in output

    def test_cli_info(self) -> None:
        """Test CLI info command."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "info", "dracula"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "Theme:" in output or "dracula" in output

    def test_cli_main_module_execution(self) -> None:
        """Test CLI main module execution."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "ThemeWeaver" in result.stdout

    def test_cli_no_command_shows_help(self) -> None:
        """Test that CLI shows help when no command is specified."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout
        assert "Available commands" in result.stdout

    def test_cli_version_argument(self) -> None:
        """Test CLI version argument."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "--version"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "ThemeWeaver 1.0.0" in result.stdout

    def test_cli_interpolate_command_basic(self) -> None:
        """Test CLI interpolate command basic functionality."""
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

    def test_cli_interpolate_command_with_method(self) -> None:
        """Test CLI interpolate command with different methods."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "interpolate",
                "#FF0000",
                "#0000FF",
                "5",
                "--method",
                "cubic",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "#FF0000" in result.stdout
        assert "#0000FF" in result.stdout

    def test_cli_interpolate_command_with_exponent(self) -> None:
        """Test CLI interpolate command with exponential method and exponent."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "interpolate",
                "#FF0000",
                "#0000FF",
                "4",
                "--method",
                "exponential",
                "--exponent",
                "3",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "#FF0000" in result.stdout
        assert "#0000FF" in result.stdout

    def test_cli_interpolate_command_with_output_format(self) -> None:
        """Test CLI interpolate command with different output formats."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "interpolate",
                "#FF0000",
                "#0000FF",
                "3",
                "--output",
                "json",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        # The output is JSON with a "palette" structure
        assert (
            '"palette"' in result.stdout
            or '"colors"' in result.stdout
            or "[" in result.stdout
        )

    def test_cli_interpolate_command_with_analysis(self) -> None:
        """Test CLI interpolate command with analysis flag."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "interpolate",
                "#FF0000",
                "#0000FF",
                "3",
                "--analyze",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        # Should show some analysis output
        assert len(result.stdout) > 0

    def test_cli_interpolate_command_with_validation(self) -> None:
        """Test CLI interpolate command with validation flag."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "themeweaver.cli",
                "interpolate",
                "#FF0000",
                "#0000FF",
                "3",
                "--validate",
            ],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        # Should show validation output
        assert len(result.stdout) > 0
