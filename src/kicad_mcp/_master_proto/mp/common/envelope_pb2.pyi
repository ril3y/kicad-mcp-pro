from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AS_UNKNOWN: _ClassVar[ApiStatusCode]
    AS_OK: _ClassVar[ApiStatusCode]
    AS_TIMEOUT: _ClassVar[ApiStatusCode]
    AS_BAD_REQUEST: _ClassVar[ApiStatusCode]
    AS_NOT_READY: _ClassVar[ApiStatusCode]
    AS_UNHANDLED: _ClassVar[ApiStatusCode]
    AS_TOKEN_MISMATCH: _ClassVar[ApiStatusCode]
    AS_BUSY: _ClassVar[ApiStatusCode]
    AS_UNIMPLEMENTED: _ClassVar[ApiStatusCode]
AS_UNKNOWN: ApiStatusCode
AS_OK: ApiStatusCode
AS_TIMEOUT: ApiStatusCode
AS_BAD_REQUEST: ApiStatusCode
AS_NOT_READY: ApiStatusCode
AS_UNHANDLED: ApiStatusCode
AS_TOKEN_MISMATCH: ApiStatusCode
AS_BUSY: ApiStatusCode
AS_UNIMPLEMENTED: ApiStatusCode

class ApiRequestHeader(_message.Message):
    __slots__ = ("kicad_token", "client_name")
    KICAD_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    kicad_token: str
    client_name: str
    def __init__(self, kicad_token: _Optional[str] = ..., client_name: _Optional[str] = ...) -> None: ...

class ApiRequest(_message.Message):
    __slots__ = ("header", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: ApiRequestHeader
    message: _any_pb2.Any
    def __init__(self, header: _Optional[_Union[ApiRequestHeader, _Mapping]] = ..., message: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class ApiResponseHeader(_message.Message):
    __slots__ = ("kicad_token",)
    KICAD_TOKEN_FIELD_NUMBER: _ClassVar[int]
    kicad_token: str
    def __init__(self, kicad_token: _Optional[str] = ...) -> None: ...

class ApiResponse(_message.Message):
    __slots__ = ("header", "status", "message")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: ApiResponseHeader
    status: ApiResponseStatus
    message: _any_pb2.Any
    def __init__(self, header: _Optional[_Union[ApiResponseHeader, _Mapping]] = ..., status: _Optional[_Union[ApiResponseStatus, _Mapping]] = ..., message: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class ApiResponseStatus(_message.Message):
    __slots__ = ("status", "error_message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: ApiStatusCode
    error_message: str
    def __init__(self, status: _Optional[_Union[ApiStatusCode, str]] = ..., error_message: _Optional[str] = ...) -> None: ...
