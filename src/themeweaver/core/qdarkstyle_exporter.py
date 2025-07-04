"""
QDarkStyle asset generation module for ThemeWeaver.

This module handles the generation of QDarkStyle-compatible assets using the new
CLI API from QDarkStyle PR #363, which supports custom palette generation outside
the package structure.
"""

import importlib.util
import logging
import subprocess
import tempfile
from pathlib import Path

_logger = logging.getLogger(__name__)

# Check QDarkStyle availability without importing
QDS_AVAILABLE = importlib.util.find_spec("qdarkstyle") is not None
QDS_IMPORT_ERROR = None if QDS_AVAILABLE else "QDarkStyle package not found"


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
        self,
        palette_class: type,
        export_dir: Path,
        variant: str,
        cleanup_intermediate: bool = True,
    ) -> Path:
        """Export QDarkStyle assets using the new CLI API from PR #363.

        Args:
            palette_class: The palette class to export
            export_dir: Base export directory
            variant: Variant name ('dark' or 'light')
            cleanup_intermediate: Whether to remove intermediate files (SASS, SCSS templates, redundant palette.py)

        Returns:
            Path to the variant's asset directory
        """
        # Create the variant directory structure
        variant_dir = export_dir / variant
        variant_dir.mkdir(parents=True, exist_ok=True)

        try:
            palette_instance = palette_class()

            _logger.info(
                "🎨 Generating %s theme assets using QDarkStyle CLI...", variant
            )

            # Create temporary palette file for QDarkStyle CLI
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as temp_file:
                temp_palette_path = Path(temp_file.name)
                temp_file.write(
                    self._generate_palette_file_content(palette_class, palette_instance)
                )

            try:
                # Build QDarkStyle CLI command - point to theme root, not variant dir
                theme_root = export_dir  # /build/theme (not /build/theme/dark)
                cmd = [
                    "python",
                    "-m",
                    "qdarkstyle.utils",
                    "--base_path",
                    str(theme_root),
                    "--images_path",
                    str(theme_root),
                    "--custom_palette_file",
                    str(temp_palette_path),
                    "--custom_palette_class_name",
                    palette_class.__name__,
                ]

                _logger.info("🔧 Running QDarkStyle CLI: %s", " ".join(cmd[3:]))
                _logger.info("   Working directory: %s", theme_root)
                _logger.info("   Theme root: %s", theme_root)
                _logger.info("   Variant: %s", variant)
                _logger.info("   Full command: %s", " ".join(cmd))

                # Run QDarkStyle CLI with visible output from theme root
                result = subprocess.run(
                    cmd, capture_output=True, text=True, cwd=theme_root
                )

                _logger.info("📊 QDarkStyle CLI execution completed!")

                # Always show QDarkStyle CLI stderr if present
                if result.stderr.strip():
                    _logger.info("📝 QDarkStyle CLI output:")
                    for line in result.stderr.strip().split("\n"):
                        if line.strip():
                            _logger.info("  %s", line)

                if result.returncode != 0:
                    _logger.error(
                        "❌ QDarkStyle CLI failed with return code %s",
                        result.returncode,
                    )
                    raise RuntimeError(
                        f"QDarkStyle CLI failed with return code {result.returncode}"
                    )

                _logger.info("✅ QDarkStyle assets generated successfully")

                # Clean up redundant and intermediate files
                if cleanup_intermediate:
                    self._cleanup_intermediate_files(export_dir, variant_dir)

                _logger.info("📁 Assets exported to: %s", variant_dir)

                return variant_dir

            finally:
                # Clean up temporary file
                if temp_palette_path.exists():
                    temp_palette_path.unlink()

        except Exception as e:
            _logger.error(
                "❌ QDarkStyle asset generation failed for %s: %s", variant, e
            )
            _logger.exception("Exception details:")
            raise

    def _cleanup_intermediate_files(self, export_dir: Path, variant_dir: Path):
        """Remove redundant and intermediate files from the export directories.

        Args:
            export_dir: Base export directory (theme root)
            variant_dir: Path to the variant directory to clean up
        """
        # Files to remove from variant directory
        intermediate_files = [
            "palette.py",  # Redundant palette file (already in main theme directory)
            "main.scss",  # Intermediate SASS file
            "_variables.scss",  # Intermediate SASS variables file
        ]

        # Clean up variant directory
        removed_files = []
        for file_name in intermediate_files:
            file_path = variant_dir / file_name
            if file_path.exists():
                file_path.unlink()
                removed_files.append(file_name)

        # Clean up SCSS template from qss directory
        qss_dir = export_dir / "qss"
        if qss_dir.exists():
            scss_file = qss_dir / "_styles.scss"
            if scss_file.exists():
                scss_file.unlink()
                removed_files.append("_styles.scss")

                # Remove qss directory if it's now empty
                if not any(qss_dir.iterdir()):
                    qss_dir.rmdir()

        if removed_files:
            _logger.info(
                "✨ Cleanup completed - removed %d intermediate files",
                len(removed_files),
            )
        else:
            _logger.info("✨ Cleanup completed - no intermediate files found")

    def _generate_palette_file_content(
        self, palette_class: type, palette_instance
    ) -> str:
        """Generate Python file content for the palette class.

        Args:
            palette_class: The palette class to export
            palette_instance: Instance of the palette class

        Returns:
            String content for the temporary palette file
        """
        # Get all palette attributes
        attributes = []
        for attr_name in dir(palette_instance):
            if not attr_name.startswith("_") and attr_name.isupper():
                attr_value = getattr(palette_instance, attr_name)
                if isinstance(attr_value, (str, int, float)):
                    # Use repr() to properly handle strings with quotes and other edge cases
                    attributes.append(f"    {attr_name} = {repr(attr_value)}")

        # Generate the file content
        content = f'''"""
Temporary palette file for QDarkStyle CLI.
Generated by ThemeWeaver.
"""

from qdarkstyle.palette import Palette


class {palette_class.__name__}(Palette):
    """Palette class for QDarkStyle generation."""
    
{"\n".join(attributes)}
'''
        return content
