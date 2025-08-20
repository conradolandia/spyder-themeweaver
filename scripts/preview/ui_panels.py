"""
UI panel creation methods for the ThemeWeaver preview application.
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QRadioButton,
    QSlider,
    QProgressBar,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QGroupBox,
    QTabWidget,
    QScrollArea,
    QFrame,
    QDateEdit,
    QDateTimeEdit,
    QLCDNumber,
    QCommandLinkButton,
)
from PyQt5.QtCore import Qt, QSize, QDateTime


def create_left_panel(icons):
    """Create left panel with input controls.

    Args:
        icons: Dictionary of icons to use

    Returns:
        QScrollArea: Scroll area containing the left panel
    """
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setMinimumWidth(450)

    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Button Controls Group
    buttons_group = QGroupBox("Button Controls")
    buttons_layout = QVBoxLayout(buttons_group)

    buttons_layout.addWidget(QPushButton("Normal Button"))

    checked_btn = QPushButton("Checkable Button")
    checked_btn.setCheckable(True)
    checked_btn.setChecked(True)
    buttons_layout.addWidget(checked_btn)

    disabled_btn = QPushButton("Disabled Button")
    disabled_btn.setEnabled(False)
    buttons_layout.addWidget(disabled_btn)

    # Command link button
    command_btn = QCommandLinkButton(
        "Command Link", "This is a command link button with description"
    )
    buttons_layout.addWidget(command_btn)

    layout.addWidget(buttons_group)

    # Selection Controls Group
    selection_group = QGroupBox("Selection Controls")
    selection_layout = QVBoxLayout(selection_group)

    cb1 = QCheckBox("Checkbox 1 (unchecked)")
    selection_layout.addWidget(cb1)

    cb2 = QCheckBox("Checkbox 2 (checked)")
    cb2.setChecked(True)
    selection_layout.addWidget(cb2)

    cb3 = QCheckBox("Checkbox 3 (indeterminate)")
    cb3.setTristate(True)
    cb3.setCheckState(Qt.PartiallyChecked)
    selection_layout.addWidget(cb3)

    cb4 = QCheckBox("Disabled Checkbox")
    cb4.setEnabled(False)
    selection_layout.addWidget(cb4)

    selection_layout.addWidget(QFrame())  # Separator

    rb1 = QRadioButton("Radio 1")
    selection_layout.addWidget(rb1)

    rb2 = QRadioButton("Radio 2 (selected)")
    rb2.setChecked(True)
    selection_layout.addWidget(rb2)

    rb3 = QRadioButton("Radio 3")
    selection_layout.addWidget(rb3)

    rb4 = QRadioButton("Disabled Radio")
    rb4.setEnabled(False)
    selection_layout.addWidget(rb4)

    layout.addWidget(selection_group)

    # Sliders and Progress Group
    progress_group = QGroupBox("Progress & Sliders")
    progress_layout = QVBoxLayout(progress_group)

    progress_layout.addWidget(QLabel("Horizontal Slider:"))
    h_slider = QSlider(Qt.Horizontal)
    h_slider.setRange(0, 100)
    h_slider.setValue(60)
    progress_layout.addWidget(h_slider)

    # Vertical slider in horizontal layout
    v_layout = QHBoxLayout()
    v_layout.addWidget(QLabel("Vertical:"))
    v_slider = QSlider(Qt.Vertical)
    v_slider.setRange(0, 100)
    v_slider.setValue(40)
    v_slider.setMaximumHeight(80)
    v_layout.addWidget(v_slider)
    v_layout.addStretch()
    progress_layout.addLayout(v_layout)

    progress_layout.addWidget(QLabel("Progress Bar:"))
    progress1 = QProgressBar()
    progress1.setValue(75)
    progress_layout.addWidget(progress1)

    progress2 = QProgressBar()
    progress2.setValue(30)
    progress2.setEnabled(False)
    progress_layout.addWidget(progress2)

    layout.addWidget(progress_group)

    # Input Controls Group
    inputs_group = QGroupBox("Input Controls")
    inputs_layout = QVBoxLayout(inputs_group)

    inputs_layout.addWidget(QLabel("Text Input:"))
    line_edit = QLineEdit("Sample text input")
    line_edit.setPlaceholderText("Enter text here...")
    inputs_layout.addWidget(line_edit)

    inputs_layout.addWidget(QLabel("Number Input:"))
    spin_box = QSpinBox()
    spin_box.setRange(0, 1000)
    spin_box.setValue(42)
    inputs_layout.addWidget(spin_box)

    inputs_layout.addWidget(QLabel("Decimal Input:"))
    double_spin = QDoubleSpinBox()
    double_spin.setRange(0.0, 100.0)
    double_spin.setValue(3.14159)
    double_spin.setDecimals(5)
    inputs_layout.addWidget(double_spin)

    inputs_layout.addWidget(QLabel("Dropdown:"))
    combo = QComboBox()
    combo.setIconSize(QSize(16, 16))
    combo.addItem(icons["check"], "Option 1")
    combo.addItem(icons["check"], "Option 2")
    combo.addItem(icons["check"], "Option 3")
    combo.addItem("Disabled Option")
    combo.setItemData(3, False, Qt.UserRole - 1)  # Disable last item
    inputs_layout.addWidget(combo)

    # Editable combo box
    inputs_layout.addWidget(QLabel("Editable Dropdown:"))
    editable_combo = QComboBox()
    editable_combo.setEditable(True)
    editable_combo.addItems(["Edit me", "Or select", "From list"])
    inputs_layout.addWidget(editable_combo)

    layout.addWidget(inputs_group)

    # Date/Time Controls Group
    datetime_group = QGroupBox("Date & Time Controls")
    datetime_layout = QVBoxLayout(datetime_group)

    datetime_layout.addWidget(QLabel("Date:"))
    date_edit = QDateEdit()
    date_edit.setDate(QDateTime.currentDateTime().date())
    date_edit.setCalendarPopup(True)
    datetime_layout.addWidget(date_edit)

    datetime_layout.addWidget(QLabel("Date & Time:"))
    datetime_edit = QDateTimeEdit()
    datetime_edit.setDateTime(QDateTime.currentDateTime())
    datetime_edit.setCalendarPopup(True)
    datetime_layout.addWidget(datetime_edit)

    layout.addWidget(datetime_group)

    layout.addStretch()
    scroll_area.setWidget(widget)
    return scroll_area


def create_right_panel(tab_functions):
    """Create right panel with content displays.

    Args:
        tab_functions: Dictionary of tab creation functions

    Returns:
        tuple: (QTabWidget, dict) - Tab widget and references to specific tabs
    """
    # Create tab widget with tabs in different positions
    tab_widget = QTabWidget()
    tab_widget.setTabPosition(QTabWidget.North)

    # Color Palette Tab - use optimized version
    if "colors" in tab_functions:
        from .color_tab import ColorTab
        colors_tab = ColorTab()
    else:
        colors_tab = QWidget()  # Fallback
    tab_widget.addTab(colors_tab, "Color Palette")

    # Data Views Tab
    views_tab = tab_functions["views"]()
    tab_widget.addTab(views_tab, "Data Views")

    # Return tab widget and references to specific tabs
    tab_references = {
        "colors_tab": colors_tab,
        "views_tab": views_tab,
    }

    return tab_widget, tab_references
