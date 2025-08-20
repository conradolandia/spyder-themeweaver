"""
Main window class for the ThemeWeaver preview application.
"""

from PyQt5.QtCore import QByteArray, QSettings, QSize, Qt, QTimer
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from . import theme_loader, ui_components, ui_panels, ui_tabs
from .async_theme_loader import ThemeLoaderThread, ThemePreloader


class ThemePreviewWindow(QMainWindow):
    """Main window for theme preview application."""

    def __init__(self):
        super().__init__()
        self._current_theme = None
        self._current_variant = None

        # Initialize settings for window geometry persistence
        self.settings = QSettings("ThemeWeaver", "ThemePreview")

        # Initialize async theme loader
        self._theme_loader_thread = ThemeLoaderThread()
        self._theme_loader_thread.theme_loaded.connect(self._on_theme_loaded)
        self._theme_loader_thread.loading_failed.connect(self._on_theme_loading_failed)
        self._theme_loader_thread.status_update.connect(self._on_status_update)

        # Initialize preloader (will be started after UI setup)
        self._preloader = None
        self._is_loading = False

        self.init_ui()
        self.setup_theme_selector()
        self.restore_geometry()

        # Start background preloading
        self._start_background_preloading()

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
        """Load the selected theme variant asynchronously."""
        theme_name = self.theme_combo.currentText()
        variant = self.variant_combo.currentText()

        if not theme_name or not variant:
            return

        # Skip if already loading the same theme
        if (
            self._is_loading
            and self._current_theme == theme_name
            and self._current_variant == variant
        ):
            return

        # Set current theme and variant
        self._current_theme = theme_name
        self._current_variant = variant

        # Show loading state
        self._show_loading_state(True)

        # Stop any ongoing loading
        self._theme_loader_thread.stop_loading()

        # Start async loading
        self._theme_loader_thread.load_theme_async(theme_name, variant)

    def reset_theme(self):
        """Reset to default theme."""
        QApplication.instance().setStyleSheet("")
        self.statusBar().showMessage("Reset to default theme")

    def _show_loading_state(self, loading):
        """Show or hide loading state indicators."""
        self._is_loading = loading

        # Disable controls during loading to prevent user interaction
        self.theme_combo.setEnabled(not loading)
        self.variant_combo.setEnabled(not loading)

    def _on_theme_loaded(self, theme_name, variant, stylesheet):
        """Handle successful theme loading."""
        self._show_loading_state(False)

        # Apply stylesheet in next event loop to avoid blocking
        QTimer.singleShot(0, lambda: self._apply_theme(theme_name, variant, stylesheet))

    def _on_theme_loading_failed(self, theme_name, variant, error):
        """Handle theme loading failure."""
        self._show_loading_state(False)
        self.statusBar().showMessage(
            f"Failed to load theme {theme_name} ({variant}): {error}"
        )

    def _on_status_update(self, message):
        """Handle status updates from theme loader."""
        self.statusBar().showMessage(message)

    def _apply_theme(self, theme_name, variant, stylesheet):
        """Apply the loaded theme to the application."""
        try:
            QApplication.instance().setStyleSheet(stylesheet)
            self.statusBar().showMessage(f"Applied theme: {theme_name} ({variant})")

            # Update color palette tab if it exists
            if hasattr(self, "tab_references") and "colors_tab" in self.tab_references:
                colors_tab = self.tab_references["colors_tab"]
                if hasattr(colors_tab, "update_colors"):
                    # Update the colors tab with current theme and variant
                    colors_tab._current_theme = theme_name
                    colors_tab._current_variant = variant
                    # Use timer to avoid blocking UI during color updates
                    QTimer.singleShot(100, colors_tab.update_colors)

        except Exception as e:
            self.statusBar().showMessage(f"Error applying theme: {e}")

    def _start_background_preloading(self):
        """Start background preloading of all themes."""
        # Get available themes
        themes = theme_loader.get_available_themes()
        if not themes:
            return

        # Start preloader
        self._preloader = ThemePreloader(themes)
        self._preloader.preload_progress.connect(self._on_preload_progress)
        self._preloader.preload_complete.connect(self._on_preload_complete)

        # Start preloading after a short delay to let UI initialize
        QTimer.singleShot(2000, self._preloader.start)

    def _on_preload_progress(self, status, current, total):
        """Handle preload progress updates."""
        # Only show preload status if not actively loading a theme
        if not self._is_loading:
            self.statusBar().showMessage(f"Background: {status} ({current}/{total})")

    def _on_preload_complete(self, loaded_count):
        """Handle preload completion."""
        if not self._is_loading:
            self.statusBar().showMessage(
                f"Background preloading complete: {loaded_count} themes cached"
            )

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
        # Stop background threads
        if self._theme_loader_thread.isRunning():
            self._theme_loader_thread.stop_loading()
            self._theme_loader_thread.wait(3000)  # Wait up to 3 seconds

        if self._preloader and self._preloader.isRunning():
            self._preloader.stop_preloading()
            self._preloader.wait(3000)  # Wait up to 3 seconds

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
