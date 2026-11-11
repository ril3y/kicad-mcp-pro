from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmbeddedFileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EFT_UNKNOWN: _ClassVar[EmbeddedFileType]
    EFT_OTHER: _ClassVar[EmbeddedFileType]
    EFT_FONT: _ClassVar[EmbeddedFileType]
    EFT_MODEL: _ClassVar[EmbeddedFileType]
    EFT_WORKSHEET: _ClassVar[EmbeddedFileType]
    EFT_DATASHEET: _ClassVar[EmbeddedFileType]
EFT_UNKNOWN: EmbeddedFileType
EFT_OTHER: EmbeddedFileType
EFT_FONT: EmbeddedFileType
EFT_MODEL: EmbeddedFileType
EFT_WORKSHEET: EmbeddedFileType
EFT_DATASHEET: EmbeddedFileType

class EmbeddedFile(_message.Message):
    __slots__ = ("name", "type", "data", "data_hash")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_HASH_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: EmbeddedFileType
    data: bytes
    data_hash: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[EmbeddedFileType, str]] = ..., data: _Optional[bytes] = ..., data_hash: _Optional[str] = ...) -> None: ...

class EmbeddedFiles(_message.Message):
    __slots__ = ("files",)
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[EmbeddedFile]
    def __init__(self, files: _Optional[_Iterable[_Union[EmbeddedFile, _Mapping]]] = ...) -> None: ...
