from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TS_UNKNOWN: _ClassVar[TaskState]
    TS_RUNNING: _ClassVar[TaskState]
    TS_COMPLETED: _ClassVar[TaskState]
    TS_FAILED: _ClassVar[TaskState]
    TS_CANCELLED: _ClassVar[TaskState]
TS_UNKNOWN: TaskState
TS_RUNNING: TaskState
TS_COMPLETED: TaskState
TS_FAILED: TaskState
TS_CANCELLED: TaskState

class TaskToken(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class GetTaskStatus(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: TaskToken
    def __init__(self, token: _Optional[_Union[TaskToken, _Mapping]] = ...) -> None: ...

class TaskStatusResponse(_message.Message):
    __slots__ = ("state", "error_message")
    STATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    state: TaskState
    error_message: str
    def __init__(self, state: _Optional[_Union[TaskState, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class StartTaskResponse(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: TaskToken
    def __init__(self, token: _Optional[_Union[TaskToken, _Mapping]] = ...) -> None: ...
