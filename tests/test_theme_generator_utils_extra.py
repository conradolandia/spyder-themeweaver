"""Additional branch coverage for theme_generator_utils."""

from unittest.mock import patch

from themeweaver.color_utils import theme_generator_utils as tgu


def _fake_palette(prefix: str) -> dict[str, str]:
    base = sum(ord(c) for c in prefix) % 120 + 80
    return {
        f"B{i * 10}": f"#{(base + i) % 256:02X}{(base + i * 2) % 256:02X}{(base + i * 3) % 256:02X}"
        for i in range(1, 18)
    }


def test_get_palette_names_fallback_for_empty_normalized_name() -> None:
    colors = ["#111111", "#222222", "#333333", "#444444", "#555555", "#666666"]
    color_names = {c: "name" for c in colors}

    with (
        patch(
            "themeweaver.color_utils.theme_generator_utils.normalize_color_name_to_safe_ascii",
            return_value="",
        ),
        patch(
            "themeweaver.color_utils.theme_generator_utils.generate_random_adjective",
            return_value="Calm",
        ),
    ):
        names = tgu.get_palette_names(colors, color_names)

    assert names["primary"] == "CalmColor111111"
    assert names["group_base"] == "CalmColor666666"


def test_build_colorsystem_defaults_syntax_dark_only_variant() -> None:
    palettes = {
        "primary": [f"#A{i:02X}" for i in range(16)],
        "secondary": [f"#B{i:02X}" for i in range(16)],
        "error": [f"#C{i:02X}" for i in range(16)],
        "success": [f"#D{i:02X}" for i in range(16)],
        "warning": [f"#E{i:02X}" for i in range(16)],
    }
    names = {
        "primary": "P",
        "secondary": "S",
        "error": "E",
        "success": "U",
        "warning": "W",
        "group_base": "Group",
    }

    with patch(
        "themeweaver.color_utils.theme_generator_utils.generate_palettes_from_color"
    ) as mock_gen:
        mock_gen.side_effect = [
            (_fake_palette("D"), _fake_palette("L")),  # group
            _fake_palette("SD"),  # default dark syntax fallback
        ]
        colorsystem = tgu.build_colorsystem(
            palettes=palettes,
            names=names,
            group_initial_color="#123456",
            syntax_colors_dark=None,
            syntax_colors_light=None,
            variants=["dark"],
        )

    assert "AutoSyntaxDark" in colorsystem
    assert "AutoSyntaxLight" not in colorsystem
    assert "Logos" in colorsystem


def test_build_colorsystem_provided_light_syntax_list() -> None:
    palettes = {
        "primary": [f"#A{i:02X}" for i in range(16)],
        "secondary": [f"#B{i:02X}" for i in range(16)],
        "error": [f"#C{i:02X}" for i in range(16)],
        "success": [f"#D{i:02X}" for i in range(16)],
        "warning": [f"#E{i:02X}" for i in range(16)],
    }
    names = {
        "primary": "P",
        "secondary": "S",
        "error": "E",
        "success": "U",
        "warning": "W",
        "group_base": "Group",
        "syntax_light": "MySyntaxLight",
    }

    with (
        patch(
            "themeweaver.color_utils.theme_generator_utils.generate_palettes_from_color"
        ) as mock_gen,
        patch(
            "themeweaver.color_utils.theme_generator_utils.generate_syntax_palette_from_colors",
            return_value=_fake_palette("LS"),
        ),
    ):
        mock_gen.side_effect = [
            (_fake_palette("D"), _fake_palette("L")),  # group
            _fake_palette("DD"),  # default dark syntax fallback
        ]
        colorsystem = tgu.build_colorsystem(
            palettes=palettes,
            names=names,
            group_initial_color="#123456",
            syntax_colors_dark=None,
            syntax_colors_light=["#111111"] * 17,
            variants=["dark", "light"],
        )

    assert "DefaultSyntaxDark" in colorsystem
    assert "MySyntaxLight" in colorsystem


def test_parse_syntax_format_invalid_tokens_ignored() -> None:
    fmt = "keyword:bold,unknown:bold,comment:both,broken,instance:none"
    parsed = tgu.parse_syntax_format(fmt)
    assert parsed["keyword"]["bold"] is True
    assert parsed["comment"]["bold"] is True and parsed["comment"]["italic"] is True
    assert parsed["instance"]["bold"] is False and parsed["instance"]["italic"] is False


def test_validate_input_colors_with_invalid_syntax_entry() -> None:
    ok, msg = tgu.validate_input_colors(
        "#1A72BB",
        "#FF5500",
        "#E11C1C",
        "#00AA55",
        "#FF9900",
        "#8844EE",
        syntax_colors=["#777777", "#GGGGGG"],
    )
    assert ok is False
    assert "syntax_2" in msg
