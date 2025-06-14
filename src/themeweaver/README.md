# Spyder ThemeWeaver

A tool to create and export themes for the Spyder IDE

## Objectives

- Currently we have a skeleton directory as follows: 
```
  src
└── themeweaver
    ├── color_utils
    │   ├── README.md
    │   ├── __init__.py
    │   ├── analyze_palette.py
    │   ├── color_analysis.py
    │   ├── color_generation.py
    │   ├── color_utils.py
    │   ├── famous_palettes.py
    │   ├── generate_groups.py
    │   ├── interpolate_colors.py
    │   └── palette_loaders.py
    ├── themes
    ├── README.md
    ├── __init__.py
    ├── colorsystem.py
    ├── colorsystem.yaml
    ├── palette.py
    └── theme.py
pixi.lock
pyproject.toml
```
- The application should basically create themes for spyder using QDarkStyle's engine, generating a folder with a Python file with the expected classes (`palette.py`) which will load color definitions from a yaml file (`colorsystem.yaml`) using dynamic mapping functions (`colorsystem.py`), and a subfolder (`theme`) with required assets (`dark` and `light`) from QDarkStyle.
  - We will use the scripts `qdarkstyle/utils/__main__.py` and `qdarkstyle/utils/__init__.py` from QDarkStyle as examples for a starting point for asset generation
  - We will use ThemeWeaver's color utilities to generate te required gradients and color groups: 
    - From a single color, calculate its darkest and lightest viable shades, and generate possible interpolations (using `src/themeweaver/color_utils/interpolate_colors.py`)
    - Or, alternatively, we can provide a darkest color, a lightest color, and interpolate them with the same methods
  - We will create and use the class Theme from `src/themeweaver/theme.py` which will generate required assets using the selected colors, copy the required files and pack the theme
  - We will also create a new metod to generate Syntax Highlighting themes in sync with the UI themes, in a separate file
- Create color themes: Solarized (currently hardcoded but awaiting proper implementation), Dracula, Gruvbox, Monokai, Obsidian, Retta, Zenburn, QDarkStyle (currently the only UI theme available in Spyder)
- Create a visual map in SVG to match all color instances to where they are used in the UI, for users and developers
- Create a tool to help users create their own themes, with a QT user interface that displays the color theme being edited and a sample of UI elements that can be used as a preview (could be real UI elements or just a graphic simulation in SVG)
