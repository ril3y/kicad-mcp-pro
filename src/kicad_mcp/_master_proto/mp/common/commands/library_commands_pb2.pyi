from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import library_types_pb2 as _library_types_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLibraryTable(_message.Message):
    __slots__ = ("type", "scope", "substituted")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    SUBSTITUTED_FIELD_NUMBER: _ClassVar[int]
    type: _library_types_pb2.LibraryType
    scope: _library_types_pb2.LibraryTableScope
    substituted: bool
    def __init__(self, type: _Optional[_Union[_library_types_pb2.LibraryType, str]] = ..., scope: _Optional[_Union[_library_types_pb2.LibraryTableScope, str]] = ..., substituted: bool = ...) -> None: ...

class LibraryTableResponse(_message.Message):
    __slots__ = ("table", "rows")
    TABLE_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    table: _library_types_pb2.LibraryTable
    rows: _containers.RepeatedCompositeFieldContainer[_library_types_pb2.LibraryTableEntry]
    def __init__(self, table: _Optional[_Union[_library_types_pb2.LibraryTable, _Mapping]] = ..., rows: _Optional[_Iterable[_Union[_library_types_pb2.LibraryTableEntry, _Mapping]]] = ...) -> None: ...

class AddLibraryTableEntry(_message.Message):
    __slots__ = ("entry", "scope")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    entry: _library_types_pb2.LibraryTableEntry
    scope: _library_types_pb2.LibraryTableScope
    def __init__(self, entry: _Optional[_Union[_library_types_pb2.LibraryTableEntry, _Mapping]] = ..., scope: _Optional[_Union[_library_types_pb2.LibraryTableScope, str]] = ...) -> None: ...

class UpdateLibraryTableEntry(_message.Message):
    __slots__ = ("entry", "scope")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    entry: _library_types_pb2.LibraryTableEntry
    scope: _library_types_pb2.LibraryTableScope
    def __init__(self, entry: _Optional[_Union[_library_types_pb2.LibraryTableEntry, _Mapping]] = ..., scope: _Optional[_Union[_library_types_pb2.LibraryTableScope, str]] = ...) -> None: ...

class DeleteLibraryTableEntry(_message.Message):
    __slots__ = ("type", "nickname", "scope")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    type: _library_types_pb2.LibraryType
    nickname: str
    scope: _library_types_pb2.LibraryTableScope
    def __init__(self, type: _Optional[_Union[_library_types_pb2.LibraryType, str]] = ..., nickname: _Optional[str] = ..., scope: _Optional[_Union[_library_types_pb2.LibraryTableScope, str]] = ...) -> None: ...

class GetLibraryStatuses(_message.Message):
    __slots__ = ("types", "scope")
    TYPES_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    types: _containers.RepeatedScalarFieldContainer[_library_types_pb2.LibraryType]
    scope: _library_types_pb2.LibraryTableScope
    def __init__(self, types: _Optional[_Iterable[_Union[_library_types_pb2.LibraryType, str]]] = ..., scope: _Optional[_Union[_library_types_pb2.LibraryTableScope, str]] = ...) -> None: ...

class LibraryStatusResponse(_message.Message):
    __slots__ = ("libraries",)
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    libraries: _containers.RepeatedCompositeFieldContainer[_library_types_pb2.LibraryStatusEntry]
    def __init__(self, libraries: _Optional[_Iterable[_Union[_library_types_pb2.LibraryStatusEntry, _Mapping]]] = ...) -> None: ...

class ReloadLibrary(_message.Message):
    __slots__ = ("type", "scope", "nickname")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    type: _library_types_pb2.LibraryType
    scope: _library_types_pb2.LibraryTableScope
    nickname: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, type: _Optional[_Union[_library_types_pb2.LibraryType, str]] = ..., scope: _Optional[_Union[_library_types_pb2.LibraryTableScope, str]] = ..., nickname: _Optional[_Iterable[str]] = ...) -> None: ...

class LoadAllLibraries(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: _containers.RepeatedScalarFieldContainer[_library_types_pb2.LibraryType]
    def __init__(self, type: _Optional[_Iterable[_Union[_library_types_pb2.LibraryType, str]]] = ...) -> None: ...

class GetLibraryItems(_message.Message):
    __slots__ = ("type", "nickname")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    type: _library_types_pb2.LibraryType
    nickname: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, type: _Optional[_Union[_library_types_pb2.LibraryType, str]] = ..., nickname: _Optional[_Iterable[str]] = ...) -> None: ...

class LibraryItemsResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.LibraryIdentifier]
    def __init__(self, items: _Optional[_Iterable[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]]] = ...) -> None: ...

class GetItemsFromLibrary(_message.Message):
    __slots__ = ("type", "document", "item_ids")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    type: _library_types_pb2.LibraryType
    document: _base_types_pb2.DocumentSpecifier
    item_ids: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.LibraryIdentifier]
    def __init__(self, type: _Optional[_Union[_library_types_pb2.LibraryType, str]] = ..., document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., item_ids: _Optional[_Iterable[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]]] = ...) -> None: ...

class SearchLibraries(_message.Message):
    __slots__ = ("type", "query")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    type: _library_types_pb2.LibraryType
    query: str
    def __init__(self, type: _Optional[_Union[_library_types_pb2.LibraryType, str]] = ..., query: _Optional[str] = ...) -> None: ...

class SearchLibrariesResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.LibraryIdentifier]
    def __init__(self, items: _Optional[_Iterable[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]]] = ...) -> None: ...

class PlaceFromLibraryResponse(_message.Message):
    __slots__ = ("header", "item")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    item: _any_pb2.Any
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., item: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
