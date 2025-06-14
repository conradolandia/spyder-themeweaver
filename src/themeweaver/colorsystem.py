# Solarized Palette for Spyder
# Based on the Solarized color palette, but with a wider range of colors
# https://ethanschoonover.com/solarized/

import yaml
from pathlib import Path


def _load_colors_from_yaml():
    """Load color definitions from colorsystem.yaml file."""
    # Get the directory where this Python file is located
    current_dir = Path(__file__).parent
    yaml_file = current_dir / "colorsystem.yaml"
    
    try:
        with open(yaml_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Color system YAML file not found: {yaml_file}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")


def _create_color_class(name, colors):
    """Dynamically create a color class with the given name and color values."""
    class_attrs = {}
    for key, value in colors.items():
        class_attrs[key] = value
    
    # Create the class dynamically
    color_class = type(name, (), class_attrs)
    return color_class


# Load colors from YAML and create classes
_color_data = _load_colors_from_yaml()

# Create all color classes dynamically
Primary = _create_color_class('Primary', _color_data['Gunmetal'])
Secondary = _create_color_class('Secondary', _color_data['Midnight'])
Green = _create_color_class('Green', _color_data['Green'])
Red = _create_color_class('Red', _color_data['Red'])
Orange = _create_color_class('Orange', _color_data['Orange'])
GroupDark = _create_color_class('GroupDark', _color_data['GroupDark'])
GroupLight = _create_color_class('GroupLight', _color_data['GroupLight'])
Logos = _create_color_class('Logos', _color_data['Logos'])


# Export all classes for backward compatibility
__all__ = [
    'Primary',
    'Secondary', 
    'Green',
    'Red',
    'Orange',
    'GroupDark',
    'GroupLight',
    'Logos'
]
