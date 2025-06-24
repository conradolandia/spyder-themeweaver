"""
QDarkStyle asset generation module for ThemeWeaver.

This module handles the generation of QDarkStyle-compatible assets including:
- SVG to PNG image conversion with theme colors
- SCSS compilation to QSS stylesheets
- QRC resource file generation and compilation
"""

import shutil
from pathlib import Path

try:
    import qdarkstyle
    from qdarkstyle.utils.scss import create_qss
    from qdarkstyle.utils.images import (
        create_images,
        generate_qrc_file,
        compile_qrc_file,
    )

    QDS_AVAILABLE = True
    QDS_IMPORT_ERROR = None
except ImportError as e:
    QDS_AVAILABLE = False
    QDS_IMPORT_ERROR = str(e)


class QDarkStyleAssetExporter:
    """Handles QDarkStyle asset generation using proper QDarkStyle utilities."""

    def __init__(self):
        """Initialize the QDarkStyle asset exporter."""
        if not QDS_AVAILABLE:
            raise ImportError(
                f"QDarkStyle not available. Import error: {QDS_IMPORT_ERROR}. "
                "Please install it to use the exporter: pip install qdarkstyle"
            )

    def export_assets(
        self, palette_class: type, export_dir: Path, variant: str
    ) -> Path:
        """Export QDarkStyle assets for a palette using proper QDarkStyle utilities.

        Args:
            palette_class: The palette class to export
            export_dir: Base export directory
            variant: Variant name ('dark' or 'light')

        Returns:
            Path to the variant's asset directory
        """
        # Create the variant directory structure
        variant_dir = export_dir / variant
        variant_dir.mkdir(parents=True, exist_ok=True)

        # Create rc subdirectory for images
        rc_dir = variant_dir / "rc"
        rc_dir.mkdir(parents=True, exist_ok=True)

        try:
            palette_instance = palette_class()

            print("  📁 Setting up QDarkStyle directory structure...")
            self._setup_qdarkstyle_structure(export_dir, variant_dir)

            print("  🖼️  Generating images with QDarkStyle utilities...")
            # Use QDarkStyle's create_images with custom rc_path
            create_images(rc_path=str(rc_dir), palette=palette_instance)

            print("  📄 Generating QRC file...")
            # QDarkStyle's generate_qrc_file expects files in its own package directory structure
            # But it should work somewhat like this...
            # generate_qrc_file(resource_prefix='qss_icons', style_prefix='qdarkstyle', palette=None):
            qrc_content = generate_qrc_file(resource_prefix='qss_icons', style_prefix='darkstyle', palette=palette_instance)
            qrc_file = variant_dir / f"{variant}style.qrc"
            qrc_file.write_text(str(qrc_content))
            print(f"    📄 Created {qrc_file.name}")
            
            print("  🎨 Generating QSS with proper SCSS variables...")
            # Use QDarkStyle's create_qss with base_path
            create_qss(palette=palette_instance, base_path=str(export_dir))

            # Try to compile the QRC file to Python if pyrcc5 is available
            # compile_qrc_file(compile_for='qtpy', qrc_path=None, palette=None):
            try:
                print(f"    🐍 Compiling QRC to Python: {qrc_file}")
                compile_qrc_file(compile_for='qtpy', qrc_path=str(variant_dir), palette=palette_instance)
            except Exception as e:
                print(f"    ⚠️  QRC compilation failed (non-critical): {e}")

            print(f"  📁 Assets exported to: {variant_dir}")
            return variant_dir

        except Exception as e:
            print(f"❌ QDarkStyle asset generation failed for {variant}: {e}")
            import traceback

            traceback.print_exc()
            raise

    def _setup_qdarkstyle_structure(self, export_dir: Path, variant_dir: Path):
        """Set up the directory structure that QDarkStyle utilities expect.

        QDarkStyle's create_qss expects specific files:
        1. [variant]/main.scss
        2. qss/_style.scss
        """
        # Copy required SCSS files from QDarkStyle package
        qdarkstyle_package_path = Path(qdarkstyle.__file__).parent

        # Copy main.scss from QDarkStyle's dark or light directory (they're the same)
        source_main_scss = qdarkstyle_package_path / "dark" / "main.scss"
        target_main_scss = variant_dir / "main.scss"
        if source_main_scss.exists():
            shutil.copy2(source_main_scss, target_main_scss)
            print("    📄 Copied main.scss")
        else:
            raise FileNotFoundError(
                f"Required main.scss not found at {source_main_scss}"
            )

        # Copy qss directory with _style.scss
        source_qss_dir = qdarkstyle_package_path / "qss"
        target_qss_dir = export_dir / "qss"
        if source_qss_dir.exists():
            if target_qss_dir.exists():
                shutil.rmtree(target_qss_dir)
            shutil.copytree(source_qss_dir, target_qss_dir)
            print("    📁 Copied qss directory with _style.scss")
        else:
            raise FileNotFoundError(
                f"Required qss directory not found at {source_qss_dir}"
            )
