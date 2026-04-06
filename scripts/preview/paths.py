"""Filesystem paths for the preview app (repo-relative, not cwd-relative)."""

from pathlib import Path


def get_repo_root() -> Path:
    """Parent of ``scripts/`` (repository root)."""
    return Path(__file__).resolve().parent.parent.parent


def get_themes_dir() -> Path:
    """Directory containing theme YAML (``colorsystem.yaml``, ``mappings.yaml``, …)."""
    return get_repo_root() / "themes"
