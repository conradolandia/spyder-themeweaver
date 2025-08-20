"""
Asynchronous theme loading functionality for the ThemeWeaver preview application.
"""

from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker
from pathlib import Path
from .theme_cache import theme_cache
import re


class ThemeLoaderThread(QThread):
    """Thread for loading themes asynchronously."""

    # Signals to communicate with main thread
    theme_loaded = pyqtSignal(str, str, str)  # theme_name, variant, stylesheet
    loading_failed = pyqtSignal(str, str, str)  # theme_name, variant, error
    status_update = pyqtSignal(str)  # status message

    def __init__(self):
        super().__init__()
        self._mutex = QMutex()
        self._theme_name = None
        self._variant = None
        self._should_stop = False

    def load_theme_async(self, theme_name, variant):
        """Request asynchronous theme loading."""
        with QMutexLocker(self._mutex):
            self._theme_name = theme_name
            self._variant = variant
            self._should_stop = False

        if not self.isRunning():
            self.start()

    def stop_loading(self):
        """Stop current loading operation."""
        with QMutexLocker(self._mutex):
            self._should_stop = True

    def run(self):
        """Thread execution method."""
        with QMutexLocker(self._mutex):
            theme_name = self._theme_name
            variant = self._variant

        if not theme_name or not variant:
            return

        try:
            self.status_update.emit(f"Loading theme: {theme_name} ({variant})")

            # Check if we should stop
            with QMutexLocker(self._mutex):
                if self._should_stop:
                    return

            # Check processed cache first
            cached_stylesheet = theme_cache.get(theme_name, variant)
            if cached_stylesheet:
                self.status_update.emit(
                    f"Loaded theme from cache: {theme_name} ({variant})"
                )
                self.theme_loaded.emit(theme_name, variant, cached_stylesheet)
                return

            # Check raw cache to avoid file I/O
            raw_stylesheet = theme_cache.get_raw(theme_name, variant)
            if raw_stylesheet:
                self.status_update.emit(
                    f"Processing cached stylesheet: {theme_name} ({variant})"
                )
                # Process the raw stylesheet
                processed_stylesheet = self._convert_resource_paths_to_filesystem(
                    raw_stylesheet, theme_name, variant, None
                )
                # Cache the processed version
                theme_cache.set(theme_name, variant, processed_stylesheet)
                self.status_update.emit(
                    f"Processed and cached theme: {theme_name} ({variant})"
                )
                self.theme_loaded.emit(theme_name, variant, processed_stylesheet)
                return

            # Check if we should stop
            with QMutexLocker(self._mutex):
                if self._should_stop:
                    return

            # Get the build directory
            current_dir = Path(__file__).parent.parent.parent
            build_dir = current_dir / "build"

            # Look for the QSS file
            qss_file = build_dir / theme_name / variant / f"{variant}style.qss"

            if not qss_file.exists():
                self.loading_failed.emit(
                    theme_name, variant, f"Theme file not found: {qss_file}"
                )
                return

            self.status_update.emit(f"Reading stylesheet: {qss_file.name}")

            # Read the stylesheet
            with open(qss_file, "r", encoding="utf-8") as f:
                raw_stylesheet = f.read()

            # Cache the raw stylesheet to avoid future file I/O
            theme_cache.set_raw(theme_name, variant, raw_stylesheet)

            # Check if we should stop before processing
            with QMutexLocker(self._mutex):
                if self._should_stop:
                    return

            self.status_update.emit("Converting resource paths...")

            # Convert Qt resource paths to file system paths
            stylesheet = self._convert_resource_paths_to_filesystem(
                raw_stylesheet, theme_name, variant, build_dir
            )

            # Check if we should stop before caching
            with QMutexLocker(self._mutex):
                if self._should_stop:
                    return

            # Cache the processed stylesheet for future use
            theme_cache.set(theme_name, variant, stylesheet)

            self.status_update.emit(
                f"Loaded and cached theme: {theme_name} ({variant})"
            )
            self.theme_loaded.emit(theme_name, variant, stylesheet)

        except Exception as e:
            self.loading_failed.emit(theme_name, variant, str(e))

    def _convert_resource_paths_to_filesystem(
        self, stylesheet, theme_name, variant, build_dir
    ):
        """Convert Qt resource paths to file system paths in the stylesheet."""
        # Pattern to match Qt resource paths like :/qss_icons/dark/rc/icon.png
        resource_pattern = r'url\(":/qss_icons/([^"]+)"\)'

        # Use relative paths instead of absolute paths
        # build_dir might be None when processing from raw cache
        relative_path = f"build/{theme_name}/{variant}/rc"

        def replace_resource_path(match):
            resource_path = match.group(1)  # e.g., "dark/rc/icon.png"

            # Extract just the filename from the resource path
            filename = resource_path.split("/rc/")[-1]

            # Build the relative path
            rel_path = f"{relative_path}/{filename}"

            # Qt stylesheets work better with relative paths
            return f'url("{rel_path}")'

        # Replace all resource paths with file system paths
        return re.sub(resource_pattern, replace_resource_path, stylesheet)


class ThemePreloader(QThread):
    """Thread for preloading all available themes in the background."""

    # Signals
    preload_progress = pyqtSignal(str, int, int)  # status, current, total
    preload_complete = pyqtSignal(int)  # number of themes preloaded

    def __init__(self, themes):
        super().__init__()
        self._themes = themes
        self._should_stop = False

    def stop_preloading(self):
        """Stop preloading operation."""
        self._should_stop = True

    def run(self):
        """Preload all themes in background."""
        variants = ["dark", "light"]
        total_themes = len(self._themes) * len(variants)
        loaded_count = 0

        current_dir = Path(__file__).parent.parent.parent
        build_dir = current_dir / "build"

        for i, theme_name in enumerate(self._themes):
            if self._should_stop:
                break

            for variant in variants:
                if self._should_stop:
                    break

                # Skip if already cached (check both processed and raw)
                if theme_cache.get(theme_name, variant) or theme_cache.get_raw(
                    theme_name, variant
                ):
                    loaded_count += 1
                    continue

                try:
                    current = i * len(variants) + variants.index(variant) + 1
                    self.preload_progress.emit(
                        f"Preloading {theme_name} ({variant})", current, total_themes
                    )

                    qss_file = build_dir / theme_name / variant / f"{variant}style.qss"

                    if qss_file.exists():
                        with open(qss_file, "r", encoding="utf-8") as f:
                            raw_stylesheet = f.read()

                        # Cache raw stylesheet first
                        theme_cache.set_raw(theme_name, variant, raw_stylesheet)

                        # Convert resource paths and cache processed version
                        loader = ThemeLoaderThread()
                        processed_stylesheet = (
                            loader._convert_resource_paths_to_filesystem(
                                raw_stylesheet, theme_name, variant, build_dir
                            )
                        )

                        # Cache the processed stylesheet
                        theme_cache.set(theme_name, variant, processed_stylesheet)
                        loaded_count += 1

                except Exception:
                    # Silently skip failed themes during preloading
                    pass

        if not self._should_stop:
            self.preload_complete.emit(loaded_count)
