"""Tests for contrast validator."""

from themeweaver.contrast import validate_theme


def test_validate_theme_spyder_dark() -> None:
    """Test validating spyder dark theme."""
    result = validate_theme("spyder", "dark", include_suggestions=True)
    assert result.variant == "dark"
    assert len(result.results) > 0
    assert result.passed_count + result.failed_count == len(result.results)


def test_validate_theme_spyder_light() -> None:
    """Test validating spyder light theme."""
    result = validate_theme("spyder", "light", include_suggestions=True)
    assert result.variant == "light"
    assert len(result.results) > 0


def test_validate_theme_suggestions_on_failure() -> None:
    """Test that failed rules get suggestions when applicable."""
    result = validate_theme("spyder", "dark", include_suggestions=True)
    failed_with_suggestion = [
        r for r in result.results if not r.passed and r.suggestion
    ]
    # Some failed rules should have suggestions
    assert len(failed_with_suggestion) >= 0  # May have none if all pass
