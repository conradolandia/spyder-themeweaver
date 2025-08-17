#!/usr/bin/env python3
"""
Example script showing how to use the ThemeWeaver CLI to generate themes.

This script demonstrates various ways to create themes using the themeweaver
command-line interface.
"""

import subprocess
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def run_command(command, description):
    """Run a command and show its output."""
    print(f"\n🔧 {description}")
    print(f"💻 Command: {' '.join(command)}")
    print("📋 Output:")
    print("-" * 50)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        print("✅ Command completed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with return code {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)

    print("-" * 50)


def main():
    # Example 1: Generate theme from single colors (new approach)
    run_command(
        [
            "python",
            "-m",
            "themeweaver.cli",
            "generate",
            "modern_blue",
            "--single-colors",
            "#1A72BB",  # Primary
            "#FF5500",  # Secondary
            "#E11C1C",  # Red
            "#00AA55",  # Green
            "#FF9900",  # Orange
            "#8844EE",  # Group
            "--display-name",
            "Modern Blue",
            "--description",
            "A modern theme with individual color palettes",
            "--author",
            "Example User",
            "--tags",
            "blue,modern,individual",
            "--overwrite",
        ],
        "Generate theme from individual colors (new approach)",
    )
    
    # Example 2: Generate theme from specific colors (legacy approach)
    run_command(
        [
            "python",
            "-m",
            "themeweaver.cli",
            "generate",
            "ocean_blue",
            "--colors",
            "#051F36",
            "#EEE8D5",
            "#222C33",
            "#FDF6E3",
            "--display-name",
            "Ocean Blue",
            "--description",
            "A calming ocean-inspired theme",
            "--author",
            "Example User",
            "--tags",
            "blue,ocean,calm",
            "--method",
            "lch",
            "--overwrite",
        ],
        "Generate theme from specific colors (legacy approach)",
    )

    # Example 3: Generate theme using algorithmic approach
    run_command(
        [
            "python",
            "-m",
            "themeweaver.cli",
            "generate",
            "sunset_warm",
            "--palette-name",
            "SunsetWarm",
            "--start-hue",
            "20",
            "--num-colors",
            "12",
            "--target-delta-e",
            "25",
            "--display-name",
            "Sunset Warm",
            "--description",
            "A warm sunset-inspired theme",
            "--author",
            "Example User",
            "--tags",
            "warm,sunset,orange",
            "--overwrite",
        ],
        "Generate theme using algorithmic approach",
    )

    # Example 4: Generate theme with uniform hue distribution
    run_command(
        [
            "python",
            "-m",
            "themeweaver.cli",
            "generate",
            "rainbow_uniform",
            "--palette-name",
            "RainbowUniform",
            "--start-hue",
            "0",
            "--num-colors",
            "12",
            "--uniform",
            "--display-name",
            "Rainbow Uniform",
            "--description",
            "A theme with uniform hue distribution",
            "--author",
            "Example User",
            "--tags",
            "rainbow,uniform,colorful",
            "--overwrite",
        ],
        "Generate theme with uniform hue distribution",
    )

    # Example 5: List all themes including newly generated ones
    run_command(
        ["python", "-m", "themeweaver.cli", "list"], "List all available themes"
    )

    # Example 6: Validate a generated theme
    run_command(
        ["python", "-m", "themeweaver.cli", "validate", "ocean_blue"],
        "Validate the ocean_blue theme",
    )

    print("\n🎉 Theme generation examples completed!")
    print("💡 You can now use these themes with: themeweaver export --theme THEME_NAME")


if __name__ == "__main__":
    main()
