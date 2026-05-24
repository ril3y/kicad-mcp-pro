from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import enums_pb2 as _enums_pb2
from mp.board import board_types_pb2 as _board_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NetClassType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NCT_UNKNOWN: _ClassVar[NetClassType]
    NCT_EXPLICIT: _ClassVar[NetClassType]
    NCT_IMPLICIT: _ClassVar[NetClassType]
NCT_UNKNOWN: NetClassType
NCT_EXPLICIT: NetClassType
NCT_IMPLICIT: NetClassType

class NetClassBoardSettings(_message.Message):
    __slots__ = ("clearance", "track_width", "diff_pair_track_width", "diff_pair_gap", "diff_pair_via_gap", "via_stack", "microvia_stack", "color", "tuning_profile")
    CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    TRACK_WIDTH_FIELD_NUMBER: _ClassVar[int]
    DIFF_PAIR_TRACK_WIDTH_FIELD_NUMBER: _ClassVar[int]
    DIFF_PAIR_GAP_FIELD_NUMBER: _ClassVar[int]
    DIFF_PAIR_VIA_GAP_FIELD_NUMBER: _ClassVar[int]
    VIA_STACK_FIELD_NUMBER: _ClassVar[int]
    MICROVIA_STACK_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    TUNING_PROFILE_FIELD_NUMBER: _ClassVar[int]
    clearance: _base_types_pb2.Distance
    track_width: _base_types_pb2.Distance
    diff_pair_track_width: _base_types_pb2.Distance
    diff_pair_gap: _base_types_pb2.Distance
    diff_pair_via_gap: _base_types_pb2.Distance
    via_stack: _board_types_pb2.PadStack
    microvia_stack: _board_types_pb2.PadStack
    color: _base_types_pb2.Color
    tuning_profile: str
    def __init__(self, clearance: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., track_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., diff_pair_track_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., diff_pair_gap: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., diff_pair_via_gap: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., via_stack: _Optional[_Union[_board_types_pb2.PadStack, _Mapping]] = ..., microvia_stack: _Optional[_Union[_board_types_pb2.PadStack, _Mapping]] = ..., color: _Optional[_Union[_base_types_pb2.Color, _Mapping]] = ..., tuning_profile: _Optional[str] = ...) -> None: ...

class NetClassSchematicSettings(_message.Message):
    __slots__ = ("wire_width", "bus_width", "color", "line_style")
    WIRE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    BUS_WIDTH_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    LINE_STYLE_FIELD_NUMBER: _ClassVar[int]
    wire_width: _base_types_pb2.Distance
    bus_width: _base_types_pb2.Distance
    color: _base_types_pb2.Color
    line_style: _enums_pb2.StrokeLineStyle
    def __init__(self, wire_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., bus_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., color: _Optional[_Union[_base_types_pb2.Color, _Mapping]] = ..., line_style: _Optional[_Union[_enums_pb2.StrokeLineStyle, str]] = ...) -> None: ...

class NetClass(_message.Message):
    __slots__ = ("name", "priority", "board", "schematic", "type", "constituents")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    BOARD_FIELD_NUMBER: _ClassVar[int]
    SCHEMATIC_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONSTITUENTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    priority: int
    board: NetClassBoardSettings
    schematic: NetClassSchematicSettings
    type: NetClassType
    constituents: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., priority: _Optional[int] = ..., board: _Optional[_Union[NetClassBoardSettings, _Mapping]] = ..., schematic: _Optional[_Union[NetClassSchematicSettings, _Mapping]] = ..., type: _Optional[_Union[NetClassType, str]] = ..., constituents: _Optional[_Iterable[str]] = ...) -> None: ...

class TextVariables(_message.Message):
    __slots__ = ("variables",)
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    variables: _containers.ScalarMap[str, str]
    def __init__(self, variables: _Optional[_Mapping[str, str]] = ...) -> None: ...
