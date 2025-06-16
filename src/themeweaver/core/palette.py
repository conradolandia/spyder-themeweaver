"""Spyder Solarized theme palette - dynamically generated from YAML mappings."""

from qdarkstyle.palette import Palette
from themeweaver.core.colorsystem import (
    Primary,
    Secondary,
    Green,
    Red,
    Orange,
    GroupDark,
    GroupLight,
    Logos,
    load_semantic_mappings_from_yaml,
    create_palette_class,
)


def create_palettes(theme_name="solarized"):
    """Create DarkPalette and LightPalette classes dynamically from YAML mappings.

    Args:
        theme_name (str): Name of the theme to load. Defaults to "solarized".

    Returns:
        tuple: (DarkPalette, LightPalette) classes

    Raises:
        FileNotFoundError: If theme files are not found.
        ValueError: If YAML parsing or color resolution fails.
    """
    # Load semantic mappings from YAML
    semantic_mappings = load_semantic_mappings_from_yaml(theme_name)

    # Available color classes for reference resolution
    color_classes = {
        "Primary": Primary,
        "Secondary": Secondary,
        "Green": Green,
        "Red": Red,
        "Orange": Orange,
        "GroupDark": GroupDark,
        "GroupLight": GroupLight,
        "Logos": Logos,
    }

    # Create palette classes dynamically
    dark_mappings = semantic_mappings.get("dark", {})
    light_mappings = semantic_mappings.get("light", {})

    if not dark_mappings:
        raise ValueError(f"No dark semantic mappings found for theme '{theme_name}'")
    if not light_mappings:
        raise ValueError(f"No light semantic mappings found for theme '{theme_name}'")

    DarkPalette = create_palette_class("dark", dark_mappings, color_classes, Palette)
    LightPalette = create_palette_class("light", light_mappings, color_classes, Palette)

    return DarkPalette, LightPalette


# Create the palette classes at module level for backward compatibility
DarkPalette, LightPalette = create_palettes()


# Export classes
__all__ = [
    "DarkPalette",
    "LightPalette",
    "create_palettes",
]
