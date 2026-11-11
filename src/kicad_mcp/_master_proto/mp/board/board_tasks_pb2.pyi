from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.board import board_rules_pb2 as _board_rules_pb2
from mp.common import tasks_pb2 as _tasks_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartRefillZonesTask(_message.Message):
    __slots__ = ("board", "zones")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    zones: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., zones: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...

class StartDrcTask(_message.Message):
    __slots__ = ("board", "report_all_track_errors", "test_schematic_parity", "require_zones_filled")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    REPORT_ALL_TRACK_ERRORS_FIELD_NUMBER: _ClassVar[int]
    TEST_SCHEMATIC_PARITY_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_ZONES_FILLED_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    report_all_track_errors: bool
    test_schematic_parity: bool
    require_zones_filled: bool
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., report_all_track_errors: bool = ..., test_schematic_parity: bool = ..., require_zones_filled: bool = ...) -> None: ...

class GetDrcTaskResult(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: _tasks_pb2.TaskToken
    def __init__(self, token: _Optional[_Union[_tasks_pb2.TaskToken, _Mapping]] = ...) -> None: ...

class DrcTaskResult(_message.Message):
    __slots__ = ("violations", "ignored_count", "excluded_count")
    VIOLATIONS_FIELD_NUMBER: _ClassVar[int]
    IGNORED_COUNT_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_COUNT_FIELD_NUMBER: _ClassVar[int]
    violations: _containers.RepeatedCompositeFieldContainer[_board_rules_pb2.DrcMarker]
    ignored_count: int
    excluded_count: int
    def __init__(self, violations: _Optional[_Iterable[_Union[_board_rules_pb2.DrcMarker, _Mapping]]] = ..., ignored_count: _Optional[int] = ..., excluded_count: _Optional[int] = ...) -> None: ...
