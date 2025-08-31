# 🎨 ThemeWeaver

ThemeWeaver is a Python tool to generate and export themes for the Spyder IDE with QDarkStyle integration. It provides a flexible framework for creating consistent color schemes across different theme variants (dark/light) and export QT assets based on them. It also provides files to integrate the themes with Spyder.

## 📦 Project Setup

This project uses [Pixi](https://pixi.sh/) for dependency management and task automation. All commands are defined in `pyproject.toml` and should be run with `pixi run`.

### Prerequisites
- [Pixi](https://pixi.sh/) installed on your system
- Python 3.12+ (managed by pixi)

### Installation

```bash
# Install dependencies (includes QDarkStyle develop branch)
pixi install

# Verify installation
pixi run python --version
```

## 🚀 Quick Start

### List Available Themes
```bash
pixi run list-themes
```

### Export a Theme
```bash
# Export all variants of a theme
pixi run export qdarkstyle

# Export specific variants only
pixi run export-light qdarkstyle
pixi run export-dark qdarkstyle

# Export all themes
pixi run export-all
```

### Package Themes for Distribution
```bash
# Package a single theme (ZIP format)
pixi run package --theme dracula

# Package a theme in TAR.GZ format
pixi run package --theme solarized --format tar.gz

# Package a theme as uncompressed folder
pixi run package --theme gruvbox --format folder

# Package all exported themes
pixi run package

# Package with custom output directory
pixi run package --theme gruvbox --output ~/.config/spyder-py3/themes
```

### Preview Themes
```bash
# First export themes
pixi run export-all

# Then launch the preview application
pixi run preview
```

### Generate Themes
```bash
# Generate a new Spyder-compatible theme from colors
pixi run generate my_theme \
  --colors "#1A72BB" "#FF5500" "#E11C1C" "#00AA55" "#FF9900" "#8844EE" \
  --display-name "My Custom Theme" \
  --description "A theme generated from individual colors" \
  --author "Your Name" \
  --tags "custom,blue,modern"
```

## 💻 CLI Commands

ThemeWeaver provides a comprehensive command-line interface. All commands are available through pixi tasks:

### Theme Management
```bash
# List all available themes
pixi run list-themes

# Show detailed theme information
pixi run theme-info solarized

# Validate theme configuration
pixi run validate solarized

# Generate a new Spyder-compatible theme from colors
# Color order: Primary, Secondary, Error, Success, Warning, Group
pixi run generate my_theme \
  --colors "#1e1e2e" "#b4befe" "#f38ba8" "#a6e3a1" "#fab387" "#eba0ac"  \
  --display-name "My Custom Theme" \
  --description "A theme generated from individual colors" \
  --author "Your Name" \
  --tags "custom,blue,modern"
```

### Color Utilities
```bash
# Generate color palettes
pixi run palette --method optimal --num-colors 12
pixi run palette --from-color "#FF5500" --num-colors 12
pixi run palette --method perceptual --target-delta-e 30

# Interpolate between colors
pixi run interpolate "#002B36" "#EEE8D5" 16
pixi run interpolate-lch "#002B36" "#EEE8D5" 16
pixi run interpolate-hsv "#002B36" "#EEE8D5" 16
```

### Direct CLI Access
For advanced usage, you can also access the CLI directly:
```bash
pixi run cli --help
pixi run cli export --help
pixi run cli generate --help
```

## 🖼️ Theme Preview

ThemeWeaver includes a Qt-based theme preview application for visual testing and comparison:

```bash
# Export themes first
pixi run export-all

# Launch preview application
pixi run preview
```

The preview application requires PyQt5, which is included in the pixi environment.

## 🔧 Development

### Code Quality
```bash
# Lint code
pixi run lint

# Format code
pixi run format

# Fix linting issues automatically
pixi run lint-fix

# Run all checks
pixi run check
```

### Testing
```bash
# Run tests
pixi run test

# Run tests with coverage
pixi run test-cov

# View coverage report
pixi run inspect-cov # Then, open your browser and point it to localhost:8000
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pixi run pre-commit-install

# Run pre-commit on all files
pixi run pre-commit-run

# Update pre-commit hooks
pixi run pre-commit-update
```

## 📋 Available Tasks

All available pixi tasks are defined in `pyproject.toml`:

| Task | Description |
|------|-------------|
| `lint` | Check code with ruff |
| `format` | Format code with ruff |
| `lint-fix` | Fix linting issues automatically |
| `check` | Run all code quality checks |
| `cli` | Access the main CLI |
| `export` | Export a specific theme |
| `export-light` | Export light variant of a theme |
| `export-dark` | Export dark variant of a theme |
| `export-all` | Export all themes |
| `package` | Package exported themes |
| `package-all` | Package all exported themes |
| `list-themes` | List available themes |
| `theme-info` | Show theme information |
| `generate` | Generate a new theme |
| `validate` | Validate theme configuration |
| `interpolate` | Interpolate between colors |
| `interpolate-lch` | Interpolate using LCH method |
| `interpolate-hsv` | Interpolate using HSV method |
| `palette` | Generate color palettes |
| `preview` | Launch theme preview application |
| `test` | Run tests |
| `test-cov` | Run tests with coverage |
| `inspect-cov` | View coverage report |
| `pre-commit-install` | Install pre-commit hooks |
| `pre-commit-run` | Run pre-commit on all files |
| `pre-commit-update` | Update pre-commit hooks |

## 🔗 Dependencies

ThemeWeaver uses the following key dependencies (managed by pixi):

- **Python 3.12** - Runtime environment
- **QDarkStyle** - Qt styling framework (development version)
- **PyQt5** - Qt bindings for preview application
- **PyYAML** - YAML configuration parsing
- **colorspacious** - Color space calculations
- **qtsass** - Qt SASS compilation
- **ruff** - Code linting and formatting
- **pytest** - Testing framework

**Note:** QDarkStyle is currently using the `develop` branch which provides additional CLI functionality not available in the released version. This dependency will be updated to use the released version once QDarkStyle publishes the new API.

## 🏗️ Project Structure

```
themeweaver/
├── src/themeweaver/          # Main package
│   ├── cli/                  # Command-line interface
│   ├── core/                 # Core functionality
│   ├── color_utils/          # Color utilities
│   └── themes/               # Theme definitions
├── scripts/                  # Utility scripts
│   └── preview/              # Theme preview application
├── tests/                    # Test suite
├── pyproject.toml           # Project configuration and tasks
└── README.md                # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your functions
5. Run code quality checks: `pixi run check`
6. Run tests: `pixi run test`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
