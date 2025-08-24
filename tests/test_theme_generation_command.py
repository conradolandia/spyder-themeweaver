"""
Tests for theme generation CLI command.
"""

import sys
from io import StringIO
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

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
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
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
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

                            mock_validate.assert_called_once()
                            # Check that syntax_colors was passed as string
                            call_kwargs = mock_validate.call_args[1]
                            assert call_kwargs["syntax_colors"] == "#FF8000"
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_with_syntax_colors_custom(self) -> None:
        """Test theme generation with custom syntax colors palette."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = [f"#FF{i:02X}00" for i in range(16)]  # 16 colors
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
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

                            mock_validate.assert_called_once()
                            # Check that syntax_colors was passed as list
                            call_kwargs = mock_validate.call_args[1]
                            assert isinstance(call_kwargs["syntax_colors"], list)
                            assert len(call_kwargs["syntax_colors"]) == 16
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

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
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

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
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
        """Test theme generation with analysis enabled."""
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

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class:
                mock_generator = Mock()
                mock_generator_class.return_value = mock_generator
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
                            "themeweaver.core.palette.create_palettes"
                        ) as mock_create_palettes:
                            mock_palettes = Mock()
                            mock_palettes.supported_variants = ["dark", "light"]
                            mock_palettes.get_palette.return_value = Mock()
                            mock_create_palettes.return_value = mock_palettes
                            with patch(
                                "themeweaver.cli.commands.theme_generation._logger"
                            ) as mock_logger:
                                cmd_generate(args)

                                mock_create_palettes.assert_called_once_with(
                                    "test_theme"
                                )
                                mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_generate_invalid_syntax_colors_count(self) -> None:
        """Test theme generation with invalid syntax colors count."""
        args = Mock()
        args.name = "test_theme"
        args.colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        args.syntax_colors = ["#FF0000", "#00FF00"]  # Invalid count (should be 1 or 16)
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False

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
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False

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
        args.display_name = None
        args.description = None
        args.author = "Test Author"
        args.tags = None
        args.overwrite = False
        args.analyze = False

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
