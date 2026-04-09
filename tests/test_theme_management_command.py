"""Additional coverage for theme management commands."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from themeweaver.cli.commands.theme_management import cmd_info, cmd_list, cmd_validate


def test_cmd_list_no_themes_logs_and_returns() -> None:
    args = SimpleNamespace(theme_dir=None)
    with (
        patch("themeweaver.cli.commands.theme_management.list_themes", return_value=[]),
        patch("themeweaver.cli.commands.theme_management._logger") as mock_logger,
    ):
        cmd_list(args)
    mock_logger.info.assert_called_with("No themes found.")


def test_cmd_list_handles_metadata_errors_per_theme() -> None:
    args = SimpleNamespace(theme_dir=None)
    with (
        patch(
            "themeweaver.cli.commands.theme_management.list_themes",
            return_value=["ok-theme", "bad-theme"],
        ),
        patch(
            "themeweaver.cli.commands.theme_management.load_theme_metadata_from_yaml",
            side_effect=[
                {
                    "display_name": "OK",
                    "description": "good",
                    "variants": {"dark": True, "light": False},
                },
                RuntimeError("boom"),
            ],
        ),
        patch("themeweaver.cli.commands.theme_management._logger") as mock_logger,
    ):
        cmd_list(args)
    assert mock_logger.info.called
    assert mock_logger.error.called


def test_cmd_info_passes_theme_and_optional_dir() -> None:
    args = SimpleNamespace(theme="dracula", theme_dir="/tmp/themes")
    with patch(
        "themeweaver.cli.commands.theme_management.show_theme_info"
    ) as mock_show:
        cmd_info(args)
    mock_show.assert_called_once_with("dracula", themes_dir=Path("/tmp/themes"))


def test_cmd_validate_runs_all_steps_and_palette_instantiation() -> None:
    args = SimpleNamespace(theme="dracula", theme_dir=None)
    palettes = Mock()
    palettes.supported_variants = ["dark", "light"]
    dark_palette_cls = type("DarkPalette", (), {"ID": "DarkID"})
    light_palette_cls = type("LightPalette", (), {"ID": "LightID"})

    def get_palette(v: str):
        return dark_palette_cls if v == "dark" else light_palette_cls

    palettes.get_palette.side_effect = get_palette

    with (
        patch(
            "themeweaver.cli.commands.theme_management.load_theme_metadata_from_yaml"
        ) as mock_meta,
        patch(
            "themeweaver.cli.commands.theme_management.create_palettes",
            return_value=palettes,
        ) as mock_create,
        patch("themeweaver.cli.commands.theme_management._logger") as mock_logger,
    ):
        cmd_validate(args)

    mock_meta.assert_called_once()
    mock_create.assert_called_once()
    assert mock_logger.info.called
