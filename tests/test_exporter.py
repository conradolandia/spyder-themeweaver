#!/usr/bin/env python3
"""
Integration tests for the ThemeWeaver exporter.

This module tests the complete export pipeline without requiring CLI setup.
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from themeweaver.core.exporter import ThemeExporter


class TestThemeExporter:
    """Integration tests for ThemeExporter functionality."""

    def setup_method(self):
        """Setup test environment with temporary build directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.build_dir = Path(self.temp_dir) / "build"
        self.exporter = ThemeExporter(build_dir=self.build_dir)

    def teardown_method(self):
        """Cleanup test environment."""
        if hasattr(self, 'temp_dir') and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_exporter_initialization(self):
        """Test that exporter initializes correctly."""
        assert self.exporter.build_dir == self.build_dir
        assert self.exporter.themes_dir.exists()
        assert self.exporter.themes_dir.name == "themes"

    def test_theme_discovery(self):
        """Test that exporter can discover available themes."""
        themes = list(self.exporter.themes_dir.iterdir())
        available_themes = [
            t.name for t in themes if t.is_dir() and not t.name.startswith(".")
        ]
        
        assert len(available_themes) > 0
        assert "solarized" in available_themes

    def test_solarized_theme_export(self):
        """Test complete export of solarized theme."""
        # Export solarized theme
        result = self.exporter.export_theme("solarized")
        
        # Verify export results
        assert isinstance(result, dict)
        assert len(result) > 0
        
        # Check that expected variants are present
        expected_variants = ["dark", "light"]
        for variant in expected_variants:
            assert variant in result
            assert isinstance(result[variant], Path)
            assert result[variant].exists()

    def test_exported_files_structure(self):
        """Test that exported files have expected structure."""
        # Export theme
        result = self.exporter.export_theme("solarized")
        
        # Check main export directory
        solarized_dir = self.build_dir / "solarized"
        assert solarized_dir.exists()
        
        # Check for expected files
        expected_files = ["colorsystem.py", "palette.py"]
        for file_name in expected_files:
            file_path = solarized_dir / file_name
            assert file_path.exists()
            assert file_path.stat().st_size > 0
        
        # Check variant directories
        for variant in ["dark", "light"]:
            variant_dir = solarized_dir / variant
            assert variant_dir.exists()
            
            # Check for QDarkStyle files
            qss_file = variant_dir / f"{variant}style.qss"
            assert qss_file.exists()

    def test_theme_not_found_error(self):
        """Test that exporter raises appropriate error for non-existent theme."""
        with pytest.raises(FileNotFoundError):
            self.exporter.export_theme("nonexistent_theme")

    def test_export_specific_variants(self):
        """Test exporting specific variants only."""
        # Export only dark variant
        result = self.exporter.export_theme("solarized", variants=["dark"])
        
        assert "dark" in result
        assert "light" not in result
        
        # Verify only dark variant directory exists
        solarized_dir = self.build_dir / "solarized"
        assert (solarized_dir / "dark").exists()
        # Light directory might exist from QDarkStyle CLI, but shouldn't be in results

    def test_export_all_themes(self):
        """Test exporting all available themes."""
        result = self.exporter.export_all_themes()
        
        assert isinstance(result, dict)
        assert len(result) > 0
        assert "solarized" in result
        
        # Each theme should have exported variants
        for theme_name, variants in result.items():
            assert isinstance(variants, dict)
            assert len(variants) > 0


# Legacy test function for backward compatibility
def test_exporter():
    """Legacy test function that demonstrates the exporter working."""
    print("🧪 Testing ThemeWeaver Exporter (Legacy)")
    print("=" * 50)

    try:
        # Create exporter
        exporter = ThemeExporter()
        print(f"📁 Build directory: {exporter.build_dir}")
        print(f"📁 Themes directory: {exporter.themes_dir}")

        # Test listing themes
        themes = list(exporter.themes_dir.iterdir())
        available_themes = [
            t.name for t in themes if t.is_dir() and not t.name.startswith(".")
        ]
        print(f"📚 Available themes: {available_themes}")

        if "solarized" in available_themes:
            print("\n🎨 Testing solarized theme export...")

            # Export solarized theme
            result = exporter.export_theme("solarized")

            print("✅ Export completed successfully!")
            print(f"📋 Exported variants: {list(result.keys())}")

            # Check generated files
            solarized_dir = exporter.build_dir / "solarized"
            if solarized_dir.exists():
                print(f"\n📁 Generated files in {solarized_dir}:")
                for item in solarized_dir.iterdir():
                    if item.is_file():
                        print(f"  📄 {item.name} ({item.stat().st_size} bytes)")
                    else:
                        print(f"  📁 {item.name}/")
                        # Show files in subdirectories
                        for subitem in item.iterdir():
                            print(f"    📄 {subitem.name}")

        else:
            print("⚠️  Solarized theme not found, skipping export test")

    except ImportError as e:
        print(f"❌ Import error (QDarkStyle may not be installed): {e}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_exporter()
