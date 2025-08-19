"""
Main window class for the ThemeWeaver preview application.
"""

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QSplitter,
    QApplication,
)
from PyQt5.QtCore import Qt, QSize, QSettings, QByteArray
from PyQt5.QtGui import QCloseEvent

from . import ui_components, ui_panels
from . import theme_loader
from . import ui_tabs


class ThemePreviewWindow(QMainWindow):
    """Main window for theme preview application."""

    def __init__(self):
        super().__init__()
        self._current_theme = None
        self._current_variant = None

        # Initialize settings for window geometry persistence
        self.settings = QSettings("ThemeWeaver", "ThemePreview")

        self.init_ui()
        self.setup_theme_selector()
        self.restore_geometry()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("ThemeWeaver - Theme Preview")
        # Don't set geometry here - it will be restored from settings

        # Create icons for UI elements
        self.icons = self.create_theme_icons()

        # Create menu bar first
        ui_components.create_menu_bar(self, self.style())

        # Create central widget with main splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Theme selector at top
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))

        self.theme_combo = QComboBox()
        self.theme_combo.setIconSize(QSize(16, 16))
        self.theme_combo.currentTextChanged.connect(self.load_theme)
        theme_layout.addWidget(self.theme_combo)

        self.variant_combo = QComboBox()
        self.variant_combo.setIconSize(QSize(16, 16))
        self.variant_combo.addItem(self.icons["variant_dark"], "dark")
        self.variant_combo.addItem(self.icons["variant_light"], "light")
        self.variant_combo.currentTextChanged.connect(self.load_theme)
        theme_layout.addWidget(QLabel("Variant:"))
        theme_layout.addWidget(self.variant_combo)

        # Reset button
        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_theme)
        theme_layout.addWidget(reset_btn)

        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        # Create main content area
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)

        # Create tab functions dictionary
        tab_functions = {
            "views": ui_tabs.create_views_tab,
            # "calendar": ui_tabs.create_calendar_tab,
            # "splitter": ui_tabs.create_splitter_tab,
            "colors": ui_tabs.create_color_palette_tab,
        }

        # Left panel - Controls and inputs
        left_panel = ui_panels.create_left_panel(self.icons)
        main_splitter.addWidget(left_panel)

        # Right panel - Content and displays
        right_panel, self.tab_references = ui_panels.create_right_panel(tab_functions)
        main_splitter.addWidget(right_panel)

        # Set splitter proportions
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)

        # Create status bar
        self.status_bar = ui_components.create_status_bar(self)

    def setup_theme_selector(self):
        """Setup the theme selector with available themes."""
        # Get available themes
        themes = theme_loader.get_available_themes()
        # themes = ["solarized", "dracula"]  # Hardcode for testing

        # Add themes with icons
        for theme in themes:
            self.theme_combo.addItem(self.icons["theme"], theme)

        if themes:
            self.statusBar().showMessage(
                f"Found {len(themes)} theme(s) - Select a theme to preview"
            )
            # Load the first theme automatically
            self.load_theme()
        else:
            self.statusBar().showMessage("No themes found in build directory")

    def load_theme(self):
        """Load the selected theme variant."""
        theme_name = self.theme_combo.currentText()
        variant = self.variant_combo.currentText()

        if not theme_name or not variant:
            return

        # Set current theme and variant
        self._current_theme = theme_name
        self._current_variant = variant

        # Create a wrapper function for status bar updates
        def status_callback(message):
            self.statusBar().showMessage(message)

        success, stylesheet = theme_loader.load_theme(
            theme_name, variant, status_callback
        )

        if success and stylesheet:
            # Apply to the application using QTimer to avoid blocking the UI
            from PyQt5.QtCore import QTimer

            def apply_stylesheet():
                QApplication.instance().setStyleSheet(stylesheet)
                self.statusBar().showMessage(f"Applied theme: {theme_name} ({variant})")

                # Update color palette tab if it exists
                if (
                    hasattr(self, "tab_references")
                    and "colors_tab" in self.tab_references
                ):
                    colors_tab = self.tab_references["colors_tab"]
                    if hasattr(colors_tab, "update_colors"):
                        # Update the colors tab with current theme and variant
                        colors_tab._current_theme = theme_name
                        colors_tab._current_variant = variant
                        colors_tab.update_colors()

            # Apply stylesheet in the next event loop iteration to avoid blocking
            QTimer.singleShot(0, apply_stylesheet)
        else:
            self.statusBar().showMessage(
                f"Failed to load theme: {theme_name} ({variant})"
            )

    def reset_theme(self):
        """Reset to default theme."""
        QApplication.instance().setStyleSheet("")
        self.statusBar().showMessage("Reset to default theme")

    def create_theme_icons(self):
        """Create icons for theme elements using system standard icons."""
        icons = {}

        # Create theme-related icons using system standard icons
        icons["check"] = self.style().standardIcon(self.style().SP_DialogApplyButton)
        icons["theme"] = self.style().standardIcon(self.style().SP_DesktopIcon)
        icons["variant_dark"] = self.style().standardIcon(self.style().SP_MediaPlay)
        icons["variant_light"] = self.style().standardIcon(self.style().SP_MediaStop)

        return icons

    def closeEvent(self, event: QCloseEvent):
        """Override close event to save window geometry before closing."""
        self.save_geometry()
        super().closeEvent(event)

    def save_geometry(self):
        """Save window geometry to settings."""
        geometry = self.saveGeometry()
        self.settings.setValue("geometry", geometry)
        self.settings.sync()

    def restore_geometry(self):
        """Restore window geometry from settings."""
        geometry = self.settings.value("geometry")
        if geometry:
            # Try to restore the saved geometry
            if self.restoreGeometry(QByteArray(geometry)):
                return

        # Fallback to default geometry if restoration fails
        self.setGeometry(50, 50, 1400, 900)
