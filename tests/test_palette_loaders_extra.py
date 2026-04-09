"""Additional branch coverage for palette loader utilities."""

from pathlib import Path

import pytest

from themeweaver.color_utils.palette_loaders import (
    _extract_color_group_from_yaml,
    get_available_color_groups,
    load_color_groups_from_file,
    load_palette_from_file,
    validate_palette_data,
)


def test_extract_color_group_non_dict_returns_none_pair() -> None:
    assert _extract_color_group_from_yaml(["not", "dict"]) == (None, None)


def test_extract_color_group_requested_or_first_available() -> None:
    data = {
        "Primary": {"B10": "#111111", "x": 1},
        "Secondary": {"B10": "#222222"},
    }
    name, colors = _extract_color_group_from_yaml(data, "Secondary")
    assert name == "Secondary"
    assert colors == {"B10": "#222222"}

    first_name, first_colors = _extract_color_group_from_yaml(data, "Missing")
    assert first_name == "Primary"
    assert first_colors == {"B10": "#111111"}


def test_load_color_groups_from_python_file(tmp_path: Path) -> None:
    py = tmp_path / "colors.py"
    py.write_text(
        """
class Primary:
    B10 = "#AA0000"
    B20 = "#BB0000"
    X = 12

class Empty:
    VALUE = 123
""".strip(),
        encoding="utf-8",
    )
    groups = load_color_groups_from_file(py)
    assert "Primary" in groups
    assert groups["Primary"]["B10"] == "#AA0000"
    assert "Empty" not in groups


def test_load_palette_from_python_color_groups(tmp_path: Path) -> None:
    py = tmp_path / "pal.py"
    py.write_text(
        """
class GroupDark:
    B10 = "#101010"
    B20 = "#202020"
""".strip(),
        encoding="utf-8",
    )
    palette = load_palette_from_file(py)
    assert "GroupDark" in palette["name"]
    assert palette["colors"]["B10"] == "#101010"


def test_load_palette_yaml_nested_and_flat_fallback(tmp_path: Path) -> None:
    nested = tmp_path / "nested.yaml"
    nested.write_text(
        """
Primary:
  B10: "#111111"
Meta:
  author: "x"
""".strip(),
        encoding="utf-8",
    )
    p1 = load_palette_from_file(nested)
    assert p1["colors"]["B10"] == "#111111"

    flat_mixed = tmp_path / "mixed.yaml"
    flat_mixed.write_text(
        """
red: "#ff0000"
note: "not a color"
""".strip(),
        encoding="utf-8",
    )
    p2 = load_palette_from_file(flat_mixed)
    assert p2["colors"]["red"] == "#ff0000"
    assert p2["colors"]["note"] == "not a color"


def test_load_palette_json_non_dict_raises_value_error(tmp_path: Path) -> None:
    j = tmp_path / "list.json"
    j.write_text('["a", "b"]', encoding="utf-8")
    with pytest.raises(ValueError, match="Could not parse palette"):
        load_palette_from_file(j)


def test_validate_palette_data_invalid_shapes() -> None:
    with pytest.raises(ValueError, match="must be a dictionary"):
        validate_palette_data("bad")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must be a dictionary"):
        validate_palette_data({"name": "n", "colors": []})


def test_get_available_color_groups_yaml_and_bad_yaml(tmp_path: Path) -> None:
    good = tmp_path / "groups.yaml"
    good.write_text(
        """
Primary:
  B10: "#111111"
Meta:
  value: 1
""".strip(),
        encoding="utf-8",
    )
    assert get_available_color_groups(good) == ["Primary"]

    bad = tmp_path / "bad.yaml"
    bad.write_text(":\n  - [", encoding="utf-8")
    assert get_available_color_groups(bad) == []
