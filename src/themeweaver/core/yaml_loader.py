"""
Centralized YAML loading utilities for ThemeWeaver.

This module provides unified functions for loading theme configuration files,
eliminating duplication across different modules.
"""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def load_yaml_file(file_path: Path, section: Optional[str] = None) -> Any:
    """
    Load and parse a YAML file with optional section extraction.

    Args:
        file_path: Path to the YAML file
        section: Optional section name to extract from the loaded data

    Returns:
        Parsed YAML data or the specified section

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the YAML file contains invalid syntax
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if section and isinstance(data, dict):
            return data.get(section, {})
        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {file_path}: {e}")


def load_colors_from_yaml(theme_name: str = "solarized") -> Dict[str, Any]:
    """
    Load color definitions from colorsystem.yaml file for a specific theme.

    Args:
        theme_name: Name of the theme to load. Defaults to "solarized".

    Returns:
        Color definitions loaded from the YAML file.

    Raises:
        FileNotFoundError: If the theme directory or colorsystem.yaml file doesn't exist.
        ValueError: If the YAML file contains invalid syntax.
    """
    current_dir = Path(__file__).parent
    yaml_file = current_dir.parent / "themes" / theme_name / "colorsystem.yaml"
    return load_yaml_file(yaml_file)


def load_color_mappings_from_yaml(theme_name: str = "solarized") -> Dict[str, Any]:
    """
    Load color class mappings from mappings.yaml file for a specific theme.

    Args:
        theme_name: Name of the theme to load. Defaults to "solarized".

    Returns:
        Color class mappings loaded from the YAML file.

    Raises:
        FileNotFoundError: If the theme directory or mappings.yaml file doesn't exist.
        ValueError: If the YAML file contains invalid syntax.
    """
    current_dir = Path(__file__).parent
    mappings_file = current_dir.parent / "themes" / theme_name / "mappings.yaml"
    return load_yaml_file(mappings_file, "color_classes")


def load_semantic_mappings_from_yaml(theme_name: str = "solarized") -> Dict[str, Any]:
    """
    Load semantic UI mappings from mappings.yaml file for a specific theme.

    Args:
        theme_name: Name of the theme to load. Defaults to "solarized".

    Returns:
        Semantic mappings for dark and light variants.

    Raises:
        FileNotFoundError: If the theme directory or mappings.yaml file doesn't exist.
        ValueError: If the YAML file contains invalid syntax.
    """
    current_dir = Path(__file__).parent
    mappings_file = current_dir.parent / "themes" / theme_name / "mappings.yaml"
    return load_yaml_file(mappings_file, "semantic_mappings")


def load_theme_metadata_from_yaml(theme_name: str = "solarized") -> Dict[str, Any]:
    """
    Load theme metadata from theme.yaml file for a specific theme.

    Args:
        theme_name: Name of the theme to load. Defaults to "solarized".

    Returns:
        Theme metadata loaded from the YAML file.

    Raises:
        FileNotFoundError: If the theme directory or theme.yaml file doesn't exist.
        ValueError: If the YAML file contains invalid syntax.
    """
    current_dir = Path(__file__).parent
    yaml_file = current_dir.parent / "themes" / theme_name / "theme.yaml"
    return load_yaml_file(yaml_file)
