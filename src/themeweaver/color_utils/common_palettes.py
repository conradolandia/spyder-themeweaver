"""
Common color palettes for reference and analysis.

This module contains well-known color palettes that can be used for
analysis and inspiration in theme generation.
"""

import logging
import yaml
from pathlib import Path

_logger = logging.getLogger(__name__)

# Path to the common palettes YAML file
_PALETTES_FILE = Path(__file__).parent / "common_palettes.yaml"


def _load_common_palettes():
    """Load common palettes from YAML file."""
    try:
        with open(_PALETTES_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        _logger.warning("Could not load common palettes from %s: %s", _PALETTES_FILE, e)
        return {}


# Load common palettes from YAML
COMMON_PALETTES = _load_common_palettes()


def get_palette_names():
    """Get list of available common palette names."""
    return list(COMMON_PALETTES.keys())


def get_palette(name):
    """Get a common palette by name."""
    return COMMON_PALETTES.get(name)


def get_all_palettes():
    """Get all common palettes."""
    return COMMON_PALETTES.copy()
