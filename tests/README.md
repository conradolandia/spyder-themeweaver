# ThemeWeaver Test Suite

## Overview

This directory contains a comprehensive test suite for ThemeWeaver, covering all major components of the theme generation and export system.

## Test Structure

### Integration Tests
- **`test_exporter.py`** - Complete theme export pipeline testing
  - ThemeExporter initialization and configuration
  - Theme discovery and validation
  - Export functionality (single themes, all themes, specific variants)
  - File structure validation
  - Error handling

### Core System Tests
- **`test_colorsystem.py`** - Core color system functionality (45 tests)
  - YAML color loading and validation
  - Dynamic color class creation
  - Theme metadata handling
  - Semantic color mappings
  - Palette integration and containers
  - Error handling and edge cases

### Color Utilities Tests
- **`test_color_utils.py`** - Color manipulation and analysis utilities (13 tests)
  - Color space conversions (RGB, HSV, LCH)
  - Theme-optimized color generation
  - Palette analysis and validation
  - Chromatic distance calculations
  - Common palette access

## Running Tests

### All tests
```bash
python -m pytest tests/ -v
```

### Specific test modules
```bash
python -m pytest tests/test_exporter.py -v
python -m pytest tests/test_colorsystem.py -v
python -m pytest tests/test_color_utils.py -v
```

### With coverage
```bash
python -m pytest tests/ --cov=src/themeweaver --cov-report=html
```

## Test Coverage

- **Total Tests:** 66 tests
- **Core System:** 45 tests (colorsystem)
- **Color Utilities:** 13 tests (color_utils)
- **Integration:** 8 tests (exporter)

## Dependencies

- Python 3.11+
- pytest >=8.4.0
- PyYAML >=6.0.2
- colorspacious >=1.1.2 (for LCH color space and Delta E calculations)
- qdarkstyle (for integration tests)

## Test Data

Tests use the actual theme configuration files from `src/themeweaver/themes/`:
- `solarized/` - Primary test theme
- `dracula/` - Secondary test theme

Each theme includes:
- `theme.yaml` - Theme metadata
- `colorsystem.yaml` - Color definitions
- `mappings.yaml` - Semantic color mappings
