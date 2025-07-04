"""
UI tab creation methods for the ThemeWeaver preview application.
"""

from datetime import date

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
)
from PyQt5.QtCore import Qt


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
def fibonacci(n):
    '''Calculate fibonacci number using recursion.'''
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

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
