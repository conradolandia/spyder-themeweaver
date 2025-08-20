"""
Theme caching system for the ThemeWeaver preview application.

This module provides caching functionality to speed up theme switching
by storing loaded themes in memory.
"""

from typing import Dict, Optional, Tuple
import time


class ThemeCache:
    """Cache for loaded themes to improve performance."""

    def __init__(self):
        self._cache: Dict[
            str, Tuple[str, float]
        ] = {}  # key: (theme_name, variant), value: (stylesheet, timestamp)
        self._raw_cache: Dict[
            str, Tuple[str, float]
        ] = {}  # Cache for raw (unprocessed) stylesheets
        self._cache_timeout = 300  # 5 minutes cache timeout
        self._max_cache_size = 20  # Maximum number of cached themes

    def _get_cache_key(self, theme_name: str, variant: str) -> str:
        """Generate cache key for theme and variant."""
        return f"{theme_name}:{variant}"

    def get(self, theme_name: str, variant: str) -> Optional[str]:
        """Get cached stylesheet if available and not expired."""
        cache_key = self._get_cache_key(theme_name, variant)

        if cache_key in self._cache:
            stylesheet, timestamp = self._cache[cache_key]
            current_time = time.time()

            # Check if cache entry is still valid
            if current_time - timestamp < self._cache_timeout:
                return stylesheet
            else:
                # Remove expired entry
                del self._cache[cache_key]

        return None

    def set(self, theme_name: str, variant: str, stylesheet: str) -> None:
        """Cache a stylesheet for theme and variant."""
        cache_key = self._get_cache_key(theme_name, variant)
        current_time = time.time()

        # Remove oldest entries if cache is full
        if len(self._cache) >= self._max_cache_size:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]

        self._cache[cache_key] = (stylesheet, current_time)

    def get_raw(self, theme_name: str, variant: str) -> Optional[str]:
        """Get cached raw stylesheet if available and not expired."""
        cache_key = self._get_cache_key(theme_name, variant)

        if cache_key in self._raw_cache:
            stylesheet, timestamp = self._raw_cache[cache_key]
            current_time = time.time()

            # Check if cache entry is still valid
            if current_time - timestamp < self._cache_timeout:
                return stylesheet
            else:
                # Remove expired entry
                del self._raw_cache[cache_key]

        return None

    def set_raw(self, theme_name: str, variant: str, stylesheet: str) -> None:
        """Cache a raw stylesheet for theme and variant."""
        cache_key = self._get_cache_key(theme_name, variant)
        current_time = time.time()

        # Remove oldest entries if cache is full
        if len(self._raw_cache) >= self._max_cache_size:
            oldest_key = min(
                self._raw_cache.keys(), key=lambda k: self._raw_cache[k][1]
            )
            del self._raw_cache[oldest_key]

        self._raw_cache[cache_key] = (stylesheet, current_time)

    def clear(self) -> None:
        """Clear all cached themes."""
        self._cache.clear()
        self._raw_cache.clear()

    def remove(self, theme_name: str, variant: str) -> None:
        """Remove specific theme from cache."""
        cache_key = self._get_cache_key(theme_name, variant)
        if cache_key in self._cache:
            del self._cache[cache_key]
        if cache_key in self._raw_cache:
            del self._raw_cache[cache_key]

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "cached_themes": len(self._cache),
            "cached_raw_themes": len(self._raw_cache),
            "max_cache_size": self._max_cache_size,
            "cache_timeout": self._cache_timeout,
        }


# Global cache instance
theme_cache = ThemeCache()
