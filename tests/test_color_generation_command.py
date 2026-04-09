#!/usr/bin/env python3
"""
Tests for color generation command in themeweaver.

Tests the palette generation functionality including:
- Different generation methods (perceptual, optimal, uniform, syntax)
- Output formats (class, json, list)
- Error handling
- Analysis functionality

Run with: `python -m pytest tests/test_color_generation_command.py -v`
"""

import json
import logging
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from themeweaver.cli.commands.color_generation import cmd_palette


class TestColorGenerationCommand:
    """Test color generation command functionality."""

    def test_cmd_palette_syntax_method_missing_from_color(self, caplog) -> None:
        """Test syntax method error when --from-color is missing."""
        args = Mock()
        args.method = "syntax"
        args.from_color = None
        args.num_colors = 16
        args.start_hue = None
        args.output_format = "list"
        args.no_analysis = False

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            cmd_palette(args)
            __output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert "❌ Syntax method requires --from-color argument" in caplog.text

    def test_cmd_palette_output_format_class(self) -> None:
        """Test palette generation with class output format."""
        args = Mock()
        args.method = "perceptual"
        args.from_color = None
        args.num_colors = 3
        args.start_hue = None
        args.output_format = "class"
        args.no_analysis = False

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_theme_colors"
            ) as mock_generate:
                mock_generate.return_value = ["#FF0000", "#00FF00", "#0000FF"]
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ):
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert "class GroupDark:" in output
        assert "class GroupLight:" in output
        assert "B10 = '#FF0000'" in output
        assert "B20 = '#00FF00'" in output
        assert "B30 = '#0000FF'" in output

    def test_cmd_palette_output_format_class_syntax(self) -> None:
        """Test palette generation with class output format for syntax method."""
        args = Mock()
        args.method = "syntax"
        args.from_color = "#FF0000"
        args.num_colors = 3
        args.start_hue = None
        args.output_format = "class"
        args.no_analysis = False

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_palettes_from_color"
            ) as mock_generate:
                mock_generate.return_value = {
                    "B0": "#FF0000",
                    "B10": "#00FF00",
                    "B20": "#0000FF",
                }
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ):
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert "class Syntax:" in output
        assert "B10 = '#FF0000'" in output
        assert "B20 = '#00FF00'" in output
        assert "B30 = '#0000FF'" in output

    def test_cmd_palette_output_format_json(self) -> None:
        """Test palette generation with JSON output format."""
        args = Mock()
        args.method = "perceptual"
        args.from_color = None
        args.num_colors = 3
        args.start_hue = None
        args.output_format = "json"
        args.no_analysis = False

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_theme_colors"
            ) as mock_generate:
                mock_generate.return_value = ["#FF0000", "#00FF00", "#0000FF"]
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ):
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Parse JSON output - find the JSON part before the analysis output
        json_start = output.find("{")
        json_end = output.rfind("}") + 1
        json_str = output[json_start:json_end]

        json_data = json.loads(json_str)
        assert "GroupDark" in json_data
        assert "GroupLight" in json_data
        assert json_data["GroupDark"]["B10"] == "#FF0000"
        assert json_data["GroupDark"]["B20"] == "#00FF00"
        assert json_data["GroupDark"]["B30"] == "#0000FF"

    def test_cmd_palette_output_format_json_syntax(self) -> None:
        """Test palette generation with JSON output format for syntax method."""
        args = Mock()
        args.method = "syntax"
        args.from_color = "#FF0000"
        args.num_colors = 3
        args.start_hue = None
        args.output_format = "json"
        args.no_analysis = False

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_palettes_from_color"
            ) as mock_generate:
                mock_generate.return_value = {
                    "B0": "#FF0000",
                    "B10": "#00FF00",
                    "B20": "#0000FF",
                }
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ):
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Parse JSON output - find the JSON part before the analysis output
        json_start = output.find("{")
        json_end = output.rfind("}") + 1
        json_str = output[json_start:json_end]

        json_data = json.loads(json_str)
        assert "Syntax" in json_data
        assert json_data["Syntax"]["B10"] == "#FF0000"
        assert json_data["Syntax"]["B20"] == "#00FF00"
        assert json_data["Syntax"]["B30"] == "#0000FF"

    def test_cmd_palette_output_format_list(self) -> None:
        """Test palette generation with list output format."""
        args = Mock()
        args.method = "perceptual"
        args.from_color = None
        args.num_colors = 3
        args.start_hue = None
        args.output_format = "list"
        args.no_analysis = False

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_theme_colors"
            ) as mock_generate:
                mock_generate.return_value = ["#FF0000", "#00FF00", "#0000FF"]
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ):
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert "GroupDark colors:" in output
        assert "GroupLight colors:" in output
        assert "  B10: #FF0000" in output
        assert "  B20: #00FF00" in output
        assert "  B30: #0000FF" in output

    def test_cmd_palette_output_format_list_syntax(self) -> None:
        """Test palette generation with list output format for syntax method."""
        args = Mock()
        args.method = "syntax"
        args.from_color = "#FF0000"
        args.num_colors = 3
        args.start_hue = None
        args.output_format = "list"
        args.no_analysis = False

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_palettes_from_color"
            ) as mock_generate:
                mock_generate.return_value = {
                    "B0": "#FF0000",
                    "B10": "#00FF00",
                    "B20": "#0000FF",
                }
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ):
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert "Syntax colors:" in output
        assert "  B10: #FF0000" in output
        assert "  B20: #00FF00" in output
        assert "  B30: #0000FF" in output

    def test_cmd_palette_without_analysis(self) -> None:
        """Test palette generation with analysis disabled."""
        args = Mock()
        args.method = "perceptual"
        args.from_color = None
        args.num_colors = 3
        args.start_hue = None
        args.output_format = "list"
        args.no_analysis = True

        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_theme_colors"
            ) as mock_generate:
                mock_generate.return_value = ["#FF0000", "#00FF00", "#0000FF"]
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ) as mock_analyze:
                    cmd_palette(args)
                    __output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        # Check that analysis was not called
        assert mock_analyze.call_count == 0

    def test_cmd_palette_from_color_golden_ratio_list(self) -> None:
        """Golden-ratio path when --from-color is set (takes precedence over method)."""
        args = Mock()
        args.method = "perceptual"
        args.from_color = "#FF0000"
        args.num_colors = 3
        args.start_hue = None
        args.output_format = "list"
        args.no_analysis = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_palettes_from_color"
            ) as mock_gp:
                mock_gp.return_value = (
                    {"a": "#111111", "b": "#222222", "c": "#333333"},
                    {"a": "#AAAAAA", "b": "#BBBBBB", "c": "#CCCCCC"},
                )
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ) as mock_analyze:
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        mock_gp.assert_called_once_with("#FF0000", 3)
        assert mock_analyze.call_count == 0
        assert "GroupDark colors:" in output
        assert "  B10: #111111" in output
        assert "GroupLight colors:" in output
        assert "  B10: #AAAAAA" in output

    def test_cmd_palette_optimal_method_list(self) -> None:
        args = Mock()
        args.method = "optimal"
        args.from_color = None
        args.num_colors = 2
        args.start_hue = 120
        args.output_format = "list"
        args.no_analysis = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_optimal_colors"
            ) as mock_opt:
                mock_opt.side_effect = [["#010101", "#020202"], ["#FEFEFE", "#FDFDFD"]]
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ) as mock_analyze:
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert mock_opt.call_args_list[0][0][:2] == (2, "dark")
        assert mock_opt.call_args_list[0][0][2] == 120
        assert mock_opt.call_args_list[1][0][:2] == (2, "light")
        assert mock_analyze.call_count == 0
        assert "  B10: #010101" in output
        assert "  B10: #FEFEFE" in output

    def test_cmd_palette_uniform_method_list(self) -> None:
        args = Mock()
        args.method = "uniform"
        args.from_color = None
        args.num_colors = 2
        args.start_hue = None
        args.output_format = "list"
        args.no_analysis = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with patch(
                "themeweaver.cli.commands.color_generation.generate_theme_colors"
            ) as mock_gen:
                mock_gen.side_effect = [["#030303", "#040404"], ["#FCFCFC", "#FBFBFB"]]
                with patch(
                    "themeweaver.cli.commands.color_generation.analyze_chromatic_distances"
                ) as mock_analyze:
                    cmd_palette(args)
                    output = captured_output.getvalue()
        finally:
            sys.stdout = sys.__stdout__

        assert mock_gen.call_count == 2
        assert mock_gen.call_args_list[0][0][0] == "dark"
        assert mock_gen.call_args_list[0][1]["uniform"] is True
        assert mock_analyze.call_count == 0
        assert "  B10: #030303" in output

    def test_cmd_palette_non_quiet_logs_header(self, caplog) -> None:
        """When output_format is not class/json/list, header logs are emitted."""
        args = Mock()
        args.method = "perceptual"
        args.from_color = None
        args.num_colors = 4
        args.start_hue = 200
        args.output_format = "none"
        args.no_analysis = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with caplog.at_level(logging.INFO):
                with patch(
                    "themeweaver.cli.commands.color_generation.generate_theme_colors"
                ) as mock_gen:
                    mock_gen.side_effect = [
                        ["#A", "#B", "#C", "#D"],
                        ["#a", "#b", "#c", "#d"],
                    ]
                    cmd_palette(args)
        finally:
            sys.stdout = sys.__stdout__

        assert "🎨 Generated using Golden ratio distribution" in caplog.text
        assert "🎯 Start hue: 200" in caplog.text
        assert "📊 Colors: 4" in caplog.text
        assert captured_output.getvalue() == ""

    def test_cmd_palette_non_quiet_start_hue_auto_logged(self, caplog) -> None:
        args = Mock()
        args.method = "perceptual"
        args.from_color = None
        args.num_colors = 2
        args.start_hue = None
        args.output_format = "none"
        args.no_analysis = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with caplog.at_level(logging.INFO):
                with patch(
                    "themeweaver.cli.commands.color_generation.generate_theme_colors"
                ) as mock_gen:
                    mock_gen.side_effect = [["#1", "#2"], ["#9", "#8"]]
                    cmd_palette(args)
        finally:
            sys.stdout = sys.__stdout__

        assert "auto (37° dark, 53° light)" in caplog.text
        assert captured_output.getvalue() == ""

    def test_cmd_palette_non_quiet_from_color_logs(self, caplog) -> None:
        args = Mock()
        args.method = "perceptual"
        args.from_color = "#ABCDEF"
        args.num_colors = 2
        args.start_hue = None
        args.output_format = "none"
        args.no_analysis = True

        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            with caplog.at_level(logging.INFO):
                with patch(
                    "themeweaver.cli.commands.color_generation.generate_palettes_from_color"
                ) as mock_gp:
                    mock_gp.return_value = ({"x": "#1"}, {"y": "#2"})
                    cmd_palette(args)
        finally:
            sys.stdout = sys.__stdout__

        assert "🎯 Starting color: #ABCDEF" in caplog.text
        assert "Golden ratio from #ABCDEF" in caplog.text
        assert captured_output.getvalue() == ""

    def test_cmd_palette_syntax_missing_from_color_non_quiet(self, caplog) -> None:
        args = Mock()
        args.method = "syntax"
        args.from_color = None
        args.num_colors = 8
        args.start_hue = None
        args.output_format = "none"
        args.no_analysis = False

        with caplog.at_level(logging.ERROR):
            cmd_palette(args)

        assert "❌ Syntax method requires --from-color argument" in caplog.text


if __name__ == "__main__":
    # Run tests with pytest
    exit_code = pytest.main([__file__, "-v"])
    sys.exit(exit_code)
