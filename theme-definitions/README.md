# Theme Definitions

This directory contains theme definitions in YAML format for ThemeWeaver. These definitions allow creating complete themes without the need to specify all parameters in the command line.

## Usage

To generate a theme from a YAML file, use the following command:

```bash
pixi run generate theme-name --from-yaml /path/to/file.yaml
```

Where:
- `theme-name` is the name that will be used for the theme directory
- `--from-yaml` specifies the path to the YAML file with the theme definition

## YAML File Structure

Theme definition YAML files have the following structure:

```yaml
theme-name:
  overwrite: true|false                # Optional, overwrite if exists
  variants: [dark, light]              # Optional, variants to generate
  display-name: "Theme Name"           # Optional, display name
  description: "Theme description"    # Optional, description
  author: "Theme author"               # Optional, author
  tags: [tag1, tag2, tag3]             # Optional, tags
  colors:                              # Required, 6 base colors
    - "#color1"  # Primary
    - "#color2"  # Secondary
    - "#color3"  # Error
    - "#color4"  # Success
    - "#color5"  # Warning
    - "#color6"  # Special
  syntax-format:                       # Optional, syntax formatting
    normal: none|bold|italic|both
    keyword: none|bold|italic|both
    magic: none|bold|italic|both
    builtin: none|bold|italic|both
    definition: none|bold|italic|both
    comment: none|bold|italic|both
    string: none|bold|italic|both
    number: none|bold|italic|both
    instance: none|bold|italic|both
  syntax-colors:                       # Optional, syntax colors
    dark:                              # For dark variant
      - "#B0"
      - "#B1"
      - "#B2"
      # ... up to 16 colors
    light:                             # For light variant
      - "#B0"
      - "#B1"
      - "#B2"
      # ... up to 16 colors
```

## Example

```yaml
my-theme:
  overwrite: true
  variants: [dark, light]
  display-name: "My Theme"
  description: "A custom theme"
  author: "My Name"
  tags: [dark, high-contrast, minimal]
  colors:
    - "#1e1e2e"  # Primary
    - "#b4befe"  # Secondary
    - "#f38ba8"  # Error
    - "#a6e3a1"  # Success
    - "#fab387"  # Warning
    - "#eba0ac"  # Special
  syntax-format:
    normal: none
    keyword: bold
    magic: bold
    builtin: none
    definition: none
    comment: italic
    string: none
    number: none
    instance: both
  syntax-colors:
    dark:
      - "#181926"  # B0
      - "#1e1e2e"  # B1
      - "#89b4fa"  # B2
      - "#cdd6f4"  # B3
      - "#181926"  # B4
      - "#a6e3a1"  # B5
      - "#f38ba8"  # B6
      - "#cdd6f4"  # B7
      - "#f38ba8"  # B8
      - "#94e2d5"  # B9
      - "#89b4fa"  # B10
      - "#a6e3a1"  # B11
      - "#7f849c"  # B12
      - "#f9e2af"  # B13
      - "#cba6f7"  # B14
      - "#cdd6f4"  # B15
    light:
      - "#e6e9ef"  # B0
      - "#eff1f5"  # B1
      - "#1e66f5"  # B2
      - "#4c4f69"  # B3
      - "#e6e9ef"  # B4
      - "#40a02b"  # B5
      - "#d20f39"  # B6
      - "#4c4f69"  # B7
      - "#d20f39"  # B8
      - "#179299"  # B9
      - "#1e66f5"  # B10
      - "#40a02b"  # B11
      - "#9ca0b0"  # B12
      - "#df8e1d"  # B13
      - "#8839ef"  # B14
      - "#4c4f69"  # B15
```

## Notes

- For syntax colors, you can provide 1 color (for auto-generation) or 16 colors (for a custom palette).
- If syntax colors are not specified, they will be automatically generated from the group colors.
- If variants are not specified, both (dark and light) will be generated.
- The theme name in the YAML file can be different from the name used in the command line. The command line name takes precedence.
