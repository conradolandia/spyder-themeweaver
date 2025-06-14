"""
Palette loading utilities for themeweaver.

This module provides functions to load color palettes from various sources
including files, command line arguments, and data structures.
"""

import json
from pathlib import Path

from .color_analysis import load_color_groups_from_file


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
