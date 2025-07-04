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

- **`scripts/`** - Development and utility scripts
  - `theme_preview.py` - Qt-based theme preview application
  - `inspect_theme_objects.py` - Theme development debugging tool
  - `preview/` - Modular preview application components:
    - `main.py` - Application entry point
    - `main_window.py` - Main window class
    - `theme_loader.py` - Theme loading and management
    - `ui_components.py` - Basic UI components
    - `ui_panels.py` - Complex UI panels
    - `ui_tabs.py` - Tab-based UI layout

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

## CLI Usage

ThemeWeaver provides a comprehensive command-line interface for theme management:

```bash
# List all available themes
pixi run python -m themeweaver.cli list

# Show detailed theme information
pixi run python -m themeweaver.cli info solarized

# Export a specific theme
pixi run python -m themeweaver.cli export --theme solarized

# Export only specific variants
pixi run python -m themeweaver.cli export --theme solarized --variants dark

# Export all themes
pixi run python -m themeweaver.cli export --all

# Validate theme configuration
pixi run python -m themeweaver.cli validate solarized

# Show help for any command
pixi run python -m themeweaver.cli --help
pixi run python -m themeweaver.cli export --help
```

## Theme Preview

ThemeWeaver includes a Qt-based theme preview application that allows you to visually test and compare generated themes:

```bash
# First, export themes to the build directory
pixi run python -m themeweaver.cli export --all

# Then launch the theme preview
python scripts/theme_preview.py
```

**Prerequisites**: PyQt5 must be installed to run the preview application (`pip install PyQt5`).

## Development Tools

ThemeWeaver includes several development and utility scripts:

### Theme Inspection
```bash
# Inspect internal theme object structure
python scripts/inspect_theme_objects.py
```

### Color Utilities
```bash
# Interpolate between colors with various methods
python -m themeweaver.color_utils.interpolate_colors '#002B36' '#EEE8D5' 16 --method lch

# Generate Spyder-compatible color palettes
python -m themeweaver.color_utils.interpolate_colors '#002B36' '#EEE8D5' --spyder --method lch

# Analyze existing color palettes
python -m themeweaver.color_utils.analyze_palette solarized --compare

# Generate group-style color palettes
python -m themeweaver.color_utils.generate_groups --target-delta-e 30
```

These tools are particularly useful for:
- **Theme Development**: Understanding color relationships and palette structures
- **Color Analysis**: Analyzing existing themes and finding optimal generation parameters
- **Palette Generation**: Creating new color schemes with perceptually uniform spacing
- **Quality Assurance**: Validating theme consistency and visual harmony

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
- Comprehensive test suite with pytest
- Modular architecture with clean separation of concerns

```bash
# Lint code
pixi run lint

# Format code  
pixi run format

# Run tests
pixi run pytest

# Run development scripts
python scripts/theme_preview.py
python scripts/inspect_theme_objects.py
```

### Project Organization

The project follows a clean modular architecture:
- **Core modules** (`src/themeweaver/core/`) handle theme generation and export
- **Color utilities** (`src/themeweaver/color_utils/`) provide advanced color manipulation
- **Theme definitions** (`src/themeweaver/themes/`) contain reusable theme configurations
- **Development scripts** (`scripts/`) offer debugging and preview tools
- **Test suite** (`tests/`) ensures code quality and functionality 
