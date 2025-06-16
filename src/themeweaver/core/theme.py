"""Theme class for ThemeWeaver."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qdarkstyle.palette import Palette


class Theme:
    """Represents a theme with dark and light palette variants."""

    def __init__(self, name: str, dark_palette: "Palette", light_palette: "Palette"):
        """Initialize Theme with name and palette variants.

        Args:
            name: Theme name
            dark_palette: Dark variant palette class
            light_palette: Light variant palette class
        """
        self.name = name
        self.dark_palette = dark_palette
        self.light_palette = light_palette

    def __str__(self):
        """String representation of the theme."""
        return f"{self.name} ({self.dark_palette.ID} / {self.light_palette.ID})"
