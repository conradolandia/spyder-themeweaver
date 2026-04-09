"""Tests for color name normalization and API parsing."""

from themeweaver.color_utils.color_names import normalize_color_name_to_safe_ascii


def test_normalize_apostrophe_and_spaces() -> None:
    assert normalize_color_name_to_safe_ascii("Guns N' Roses") == "GunsNRoses"
    assert normalize_color_name_to_safe_ascii("Red") == "Red"


def test_normalize_curly_apostrophe() -> None:
    # U+2019 RIGHT SINGLE QUOTATION MARK
    assert normalize_color_name_to_safe_ascii("Guns N\u2019 Roses") == "GunsNRoses"


def test_normalize_accented_latin() -> None:
    assert normalize_color_name_to_safe_ascii("Café Noir") == "CafeNoir"


def test_normalize_empty_or_whitespace() -> None:
    assert normalize_color_name_to_safe_ascii("") == ""
    assert normalize_color_name_to_safe_ascii("   ") == ""


def test_normalize_non_latin_only() -> None:
    assert normalize_color_name_to_safe_ascii("日本") == ""


def test_normalize_mixed_and_digits() -> None:
    assert normalize_color_name_to_safe_ascii("Level 42 Gray") == "Level42Gray"
