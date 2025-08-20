"""
Tests for CLI functionality.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from themeweaver.cli.commands.theme_management import cmd_list
from themeweaver.cli.utils import list_themes, setup_logging, show_theme_info


class TestCLI:
    """Test CLI functionality."""

    def test_setup_logging(self):
        """Test logging setup."""
        setup_logging()
        # Should not raise any exceptions

    def test_list_themes(self):
        """Test theme listing."""
        themes = list_themes()
        assert isinstance(themes, list)
        assert len(themes) > 0
        # Should include known themes
        assert "dracula" in themes
        assert "solarized" in themes

    def test_list_themes_with_custom_dir(self, tmp_path):
        """Test theme listing with custom directory."""
        # Create a mock theme directory
        theme_dir = tmp_path / "test_theme"
        theme_dir.mkdir()
        (theme_dir / "theme.yaml").touch()

        themes = list_themes(tmp_path)
        assert "test_theme" in themes

    @patch("themeweaver.cli.utils._logger")
    def test_show_theme_info(self, mock_logger):
        """Test theme info display."""
        show_theme_info("dracula")
        # Should call logger methods
        assert mock_logger.info.called

    @patch("themeweaver.cli.utils._logger")
    def test_show_theme_info_invalid(self, mock_logger):
        """Test theme info with invalid theme."""
        show_theme_info("nonexistent_theme")
        # Should log error
        assert mock_logger.error.called

    @patch("themeweaver.cli.commands.theme_management._logger")
    def test_cmd_list(self, mock_logger):
        """Test list command."""
        cmd_list(None)
        # Should call logger
        assert mock_logger.info.called


class TestCLICommands:
    """Test CLI commands via subprocess."""

    def test_cli_help(self):
        """Test CLI help output."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        assert "ThemeWeaver" in result.stdout

    def test_cli_list(self):
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

    def test_cli_info(self):
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

    def test_cli_validate(self):
        """Test CLI validate command."""
        result = subprocess.run(
            [sys.executable, "-m", "themeweaver.cli", "validate", "dracula"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "Valid" in output or "dracula" in output
