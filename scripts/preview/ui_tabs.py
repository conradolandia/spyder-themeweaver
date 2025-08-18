"""
UI tab creation methods for the ThemeWeaver preview application.
"""

from datetime import date
import yaml
from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QPlainTextEdit,
    QListWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QSplitter,
    QToolBox,
    QCalendarWidget,
    QCheckBox,
    QScrollArea,
    QFrame,
    QGridLayout,
    QComboBox,
    QTabWidget,
    QGroupBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QPixmap


def create_text_tab():
    """Create text editor tab."""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Text editors
    splitter = QSplitter(Qt.Vertical)

    # Plain text edit
    layout.addWidget(QLabel("QTextEdit with sample code:"))
    text_edit = QTextEdit()
    text_edit.setPlainText("""# Sample Python Code with Syntax


# Test the function
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")

# Dictionary and list examples
data = {
    'name': 'ThemeWeaver',
    'version': '1.0.0',
    'features': ['themes', 'preview', 'export']
}

# Boolean and None values
is_active = True
result = None

# Multi-line string
description = '''
This is a multi-line string
that demonstrates text highlighting
in the theme preview application.
'''

print(f"Project: {data['name']} v{data['version']}")
""")
    splitter.addWidget(text_edit)

    # Plain text edit
    layout.addWidget(QLabel("QPlainTextEdit:"))
    plain_edit = QPlainTextEdit()
    plain_edit.setPlainText("""Plain text editor example.
This widget shows how plain text
is rendered with the current theme.

It supports:
- Multiple lines
- Simple text formatting
- Basic text operations

No syntax highlighting here,
just plain text rendering.""")
    splitter.addWidget(plain_edit)

    layout.addWidget(splitter)
    return widget


def create_views_tab():
    """Create data views tab with lists, trees, and tables."""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Horizontal splitter for views
    splitter = QSplitter(Qt.Horizontal)

    # Left side - List and Tree
    left_widget = QWidget()
    left_layout = QVBoxLayout(left_widget)

    # List widget
    left_layout.addWidget(QLabel("QListWidget:"))
    list_widget = QListWidget()
    list_widget.addItems(
        [
            "List item 1",
            "List item 2 (selected)",
            "List item 3",
            "List item 4",
            "List item 5",
            "Disabled item",
            "Last item",
        ]
    )
    list_widget.setCurrentRow(1)
    list_widget.item(5).setFlags(list_widget.item(5).flags() & ~Qt.ItemIsEnabled)
    left_layout.addWidget(list_widget)

    # Tree widget with comprehensive structure
    left_layout.addWidget(QLabel("QTreeWidget with branches:"))
    tree_widget = QTreeWidget()
    tree_widget.setHeaderLabels(["Name", "Type", "Size", "Modified"])

    # Create comprehensive tree structure
    project_root = QTreeWidgetItem(
        tree_widget, ["ThemeWeaver Project", "Folder", "", "Today"]
    )

    src_folder = QTreeWidgetItem(project_root, ["src/", "Folder", "", "Today"])
    QTreeWidgetItem(src_folder, ["main.py", "Python", "2.5 KB", "2 hours ago"])
    QTreeWidgetItem(src_folder, ["theme.py", "Python", "4.1 KB", "1 hour ago"])
    QTreeWidgetItem(src_folder, ["utils.py", "Python", "1.8 KB", "Yesterday"])

    core_folder = QTreeWidgetItem(src_folder, ["core/", "Folder", "", "Today"])
    QTreeWidgetItem(core_folder, ["palette.py", "Python", "3.2 KB", "3 hours ago"])
    QTreeWidgetItem(core_folder, ["exporter.py", "Python", "5.7 KB", "Today"])

    docs_folder = QTreeWidgetItem(project_root, ["docs/", "Folder", "", "Yesterday"])
    QTreeWidgetItem(docs_folder, ["README.md", "Markdown", "4.3 KB", "Yesterday"])
    QTreeWidgetItem(docs_folder, ["guide.txt", "Text", "8.7 KB", "2 days ago"])

    tests_folder = QTreeWidgetItem(project_root, ["tests/", "Folder", "", "Today"])
    QTreeWidgetItem(tests_folder, ["test_theme.py", "Python", "2.1 KB", "Today"])
    QTreeWidgetItem(tests_folder, ["test_export.py", "Python", "1.9 KB", "Today"])

    tree_widget.expandAll()
    tree_widget.resizeColumnToContents(0)
    left_layout.addWidget(tree_widget)

    splitter.addWidget(left_widget)

    # Right side - Table
    right_widget = QWidget()
    right_layout = QVBoxLayout(right_widget)

    right_layout.addWidget(QLabel("QTableWidget with sorting:"))
    table_widget = QTableWidget(8, 5)
    table_widget.setHorizontalHeaderLabels(
        ["Name", "Status", "Priority", "Progress", "Due Date"]
    )

    # Populate table with sample data
    table_data = [
        ["Design System", "In Progress", "High", "75%", "2024-02-15"],
        ["Theme Export", "Completed", "High", "100%", "2024-02-10"],
        ["Color Palette", "In Progress", "Medium", "60%", "2024-02-20"],
        ["Documentation", "Pending", "Low", "25%", "2024-02-25"],
        ["Testing", "In Progress", "High", "80%", "2024-02-18"],
        ["Bug Fixes", "Completed", "Medium", "100%", "2024-02-12"],
        ["Performance", "Pending", "Medium", "10%", "2024-03-01"],
        ["Deployment", "Pending", "Low", "0%", "2024-03-05"],
    ]

    for row, row_data in enumerate(table_data):
        for col, value in enumerate(row_data):
            item = QTableWidgetItem(value)
            if col == 1:  # Status column
                if value == "Completed":
                    item.setBackground(Qt.green)
                elif value == "In Progress":
                    item.setBackground(Qt.yellow)
            table_widget.setItem(row, col, item)

    # Enable sorting
    table_widget.setSortingEnabled(True)
    table_widget.resizeColumnsToContents()

    # Select a row
    table_widget.selectRow(1)

    right_layout.addWidget(table_widget)

    splitter.addWidget(right_widget)
    layout.addWidget(splitter)
    return widget


def create_toolbox_tab():
    """Create tool box tab."""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    layout.addWidget(QLabel("QToolBox with different tools:"))

    toolbox = QToolBox()

    # Page 1 - Drawing Tools
    drawing_page = QWidget()
    drawing_layout = QVBoxLayout(drawing_page)
    drawing_layout.addWidget(QPushButton("Pen Tool"))
    drawing_layout.addWidget(QPushButton("Brush Tool"))
    drawing_layout.addWidget(QPushButton("Eraser Tool"))
    drawing_layout.addWidget(QPushButton("Fill Tool"))
    drawing_layout.addStretch()
    toolbox.addItem(drawing_page, "Drawing Tools")

    # Page 2 - Selection Tools
    select_page = QWidget()
    select_layout = QVBoxLayout(select_page)
    select_layout.addWidget(QPushButton("Rectangle Select"))
    select_layout.addWidget(QPushButton("Ellipse Select"))
    select_layout.addWidget(QPushButton("Lasso Select"))
    select_layout.addWidget(QPushButton("Magic Wand"))
    select_layout.addStretch()
    toolbox.addItem(select_page, "Selection Tools")

    # Page 3 - Transform Tools
    transform_page = QWidget()
    transform_layout = QVBoxLayout(transform_page)
    transform_layout.addWidget(QPushButton("Move"))
    transform_layout.addWidget(QPushButton("Rotate"))
    transform_layout.addWidget(QPushButton("Scale"))
    transform_layout.addWidget(QPushButton("Skew"))
    transform_layout.addStretch()
    toolbox.addItem(transform_page, "Transform Tools")

    # Page 4 - Text Tools
    text_page = QWidget()
    text_layout = QVBoxLayout(text_page)
    text_layout.addWidget(QPushButton("Text Tool"))
    text_layout.addWidget(QPushButton("Font Selector"))
    text_layout.addWidget(QCheckBox("Bold"))
    text_layout.addWidget(QCheckBox("Italic"))
    text_layout.addWidget(QCheckBox("Underline"))
    text_layout.addStretch()
    toolbox.addItem(text_page, "Text Tools")

    layout.addWidget(toolbox)
    return widget


def create_calendar_tab():
    """Create calendar tab."""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    layout.addWidget(QLabel("QCalendarWidget:"))

    calendar = QCalendarWidget()
    calendar.setGridVisible(True)
    calendar.setVerticalHeaderFormat(QCalendarWidget.ISOWeekNumbers)

    # Highlight today
    calendar.setSelectedDate(date.today())

    layout.addWidget(calendar)

    # Add some controls below calendar
    controls_layout = QHBoxLayout()
    controls_layout.addWidget(QLabel("Navigate:"))

    prev_btn = QPushButton("Previous Month")
    next_btn = QPushButton("Next Month")
    today_btn = QPushButton("Today")

    controls_layout.addWidget(prev_btn)
    controls_layout.addWidget(next_btn)
    controls_layout.addWidget(today_btn)
    controls_layout.addStretch()

    layout.addLayout(controls_layout)

    return widget


def create_splitter_tab():
    """Create splitter demonstration tab."""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    layout.addWidget(QLabel("QSplitter demonstrations:"))

    # Main vertical splitter
    main_splitter = QSplitter(Qt.Vertical)

    # Top horizontal splitter
    top_splitter = QSplitter(Qt.Horizontal)

    # Left panel
    left_panel = QTextEdit()
    left_panel.setPlainText(
        "Left panel\nResize by dragging the splitter handle.\n\nThis demonstrates horizontal splitter styling."
    )
    top_splitter.addWidget(left_panel)

    # Middle panel
    middle_panel = QListWidget()
    middle_panel.addItems(["Item 1", "Item 2", "Item 3", "Middle panel", "More items"])
    top_splitter.addWidget(middle_panel)

    # Right panel
    right_panel = QTreeWidget()
    right_panel.setHeaderLabels(["Name", "Value"])
    root = QTreeWidgetItem(right_panel, ["Root", ""])
    QTreeWidgetItem(root, ["Child 1", "Value 1"])
    QTreeWidgetItem(root, ["Child 2", "Value 2"])
    right_panel.expandAll()
    top_splitter.addWidget(right_panel)

    main_splitter.addWidget(top_splitter)

    # Bottom panel
    bottom_panel = QTextEdit()
    bottom_panel.setPlainText(
        "Bottom panel\n\nThis shows vertical splitter styling.\nYou can resize this by dragging the horizontal splitter handle above."
    )
    main_splitter.addWidget(bottom_panel)

    # Set initial sizes
    main_splitter.setSizes([300, 150])
    top_splitter.setSizes([200, 150, 200])

    layout.addWidget(main_splitter)
    return widget


def create_color_palette_tab():
    """Create comprehensive color palette preview tab."""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Header
    header_label = QLabel("Color Palette Preview")
    header_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
    layout.addWidget(header_label)

    # Theme and variant selector
    selector_layout = QHBoxLayout()
    selector_layout.addWidget(QLabel("Theme:"))
    theme_combo = QComboBox()

    # Get available themes from src/themeweaver/themes
    themes_dir = Path(__file__).parent.parent.parent / "src" / "themeweaver" / "themes"
    if themes_dir.exists() and themes_dir.is_dir():
        available_themes = [
            d.name for d in themes_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]
    else:
        available_themes = []

    theme_combo.addItems(available_themes)
    selector_layout.addWidget(theme_combo)
    
    selector_layout.addWidget(QLabel("Variant:"))
    variant_combo = QComboBox()
    variant_combo.addItems(["dark", "light"])
    selector_layout.addWidget(variant_combo)
    
    selector_layout.addStretch()
    layout.addLayout(selector_layout)

    # Create tab widget for different views
    tab_widget = QTabWidget()
    
    # Load and display colors
    def load_and_display_colors():
        theme_name = theme_combo.currentText()
        variant = variant_combo.currentText()
        
        try:
            # Load color data
            colors = load_colors_from_yaml(theme_name)
            mappings = load_mappings_from_yaml(theme_name)
            
            # Clear existing tabs
            tab_widget.clear()
            
            # Add base palettes tab
            base_palettes_tab = create_base_palettes_tab(colors)
            tab_widget.addTab(base_palettes_tab, "Base Palettes")
            
            # Add semantic mappings tab
            semantic_tab = create_semantic_mappings_tab(colors, mappings, variant)
            tab_widget.addTab(semantic_tab, "Semantic Mappings")
            
        except Exception as e:
            error_label = QLabel(f"Error loading colors: {e}")
            error_label.setStyleSheet("color: red; padding: 10px;")
            layout.addWidget(error_label)
    
    # Connect selectors to color loading
    theme_combo.currentTextChanged.connect(load_and_display_colors)
    variant_combo.currentTextChanged.connect(load_and_display_colors)
    
    layout.addWidget(tab_widget)
    
    # Initial load
    load_and_display_colors()
    
    return widget


def create_base_palettes_tab(colors):
    """Create tab showing base color palettes."""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    
    container = QWidget()
    container_layout = QVBoxLayout(container)
    
    for palette_name, color_dict in colors.items():
        if not isinstance(color_dict, dict):
            continue
            
        # Create palette group
        group = QGroupBox(palette_name)
        group_layout = QVBoxLayout(group)
        
        # Create color grid
        color_grid = QGridLayout()
        color_grid.setSpacing(5)
        
        row = 0
        col = 0
        max_cols = 8
        
        for color_name, color_value in color_dict.items():
            if not isinstance(color_value, str) or not color_value.startswith("#"):
                continue
                
            # Create color swatch
            color_widget = create_color_swatch(color_name, color_value)
            color_grid.addWidget(color_widget, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        group_layout.addLayout(color_grid)
        container_layout.addWidget(group)
    
    scroll_area.setWidget(container)
    layout.addWidget(scroll_area)
    
    return widget


def create_semantic_mappings_tab(colors, mappings, variant):
    """Create tab showing semantic color mappings."""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    
    container = QWidget()
    container_layout = QVBoxLayout(container)
    
    # Get semantic mappings for the selected variant
    semantic_mappings = mappings.get("semantic_mappings", {}).get(variant, {})
    color_classes = mappings.get("color_classes", {})
    
    # Group semantic mappings by category
    categories = {
        "Background": [k for k in semantic_mappings.keys() if "BACKGROUND" in k],
        "Text": [k for k in semantic_mappings.keys() if "TEXT" in k],
        "Accent": [k for k in semantic_mappings.keys() if "ACCENT" in k],
        "Success/Error/Warning": [k for k in semantic_mappings.keys() if any(x in k for x in ["SUCCESS", "ERROR", "WARN"])],
        "Icons": [k for k in semantic_mappings.keys() if "ICON" in k],
        "Groups": [k for k in semantic_mappings.keys() if "GROUP" in k],
        "Highlight": [k for k in semantic_mappings.keys() if "HIGHLIGHT" in k],
        "Occurrence": [k for k in semantic_mappings.keys() if "OCCURRENCE" in k],
        "Logos": [k for k in semantic_mappings.keys() if "LOGO" in k],
        "Other": [k for k in semantic_mappings.keys() if not any(x in k for x in ["BACKGROUND", "TEXT", "ACCENT", "SUCCESS", "ERROR", "WARN", "ICON", "GROUP", "HIGHLIGHT", "OCCURRENCE", "LOGO"])],
    }
    
    for category_name, semantic_keys in categories.items():
        if not semantic_keys:
            continue
            
        # Create category group
        group = QGroupBox(f"{category_name} Colors")
        group_layout = QVBoxLayout(group)
        
        # Create table for semantic mappings
        table = QTableWidget(len(semantic_keys), 4)
        table.setHorizontalHeaderLabels(["Semantic Name", "Semantic Reference", "Palette Reference", "Color"])
        table.setAlternatingRowColors(True)
        table.setMinimumHeight(200)  # Set minimum height for better navigation
        table.setMaximumHeight(600)  # Set maximum height to prevent excessive scrolling
        
        for row, semantic_name in enumerate(semantic_keys):
            color_ref = semantic_mappings[semantic_name]
            
            # Set semantic name
            name_item = QTableWidgetItem(semantic_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 0, name_item)
            
            # Set semantic reference (e.g., "Primary.B40")
            ref_item = QTableWidgetItem(color_ref)
            ref_item.setFlags(ref_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 1, ref_item)
            
            # Set palette reference (e.g., "HastyBlackPanther.B40")
            palette_ref = resolve_palette_reference(color_ref, color_classes)
            palette_item = QTableWidgetItem(palette_ref if palette_ref else color_ref)
            palette_item.setFlags(palette_item.flags() & ~Qt.ItemIsEditable)
            table.setItem(row, 2, palette_item)
            
            # Get actual color value
            color_value = resolve_color_reference(color_ref, colors, color_classes)
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
        table.setColumnWidth(3, 80)   # Color column
        
        # Set row height for all rows
        for row in range(table.rowCount()):
            table.setRowHeight(row, 25)
        group_layout.addWidget(table)
        container_layout.addWidget(group)
    
    scroll_area.setWidget(container)
    layout.addWidget(scroll_area)
    
    return widget


def resolve_color_reference(color_ref, colors, color_classes):
    """Resolve a color reference like 'Primary.B10' to actual hex color."""
    if not isinstance(color_ref, str) or "." not in color_ref:
        return None
        
    class_name, color_name = color_ref.split(".", 1)
    
    # Get the palette name from color_classes
    palette_name = color_classes.get(class_name)
    if not palette_name:
        return None
        
    # Get the color from the palette
    palette = colors.get(palette_name, {})
    return palette.get(color_name)


def resolve_palette_reference(color_ref, color_classes):
    """Resolve a color reference like 'Primary.B10' to palette reference like 'HastyBlackPanther.B10'."""
    if not isinstance(color_ref, str) or "." not in color_ref:
        return None
        
    class_name, color_name = color_ref.split(".", 1)
    
    # Get the palette name from color_classes
    palette_name = color_classes.get(class_name)
    if not palette_name:
        return None
        
    # Return the full palette reference
    return f"{palette_name}.{color_name}"


from themeweaver.core.yaml_loader import load_colors_from_yaml, load_color_mappings_from_yaml


def load_mappings_from_yaml(theme_name):
    """Load mappings from theme's mappings.yaml file."""
    # Use the centralized function but return the full mappings data
    from themeweaver.core.yaml_loader import load_yaml_file
    from pathlib import Path
    
    current_dir = Path(__file__).parent.parent.parent
    yaml_file = current_dir / "src" / "themeweaver" / "themes" / theme_name / "mappings.yaml"
    
    return load_yaml_file(yaml_file)


def create_color_swatch(color_name, color_value):
    """Create a color swatch widget."""
    container = QWidget()
    container.setFixedSize(80, 60)
    container.setStyleSheet(f"""
        QWidget {{
            background-color: {color_value};
        }}
    """)
    
    layout = QVBoxLayout(container)
    layout.setContentsMargins(2, 2, 2, 2)
    layout.setSpacing(2)
    
    # Color name label
    name_label = QLabel(color_name)
    name_label.setAlignment(Qt.AlignCenter)
    name_label.setStyleSheet("""
        QLabel {
            padding: 1px;
            font-size: 8px;
            font-weight: bold;
        }
    """)
    layout.addWidget(name_label)
    
    # Color value label
    value_label = QLabel(color_value)
    value_label.setAlignment(Qt.AlignCenter)
    value_label.setStyleSheet("""
        QLabel {
            padding: 1px;
            font-size: 8px;
        }
    """)
    layout.addWidget(value_label)
    
    return container


def create_small_color_swatch(color_value):
    """Create a small color swatch for table cells."""
    container = QWidget()
    container.setFixedSize(60, 20)  # Increased width for better visibility
    container.setStyleSheet(f"""
        QWidget {{
            background-color: {color_value};
            border: 1px solid #cccccc;
        }}
    """)
    
    # Add color value as tooltip
    container.setToolTip(color_value)
    
    return container
