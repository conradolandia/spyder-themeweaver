"""
Palette loading utilities for themeweaver.

This module provides functions to load color palettes from various sources
including files, command line arguments, and data structures.
"""

import json
from pathlib import Path

import yaml

from themeweaver.color_utils.color_analysis import load_color_groups_from_file


def _extract_color_group_from_yaml(yaml_data, group_name=None):
    """
    Extract a single color group from YAML data.

    Args:
        yaml_data: Parsed YAML data (dict)
        group_name: Specific color group to extract (if None, uses first found)

    Returns:
        Tuple of (group_name, colors_dict) or (None, None) if no valid group found
    """
    if not isinstance(yaml_data, dict):
        return None, None

    # Check if this is a nested color system (Primary: {B10: "#color", ...})
    color_groups = {}
    for name, values in yaml_data.items():
        if isinstance(values, dict):
            # Filter to only include hex color values
            colors = {
                k: v
                for k, v in values.items()
                if isinstance(v, str) and v.startswith("#")
            }
            if colors:
                color_groups[name] = colors

    if not color_groups:
        return None, None

    # Return requested group or first available
    if group_name and group_name in color_groups:
        return group_name, color_groups[group_name]
    else:
        first_group = list(color_groups.keys())[0]
        return first_group, color_groups[first_group]


def load_palette_from_file(file_path):
    """Load a palette from various file formats."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    errors = []

    # Try loading as Python color groups first
    try:
        color_groups = load_color_groups_from_file(str(file_path))
        if color_groups:
            # Use the first group found
            group_name = list(color_groups.keys())[0]
            colors = color_groups[group_name]
            return {"name": f"{group_name} (from {file_path.name})", "colors": colors}
    except (ImportError, SyntaxError, AttributeError, KeyError, TypeError) as e:
        errors.append(f"Python color groups: {type(e).__name__}: {e}")
    except Exception as e:
        errors.append(f"Python color groups: Unexpected error: {type(e).__name__}: {e}")

    # Try loading as YAML
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict):
                # Try extracting a color group from nested YAML structure
                group_name, colors = _extract_color_group_from_yaml(data)
                if group_name and colors:
                    return {
                        "name": f"{group_name} (from {file_path.name})",
                        "colors": colors,
                    }

                # If it's already in the expected format, return as-is
                if "colors" in data:
                    return data

                # Check if it's a flat color dictionary (all values are hex colors)
                if all(isinstance(v, str) and v.startswith("#") for v in data.values()):
                    return {"name": f"Palette from {file_path.name}", "colors": data}

                # Otherwise, assume it's some other format and try to use it
                return {"name": f"Palette from {file_path.name}", "colors": data}
    except yaml.YAMLError as e:
        errors.append(f"YAML parsing: {e}")
    except Exception as e:
        errors.append(f"YAML: Unexpected error: {type(e).__name__}: {e}")

    # Try loading as JSON
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                # Handle different JSON formats
                if "colors" in data:
                    return data
                else:
                    return {"name": f"Palette from {file_path.name}", "colors": data}
            else:
                errors.append(f"JSON: Expected dictionary, got {type(data).__name__}")
    except json.JSONDecodeError as e:
        errors.append(f"JSON parsing: {e}")
    except (UnicodeDecodeError, OSError) as e:
        errors.append(f"File reading: {type(e).__name__}: {e}")
    except Exception as e:
        errors.append(f"JSON: Unexpected error: {type(e).__name__}: {e}")

    # If we get here, all attempts failed
    error_details = "; ".join(errors) if errors else "Unknown format"
    raise ValueError(
        f"Could not parse palette from {file_path}. Attempted formats failed: {error_details}"
    )


def parse_palette_from_args(colors_arg):
    """Parse palette from command line argument."""
    colors = {}

    for item in colors_arg:
        if "=" in item:
            name, hex_color = item.split("=", 1)
            colors[name.strip()] = hex_color.strip()
        else:
            # Auto-name if no name provided
            colors[f"color{len(colors) + 1}"] = item.strip()

    return {"name": "Custom Palette", "colors": colors}


def validate_palette_data(palette_data):
    """Validate that palette data has the required structure."""
    if not isinstance(palette_data, dict):
        raise ValueError("Palette data must be a dictionary")

    if "name" not in palette_data:
        raise ValueError("Palette data must have a 'name' field")

    if "colors" not in palette_data:
        raise ValueError("Palette data must have a 'colors' field")

    if not isinstance(palette_data["colors"], dict):
        raise ValueError("Palette 'colors' field must be a dictionary")

    if not palette_data["colors"]:
        raise ValueError("Palette must contain at least one color")

    return True


def get_available_color_groups(file_path):
    """
    Get a list of available color group names from a file.

    Args:
        file_path: Path to the file containing color groups

    Returns:
        List of color group names
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return []

    try:
        # Try YAML first
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict):
                # Look for nested color groups
                group_names = []
                for name, values in data.items():
                    if isinstance(values, dict):
                        # Check if it contains color values
                        colors = {
                            k: v
                            for k, v in values.items()
                            if isinstance(v, str) and v.startswith("#")
                        }
                        if colors:
                            group_names.append(name)
                return group_names
    except Exception:
        pass

    return []
