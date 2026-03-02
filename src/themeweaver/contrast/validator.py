"""Contrast validation engine."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from themeweaver.color_utils import (
    adjust_for_contrast,
    blend_alpha,
    contrast_ratio,
)
from themeweaver.contrast.color_resolver import get_color_for_rule, resolve_theme_colors
from themeweaver.contrast.rules_loader import load_rules


@dataclass
class RuleResult:
    """Result of validating a single contrast rule."""

    rule_id: str
    passed: bool
    actual_ratio: Optional[float] = None
    message: str = ""
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of contrast validation for a theme variant."""

    variant: str
    results: List[RuleResult] = field(default_factory=list)
    passed_count: int = 0
    failed_count: int = 0

    @property
    def all_passed(self) -> bool:
        return self.failed_count == 0


# Round contrast ratios to 1 decimal before comparison to avoid float precision issues
_CONTRAST_PRECISION = 1


def _round_ratio(ratio: float) -> float:
    return round(ratio, _CONTRAST_PRECISION)


def _sort_rules_by_dependency(rules: Dict[str, Any]) -> List[str]:
    """Sort rule IDs so that referenced rules (greater_than) come first."""
    order: List[str] = []
    seen: set = set()

    def visit(rid: str) -> None:
        if rid in seen:
            return
        seen.add(rid)
        rule = rules.get(rid)
        if rule and "greater_than" in rule:
            ref = rule["greater_than"]
            if ref in rules:
                visit(ref)
        order.append(rid)

    for rid in rules:
        visit(rid)
    return order


def validate_theme(
    theme_name: str,
    variant: str,
    themes_dir: Optional[Path] = None,
    rules_dir: Optional[Path] = None,
    include_suggestions: bool = True,
) -> ValidationResult:
    """
    Validate a theme's contrast against Spyder UI rules.

    Args:
        theme_name: Theme name
        variant: "dark" or "light"
        themes_dir: Themes directory
        rules_dir: Rules YAML directory
        include_suggestions: Whether to compute adjust_for_contrast suggestions for failures

    Returns:
        ValidationResult with per-rule pass/fail and optional suggestions
    """
    rules = load_rules(variant, rules_dir)
    default_tolerance = float(rules.pop("_default_tolerance", 0))
    colors = resolve_theme_colors(theme_name, variant, themes_dir)

    ratio_cache: Dict[str, float] = {}
    results: List[RuleResult] = []
    rule_order = _sort_rules_by_dependency(rules)

    for rule_id in rule_order:
        rule = rules.get(rule_id)
        if not rule:
            continue

        fg_hex = get_color_for_rule(colors, rule, "fg")
        bg_hex = get_color_for_rule(colors, rule, "bg")

        if not fg_hex or not bg_hex:
            results.append(
                RuleResult(
                    rule_id=rule_id,
                    passed=False,
                    message=f"Missing color: fg={fg_hex is None}, bg={bg_hex is None}",
                )
            )
            continue

        # PE22: fg has 75% opacity
        if rule.get("fg_opacity"):
            alpha = rule["fg_opacity"]
            fg_hex = blend_alpha(bg_hex, fg_hex, alpha)

        # PE5A-C: check fg/lbg, lbg/bg, fg/bg
        if "line_bg" in rule and "fg_lbg_min" in rule:
            line_bg_hex = get_color_for_rule(colors, rule, "line_bg")
            if not line_bg_hex:
                results.append(
                    RuleResult(rule_id=rule_id, passed=False, message="Missing line_bg")
                )
                continue

            fg_lbg = _round_ratio(contrast_ratio(fg_hex, line_bg_hex))
            lbg_bg = _round_ratio(contrast_ratio(line_bg_hex, bg_hex))
            fg_bg = _round_ratio(contrast_ratio(fg_hex, bg_hex))

            tol = float(rule.get("tolerance", default_tolerance))
            passed = True
            msg_parts = []
            min_fg_lbg = float(rule.get("fg_lbg_min", 0))
            min_lbg_bg = float(rule.get("lbg_bg_min", 0))
            min_fg_bg = float(rule.get("fg_bg_min", 0))
            if fg_lbg < min_fg_lbg - tol:
                passed = False
                msg_parts.append(f"FG/LBG {fg_lbg:.1f} < {min_fg_lbg}")
            if lbg_bg < min_lbg_bg - tol:
                passed = False
                msg_parts.append(f"LBG/BG {lbg_bg:.1f} < {min_lbg_bg}")
            if fg_bg < min_fg_bg - tol:
                passed = False
                msg_parts.append(f"FG/BG {fg_bg:.1f} < {min_fg_bg}")

            ratio_cache[rule_id] = fg_bg
            suggestion = None
            if not passed and include_suggestions:
                orig_fg = get_color_for_rule(colors, rule, "fg")
                if orig_fg:
                    min_r = rule.get("fg_bg_min", 9)
                    suggestion_hex = adjust_for_contrast(orig_fg, bg_hex, min_r)
                    if suggestion_hex:
                        suggestion = f"Try {rule['fg']}: {suggestion_hex} (was {orig_fg}) to meet ratio {min_r}"

            results.append(
                RuleResult(
                    rule_id=rule_id,
                    passed=passed,
                    actual_ratio=fg_bg,
                    message="; ".join(msg_parts) if msg_parts else "OK",
                    suggestion=suggestion,
                )
            )
            continue

        # Standard contrast check
        ratio = _round_ratio(contrast_ratio(fg_hex, bg_hex))
        ratio_cache[rule_id] = ratio

        passed = True
        msg_parts = []
        failed_min = False

        tol = float(rule.get("tolerance", default_tolerance))
        min_ratio = float(rule["min_ratio"]) if "min_ratio" in rule else None
        max_ratio = float(rule["max_ratio"]) if "max_ratio" in rule else None
        if min_ratio is not None and ratio < min_ratio - tol:
            passed = False
            failed_min = True
            msg_parts.append(f"ratio {ratio:.1f} < {min_ratio}")

        if max_ratio is not None and ratio > max_ratio + tol:
            passed = False
            msg_parts.append(f"ratio {ratio:.1f} > {max_ratio}")

        if "greater_than" in rule:
            ref_ratio = ratio_cache.get(rule["greater_than"])
            if ref_ratio is not None:
                ref_rounded = _round_ratio(ref_ratio)
                if ratio < ref_rounded - tol:
                    passed = False
                    msg_parts.append(
                        f"ratio {ratio:.1f} <= {rule['greater_than']} ({ref_rounded:.1f})"
                    )

        suggestion = None
        if (
            not passed
            and include_suggestions
            and failed_min
            and "fg_opacity" not in rule
        ):
            orig_fg = get_color_for_rule(colors, rule, "fg")
            if orig_fg and "fg_opacity" not in rule:
                min_r = rule["min_ratio"]
                suggestion_hex = adjust_for_contrast(orig_fg, bg_hex, min_r)
                if suggestion_hex:
                    suggestion = f"Try {rule['fg']}: {suggestion_hex} (was {orig_fg}) to meet ratio {min_r}"

        results.append(
            RuleResult(
                rule_id=rule_id,
                passed=passed,
                actual_ratio=ratio,
                message="; ".join(msg_parts) if msg_parts else "OK",
                suggestion=suggestion,
            )
        )

    passed_count = sum(1 for r in results if r.passed)
    failed_count = len(results) - passed_count

    return ValidationResult(
        variant=variant,
        results=results,
        passed_count=passed_count,
        failed_count=failed_count,
    )
