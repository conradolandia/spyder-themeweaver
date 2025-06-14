# Spyder ThemeWeaver

A tool to create and export themes for the Spyder IDE

## Objectives

- The application should basically create themes for spyder using QDarkStyle's engine, generating a folder with a Python file with the expected classes and a subfolder with required assets from QDarkStyle.
  - We will use the scripts `qdarkstyle/utils/__main__.py` and `qdarkstyle/utils/__init__.py` from QDarkStyle as examples for a starting point for asset generation
  - We will use ThemeWeaver's color utilities to generate te required gradients and color groups: 
    - From a single color, calculate its darkest and lightest viable shades, and generate possible interpolations (using `src/themeweaver/color_utils/interpolate_colors.py`)
    - Or, alternatively, we can provide a darkest color, a lightest color, and interpolate them with the same methods
  - We will create and use the class Theme from `src/themeweaver/theme.py` which will generate required assets using the selected colors, copy the required files and pack the theme
- Create color themes: Solarized (done), Dracula, Gruvbox, Monokai, Obsidian, Retta, Zenburn, Spyder (current theme)
- Create a visual map in SVG to match all color instances to where they are used in the UI, for users and developers
- Create a tool to help users create their own themes, with a QT user interface that displays the color theme being edited and a sample of UI elements that can be used as a preview (could be real UI elements or just a graphic simulation in SVG)
