"""Tests for syntax schema single source of truth."""

from themeweaver.color_utils.palette_generators import (
    generate_syntax_palette_from_colors,
)
from themeweaver.core.syntax_schema import (
    build_editor_syntax_mappings,
    formatted_editor_keys,
    syntax_palette_keys,
    syntax_palette_slot_count,
)


def test_palette_slot_count_matches_keys() -> None:
    assert len(syntax_palette_keys()) == syntax_palette_slot_count()


def test_generate_syntax_palette_uses_schema_keys() -> None:
    count = syntax_palette_slot_count()
    colors = [f"#{i:02x}{i:02x}{i:02x}" for i in range(count)]
    palette = generate_syntax_palette_from_colors(colors)

    assert list(palette.keys()) == syntax_palette_keys()
    assert len(palette) == count


def test_builder_contains_all_formatted_editor_keys() -> None:
    dark = build_editor_syntax_mappings("dark", None)
    light = build_editor_syntax_mappings("light", None)

    for key in formatted_editor_keys():
        assert key in dark
        assert key in light
