# Color System mapping for Theme Weaver

from themeweaver.core.yaml_loader import (
    load_theme_metadata_from_yaml,
    load_colors_from_yaml,
    load_color_mappings_from_yaml,
    load_semantic_mappings_from_yaml,
)


def _create_color_class(name, colors):
    """Dynamically create a color class with the given name and color values."""
    class_attrs = {}
    for key, value in colors.items():
        class_attrs[key] = value

    # Create the class dynamically
    color_class = type(name, (), class_attrs)
    return color_class


def _resolve_color_reference(color_ref, color_classes):
    """Resolve a color reference string like 'Primary.B10' to actual color value.

    Args:
        color_ref (str): Color reference in format 'ClassName.Attribute'
        color_classes (dict): Dictionary of available color classes

    Returns:
        str: The resolved color value

    Raises:
        ValueError: If the color reference cannot be resolved
    """
    if isinstance(color_ref, (int, float)):
        # Non-color values like OPACITY_TOOLTIP
        return color_ref

    if not isinstance(color_ref, str) or "." not in color_ref:
        raise ValueError(f"Invalid color reference format: {color_ref}")

    class_name, attribute = color_ref.split(".", 1)

    if class_name not in color_classes:
        raise ValueError(f"Color class '{class_name}' not found")

    color_class = color_classes[class_name]
    if not hasattr(color_class, attribute):
        raise ValueError(
            f"Attribute '{attribute}' not found in color class '{class_name}'"
        )

    return getattr(color_class, attribute)


def create_palette_class(palette_id, semantic_mappings, color_classes, base_class):
    """Dynamically create a palette class from semantic mappings.

    Args:
        palette_id (str): Identifier for the palette ("dark" or "light")
        semantic_mappings (dict): Semantic color mappings for this palette
        color_classes (dict): Available color classes (Primary, Secondary, etc.)
        base_class: Base class to inherit from (e.g., qdarkstyle.palette.Palette)

    Returns:
        type: Dynamically created palette class
    """
    class_attrs = {"ID": palette_id}

    # Resolve all color references to actual values
    for semantic_name, color_ref in semantic_mappings.items():
        try:
            resolved_value = _resolve_color_reference(color_ref, color_classes)
            class_attrs[semantic_name] = resolved_value
        except ValueError as e:
            raise ValueError(f"Failed to resolve '{semantic_name}': {e}")

    # Create the class dynamically
    class_name = f"{palette_id.capitalize()}Palette"
    palette_class = type(class_name, (base_class,), class_attrs)
    return palette_class


def get_color_classes_for_theme(theme_name="solarized"):
    """Get theme-specific color classes without global caching.

    Args:
        theme_name (str): Name of the theme to load. Defaults to "solarized".

    Returns:
        dict: Dictionary of color classes for the theme

    Raises:
        FileNotFoundError: If theme files are not found.
        ValueError: If YAML parsing fails.
    """
    # Load colors and mappings from YAML for the specific theme
    color_data = load_colors_from_yaml(theme_name)
    color_mappings = load_color_mappings_from_yaml(theme_name)

    # Create all color classes dynamically using mappings
    created_classes = {}
    for class_name, palette_name in color_mappings.items():
        if palette_name in color_data:
            created_classes[class_name] = _create_color_class(
                class_name, color_data[palette_name]
            )
        else:
            raise ValueError(
                f"Palette '{palette_name}' not found in colorsystem.yaml for class '{class_name}'"
            )

    return created_classes


# Create default color classes for backward compatibility (solarized theme)
# These will be used when importing this module directly
_default_color_classes = get_color_classes_for_theme("solarized")

# Make the default classes available at module level for backward compatibility
Primary = _default_color_classes.get("Primary")
Secondary = _default_color_classes.get("Secondary")
Success = _default_color_classes.get("Success")
Error = _default_color_classes.get("Error")
Warning = _default_color_classes.get("Warning")
GroupDark = _default_color_classes.get("GroupDark")
GroupLight = _default_color_classes.get("GroupLight")
Logos = _default_color_classes.get("Logos")


# Export all classes and utility functions
__all__ = [
    "load_theme_metadata_from_yaml",
    "load_colors_from_yaml",
    "load_color_mappings_from_yaml",
    "load_semantic_mappings_from_yaml",
    "create_palette_class",
    "get_color_classes_for_theme",
    "Primary",
    "Secondary",
    "Success",
    "Error",
    "Warning",
    "GroupDark",
    "GroupLight",
    "Logos",
]
