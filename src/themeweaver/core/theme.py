from themeweaver.core.palette import DarkPalette, LightPalette


class Theme:
    def __init__(
        self, name: str, dark_palette: DarkPalette, light_palette: LightPalette
    ):
        self.name = name
        self.dark_palette = dark_palette
        self.light_palette = light_palette

    def __str__(self):
        return f"{self.name} ({self.dark_palette.ID} / {self.light_palette.ID})"
