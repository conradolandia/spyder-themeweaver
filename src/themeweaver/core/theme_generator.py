"""
Theme generator for creating new Spyder themes.

This module provides functionality to generate complete theme definition files
using the existing color generation utilities from themeweaver.color_utils.
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from themeweaver.color_utils.color_generation import (
    generate_theme_optimized_colors,
    generate_group_uniform_palette,
)
from themeweaver.color_utils.color_names import (
    get_palette_name_from_color,
    get_multiple_color_names,
    calculate_color_distance,
)
from themeweaver.color_utils.interpolate_colors import (
    interpolate_colors_spyder,
    validate_spyder_colors,
)
from themeweaver.color_utils import rgb_to_lch, hex_to_rgb, lch_to_hex

_logger = logging.getLogger(__name__)


class ThemeGenerator:
    """Generator for creating complete Spyder theme definitions."""

    def __init__(self, themes_dir: Optional[Path] = None):
        """Initialize the theme generator.

        Args:
            themes_dir: Directory where themes are stored. If None, uses default.
        """
        if themes_dir is None:
            themes_dir = Path(__file__).parent.parent / "themes"

        self.themes_dir = Path(themes_dir)
        self.themes_dir.mkdir(exist_ok=True)

    def generate_theme_from_colors(
        self,
        theme_name: str,
        primary_colors: Tuple[str, str],
        secondary_colors: Tuple[str, str],
        method: str = "lch",
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        author: str = "ThemeWeaver",
        tags: Optional[List[str]] = None,
        use_creative_names: bool = True,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Generate a complete theme from primary and secondary color pairs.

        Args:
            theme_name: Name for the theme (used for directory name)
            primary_colors: Tuple of (dark_color, light_color) for primary palette
            secondary_colors: Tuple of (dark_color, light_color) for secondary palette
            method: Interpolation method for color generation
            display_name: Human-readable theme name
            description: Theme description
            author: Theme author
            tags: List of tags for the theme
            use_creative_names: Whether to use creative names for color palettes
            overwrite: Whether to overwrite existing theme

        Returns:
            Dict with paths to generated files
        """
        # Validate colors
        self._validate_color_pairs(primary_colors, secondary_colors)

        # Create theme directory
        theme_dir = self.themes_dir / theme_name
        if theme_dir.exists() and not overwrite:
            raise ValueError(
                f"Theme '{theme_name}' already exists. Use overwrite=True to replace."
            )

        theme_dir.mkdir(exist_ok=True)

        # Generate color palettes
        _logger.info(f"🎨 Generating color palettes for theme '{theme_name}'...")
        colorsystem_data = self._generate_colorsystem(
            primary_colors, secondary_colors, method, use_creative_names
        )

        # Generate theme metadata
        theme_data = self._generate_theme_metadata(
            theme_name, display_name, description, author, tags
        )

        # Generate color mappings
        mappings_data = self._generate_mappings(colorsystem_data)

        # Write files
        files = {}
        files["theme.yaml"] = self._write_yaml_file(
            theme_dir / "theme.yaml", theme_data
        )
        files["colorsystem.yaml"] = self._write_yaml_file(
            theme_dir / "colorsystem.yaml", colorsystem_data
        )
        files["mappings.yaml"] = self._write_yaml_file(
            theme_dir / "mappings.yaml", mappings_data
        )

        _logger.info(f"✅ Theme '{theme_name}' generated successfully!")
        return files

    def generate_theme_from_palette(
        self,
        theme_name: str,
        palette_name: str,
        start_hue: Optional[int] = None,
        num_colors: int = 12,
        target_delta_e: float = 25,
        uniform: bool = False,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        author: str = "ThemeWeaver",
        tags: Optional[List[str]] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Generate a theme using algorithmic color generation.

        Args:
            theme_name: Name for the theme (used for directory name)
            palette_name: Name for the primary color palette
            start_hue: Starting hue for color generation (0-360)
            num_colors: Number of colors in group palettes
            target_delta_e: Target perceptual distance between colors
            uniform: Whether to use uniform hue steps instead of perceptual spacing
            display_name: Human-readable theme name
            description: Theme description
            author: Theme author
            tags: List of tags for the theme
            overwrite: Whether to overwrite existing theme

        Returns:
            Dict with paths to generated files
        """
        # Create theme directory
        theme_dir = self.themes_dir / theme_name
        if theme_dir.exists() and not overwrite:
            raise ValueError(
                f"Theme '{theme_name}' already exists. Use overwrite=True to replace."
            )

        theme_dir.mkdir(exist_ok=True)

        # Generate algorithmic color palettes
        _logger.info(
            f"🎨 Generating algorithmic color palettes for theme '{theme_name}'..."
        )
        colorsystem_data = self._generate_algorithmic_colorsystem(
            palette_name, start_hue, num_colors, target_delta_e, uniform
        )

        # Analyze generated colors
        self._analyze_algorithmic_palette(colorsystem_data, palette_name)

        # Generate theme metadata
        theme_data = self._generate_theme_metadata(
            theme_name, display_name, description, author, tags
        )

        # Generate color mappings
        mappings_data = self._generate_mappings(colorsystem_data)

        # Write files
        files = {}
        files["theme.yaml"] = self._write_yaml_file(
            theme_dir / "theme.yaml", theme_data
        )
        files["colorsystem.yaml"] = self._write_yaml_file(
            theme_dir / "colorsystem.yaml", colorsystem_data
        )
        files["mappings.yaml"] = self._write_yaml_file(
            theme_dir / "mappings.yaml", mappings_data
        )

        _logger.info(f"✅ Theme '{theme_name}' generated successfully!")
        return files

    def _validate_color_pairs(
        self, primary_colors: Tuple[str, str], secondary_colors: Tuple[str, str]
    ) -> None:
        """Validate that color pairs are appropriate for theme generation."""
        # Validate primary colors
        is_valid, error_msg = validate_spyder_colors(
            primary_colors[0], primary_colors[1]
        )
        if not is_valid:
            raise ValueError(f"Invalid primary colors: {error_msg}")

        # Validate secondary colors
        is_valid, error_msg = validate_spyder_colors(
            secondary_colors[0], secondary_colors[1]
        )
        if not is_valid:
            raise ValueError(f"Invalid secondary colors: {error_msg}")

        # Check color distances for good contrast
        self._validate_color_distances(primary_colors, secondary_colors)

    def _validate_color_distances(
        self, primary_colors: Tuple[str, str], secondary_colors: Tuple[str, str]
    ) -> None:
        """Validate that colors have sufficient contrast for good theme design."""
        # Check primary color contrast
        primary_distance = calculate_color_distance(
            primary_colors[0], primary_colors[1]
        )
        if primary_distance < 100:  # Minimum distance in RGB space
            _logger.warning(
                "⚠️  Primary colors have low contrast (distance: %.1f). Consider using more contrasting colors.",
                primary_distance,
            )

        # Check secondary color contrast
        secondary_distance = calculate_color_distance(
            secondary_colors[0], secondary_colors[1]
        )
        if secondary_distance < 100:
            _logger.warning(
                "⚠️  Secondary colors have low contrast (distance: %.1f). Consider using more contrasting colors.",
                secondary_distance,
            )

        # Check primary vs secondary distinction
        cross_distance1 = calculate_color_distance(
            primary_colors[0], secondary_colors[0]
        )
        cross_distance2 = calculate_color_distance(
            primary_colors[1], secondary_colors[1]
        )

        if cross_distance1 < 50 or cross_distance2 < 50:
            _logger.warning(
                "⚠️  Primary and secondary colors are very similar. Consider using more distinct color families."
            )

        _logger.info("✅ Color distance validation completed")
        _logger.info(f"  Primary contrast: {primary_distance:.1f}")
        _logger.info(f"  Secondary contrast: {secondary_distance:.1f}")
        _logger.info(f"  Cross distances: {cross_distance1:.1f}, {cross_distance2:.1f}")

    def _log_color_analysis(
        self,
        primary_colors: Tuple[str, str],
        secondary_colors: Tuple[str, str],
        color_names: Dict[str, str],
    ) -> None:
        """Log detailed color analysis for the generated theme."""
        _logger.info("🎨 Color Analysis:")
        _logger.info(
            f"  Primary Dark:  {primary_colors[0]} → {color_names.get(primary_colors[0], 'Unknown')}"
        )
        _logger.info(
            f"  Primary Light: {primary_colors[1]} → {color_names.get(primary_colors[1], 'Unknown')}"
        )
        _logger.info(
            f"  Secondary Dark:  {secondary_colors[0]} → {color_names.get(secondary_colors[0], 'Unknown')}"
        )
        _logger.info(
            f"  Secondary Light: {secondary_colors[1]} → {color_names.get(secondary_colors[1], 'Unknown')}"
        )

    def _analyze_algorithmic_palette(
        self, colorsystem_data: Dict, palette_name: str
    ) -> None:
        """Analyze and log information about algorithmically generated palettes."""
        if palette_name in colorsystem_data:
            palette = colorsystem_data[palette_name]

            # Get a sample of colors for analysis (e.g., B10, B50, B100, B140)
            sample_colors = []
            for step in [10, 50, 100, 140]:
                key = f"B{step}"
                if key in palette:
                    sample_colors.append(palette[key])

            if sample_colors:
                # Get color names for sample colors
                color_names = get_multiple_color_names(sample_colors)

                _logger.info(f"🎨 Algorithmic Palette Analysis for '{palette_name}':")
                for i, color in enumerate(sample_colors):
                    step = [10, 50, 100, 140][i]
                    name = color_names.get(color, "Unknown")
                    _logger.info(f"  B{step}: {color} → {name}")

                # Calculate color distances within palette
                if len(sample_colors) >= 2:
                    distances = []
                    for i in range(len(sample_colors) - 1):
                        dist = calculate_color_distance(
                            sample_colors[i], sample_colors[i + 1]
                        )
                        distances.append(dist)

                    avg_distance = sum(distances) / len(distances)
                    _logger.info(f"  Average color distance: {avg_distance:.1f}")

                    if avg_distance < 50:
                        _logger.warning("⚠️  Colors in palette may be too similar")
                    elif avg_distance > 200:
                        _logger.warning("⚠️  Colors in palette may be too contrasting")
                    else:
                        _logger.info("✅ Good color distribution in palette")

    def _generate_colorsystem(
        self,
        primary_colors: Tuple[str, str],
        secondary_colors: Tuple[str, str],
        method: str,
        use_creative_names: bool,
    ) -> Dict:
        """Generate the colorsystem.yaml content."""
        colorsystem = {}

        # Generate primary palette
        primary_palette = interpolate_colors_spyder(
            primary_colors[0], primary_colors[1], method
        )

        # Generate secondary palette
        secondary_palette = interpolate_colors_spyder(
            secondary_colors[0], secondary_colors[1], method
        )

        # Get color names for analysis (batch API call for efficiency)
        all_colors = [
            primary_colors[0],
            primary_colors[1],
            secondary_colors[0],
            secondary_colors[1],
        ]
        color_names = get_multiple_color_names(all_colors)

        # Generate palette names with enhanced analysis
        if use_creative_names:
            primary_name = get_palette_name_from_color(primary_colors[0], creative=True)
            secondary_name = get_palette_name_from_color(
                secondary_colors[0], creative=True
            )
        else:
            primary_name = get_palette_name_from_color(
                primary_colors[0], creative=False
            )
            secondary_name = get_palette_name_from_color(
                secondary_colors[0], creative=False
            )

        # Log color analysis
        self._log_color_analysis(primary_colors, secondary_colors, color_names)

        # Add primary palette
        colorsystem[primary_name] = {}
        for i, color in enumerate(primary_palette):
            step = i * 10
            colorsystem[primary_name][f"B{step}"] = color

        # Add secondary palette
        colorsystem[secondary_name] = {}
        for i, color in enumerate(secondary_palette):
            step = i * 10
            colorsystem[secondary_name][f"B{step}"] = color

        # Add standard palettes (Green, Red, Orange)
        colorsystem.update(self._generate_standard_palettes(primary_colors, method))

        # Add Group palettes
        colorsystem.update(self._generate_group_palettes())

        # Add Logos palette
        colorsystem.update(self._generate_logos_palette())

        # Store palette names for mappings
        colorsystem["_palette_names"] = {
            "primary": primary_name,
            "secondary": secondary_name,
        }

        return colorsystem

    def _generate_algorithmic_colorsystem(
        self,
        palette_name: str,
        start_hue: Optional[int],
        num_colors: int,
        target_delta_e: float,
        uniform: bool,
    ) -> Dict:
        """Generate colorsystem using algorithmic color generation."""
        colorsystem = {}

        # Generate primary palette using algorithmic approach
        if uniform:
            # For uniform generation, get colors for dark/light endpoints
            dark_colors = generate_group_uniform_palette(
                "dark", 4
            )  # Get 4 colors to have options
            light_colors = generate_group_uniform_palette("light", 4)

            # Use first (darkest) and last (lightest) for interpolation endpoints
            primary_dark = dark_colors[0]
            primary_light = light_colors[-1]

            # Use second darkest and second lightest for secondary
            secondary_dark = dark_colors[1] if len(dark_colors) > 1 else dark_colors[0]
            secondary_light = (
                light_colors[-2] if len(light_colors) > 1 else light_colors[-1]
            )
        else:
            # For optimized generation, create colors suitable for Spyder endpoints
            dark_colors = generate_theme_optimized_colors(
                theme="dark",
                start_hue=start_hue,
                num_colors=4,
                target_delta_e=target_delta_e,
            )
            light_colors = generate_theme_optimized_colors(
                theme="light",
                start_hue=start_hue,
                num_colors=4,
                target_delta_e=target_delta_e,
            )

            # Use first and last colors as endpoints for primary palette
            primary_dark = dark_colors[0]
            primary_light = light_colors[-1]

            # Use middle colors for secondary palette to create variation
            secondary_dark = dark_colors[1] if len(dark_colors) > 1 else dark_colors[0]
            secondary_light = (
                light_colors[-2] if len(light_colors) > 1 else light_colors[-1]
            )

        # Generate Spyder-compliant palettes using interpolate_colors_spyder
        primary_palette = interpolate_colors_spyder(primary_dark, primary_light, "lch")
        secondary_palette = interpolate_colors_spyder(
            secondary_dark, secondary_light, "lch"
        )

        # Add primary palette with proper B-step format
        colorsystem[palette_name] = {}
        for i, color in enumerate(primary_palette):
            step = i * 10
            colorsystem[palette_name][f"B{step}"] = color

        # Create secondary palette name and add it
        secondary_name = f"{palette_name}Light"
        colorsystem[secondary_name] = {}
        for i, color in enumerate(secondary_palette):
            step = i * 10
            colorsystem[secondary_name][f"B{step}"] = color

        # Add standard palettes
        colorsystem.update(self._generate_standard_palettes())

        # Add Group palettes
        colorsystem.update(
            self._generate_group_palettes(
                start_hue, num_colors, target_delta_e, uniform
            )
        )

        # Add Logos palette
        colorsystem.update(self._generate_logos_palette())

        # Store palette names for mappings
        colorsystem["_palette_names"] = {
            "primary": palette_name,
            "secondary": secondary_name,
        }

        return colorsystem

    def _generate_standard_palettes(
        self, primary_colors: Optional[Tuple[str, str]] = None, method: str = "lch"
    ) -> Dict:
        """Generate standard Green, Red, Orange palettes using dynamic color generation.

        Args:
            primary_colors: Tuple of (dark_color, light_color) for primary palette (if available)
                          If provided, uses these colors' characteristics for harmonization
            method: Interpolation method for color generation

        Returns:
            Dict with Green, Red, Orange palettes
        """
        # Define color wheel regions
        GREEN_HUE = 120  # Green region
        RED_HUE = 0  # Red region
        ORANGE_HUE = 30  # Orange-yellow region

        # Determine base characteristics for harmonization
        if primary_colors:
            # Extract characteristics from user-provided colors for harmonization
            # Get LCH characteristics from primary colors to harmonize standard palettes
            primary_dark_lch = rgb_to_lch(hex_to_rgb(primary_colors[0]))
            primary_light_lch = rgb_to_lch(hex_to_rgb(primary_colors[1]))

            # Use average lightness and chroma characteristics for harmonization
            base_lightness_dark = primary_dark_lch[0]
            base_lightness_light = primary_light_lch[0]
            base_chroma = (primary_dark_lch[1] + primary_light_lch[1]) / 2

            # Generate harmonized colors using user color characteristics
            green_dark = lch_to_hex(base_lightness_dark, base_chroma, GREEN_HUE)
            green_light = lch_to_hex(base_lightness_light, base_chroma, GREEN_HUE)

            red_dark = lch_to_hex(base_lightness_dark, base_chroma, RED_HUE)
            red_light = lch_to_hex(base_lightness_light, base_chroma, RED_HUE)

            orange_dark = lch_to_hex(base_lightness_dark, base_chroma, ORANGE_HUE)
            orange_light = lch_to_hex(base_lightness_light, base_chroma, ORANGE_HUE)

        else:
            # Use algorithmic generation with specific hue regions
            # For standard palettes, generate more subdued colors that work well with black/white endpoints
            # Use moderate lightness and chroma values to avoid jarring transitions

            # Define more conservative LCH values for smooth gradients
            DARK_LIGHTNESS = 15  # Dark enough to transition smoothly from black
            LIGHT_LIGHTNESS = 85  # Light enough to transition smoothly to white
            MODERATE_CHROMA = 50  # Moderate saturation to avoid harsh jumps

            # Generate harmonized colors using conservative LCH values
            green_dark = lch_to_hex(DARK_LIGHTNESS, MODERATE_CHROMA, GREEN_HUE)
            green_light = lch_to_hex(LIGHT_LIGHTNESS, MODERATE_CHROMA, GREEN_HUE)

            red_dark = lch_to_hex(DARK_LIGHTNESS, MODERATE_CHROMA, RED_HUE)
            red_light = lch_to_hex(LIGHT_LIGHTNESS, MODERATE_CHROMA, RED_HUE)

            orange_dark = lch_to_hex(DARK_LIGHTNESS, MODERATE_CHROMA, ORANGE_HUE)
            orange_light = lch_to_hex(LIGHT_LIGHTNESS, MODERATE_CHROMA, ORANGE_HUE)

        # Generate full 16-color palettes using interpolate_colors_spyder
        green_palette = interpolate_colors_spyder(green_dark, green_light, method)
        red_palette = interpolate_colors_spyder(red_dark, red_light, method)
        orange_palette = interpolate_colors_spyder(orange_dark, orange_light, method)

        # Convert to B-step format
        standard_palettes = {}

        # Add Green palette
        standard_palettes["Green"] = {}
        for i, color in enumerate(green_palette):
            step = i * 10
            standard_palettes["Green"][f"B{step}"] = color

        # Add Red palette
        standard_palettes["Red"] = {}
        for i, color in enumerate(red_palette):
            step = i * 10
            standard_palettes["Red"][f"B{step}"] = color

        # Add Orange palette
        standard_palettes["Orange"] = {}
        for i, color in enumerate(orange_palette):
            step = i * 10
            standard_palettes["Orange"][f"B{step}"] = color

        return standard_palettes

    def _generate_group_palettes(
        self,
        start_hue: Optional[int] = None,
        num_colors: int = 12,
        target_delta_e: float = 25,
        uniform: bool = False,
    ) -> Dict:
        """Generate GroupDark and GroupLight palettes."""
        if uniform:
            dark_colors = generate_group_uniform_palette("dark", num_colors)
            light_colors = generate_group_uniform_palette("light", num_colors)
        else:
            dark_colors = generate_theme_optimized_colors(
                theme="dark",
                start_hue=start_hue,
                num_colors=num_colors,
                target_delta_e=target_delta_e,
            )
            light_colors = generate_theme_optimized_colors(
                theme="light",
                start_hue=start_hue,
                num_colors=num_colors,
                target_delta_e=target_delta_e,
            )

        group_palettes = {"GroupDark": {}, "GroupLight": {}}

        # Add GroupDark colors
        for i, color in enumerate(dark_colors):
            step = (i + 1) * 10
            group_palettes["GroupDark"][f"B{step}"] = color

        # Add GroupLight colors
        for i, color in enumerate(light_colors):
            step = (i + 1) * 10
            group_palettes["GroupLight"][f"B{step}"] = color

        return group_palettes

    def _generate_logos_palette(self) -> Dict:
        """Generate standard Logos palette."""
        return {
            "Logos": {
                "B10": "#3775a9",
                "B20": "#ffd444",
                "B30": "#414141",
                "B40": "#fafafa",
                "B50": "#ee0000",
            }
        }

    def _generate_theme_metadata(
        self,
        theme_name: str,
        display_name: Optional[str],
        description: Optional[str],
        author: str,
        tags: Optional[List[str]],
    ) -> Dict:
        """Generate theme.yaml content."""
        return {
            "name": theme_name,
            "display_name": display_name or theme_name.replace("_", " ").title(),
            "description": description or f"Generated theme: {theme_name}",
            "author": author,
            "version": "1.0.0",
            "license": "MIT",
            "tags": tags or ["dark", "light", "generated"],
            "variants": {"dark": True, "light": True},
        }

    def _generate_mappings(self, colorsystem_data: Dict) -> Dict:
        """Generate mappings.yaml content."""
        # Extract palette names
        palette_names = colorsystem_data.pop(
            "_palette_names", {"primary": "Primary", "secondary": "Secondary"}
        )

        primary_name = palette_names["primary"]
        secondary_name = palette_names["secondary"]

        return {
            "color_classes": {
                "Primary": primary_name,
                "Secondary": secondary_name,
                "Green": "Green",
                "Red": "Red",
                "Orange": "Orange",
                "GroupDark": "GroupDark",
                "GroupLight": "GroupLight",
                "Logos": "Logos",
            },
            "semantic_mappings": {
                "dark": {
                    # Background colors
                    "COLOR_BACKGROUND_1": "Primary.B10",
                    "COLOR_BACKGROUND_2": "Primary.B20",
                    "COLOR_BACKGROUND_3": "Primary.B30",
                    "COLOR_BACKGROUND_4": "Primary.B40",
                    "COLOR_BACKGROUND_5": "Primary.B50",
                    "COLOR_BACKGROUND_6": "Primary.B60",
                    # Text colors
                    "COLOR_TEXT_1": "Primary.B130",
                    "COLOR_TEXT_2": "Primary.B110",
                    "COLOR_TEXT_3": "Primary.B90",
                    "COLOR_TEXT_4": "Primary.B80",
                    # Accent colors
                    "COLOR_ACCENT_1": "Secondary.B20",
                    "COLOR_ACCENT_2": "Secondary.B40",
                    "COLOR_ACCENT_3": "Secondary.B50",
                    "COLOR_ACCENT_4": "Secondary.B70",
                    "COLOR_ACCENT_5": "Secondary.B80",
                    # Disabled elements
                    "COLOR_DISABLED": "Primary.B70",
                    # Colors for information and feedback in dialogs
                    "COLOR_SUCCESS_1": "Green.B40",
                    "COLOR_SUCCESS_2": "Green.B70",
                    "COLOR_SUCCESS_3": "Green.B90",
                    "COLOR_ERROR_1": "Red.B40",
                    "COLOR_ERROR_2": "Red.B70",
                    "COLOR_ERROR_3": "Red.B110",
                    "COLOR_WARN_1": "Orange.B40",
                    "COLOR_WARN_2": "Orange.B70",
                    "COLOR_WARN_3": "Orange.B90",
                    "COLOR_WARN_4": "Orange.B100",
                    # Icon colors
                    "ICON_1": "Primary.B140",
                    "ICON_2": "Secondary.B80",
                    "ICON_3": "Green.B80",
                    "ICON_4": "Red.B70",
                    "ICON_5": "Orange.B70",
                    "ICON_6": "Primary.B30",
                    # Colors for icons and variable explorer
                    "GROUP_1": "GroupDark.B10",
                    "GROUP_2": "GroupDark.B20",
                    "GROUP_3": "GroupDark.B30",
                    "GROUP_4": "GroupDark.B40",
                    "GROUP_5": "GroupDark.B50",
                    "GROUP_6": "GroupDark.B60",
                    "GROUP_7": "GroupDark.B70",
                    "GROUP_8": "GroupDark.B80",
                    "GROUP_9": "GroupDark.B90",
                    "GROUP_10": "GroupDark.B100",
                    "GROUP_11": "GroupDark.B110",
                    "GROUP_12": "GroupDark.B120",
                    # Colors for highlight in editor
                    "COLOR_HIGHLIGHT_1": "Secondary.B10",
                    "COLOR_HIGHLIGHT_2": "Secondary.B20",
                    "COLOR_HIGHLIGHT_3": "Secondary.B30",
                    "COLOR_HIGHLIGHT_4": "Secondary.B50",
                    # Colors for occurrences from find widget
                    "COLOR_OCCURRENCE_1": "Primary.B10",
                    "COLOR_OCCURRENCE_2": "Primary.B20",
                    "COLOR_OCCURRENCE_3": "Primary.B30",
                    "COLOR_OCCURRENCE_4": "Primary.B50",
                    "COLOR_OCCURRENCE_5": "Primary.B80",
                    # Colors for Spyder and Python logos
                    "PYTHON_LOGO_UP": "Logos.B10",
                    "PYTHON_LOGO_DOWN": "Logos.B20",
                    "SPYDER_LOGO_BACKGROUND": "Logos.B30",
                    "SPYDER_LOGO_WEB": "Logos.B40",
                    "SPYDER_LOGO_SNAKE": "Logos.B50",
                    # For special tabs
                    "SPECIAL_TABS_SEPARATOR": "Primary.B70",
                    "SPECIAL_TABS_SELECTED": "Secondary.B20",
                    # For the heart used to ask for donations
                    "COLOR_HEART": "Secondary.B80",
                    # For editor tooltips
                    "TIP_TITLE_COLOR": "Green.B80",
                    "TIP_CHAR_HIGHLIGHT_COLOR": "Orange.B90",
                    # Tooltip opacity (numeric value, not a color reference)
                    "OPACITY_TOOLTIP": 230,
                },
                "light": {
                    # Background colors
                    "COLOR_BACKGROUND_1": "Primary.B140",
                    "COLOR_BACKGROUND_2": "Primary.B130",
                    "COLOR_BACKGROUND_3": "Primary.B120",
                    "COLOR_BACKGROUND_4": "Primary.B110",
                    "COLOR_BACKGROUND_5": "Primary.B100",
                    "COLOR_BACKGROUND_6": "Primary.B90",
                    # Text colors
                    "COLOR_TEXT_1": "Primary.B10",
                    "COLOR_TEXT_2": "Primary.B20",
                    "COLOR_TEXT_3": "Primary.B50",
                    "COLOR_TEXT_4": "Primary.B70",
                    # Accent colors
                    "COLOR_ACCENT_1": "Secondary.B130",
                    "COLOR_ACCENT_2": "Secondary.B100",
                    "COLOR_ACCENT_3": "Secondary.B90",
                    "COLOR_ACCENT_4": "Secondary.B80",
                    "COLOR_ACCENT_5": "Secondary.B70",
                    # Disabled elements
                    "COLOR_DISABLED": "Primary.B80",
                    # Colors for information and feedback in dialogs
                    "COLOR_SUCCESS_1": "Green.B40",
                    "COLOR_SUCCESS_2": "Green.B70",
                    "COLOR_SUCCESS_3": "Green.B30",
                    "COLOR_ERROR_1": "Red.B40",
                    "COLOR_ERROR_2": "Red.B70",
                    "COLOR_ERROR_3": "Red.B110",
                    "COLOR_WARN_1": "Orange.B40",
                    "COLOR_WARN_2": "Orange.B70",
                    "COLOR_WARN_3": "Orange.B50",
                    "COLOR_WARN_4": "Orange.B40",
                    # Icon colors
                    "ICON_1": "Primary.B30",
                    "ICON_2": "Secondary.B50",
                    "ICON_3": "Green.B30",
                    "ICON_4": "Red.B70",
                    "ICON_5": "Orange.B70",
                    "ICON_6": "Primary.B140",
                    # Colors for icons and variable explorer
                    "GROUP_1": "GroupLight.B10",
                    "GROUP_2": "GroupLight.B20",
                    "GROUP_3": "GroupLight.B30",
                    "GROUP_4": "GroupLight.B40",
                    "GROUP_5": "GroupLight.B50",
                    "GROUP_6": "GroupLight.B60",
                    "GROUP_7": "GroupLight.B70",
                    "GROUP_8": "GroupLight.B80",
                    "GROUP_9": "GroupLight.B90",
                    "GROUP_10": "GroupLight.B100",
                    "GROUP_11": "GroupLight.B110",
                    "GROUP_12": "GroupLight.B120",
                    # Colors for highlight in editor
                    "COLOR_HIGHLIGHT_1": "Secondary.B140",
                    "COLOR_HIGHLIGHT_2": "Secondary.B130",
                    "COLOR_HIGHLIGHT_3": "Secondary.B120",
                    "COLOR_HIGHLIGHT_4": "Secondary.B110",
                    # Colors for occurrences from find widget
                    "COLOR_OCCURRENCE_1": "Primary.B120",
                    "COLOR_OCCURRENCE_2": "Primary.B110",
                    "COLOR_OCCURRENCE_3": "Primary.B100",
                    "COLOR_OCCURRENCE_4": "Primary.B90",
                    "COLOR_OCCURRENCE_5": "Primary.B60",
                    # Colors for Spyder and Python logos
                    "PYTHON_LOGO_UP": "Logos.B10",
                    "PYTHON_LOGO_DOWN": "Logos.B20",
                    "SPYDER_LOGO_BACKGROUND": "Logos.B30",
                    "SPYDER_LOGO_WEB": "Logos.B40",
                    "SPYDER_LOGO_SNAKE": "Logos.B50",
                    # For special tabs
                    "SPECIAL_TABS_SEPARATOR": "Primary.B70",
                    "SPECIAL_TABS_SELECTED": "Secondary.B70",
                    # For the heart used to ask for donations
                    "COLOR_HEART": "Red.B70",
                    # For editor tooltips
                    "TIP_TITLE_COLOR": "Green.B20",
                    "TIP_CHAR_HIGHLIGHT_COLOR": "Orange.B30",
                    # Tooltip opacity (numeric value, not a color reference)
                    "OPACITY_TOOLTIP": 230,
                },
            },
        }

    def _write_yaml_file(self, file_path: Path, data: Dict) -> str:
        """Write data to a YAML file."""
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(
                data, f, default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        _logger.info(f"📝 Created: {file_path}")
        return str(file_path)

    def list_themes(self) -> List[str]:
        """List all available themes."""
        themes = []
        for theme_dir in self.themes_dir.iterdir():
            if theme_dir.is_dir() and not theme_dir.name.startswith("."):
                if (theme_dir / "theme.yaml").exists():
                    themes.append(theme_dir.name)
        return sorted(themes)

    def theme_exists(self, theme_name: str) -> bool:
        """Check if a theme already exists."""
        return (self.themes_dir / theme_name).exists()
