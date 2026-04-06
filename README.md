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

**1. Six base colors (CLI)** — order: Primary, Secondary, Error, Success, Warning, Group.

```bash
pixi run generate my_theme \
  --colors "#1e1e2e" "#b4befe" "#f38ba8" "#a6e3a1" "#fab387" "#eba0ac" \
  --display-name "My Custom Theme" \
  --description "Generated from base colors" \
  --author "Your Name" \
  --tags "custom,dark"
```

**2. YAML definition**

```bash
pixi run generate my_theme --from-yaml theme-definition.yaml
```

Optional CLI flags (in addition to metadata): `--variants dark light`, `--overwrite`, `--output-dir <path>`, `--simple-names`, `--syntax-format 'keyword:bold,comment:italic'`, `--syntax-colors-dark` / `--syntax-colors-light` (one seed color or 16 colors each), `--no-validate-contrast` to skip post-generation contrast checks.

**YAML shape** (top-level key is a theme id; the `generate` command-line name wins for the output folder):

- `overwrite`, `variants`, `display-name`, `description`, `author`, `tags` — optional
- `colors` — required list of six hex strings (same order as `--colors`)
- `syntax-format` — optional map: `normal`, `keyword`, `magic`, `builtin`, `definition`, `comment`, `string`, `number`, `instance` → `none` | `bold` | `italic` | `both`
- `syntax-colors.dark` / `syntax-colors.light` — optional lists of 1 (seed) or 16 (full palette) hex strings

See `themes/catppuccin-mocha/` for a full theme layout (`colorsystem.yaml`, `mappings.yaml`, and optional `theme.yaml`).

**Notes**

- If `variants` is omitted, both dark and light are generated.
- If `syntax-colors` is omitted, syntax colors are derived from the group palette.

### Color utilities

**`palette`** — distinct colors (methods: `perceptual`, `optimal`, `uniform`, `syntax`). Useful options: `--num-colors`, `--from-color`, `--start-hue`, `--output-format` (`list`, `json`, `class`), `--no-analysis`.

```bash
pixi run palette --method optimal --num-colors 12
pixi run palette --method syntax --from-color "#FF5500"
```

**`gradient`** — 16-step lightness ramp from one color (default method `lch-lightness`). Also supports the same `--method` values as `interpolate` where applicable; `--output` `list` | `json` | `yaml`; `--analyze`, `--validate`.

```bash
pixi run gradient "#DF8E1D"
pixi run gradient "#DF8E1D" --output yaml --name "MyPalette"
```

**`interpolate`** — steps between two colors. Default method is `linear`; others include `lch`, `hsv`, `cubic`, `exponential`, `sine`, `cosine`, `hermite`, `quintic`. Pixi shortcuts:

```bash
pixi run interpolate "#002B36" "#EEE8D5" 16
pixi run interpolate-lch "#002B36" "#EEE8D5" 16
pixi run interpolate-hsv "#002B36" "#EEE8D5" 16
```

Additional flags: `--exponent`, `--output`, `--name`, `--simple-names`, `--analyze`, `--validate`.

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

| Task | Description |
|------|-------------|
| `lint` | Ruff check |
| `format` | Ruff format |
| `lint-fix` | Ruff check with autofix |
| `check` | Same as `lint` |
| `cli` | `python -m themeweaver.cli` (pass subcommands and flags) |
| `export` | Export one theme (`pixi run export <name>`) |
| `export-light` | Export light variant only |
| `export-dark` | Export dark variant only |
| `export-all` | Export every theme into `build/` |
| `package` | `python-package`: copy from `build/` to `dist/` (run `export` / `export-all` first; all built themes unless `--themes` after `--`) |
| `list-themes` | List theme directories |
| `theme-info` | Show theme metadata |
| `generate` | Generate a theme from colors or YAML |
| `validate` | Validate theme YAML |
| `validate-contrast` | Contrast rules for one theme |
| `validate-contrast-all` | Contrast rules for all themes |
| `interpolate` | Color interpolation (`$START_COLOR`, `$END_COLOR`, `$STEPS`) |
| `interpolate-lch` | Interpolate with `--method lch` |
| `interpolate-hsv` | Interpolate with `--method hsv` |
| `palette` | Palette generation |
| `gradient` | 16-color lightness gradient |
| `preview` | Qt preview app |
| `test` | Pytest |
| `test-cov` | Pytest with coverage |
| `inspect-cov` | Serve HTML coverage report |
| `pre-commit-install` | Install git hooks |
| `pre-commit-run` | Run hooks on all files |
| `pre-commit-update` | Autoupdate hook revisions |

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
