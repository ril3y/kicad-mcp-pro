from mp.common.types import base_types_pb2 as _base_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JS_UNSPECIFIED: _ClassVar[JobStatus]
    JS_SUCCESS: _ClassVar[JobStatus]
    JS_WARNING: _ClassVar[JobStatus]
    JS_ERROR: _ClassVar[JobStatus]
JS_UNSPECIFIED: JobStatus
JS_SUCCESS: JobStatus
JS_WARNING: JobStatus
JS_ERROR: JobStatus

class RunJobResponse(_message.Message):
    __slots__ = ("status", "output_path", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PATH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: JobStatus
    output_path: _containers.RepeatedScalarFieldContainer[str]
    message: str
    def __init__(self, status: _Optional[_Union[JobStatus, str]] = ..., output_path: _Optional[_Iterable[str]] = ..., message: _Optional[str] = ...) -> None: ...

class RunJobSettings(_message.Message):
    __slots__ = ("document", "output_path")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PATH_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    output_path: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., output_path: _Optional[str] = ...) -> None: ...
