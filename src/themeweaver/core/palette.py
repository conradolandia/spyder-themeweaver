"""Spyder theme palette generation - dynamically created from YAML configurations."""

from qdarkstyle.palette import Palette

from themeweaver.core.colorsystem import (
    create_palette_class,
    get_color_classes_for_theme,
    load_semantic_mappings_from_yaml,
    load_theme_metadata_from_yaml,
)


class ThemePalettes:
    """Container for theme palette classes with variant-aware access."""

    def __init__(self, dark_palette=None, light_palette=None):
        """Initialize with optional dark and light palette classes."""
        self.dark = dark_palette
        self.light = light_palette

    @property
    def has_dark(self):
        """Check if theme supports dark variant."""
        return self.dark is not None

    @property
    def has_light(self):
        """Check if theme supports light variant."""
        return self.light is not None

    @property
    def supported_variants(self):
        """Get list of supported variant names."""
        variants = []
        if self.has_dark:
            variants.append("dark")
        if self.has_light:
            variants.append("light")
        return variants

    def get_palette(self, variant):
        """Get palette class for specific variant.

        Args:
            variant (str): Variant name ("dark" or "light")

        Returns:
            Palette class or None if variant not supported
        """
        if variant == "dark":
            return self.dark
        elif variant == "light":
            return self.light
        else:
            return None


def create_palettes(theme_name="solarized"):
    """Create palette classes dynamically from YAML configurations based on theme variants.

    Args:
        theme_name (str): Name of the theme to load. Defaults to "solarized".

    Returns:
        ThemePalettes: Container with supported palette classes.
                      For backward compatibility, also provides .dark and .light attributes.

    Raises:
        FileNotFoundError: If theme files are not found.
        ValueError: If no supported variants are found or YAML parsing fails.
    """
    # Load theme metadata to check supported variants
    theme_metadata = load_theme_metadata_from_yaml(theme_name)
    supported_variants = theme_metadata.get("variants", {})

    if not supported_variants:
        raise ValueError(
            f"No variants specified for theme '{theme_name}' in theme.yaml"
        )

    # Load semantic mappings from YAML
    semantic_mappings = load_semantic_mappings_from_yaml(theme_name)

    # Get theme-specific color classes (no global caching)
    color_classes = get_color_classes_for_theme(theme_name)

    # Create palette classes only for supported variants
    dark_palette = None
    light_palette = None

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


# Create the default palette classes at module level for backward compatibility
# Note: These are created with solarized theme for backward compatibility only
# For theme exports, create_palettes(theme_name) should be used directly
try:
    _default_palettes = create_palettes("solarized")
    DarkPalette = _default_palettes.dark
    LightPalette = _default_palettes.light
except Exception:
    # Fallback if solarized theme is not available
    DarkPalette = None
    LightPalette = None


# Export classes and functions
__all__ = ["ThemePalettes", "DarkPalette", "LightPalette", "create_palettes"]
