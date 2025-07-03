# ThemeWeaver Development Scripts

This directory contains development and debugging scripts for ThemeWeaver.

## Scripts

### `inspect_theme_objects.py`
Development script for inspecting theme objects and their internal structure.

**Usage:**
```bash
python scripts/inspect_theme_objects.py
```

**What it does:**
- Creates theme instances with dynamically generated palettes
- Inspects internal structure of Theme and ThemePalettes objects
- Shows color attributes from dark and light palettes
- Displays inheritance information
- Compares with original QDarkStyle palettes

**Useful for:**
- Debugging theme creation issues
- Understanding object structure
- Verifying color generation
- Development and troubleshooting

## Adding New Scripts

When adding new development scripts:
1. Place them in this directory
2. Add a description in this README
3. Use the same import pattern as existing scripts
4. Include usage examples 
