"""
UI components for the ThemeWeaver preview application.

This module contains UI components like menu bar, toolbar, and dock widgets.
"""

from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QLabel,
    QProgressBar,
)


def create_menu_bar(window, style):
    """Create menu bar to test menu styling.

    Args:
        window: Parent window
        style: Window style for icons

    Returns:
        QMenuBar: The created menu bar
    """
    menubar = window.menuBar()

    # File menu with icons and separators
    file_menu = menubar.addMenu("&File")

    new_action = QAction("&New", window)
    new_action.setShortcut("Ctrl+N")
    new_action.setIcon(style.standardIcon(style.SP_FileDialogNewFolder))
    file_menu.addAction(new_action)

    open_action = QAction("&Open", window)
    open_action.setShortcut("Ctrl+O")
    open_action.setIcon(style.standardIcon(style.SP_DialogOpenButton))
    file_menu.addAction(open_action)

    file_menu.addSeparator()

    save_action = QAction("&Save", window)
    save_action.setShortcut("Ctrl+S")
    save_action.setIcon(style.standardIcon(style.SP_DialogSaveButton))
    file_menu.addAction(save_action)

    file_menu.addSeparator()

    # Submenu
    recent_menu = file_menu.addMenu("Recent Files")
    recent_menu.addAction("document1.txt")
    recent_menu.addAction("project.py")
    recent_menu.addAction("data.csv")

    file_menu.addSeparator()
    exit_action = QAction("E&xit", window)
    exit_action.setShortcut("Ctrl+Q")
    file_menu.addAction(exit_action)

    # Edit menu with checkable actions
    edit_menu = menubar.addMenu("&Edit")

    undo_action = QAction("&Undo", window)
    undo_action.setShortcut("Ctrl+Z")
    edit_menu.addAction(undo_action)

    redo_action = QAction("&Redo", window)
    redo_action.setShortcut("Ctrl+Y")
    edit_menu.addAction(redo_action)

    edit_menu.addSeparator()

    # Action group for exclusive selection
    view_group = QActionGroup(window)

    normal_view = QAction("Normal View", window)
    normal_view.setCheckable(True)
    normal_view.setChecked(True)
    view_group.addAction(normal_view)
    edit_menu.addAction(normal_view)

    compact_view = QAction("Compact View", window)
    compact_view.setCheckable(True)
    view_group.addAction(compact_view)
    edit_menu.addAction(compact_view)

    edit_menu.addSeparator()

    # Non-exclusive checkable actions
    show_toolbar = QAction("Show Toolbar", window)
    show_toolbar.setCheckable(True)
    show_toolbar.setChecked(True)
    edit_menu.addAction(show_toolbar)

    show_statusbar = QAction("Show Status Bar", window)
    show_statusbar.setCheckable(True)
    show_statusbar.setChecked(True)
    edit_menu.addAction(show_statusbar)

    # View menu
    view_menu = menubar.addMenu("&View")
    view_menu.addAction("Zoom In")
    view_menu.addAction("Zoom Out")
    view_menu.addAction("Reset Zoom")

    # Help menu
    help_menu = menubar.addMenu("&Help")
    help_menu.addAction("About")
    help_menu.addAction("Documentation")

    return menubar


def create_status_bar(window):
    """Create status bar with various widgets.

    Args:
        window: Parent window

    Returns:
        QStatusBar: The created status bar
    """
    status = window.statusBar()

    # Add permanent widgets
    status.addWidget(QLabel("Line: 1"))
    status.addWidget(QLabel("Col: 1"))

    # Progress bar in status
    progress = QProgressBar()
    progress.setMaximumWidth(200)
    progress.setValue(45)
    status.addPermanentWidget(progress)

    # Don't set initial message to avoid overlapping
    return status
