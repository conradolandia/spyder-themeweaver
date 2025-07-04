# ThemeWeaver

ThemeWeaver is a Python tool (in progress) for generating and exporting themes for the Spyder IDE with QDarkStyle integration. It provides a flexible framework for creating consistent color schemes across different theme variants (dark/light) and exporting them in multiple formats.

## What it does

- **Theme Generation**: Creates Spyder-compatible themes from YAML configuration files
- **Multi-format Export**: Exports themes for both Spyder IDE and QDarkStyle formats
- **Color System Management**: Provides advanced color utilities and palette generation
- **Variant Support**: Handles dark and light theme variants from a single configuration
- **CLI Interface**: Command-line tools for theme management and validation

## Project Structure

### Core Components

- **`src/themeweaver/core/`** - Core functionality
  - `theme.py` - Theme class definitions
  - `palette.py` - Palette management and creation
  - `colorsystem.py` - Color system loading from YAML configs
  - `exporter.py` - Main theme export functionality
  - `spyder_generator.py` - Spyder-specific file generation
  - `qdarkstyle_exporter.py` - QDarkStyle format export
  - `theme_exporter.py` - Universal theme export interface

- **`src/themeweaver/color_utils/`** - Color manipulation utilities
  - Advanced color analysis and generation tools
  - Palette optimization and interpolation methods
  - Common color palettes and naming utilities

- **`src/themeweaver/themes/`** - Theme definitions
  - Each theme folder contains:
    - `theme.yaml` - Theme metadata and configuration
    - `colorsystem.yaml` - Color definitions and palettes
    - `mappings.yaml` - Semantic color mappings for variants

### Theme Configuration Files

Each theme uses three YAML files:

1. **`theme.yaml`** - Theme metadata (name, description, author, supported variants)
2. **`colorsystem.yaml`** - Base color definitions and color group mappings
3. **`mappings.yaml`** - Semantic mappings for dark/light variants (UI elements to colors)

**All three files are required** for theme generation. ThemeWeaver does not provide fallback mechanisms or inherit from QDarkStyle default values.

**What happens with missing files:**

- **Missing `colorsystem.yaml`**: Export fails with `FileNotFoundError: Color system YAML file not found`
- **Missing `mappings.yaml`**: Export fails with `FileNotFoundError: Color mappings YAML file not found`
- **Missing `theme.yaml`**: Export fails with `FileNotFoundError: Theme metadata YAML file not found`

This design ensures themes are self-contained and predictable. To create a minimal theme:

1. Use all three files with minimal content
2. Define basic color groups in `colorsystem.yaml`
3. Provide essential semantic mappings in `mappings.yaml`
4. Specify metadata and supported variants in `theme.yaml`

For examples, see the existing themes in `src/themeweaver/themes/`.

## Available Themes

Currently includes:
- **Dracula** - Based on the popular Dracula color palette
- **Solarized** - Based on the Solarized color scheme

## CLI Usage (not fully implemented yet)

```bash
# List all available themes
pixi run python -m themeweaver.cli list

# Show theme information
pixi run python -m themeweaver.cli info dracula

# Export a specific theme
pixi run python -m themeweaver.cli export --theme dracula

# Export all themes
pixi run python -m themeweaver.cli export --all

# Validate theme configuration
pixi run python -m themeweaver.cli validate dracula
```

## Theme Preview

ThemeWeaver includes a Qt-based theme preview application that allows you to visually test and compare generated themes:

```bash
# First, export themes to the build directory
pixi run python -m themeweaver.cli export --all

# Then launch the theme preview
python scripts/theme_preview.py
```

The preview application provides:
- **Live theme switching** between all exported themes and variants
- **Comprehensive widget showcase** including buttons, inputs, tables, text editors, etc.
- **Real-time visual feedback** to see exactly how themes look in Qt applications
- **Side-by-side comparison** capabilities for different themes and variants

This is particularly useful for:
- Quality assurance before distributing themes
- Fine-tuning color choices and contrast
- Demonstrating themes to stakeholders
- Testing accessibility and readability

**Prerequisites**: PyQt5 must be installed to run the preview application (`pip install PyQt5`).

## Installation

This project uses [Pixi](https://pixi.sh/) for dependency management:

```bash
# Install dependencies
pixi install

# Run CLI
pixi run python -m themeweaver.cli --help
```

## Dependencies

- **QDarkStyle** (>=3.2.3) - Qt styling framework
- **PyQt5** - Qt bindings for the preview application
- **PyYAML** - YAML configuration parsing
- **colorspacious** - Color space calculations
- **qtsass** - Qt SASS compilation

## Development

- **Python 3.12+** required
- Uses Ruff for linting and formatting
- Includes pytest for testing (TODO)

```bash
# Lint code
pixi run lint

# Format code  
pixi run format

# Run tests
pixi run pytest
``` 
