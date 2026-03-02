"""Spyder UI color contrast validation."""

from themeweaver.contrast.color_resolver import resolve_theme_colors
from themeweaver.contrast.rules_loader import load_rules
from themeweaver.contrast.validator import RuleResult, ValidationResult, validate_theme

__all__ = [
    "load_rules",
    "resolve_theme_colors",
    "validate_theme",
    "ValidationResult",
    "RuleResult",
]
