"""
Tests for CLI functionality.
"""

import subprocess
import sys
from importlib.metadata import version as pkg_version
from pathlib import Path
from unittest.mock import Mock, patch

from cli_invoke import REPO_ROOT, invoke_cli

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
        args.theme_dir = None
        cmd_list(args)
        # Should call logger
        assert mock_logger.info.called


class TestCLICommands:
    """Test CLI commands in-process (fast); see subprocess smoke test below."""

    def test_cli_help(self) -> None:
        """Test CLI help output."""
        r = invoke_cli("--help")
        assert r.returncode == 0
        assert "ThemeWeaver" in r.stdout

    def test_cli_list(self) -> None:
        """Test CLI list command."""
        r = invoke_cli("list")
        assert r.returncode == 0
        assert "Available themes" in r.output or "dracula" in r.output

    def test_cli_info(self) -> None:
        """Test CLI info command."""
        r = invoke_cli("info", "dracula")
        assert r.returncode == 0
        assert "Theme:" in r.output or "dracula" in r.output

    def test_cli_no_command_shows_help(self) -> None:
        """Test that CLI shows help when no command is specified."""
        r = invoke_cli()
        assert r.returncode == 0
        assert "usage:" in r.stdout
        assert "Available commands" in r.stdout

    def test_cli_version_argument(self) -> None:
        """Test CLI version argument."""
        r = invoke_cli("--version")
        assert r.returncode == 0
        assert f"ThemeWeaver {pkg_version('themeweaver')}" in r.stdout

    def test_cli_interpolate_command_basic(self) -> None:
        """Test CLI interpolate command basic functionality."""
        r = invoke_cli("interpolate", "#FF0000", "#0000FF", "3")
        assert r.returncode == 0
        assert "#FF0000" in r.stdout
        assert "#0000FF" in r.stdout

    def test_cli_interpolate_command_with_method(self) -> None:
        """Test CLI interpolate command with different methods."""
        r = invoke_cli(
            "interpolate",
            "#FF0000",
            "#0000FF",
            "5",
            "--method",
            "cubic",
        )
        assert r.returncode == 0
        assert "#FF0000" in r.stdout
        assert "#0000FF" in r.stdout

    def test_cli_interpolate_command_with_exponent(self) -> None:
        """Test CLI interpolate command with exponential method and exponent."""
        r = invoke_cli(
            "interpolate",
            "#FF0000",
            "#0000FF",
            "4",
            "--method",
            "exponential",
            "--exponent",
            "3",
        )
        assert r.returncode == 0
        assert "#FF0000" in r.stdout
        assert "#0000FF" in r.stdout

    def test_cli_interpolate_command_with_output_format(self) -> None:
        """Test CLI interpolate command with different output formats."""
        r = invoke_cli(
            "interpolate",
            "#FF0000",
            "#0000FF",
            "3",
            "--output",
            "json",
        )
        assert r.returncode == 0
        assert '"palette"' in r.stdout or '"colors"' in r.stdout or "[" in r.stdout

    def test_cli_interpolate_command_with_analysis(self) -> None:
        """Test CLI interpolate command with analysis flag."""
        r = invoke_cli(
            "interpolate",
            "#FF0000",
            "#0000FF",
            "3",
            "--analyze",
        )
        assert r.returncode == 0
        assert len(r.stdout) > 0

    def test_cli_interpolate_command_with_validation(self) -> None:
        """Test CLI interpolate command with validation flag."""
        r = invoke_cli(
            "interpolate",
            "#FF0000",
            "#0000FF",
            "3",
            "--validate",
        )
        assert r.returncode == 0
        assert len(r.stdout) > 0


class TestCLIPackageEntrypoint:
    """Single subprocess check that ``python -m themeweaver.cli`` works."""

    def test_python_m_cli_help_smoke(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        assert result.returncode == 0
        assert "ThemeWeaver" in result.stdout
