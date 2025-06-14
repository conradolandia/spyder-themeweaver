"""QDarkStyle default dark palette."""

# Local imports
from colorsystem import (
    Green,
    GroupDark,
    GroupLight,
    Gunmetal,
    Logos,
    Midnight,
    Orange,
    Red,
)
from qdarkstyle.palette import Palette


class DarkPalette(Palette):
    """Dark palette variables."""

    # Identifier
    ID = "dark"

    # Background colors
    COLOR_BACKGROUND_1 = Gunmetal.B10
    COLOR_BACKGROUND_2 = Gunmetal.B20
    COLOR_BACKGROUND_3 = Gunmetal.B30
    COLOR_BACKGROUND_4 = Gunmetal.B20
    COLOR_BACKGROUND_5 = Gunmetal.B40
    COLOR_BACKGROUND_6 = Gunmetal.B50

    # Text colors
    COLOR_TEXT_1 = Gunmetal.B130
    COLOR_TEXT_2 = Gunmetal.B120
    COLOR_TEXT_3 = Gunmetal.B110
    COLOR_TEXT_4 = Gunmetal.B100

    # Accent colors
    COLOR_ACCENT_1 = Midnight.B10
    COLOR_ACCENT_2 = Midnight.B20
    COLOR_ACCENT_3 = Midnight.B30
    COLOR_ACCENT_4 = Midnight.B40
    COLOR_ACCENT_5 = Midnight.B50

    # Disabled elements
    COLOR_DISABLED = Gunmetal.B70

    # Colors for information and feedback in dialogs
    COLOR_SUCCESS_1 = Green.B40
    COLOR_SUCCESS_2 = Green.B70
    COLOR_SUCCESS_3 = Green.B90

    COLOR_ERROR_1 = Red.B40
    COLOR_ERROR_2 = Red.B70
    COLOR_ERROR_3 = Red.B110

    COLOR_WARN_1 = Orange.B40
    COLOR_WARN_2 = Orange.B70
    COLOR_WARN_3 = Orange.B90
    COLOR_WARN_4 = Orange.B100

    # Icon colors
    ICON_1 = Gunmetal.B140
    ICON_2 = Midnight.B80
    ICON_3 = Green.B80
    ICON_4 = Red.B70
    ICON_5 = Orange.B70
    ICON_6 = Gunmetal.B30

    # Colors for icons and variable explorer in dark mode
    GROUP_1 = GroupDark.B10
    GROUP_2 = GroupDark.B20
    GROUP_3 = GroupDark.B30
    GROUP_4 = GroupDark.B40
    GROUP_5 = GroupDark.B50
    GROUP_6 = GroupDark.B60
    GROUP_7 = GroupDark.B70
    GROUP_8 = GroupDark.B80
    GROUP_9 = GroupDark.B90
    GROUP_10 = GroupDark.B100
    GROUP_11 = GroupDark.B110
    GROUP_12 = GroupDark.B120

    # Colors for highlight in editor
    COLOR_HIGHLIGHT_1 = Midnight.B10
    COLOR_HIGHLIGHT_2 = Midnight.B20
    COLOR_HIGHLIGHT_3 = Midnight.B30
    COLOR_HIGHLIGHT_4 = Midnight.B50

    # Colors for occurrences from find widget
    COLOR_OCCURRENCE_1 = Gunmetal.B10
    COLOR_OCCURRENCE_2 = Gunmetal.B20
    COLOR_OCCURRENCE_3 = Gunmetal.B30
    COLOR_OCCURRENCE_4 = Gunmetal.B50
    COLOR_OCCURRENCE_5 = Gunmetal.B80

    # Colors for Spyder and Python logos
    PYTHON_LOGO_UP = Logos.B10
    PYTHON_LOGO_DOWN = Logos.B20
    SPYDER_LOGO_BACKGROUND = Logos.B30
    SPYDER_LOGO_WEB = Logos.B40
    SPYDER_LOGO_SNAKE = Logos.B50

    # For special tabs
    SPECIAL_TABS_SEPARATOR = Gunmetal.B70
    SPECIAL_TABS_SELECTED = COLOR_ACCENT_2

    # For the heart used to ask for donations
    COLOR_HEART = Midnight.B80

    # For editor tooltips
    TIP_TITLE_COLOR = Green.B80
    TIP_CHAR_HIGHLIGHT_COLOR = Orange.B90

    # Tooltip opacity
    OPACITY_TOOLTIP = 230


class LightPalette(Palette):
    """Light palette variables."""

    # Identifier
    ID = "light"

    # Background colors
    COLOR_BACKGROUND_1 = Gunmetal.B140
    COLOR_BACKGROUND_2 = Gunmetal.B130
    COLOR_BACKGROUND_3 = Gunmetal.B120
    COLOR_BACKGROUND_4 = Gunmetal.B110
    COLOR_BACKGROUND_5 = Gunmetal.B100
    COLOR_BACKGROUND_6 = Gunmetal.B90

    # Text colors
    COLOR_TEXT_1 = Gunmetal.B20
    COLOR_TEXT_2 = Gunmetal.B30
    COLOR_TEXT_3 = Gunmetal.B50
    COLOR_TEXT_4 = Gunmetal.B70

    # Accent colors
    COLOR_ACCENT_1 = Midnight.B70
    COLOR_ACCENT_2 = Midnight.B60
    COLOR_ACCENT_3 = Midnight.B50
    COLOR_ACCENT_4 = Midnight.B40
    COLOR_ACCENT_5 = Midnight.B30

    # Disabled elements
    COLOR_DISABLED = Gunmetal.B60

    # Colors for information and feedback in dialogs
    COLOR_SUCCESS_1 = Green.B40
    COLOR_SUCCESS_2 = Green.B70
    COLOR_SUCCESS_3 = Green.B30

    COLOR_ERROR_1 = Red.B40
    COLOR_ERROR_2 = Red.B70
    COLOR_ERROR_3 = Red.B110

    COLOR_WARN_1 = Orange.B40
    COLOR_WARN_2 = Orange.B70
    COLOR_WARN_3 = Orange.B50
    COLOR_WARN_4 = Orange.B40

    # Icon colors
    ICON_1 = Gunmetal.B30
    ICON_2 = Midnight.B50
    ICON_3 = Green.B30
    ICON_4 = Red.B70
    ICON_5 = Orange.B70
    ICON_6 = Gunmetal.B140

    # Colors for icons and variable explorer in light mode
    GROUP_1 = GroupLight.B10
    GROUP_2 = GroupLight.B20
    GROUP_3 = GroupLight.B30
    GROUP_4 = GroupLight.B40
    GROUP_5 = GroupLight.B50
    GROUP_6 = GroupLight.B60
    GROUP_7 = GroupLight.B70
    GROUP_8 = GroupLight.B80
    GROUP_9 = GroupLight.B90
    GROUP_10 = GroupLight.B100
    GROUP_11 = GroupLight.B110
    GROUP_12 = GroupLight.B120

    # Colors for highlight in editor
    COLOR_HIGHLIGHT_1 = Midnight.B140
    COLOR_HIGHLIGHT_2 = Midnight.B130
    COLOR_HIGHLIGHT_3 = Midnight.B120
    COLOR_HIGHLIGHT_4 = Midnight.B110

    # Colors for occurrences from find widget
    COLOR_OCCURRENCE_1 = Gunmetal.B120
    COLOR_OCCURRENCE_2 = Gunmetal.B110
    COLOR_OCCURRENCE_3 = Gunmetal.B100
    COLOR_OCCURRENCE_4 = Gunmetal.B90
    COLOR_OCCURRENCE_5 = Gunmetal.B60

    # Colors for Spyder and Python logos
    PYTHON_LOGO_UP = Logos.B10
    PYTHON_LOGO_DOWN = Logos.B20
    SPYDER_LOGO_BACKGROUND = Logos.B30
    SPYDER_LOGO_WEB = Logos.B40
    SPYDER_LOGO_SNAKE = Logos.B50

    # For special tabs
    SPECIAL_TABS_SEPARATOR = Gunmetal.B70
    SPECIAL_TABS_SELECTED = COLOR_ACCENT_5

    # For the heart used to ask for donations
    COLOR_HEART = Red.B70

    # For editor tooltips
    TIP_TITLE_COLOR = Green.B20
    TIP_CHAR_HIGHLIGHT_COLOR = Orange.B30

    # Tooltip opacity
    OPACITY_TOOLTIP = 230
