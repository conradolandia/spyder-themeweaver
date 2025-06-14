# Themeweaver Color Utils

A comprehensive color manipulation, generation, and analysis toolkit for creating perceptually uniform color palettes using scientifically sound methods.

## 🎨 Overview

The `color_utils` package provides a complete suite of tools for working with colors in theme development, with a focus on:

- **Perceptually uniform color generation** using LCH color space
- **Scientific color analysis** with Delta E perceptual distance calculations
- **Famous palette analysis** for understanding design principles
- **Flexible palette loading** from various sources
- **Command-line utilities** for practical color workflow

## 📦 Installation & Dependencies

### Required Dependencies
```bash
pip install colorspacious  # For LCH color space calculations (requires numpy)
```

## 🛠️ Available Modules

### 1. **Core Color Utilities** (`color_utils.py`)

Essential color conversion and manipulation functions.

#### Functions:
- `hex_to_rgb(hex_color)` - Convert hex to RGB
- `rgb_to_hex(rgb)` - Convert RGB to hex
- `rgb_to_hsv(rgb)` - Convert RGB to HSV
- `hsv_to_rgb(hsv)` - Convert HSV to RGB
- `rgb_to_lch(rgb)` - Convert RGB to LCH color space
- `lch_to_hex(lightness, chroma, hue)` - Convert LCH to hex
- `calculate_delta_e(color1, color2)` - Calculate perceptual distance
- `get_color_info(hex_color)` - Get comprehensive color information
- `linear_interpolate(start, end, factor)` - Linear interpolation between two values

#### Example:
```python
from themeweaver.color_utils import hex_to_rgb, rgb_to_lch, calculate_delta_e

# Convert and analyze colors
rgb = hex_to_rgb("#ff0000")
lightness, chroma, hue = rgb_to_lch(rgb)
distance = calculate_delta_e("#ff0000", "#00ff00")
```

### 2. **Color Generation** (`color_generation.py`)

Advanced algorithms for generating perceptually uniform color palettes.

#### Functions:
- `generate_theme_optimized_colors(theme, num_colors, target_delta_e, start_hue)`

#### Parameters:
- `theme`: "dark" or "light" - optimizes for background type
- `num_colors`: Number of colors to generate (default: 12)
- `target_delta_e`: Target perceptual distance between colors (default: 25)
- `start_hue`: Starting hue in degrees (default: auto)

#### Example:
```python
from themeweaver.color_utils import generate_theme_optimized_colors

# Generate 8 colors optimized for dark themes
colors = generate_theme_optimized_colors(
    theme="dark",
    num_colors=8,
    target_delta_e=25,
    start_hue=30
)
```

### 3. **Color Analysis** (`color_analysis.py`)

Comprehensive tools for analyzing existing color palettes and groups.

#### Core Analysis Functions:
- `analyze_existing_colors(colors, group_name)` - Analyze color characteristics
- `analyze_chromatic_distances(colors, group_name)` - Analyze perceptual spacing
- `print_color_analysis(color_groups, group_names)` - Print detailed analysis

#### Palette Analysis Functions:
- `analyze_palette_lch(palette_data)` - Analyze palette in LCH space
- `find_optimal_parameters(palette_data, max_colors)` - Find optimal generation parameters
- `compare_with_generated(palette_data, theme)` - Compare with generated colors
- `generate_inspired_palette(palette_data, theme)` - Generate inspired variations

#### File Loading:
- `load_color_groups_from_file(file_path)` - Load color groups from Python files
- `extract_colors_from_group(color_group_dict)` - Extract colors from group

#### Example:
```python
from themeweaver.color_utils import analyze_palette_lch, find_optimal_parameters

palette = {
    'name': 'My Palette',
    'colors': {'red': '#ff0000', 'green': '#00ff00', 'blue': '#0000ff'}
}

# Analyze the palette
analysis = analyze_palette_lch(palette)
best_params, distance = find_optimal_parameters(palette)
```

### 4. **Famous Palettes** (`famous_palettes.py`)

Curated collection of well-known color palettes for reference and analysis.

#### Available Palettes:
- **Solarized** - Precision colors for machines and people
- **Material Design** - Google's design language colors
- **Dracula** - Dark theme for developers
- **Nord** - Arctic, north-bluish color palette

#### Functions:
- `get_palette_names()` - List all available palette names
- `get_palette(name)` - Get specific palette by name
- `get_all_palettes()` - Get all palettes
- `FAMOUS_PALETTES` - Direct access to palette dictionary

#### Example:
```python
from themeweaver.color_utils import get_palette, get_palette_names

# List available palettes
names = get_palette_names()  # ['solarized', 'material', 'dracula', 'nord']

# Get specific palette
solarized = get_palette('solarized')
print(solarized['colors']['blue'])  # '#268bd2'
```

### 5. **Palette Loaders** (`palette_loaders.py`)

Flexible utilities for loading palettes from various sources with intelligent format detection.

#### Functions:
- `load_palette_from_file(file_path)` - Load from Python, YAML, or JSON files
- `get_available_color_groups(file_path)` - List available color groups in a file
- `parse_palette_from_args(colors_arg)` - Parse from command line arguments
- `validate_palette_data(palette_data)` - Validate palette structure

#### Supported Formats:
- **YAML files** with nested color groups (Primary: {B10: "#color", ...})
- **Python files** with color group classes
- **JSON files** with color dictionaries
- **Command line** color definitions

#### Example:
```python
from themeweaver.color_utils import load_palette_from_file, get_available_color_groups

# Load from YAML color system file
palette = load_palette_from_file('colorsystem.yaml')

# Check what color groups are available
groups = get_available_color_groups('colorsystem.yaml')
# Returns: ['Primary', 'Secondary', 'Green', 'Red', ...]

# Load from JSON file
palette = load_palette_from_file('my_colors.json')

# Parse from command line style
from themeweaver.color_utils import parse_palette_from_args
palette = parse_palette_from_args(['red=#ff0000', 'blue=#0000ff'])
```

### 6. **Color Interpolation** (`interpolate_colors.py`)

Advanced color interpolation and gradient generation.

#### Functions:
- Various interpolation methods between colors
- Gradient generation utilities
- Smooth color transitions

## 🖥️ Command Line Tools

### 1. **Palette Analyzer** (`analyze_palette.py`)

Comprehensive palette analysis and parameter optimization tool.

#### Usage:
```bash
# Analyze famous palettes
python -m themeweaver.color_utils.analyze_palette solarized
python -m themeweaver.color_utils.analyze_palette material --compare --generate

# Analyze custom colors
python -m themeweaver.color_utils.analyze_palette --colors 'red=#ff0000' 'blue=#0000ff'

# Analyze from file
python -m themeweaver.color_utils.analyze_palette --file my_palette.json
```

#### Options:
- `--compare` - Compare with current generation algorithms
- `--generate` - Generate inspired palette variations
- `--theme {dark,light}` - Specify theme for generation
- `--max-colors N` - Limit colors for parameter testing

### 2. **Group Generator** (`generate_groups.py`)

Generate color groups with scientific spacing.

#### Usage:
```bash
# Generate with defaults
python -m themeweaver.color_utils.generate_groups

# Customize parameters
python -m themeweaver.color_utils.generate_groups --target-delta-e 30 --start-hue 45
```

## 📊 Analysis Output Examples

### Palette Analysis
```
=== SOLARIZED ANALYSIS ===

Color        Hex      L      C      H     
--------------------------------------------------
yellow       #b58900  59.6  65.0  84.1
orange       #cb4b16  49.2  72.5  47.9
red          #dc322f  49.1  77.3  34.1
...

--- SOLARIZED CHARACTERISTICS ---
Colors: 8
Lightness: min=49.1, max=60.1, avg=54.2
Chroma: min=34.2, max=77.3, avg=59.4
Hue range: 34.1° to 354.9°
```

### Parameter Optimization
```
=== FINDING OPTIMAL PARAMETERS ===

TARGET PALETTE AVERAGES:
  Lightness: 54.2
  Chroma: 59.4
  Start hue: 34.1°

--- TESTING PARAMETERS ---
ΔE=15, start_hue=34° → avg distance: 28.3
ΔE=20, start_hue=34° → avg distance: 19.9
ΔE=25, start_hue=34° → avg distance: 18.6  ← BEST

BEST PARAMETERS for Solarized-like palette:
  {'target_delta_e': 25, 'start_hue': 34}
```

## 🔬 Scientific Background

### LCH Color Space
The package uses **LCH (Lightness, Chroma, Hue)** color space for perceptually uniform color generation:
- **Lightness**: Perceived brightness (0-100)
- **Chroma**: Color intensity/saturation (0-150+)
- **Hue**: Color angle (0-360°)

### Delta E (ΔE)
Perceptual color difference measurement:
- **ΔE < 1**: Not perceptible by human eyes
- **ΔE 1-3**: Perceptible through close observation
- **ΔE 3-5**: Perceptible at a glance
- **ΔE 5-10**: Colors are more similar than opposite
- **ΔE > 10**: Colors are more different than similar

### Optimal Spacing
The package targets **ΔE ≈ 25** for theme colors, providing:
- Clear visual distinction between colors
- Consistent perceptual spacing
- Optimal readability and accessibility

## 🎯 Use Cases

### Theme Development
```python
# Generate consistent color groups for themes
from themeweaver.color_utils import generate_theme_optimized_colors

dark_colors = generate_theme_optimized_colors(theme="dark", num_colors=12)
light_colors = generate_theme_optimized_colors(theme="light", num_colors=12)
```

### Palette Analysis
```python
# Analyze existing brand colors
from themeweaver.color_utils import analyze_palette_lch

brand_palette = {
    'name': 'Brand Colors',
    'colors': {'primary': '#1e3a8a', 'secondary': '#10b981', 'accent': '#f59e0b'}
}

analysis = analyze_palette_lch(brand_palette)
```

### Color Validation
```python
# Ensure sufficient contrast between colors
from themeweaver.color_utils import calculate_delta_e

contrast = calculate_delta_e('#1e3a8a', '#10b981')
if contrast < 10:
    print("⚠️ Colors may be too similar")
```

## 🤝 Contributing

The color_utils package is designed to be extensible:

1. **Add new famous palettes** to `famous_palettes.py`
2. **Implement new color spaces** in `color_utils.py`
3. **Create analysis methods** in `color_analysis.py`
4. **Add generation algorithms** in `color_generation.py`

## 📚 API Reference

For detailed API documentation, refer to the docstrings in each module or use Python's built-in help:

```python
import themeweaver.color_utils as cu
help(cu.generate_theme_optimized_colors)
```

---

*This package provides the foundation for scientifically-grounded color palette generation and analysis, enabling developers and designers to create visually consistent and accessible themes.* 
