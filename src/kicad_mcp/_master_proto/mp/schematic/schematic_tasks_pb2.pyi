from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.schematic import schematic_rules_pb2 as _schematic_rules_pb2
from mp.common import tasks_pb2 as _tasks_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartErcTask(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class GetErcTaskResult(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: _tasks_pb2.TaskToken
    def __init__(self, token: _Optional[_Union[_tasks_pb2.TaskToken, _Mapping]] = ...) -> None: ...

class ErcTaskResult(_message.Message):
    __slots__ = ("violations", "ignored_count", "excluded_count")
    VIOLATIONS_FIELD_NUMBER: _ClassVar[int]
    IGNORED_COUNT_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_COUNT_FIELD_NUMBER: _ClassVar[int]
    violations: _containers.RepeatedCompositeFieldContainer[_schematic_rules_pb2.ErcMarker]
    ignored_count: int
    excluded_count: int
    def __init__(self, violations: _Optional[_Iterable[_Union[_schematic_rules_pb2.ErcMarker, _Mapping]]] = ..., ignored_count: _Optional[int] = ..., excluded_count: _Optional[int] = ...) -> None: ...
