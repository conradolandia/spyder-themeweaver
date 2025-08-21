# 🎨 ThemeWeaver

ThemeWeaver is a Python tool (in progress) for generating and exporting themes for the Spyder IDE with QDarkStyle integration. It provides a flexible framework for creating consistent color schemes across different theme variants (dark/light) and exporting them in multiple formats.

## ✨ What it does

- **Theme Generation**: Creates Spyder-compatible themes from YAML configuration files
- **Multi-format Export**: Exports themes for both Spyder IDE and QDarkStyle formats
- **Color System Management**: Provides advanced color utilities and palette generation
- **Variant Support**: Handles dark and light theme variants from a single configuration
- **CLI Interface**: Command-line tools for theme management and validation

## 💻 CLI Usage

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

## 🖼️ Theme Preview

ThemeWeaver includes a Qt-based theme preview application that allows you to visually test and compare generated themes:

```bash
# First, export themes to the build directory
pixi run python -m themeweaver.cli export --all

# Then launch the theme preview
python scripts/theme_preview.py
```

**📋 Prerequisites**: PyQt5 must be installed to run the preview application (`pip install PyQt5`).

## 🧪 Development Tools

ThemeWeaver includes several development and utility scripts:

### 🌈 Color Utilities
```bash
# Interpolate between colors with various methods
python -m themeweaver.color_utils.interpolate_colors '#002B36' '#EEE8D5' 16 --method lch

# Generate Spyder-compatible color palettes
python -m themeweaver.color_utils.interpolate_colors '#002B36' '#EEE8D5' --spyder --method lch

# Generate color palettes
# Optimal distinguishability for variable explorer
python -m themeweaver.cli palette --method optimal --num-colors 12

# Generate from a specific color using golden ratio
python -m themeweaver.cli palette --from-color "#FF5500" --num-colors 12

# Perceptual spacing with custom Delta E
python -m themeweaver.cli palette --method perceptual --target-delta-e 30
```

### Theme Generation
```bash
# Generate a theme from individual colors (6 colors required)
pixi run python -m themeweaver.cli generate my_theme \
  --colors "#1A72BB" "#FF5500" "#E11C1C" "#00AA55" "#FF9900" "#8844EE" \
  --display-name "My Custom Theme" \
  --description "A theme generated from individual colors" \
  --author "Your Name" \
  --tags "custom,blue,modern"
```

## 📦 Installation

This project uses [Pixi](https://pixi.sh/) for dependency management:

```bash
# Install dependencies
pixi install

# Run CLI
pixi run python -m themeweaver.cli --help
```

## 🔗 Dependencies

- **QDarkStyle** (>=3.2.3) - Qt styling framework
- **PyQt5** - Qt bindings for the preview application
- **PyYAML** - YAML configuration parsing
- **colorspacious** - Color space calculations
- **qtsass** - Qt SASS compilation

## 🚀 Development

- **Python 3.12+** required
- Uses Ruff for linting and formatting
- Comprehensive test suite with pytest
- Modular architecture with clean separation of concerns
- Pre-commit hooks for code quality

```bash
# Lint code
pixi run lint

# Format code
pixi run format

# Run tests
pixi run test

# Run tests with coverage
pixi run test-cov

# Setup pre-commit hooks
pixi run pre-commit-install

# Run pre-commit on all files
pixi run pre-commit-run

# Update pre-commit hooks
pixi run pre-commit-update

# Run development scripts
python scripts/theme_preview.py
python scripts/inspect_theme_objects.py
```
