"""
Syntax highlighting preview tab for ThemeWeaver.

This tab shows code examples with syntax highlighting using the current theme's
syntax colors.
"""

# Import yaml directly instead of using themeweaver loaders
import yaml
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SyntaxHighlighter(QPlainTextEdit):
    """Custom text editor with syntax highlighting based on theme colors."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Set monospace font
        font = QFont("Monospace")
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(10)
        self.setFont(font)

        # Set minimum size
        self.setMinimumSize(QSize(500, 300))

        # Default colors (will be overridden by theme)
        self.colors = {
            "background": "#ffffff",
            "currentline": "#f7f7f7",
            "currentcell": "#eaeaea",
            "normal": "#000000",
            "keyword": "#0000ff",
            "magic": "#0000ff",
            "builtin": "#900090",
            "definition": "#000000",
            "comment": "#adadad",
            "string": "#00aa00",
            "number": "#800000",
            "instance": "#924900",
        }

        self.formats = {
            "normal": [False, False],
            "keyword": [False, False],
            "magic": [False, False],
            "builtin": [False, False],
            "definition": [True, False],
            "comment": [False, True],
            "string": [False, False],
            "number": [False, False],
            "instance": [False, True],
        }

        # Set default style
        self.update_style()

    def update_theme_colors(self, theme_name, variant):
        """Update colors based on theme and variant."""
        try:
            # Determine the theme path - look in src directory
            from pathlib import Path

            # Theme YAML files are in the src directory
            theme_dir = (
                Path(__file__).parent.parent.parent
                / "src"
                / "themeweaver"
                / "themes"
                / theme_name
            )

            # Load colors data from the appropriate directory
            colors_path = theme_dir / "colorsystem.yaml"
            mappings_path = theme_dir / "mappings.yaml"

            if not colors_path.exists() or not mappings_path.exists():
                print(f"Theme files not found for {theme_name}")
                return

            # Load data from files
            with open(colors_path, "r") as f:
                colors_data = yaml.safe_load(f)

            with open(mappings_path, "r") as f:
                mappings_yaml = yaml.safe_load(f)
                mappings_data = mappings_yaml.get("color_classes", {})
                semantic_mappings = mappings_yaml.get("semantic_mappings", {})

            # Determine which syntax palette to use
            syntax_class = "Syntax" if variant.lower() == "dark" else "SyntaxLight"
            syntax_palette_name = mappings_data.get(syntax_class)

            if not syntax_palette_name or syntax_palette_name not in colors_data:
                print(
                    f"Warning: Syntax palette '{syntax_palette_name}' not found for {variant} variant"
                )
                return

            # Debug info
            print(
                f"Using {syntax_class} palette: {syntax_palette_name} for {variant} variant"
            )

            # Get the semantic mappings for the current variant
            variant_mappings = semantic_mappings.get(variant.lower(), {})

            # Map editor colors
            self.colors["background"] = self._resolve_color(
                variant_mappings.get("EDITOR_BACKGROUND", ""),
                colors_data,
                mappings_data,
            )
            self.colors["currentline"] = self._resolve_color(
                variant_mappings.get("EDITOR_CURRENTLINE", ""),
                colors_data,
                mappings_data,
            )
            self.colors["currentcell"] = self._resolve_color(
                variant_mappings.get("EDITOR_CURRENTCELL", ""),
                colors_data,
                mappings_data,
            )

            # Map syntax colors
            for key in [
                "EDITOR_NORMAL",
                "EDITOR_KEYWORD",
                "EDITOR_MAGIC",
                "EDITOR_BUILTIN",
                "EDITOR_DEFINITION",
                "EDITOR_COMMENT",
                "EDITOR_STRING",
                "EDITOR_NUMBER",
                "EDITOR_INSTANCE",
            ]:
                simple_key = key.replace("EDITOR_", "").lower()

                value = variant_mappings.get(key)
                if isinstance(value, list) and len(value) >= 1:
                    # Format is [color_ref, bold, italic]
                    color_ref = value[0]
                    if len(value) >= 3:
                        self.formats[simple_key] = [value[1], value[2]]

                    color = self._resolve_color(color_ref, colors_data, mappings_data)
                    if color:
                        self.colors[simple_key] = color

            # Update the style
            self.update_style()

        except Exception as e:
            print(f"Error loading syntax colors: {e}")

    def _resolve_color(self, color_ref, colors_data, mappings_data):
        """Resolve a color reference to an actual hex color."""
        if not isinstance(color_ref, str) or "." not in color_ref:
            return None

        class_name, color_name = color_ref.split(".", 1)

        # Get the palette name from mappings
        palette_name = mappings_data.get(class_name)
        if not palette_name:
            return None

        # Get the color from the palette
        palette = colors_data.get(palette_name, {})
        return palette.get(color_name, "#000000")

    def update_style(self):
        """Update the editor style based on current colors."""
        # Set background color
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {self.colors["background"]};
                color: {self.colors["normal"]};
            }}
        """)

        # Highlight current line
        extra_selections = []
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(self.colors["currentline"]))
        selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

        # Force update
        self.update()

    def apply_syntax_highlighting(self):
        """Apply syntax highlighting to the current text."""
        # This is a simplified version that just uses different colors for different parts
        # In a real implementation, you would use a proper syntax highlighter

        cursor = self.textCursor()
        cursor.setPosition(0)

        # Save the original text and clear the editor
        text = self.toPlainText()
        self.clear()

        # Create formats for different syntax elements
        formats = {}
        for key, format_flags in self.formats.items():
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(self.colors[key]))
            if format_flags[0]:  # Bold
                fmt.setFontWeight(QFont.Bold)
            if format_flags[1]:  # Italic
                fmt.setFontItalic(True)
            formats[key] = fmt

        # Simple parsing of Python code
        lines = text.split("\n")
        for line in lines:
            # Process each line
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)

            # Default to normal text
            self.setCurrentCharFormat(formats["normal"])

            # Simple syntax highlighting
            if line.strip().startswith("#"):
                # Comment
                self.setCurrentCharFormat(formats["comment"])
                self.insertPlainText(line + "\n")
            elif line.strip().startswith("def "):
                # Function definition
                parts = line.split("def ", 1)
                self.insertPlainText(parts[0])

                self.setCurrentCharFormat(formats["keyword"])
                self.insertPlainText("def ")

                # Function name
                name_parts = parts[1].split("(", 1)
                self.setCurrentCharFormat(formats["definition"])
                self.insertPlainText(name_parts[0])

                # Parameters
                self.setCurrentCharFormat(formats["normal"])
                self.insertPlainText("(" + name_parts[1] + "\n")
            elif line.strip().startswith("class "):
                # Class definition
                parts = line.split("class ", 1)
                self.insertPlainText(parts[0])

                self.setCurrentCharFormat(formats["keyword"])
                self.insertPlainText("class ")

                # Class name
                name_parts = parts[1].split(":", 1)
                self.setCurrentCharFormat(formats["definition"])
                self.insertPlainText(name_parts[0])

                if len(name_parts) > 1:
                    self.setCurrentCharFormat(formats["normal"])
                    self.insertPlainText(":" + name_parts[1])
                self.insertPlainText("\n")
            elif '"' in line or "'" in line:
                # String handling (simplified)
                in_string = False
                string_char = None
                current_part = ""

                for char in line:
                    if not in_string and (char == '"' or char == "'"):
                        # Start of string
                        if current_part:
                            self.setCurrentCharFormat(formats["normal"])
                            self.insertPlainText(current_part)
                            current_part = ""

                        in_string = True
                        string_char = char
                        current_part = char
                    elif in_string and char == string_char:
                        # End of string
                        current_part += char
                        self.setCurrentCharFormat(formats["string"])
                        self.insertPlainText(current_part)
                        current_part = ""
                        in_string = False
                    else:
                        current_part += char

                # Handle any remaining text
                if current_part:
                    if in_string:
                        self.setCurrentCharFormat(formats["string"])
                    else:
                        self.setCurrentCharFormat(formats["normal"])
                    self.insertPlainText(current_part)

                self.insertPlainText("\n")
            else:
                # Handle keywords
                keywords = [
                    "import",
                    "from",
                    "as",
                    "if",
                    "else",
                    "elif",
                    "for",
                    "while",
                    "return",
                    "True",
                    "False",
                    "None",
                    "and",
                    "or",
                    "not",
                    "in",
                    "is",
                ]

                words = []
                current_word = ""
                for char in line:
                    if char.isalnum() or char == "_":
                        current_word += char
                    else:
                        if current_word:
                            words.append((current_word, char))
                            current_word = ""
                        else:
                            words.append(("", char))

                if current_word:
                    words.append((current_word, ""))

                for word, separator in words:
                    if word in keywords:
                        self.setCurrentCharFormat(formats["keyword"])
                        self.insertPlainText(word)
                    elif word.startswith("__") and word.endswith("__"):
                        self.setCurrentCharFormat(formats["magic"])
                        self.insertPlainText(word)
                    elif word.isdigit() or (word and word[0].isdigit()):
                        self.setCurrentCharFormat(formats["number"])
                        self.insertPlainText(word)
                    elif word:
                        self.setCurrentCharFormat(formats["normal"])
                        self.insertPlainText(word)

                    if separator:
                        self.setCurrentCharFormat(formats["normal"])
                        self.insertPlainText(separator)

                self.insertPlainText("\n")

        # Move cursor to beginning
        cursor = self.textCursor()
        cursor.setPosition(0)
        self.setTextCursor(cursor)


class SyntaxTab(QWidget):
    """Tab showing syntax highlighting examples."""

    def __init__(self):
        super().__init__()
        self._current_theme = None
        self._current_variant = None
        self._init_ui()

    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)

        # Header with language selector
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Syntax Highlighting Preview"))

        self.language_combo = QComboBox()
        self.language_combo.addItem("Python")
        # Could add more languages in the future
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        header_layout.addWidget(QLabel("Language:"))
        header_layout.addWidget(self.language_combo)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Syntax highlighting preview
        self.editor = SyntaxHighlighter()
        layout.addWidget(self.editor)

        # Load example code
        self._load_example_code()

    def _load_example_code(self):
        """Load example code based on selected language."""
        language = self.language_combo.currentText()

        if language == "Python":
            code = self._get_python_example()
        else:
            code = "# No example available for this language"

        self.editor.setPlainText(code)
        self.editor.apply_syntax_highlighting()

    def _on_language_changed(self, language):
        """Handle language change."""
        self._load_example_code()
        self.editor.apply_syntax_highlighting()

    def _get_python_example(self):
        """Get Python example code."""
        return '''# Example Python code for syntax highlighting
import os
import sys
from datetime import datetime

class SyntaxExample:
    """A class to demonstrate syntax highlighting."""

    def __init__(self, name, value=42):
        self.name = name
        self.value = value
        self._created_at = datetime.now()

    def calculate(self, x, y=10):
        """Perform a calculation with the given values."""
        result = 0

        # Loop through a range
        for i in range(y):
            if i % 2 == 0:
                result += x * i
            else:
                result -= x / (i + 1)

        return result

    @property
    def age(self):
        """Return the age of this object in seconds."""
        delta = datetime.now() - self._created_at
        return delta.total_seconds()

# Create an instance and use it
example = SyntaxExample("Test", 100)
value = example.calculate(5)
print(f"The result is: {value}")
print(f"Object age: {example.age} seconds")

# Constants and special values
MAX_VALUE = 1000
MIN_VALUE = -1000
PI = 3.14159265359
ENABLED = True
DISABLED = False
EMPTY = None

# Conditional logic
if ENABLED and value < MAX_VALUE:
    print("Value is within acceptable range")
elif value >= MAX_VALUE:
    print("Value exceeds maximum")
else:
    print("Feature is disabled")
'''

    def update_colors(self):
        """Update colors based on current theme/variant."""
        if not self._current_theme or not self._current_variant:
            print("No theme or variant set")
            return

        print(
            f"Updating colors for theme: {self._current_theme}, variant: {self._current_variant}"
        )
        self.editor.update_theme_colors(self._current_theme, self._current_variant)
        self.editor.apply_syntax_highlighting()

    def set_theme(self, theme_name, variant):
        """Set the current theme and variant."""
        print(f"Setting theme: {theme_name}, variant: {variant}")
        self._current_theme = theme_name
        self._current_variant = variant
        self.update_colors()
