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


class TestThemeGenerationYamlAndHelpers:
    def test_cmd_generate_dispatches_to_yaml_path(self) -> None:
        args = Mock()
        args.from_yaml = "/tmp/theme.yaml"
        args.output_dir = "/tmp/themes-out"

        with (
            patch(
                "themeweaver.cli.commands.theme_generation.ThemeGenerator"
            ) as mock_generator_class,
            patch(
                "themeweaver.cli.commands.theme_generation._generate_from_yaml"
            ) as mock_yaml,
        ):
            mock_generator = Mock()
            mock_generator_class.return_value = mock_generator
            cmd_generate(args)

        mock_generator_class.assert_called_once_with(themes_dir="/tmp/themes-out")
        mock_yaml.assert_called_once_with(args, mock_generator)

    def test_generate_from_yaml_file_not_found(self) -> None:
        from themeweaver.cli.commands.theme_generation import _generate_from_yaml

        args = Mock()
        args.from_yaml = "/path/does/not/exist.yaml"
        args.name = "x"

        with pytest.raises(FileNotFoundError):
            _generate_from_yaml(args, Mock())

    def test_generate_from_yaml_success_and_contrast_toggle(
        self, tmp_path: Path
    ) -> None:
        from themeweaver.cli.commands.theme_generation import _generate_from_yaml

        yaml_file = tmp_path / "theme.yaml"
        yaml_file.write_text("name: sample", encoding="utf-8")

        args = Mock()
        args.from_yaml = str(yaml_file)
        args.name = "cli-name"
        args.output_dir = str(tmp_path / "out")
        args.overwrite = True
        args.validate_contrast = False

        generator = Mock()
        generator.themes_dir = tmp_path / "themes"
        generator.theme_exists.return_value = True
        generator.generate_theme_from_data.return_value = {"theme.yaml": "ok"}

        parsed = {
            "name": "yaml-name",
            "colors": [
                "#111111",
                "#222222",
                "#333333",
                "#444444",
                "#555555",
                "#666666",
            ],
            "variants": ["dark"],
            "author": "A",
            "overwrite": False,
        }

        with (
            patch(
                "themeweaver.cli.commands.theme_generation.load_theme_from_yaml",
                return_value={"raw": "data"},
            ),
            patch(
                "themeweaver.cli.commands.theme_generation.parse_theme_definition",
                return_value=parsed,
            ),
            patch(
                "themeweaver.cli.commands.theme_generation.validate_input_colors",
                return_value=(True, ""),
            ),
            patch(
                "themeweaver.cli.commands.theme_generation.generate_theme_from_colors",
                return_value={"k": "v"},
            ),
            patch(
                "themeweaver.cli.commands.theme_generation._run_contrast_validation"
            ) as mock_contrast,
        ):
            _generate_from_yaml(args, generator)

        generator.generate_theme_from_data.assert_called_once()
        assert mock_contrast.call_count == 0

    def test_generate_from_yaml_maps_parse_errors(self, tmp_path: Path) -> None:
        from themeweaver.cli.commands.theme_generation import _generate_from_yaml

        yaml_file = tmp_path / "theme.yaml"
        yaml_file.write_text("name: sample", encoding="utf-8")
        args = Mock()
        args.from_yaml = str(yaml_file)
        args.name = "x"
        args.overwrite = False

        with patch(
            "themeweaver.cli.commands.theme_generation.load_theme_from_yaml",
            side_effect=ValueError("bad schema"),
        ):
            with pytest.raises(SystemExit):
                _generate_from_yaml(args, Mock())

    def test_run_contrast_validation_logs_failed_rules_and_exceptions(
        self, tmp_path: Path
    ) -> None:
        from themeweaver.cli.commands.theme_generation import _run_contrast_validation

        failed_rule = Mock()
        failed_rule.passed = False
        failed_rule.rule_id = "r1"
        failed_rule.message = "too low"
        failed_rule.suggestion = "increase contrast"

        ok_result = Mock()
        ok_result.all_passed = True
        ok_result.results = [Mock()]
        bad_result = Mock()
        bad_result.all_passed = False
        bad_result.failed_count = 1
        bad_result.passed_count = 2
        bad_result.results = [failed_rule]

        with (
            patch(
                "themeweaver.cli.commands.theme_generation.validate_theme",
                side_effect=[ok_result, bad_result, ValueError("missing variant")],
            ),
            patch("themeweaver.cli.commands.theme_generation._logger") as mock_logger,
        ):
            _run_contrast_validation("t1", ["dark", "light", "auto"], tmp_path)

        assert mock_logger.info.called
        assert mock_logger.warning.called

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
        args.syntax_colors = [f"#FF{i:02X}00" for i in range(17)]
        args.syntax_colors_dark = [f"#FF{i:02X}00" for i in range(17)]
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
                            assert len(syntax_call[1]["syntax_colors"]) == 17
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
        args.syntax_colors = ["#FF0000", "#00FF00"]  # Invalid count (should be 1 or 17)
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
