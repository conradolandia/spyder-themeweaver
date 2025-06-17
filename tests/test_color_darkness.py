#!/usr/bin/env python3
"""Unit tests for color darkness detection functionality."""

import sys
import unittest
import yaml
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from themeweaver.color_utils import is_color_dark, get_color_brightness_info


class TestColorDarkness(unittest.TestCase):
    """Test cases for color darkness detection functions."""

    def test_is_color_dark_basic(self):
        """Test basic dark/light color detection."""
        # Test clearly dark colors
        self.assertTrue(is_color_dark("#000000"))  # Black
        self.assertTrue(is_color_dark("#191919"))  # Very dark gray
        self.assertTrue(is_color_dark("#333333"))  # Dark gray
        
        # Test clearly light colors
        self.assertFalse(is_color_dark("#FFFFFF"))  # White
        self.assertFalse(is_color_dark("#CCCCCC"))  # Light gray
        self.assertFalse(is_color_dark("#999999"))  # Medium-light gray

    def test_is_color_dark_primary_colors(self):
        """Test primary colors which have interesting lightness values."""
        # Red has moderate lightness (~53) - should be light with default threshold
        self.assertFalse(is_color_dark("#FF0000"))
        
        # Green is quite light (~88) - should be light
        self.assertFalse(is_color_dark("#00FF00"))
        
        # Blue is relatively dark (~32) - should be dark
        self.assertTrue(is_color_dark("#0000FF"))
        
        # Yellow is very light (~97) - should be light
        self.assertFalse(is_color_dark("#FFFF00"))

    def test_is_color_dark_custom_threshold(self):
        """Test color darkness with custom thresholds."""
        red = "#FF0000"  # Lightness ~53
        
        # With low threshold, red should be light
        self.assertFalse(is_color_dark(red, threshold=30.0))
        
        # With high threshold, red should be dark
        self.assertTrue(is_color_dark(red, threshold=60.0))

    def test_is_color_dark_edge_cases(self):
        """Test edge cases and error handling."""
        # Test invalid hex colors
        with self.assertRaises(ValueError):
            is_color_dark("#GGGGGG")  # Invalid hex
            
        with self.assertRaises(ValueError):
            is_color_dark("#FF")  # Too short
            
        with self.assertRaises(ValueError):
            is_color_dark("FF0000")  # Missing #
            
        with self.assertRaises(ValueError):
            is_color_dark("")  # Empty string
            
        with self.assertRaises(ValueError):
            is_color_dark("#")  # Just #

    def test_get_color_brightness_info_structure(self):
        """Test that brightness info returns correct structure."""
        info = get_color_brightness_info("#FF0000")
        
        # Check that all expected keys are present
        expected_keys = {
            'hex', 'lch_lightness', 'rgb_luminance', 'hsv_value',
            'is_dark_lch', 'is_dark_luminance', 'is_dark_hsv'
        }
        self.assertEqual(set(info.keys()), expected_keys)
        
        # Check data types
        self.assertIsInstance(info['hex'], str)
        self.assertIsInstance(info['lch_lightness'], (float, type(None)))
        self.assertIsInstance(info['rgb_luminance'], float)
        self.assertIsInstance(info['hsv_value'], float)
        self.assertIsInstance(info['is_dark_lch'], (bool, type(None)))
        self.assertIsInstance(info['is_dark_luminance'], bool)
        self.assertIsInstance(info['is_dark_hsv'], bool)

    def test_get_color_brightness_info_values(self):
        """Test that brightness info returns reasonable values."""
        # Test black
        black_info = get_color_brightness_info("#000000")
        self.assertAlmostEqual(black_info['lch_lightness'], 0.0, places=1)
        self.assertAlmostEqual(black_info['rgb_luminance'], 0.0, places=3)
        self.assertAlmostEqual(black_info['hsv_value'], 0.0, places=3)
        self.assertTrue(black_info['is_dark_lch'])
        self.assertTrue(black_info['is_dark_luminance'])
        self.assertTrue(black_info['is_dark_hsv'])
        
        # Test white
        white_info = get_color_brightness_info("#FFFFFF")
        self.assertAlmostEqual(white_info['lch_lightness'], 100.0, places=1)
        self.assertAlmostEqual(white_info['rgb_luminance'], 1.0, places=3)
        self.assertAlmostEqual(white_info['hsv_value'], 1.0, places=3)
        self.assertFalse(white_info['is_dark_lch'])
        self.assertFalse(white_info['is_dark_luminance'])
        self.assertFalse(white_info['is_dark_hsv'])

    def test_lch_vs_other_methods(self):
        """Test differences between LCh and other brightness methods."""
        # Red is a good example where different methods disagree
        red_info = get_color_brightness_info("#FF0000")
        
        # Red has moderate LCh lightness but low RGB luminance
        self.assertGreater(red_info['lch_lightness'], 50)  # Light in LCh
        self.assertLess(red_info['rgb_luminance'], 0.5)    # Dark in RGB luminance
        self.assertGreater(red_info['hsv_value'], 0.5)     # Light in HSV
        
        # So LCh and RGB methods should disagree for red
        self.assertNotEqual(red_info['is_dark_lch'], red_info['is_dark_luminance'])

    def test_threshold_boundary(self):
        """Test colors right at the threshold boundary."""
        # Find a color that's right at the 50.0 threshold
        gray = "#808080"  # Should be close to 50
        gray_info = get_color_brightness_info(gray)
        
        # Test with threshold slightly above and below the color's lightness
        lightness = gray_info['lch_lightness']
        
        # Should be dark with threshold above its lightness
        self.assertTrue(is_color_dark(gray, threshold=lightness + 1))
        
        # Should be light with threshold below its lightness
        self.assertFalse(is_color_dark(gray, threshold=lightness - 1))


def test_colorsystem_gradients():
    """Test is_color_dark with gradients from colorsystem.yaml."""
    
    # Load the colorsystem.yaml file
    colorsystem_path = Path(__file__).parent.parent / "src" / "themeweaver" / "themes" / "solarized" / "colorsystem.yaml"
    
    try:
        with open(colorsystem_path, 'r') as f:
            colorsystem = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Could not find colorsystem.yaml at {colorsystem_path}")
        return
    
    print("=== Color Darkness Analysis: Solarized Color System ===\n")
    
    # Test default threshold (40.0)
    threshold = 40.0
    print(f"Using threshold: {threshold:.1f} (colors below this are 'dark')\n")
    
    # Skip some groups that might not be color gradients
    skip_groups = {'GroupDark', 'GroupLight', 'Logos'}
    
    for group_name, colors in colorsystem.items():
        if group_name in skip_groups:
            continue
            
        print(f"{group_name} Gradient:")
        print("-" * 50)
        print(f"{'Level':<6} {'Hex':<9} {'LCh L*':<8} {'Dark?':<6} {'Status'}")
        print("-" * 50)
        
        # Sort by level (B0, B10, B20, etc.)
        sorted_levels = sorted(colors.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 999)
        
        for level in sorted_levels:
            hex_color = colors[level]
            
            # Skip colors with double ## (seems to be a typo in the YAML)
            if hex_color.startswith('##'):
                hex_color = hex_color[1:]  # Remove one #
            
            try:
                is_dark = is_color_dark(hex_color, threshold=threshold)
                brightness_info = get_color_brightness_info(hex_color)
                lightness = brightness_info['lch_lightness']
                
                dark_str = "Yes" if is_dark else "No"
                lightness_str = f"{lightness:.1f}" if lightness is not None else "N/A"
                
                # Add visual indicator
                status = "🌑 DARK" if is_dark else "☀️ LIGHT"
                
                print(f"{level:<6} {hex_color:<9} {lightness_str:<8} {dark_str:<6} {status}")
                
            except Exception as e:
                print(f"{level:<6} {hex_color:<9} ERROR   N/A    ❌ {str(e)}")
        
        print()  # Empty line between groups
    
    # Test with different thresholds for one group
    print("=" * 60)
    print("Threshold Sensitivity Test (Gunmetal Gradient)")
    print("=" * 60)
    
    gunmetal = colorsystem.get('Gunmetal', {})
    test_levels = ['B20', 'B30', 'B40', 'B50', 'B60']  # Middle range colors
    thresholds = [30.0, 40.0, 50.0, 60.0]
    
    print(f"{'Level':<6} {'Hex':<9} {'LCh L*':<8}", end="")
    for thresh in thresholds:
        print(f"T={thresh:<4.0f}", end=" ")
    print()
    print("-" * (6 + 9 + 8 + len(thresholds) * 6))
    
    for level in test_levels:
        if level in gunmetal:
            hex_color = gunmetal[level]
            try:
                brightness_info = get_color_brightness_info(hex_color)
                lightness = brightness_info['lch_lightness']
                lightness_str = f"{lightness:.1f}" if lightness is not None else "N/A"
                
                print(f"{level:<6} {hex_color:<9} {lightness_str:<8}", end="")
                
                for thresh in thresholds:
                    is_dark = is_color_dark(hex_color, threshold=thresh)
                    result = "D" if is_dark else "L"
                    print(f"{result:<5}", end=" ")
                print()
                
            except Exception as e:
                print(f"{level:<6} {hex_color:<9} ERROR   {str(e)}")
    
    print("\nLegend: D=Dark, L=Light")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gradients":
        test_colorsystem_gradients()
    else:
        unittest.main() 
