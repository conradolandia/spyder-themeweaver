"""Tests for theme package CLI command."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from themeweaver.cli.commands.theme_package import (
    _read_package_metadata_from_pyproject,
    cmd_python_package,
)


class TestReadPackageMetadata:
    def test_returns_defaults_when_pyproject_missing(self, tmp_path: Path) -> None:
        metadata = _read_package_metadata_from_pyproject(tmp_path)
        assert metadata["version"] == "1.0.0"
        assert metadata["display_name"] == "Spyder Themes"
        assert metadata["requires-python"] == ">=3.9"

    def test_merges_defaults_with_spyder_package_section(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            """
[tool.themeweaver.spyder-package]
version = "2.1.0"
display_name = "My Theme Pack"
author = "Alice"
""".strip(),
            encoding="utf-8",
        )

        metadata = _read_package_metadata_from_pyproject(tmp_path)
        assert metadata["version"] == "2.1.0"
        assert metadata["display_name"] == "My Theme Pack"
        assert metadata["author"] == "Alice"
        # Not provided in file -> default still present.
        assert metadata["license"] == "MIT"

    def test_returns_defaults_on_invalid_toml(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            "[tool.themeweaver.spyder-package\nversion = 'oops'",
            encoding="utf-8",
        )

        metadata = _read_package_metadata_from_pyproject(tmp_path)
        assert metadata["version"] == "1.0.0"
        assert metadata["description"] == "Collection of themes for Spyder IDE"


class TestCmdPythonPackage:
    def test_cmd_python_package_passes_parsed_args(self) -> None:
        args = Mock()
        args.themes = "dracula, solarized"
        args.build_dir = "/tmp/build"
        args.output = "/tmp/out"
        args.package_name = "spyder_custom"
        args.with_pyproject = False
        args.validate = False

        with patch(
            "themeweaver.cli.commands.theme_package.SpyderPackageExporter"
        ) as mock_exporter_class:
            mock_exporter = Mock()
            mock_exporter.workspace_root = Path("/workspace")
            mock_exporter_class.return_value = mock_exporter

            with patch(
                "themeweaver.cli.commands.theme_package._read_package_metadata_from_pyproject",
                return_value={"version": "9.9.9"},
            ):
                cmd_python_package(args)

        mock_exporter_class.assert_called_once_with(
            build_dir=Path("/tmp/build"),
            output_dir=Path("/tmp/out"),
            package_name="spyder_custom",
        )
        mock_exporter.create_package.assert_called_once_with(
            theme_names=["dracula", "solarized"],
            metadata={"version": "9.9.9"},
            with_pyproject=False,
            validate=False,
        )

    def test_cmd_python_package_uses_defaults_for_missing_optional_args(self) -> None:
        # Intentionally omit build_dir and package_name to test hasattr branches.
        args = SimpleNamespace(
            themes=None,
            output=None,
            with_pyproject=True,
            validate=True,
        )

        with patch(
            "themeweaver.cli.commands.theme_package.SpyderPackageExporter"
        ) as mock_exporter_class:
            mock_exporter = Mock()
            mock_exporter.workspace_root = Path("/workspace")
            mock_exporter_class.return_value = mock_exporter

            with patch(
                "themeweaver.cli.commands.theme_package._read_package_metadata_from_pyproject",
                return_value={"version": "1.2.3"},
            ):
                cmd_python_package(args)

        mock_exporter_class.assert_called_once_with(
            build_dir=None,
            output_dir=None,
            package_name="spyder_themes",
        )
        mock_exporter.create_package.assert_called_once_with(
            theme_names=None,
            metadata={"version": "1.2.3"},
            with_pyproject=True,
            validate=True,
        )
