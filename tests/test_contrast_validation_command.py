"""Tests for contrast validation CLI command."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from themeweaver.cli.commands.contrast_validation import (
    _get_themes_to_validate,
    cmd_validate_contrast,
)
from themeweaver.contrast.validator import RuleResult, ValidationResult


class TestGetThemesToValidate:
    def test_single_theme(self) -> None:
        args = Mock()
        args.all = False
        args.theme = "spyder"
        args.theme_dir = None
        assert _get_themes_to_validate(args) == ["spyder"]

    def test_no_theme_returns_empty(self) -> None:
        args = Mock()
        args.all = False
        args.theme = None
        assert _get_themes_to_validate(args) == []

    def test_all_discovers_sorted(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        td = tmp_path / "themes"
        td.mkdir()
        (td / "zebra").mkdir()
        (td / "alpha").mkdir()
        (td / "skip.txt").write_text("x", encoding="utf-8")
        (td / ".hidden").mkdir()

        args = Mock()
        args.all = True
        args.theme_dir = None
        monkeypatch.chdir(tmp_path)
        names = _get_themes_to_validate(args)
        assert names == ["alpha", "zebra"]

    def test_all_custom_theme_dir(self, tmp_path: Path) -> None:
        td = tmp_path / "mythemes"
        (td / "t1").mkdir(parents=True)
        args = Mock()
        args.all = True
        args.theme_dir = str(td)
        assert _get_themes_to_validate(args) == ["t1"]

    def test_all_missing_directory(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        monkeypatch.chdir(tmp_path)
        args = Mock()
        args.all = True
        args.theme_dir = None
        assert _get_themes_to_validate(args) == []
        assert "Theme directory not found" in caplog.text


class TestCmdValidateContrast:
    @staticmethod
    def _make_result(
        *,
        passed: int,
        failed: int,
        rule_passed: bool = True,
        with_suggestion: bool = False,
    ) -> ValidationResult:
        results = []
        for _ in range(passed):
            results.append(
                RuleResult(rule_id="P1", passed=True, message="ok", actual_ratio=4.5)
            )
        for i in range(failed):
            results.append(
                RuleResult(
                    rule_id=f"F{i}",
                    passed=False,
                    message="bad",
                    actual_ratio=1.0,
                    suggestion="try darker" if with_suggestion else None,
                )
            )
        return ValidationResult(
            variant="dark",
            results=results,
            passed_count=passed,
            failed_count=failed,
        )

    def test_no_themes_logs_error(self, caplog: pytest.LogCaptureFixture) -> None:
        args = Mock()
        args.theme = None
        args.all = False
        args.theme_dir = None
        args.rules_dir = None
        args.variant = "dark"
        args.verbose = False
        with caplog.at_level("ERROR"):
            cmd_validate_contrast(args)
        assert "No themes to validate" in caplog.text

    def test_single_theme_pass(self, caplog: pytest.LogCaptureFixture) -> None:
        args = Mock()
        args.theme = "spyder"
        args.all = False
        args.theme_dir = None
        args.rules_dir = None
        args.variant = "dark"
        args.verbose = False
        ok = self._make_result(passed=2, failed=0)
        with patch(
            "themeweaver.cli.commands.contrast_validation.validate_theme",
            return_value=ok,
        ):
            with caplog.at_level("INFO"):
                cmd_validate_contrast(args)
        assert "Contrast validation for theme: spyder" in caplog.text
        assert "dark: PASS" in caplog.text

    def test_verbose_shows_passed_rules(self, caplog: pytest.LogCaptureFixture) -> None:
        args = Mock()
        args.theme = "spyder"
        args.all = False
        args.theme_dir = None
        args.rules_dir = None
        args.variant = "light"
        args.verbose = True
        res = self._make_result(passed=1, failed=0)
        res.variant = "light"
        with patch(
            "themeweaver.cli.commands.contrast_validation.validate_theme",
            return_value=res,
        ):
            with caplog.at_level("INFO"):
                cmd_validate_contrast(args)
        assert "[P]" in caplog.text

    def test_mixed_results_skip_passed_lines_when_not_verbose(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Inner loop runs (failure present); passed rules hit continue when verbose is off."""
        args = Mock()
        args.theme = "spyder"
        args.all = False
        args.theme_dir = None
        args.rules_dir = None
        args.variant = "dark"
        args.verbose = False
        results = [
            RuleResult("OK1", True, message="fine", actual_ratio=5.0),
            RuleResult("BAD1", False, message="low", actual_ratio=1.0),
        ]
        res = ValidationResult(
            variant="dark",
            results=results,
            passed_count=1,
            failed_count=1,
        )
        with patch(
            "themeweaver.cli.commands.contrast_validation.validate_theme",
            return_value=res,
        ):
            with caplog.at_level("INFO"):
                cmd_validate_contrast(args)
        assert "[F]" in caplog.text
        assert "BAD1" in caplog.text
        assert "OK1" not in caplog.text

    def test_failure_shows_suggestion(self, caplog: pytest.LogCaptureFixture) -> None:
        args = Mock()
        args.theme = "spyder"
        args.all = False
        args.theme_dir = None
        args.rules_dir = None
        args.variant = "dark"
        args.verbose = False
        res = self._make_result(passed=0, failed=1, with_suggestion=True)
        with patch(
            "themeweaver.cli.commands.contrast_validation.validate_theme",
            return_value=res,
        ):
            with caplog.at_level("INFO"):
                cmd_validate_contrast(args)
        assert "[F]" in caplog.text
        assert "Suggestion: try darker" in caplog.text

    def test_validate_theme_error_continues(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        args = Mock()
        args.theme = "missing"
        args.all = False
        args.theme_dir = None
        args.rules_dir = None
        args.variant = "both"
        args.verbose = False

        def boom(**_kwargs):
            raise ValueError("no such theme")

        with patch(
            "themeweaver.cli.commands.contrast_validation.validate_theme",
            side_effect=boom,
        ):
            with caplog.at_level("ERROR"):
                cmd_validate_contrast(args)
        assert "no such theme" in caplog.text

    def test_both_variants(self, caplog: pytest.LogCaptureFixture) -> None:
        args = Mock()
        args.theme = "spyder"
        args.all = False
        args.theme_dir = None
        args.rules_dir = None
        args.variant = "both"
        args.verbose = False

        def fake_validate(*, variant, **_kwargs):
            r = ValidationResult(
                variant=variant, results=[], passed_count=1, failed_count=0
            )
            return r

        with patch(
            "themeweaver.cli.commands.contrast_validation.validate_theme",
            side_effect=fake_validate,
        ):
            with caplog.at_level("INFO"):
                cmd_validate_contrast(args)
        assert "dark: PASS" in caplog.text
        assert "light: PASS" in caplog.text

    def test_grand_total_multiple_themes(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        args = Mock()
        args.all = False
        args.theme = None
        args.theme_dir = None
        args.rules_dir = None
        args.variant = "dark"
        args.verbose = False

        with (
            patch(
                "themeweaver.cli.commands.contrast_validation._get_themes_to_validate",
                return_value=["a", "b"],
            ),
            patch(
                "themeweaver.cli.commands.contrast_validation.validate_theme",
                return_value=self._make_result(passed=1, failed=0),
            ),
        ):
            with caplog.at_level("INFO"):
                cmd_validate_contrast(args)
        assert "Grand total:" in caplog.text
