from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LibraryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LT_UNKNOWN: _ClassVar[LibraryType]
    LT_SYMBOL: _ClassVar[LibraryType]
    LT_FOOTPRINT: _ClassVar[LibraryType]
    LT_DESIGN_BLOCK: _ClassVar[LibraryType]

class LibraryTableScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LTS_UNKNOWN: _ClassVar[LibraryTableScope]
    LTS_GLOBAL: _ClassVar[LibraryTableScope]
    LTS_PROJECT: _ClassVar[LibraryTableScope]
    LTS_BOTH: _ClassVar[LibraryTableScope]

class LibraryLoadStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LLS_UNKNOWN: _ClassVar[LibraryLoadStatus]
    LLS_INVALID: _ClassVar[LibraryLoadStatus]
    LLS_LOADING: _ClassVar[LibraryLoadStatus]
    LLS_LOADED: _ClassVar[LibraryLoadStatus]
    LLS_ERROR: _ClassVar[LibraryLoadStatus]
LT_UNKNOWN: LibraryType
LT_SYMBOL: LibraryType
LT_FOOTPRINT: LibraryType
LT_DESIGN_BLOCK: LibraryType
LTS_UNKNOWN: LibraryTableScope
LTS_GLOBAL: LibraryTableScope
LTS_PROJECT: LibraryTableScope
LTS_BOTH: LibraryTableScope
LLS_UNKNOWN: LibraryLoadStatus
LLS_INVALID: LibraryLoadStatus
LLS_LOADING: LibraryLoadStatus
LLS_LOADED: LibraryLoadStatus
LLS_ERROR: LibraryLoadStatus

class LibraryTableEntry(_message.Message):
    __slots__ = ("nickname", "uri", "type", "scope", "description", "options", "disabled", "hidden", "writable")
    class OptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    WRITABLE_FIELD_NUMBER: _ClassVar[int]
    nickname: str
    uri: str
    type: LibraryType
    scope: LibraryTableScope
    description: str
    options: _containers.ScalarMap[str, str]
    disabled: bool
    hidden: bool
    writable: bool
    def __init__(self, nickname: _Optional[str] = ..., uri: _Optional[str] = ..., type: _Optional[_Union[LibraryType, str]] = ..., scope: _Optional[_Union[LibraryTableScope, str]] = ..., description: _Optional[str] = ..., options: _Optional[_Mapping[str, str]] = ..., disabled: bool = ..., hidden: bool = ..., writable: bool = ...) -> None: ...

class LibraryStatusEntry(_message.Message):
    __slots__ = ("entry", "status", "error_message")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    entry: LibraryTableEntry
    status: LibraryLoadStatus
    error_message: str
    def __init__(self, entry: _Optional[_Union[LibraryTableEntry, _Mapping]] = ..., status: _Optional[_Union[LibraryLoadStatus, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class LibraryTable(_message.Message):
    __slots__ = ("path", "scope", "valid", "error_message")
    PATH_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    path: str
    scope: LibraryTableScope
    valid: bool
    error_message: str
    def __init__(self, path: _Optional[str] = ..., scope: _Optional[_Union[LibraryTableScope, str]] = ..., valid: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class LibraryTableMutationResponse(_message.Message):
    __slots__ = ("table",)
    TABLE_FIELD_NUMBER: _ClassVar[int]
    table: LibraryTable
    def __init__(self, table: _Optional[_Union[LibraryTable, _Mapping]] = ...) -> None: ...

class LibraryCommandStatus(_message.Message):
    __slots__ = ("code", "error_message")
    class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LCS_UNKNOWN: _ClassVar[LibraryCommandStatus.Code]
        LCS_OK: _ClassVar[LibraryCommandStatus.Code]
        LCS_NOT_FOUND: _ClassVar[LibraryCommandStatus.Code]
        LCS_READ_ONLY: _ClassVar[LibraryCommandStatus.Code]
        LCS_ALREADY_EXISTS: _ClassVar[LibraryCommandStatus.Code]
        LCS_ERROR: _ClassVar[LibraryCommandStatus.Code]
    LCS_UNKNOWN: LibraryCommandStatus.Code
    LCS_OK: LibraryCommandStatus.Code
    LCS_NOT_FOUND: LibraryCommandStatus.Code
    LCS_READ_ONLY: LibraryCommandStatus.Code
    LCS_ALREADY_EXISTS: LibraryCommandStatus.Code
    LCS_ERROR: LibraryCommandStatus.Code
    CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: LibraryCommandStatus.Code
    error_message: str
    def __init__(self, code: _Optional[_Union[LibraryCommandStatus.Code, str]] = ..., error_message: _Optional[str] = ...) -> None: ...
