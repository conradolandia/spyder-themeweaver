"""
Optimized color tab implementation that reuses widgets for better performance.
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QLabel,
    QScrollArea,
    QGridLayout,
    QFrame,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtCore import Qt, QTimer
from pathlib import Path
from .ui_tabs import (
    load_colors_from_yaml,
    load_yaml_file,
    _get_cached_yaml_data,
    _set_cached_yaml_data,
    resolve_color_reference,
    resolve_palette_reference,
    create_small_color_swatch,
)


class ColorTab(QWidget):
    """Optimized color tab that reuses widgets for better performance."""

    def __init__(self, theme_name=None, variant=None):
        super().__init__()
        self._current_theme = theme_name
        self._current_variant = variant

        # Cache for created widgets to avoid recreation
        self._base_palette_widgets = {}
        self._semantic_mapping_widgets = {}
        self._last_colors_data = None
        self._last_mappings_data = None

        self._init_ui()

        # Initial update if theme/variant are provided
        if theme_name and variant:
            # Use timer to avoid blocking during initial creation
            QTimer.singleShot(0, self.update_colors)

    def _init_ui(self):
        """Initialize the UI structure."""
        layout = QVBoxLayout(self)

        # Header
        self.header_label = QLabel("Color Palette Preview")
        self.header_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; margin: 10px;"
        )
        layout.addWidget(self.header_label)

        # Create tab widget for different views
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create placeholder tabs (will be populated by update_colors)
        self._create_base_palettes_tab()
        self._create_semantic_mappings_tab()

    def _create_base_palettes_tab(self):
        """Create the base palettes tab structure."""
        self.base_widget = QWidget()
        layout = QVBoxLayout(self.base_widget)

        self.base_scroll_area = QScrollArea()
        self.base_scroll_area.setWidgetResizable(True)

        self.base_container = QWidget()
        self.base_container_layout = QVBoxLayout(self.base_container)

        self.base_scroll_area.setWidget(self.base_container)
        layout.addWidget(self.base_scroll_area)

        self.tab_widget.addTab(self.base_widget, "Base Palettes")

    def _create_semantic_mappings_tab(self):
        """Create the semantic mappings tab structure."""
        self.semantic_widget = QWidget()
        layout = QVBoxLayout(self.semantic_widget)

        self.semantic_scroll_area = QScrollArea()
        self.semantic_scroll_area.setWidgetResizable(True)

        self.semantic_container = QWidget()
        self.semantic_container_layout = QVBoxLayout(self.semantic_container)

        self.semantic_scroll_area.setWidget(self.semantic_container)
        layout.addWidget(self.semantic_scroll_area)

        self.tab_widget.addTab(self.semantic_widget, "Semantic Mappings")

    def update_colors(self):
        """Update colors based on current theme/variant."""
        current_theme = getattr(self, "_current_theme", None)
        current_variant = getattr(self, "_current_variant", None)

        if not current_theme or not current_variant:
            return

        try:
            # Load colors data
            colors_cache_key = f"colors:{current_theme}"
            colors = _get_cached_yaml_data(colors_cache_key)
            if not colors:
                colors = load_colors_from_yaml(current_theme)
                _set_cached_yaml_data(colors_cache_key, colors)

            # Load mappings data
            mappings_cache_key = f"mappings:{current_theme}"
            mappings = _get_cached_yaml_data(mappings_cache_key)
            if not mappings:
                current_dir = Path(__file__).parent.parent.parent
                mappings_file = (
                    current_dir
                    / "src"
                    / "themeweaver"
                    / "themes"
                    / current_theme
                    / "mappings.yaml"
                )
                mappings = load_yaml_file(mappings_file)
                _set_cached_yaml_data(mappings_cache_key, mappings)

            # Only update if data has changed to avoid unnecessary work
            colors_changed = self._last_colors_data != colors
            mappings_changed = self._last_mappings_data != mappings

            if colors_changed:
                self._update_base_palettes(colors)
                self._last_colors_data = colors

            if colors_changed or mappings_changed:
                self._update_semantic_mappings(colors, mappings, current_variant)
                self._last_mappings_data = mappings

        except Exception as e:
            # Create or update error label
            if not hasattr(self, "_error_label"):
                self._error_label = QLabel()
                self._error_label.setStyleSheet("color: red; padding: 10px;")
                self.layout().addWidget(self._error_label)

            self._error_label.setText(f"Error loading colors: {e}")
            self._error_label.setVisible(True)

    def _update_base_palettes(self, colors):
        """Update base palettes tab with minimal widget recreation."""
        # Clear old widgets that are no longer needed
        new_palette_names = set(colors.keys())
        old_palette_names = set(self._base_palette_widgets.keys())

        # Remove widgets for palettes that no longer exist
        for palette_name in old_palette_names - new_palette_names:
            widget = self._base_palette_widgets.pop(palette_name)
            widget.setParent(None)
            widget.deleteLater()

        # Update or create widgets for each palette, ensuring correct order
        # First, remove all widgets from layout to reorder them
        widgets_to_reorder = []

        for palette_name, color_dict in colors.items():
            if not isinstance(color_dict, dict):
                continue

            if palette_name in self._base_palette_widgets:
                # Update existing widget
                widget = self._base_palette_widgets[palette_name]
                self._update_palette_widget(widget, palette_name, color_dict)
                # Remove from layout temporarily
                self.base_container_layout.removeWidget(widget)
                widgets_to_reorder.append(widget)
            else:
                # Create new widget
                palette_widget = self._create_palette_widget(palette_name, color_dict)
                self._base_palette_widgets[palette_name] = palette_widget
                widgets_to_reorder.append(palette_widget)

        # Add all widgets back in the correct order
        for widget in widgets_to_reorder:
            self.base_container_layout.addWidget(widget)

    def _update_semantic_mappings(self, colors, mappings, variant):
        """Update semantic mappings tab with minimal widget recreation."""
        # For now, clear and recreate semantic mappings as they're more complex
        # This could be further optimized in the future
        for widget in self._semantic_mapping_widgets.values():
            widget.setParent(None)
            widget.deleteLater()
        self._semantic_mapping_widgets.clear()

        # Recreate semantic mappings - use correct path
        semantic_mappings = mappings.get("semantic_mappings", {}) if mappings else {}

        if semantic_mappings and variant in semantic_mappings:
            mapping_widget = self._create_semantic_mapping_widget(
                colors, mappings, variant
            )
            self._semantic_mapping_widgets["main"] = mapping_widget
            self.semantic_container_layout.addWidget(mapping_widget)

    def _create_palette_widget(self, palette_name, color_dict):
        """Create widget for a color palette."""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(frame)

        # Palette title
        title_label = QLabel(palette_name.replace("_", " ").title())
        title_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title_label)

        # Color grid
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(1)
        grid_layout.setContentsMargins(2, 2, 2, 2)

        row, col = 0, 0
        max_cols = 8

        for color_name, color_value in color_dict.items():
            if isinstance(color_value, str) and color_value.startswith("#"):
                color_swatch = self._create_color_swatch(color_name, color_value)
                grid_layout.addWidget(color_swatch, row, col)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

        layout.addWidget(grid_widget)
        return frame

    def _update_palette_widget(self, widget, palette_name, color_dict):
        """Update existing palette widget with new data."""
        layout = widget.layout()

        # Update title
        title_label = layout.itemAt(0).widget()
        title_label.setText(palette_name.replace("_", " ").title())

        # Get grid widget
        grid_widget = layout.itemAt(1).widget()
        grid_layout = grid_widget.layout()

        # Clear existing color swatches
        while grid_layout.count():
            child = grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add new color swatches
        row, col = 0, 0
        max_cols = 8

        for color_name, color_value in color_dict.items():
            if isinstance(color_value, str) and color_value.startswith("#"):
                color_swatch = self._create_color_swatch(color_name, color_value)
                grid_layout.addWidget(color_swatch, row, col)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

    def _create_color_swatch(self, color_name, color_value):
        """Create a color swatch widget."""
        container = QWidget()
        container.setFixedSize(70, 75)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(1)

        # Color display
        color_widget = QWidget()
        color_widget.setFixedHeight(40)
        color_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {color_value};
                border: 1px solid #cccccc;
                border-radius: 2px;
            }}
        """)
        layout.addWidget(color_widget)

        # Color name
        name_label = QLabel(color_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet(
            "font-size: 7px; font-weight: bold; background-color: transparent;"
        )
        layout.addWidget(name_label)

        # Color value
        value_label = QLabel(color_value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("font-size: 7px; background-color: transparent;")
        layout.addWidget(value_label)

        container.setToolTip(f"{color_name}: {color_value}")
        return container

    def _create_semantic_mapping_widget(self, colors, mappings, variant):
        """Create widget for semantic mappings with proper implementation."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Header
        header_label = QLabel(f"Semantic Mappings ({variant.title()})")
        header_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(header_label)

        # Scroll area for mappings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout(container)

        semantic_mappings = mappings.get("semantic_mappings", {}).get(variant, {})
        if not semantic_mappings:
            error_label = QLabel(f"No semantic mappings found for variant '{variant}'")
            error_label.setStyleSheet("color: red; padding: 10px;")
            container_layout.addWidget(error_label)
        else:
            # Get color classes for resolution
            color_classes = mappings.get("color_classes", colors)

            # Categorize semantic mappings
            categories = {
                "Background": [
                    k for k in semantic_mappings.keys() if "BACKGROUND" in k
                ],
                "Text": [k for k in semantic_mappings.keys() if "TEXT" in k],
                "Accent": [k for k in semantic_mappings.keys() if "ACCENT" in k],
                "Success/Error/Warning": [
                    k
                    for k in semantic_mappings.keys()
                    if any(x in k for x in ["SUCCESS", "ERROR", "WARN"])
                ],
                "Icons": [k for k in semantic_mappings.keys() if "ICON" in k],
                "Groups": [k for k in semantic_mappings.keys() if "GROUP" in k],
                "Highlight": [k for k in semantic_mappings.keys() if "HIGHLIGHT" in k],
                "Occurrence": [
                    k for k in semantic_mappings.keys() if "OCCURRENCE" in k
                ],
                "Logos": [k for k in semantic_mappings.keys() if "LOGO" in k],
                "Other": [
                    k
                    for k in semantic_mappings.keys()
                    if not any(
                        x in k
                        for x in [
                            "BACKGROUND",
                            "TEXT",
                            "ACCENT",
                            "SUCCESS",
                            "ERROR",
                            "WARN",
                            "ICON",
                            "GROUP",
                            "HIGHLIGHT",
                            "OCCURRENCE",
                            "LOGO",
                        ]
                    )
                ],
            }

            for category_name, semantic_keys in categories.items():
                if not semantic_keys:
                    continue

                # Create category group
                group = QGroupBox(f"{category_name} Colors")
                group_layout = QVBoxLayout(group)

                # Create table for semantic mappings
                table = QTableWidget(len(semantic_keys), 4)
                table.setHorizontalHeaderLabels(
                    [
                        "Semantic Name",
                        "Semantic Reference",
                        "Palette Reference",
                        "Color",
                    ]
                )
                table.setAlternatingRowColors(True)
                table.setMinimumHeight(150)
                table.setMaximumHeight(400)

                for row, semantic_name in enumerate(semantic_keys):
                    color_ref = semantic_mappings[semantic_name]

                    # Set semantic name
                    name_item = QTableWidgetItem(semantic_name)
                    name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                    table.setItem(row, 0, name_item)

                    # Set semantic reference
                    ref_item = QTableWidgetItem(color_ref)
                    ref_item.setFlags(ref_item.flags() & ~Qt.ItemIsEditable)
                    table.setItem(row, 1, ref_item)

                    # Set palette reference
                    palette_ref = resolve_palette_reference(color_ref, color_classes)
                    palette_item = QTableWidgetItem(
                        palette_ref if palette_ref else color_ref
                    )
                    palette_item.setFlags(palette_item.flags() & ~Qt.ItemIsEditable)
                    table.setItem(row, 2, palette_item)

                    # Get actual color value
                    color_value = resolve_color_reference(
                        color_ref, colors, color_classes
                    )
                    if color_value:
                        # Create color swatch widget
                        color_widget = create_small_color_swatch(color_value)
                        table.setCellWidget(row, 3, color_widget)
                    else:
                        # If it's a numeric value (like opacity), show as text
                        table.setItem(row, 3, QTableWidgetItem(str(color_ref)))

                # Set column widths for better readability
                table.setColumnWidth(0, 200)  # Semantic Name column
                table.setColumnWidth(1, 150)  # Semantic Reference column
                table.setColumnWidth(2, 200)  # Palette Reference column
                table.setColumnWidth(3, 80)  # Color column

                # Set row height for all rows
                for row in range(table.rowCount()):
                    table.setRowHeight(row, 25)

                group_layout.addWidget(table)
                container_layout.addWidget(group)

        scroll_area.setWidget(container)
        layout.addWidget(scroll_area)

        return widget
