"""Tests for yaml_theme_loader (definition files for theme generation)."""

from pathlib import Path

import pytest
import yaml

from themeweaver.core.yaml_theme_loader import (
    load_theme_from_yaml,
    parse_theme_definition,
)


class TestLoadThemeFromYaml:
    def test_file_not_found(self, tmp_path: Path) -> None:
        missing = tmp_path / "nope.yaml"
        with pytest.raises(FileNotFoundError, match="Theme definition file not found"):
            load_theme_from_yaml(missing)

    def test_empty_yaml(self, tmp_path: Path) -> None:
        p = tmp_path / "t.yaml"
        p.write_text("", encoding="utf-8")
        with pytest.raises(ValueError, match="Empty or invalid YAML"):
            load_theme_from_yaml(p)

    def test_multiple_top_level_keys(self, tmp_path: Path) -> None:
        p = tmp_path / "t.yaml"
        p.write_text(
            yaml.dump({"a": {"colors": []}, "b": {"colors": []}}),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="single top-level key"):
            load_theme_from_yaml(p)

    def test_success_adds_name(self, tmp_path: Path) -> None:
        p = tmp_path / "t.yaml"
        p.write_text(
            yaml.dump(
                {
                    "my-theme": {
                        "colors": [
                            "#111111",
                            "#222222",
                            "#333333",
                            "#444444",
                            "#555555",
                            "#666666",
                        ]
                    }
                }
            ),
            encoding="utf-8",
        )
        data = load_theme_from_yaml(p)
        assert data["name"] == "my-theme"
        assert len(data["colors"]) == 6


class TestParseThemeDefinition:
    def test_requires_name(self) -> None:
        with pytest.raises(ValueError, match="Theme name is required"):
            parse_theme_definition({"colors": ["#"] * 6})

    def test_requires_six_colors(self) -> None:
        with pytest.raises(ValueError, match="exactly 6 colors"):
            parse_theme_definition({"name": "x", "colors": ["#000000"]})

    def test_invalid_color_type(self) -> None:
        with pytest.raises(ValueError, match="must be a string"):
            parse_theme_definition(
                {
                    "name": "x",
                    "colors": [
                        1,
                        "#222222",
                        "#333333",
                        "#444444",
                        "#555555",
                        "#666666",
                    ],
                }
            )

    def test_invalid_color_hex(self) -> None:
        with pytest.raises(ValueError, match="not a valid hex color"):
            parse_theme_definition(
                {
                    "name": "x",
                    "colors": [
                        "not-a-color",
                        "#222222",
                        "#333333",
                        "#444444",
                        "#555555",
                        "#666666",
                    ],
                }
            )

    def test_three_digit_hex_rejected(self) -> None:
        with pytest.raises(ValueError, match="Expected format: #RRGGBB"):
            parse_theme_definition(
                {
                    "name": "x",
                    "colors": ["#111", "#222", "#333", "#444", "#555", "#666"],
                }
            )

    def test_syntax_format_mapping(self) -> None:
        out = parse_theme_definition(
            {
                "name": "x",
                "colors": [
                    "#111111",
                    "#222222",
                    "#333333",
                    "#444444",
                    "#555555",
                    "#666666",
                ],
                "syntax-format": {"keyword": "bold", "comment": "italic"},
            }
        )
        assert out["syntax_format"] == "keyword:bold,comment:italic"

    def test_syntax_colors_single_seed(self) -> None:
        out = parse_theme_definition(
            {
                "name": "x",
                "colors": [
                    "#111111",
                    "#222222",
                    "#333333",
                    "#444444",
                    "#555555",
                    "#666666",
                ],
                "syntax-colors": {"dark": ["#abcdef"], "light": ["#fedcba"]},
            }
        )
        assert out["syntax_colors_dark"] == "#abcdef"
        assert out["syntax_colors_light"] == "#fedcba"

    def test_syntax_colors_sixteen_rejected(self) -> None:
        dark = [f"#{i:02x}{i:02x}{i:02x}" for i in range(16)]
        with pytest.raises(ValueError, match="either 1 color"):
            parse_theme_definition(
                {
                    "name": "x",
                    "colors": [
                        "#111111",
                        "#222222",
                        "#333333",
                        "#444444",
                        "#555555",
                        "#666666",
                    ],
                    "syntax-colors": {"dark": dark},
                }
            )

    def test_syntax_colors_seventeen(self) -> None:
        dark = [f"#{i:02x}{i:02x}{i:02x}" for i in range(17)]
        out = parse_theme_definition(
            {
                "name": "x",
                "colors": [
                    "#111111",
                    "#222222",
                    "#333333",
                    "#444444",
                    "#555555",
                    "#666666",
                ],
                "syntax-colors": {"dark": dark},
            }
        )
        assert len(out["syntax_colors_dark"]) == 17

    def test_syntax_colors_invalid_count(self) -> None:
        with pytest.raises(ValueError, match="either 1 color"):
            parse_theme_definition(
                {
                    "name": "x",
                    "colors": [
                        "#111111",
                        "#222222",
                        "#333333",
                        "#444444",
                        "#555555",
                        "#666666",
                    ],
                    "syntax-colors": {"dark": ["#000000", "#111111"]},
                }
            )

    def test_syntax_colors_empty_list_skips_hex_validation(self) -> None:
        out = parse_theme_definition(
            {
                "name": "x",
                "colors": [
                    "#111111",
                    "#222222",
                    "#333333",
                    "#444444",
                    "#555555",
                    "#666666",
                ],
                "syntax-colors": {"dark": []},
            }
        )
        assert out["syntax_colors_dark"] is None

    def test_syntax_colors_invalid_element_type(self) -> None:
        with pytest.raises(ValueError, match="must be a string"):
            parse_theme_definition(
                {
                    "name": "x",
                    "colors": [
                        "#111111",
                        "#222222",
                        "#333333",
                        "#444444",
                        "#555555",
                        "#666666",
                    ],
                    "syntax-colors": {"dark": [123]},
                }
            )

    def test_syntax_colors_invalid_hex(self) -> None:
        with pytest.raises(ValueError, match="not a valid hex color"):
            parse_theme_definition(
                {
                    "name": "x",
                    "colors": [
                        "#111111",
                        "#222222",
                        "#333333",
                        "#444444",
                        "#555555",
                        "#666666",
                    ],
                    "syntax-colors": {"dark": ["#gggggg"]},
                }
            )

    def test_syntax_colors_three_digit_hex_rejected(self) -> None:
        with pytest.raises(ValueError, match="Expected format: #RRGGBB"):
            parse_theme_definition(
                {
                    "name": "x",
                    "colors": [
                        "#111111",
                        "#222222",
                        "#333333",
                        "#444444",
                        "#555555",
                        "#666666",
                    ],
                    "syntax-colors": {"dark": ["#abc"]},
                }
            )

    def test_optional_fields_defaults(self) -> None:
        out = parse_theme_definition(
            {
                "name": "x",
                "colors": [
                    "#111111",
                    "#222222",
                    "#333333",
                    "#444444",
                    "#555555",
                    "#666666",
                ],
                "display-name": "DN",
                "description": "D",
                "author": "A",
                "tags": ["t1"],
                "overwrite": True,
                "variants": ["dark"],
            }
        )
        assert out["display_name"] == "DN"
        assert out["description"] == "D"
        assert out["author"] == "A"
        assert out["tags"] == ["t1"]
        assert out["overwrite"] is True
        assert out["variants"] == ["dark"]
