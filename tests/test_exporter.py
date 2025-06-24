#!/usr/bin/env python3
"""
Test script for the ThemeWeaver exporter.

This script tests the exporter functionality without requiring full CLI setup.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from themeweaver.core.exporter import ThemeExporter


def test_exporter():
    """Test the exporter with the solarized theme."""
    print("🧪 Testing ThemeWeaver Exporter")
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
