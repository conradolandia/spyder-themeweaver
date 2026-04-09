"""
Single source of truth for syntax palette and editor role mappings.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Literal, Optional, Tuple

Variant = Literal["dark", "light"]
MappingKind = Literal["primary_plain", "syntax_plain", "syntax_formatted"]

SYNTAX_PALETTE_STEP = 10
SYNTAX_PALETTE_START = 10
SYNTAX_PALETTE_SLOT_COUNT = 17


@dataclass(frozen=True)
class EditorMappingSpec:
    spyder_key: str
    mapping_kind: MappingKind
    slot_index: Optional[int] = None
    format_element: Optional[str] = None
    primary_dark_ref: Optional[str] = None
    primary_light_ref: Optional[str] = None


def syntax_palette_slot_count() -> int:
    return SYNTAX_PALETTE_SLOT_COUNT


def syntax_palette_keys() -> List[str]:
    return [
        f"B{SYNTAX_PALETTE_START + i * SYNTAX_PALETTE_STEP}"
        for i in range(SYNTAX_PALETTE_SLOT_COUNT)
    ]


def default_format_bold_italic() -> Dict[str, Dict[str, bool]]:
    return {
        "normal": {"bold": False, "italic": False},
        "keyword": {"bold": True, "italic": False},
        "magic": {"bold": True, "italic": False},
        "builtin": {"bold": False, "italic": False},
        "definition": {"bold": False, "italic": False},
        "comment": {"bold": False, "italic": True},
        "string": {"bold": False, "italic": False},
        "number": {"bold": False, "italic": False},
        "instance": {"bold": False, "italic": True},
        "symbol": {"bold": False, "italic": False},
    }


def syntax_format_elements() -> Tuple[str, ...]:
    return tuple(default_format_bold_italic().keys())


EDITOR_MAPPING_SPECS: Tuple[EditorMappingSpec, ...] = (
    EditorMappingSpec(
        spyder_key="EDITOR_BACKGROUND",
        mapping_kind="primary_plain",
        primary_dark_ref="Primary.B10",
        primary_light_ref="Primary.B140",
    ),
    EditorMappingSpec("EDITOR_CURRENTLINE", "syntax_plain", slot_index=0),
    EditorMappingSpec("EDITOR_CURRENTCELL", "syntax_plain", slot_index=1),
    EditorMappingSpec("EDITOR_OCCURRENCE", "syntax_plain", slot_index=2),
    EditorMappingSpec("EDITOR_CTRLCLICK", "syntax_plain", slot_index=3),
    EditorMappingSpec("EDITOR_SIDEAREAS", "syntax_plain", slot_index=4),
    EditorMappingSpec("EDITOR_MATCHED_P", "syntax_plain", slot_index=5),
    EditorMappingSpec("EDITOR_UNMATCHED_P", "syntax_plain", slot_index=6),
    EditorMappingSpec(
        "EDITOR_NORMAL", "syntax_formatted", slot_index=7, format_element="normal"
    ),
    EditorMappingSpec(
        "EDITOR_KEYWORD", "syntax_formatted", slot_index=8, format_element="keyword"
    ),
    EditorMappingSpec(
        "EDITOR_MAGIC", "syntax_formatted", slot_index=9, format_element="magic"
    ),
    EditorMappingSpec(
        "EDITOR_BUILTIN", "syntax_formatted", slot_index=10, format_element="builtin"
    ),
    EditorMappingSpec(
        "EDITOR_DEFINITION",
        "syntax_formatted",
        slot_index=11,
        format_element="definition",
    ),
    EditorMappingSpec(
        "EDITOR_COMMENT", "syntax_formatted", slot_index=12, format_element="comment"
    ),
    EditorMappingSpec(
        "EDITOR_STRING", "syntax_formatted", slot_index=13, format_element="string"
    ),
    EditorMappingSpec(
        "EDITOR_NUMBER", "syntax_formatted", slot_index=14, format_element="number"
    ),
    EditorMappingSpec(
        "EDITOR_INSTANCE", "syntax_formatted", slot_index=15, format_element="instance"
    ),
    EditorMappingSpec(
        "EDITOR_SYMBOL", "syntax_formatted", slot_index=16, format_element="symbol"
    ),
)


def formatted_editor_keys() -> Tuple[str, ...]:
    return tuple(
        spec.spyder_key
        for spec in EDITOR_MAPPING_SPECS
        if spec.mapping_kind == "syntax_formatted"
    )


def _default_formatted_value(
    element: str, syntax_format: Optional[Dict[str, Dict[str, bool]]], color_ref: str
) -> List[object]:
    defaults = default_format_bold_italic()
    if syntax_format and element in syntax_format:
        format_spec = syntax_format[element]
        return [
            color_ref,
            format_spec.get("bold", False),
            format_spec.get("italic", False),
        ]

    fallback = defaults.get(element, {"bold": False, "italic": False})
    return [color_ref, fallback["bold"], fallback["italic"]]


def build_editor_syntax_mappings(
    variant: Variant,
    syntax_format: Optional[Dict[str, Dict[str, bool]]] = None,
    format_color: Optional[
        Callable[[str, Optional[Dict[str, Dict[str, bool]]], str], List[object]]
    ] = None,
) -> Dict[str, object]:
    syntax_class = "Syntax" if variant == "dark" else "SyntaxLight"
    keys = syntax_palette_keys()
    mappings: Dict[str, object] = {}

    for spec in EDITOR_MAPPING_SPECS:
        if spec.mapping_kind == "primary_plain":
            mappings[spec.spyder_key] = (
                spec.primary_dark_ref if variant == "dark" else spec.primary_light_ref
            )
            continue

        if spec.slot_index is None:
            raise ValueError(f"Missing slot_index for {spec.spyder_key}")
        if spec.slot_index >= len(keys):
            raise ValueError(f"Slot index out of range for {spec.spyder_key}")

        color_ref = f"{syntax_class}.{keys[spec.slot_index]}"

        if spec.mapping_kind == "syntax_plain":
            mappings[spec.spyder_key] = color_ref
            continue

        if spec.format_element is None:
            raise ValueError(f"Missing format_element for {spec.spyder_key}")

        if format_color:
            mappings[spec.spyder_key] = format_color(
                spec.format_element, syntax_format, color_ref
            )
        else:
            mappings[spec.spyder_key] = _default_formatted_value(
                spec.format_element, syntax_format, color_ref
            )

    return mappings
