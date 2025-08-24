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
        assert "B0 = '#FF0000'" in output
        assert "B10 = '#00FF00'" in output
        assert "B20 = '#0000FF'" in output

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
        assert json_data["Syntax"]["B0"] == "#FF0000"
        assert json_data["Syntax"]["B10"] == "#00FF00"
        assert json_data["Syntax"]["B20"] == "#0000FF"

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
        assert "  B0: #FF0000" in output
        assert "  B10: #00FF00" in output
        assert "  B20: #0000FF" in output

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


if __name__ == "__main__":
    # Run tests with pytest
    exit_code = pytest.main([__file__, "-v"])
    sys.exit(exit_code)
