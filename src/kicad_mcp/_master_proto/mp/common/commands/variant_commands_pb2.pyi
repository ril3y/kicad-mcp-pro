from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import variants_pb2 as _variants_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetVariants(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class VariantsResponse(_message.Message):
    __slots__ = ("document", "variants")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    VARIANTS_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    variants: _containers.RepeatedCompositeFieldContainer[_variants_pb2.DesignVariant]
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., variants: _Optional[_Iterable[_Union[_variants_pb2.DesignVariant, _Mapping]]] = ...) -> None: ...

class AddVariant(_message.Message):
    __slots__ = ("document", "name", "description")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    name: str
    description: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class DeleteVariant(_message.Message):
    __slots__ = ("document", "name")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    name: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class RenameVariant(_message.Message):
    __slots__ = ("document", "old_name", "new_name")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    OLD_NAME_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    old_name: str
    new_name: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., old_name: _Optional[str] = ..., new_name: _Optional[str] = ...) -> None: ...

class SetVariantDescription(_message.Message):
    __slots__ = ("document", "name", "description")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    name: str
    description: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CopyVariant(_message.Message):
    __slots__ = ("document", "old_name", "new_name", "new_description")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    OLD_NAME_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    NEW_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    old_name: str
    new_name: str
    new_description: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., old_name: _Optional[str] = ..., new_name: _Optional[str] = ..., new_description: _Optional[str] = ...) -> None: ...

class SetCurrentVariant(_message.Message):
    __slots__ = ("document", "name")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    name: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class GetCurrentVariant(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class CurrentVariantResponse(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
