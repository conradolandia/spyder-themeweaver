"""
Tests for color interpolation CLI command.
"""

import json
import sys
from io import StringIO
from unittest.mock import Mock, patch

from themeweaver.cli.commands.color_interpolation import cmd_interpolate


class TestColorInterpolationCommand:
    """Test color interpolation command functionality."""

    def test_cmd_interpolate_list_output(self) -> None:
        """Test interpolation with list output format."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 3
        args.method = "linear"
        args.exponent = 2
        args.output = "list"
        args.name = None
        args.simple_names = False
        args.analyze = False
        args.validate = False

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#800080", "#0000FF"]
                cmd_interpolate(args)
                output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert "Interpolated colors:" in output
        assert "0: #FF0000" in output
        assert "1: #800080" in output
        assert "2: #0000FF" in output

    def test_cmd_interpolate_json_output(self) -> None:
        """Test interpolation with JSON output format."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 3
        args.method = "linear"
        args.exponent = 2
        args.output = "json"
        args.name = "Test Palette"
        args.simple_names = False
        args.analyze = False
        args.validate = False

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#800080", "#0000FF"]
                cmd_interpolate(args)
                output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Parse JSON output
        json_start = output.find("{")
        json_end = output.rfind("}") + 1
        json_str = output[json_start:json_end]
        data = json.loads(json_str)

        assert "palette" in data
        assert "Test Palette" in data["palette"]
        assert data["palette"]["Test Palette"]["B0"] == "#FF0000"
        assert data["palette"]["Test Palette"]["B10"] == "#800080"
        assert data["palette"]["Test Palette"]["B20"] == "#0000FF"

    def test_cmd_interpolate_json_output_auto_name(self) -> None:
        """Test interpolation with JSON output and auto-generated name."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 2
        args.method = "linear"
        args.exponent = 2
        args.output = "json"
        args.name = None
        args.simple_names = True
        args.analyze = False
        args.validate = False

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#0000FF"]
                with patch(
                    "themeweaver.color_utils.color_names.get_palette_name_from_color"
                ) as mock_name:
                    mock_name.return_value = "Auto Red"
                    cmd_interpolate(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Parse JSON output
        json_start = output.find("{")
        json_end = output.rfind("}") + 1
        json_str = output[json_start:json_end]
        data = json.loads(json_str)

        assert "palette" in data
        assert "Auto Red" in data["palette"]

    def test_cmd_interpolate_yaml_output(self) -> None:
        """Test interpolation with YAML output format."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 2
        args.method = "linear"
        args.exponent = 2
        args.output = "yaml"
        args.name = "Test YAML"
        args.simple_names = False
        args.analyze = False
        args.validate = False

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#0000FF"]
                cmd_interpolate(args)
                output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert "# Generated color gradient using linear interpolation" in output
        assert "# From: #FF0000 to #0000FF" in output
        assert "# Steps: 2" in output
        assert "# Method: linear" in output
        assert "Test YAML:" in output

    def test_cmd_interpolate_yaml_output_exponential(self) -> None:
        """Test interpolation with YAML output and exponential method."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 3
        args.method = "exponential"
        args.exponent = 3.5
        args.output = "yaml"
        args.name = None
        args.simple_names = True
        args.analyze = False
        args.validate = False

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#800080", "#0000FF"]
                with patch(
                    "themeweaver.color_utils.color_names.get_palette_name_from_color"
                ) as mock_name:
                    mock_name.return_value = "Exponential Gradient"
                    cmd_interpolate(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert "# Generated color gradient using exponential interpolation" in output
        assert "# Exponent: 3.5" in output
        assert "Exponential Gradient:" in output

    def test_cmd_interpolate_with_analysis(self) -> None:
        """Test interpolation with analysis enabled."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 3
        args.method = "linear"
        args.exponent = 2
        args.output = "list"
        args.name = None
        args.simple_names = False
        args.analyze = True
        args.validate = False

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#800080", "#0000FF"]
                with patch(
                    "themeweaver.cli.commands.color_interpolation.analyze_interpolation"
                ) as mock_analyze:
                    cmd_interpolate(args)
                    mock_analyze.assert_called_once_with(
                        ["#FF0000", "#800080", "#0000FF"], "linear"
                    )
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_interpolate_with_validation_valid(self) -> None:
        """Test interpolation with validation enabled (valid gradient)."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 3
        args.method = "linear"
        args.exponent = 2
        args.output = "list"
        args.name = None
        args.simple_names = False
        args.analyze = False
        args.validate = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#800080", "#0000FF"]
                with patch(
                    "themeweaver.cli.commands.color_interpolation.validate_gradient_uniqueness"
                ) as mock_validate:
                    mock_validate.return_value = (
                        True,
                        {"total_colors": 3, "unique_colors": 3, "count": 0},
                    )
                    with patch(
                        "themeweaver.cli.commands.color_interpolation._logger"
                    ) as mock_logger:
                        cmd_interpolate(args)
                        mock_validate.assert_called_once_with(
                            ["#FF0000", "#800080", "#0000FF"], "linear"
                        )
                        mock_logger.info.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_interpolate_with_validation_invalid(self) -> None:
        """Test interpolation with validation enabled (invalid gradient)."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 3
        args.method = "linear"
        args.exponent = 2
        args.output = "list"
        args.name = None
        args.simple_names = False
        args.analyze = False
        args.validate = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#800080", "#0000FF"]
                with patch(
                    "themeweaver.cli.commands.color_interpolation.validate_gradient_uniqueness"
                ) as mock_validate:
                    mock_validate.return_value = (
                        False,
                        {"total_colors": 3, "unique_colors": 2, "count": 1},
                    )
                    with patch(
                        "themeweaver.cli.commands.color_interpolation._logger"
                    ) as mock_logger:
                        cmd_interpolate(args)
                        mock_validate.assert_called_once_with(
                            ["#FF0000", "#800080", "#0000FF"], "linear"
                        )
                        mock_logger.warning.assert_called()
        finally:
            sys.stdout = sys.__stdout__

    def test_cmd_interpolate_with_analysis_and_validation(self) -> None:
        """Test interpolation with both analysis and validation enabled."""
        args = Mock()
        args.start_color = "#FF0000"
        args.end_color = "#0000FF"
        args.steps = 3
        args.method = "lch"
        args.exponent = 2
        args.output = "list"
        args.name = None
        args.simple_names = False
        args.analyze = True
        args.validate = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_interpolation.interpolate_colors"
            ) as mock_interpolate:
                mock_interpolate.return_value = ["#FF0000", "#800080", "#0000FF"]
                with patch(
                    "themeweaver.cli.commands.color_interpolation.analyze_interpolation"
                ) as mock_analyze:
                    with patch(
                        "themeweaver.cli.commands.color_interpolation.validate_gradient_uniqueness"
                    ) as mock_validate:
                        mock_validate.return_value = (
                            True,
                            {"total_colors": 3, "unique_colors": 3, "count": 0},
                        )
                        with patch(
                            "themeweaver.cli.commands.color_interpolation._logger"
                        ):
                            cmd_interpolate(args)
                            mock_analyze.assert_called_once_with(
                                ["#FF0000", "#800080", "#0000FF"], "lch"
                            )
                            mock_validate.assert_called_once_with(
                                ["#FF0000", "#800080", "#0000FF"], "lch"
                            )
        finally:
            sys.stdout = sys.__stdout__
