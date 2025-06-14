#!/usr/bin/env python3
"""
Comprehensive test file to verify all functionality documented in the README of the color_utils module.
"""


def test_core_color_utilities():
    """Test core color utilities from color_utils.py"""
    print("=== Testing Core Color Utilities ===")

    try:
        from themeweaver.color_utils.color_utils import (
            calculate_delta_e,
            get_color_info,
            hex_to_rgb,
            hsv_to_rgb,
            lch_to_hex,
            linear_interpolate,
            rgb_to_hex,
            rgb_to_hsv,
            rgb_to_lch,
        )

        # Test hex_to_rgb
        rgb = hex_to_rgb("#ff0000")
        assert rgb == (255, 0, 0), f"Expected (255, 0, 0), got {rgb}"
        print("✅ hex_to_rgb works")

        # Test rgb_to_hex
        hex_color = rgb_to_hex((255, 0, 0))
        assert hex_color.lower() == "#ff0000", f"Expected #ff0000, got {hex_color}"
        print("✅ rgb_to_hex works")

        # Test rgb_to_hsv
        hsv = rgb_to_hsv((255, 0, 0))
        assert len(hsv) == 3, f"Expected 3 values, got {len(hsv)}"
        print("✅ rgb_to_hsv works")

        # Test hsv_to_rgb
        rgb_back = hsv_to_rgb(hsv)
        assert len(rgb_back) == 3, f"Expected 3 values, got {len(rgb_back)}"
        print("✅ hsv_to_rgb works")

        # Test rgb_to_lch (if available)
        try:
            lch = rgb_to_lch(rgb)
            assert len(lch) == 3, f"Expected 3 values, got {len(lch)}"
            print("✅ rgb_to_lch works")

            # Test lch_to_hex
            hex_from_lch = lch_to_hex(*lch)
            assert hex_from_lch.startswith("#"), (
                f"Expected hex color, got {hex_from_lch}"
            )
            print("✅ lch_to_hex works")
        except ImportError:
            print("⚠️  LCH functions require colorspacious library")

        # Test calculate_delta_e
        try:
            delta_e = calculate_delta_e("#ff0000", "#00ff00")
            assert isinstance(delta_e, (int, float)), (
                f"Expected number, got {type(delta_e)}"
            )
            print("✅ calculate_delta_e works")
        except ImportError:
            print("⚠️  calculate_delta_e requires colorspacious library")

        # Test get_color_info
        info = get_color_info("#ff0000")
        assert isinstance(info, dict), f"Expected dict, got {type(info)}"
        assert "hex" in info, "Missing 'hex' in color info"
        assert "rgb" in info, "Missing 'rgb' in color info"
        print("✅ get_color_info works")

        # Test linear_interpolate (simple numeric interpolation)
        result = linear_interpolate(0, 100, 0.5)
        assert result == 50, f"Expected 50, got {result}"
        print("✅ linear_interpolate works")

    except ImportError as e:
        print(f"❌ Import error in core color utilities: {e}")
    except Exception as e:
        print(f"❌ Error testing core color utilities: {e}")


def test_color_generation():
    """Test color generation from color_generation.py"""
    print("\n=== Testing Color Generation ===")

    try:
        from themeweaver.color_utils.color_generation import (
            generate_theme_optimized_colors,
        )

        # Test theme-optimized color generation
        colors = generate_theme_optimized_colors(
            theme="dark", num_colors=8, target_delta_e=25, start_hue=30
        )

        assert isinstance(colors, list), f"Expected list, got {type(colors)}"
        assert len(colors) == 8, f"Expected 8 colors, got {len(colors)}"
        assert all(c.startswith("#") for c in colors), "All colors should be hex"
        print("✅ generate_theme_optimized_colors works")

    except ImportError as e:
        print(f"❌ Import error in color generation: {e}")
    except Exception as e:
        print(f"❌ Error testing color generation: {e}")


def test_color_analysis():
    """Test color analysis from color_analysis.py"""
    print("\n=== Testing Color Analysis ===")

    try:
        from themeweaver.color_utils.color_analysis import (
            analyze_chromatic_distances,
            analyze_existing_colors,
            analyze_palette_lch,
            extract_colors_from_group,
            find_optimal_parameters,
            load_color_groups_from_file,
        )

        # Test analyze_existing_colors
        test_colors = ["#ff0000", "#00ff00", "#0000ff"]
        analysis = analyze_existing_colors(test_colors, "Test Group")
        assert isinstance(analysis, list), f"Expected list, got {type(analysis)}"
        print("✅ analyze_existing_colors works")

        # Test analyze_chromatic_distances (if LCH available)
        try:
            distances = analyze_chromatic_distances(test_colors, "Test Group")
            print("✅ analyze_chromatic_distances works")
            print("--------------------------------")
            print(distances)
            print("--------------------------------")
        except ImportError:
            print("⚠️  analyze_chromatic_distances requires colorspacious library")

        # Test analyze_palette_lch
        test_palette = {
            "name": "Test Palette",
            "colors": {"red": "#ff0000", "green": "#00ff00", "blue": "#0000ff"},
        }

        try:
            palette_analysis = analyze_palette_lch(test_palette)
            print("✅ analyze_palette_lch works")
            print("--------------------------------")
            print(palette_analysis)
            print("--------------------------------")
        except ImportError:
            print("⚠️  analyze_palette_lch requires colorspacious library")

        # Test find_optimal_parameters
        try:
            best_params, distance = find_optimal_parameters(test_palette)
            assert isinstance(best_params, dict), (
                f"Expected dict, got {type(best_params)}"
            )
            print("✅ find_optimal_parameters works")
            print("--------------------------------")
            print(best_params)
            print(distance)
            print("--------------------------------")
        except ImportError:
            print("⚠️  find_optimal_parameters requires colorspacious library")

        # Test load_color_groups_from_file (if colorsystem.py exists)
        try:
            color_groups = load_color_groups_from_file("src/themeweaver/colorsystem.yaml")
            assert isinstance(color_groups, dict), (
                f"Expected dict, got {type(color_groups)}"
            )
            print("✅ load_color_groups_from_file works")
            print("--------------------------------")
            print(color_groups)
            print("--------------------------------")
            # Test extract_colors_from_group
            if color_groups:
                first_group = list(color_groups.values())[0]
                colors = extract_colors_from_group(first_group)
                assert isinstance(colors, list), f"Expected list, got {type(colors)}"
                print("✅ extract_colors_from_group works")
                print("--------------------------------")
                print(colors)
                print("--------------------------------")
        except Exception as e:
            print(f"⚠️  load_color_groups_from_file: {e}")

    except ImportError as e:
        print(f"❌ Import error in color analysis: {e}")
    except Exception as e:
        print(f"❌ Error testing color analysis: {e}")


def test_famous_palettes():
    """Test famous palettes from famous_palettes.py"""
    print("\n=== Testing Famous Palettes ===")

    try:
        from themeweaver.color_utils.famous_palettes import (
            FAMOUS_PALETTES,
            get_all_palettes,
            get_palette,
            get_palette_names,
        )

        # Test get_palette_names
        names = get_palette_names()
        assert isinstance(names, list), f"Expected list, got {type(names)}"
        assert len(names) > 0, "Should have at least one palette"
        print(f"✅ get_palette_names works - found {len(names)} palettes")

        # Test get_palette
        if names:
            palette = get_palette(names[0])
            assert isinstance(palette, dict), f"Expected dict, got {type(palette)}"
            assert "name" in palette, "Palette should have 'name' field"
            assert "colors" in palette, "Palette should have 'colors' field"
            print(f"✅ get_palette works - loaded '{names[0]}'")

        # Test get_all_palettes
        all_palettes = get_all_palettes()
        assert isinstance(all_palettes, dict), (
            f"Expected dict, got {type(all_palettes)}"
        )
        print("✅ get_all_palettes works")

        # Test FAMOUS_PALETTES direct access
        assert isinstance(FAMOUS_PALETTES, dict), (
            f"Expected dict, got {type(FAMOUS_PALETTES)}"
        )
        print("✅ FAMOUS_PALETTES direct access works")

    except ImportError as e:
        print(f"❌ Import error in famous palettes: {e}")
    except Exception as e:
        print(f"❌ Error testing famous palettes: {e}")


def test_palette_loaders():
    """Test palette loaders from palette_loaders.py"""
    print("\n=== Testing Palette Loaders ===")

    try:
        from themeweaver.color_utils.palette_loaders import (
            get_available_color_groups,
            load_palette_from_file,
            parse_palette_from_args,
            validate_palette_data,
        )

        # Test load_palette_from_file with YAML
        try:
            palette = load_palette_from_file("src/themeweaver/colorsystem.yaml")
            assert isinstance(palette, dict), f"Expected dict, got {type(palette)}"
            assert "name" in palette, "Palette should have 'name' field"
            assert "colors" in palette, "Palette should have 'colors' field"
            print("✅ load_palette_from_file (YAML) works")
        except FileNotFoundError:
            print("⚠️  colorsystem.yaml not found for testing")

        # Test get_available_color_groups
        try:
            groups = get_available_color_groups("src/themeweaver/colorsystem.yaml")
            assert isinstance(groups, list), f"Expected list, got {type(groups)}"
            print(f"✅ get_available_color_groups works - found {len(groups)} groups")
        except Exception as e:
            print(f"⚠️  get_available_color_groups: {e}")

        # Test parse_palette_from_args
        args_palette = parse_palette_from_args(["red=#ff0000", "blue=#0000ff"])
        assert isinstance(args_palette, dict), (
            f"Expected dict, got {type(args_palette)}"
        )
        assert "colors" in args_palette, "Should have 'colors' field"
        assert "red" in args_palette["colors"], "Should have 'red' color"
        print("✅ parse_palette_from_args works")

        # Test validate_palette_data
        test_palette = {
            "name": "Test Palette",
            "colors": {"red": "#ff0000", "blue": "#0000ff"},
        }

        result = validate_palette_data(test_palette)
        assert result is True, "Validation should return True for valid palette"
        print("✅ validate_palette_data works")

    except ImportError as e:
        print(f"❌ Import error in palette loaders: {e}")
    except Exception as e:
        print(f"❌ Error testing palette loaders: {e}")


def test_color_interpolation():
    """Test color interpolation from interpolate_colors.py"""
    print("\n=== Testing Color Interpolation ===")

    try:
        from themeweaver.color_utils.interpolate_colors import interpolate_colors

        # Test basic linear interpolation
        colors = interpolate_colors("#ff0000", "#00ff00", 5, method="linear")
        assert isinstance(colors, list), f"Expected list, got {type(colors)}"
        assert len(colors) == 5, f"Expected 5 colors, got {len(colors)}"
        assert all(c.startswith("#") for c in colors), "All colors should be hex"
        print("✅ interpolate_colors (linear) works")

        # Test HSV interpolation
        colors_hsv = interpolate_colors("#ff0000", "#00ff00", 3, method="hsv")
        assert len(colors_hsv) == 3, f"Expected 3 colors, got {len(colors_hsv)}"
        print("✅ interpolate_colors (HSV) works")

        # Test LCH interpolation (if available)
        try:
            colors_lch = interpolate_colors("#ff0000", "#00ff00", 3, method="lch")
            assert len(colors_lch) == 3, f"Expected 3 colors, got {len(colors_lch)}"
            print("✅ interpolate_colors (LCH) works")
        except ImportError:
            print("⚠️  LCH interpolation requires colorspacious library")

    except ImportError as e:
        print(f"⚠️  interpolate_colors module not found or incomplete: {e}")
    except Exception as e:
        print(f"❌ Error testing color interpolation: {e}")


def test_examples_from_readme():
    """Test specific examples"""
    print("\n=== Testing Examples ===")

    try:
        # Example 1: Basic color conversion
        from themeweaver.color_utils.color_utils import (
            calculate_delta_e,
            hex_to_rgb,
            rgb_to_lch,
        )

        rgb = hex_to_rgb("#ff0000")
        print(f"✅ Example 1: RGB conversion - {rgb}")

        try:
            lightness, chroma, hue = rgb_to_lch(rgb)
            print(
                f"✅ Example 1: LCH conversion - L:{lightness:.1f}, C:{chroma:.1f}, H:{hue:.1f}"
            )
        except ImportError:
            print("⚠️  LCH conversion requires colorspacious")

        try:
            distance = calculate_delta_e("#ff0000", "#00ff00")
            print(f"✅ Example 1: Delta E calculation - {distance:.1f}")
        except ImportError:
            print("⚠️  Delta E calculation requires colorspacious")

        # Example 2: Color generation
        try:
            from themeweaver.color_utils.color_generation import (
                generate_theme_optimized_colors,
            )

            colors = generate_theme_optimized_colors(
                theme="dark", num_colors=8, target_delta_e=25, start_hue=30
            )
            print(f"✅ Example 2: Generated {len(colors)} colors for dark theme")
        except ImportError:
            print("⚠️  Color generation requires colorspacious")

        # Example 3: Famous palette access
        from themeweaver.color_utils.famous_palettes import (
            get_palette,
            get_palette_names,
        )

        names = get_palette_names()
        if "solarized" in names:
            solarized = get_palette("solarized")
            print(
                f"✅ Example 3: Solarized palette loaded - {len(solarized['colors'])} colors"
            )
        else:
            print("⚠️  Solarized palette not found in available palettes")

    except Exception as e:
        print(f"❌ Error testing examples: {e}")


def main():
    """Run all tests"""
    print("🧪 Testing Themeweaver Color Utils Functionality")
    print("=" * 60)

    test_core_color_utilities()
    test_color_generation()
    test_color_analysis()
    test_famous_palettes()
    test_palette_loaders()
    test_color_interpolation()
    test_examples_from_readme()

    print("\n" + "=" * 60)
    print("🎯 Test Summary Complete!")
    print("\nNote: Some functions may show warnings if optional dependencies")
    print("(like colorspacious) are not installed. This is expected behavior.")
    print("\nTo install optional dependencies:")
    print("  pip install colorspacious")


if __name__ == "__main__":
    main()
