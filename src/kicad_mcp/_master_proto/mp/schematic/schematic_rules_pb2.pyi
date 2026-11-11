from mp.common.types import base_types_pb2 as _base_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErcErrorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERCET_UNKNOWN: _ClassVar[ErcErrorType]
    ERCET_DUPLICATE_SHEET_NAME: _ClassVar[ErcErrorType]
    ERCET_ENDPOINT_OFF_GRID: _ClassVar[ErcErrorType]
    ERCET_PIN_NOT_CONNECTED: _ClassVar[ErcErrorType]
    ERCET_PIN_NOT_DRIVEN: _ClassVar[ErcErrorType]
    ERCET_POWERPIN_NOT_DRIVEN: _ClassVar[ErcErrorType]
    ERCET_HIERARCHICAL_LABEL: _ClassVar[ErcErrorType]
    ERCET_NOCONNECT_CONNECTED: _ClassVar[ErcErrorType]
    ERCET_NOCONNECT_NOT_CONNECTED: _ClassVar[ErcErrorType]
    ERCET_LABEL_NOT_CONNECTED: _ClassVar[ErcErrorType]
    ERCET_SIMILAR_LABELS: _ClassVar[ErcErrorType]
    ERCET_SIMILAR_POWER: _ClassVar[ErcErrorType]
    ERCET_SIMILAR_LABEL_AND_POWER: _ClassVar[ErcErrorType]
    ERCET_SINGLE_GLOBAL_LABEL: _ClassVar[ErcErrorType]
    ERCET_SAME_LOCAL_GLOBAL_LABEL: _ClassVar[ErcErrorType]
    ERCET_SAME_LOCAL_GLOBAL_POWER: _ClassVar[ErcErrorType]
    ERCET_DIFFERENT_UNIT_FP: _ClassVar[ErcErrorType]
    ERCET_MISSING_POWER_INPUT_PIN: _ClassVar[ErcErrorType]
    ERCET_MISSING_INPUT_PIN: _ClassVar[ErcErrorType]
    ERCET_MISSING_BIDI_PIN: _ClassVar[ErcErrorType]
    ERCET_MISSING_UNIT: _ClassVar[ErcErrorType]
    ERCET_DIFFERENT_UNIT_NET: _ClassVar[ErcErrorType]
    ERCET_BUS_ALIAS_CONFLICT: _ClassVar[ErcErrorType]
    ERCET_DRIVER_CONFLICT: _ClassVar[ErcErrorType]
    ERCET_BUS_ENTRY_CONFLICT: _ClassVar[ErcErrorType]
    ERCET_BUS_TO_BUS_CONFLICT: _ClassVar[ErcErrorType]
    ERCET_BUS_TO_NET_CONFLICT: _ClassVar[ErcErrorType]
    ERCET_GROUND_PIN_NOT_GROUND: _ClassVar[ErcErrorType]
    ERCET_LABEL_SINGLE_PIN: _ClassVar[ErcErrorType]
    ERCET_UNRESOLVED_VARIABLE: _ClassVar[ErcErrorType]
    ERCET_UNDEFINED_NETCLASS: _ClassVar[ErcErrorType]
    ERCET_SIMULATION_MODEL: _ClassVar[ErcErrorType]
    ERCET_WIRE_DANGLING: _ClassVar[ErcErrorType]
    ERCET_LIB_SYMBOL_ISSUES: _ClassVar[ErcErrorType]
    ERCET_LIB_SYMBOL_MISMATCH: _ClassVar[ErcErrorType]
    ERCET_FOOTPRINT_LINK_ISSUES: _ClassVar[ErcErrorType]
    ERCET_FOOTPRINT_FILTERS: _ClassVar[ErcErrorType]
    ERCET_UNANNOTATED: _ClassVar[ErcErrorType]
    ERCET_EXTRA_UNITS: _ClassVar[ErcErrorType]
    ERCET_DIFFERENT_UNIT_VALUE: _ClassVar[ErcErrorType]
    ERCET_DUPLICATE_REFERENCE: _ClassVar[ErcErrorType]
    ERCET_BUS_ENTRY_NEEDED: _ClassVar[ErcErrorType]
    ERCET_FOUR_WAY_JUNCTION: _ClassVar[ErcErrorType]
    ERCET_LABEL_MULTIPLE_WIRES: _ClassVar[ErcErrorType]
    ERCET_UNCONNECTED_WIRE_ENDPOINT: _ClassVar[ErcErrorType]
    ERCET_STACKED_PIN_SYNTAX: _ClassVar[ErcErrorType]
    ERCET_PIN_MAP_BAD_PAD: _ClassVar[ErcErrorType]
    ERCET_PIN_MAP_UNMAPPED_PIN: _ClassVar[ErcErrorType]
    ERCET_PIN_MAP_DUPLICATE_PAD: _ClassVar[ErcErrorType]
    ERCET_PIN_MAP_STALE_PIN: _ClassVar[ErcErrorType]
    ERCET_EMPTY_LABEL_NAME: _ClassVar[ErcErrorType]
    ERCET_VARIANT_SYMBOL_INVALID: _ClassVar[ErcErrorType]
    ERCET_VARIANT_SYMBOL_INCOMPATIBLE: _ClassVar[ErcErrorType]
    ERCET_DUPLICATE_PIN_ERROR: _ClassVar[ErcErrorType]
    ERCET_PIN_TO_PIN_WARNING: _ClassVar[ErcErrorType]
    ERCET_PIN_TO_PIN_ERROR: _ClassVar[ErcErrorType]
    ERCET_ANNOTATION_ACTION: _ClassVar[ErcErrorType]
    ERCET_GENERIC_WARNING: _ClassVar[ErcErrorType]
    ERCET_GENERIC_ERROR: _ClassVar[ErcErrorType]
    ERCET_FIELD_NAME_WHITESPACE: _ClassVar[ErcErrorType]
    ERCET_WIRED_IMPLICIT_POWER: _ClassVar[ErcErrorType]
    ERCET_EMPTY_POWER_VALUE: _ClassVar[ErcErrorType]
    ERCET_DUPLICATE_SHEET_SUFFIX: _ClassVar[ErcErrorType]
    ERCET_REF_SUFFIX_MISMATCH: _ClassVar[ErcErrorType]
ERCET_UNKNOWN: ErcErrorType
ERCET_DUPLICATE_SHEET_NAME: ErcErrorType
ERCET_ENDPOINT_OFF_GRID: ErcErrorType
ERCET_PIN_NOT_CONNECTED: ErcErrorType
ERCET_PIN_NOT_DRIVEN: ErcErrorType
ERCET_POWERPIN_NOT_DRIVEN: ErcErrorType
ERCET_HIERARCHICAL_LABEL: ErcErrorType
ERCET_NOCONNECT_CONNECTED: ErcErrorType
ERCET_NOCONNECT_NOT_CONNECTED: ErcErrorType
ERCET_LABEL_NOT_CONNECTED: ErcErrorType
ERCET_SIMILAR_LABELS: ErcErrorType
ERCET_SIMILAR_POWER: ErcErrorType
ERCET_SIMILAR_LABEL_AND_POWER: ErcErrorType
ERCET_SINGLE_GLOBAL_LABEL: ErcErrorType
ERCET_SAME_LOCAL_GLOBAL_LABEL: ErcErrorType
ERCET_SAME_LOCAL_GLOBAL_POWER: ErcErrorType
ERCET_DIFFERENT_UNIT_FP: ErcErrorType
ERCET_MISSING_POWER_INPUT_PIN: ErcErrorType
ERCET_MISSING_INPUT_PIN: ErcErrorType
ERCET_MISSING_BIDI_PIN: ErcErrorType
ERCET_MISSING_UNIT: ErcErrorType
ERCET_DIFFERENT_UNIT_NET: ErcErrorType
ERCET_BUS_ALIAS_CONFLICT: ErcErrorType
ERCET_DRIVER_CONFLICT: ErcErrorType
ERCET_BUS_ENTRY_CONFLICT: ErcErrorType
ERCET_BUS_TO_BUS_CONFLICT: ErcErrorType
ERCET_BUS_TO_NET_CONFLICT: ErcErrorType
ERCET_GROUND_PIN_NOT_GROUND: ErcErrorType
ERCET_LABEL_SINGLE_PIN: ErcErrorType
ERCET_UNRESOLVED_VARIABLE: ErcErrorType
ERCET_UNDEFINED_NETCLASS: ErcErrorType
ERCET_SIMULATION_MODEL: ErcErrorType
ERCET_WIRE_DANGLING: ErcErrorType
ERCET_LIB_SYMBOL_ISSUES: ErcErrorType
ERCET_LIB_SYMBOL_MISMATCH: ErcErrorType
ERCET_FOOTPRINT_LINK_ISSUES: ErcErrorType
ERCET_FOOTPRINT_FILTERS: ErcErrorType
ERCET_UNANNOTATED: ErcErrorType
ERCET_EXTRA_UNITS: ErcErrorType
ERCET_DIFFERENT_UNIT_VALUE: ErcErrorType
ERCET_DUPLICATE_REFERENCE: ErcErrorType
ERCET_BUS_ENTRY_NEEDED: ErcErrorType
ERCET_FOUR_WAY_JUNCTION: ErcErrorType
ERCET_LABEL_MULTIPLE_WIRES: ErcErrorType
ERCET_UNCONNECTED_WIRE_ENDPOINT: ErcErrorType
ERCET_STACKED_PIN_SYNTAX: ErcErrorType
ERCET_PIN_MAP_BAD_PAD: ErcErrorType
ERCET_PIN_MAP_UNMAPPED_PIN: ErcErrorType
ERCET_PIN_MAP_DUPLICATE_PAD: ErcErrorType
ERCET_PIN_MAP_STALE_PIN: ErcErrorType
ERCET_EMPTY_LABEL_NAME: ErcErrorType
ERCET_VARIANT_SYMBOL_INVALID: ErcErrorType
ERCET_VARIANT_SYMBOL_INCOMPATIBLE: ErcErrorType
ERCET_DUPLICATE_PIN_ERROR: ErcErrorType
ERCET_PIN_TO_PIN_WARNING: ErcErrorType
ERCET_PIN_TO_PIN_ERROR: ErcErrorType
ERCET_ANNOTATION_ACTION: ErcErrorType
ERCET_GENERIC_WARNING: ErcErrorType
ERCET_GENERIC_ERROR: ErcErrorType
ERCET_FIELD_NAME_WHITESPACE: ErcErrorType
ERCET_WIRED_IMPLICIT_POWER: ErcErrorType
ERCET_EMPTY_POWER_VALUE: ErcErrorType
ERCET_DUPLICATE_SHEET_SUFFIX: ErcErrorType
ERCET_REF_SUFFIX_MISMATCH: ErcErrorType

class ErcSymbolChildReference(_message.Message):
    __slots__ = ("text_value",)
    TEXT_VALUE_FIELD_NUMBER: _ClassVar[int]
    text_value: str
    def __init__(self, text_value: _Optional[str] = ...) -> None: ...

class ErcMarker(_message.Message):
    __slots__ = ("error_type", "position", "items", "sheet_specific_path", "main_item_sheet_path", "aux_item_sheet_path", "child", "description", "severity", "excluded")
    ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    SHEET_SPECIFIC_PATH_FIELD_NUMBER: _ClassVar[int]
    MAIN_ITEM_SHEET_PATH_FIELD_NUMBER: _ClassVar[int]
    AUX_ITEM_SHEET_PATH_FIELD_NUMBER: _ClassVar[int]
    CHILD_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_FIELD_NUMBER: _ClassVar[int]
    error_type: ErcErrorType
    position: _base_types_pb2.Vector2
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    sheet_specific_path: _base_types_pb2.SheetPath
    main_item_sheet_path: _base_types_pb2.SheetPath
    aux_item_sheet_path: _base_types_pb2.SheetPath
    child: ErcSymbolChildReference
    description: str
    severity: _base_types_pb2.RuleSeverity
    excluded: bool
    def __init__(self, error_type: _Optional[_Union[ErcErrorType, str]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., sheet_specific_path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ..., main_item_sheet_path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ..., aux_item_sheet_path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ..., child: _Optional[_Union[ErcSymbolChildReference, _Mapping]] = ..., description: _Optional[str] = ..., severity: _Optional[_Union[_base_types_pb2.RuleSeverity, str]] = ..., excluded: bool = ...) -> None: ...

class ErcSeveritySetting(_message.Message):
    __slots__ = ("rule_type", "severity")
    RULE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    rule_type: ErcErrorType
    severity: _base_types_pb2.RuleSeverity
    def __init__(self, rule_type: _Optional[_Union[ErcErrorType, str]] = ..., severity: _Optional[_Union[_base_types_pb2.RuleSeverity, str]] = ...) -> None: ...

class ErcExclusion(_message.Message):
    __slots__ = ("marker", "comment")
    MARKER_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    marker: ErcMarker
    comment: str
    def __init__(self, marker: _Optional[_Union[ErcMarker, _Mapping]] = ..., comment: _Optional[str] = ...) -> None: ...
