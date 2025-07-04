# ThemeWeaver Theme Generator

The ThemeWeaver Theme Generator is a powerful CLI tool for creating new Spyder themes using advanced color science algorithms. It leverages the existing color utilities from themeweaver to generate complete theme definition files.

## Features

- 🎨 **Two Generation Methods**: Create themes from specific colors or use algorithmic generation
- 🔬 **Perceptually Uniform Colors**: Uses LCH color space for scientifically sound color palettes
- 🎯 **Multiple Interpolation Methods**: Linear, cubic, exponential, sine, cosine, hermite, quintic, HSV, and LCH
- 🏷️ **Creative Color Names**: Automatically generates creative names for color palettes
- 📦 **Complete Theme Files**: Generates all three required YAML files (theme.yaml, colorsystem.yaml, mappings.yaml)
- ✅ **Validation**: Built-in validation of generated themes

## Usage

### Basic Command Structure

```bash
themeweaver generate THEME_NAME [options]
```

### Method 1: Generate from Specific Colors

Generate a theme from four specific colors (primary dark, primary light, secondary dark, secondary light):

```bash
themeweaver generate ocean_blue \
  --colors "#002B36" "#EEE8D5" "#268BD2" "#FDF6E3" \
  --display-name "Ocean Blue" \
  --description "A calming ocean-inspired theme" \
  --author "Your Name" \
  --tags "blue,ocean,calm" \
  --method lch
```

### Method 2: Algorithmic Generation

Generate a theme using algorithmic color generation:

```bash
themeweaver generate sunset_warm \
  --palette-name "SunsetWarm" \
  --start-hue 20 \
  --num-colors 12 \
  --target-delta-e 25 \
  --display-name "Sunset Warm" \
  --description "A warm sunset-inspired theme" \
  --author "Your Name" \
  --tags "warm,sunset,orange"
```

### Method 3: Uniform Hue Distribution

Generate a theme with uniform hue steps:

```bash
themeweaver generate rainbow_uniform \
  --palette-name "RainbowUniform" \
  --start-hue 0 \
  --num-colors 8 \
  --uniform \
  --display-name "Rainbow Uniform" \
  --description "A theme with uniform hue distribution"
```

## Options

### Generation Methods

- `--colors PRIMARY_DARK PRIMARY_LIGHT SECONDARY_DARK SECONDARY_LIGHT`: Generate from specific colors
- `--palette-name NAME`: Name for the primary palette (used with algorithmic generation)

### Algorithmic Generation Options

- `--start-hue HUE`: Starting hue for color generation (0-360)
- `--num-colors N`: Number of colors in group palettes (default: 12)
- `--target-delta-e VALUE`: Target perceptual distance between colors (default: 25)
- `--uniform`: Use uniform hue steps instead of perceptual spacing

### Color Interpolation Method

- `--method METHOD`: Choose from:
  - **RGB-based**: `linear`, `cubic`, `exponential`, `sine`, `cosine`, `hermite`, `quintic`
  - **Color space**: `hsv`, `lch` (recommended for perceptual uniformity)

### Theme Metadata

- `--display-name NAME`: Human-readable theme name
- `--description TEXT`: Theme description
- `--author NAME`: Theme author (default: ThemeWeaver)
- `--tags TAGS`: Comma-separated list of tags

### Options

- `--simple-names`: Use simple color names instead of creative names
- `--overwrite`: Overwrite existing theme if it exists

## Examples

### Example 1: Solarized-inspired Theme

```bash
themeweaver generate solarized_custom \
  --colors "#002B36" "#FDF6E3" "#268BD2" "#DC322F" \
  --display-name "Solarized Custom" \
  --description "Custom variation of the Solarized theme" \
  --author "Ethan Schoonover" \
  --tags "solarized,low-contrast,professional" \
  --method lch
```

### Example 2: Material Design Theme

```bash
themeweaver generate material_indigo \
  --palette-name "MaterialIndigo" \
  --start-hue 231 \
  --num-colors 12 \
  --target-delta-e 30 \
  --display-name "Material Indigo" \
  --description "Inspired by Material Design indigo colors" \
  --tags "material,indigo,modern"
```

### Example 3: Warm Autumn Theme

```bash
themeweaver generate autumn_warm \
  --colors "#8B4513" "#FFF8DC" "#FF8C00" "#FFFACD" \
  --display-name "Autumn Warm" \
  --description "Warm autumn colors for cozy coding" \
  --author "Nature Lover" \
  --tags "autumn,warm,cozy" \
  --method cubic
```

### Example 4: High Contrast Theme

```bash
themeweaver generate high_contrast \
  --colors "#000000" "#FFFFFF" "#FF0000" "#00FF00" \
  --display-name "High Contrast" \
  --description "High contrast theme for accessibility" \
  --tags "accessibility,high-contrast" \
  --method linear \
  --simple-names
```

## Color Science Background

### LCH Color Space

The theme generator uses the LCH (Lightness, Chroma, Hue) color space for perceptually uniform color generation. This ensures that:

- Colors with the same Delta E distance appear equally different to the human eye
- Smooth color transitions that avoid "muddy" intermediate colors
- Scientifically sound color palettes

### Delta E Distance

Delta E is a metric for measuring perceptual color differences:

- **Delta E < 1**: Colors appear identical
- **Delta E 1-3**: Colors are perceptually close
- **Delta E 3-5**: Colors are noticeably different
- **Delta E > 5**: Colors are clearly different

The default target Delta E of 25 ensures clearly distinguishable colors in the palette.

### Interpolation Methods

Different interpolation methods provide different aesthetic results:

- **Linear**: Straight-line interpolation (fastest)
- **Cubic**: Smooth acceleration/deceleration
- **LCH**: Perceptually uniform (recommended)
- **HSV**: Avoids "muddy" colors in RGB space
- **Exponential/Sine/Cosine**: Various easing curves

## Generated Files

The theme generator creates three files in `src/themeweaver/themes/THEME_NAME/`:

### 1. theme.yaml
Contains theme metadata:
```yaml
name: "ocean_blue"
display_name: "Ocean Blue"
description: "A calming ocean-inspired theme"
author: "Your Name"
version: "1.0.0"
license: "MIT"
tags: ["blue", "ocean", "calm"]
variants:
  dark: true
  light: true
```

### 2. colorsystem.yaml
Contains color palettes with creative names:
```yaml
AquaticNavy:
  B0: "#000000"
  B10: "#002B36"
  B20: "#1A4A5C"
  # ... more colors
  B150: "#FFFFFF"

BrilliantCerulean:
  B0: "#000000"
  B10: "#268BD2"
  # ... more colors
  B150: "#FFFFFF"

# Standard palettes (Green, Red, Orange, GroupDark, GroupLight, Logos)
```

### 3. mappings.yaml
Maps semantic UI element names to color palette references:
```yaml
color_classes:
  Primary: "AquaticNavy"
  Secondary: "BrilliantCerulean"
  Green: "Green"
  # ... more mappings

semantic_mappings:
  dark:
    COLOR_BACKGROUND_1: "Primary.B10"
    COLOR_TEXT_1: "Primary.B130"
    COLOR_ACCENT_1: "Secondary.B20"
    # ... more mappings
```

## Validation and Testing

After generating a theme, you can validate it:

```bash
# Validate the theme
themeweaver validate ocean_blue

# List all themes
themeweaver list

# Export the theme
themeweaver export --theme ocean_blue
```

## Integration with Existing Tools

The theme generator integrates seamlessly with the existing themeweaver color utilities:

- Uses `generate_groups.py` for group palette generation
- Uses `interpolate_colors.py` for color interpolation
- Uses `color_names.py` for creative palette naming
- Leverages all existing color analysis and generation algorithms

## Tips for Best Results

1. **Use LCH method** for perceptually uniform colors
2. **Start with complementary colors** for primary/secondary palettes
3. **Test Delta E values** between 20-35 for good color separation
4. **Use creative names** for memorable palette identifiers
5. **Validate themes** before using them in production
6. **Consider accessibility** when choosing colors

## Advanced Usage

### Custom Color Validation

The generator automatically validates that dark colors are actually dark and light colors are actually light. This prevents common mistakes like swapping colors.

### Creative vs Simple Names

- **Creative names**: "AquaticNavy", "BrilliantCerulean" (default)
- **Simple names**: "Navy", "Blue" (with --simple-names flag)

### Overwriting Themes

Use the `--overwrite` flag to replace existing themes. The generator will warn you if a theme already exists.

### Batch Generation

You can create scripts to generate multiple themes at once using the Python API:

```python
from themeweaver.core.theme_generator import ThemeGenerator

generator = ThemeGenerator()

# Generate multiple themes
themes = [
    ("ocean_blue", ("#002B36", "#EEE8D5"), ("#268BD2", "#FDF6E3")),
    ("forest_green", ("#0F2027", "#F8F8FF"), ("#2E8B57", "#F0FFF0")),
    # ... more themes
]

for name, primary, secondary in themes:
    generator.generate_theme_from_colors(
        theme_name=name,
        primary_colors=primary,
        secondary_colors=secondary,
        method="lch",
        overwrite=True
    )
```

## Troubleshooting

### Common Issues

1. **"Theme already exists"**: Use `--overwrite` to replace existing themes
2. **"Invalid colors"**: Ensure hex colors are valid and dark/light colors are properly ordered
3. **"Color conversion failed"**: Some extreme colors may not convert properly between color spaces
4. **"Missing dependencies"**: Ensure all required packages are installed

### Getting Help

```bash
# Show help for the generate command
themeweaver generate --help

# Show general help
themeweaver --help
```

## Contributing

The theme generator is part of the themeweaver project. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

The theme generator is released under the MIT License, same as the rest of the themeweaver project. 