"""Load contrast rules from YAML files."""

from pathlib import Path
from typing import Any, Dict, List

import yaml


def _expand_rules(data: Dict[str, Any]) -> Dict[str, Any]:
    """Expand parameterized rules (e.g. PG with bg_overlays) into concrete rules."""
    result: Dict[str, Any] = {}
    for key, value in data.items():
        if key.startswith("_"):
            result[key] = value
            continue
        if not isinstance(value, dict):
            result[key] = value
            continue
        rule = dict(value)
        overlays: List[str] = rule.pop("bg_overlays", None)
        if overlays is None:
            result[key] = rule
            continue
        bg_base = rule.pop("bg_base")
        for i, overlay in enumerate(overlays, start=1):
            expanded = dict(rule)
            expanded["bg"] = [bg_base, overlay]
            result[f"{key}{i}"] = expanded
    return result


def _get_rules_dir() -> Path:
    """Return the directory containing rules YAML files."""
    return Path(__file__).parent


def load_rules(variant: str, rules_dir: Path | None = None) -> Dict[str, Any]:
    """
    Load contrast rules for a variant (dark or light).

    Args:
        variant: "dark" or "light"
        rules_dir: Directory containing rules_dark.yaml and rules_light.yaml.
                   If None, uses the package directory.

    Returns:
        Dict mapping rule ID to rule spec (fg, bg, min_ratio, etc.)
    """
    if rules_dir is None:
        rules_dir = _get_rules_dir()

    filename = f"rules_{variant}.yaml"
    filepath = rules_dir / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Rules file not found: {filepath}")

    with open(filepath, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        return {}
    return _expand_rules(data)
