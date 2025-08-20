#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Preview Application for ThemeWeaver

Qt application to preview and test generated themes,
showcasing all the UI elements styled in the QSS files.
"""

import sys

from PyQt5.QtWidgets import QApplication

from .main_window import ThemePreviewWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("ThemeWeaver Preview")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Spyder Team")

    # Create and show the main window
    window = ThemePreviewWindow()
    window.show()

    # Start the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
