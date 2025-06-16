#!/usr/bin/env python3
"""Detailed inspection of Theme objects and their internal structure."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))


def inspect_object(obj, name, max_attrs=20):
    """Inspect an object and show its internal structure."""
    print(f"\n=== Inspecting {name} ===")
    print(f"Type: {type(obj)}")
    print(f"String representation: {obj}")

    # Show __dict__ if available
    if hasattr(obj, "__dict__"):
        print(f"__dict__: {obj.__dict__}")

    # Show all attributes
    print("\nAll attributes:")
    attrs = [attr for attr in dir(obj) if not attr.startswith("_")]
    for i, attr in enumerate(attrs[:max_attrs]):
        try:
            value = getattr(obj, attr)
            if callable(value):
                print(f"  {attr}(): {type(value)} (method/function)")
            else:
                print(f"  {attr}: {value} ({type(value)})")
        except Exception as e:
            print(f"  {attr}: <Error accessing: {e}>")

    if len(attrs) > max_attrs:
        print(f"  ... and {len(attrs) - max_attrs} more attributes")

    # Show methods
    methods = [
        method
        for method in dir(obj)
        if callable(getattr(obj, method, None)) and not method.startswith("_")
    ]
    if methods:
        print(
            f"\nPublic methods: {', '.join(methods[:10])}{'...' if len(methods) > 10 else ''}"
        )


def main():
    print("=== Deep Inspection of Theme Objects ===")

    # Import the required classes
    from themeweaver.core.theme import Theme
    from themeweaver.core.palette import create_palettes, DarkPalette, LightPalette

    # Create a theme
    print("\n1. Creating theme with dynamically created palettes...")
    palettes = create_palettes("solarized")
    theme = Theme("Solarized Test", palettes.dark, palettes.light)

    # Inspect the Theme object itself
    inspect_object(theme, "Theme instance")

    # Inspect the palette container
    inspect_object(palettes, "ThemePalettes container")

    # Inspect individual palettes
    inspect_object(palettes.dark, "Dark Palette Class")
    inspect_object(palettes.light, "Light Palette Class")

    # Show specific color attributes from palettes
    print("\n=== Color Attributes from Palettes ===")
    color_attrs = [attr for attr in dir(palettes.dark) if attr.startswith("COLOR_")]
    print("\nDark palette colors:")
    for attr in color_attrs[:10]:  # Show first 10
        value = getattr(palettes.dark, attr)
        print(f"  {attr}: {value}")

    print("\nLight palette colors:")
    for attr in color_attrs[:10]:  # Show first 10
        value = getattr(palettes.light, attr)
        print(f"  {attr}: {value}")

    # Show inheritance chain
    print("\n=== Inheritance Information ===")
    print(f"Dark palette MRO: {[cls.__name__ for cls in palettes.dark.__mro__]}")
    print(f"Light palette MRO: {[cls.__name__ for cls in palettes.light.__mro__]}")

    # Create an instance of the palette to see if it behaves differently
    print("\n=== Palette Instance vs Class ===")
    try:
        dark_instance = palettes.dark()
        print(f"Dark palette instance: {dark_instance}")
        print(f"Instance type: {type(dark_instance)}")
        print(f"Instance COLOR_BACKGROUND_1: {dark_instance.COLOR_BACKGROUND_1}")
    except Exception as e:
        print(f"Could not create palette instance: {e}")

    # Show class vs instance comparison for module-level palettes
    print("\n=== Module-level Palettes ===")
    print(f"DarkPalette class: {DarkPalette}")
    print(f"DarkPalette.COLOR_BACKGROUND_1: {DarkPalette.COLOR_BACKGROUND_1}")
    print(f"LightPalette class: {LightPalette}")
    print(f"LightPalette.COLOR_BACKGROUND_1: {LightPalette.COLOR_BACKGROUND_1}")

    # Compare with original qdarkstyle palettes if available
    print("\n=== Comparison with QDarkStyle Original ===")
    try:
        from qdarkstyle.dark.palette import DarkPalette as QDarkPalette
        from qdarkstyle.light.palette import LightPalette as QLightPalette

        print(f"QDarkStyle DarkPalette: {QDarkPalette}")
        print(
            f"QDarkStyle DarkPalette.COLOR_BACKGROUND_1: {QDarkPalette.COLOR_BACKGROUND_1}"
        )
        print(f"Our DarkPalette.COLOR_BACKGROUND_1: {DarkPalette.COLOR_BACKGROUND_1}")
        print(
            f"Colors match: {QDarkPalette.COLOR_BACKGROUND_1 == DarkPalette.COLOR_BACKGROUND_1}"
        )
        print("=" * 80)
        print(f"QDarkStyle LightPalette: {QLightPalette}")
        print(
            f"QDarkStyle LightPalette.COLOR_BACKGROUND_1: {QLightPalette.COLOR_BACKGROUND_1}"
        )
        print(f"Our LightPalette.COLOR_BACKGROUND_1: {LightPalette.COLOR_BACKGROUND_1}")
        print(
            f"Colors match: {QLightPalette.COLOR_BACKGROUND_1 == LightPalette.COLOR_BACKGROUND_1}"
        )

    except ImportError:
        print("QDarkStyle palettes not available for comparison")

    print("\n=== Inspection Complete! ===")


if __name__ == "__main__":
    main()
