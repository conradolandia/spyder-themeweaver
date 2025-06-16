# Themeweaver Test Suite

## Overview

This directory contains a comprehensive and simplified test suite for the themeweaver color utilities. 

## Test Files

### `test_color_utils.py`

- **TestColorUtils**: Core color conversion and manipulation functions
- **TestColorGeneration**: Theme-optimized color generation
- **TestFamousPalettes**: Famous palette access and management
- **TestPaletteLoaders**: Palette loading and validation
- **TestCoreModules**: Core themeweaver modules (colorsystem, theme, palette)
- **TestColorAnalysis**: Color analysis and distance calculations

## Running Tests

### Using pytest (project dependency)
```bash
python -m pytest tests/test_color_utils.py -v
```

### Direct execution (also uses pytest)
```bash
python tests/test_color_utils.py
```

## Dependencies

- Python 3.7+
- PyYAML (for YAML palette loading)
- `colorspacious` (for LCH color space and Delta E calculations)
- `pytest` (for test execution)
