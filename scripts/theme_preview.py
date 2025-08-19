#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Preview Application for ThemeWeaver

Qt application to preview and test generated themes,
showcasing all the UI elements styled in the QSS files.

This file is a simple wrapper that imports and runs the modular implementation
from the scripts/preview package.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.preview.main import main

if __name__ == "__main__":
    main()
