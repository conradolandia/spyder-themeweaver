"""Tests for CLI gradient command."""

import json
import sys
from io import StringIO
from unittest.mock import Mock, patch

import pytest

from themeweaver.cli.commands.color_gradient import (
    _generate_gradient_with_method,
    cmd_gradient,
)


class TestGenerateGradientWithMethod:
    def test_lch_lightness(self) -> None:
        colors = _generate_gradient_with_method("#336699", "lch-lightness")
        assert len(colors) == 16
        assert colors[0].upper() == "#000000"
        assert colors[-1].upper() == "#FFFFFF"

    def test_linear_adds_hash_and_caps(self) -> None:
        colors = _generate_gradient_with_method("aabbcc", "linear")
        assert len(colors) == 16
        assert colors[0] == "#000000"
        assert "#AABBCC" in colors

    def test_exponential_uses_exponent(self) -> None:
        colors = _generate_gradient_with_method("#FF0000", "exponential", exponent=3.0)
        assert len(colors) == 16

    def test_pad_when_interpolate_short(self) -> None:
        with patch(
            "themeweaver.cli.commands.color_gradient.interpolate_colors",
            return_value=["#000000", "#111111"],
        ):
            colors = _generate_gradient_with_method("#FF0000", "linear")
        assert len(colors) == 16
        assert colors[0] == "#000000"
        assert colors[15] == "#FFFFFF"

    def test_trim_when_interpolate_long(self) -> None:
        long_list = [f"#{i:02x}0000" for i in range(30)]

        def fake_interp(_a, _b, _steps, _m, _e):
            return long_list

        with patch(
            "themeweaver.cli.commands.color_gradient.interpolate_colors",
            side_effect=fake_interp,
        ):
            colors = _generate_gradient_with_method("#800000", "linear")
        assert len(colors) == 16


class TestCmdGradient:
    def _stdout(self) -> StringIO:
        return StringIO()

    def test_list_output(self) -> None:
        args = Mock()
        args.color = "#123456"
        args.method = "lch-lightness"
        args.exponent = 2.0
        args.output = "list"
        args.name = None
        args.simple_names = False
        args.analyze = False
        args.validate = False
        buf = self._stdout()
        old = sys.stdout
        sys.stdout = buf
        try:
            cmd_gradient(args)
        finally:
            sys.stdout = old
        out = buf.getvalue()
        assert "B0:" in out
        assert "B150:" in out

    def test_json_output_with_name(self) -> None:
        args = Mock()
        args.color = "#123456"
        args.method = "linear"
        args.exponent = 2.0
        args.output = "json"
        args.name = "MyPal"
        args.simple_names = True
        args.analyze = False
        args.validate = False
        with patch(
            "themeweaver.cli.commands.color_gradient._generate_gradient_with_method",
            return_value=["#000000"] + ["#111111"] * 14 + ["#FFFFFF"],
        ):
            buf = self._stdout()
            old = sys.stdout
            sys.stdout = buf
            try:
                cmd_gradient(args)
            finally:
                sys.stdout = old
        data = json.loads(buf.getvalue())
        assert "MyPal" in data["palette"]

    def test_json_output_auto_palette_name(self) -> None:
        args = Mock()
        args.color = "#123456"
        args.method = "linear"
        args.exponent = 2.0
        args.output = "json"
        args.name = None
        args.simple_names = True
        args.analyze = False
        args.validate = False
        with (
            patch(
                "themeweaver.cli.commands.color_gradient._generate_gradient_with_method",
                return_value=["#000000"] + ["#111111"] * 14 + ["#FFFFFF"],
            ),
            patch(
                "themeweaver.color_utils.color_names.get_palette_name_from_color",
                return_value="auto_name",
            ),
        ):
            buf = self._stdout()
            old = sys.stdout
            sys.stdout = buf
            try:
                cmd_gradient(args)
            finally:
                sys.stdout = old
        data = json.loads(buf.getvalue())
        assert "auto_name" in data["palette"]

    def test_yaml_output_auto_name_in_yaml_branch(self) -> None:
        args = Mock()
        args.color = "#ABCDEF"
        args.method = "linear"
        args.exponent = 2.0
        args.output = "yaml"
        args.name = None
        args.simple_names = True
        args.analyze = False
        args.validate = False
        stub = ["#000000"] + ["#ABCDEF"] * 14 + ["#FFFFFF"]
        with (
            patch(
                "themeweaver.cli.commands.color_gradient._generate_gradient_with_method",
                return_value=stub,
            ),
            patch(
                "themeweaver.color_utils.color_names.get_palette_name_from_color",
                return_value="yaml_auto",
            ),
        ):
            buf = self._stdout()
            old = sys.stdout
            sys.stdout = buf
            try:
                cmd_gradient(args)
            finally:
                sys.stdout = old
        out = buf.getvalue()
        assert "yaml_auto:" in out

    def test_yaml_output_and_exponent_comment(self) -> None:
        args = Mock()
        args.color = "#FF0000"
        args.method = "exponential"
        args.exponent = 2.5
        args.output = "yaml"
        args.name = "ExpPal"
        args.simple_names = False
        args.analyze = False
        args.validate = False
        with patch(
            "themeweaver.cli.commands.color_gradient._generate_gradient_with_method",
            return_value=["#000000"] + ["#FF0000"] * 14 + ["#FFFFFF"],
        ):
            buf = self._stdout()
            old = sys.stdout
            sys.stdout = buf
            try:
                cmd_gradient(args)
            finally:
                sys.stdout = old
        out = buf.getvalue()
        assert "ExpPal:" in out
        assert "Exponent: 2.5" in out
        assert "B0:" in out

    def test_yaml_analyze_and_validate(self, caplog: pytest.LogCaptureFixture) -> None:
        args = Mock()
        args.color = "#00FF00"
        args.method = "linear"
        args.exponent = 2.0
        args.output = "yaml"
        args.name = "N"
        args.simple_names = False
        args.analyze = True
        args.validate = True
        gradient = (
            ["#000000"]
            + [f"#{i:02x}{i:02x}{i:02x}" for i in range(1, 15)]
            + ["#FFFFFF"]
        )
        with (
            patch(
                "themeweaver.cli.commands.color_gradient._generate_gradient_with_method",
                return_value=gradient,
            ),
            patch(
                "themeweaver.cli.commands.color_gradient.analyze_interpolation"
            ) as mock_analyze,
            patch(
                "themeweaver.cli.commands.color_gradient.validate_gradient_uniqueness",
                return_value=(
                    False,
                    {"total_colors": 16, "unique_colors": 8, "count": 8},
                ),
            ),
        ):
            buf = self._stdout()
            old = sys.stdout
            sys.stdout = buf
            try:
                cmd_gradient(args)
            finally:
                sys.stdout = old
        mock_analyze.assert_called_once()
        assert "Duplicate colors detected" in caplog.text

    def test_validate_success_path(self, caplog: pytest.LogCaptureFixture) -> None:
        args = Mock()
        args.color = "#112233"
        args.method = "linear"
        args.exponent = 2.0
        args.output = "yaml"
        args.name = "V"
        args.simple_names = False
        args.analyze = False
        args.validate = True
        gradient = ["#000000"] + ["#112233"] * 14 + ["#FFFFFF"]
        with (
            patch(
                "themeweaver.cli.commands.color_gradient._generate_gradient_with_method",
                return_value=gradient,
            ),
            patch(
                "themeweaver.cli.commands.color_gradient.validate_gradient_uniqueness",
                return_value=(True, {}),
            ),
        ):
            with caplog.at_level("INFO"):
                buf = self._stdout()
                old = sys.stdout
                sys.stdout = buf
                try:
                    cmd_gradient(args)
                finally:
                    sys.stdout = old
        assert "No duplicate colors found" in caplog.text

    def test_operation_context_when_not_quiet(self) -> None:
        args = Mock()
        args.color = "#ABCDEF"
        args.method = "lch-lightness"
        args.exponent = 2.0
        args.output = "unknown-format"
        args.name = None
        args.simple_names = False
        args.analyze = False
        args.validate = False
        buf = self._stdout()
        old = sys.stdout
        sys.stdout = buf
        try:
            with patch(
                "themeweaver.cli.commands.color_gradient.operation_context"
            ) as mock_ctx:
                mock_ctx.return_value.__enter__ = Mock()
                mock_ctx.return_value.__exit__ = Mock(return_value=False)
                cmd_gradient(args)
        finally:
            sys.stdout = old
        mock_ctx.assert_called_once_with("Gradient generation")

    def test_unknown_method_description_in_yaml_comment(self) -> None:
        """method_descriptions.get fallback appears in YAML header when method is unknown."""
        args = Mock()
        args.color = "#123456"
        args.method = "custom-method-xyz"
        args.exponent = 2.0
        args.output = "yaml"
        args.name = "Z"
        args.simple_names = False
        args.analyze = False
        args.validate = False
        stub = ["#000000"] + ["#123456"] * 14 + ["#FFFFFF"]
        with patch(
            "themeweaver.cli.commands.color_gradient._generate_gradient_with_method",
            return_value=stub,
        ):
            buf = self._stdout()
            old = sys.stdout
            sys.stdout = buf
            try:
                cmd_gradient(args)
            finally:
                sys.stdout = old
        assert "# Method: custom-method-xyz" in buf.getvalue()
