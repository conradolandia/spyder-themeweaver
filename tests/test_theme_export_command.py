"""
Tests for theme export CLI command.
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

from themeweaver.cli.commands.theme_export import cmd_export


class TestThemeExportCommand:
    """Test theme export command functionality."""

    def test_cmd_export_single_theme(self) -> None:
        """Test exporting a single theme."""
        args = Mock()
        args.all = False
        args.theme = "dracula"
        args.variants = "dark,light"
        args.output = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_theme.return_value = {
                    "dark": "/path/to/dracula-dark.qss",
                    "light": "/path/to/dracula-light.qss",
                }

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(None)
                    mock_exporter.export_theme.assert_called_once_with(
                        "dracula", ["dark", "light"]
                    )
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_export_single_theme_no_variants(self) -> None:
        """Test exporting a single theme without specifying variants."""
        args = Mock()
        args.all = False
        args.theme = "solarized"
        args.variants = None
        args.output = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_theme.return_value = {
                    "dark": "/path/to/solarized-dark.qss",
                    "light": "/path/to/solarized-light.qss",
                }

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(None)
                    mock_exporter.export_theme.assert_called_once_with(
                        "solarized", None
                    )
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_export_single_theme_with_output_dir(self) -> None:
        """Test exporting a single theme with custom output directory."""
        args = Mock()
        args.all = False
        args.theme = "gruvbox"
        args.variants = "dark"
        args.output = "/custom/output"

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_theme.return_value = {
                    "dark": "/custom/output/gruvbox-dark.qss"
                }

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(Path("/custom/output"))
                    mock_exporter.export_theme.assert_called_once_with(
                        "gruvbox", ["dark"]
                    )
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_export_all_themes(self) -> None:
        """Test exporting all themes."""
        args = Mock()
        args.all = True
        args.theme = None
        args.variants = None
        args.output = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_all_themes.return_value = {
                    "dracula": {
                        "dark": "/path/to/dracula-dark.qss",
                        "light": "/path/to/dracula-light.qss",
                    },
                    "solarized": {
                        "dark": "/path/to/solarized-dark.qss",
                        "light": "/path/to/solarized-light.qss",
                    },
                    "gruvbox": {"dark": "/path/to/gruvbox-dark.qss"},
                }

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(None)
                    mock_exporter.export_all_themes.assert_called_once()
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_export_all_themes_with_output_dir(self) -> None:
        """Test exporting all themes with custom output directory."""
        args = Mock()
        args.all = True
        args.theme = None
        args.variants = None
        args.output = "/custom/build"

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_all_themes.return_value = {
                    "dracula": {"dark": "/custom/build/dracula-dark.qss"},
                    "solarized": {"light": "/custom/build/solarized-light.qss"},
                }

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(Path("/custom/build"))
                    mock_exporter.export_all_themes.assert_called_once()
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_export_single_theme_single_variant(self) -> None:
        """Test exporting a single theme with single variant."""
        args = Mock()
        args.all = False
        args.theme = "monokai"
        args.variants = "dark"
        args.output = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_theme.return_value = {
                    "dark": "/path/to/monokai-dark.qss"
                }

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(None)
                    mock_exporter.export_theme.assert_called_once_with(
                        "monokai", ["dark"]
                    )
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_export_single_theme_multiple_variants(self) -> None:
        """Test exporting a single theme with multiple variants."""
        args = Mock()
        args.all = False
        args.theme = "catppuccin-mocha"
        args.variants = "dark,light,auto"
        args.output = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_theme.return_value = {
                    "dark": "/path/to/catppuccin-mocha-dark.qss",
                    "light": "/path/to/catppuccin-mocha-light.qss",
                    "auto": "/path/to/catppuccin-mocha-auto.qss",
                }

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(None)
                    mock_exporter.export_theme.assert_called_once_with(
                        "catppuccin-mocha", ["dark", "light", "auto"]
                    )
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_export_all_themes_empty_result(self) -> None:
        """Test exporting all themes with empty result."""
        args = Mock()
        args.all = True
        args.theme = None
        args.variants = None
        args.output = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_all_themes.return_value = {}

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(None)
                    mock_exporter.export_all_themes.assert_called_once()
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_export_single_theme_empty_result(self) -> None:
        """Test exporting a single theme with empty result."""
        args = Mock()
        args.all = False
        args.theme = "nonexistent"
        args.variants = None
        args.output = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_export.ThemeExporter"
            ) as mock_exporter_class:
                mock_exporter = Mock()
                mock_exporter_class.return_value = mock_exporter
                mock_exporter.export_theme.return_value = {}

                with patch(
                    "themeweaver.cli.commands.theme_export._logger"
                ) as mock_logger:
                    cmd_export(args)

                    mock_exporter_class.assert_called_once_with(None)
                    mock_exporter.export_theme.assert_called_once_with(
                        "nonexistent", None
                    )
                    mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__
