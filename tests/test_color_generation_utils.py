"""Coverage-focused tests for color generation algorithms."""

from unittest.mock import patch

from themeweaver.color_utils.color_generation import (
    apply_theme_adjustments,
    generate_optimal_colors,
    generate_theme_colors,
    generate_uniform_colors,
)


def test_apply_theme_adjustments_dark_and_light_bounds() -> None:
    dark = apply_theme_adjustments([10, 119, 30], "dark")
    light = apply_theme_adjustments([94, 119, 40], "light")
    assert dark[0] >= 15
    assert dark[1] <= 120
    assert light[0] <= 95
    assert light[1] <= 120


def test_generate_uniform_colors_calls_lch_to_hex_per_color() -> None:
    with patch(
        "themeweaver.color_utils.color_generation.lch_to_hex",
        side_effect=["#111111", "#222222", "#333333"],
    ) as mock_hex:
        colors = generate_uniform_colors(3, 0, 60, 70, "dark")
    assert colors == ["#111111", "#222222", "#333333"]
    assert mock_hex.call_count == 3


def test_generate_theme_colors_uniform_and_golden_paths() -> None:
    with patch(
        "themeweaver.color_utils.color_generation.generate_uniform_colors",
        return_value=["#AAAAAA"],
    ) as mock_uniform:
        c1 = generate_theme_colors(theme="light", num_colors=1, uniform=True)
    assert c1 == ["#AAAAAA"]
    assert mock_uniform.called

    with patch(
        "themeweaver.color_utils.color_generation.generate_golden_ratio_colors",
        return_value=["#BBBBBB"],
    ) as mock_golden:
        c2 = generate_theme_colors(theme="dark", num_colors=1, uniform=False)
    assert c2 == ["#BBBBBB"]
    assert mock_golden.called


def test_generate_optimal_colors_start_hue_and_hue_bands() -> None:
    captured_hues = []

    def fake_hex(_l: float, _c: float, h: float) -> str:
        captured_hues.append(h)
        return "#123456"

    with patch(
        "themeweaver.color_utils.color_generation.lch_to_hex", side_effect=fake_hex
    ):
        colors = generate_optimal_colors(num_colors=8, theme="dark", start_hue=70)
    assert len(colors) == 8
    assert captured_hues[0] == 70
    assert all(isinstance(c, str) and c.startswith("#") for c in colors)


def test_generate_optimal_colors_without_start_hue_light_theme() -> None:
    with patch(
        "themeweaver.color_utils.color_generation.lch_to_hex",
        return_value="#654321",
    ):
        colors = generate_optimal_colors(num_colors=5, theme="light", start_hue=None)
    assert len(colors) == 5
