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

### `theme_preview.py`
Qt application for previewing and testing generated themes visually.

**Usage:**
```bash
python scripts/theme_preview.py
```

**Prerequisites:**
- PyQt5 installed (`pip install PyQt5`)
- Themes exported to the `build/` directory

**What it does:**
- Loads generated themes from the build directory
- Allows switching between themes and variants (dark/light) in real-time
- Shows how themes look with buttons, inputs, tables, trees, text editors, etc.
- Uses system standard icons for UI elements

**Features:**
- **Theme Selector**: Dropdown with theme icons to choose from available themes and variants
- **System Icons**: Uses Qt's built-in standard icons for consistent appearance
- **Widget Showcase**: Comprehensive display of Qt widgets including:
  - Buttons (enabled/disabled states)
  - Input fields (text, numbers, dropdowns with icons)
  - Selection controls (checkboxes, radio buttons)
  - Progress bars and sliders
  - Text editor with sample Python code
  - Lists, trees, and tables
  - Menu bar and toolbar
- **Live Preview**: Instant theme switching without restart
- **Status Updates**: Real-time feedback about theme loading

**Icon System:**
- **System Icons**: Uses Qt's standard system icons for consistent cross-platform appearance
- **Theme Icons**: Desktop/computer icons for theme selection
- **Variant Icons**: Play/stop icons for dark/light variants
- **Check Icons**: Apply button icons for dropdown selections

**Useful for:**
- Visual testing of generated themes
- Comparing theme variants side-by-side
- Validating theme appearance across different widget types
- Testing system icon integration with themes
- Quality assurance before theme distribution
- Demonstrating themes to stakeholders

## Adding New Scripts

When adding new development scripts:
1. Place them in this directory
2. Add a description in this README
3. Use the same import pattern as existing scripts
4. Include usage examples 

## Running Scripts

All scripts should be run from the project root directory:

```bash
# From the themeweaver root directory
python scripts/script_name.py
```

Or you can run them directly if you have the proper Python path set up:

```bash
# Make sure PYTHONPATH includes the src directory
export PYTHONPATH=/path/to/themeweaver/src:$PYTHONPATH
python scripts/script_name.py
``` 
