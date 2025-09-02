"""
Theme packaging module for ThemeWeaver.

This module handles packaging of exported themes into compressed archives
with proper metadata inclusion for distribution and installation.
"""

import logging
import shutil
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Optional

from themeweaver.core.colorsystem import load_theme_metadata_from_yaml

_logger = logging.getLogger(__name__)


class ThemePackager:
    """Packages exported themes into compressed archives with metadata."""

    def __init__(self, output_dir: Optional[Path] = None) -> None:
        """Initialize the packager.

        Args:
            output_dir: Directory to output packages to. Defaults to workspace 'dist' directory.
        """
        # Get workspace root
        self.workspace_root = Path(__file__).parent.parent.parent.parent
        self.output_dir = output_dir or self.workspace_root / "dist"
        self.build_dir = self.workspace_root / "build"
        self.themes_dir = Path(__file__).parent.parent / "themes"

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def package_theme(self, theme_name: str, format: str = "zip") -> Path:
        """Package a single exported theme into a compressed archive or folder.

        Args:
            theme_name: Name of the theme to package
            format: Archive format ('zip', 'tar.gz') or 'folder' for uncompressed directory

        Returns:
            Path to the created package file or directory

        Raises:
            FileNotFoundError: If theme is not exported in build directory
            ValueError: If format is not supported
        """
        _logger.info("📦 Packaging theme: %s", theme_name)

        # Check if theme is exported
        theme_build_dir = self.build_dir / theme_name
        if not theme_build_dir.exists():
            raise FileNotFoundError(
                f"Theme '{theme_name}' not found in build directory. "
                f"Please export the theme first using 'themeweaver export --theme {theme_name}'"
            )

        # Load theme metadata
        try:
            theme_metadata = load_theme_metadata_from_yaml(theme_name)
        except Exception as e:
            _logger.warning("⚠️  Could not load theme metadata: %s", e)
            theme_metadata = {"name": theme_name, "display_name": theme_name}

        # Create package filename or directory name
        version = theme_metadata.get("version", "1.0.0")
        if format == "folder":
            package_name = theme_name
            package_path = self.output_dir / package_name
        else:
            package_name = f"{theme_name}-{version}.{format}"
            package_path = self.output_dir / package_name

        if format == "folder":
            # Create folder directly
            package_path.mkdir(parents=True, exist_ok=True)

            # Copy theme files directly to package directory
            self._copy_theme_files(theme_name, theme_build_dir, package_path)

            # Add metadata files
            self._add_metadata_files(theme_name, theme_metadata, package_path)
        else:
            # Create temporary directory for packaging
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                # Copy theme files to temp directory
                self._copy_theme_files(theme_name, theme_build_dir, temp_path)

                # Add metadata files
                self._add_metadata_files(theme_name, theme_metadata, temp_path)

                # Create archive
                if format == "zip":
                    self._create_zip_archive(temp_path, package_path, theme_name)
                elif format == "tar.gz":
                    self._create_tar_archive(temp_path, package_path, theme_name)
                else:
                    raise ValueError(
                        f"Unsupported format: {format}. Supported formats: zip, tar.gz, folder"
                    )

        _logger.info("✅ Created package: %s", package_path)
        return package_path

    def package_all_themes(self, format: str = "zip") -> Dict[str, Path]:
        """Package all exported themes into compressed archives or folders.

        Args:
            format: Archive format ('zip', 'tar.gz') or 'folder' for uncompressed directories

        Returns:
            Dict mapping theme names to their package paths
        """
        _logger.info("📦 Packaging all exported themes...")

        packages: Dict[str, Path] = {}

        # Find all exported themes in build directory
        if not self.build_dir.exists():
            _logger.warning("⚠️  Build directory does not exist. No themes to package.")
            return packages

        theme_dirs = [
            d
            for d in self.build_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

        for theme_dir in theme_dirs:
            theme_name = theme_dir.name
            try:
                packages[theme_name] = self.package_theme(theme_name, format)
            except Exception as e:
                _logger.error("❌ Failed to package theme '%s': %s", theme_name, e)

        return packages

    def _copy_theme_files(
        self, theme_name: str, source_dir: Path, dest_dir: Path
    ) -> None:
        """Copy theme files from build directory to temporary directory.

        Args:
            theme_name: Name of the theme
            source_dir: Source directory (build/theme_name)
            dest_dir: Destination directory (temp)
        """
        _logger.info("📋 Copying theme files...")

        # Copy all files and directories from build directory
        for item in source_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, dest_dir / item.name)
            elif item.is_dir():
                dest_item = dest_dir / item.name
                if dest_item.exists():
                    # If destination exists, remove it first
                    if dest_item.is_dir():
                        shutil.rmtree(dest_item)
                    else:
                        dest_item.unlink()
                shutil.copytree(item, dest_item)

    def _add_metadata_files(
        self, theme_name: str, metadata: Dict, dest_dir: Path
    ) -> None:
        """Add metadata files to the package.

        Args:
            theme_name: Name of the theme
            metadata: Theme metadata dictionary
            dest_dir: Destination directory for metadata files
        """
        _logger.info("📋 Adding metadata files...")

        # Copy theme.yaml from source themes directory
        theme_yaml_source = self.themes_dir / theme_name / "theme.yaml"
        if theme_yaml_source.exists():
            shutil.copy2(theme_yaml_source, dest_dir / "theme.yaml")
            _logger.info("  📄 Added: theme.yaml")

        # Create README.md
        readme_content = self._generate_readme_content(theme_name, metadata)
        readme_path = dest_dir / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")
        _logger.info("  📄 Added: README.md")

        # Create installation instructions
        install_content = self._generate_install_content(theme_name, metadata)
        install_path = dest_dir / "INSTALL.md"
        install_path.write_text(install_content, encoding="utf-8")
        _logger.info("  📄 Added: INSTALL.md")

    def _generate_readme_content(self, theme_name: str, metadata: Dict) -> str:
        """Generate README.md content for the theme package.

        Args:
            theme_name: Name of the theme
            metadata: Theme metadata

        Returns:
            README content as string
        """
        display_name = metadata.get("display_name", theme_name)
        description = metadata.get("description", "A theme for Spyder IDE")
        author = metadata.get("author", "ThemeWeaver")
        version = metadata.get("version", "1.0.0")
        license_text = metadata.get("license", "MIT")
        url = metadata.get("url", "")
        tags = metadata.get("tags", [])

        content = f"""# {display_name}

{description}

## Theme Information

- **Name**: {theme_name}
- **Display Name**: {display_name}
- **Version**: {version}
- **Author**: {author}
- **License**: {license_text}
"""

        if url:
            content += f"- **URL**: {url}\n"

        if tags:
            content += f"- **Tags**: {', '.join(tags)}\n"

        content += """
## Contents

This package contains:
- `colorsystem.py` - Color system definitions
- `palette.py` - Palette and semantic mapping definitions
- `dark/` - Dark variant assets (QSS, QRC, icons)
- `light/` - Light variant assets (QSS, QRC, icons)
- `theme.yaml` - Theme metadata
- `README.md` - This file
- `INSTALL.md` - Installation instructions

## Installation

See `INSTALL.md` for detailed installation instructions.

## Usage

After installation, the theme will be available in Spyder's theme selection menu.
"""

        return content

    def _generate_install_content(self, theme_name: str, metadata: Dict) -> str:
        """Generate installation instructions for the theme package.

        Args:
            theme_name: Name of the theme
            metadata: Theme metadata

        Returns:
            Installation content as string
        """
        display_name = metadata.get("display_name", theme_name)

        content = f"""# Installation Instructions for {display_name}

## Method 1: Manual Installation

1. Extract this package to a temporary location
2. Copy the contents to your Spyder themes directory:
   - **Windows**: `%APPDATA%\\spyder-py3\\themes\\{theme_name}\\`
   - **macOS**: `~/Library/Application Support/spyder-py3/themes/{theme_name}/`
   - **Linux**: `~/.config/spyder-py3/themes/{theme_name}/`

3. Restart Spyder
4. Go to `Tools > Preferences > Appearance`
5. Select "{display_name}" from the selection menu

## Method 2: Using Spyder's Theme Manager (Future)

When Spyder supports theme packages, you will be able to:
1. Go to `Tools > Preferences > Appearance`
2. Click "Import Theme Package"
3. Select this package file
4. The theme will be automatically installed

## File Structure

```
{theme_name}/
├── colorsystem.py      # Color system definitions
├── palette.py          # Palette definitions
├── dark/               # Dark variant
│   ├── darkstyle.qss   # Qt stylesheet
│   ├── darkstyle.qrc   # Qt resource file
│   └── rc/             # Icons and resources
├── light/              # Light variant
│   ├── darkstyle.qss   # Qt stylesheet
│   ├── darkstyle.qrc   # Qt resource file
│   └── rc/             # Icons and resources
├── theme.yaml          # Theme metadata
├── README.md           # Theme documentation
└── INSTALL.md          # This file
```

## Troubleshooting

- If the theme doesn't appear, ensure all files are copied correctly
- Check that the directory structure matches the expected layout
- Restart Spyder after installation
- Verify that the theme files have proper permissions

## Support

Theme created with [ThemeWeaver](https://github.com/conradolandia/spyder-themeweaver).
For issues with this theme, please check:
1. Spyder's theme documentation
2. ThemeWeaver project documentation
3. Create an issue in the ThemeWeaver repository
"""

        return content

    def _create_zip_archive(
        self, source_dir: Path, dest_path: Path, theme_name: str
    ) -> None:
        """Create a ZIP archive of the theme files.

        Args:
            source_dir: Source directory containing theme files
            dest_path: Destination path for the ZIP file
            theme_name: Name of the theme (for logging)
        """
        _logger.info("📦 Creating ZIP archive...")

        with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for item in source_dir.rglob("*"):
                if item.is_file():
                    # Add file to archive with relative path
                    arcname = item.relative_to(source_dir)
                    zipf.write(item, arcname)

    def _create_tar_archive(
        self, source_dir: Path, dest_path: Path, theme_name: str
    ) -> None:
        """Create a TAR.GZ archive of the theme files.

        Args:
            source_dir: Source directory containing theme files
            dest_path: Destination path for the TAR.GZ file
            theme_name: Name of the theme (for logging)
        """
        _logger.info("📦 Creating TAR.GZ archive...")

        with tarfile.open(dest_path, "w:gz") as tarf:
            tarf.add(source_dir, arcname=theme_name)
