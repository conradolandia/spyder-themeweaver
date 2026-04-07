# ThemeWeaver

ThemeWeaver is a Python tool to generate and export themes for the Spyder IDE with QDarkStyle integration. It builds consistent dark/light variants, exports Qt assets, and can package themes for Spyder.

## Project setup

This project uses [Pixi](https://pixi.sh/) for dependencies and tasks. Run tasks with `pixi run`; definitions live in `pyproject.toml`.

### Prerequisites

- [Pixi](https://pixi.sh/)
- Python 3.12+ (provided by the pixi environment)

### Installation

```bash
pixi install
pixi run python --version
```

## Quick start

```bash
# List themes in themes/
pixi run list-themes

# Export into build/ — one theme (dark + light), one variant only, or every theme
pixi run export spyder
pixi run export-light spyder
pixi run export-dark spyder
pixi run export-all

# Validate YAML theme config
pixi run validate solarized

# Validate contrast against bundled Spyder UI rules (dark/light)
pixi run validate-contrast zenburn
pixi run validate-contrast-all

# Preview (needs themes in build/ — export first)
pixi run export-all
pixi run preview

# Package for Spyder (needs themes in build/ — run export or export-all first; does not export)
pixi run package
pixi run package -- --themes dracula,solarized --output ./dist
```

Export tasks (`export`, `export-light`, `export-dark`, `export-all`) all call the `export` CLI and write under `build/`. The `package` task calls `python-package` and only copies what is already in `build/` into an installable layout under `dist/` — it never runs export for you.

Theme generation (colors or YAML) is documented under [Theme generation](#theme-generation).

## CLI reference

Use `pixi run cli …` for flags not covered by a task, or `pixi run cli <command> --help`.

### Theme management

```bash
pixi run list-themes
pixi run theme-info solarized
pixi run validate solarized
```

### Contrast validation

Checks resolved theme colors against rule sets in `src/themeweaver/contrast/` (`rules_dark.yaml`, `rules_light.yaml`). Override with `--rules-dir` if you maintain a fork of the rules.

```bash
pixi run validate-contrast zenburn
pixi run validate-contrast zenburn --variant dark
pixi run validate-contrast zenburn --verbose
pixi run validate-contrast-all
```

Same options apply when using the CLI directly: `pixi run cli validate-contrast --help`.

### Spyder Python package (`python-package`)

Creates a single installable Python package from exported themes under `build/`. Export themes before packaging.

```bash
pixi run package
pixi run package -- --themes catppuccin-mocha,dracula --output ./dist
pixi run cli python-package --package-name my_spyder_themes --output ./dist
```

Flags include `--themes` (comma-separated), `--package-name`, `-o` / `--output`, `--with-pyproject`, `--validate`.

Archive packaging (ZIP / tar.gz / folder) for loose theme folders is implemented in `ThemePackager` in the Python API only; there is no CLI subcommand for it.

### Theme generation

The `generate` command writes a new theme directory under `themes/<name>/` in the current working directory (or under `--output-dir`). It produces three files: `theme.yaml` (metadata), `colorsystem.yaml` (palette definitions), and `mappings.yaml` (semantic UI and syntax references). Those sources are what `export` reads; generation does not write to `build/`.

**Six seed colors**

The six inputs are not the entire UI palette. They seed the generator: each value anchors a family of derived colors (primary/secondary UI, state colors, group gradients, etc.) that fill `colorsystem.yaml` and drive `mappings.yaml`.

| Position | Role |
| -------- | ---- |
| 1 | Primary |
| 2 | Secondary |
| 3 | Error |
| 4 | Success |
| 5 | Warning |
| 6 | Group (starting point for group/syntax-related ramps) |

**1. From the CLI**

```bash
pixi run generate my_theme \
  --colors "#1e1e2e" "#b4befe" "#f38ba8" "#a6e3a1" "#fab387" "#eba0ac" \
  --display-name "My Custom Theme" \
  --description "Generated from base colors" \
  --author "Your Name" \
  --tags "custom,dark"
```

| Flag | Purpose |
| ---- | ------- |
| `--variants dark light` | Emit only the listed variants (default: both). |
| `--overwrite` | Replace an existing `themes/<name>/` directory. |
| `--output-dir <path>` | Parent directory for themes (default: `./themes`). Afterward, pass `--theme-dir` to `export` if you did not use the default. |
| `--simple-names` | Use simple internal color names instead of creative names in generated data. |
| `--syntax-format` | Comma-separated pairs: `element:style`. Elements: `normal`, `keyword`, `magic`, `builtin`, `definition`, `comment`, `string`, `number`, `instance`, `symbol` (operators, brackets, punctuation; maps to `EDITOR_SYMBOL` / `Syntax.B170`). Styles: `none`, `bold`, `italic`, `both`. Example: `keyword:bold,comment:italic`. |
| `--syntax-colors-dark` / `--syntax-colors-light` | Space-separated: **one** hex (seed) or **17** hex (full palette). |
| `--validate-contrast` / `--no-validate-contrast` | After generation, run contrast checks against bundled rules (default: on). Failures are logged; generation still completes. |

**2. From a YAML definition file**

```bash
pixi run generate my_theme --from-yaml theme-definition.yaml
```

The file must have **exactly one** top-level key: the theme id inside the YAML. The **directory name** is always the `generate` argument (`my_theme` above), not that key. If the YAML id and CLI name differ, the CLI name is used and a warning is printed.

YAML fields (under that single top-level theme key):

| Field | Required | Notes |
| ----- | -------- | ----- |
| `colors` | Yes | Six hex strings, same order as the table above. |
| `overwrite` | No | Same as `--overwrite`. |
| `variants` | No | List such as `[dark, light]`; default both. |
| `display-name`, `description`, `author` | No | Metadata for `theme.yaml`. |
| `tags` | No | YAML list of tags (or omit). |
| `syntax-format` | No | Map from element name to `none` / `bold` / `italic` / `both` (same elements as CLI). |
| `syntax-colors` | No | Map with optional `dark` and `light` keys; each value is a list of **1** or **17** hex strings. |

If `syntax-colors` is omitted, syntax colors are derived from the group palette. If `variants` is omitted, both dark and light are generated.

**After generation**

Run `pixi run validate <name>` on the new tree if you want structural checks only, or `pixi run validate-contrast <name>` for Spyder rule checks. To produce QSS under `build/`, run `pixi run export <name>` (and add `--theme-dir` if you used `--output-dir`).

For a hand-maintained reference layout, see `themes/catppuccin-mocha/` (`colorsystem.yaml`, `mappings.yaml`, `theme.yaml`).

### Color utilities

These commands print palettes to stdout (and optional logging). They do not modify `themes/` unless you copy values yourself. Use `pixi run cli <command> --help` for the full flag list.

#### `palette`

Builds **GroupDark** and **GroupLight** sets (or a single **Syntax** palette) as named steps `B10`, `B20`, … for groups, or `B10`…`B170` for syntax (17 colors, including the slot used for `EDITOR_SYMBOL`). Default `--num-colors` is 12 for group methods; `--method syntax` uses the full syntax size.

| `--method` | Behavior |
| ---------- | -------- |
| `perceptual` (default) | Spaced hues for dark and light “group” palettes; optional `--start-hue` (0–360). If you omit `--start-hue`, defaults are around 37° (dark) and 53° (light). |
| `optimal` | Colors tuned for distinguishability; `--start-hue` optional. |
| `uniform` | Hue steps of about 30° around the wheel. |
| `syntax` | 17-color syntax palette (B10–B170) from a seed; **requires** `--from-color`. |

**`--from-color` precedence:** If you pass `--from-color` and the method is **not** `syntax`, the implementation uses a golden-ratio-based expansion from that seed for GroupDark/GroupLight; the chosen `perceptual` / `optimal` / `uniform` method is **not** used in that branch. For `syntax`, `--from-color` is required.

| Other flags | Purpose |
| ----------- | ------- |
| `--output-format` | `list` (human-readable), `json`, or `class` (Python-like class snippets for pasting). |
| `--no-analysis` | Skip the perceptual distance summary logging after the main output. |

```bash
pixi run palette --method optimal --num-colors 12
pixi run palette --method syntax --from-color "#FF5500"
pixi run palette --from-color "#3c3836" --num-colors 10 --output-format json
```

#### `gradient`

Produces **16** colors along black → base color → white. Default `--method` is `lch-lightness` (dedicated lightness ramp). Other methods reuse the same piecewise interpolation as `interpolate` (black→color, then color→white) to fill 16 steps.

| Flag | Purpose |
| ---- | ------- |
| `--output` | `list`, `json`, or `yaml`. |
| `--name` | Palette name in structured outputs. |
| `--simple-names` | Simpler auto-generated names where applicable. |
| `--analyze` | Print interpolation analysis. |
| `--validate` | Check gradient color uniqueness. |
| `--exponent` | Used when `--method exponential`. |

```bash
pixi run gradient "#DF8E1D"
pixi run gradient "#DF8E1D" --output yaml --name "MyPalette"
```

#### `interpolate`

Steps between two hex endpoints. Default `--method` is `linear`; default step count is **8** if you omit the third positional argument.

| `--method` values | Notes |
| ----------------- | ----- |
| `linear`, `cubic`, `exponential`, `sine`, `cosine`, `hermite`, `quintic` | Curve-shaped ramps in RGB space; `exponential` uses `--exponent` (default 2). |
| `hsv`, `lch` | Perceptual or hue-space paths. |

Pixi shortcuts fix the method:

```bash
pixi run interpolate "#002B36" "#EEE8D5" 16
pixi run interpolate-lch "#002B36" "#EEE8D5" 16
pixi run interpolate-hsv "#002B36" "#EEE8D5" 16
```

Shared flags with `gradient`: `--output` (`list` / `json` / `yaml`), `--name`, `--simple-names`, `--analyze`, `--validate`, `--exponent`.

## Development

```bash
pixi run lint
pixi run format
pixi run lint-fix
pixi run check   # runs lint (ruff check) only
pixi run test
pixi run test-cov
pixi run inspect-cov   # HTTP server for htmlcov; open http://127.0.0.1:8000
```

### Pre-commit

```bash
pixi run pre-commit-install
pixi run pre-commit-run
pixi run pre-commit-update
```

## Pixi tasks

| Task                    | Description                                                                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `lint`                  | Ruff check                                                                                                                         |
| `format`                | Ruff format                                                                                                                        |
| `lint-fix`              | Ruff check with autofix                                                                                                            |
| `check`                 | Same as `lint`                                                                                                                     |
| `cli`                   | `python -m themeweaver.cli` (pass subcommands and flags)                                                                           |
| `export`                | Export one theme (`pixi run export <name>`)                                                                                        |
| `export-light`          | Export light variant only                                                                                                          |
| `export-dark`           | Export dark variant only                                                                                                           |
| `export-all`            | Export every theme into `build/`                                                                                                   |
| `package`               | `python-package`: copy from `build/` to `dist/` (run `export` / `export-all` first; all built themes unless `--themes` after `--`) |
| `list-themes`           | List theme directories                                                                                                             |
| `theme-info`            | Show theme metadata                                                                                                                |
| `generate`              | Generate a theme from colors or YAML                                                                                               |
| `validate`              | Validate theme YAML                                                                                                                |
| `validate-contrast`     | Contrast rules for one theme                                                                                                       |
| `validate-contrast-all` | Contrast rules for all themes                                                                                                      |
| `interpolate`           | Color interpolation (`$START_COLOR`, `$END_COLOR`, `$STEPS`)                                                                       |
| `interpolate-lch`       | Interpolate with `--method lch`                                                                                                    |
| `interpolate-hsv`       | Interpolate with `--method hsv`                                                                                                    |
| `palette`               | Palette generation                                                                                                                 |
| `gradient`              | 16-color lightness gradient                                                                                                        |
| `preview`               | Qt preview app                                                                                                                     |
| `test`                  | Pytest                                                                                                                             |
| `test-cov`              | Pytest with coverage                                                                                                               |
| `inspect-cov`           | Serve HTML coverage report                                                                                                         |
| `pre-commit-install`    | Install git hooks                                                                                                                  |
| `pre-commit-run`        | Run hooks on all files                                                                                                             |
| `pre-commit-update`     | Autoupdate hook revisions                                                                                                          |

## Dependencies

Managed in `pyproject.toml` (pixi): Python 3.12, [QDarkStyle](https://github.com/ColinDuquesnoy/QDarkStyleSheet) (git `develop` branch), PyYAML, colorspacious, qtsass, PyQt5 (conda `pyqt`; preview imports `PyQt5`), ruff, pytest, and related dev tools.

QDarkStyle tracks `develop` until a release exposes the APIs this project uses; the dependency pin will move to a published version when that is available.

## Project layout

```
themeweaver/
├── src/themeweaver/
│   ├── cli/           # CLI entrypoint and commands
│   ├── contrast/      # Contrast rules and validator
│   ├── core/          # Export, generation, YAML loading
│   └── color_utils/   # Palettes, interpolation, helpers
├── themes/            # Theme sources (default cwd-relative)
├── scripts/           # Preview launcher and helpers
│   └── preview/       # Preview UI implementation
├── tests/
├── pyproject.toml
└── README.md
```

## Contributing

1. Fork the repository and create a branch.
2. Change the code; add tests where it helps.
3. Run `pixi run check` and `pixi run test`.
4. Open a pull request.

## License

This project is licensed under the MIT License; see [LICENSE](./LICENSE).
