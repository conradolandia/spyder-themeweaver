"""Resolve theme semantic colors to hex values."""

from pathlib import Path
from typing import Dict, Optional, Union

from themeweaver.color_utils import blend_alpha
from themeweaver.core.palette import create_palettes


def _extract_hex(value: Union[str, tuple, int, float]) -> Optional[str]:
    """Extract hex color from palette attribute value."""
    if isinstance(value, str) and value.startswith("#"):
        return value
    if isinstance(value, (list, tuple)) and len(value) >= 1:
        first = value[0]
        if isinstance(first, str) and first.startswith("#"):
            return first
    return None


def resolve_theme_colors(
    theme_name: str,
    variant: str,
    themes_dir: Optional[Path] = None,
) -> Dict[str, str]:
    """
    Resolve all semantic color names to hex for a theme variant.

    Args:
        theme_name: Theme name (e.g. "spyder")
        variant: "dark" or "light"
        themes_dir: Directory containing themes. If None, uses default.

    Returns:
        Dict mapping semantic name to hex. Includes blended backgrounds
        for GROUP rules (e.g. PG1 uses blend of COLOR_BACKGROUND_1 + GROUP_1).
    """
    palettes = create_palettes(theme_name, themes_dir=themes_dir)
    palette_class = palettes.get_palette(variant)
    if palette_class is None:
        raise ValueError(f"Theme '{theme_name}' does not support variant '{variant}'")

    palette = palette_class()
    colors: Dict[str, str] = {}

    for name in dir(palette):
        if name.startswith("_"):
            continue
        value = getattr(palette, name)
        hex_val = _extract_hex(value)
        if hex_val:
            colors[name] = hex_val

    return colors


def get_color_for_rule(
    colors: Dict[str, str],
    rule: Dict,
    role: str,
) -> Optional[str]:
    """
    Get the effective color for a rule's foreground or background.

    Handles: simple ref, blended bg [A, B], fg_opacity.
    """
    if role == "fg":
        ref = rule.get("fg")
    elif role == "bg":
        ref = rule.get("bg")
    elif role == "line_bg":
        ref = rule.get("line_bg")
    else:
        return None

    if ref is None:
        return None

    if isinstance(ref, list):
        if len(ref) == 2 and "bg_blend" in rule:
            base, overlay = ref[0], ref[1]
            base_hex = colors.get(base)
            overlay_hex = colors.get(overlay)
            if base_hex and overlay_hex:
                return blend_alpha(base_hex, overlay_hex, rule["bg_blend"])
        return None

    return colors.get(ref)
