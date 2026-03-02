"""Tests for contrast rules loader."""

from themeweaver.contrast.rules_loader import load_rules


def test_load_rules_dark() -> None:
    """Test loading dark rules."""
    rules = load_rules("dark")
    assert isinstance(rules, dict)
    assert "PE1" in rules
    assert rules["PE1"]["fg"] == "EDITOR_NORMAL"
    assert rules["PE1"]["bg"] == "EDITOR_BACKGROUND"
    assert rules["PE1"]["min_ratio"] == 7


def test_load_rules_light() -> None:
    """Test loading light rules."""
    rules = load_rules("light")
    assert isinstance(rules, dict)
    assert "PE1" in rules
    assert rules["PE1"]["min_ratio"] == 7
    assert rules["PE6"]["min_ratio"] == 5  # Different from dark


def test_load_rules_pe5a_has_line_bg() -> None:
    """Test PE5A has line_bg and fg_lbg_min."""
    rules = load_rules("dark")
    assert "line_bg" in rules["PE5A"]
    assert rules["PE5A"]["line_bg"] == "COLOR_OCCURRENCE_4"
    assert rules["PE5A"]["fg_lbg_min"] == 3
    assert rules["PE5A"]["fg_bg_min"] == 9


def test_load_rules_pg_has_blend() -> None:
    """Test PG rules have bg blend."""
    rules = load_rules("dark")
    assert rules["PG1"]["bg"] == ["COLOR_BACKGROUND_1", "GROUP_1"]
    assert rules["PG1"]["bg_blend"] == 0.5
