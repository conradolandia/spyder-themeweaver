"""
Theme loading functionality for the ThemeWeaver preview application.
"""

from pathlib import Path
from .theme_cache import theme_cache


def load_theme(theme_name, variant, status_callback=None):
    """Load the selected theme variant.

    Args:
        theme_name: Name of the theme
        variant: Theme variant ('dark' or 'light')
        status_callback: Optional callback function to display status messages

    Returns:
        tuple: (success, stylesheet) - success is a boolean indicating if loading was successful,
                                      stylesheet is the loaded QSS stylesheet or None if failed
    """
    if not theme_name or not variant:
        if status_callback:
            status_callback("No theme or variant selected")
        return False, None

    # Check cache first
    cached_stylesheet = theme_cache.get(theme_name, variant)
    if cached_stylesheet:
        if status_callback:
            status_callback(f"Loaded theme from cache: {theme_name} ({variant})")
        return True, cached_stylesheet

    # Get the build directory
    current_dir = Path(__file__).parent.parent.parent
    build_dir = current_dir / "build"

    # Look for the QSS file
    qss_file = build_dir / theme_name / variant / f"{variant}style.qss"

    if not qss_file.exists():
        if status_callback:
            status_callback(f"Theme file not found: {qss_file}")
        return False, None

    try:
        # Read the stylesheet
        with open(qss_file, "r", encoding="utf-8") as f:
            stylesheet = f.read()

        # Convert Qt resource paths to file system paths
        stylesheet = _convert_resource_paths_to_filesystem(
            stylesheet, theme_name, variant, build_dir
        )

        # Cache the stylesheet for future use
        theme_cache.set(theme_name, variant, stylesheet)

        if status_callback:
            status_callback(f"Loaded and cached theme: {theme_name} ({variant})")

        return True, stylesheet

    except Exception as e:
        if status_callback:
            status_callback(f"Error loading theme: {e}")
        return False, None


def _convert_resource_paths_to_filesystem(stylesheet, theme_name, variant, build_dir):
    """Convert Qt resource paths to file system paths in the stylesheet.

    Args:
        stylesheet: The QSS stylesheet content
        theme_name: Name of the theme
        variant: Theme variant ('dark' or 'light')
        build_dir: Build directory path

    Returns:
        str: Modified stylesheet with file system paths
    """
    import re

    # Pattern to match Qt resource paths like :/qss_icons/dark/rc/icon.png
    resource_pattern = r'url\(":/qss_icons/([^"]+)"\)'

    # Use relative paths instead of absolute paths to avoid potential issues
    # The relative path will be relative to the current working directory
    relative_path = f"build/{theme_name}/{variant}/rc"

    def replace_resource_path(match):
        resource_path = match.group(1)  # e.g., "dark/rc/icon.png"

        # Extract just the filename from the resource path
        filename = resource_path.split("/rc/")[-1]

        # Build the relative path
        rel_path = f"{relative_path}/{filename}"

        # Qt stylesheets work better with relative paths
        return f'url("{rel_path}")'

    # Replace all resource paths with file system paths
    modified_stylesheet = re.sub(resource_pattern, replace_resource_path, stylesheet)

    return modified_stylesheet


def get_available_themes():
    """Get list of available themes from the build directory.

    Returns:
        list: List of theme names
    """
    current_dir = Path(__file__).parent.parent.parent
    build_dir = current_dir / "build"

    if not build_dir.exists():
        return []

    # Find theme directories
    themes = []
    for theme_dir in build_dir.iterdir():
        if theme_dir.is_dir() and not theme_dir.name.startswith("."):
            themes.append(theme_dir.name)

    return sorted(themes)
