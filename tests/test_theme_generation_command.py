"""
Tests for theme generation CLI command.
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from themeweaver.cli.commands.theme_generation import cmd_generate


class TestThemeGenerationCommand:
    """Test theme generation command functionality."""

    def test_cmd_generate_basic_theme(self) -> None:
        """Test basic theme generation."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None
        args.syntax_colors_dark = None
        args.syntax_colors_light = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.themes_dir = Path.cwd() / "themes"
                mock_generator.theme_exists.return_value = False
                mock_generator.generate_theme_from_data.return_value = {
                    "theme.yaml": "/path/to/theme.yaml",
                    "colorsystem.yaml": "/path/to/colorsystem.yaml",
                    "mappings.yaml": "/path/to/mappings.yaml",
                }

                with patch(
                    "themeweaver.cli.commands.theme_generation.validate_input_colors"
                ) as mock_validate:
                    mock_validate.return_value = (True, "")
                    with patch(
                        "themeweaver.cli.commands.theme_generation.generate_theme_from_colors"
                    ) as mock_generate:
                        mock_generate.return_value = {"theme": "data"}
                        with patch(
                            "themeweaver.cli.commands.theme_generation._logger"
                        ) as mock_logger:
                            cmd_generate(args)

                            mock_generator.theme_exists.assert_called_once_with(
                                "test_theme"
                            )
                            mock_validate.assert_called_once()
                            mock_generate.assert_called_once()
                            mock_generator.generate_theme_from_data.assert_called_once()
                            mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_with_syntax_colors_single(self) -> None:
        """Test theme generation with single syntax color."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = ["#FF8000"]
        args.syntax_colors_dark = ["#FF8000"]
        args.syntax_colors_light = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.themes_dir = Path.cwd() / "themes"
                mock_generator.theme_exists.return_value = False
                mock_generator.generate_theme_from_data.return_value = {
                    "theme.yaml": "/path/to/theme.yaml"
                }

                with patch(
                    "themeweaver.cli.commands.theme_generation.validate_input_colors"
                ) as mock_validate:
                    mock_validate.return_value = (True, "")
                    with patch(
                        "themeweaver.cli.commands.theme_generation.generate_theme_from_colors"
                    ) as mock_generate:
                        mock_generate.return_value = {"theme": "data"}
                        with patch("themeweaver.cli.commands.theme_generation._logger"):
                            cmd_generate(args)

                            assert mock_validate.call_count >= 1
                            # Check that syntax_colors was passed as string
                            calls = mock_validate.call_args_list
                            syntax_call = next(
                                (c for c in calls if "syntax_colors" in (c[1] or {})),
                                None,
                            )
                            assert syntax_call is not None
                            assert syntax_call[1].get("syntax_colors") == "#FF8000"
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_with_syntax_colors_custom(self) -> None:
        """Test theme generation with custom syntax colors palette."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = [f"#FF{i:02X}00" for i in range(16)]  # 16 colors
        args.syntax_colors_dark = [f"#FF{i:02X}00" for i in range(16)]
        args.syntax_colors_light = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.themes_dir = Path.cwd() / "themes"
                mock_generator.theme_exists.return_value = False
                mock_generator.generate_theme_from_data.return_value = {
                    "theme.yaml": "/path/to/theme.yaml"
                }

                with patch(
                    "themeweaver.cli.commands.theme_generation.validate_input_colors"
                ) as mock_validate:
                    mock_validate.return_value = (True, "")
                    with patch(
                        "themeweaver.cli.commands.theme_generation.generate_theme_from_colors"
                    ) as mock_generate:
                        mock_generate.return_value = {"theme": "data"}
                        with patch("themeweaver.cli.commands.theme_generation._logger"):
                            cmd_generate(args)

                            assert mock_validate.call_count >= 1
                            # Check that syntax_colors was passed as list
                            calls = mock_validate.call_args_list
                            syntax_call = next(
                                (c for c in calls if "syntax_colors" in (c[1] or {})),
                                None,
                            )
                            assert syntax_call is not None
                            assert isinstance(syntax_call[1]["syntax_colors"], list)
                            assert len(syntax_call[1]["syntax_colors"]) == 16
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_with_metadata(self) -> None:
        """Test theme generation with metadata."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = None
        args.display_name = "Test Theme"
        args.description = "A test theme"
        args.author = "Test Author"
        args.tags = "test,example,theme"
        args.overwrite = False
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None
        args.syntax_colors_dark = None
        args.syntax_colors_light = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.themes_dir = Path.cwd() / "themes"
                mock_generator.theme_exists.return_value = False
                mock_generator.generate_theme_from_data.return_value = {
                    "theme.yaml": "/path/to/theme.yaml"
                }

                with patch(
                    "themeweaver.cli.commands.theme_generation.validate_input_colors"
                ) as mock_validate:
                    mock_validate.return_value = (True, "")
                    with patch(
                        "themeweaver.cli.commands.theme_generation.generate_theme_from_colors"
                    ) as mock_generate:
                        mock_generate.return_value = {"theme": "data"}
                        with patch("themeweaver.cli.commands.theme_generation._logger"):
                            cmd_generate(args)

                            mock_generator.generate_theme_from_data.assert_called_once()
                            call_args = (
                                mock_generator.generate_theme_from_data.call_args
                            )
                            assert call_args[1]["display_name"] == "Test Theme"
                            assert call_args[1]["description"] == "A test theme"
                            assert call_args[1]["author"] == "Test Author"
                            assert call_args[1]["tags"] == ["test", "example", "theme"]
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_with_overwrite(self) -> None:
        """Test theme generation with overwrite flag."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = True
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None
        args.syntax_colors_dark = None
        args.syntax_colors_light = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.themes_dir = Path.cwd() / "themes"
                mock_generator.theme_exists.return_value = True  # Theme exists
                mock_generator.generate_theme_from_data.return_value = {
                    "theme.yaml": "/path/to/theme.yaml"
                }

                with patch(
                    "themeweaver.cli.commands.theme_generation.validate_input_colors"
                ) as mock_validate:
                    mock_validate.return_value = (True, "")
                    with patch(
                        "themeweaver.cli.commands.theme_generation.generate_theme_from_colors"
                    ) as mock_generate:
                        mock_generate.return_value = {"theme": "data"}
                        with patch("themeweaver.cli.commands.theme_generation._logger"):
                            cmd_generate(args)

                            # Should proceed even though theme exists due to overwrite=True
                            mock_generator.generate_theme_from_data.assert_called_once()
                            call_args = (
                                mock_generator.generate_theme_from_data.call_args
                            )
                            assert call_args[1]["overwrite"] is True
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_with_analysis(self) -> None:
        """Test theme generation with analysis flag (theme generates successfully)."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = True
        args.from_yaml = None
        args.output_dir = None
        args.syntax_colors_dark = None
        args.syntax_colors_light = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.themes_dir = Path.cwd() / "themes"
                mock_generator.theme_exists.return_value = False
                mock_generator.generate_theme_from_data.return_value = {
                    "theme.yaml": "/path/to/theme.yaml"
                }

                with patch(
                    "themeweaver.cli.commands.theme_generation.validate_input_colors"
                ) as mock_validate:
                    mock_validate.return_value = (True, "")
                    with patch(
                        "themeweaver.cli.commands.theme_generation.generate_theme_from_colors"
                    ) as mock_generate:
                        mock_generate.return_value = {"theme": "data"}
                        with patch(
                            "themeweaver.cli.commands.theme_generation._logger"
                        ) as mock_logger:
                            cmd_generate(args)

                            mock_generator.generate_theme_from_data.assert_called_once()
                            mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_invalid_syntax_colors_count(self) -> None:
        """Test theme generation with invalid syntax colors count."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = ["#FF0000", "#00FF00"]  # Invalid count (should be 1 or 16)
        args.syntax_colors_dark = ["#FF0000", "#00FF00"]
        args.syntax_colors_light = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.theme_exists.return_value = False

                with pytest.raises(SystemExit):
                    cmd_generate(args)
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_theme_already_exists(self) -> None:
        """Test theme generation when theme already exists without overwrite."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None
        args.syntax_colors_dark = None
        args.syntax_colors_light = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.theme_exists.return_value = True  # Theme exists

                with pytest.raises(SystemExit):
                    cmd_generate(args)
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_missing_colors(self) -> None:
        """Test theme generation with missing colors argument."""
        args = Mock()
        args.name = "test_theme"
        args.colors = None  # Missing colors
        args.syntax_colors = None
        args.syntax_colors_dark = None
        args.syntax_colors_light = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.theme_exists.return_value = False

                with pytest.raises(SystemExit):
                    cmd_generate(args)
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_invalid_colors(self) -> None:
        """Test theme generation with invalid colors."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = None
        args.syntax_colors_dark = None
        args.syntax_colors_light = None
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False
        args.from_yaml = None
        args.output_dir = None

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
                mock_generator.theme_exists.return_value = False

                with patch(
                    "themeweaver.cli.commands.theme_generation.validate_input_colors"
                ) as mock_validate:
                    mock_validate.return_value = (False, "Invalid color format")

                    with pytest.raises(SystemExit):
                        cmd_generate(args)
        finally:
            sys.stdout = sys.__stdout__
