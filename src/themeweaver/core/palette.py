"""Spyder theme palette generation - dynamically created from YAML configurations."""

from pathlib import Path
from typing import List, Optional, Type

from qdarkstyle.palette import Palette

from themeweaver.core.colorsystem import (
    create_palette_class,
    get_color_classes_for_theme,
    load_semantic_mappings_from_yaml,
    load_theme_metadata_from_yaml,
)


class ThemePalettes:
    """Container for theme palette classes with variant-aware access."""

    def __init__(
        self, dark_palette: Optional[Type] = None, light_palette: Optional[Type] = None
    ) -> None:
        """Initialize with optional dark and light palette classes."""
        self.dark = dark_palette
        self.light = light_palette

    @property
    def has_dark(self) -> bool:
        """Check if theme supports dark variant."""
        return self.dark is not None

    @property
    def has_light(self) -> bool:
        """Check if theme supports light variant."""
        return self.light is not None

    @property
    def supported_variants(self) -> List[str]:
        """Get list of supported variant names."""
        variants: List[str] = []
        if self.has_dark:
            variants.append("dark")
        if self.has_light:
            variants.append("light")
        return variants

    def get_palette(self, variant: str) -> Optional[Type]:
        """Get palette class for specific variant.

        Args:
            variant: Variant name ("dark" or "light")

        Returns:
            Palette class or None if variant not supported
        """
        if variant == "dark":
            return self.dark
        elif variant == "light":
            return self.light
        else:
            return None


def create_palettes(
    theme_name: str = "solarized", themes_dir: Optional[Path] = None
) -> ThemePalettes:
    """Create palette classes dynamically from YAML configurations based on theme variants.

    Args:
        theme_name: Name of the theme to load. Defaults to "solarized".
        themes_dir: Directory where themes are stored. If None, uses default.

    Returns:
        ThemePalettes: Container with supported palette classes, also provides .dark and .light attributes.

    Raises:
        FileNotFoundError: If theme files are not found.
        ValueError: If no supported variants are found or YAML parsing fails.
    """
    # Load theme metadata to check supported variants
    theme_metadata = load_theme_metadata_from_yaml(theme_name, themes_dir=themes_dir)
    supported_variants = theme_metadata.get("variants", {})

    if not supported_variants:
        raise ValueError(
            f"No variants specified for theme '{theme_name}' in theme.yaml"
        )

    # Load semantic mappings from YAML
    semantic_mappings = load_semantic_mappings_from_yaml(
        theme_name, themes_dir=themes_dir
    )

    # Get theme-specific color classes (no global caching)
    color_classes = get_color_classes_for_theme(theme_name, themes_dir=themes_dir)

    # Create palette classes only for supported variants
    dark_palette: Optional[Type] = None
    light_palette: Optional[Type] = None

    if supported_variants.get("dark", False):
        dark_mappings = semantic_mappings.get("dark", {})
        if not dark_mappings:
            raise ValueError(
                f"Theme '{theme_name}' supports dark variant but no dark semantic mappings found"
            )
        dark_palette = create_palette_class(
            "dark", dark_mappings, color_classes, Palette
        )

    if supported_variants.get("light", False):
        light_mappings = semantic_mappings.get("light", {})
        if not light_mappings:
            raise ValueError(
                f"Theme '{theme_name}' supports light variant but no light semantic mappings found"
            )
        light_palette = create_palette_class(
            "light", light_mappings, color_classes, Palette
        )

    # Ensure at least one variant is supported
    if dark_palette is None and light_palette is None:
        raise ValueError(f"Theme '{theme_name}' has no enabled variants in theme.yaml")

    return ThemePalettes(dark_palette, light_palette)


# Export classes and functions
__all__ = ["ThemePalettes", "create_palettes"]
