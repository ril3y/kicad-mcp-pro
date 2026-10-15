from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import enums_pb2 as _enums_pb2
from mp.schematic import schematic_types_pb2 as _schematic_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetSchematicHierarchy(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SchematicHierarchyResponse(_message.Message):
    __slots__ = ("document", "top_level_sheets")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    TOP_LEVEL_SHEETS_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    top_level_sheets: _containers.RepeatedCompositeFieldContainer[_schematic_types_pb2.SheetInstance]
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., top_level_sheets: _Optional[_Iterable[_Union[_schematic_types_pb2.SheetInstance, _Mapping]]] = ...) -> None: ...

class GetSchematicNetlist(_message.Message):
    __slots__ = ("document", "types")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    types: _containers.RepeatedScalarFieldContainer[_enums_pb2.KiCadObjectType]
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., types: _Optional[_Iterable[_Union[_enums_pb2.KiCadObjectType, str]]] = ...) -> None: ...

class SchematicNetlistResponse(_message.Message):
    __slots__ = ("document", "nets")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    NETS_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    nets: _containers.RepeatedCompositeFieldContainer[_schematic_types_pb2.SchematicNet]
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., nets: _Optional[_Iterable[_Union[_schematic_types_pb2.SchematicNet, _Mapping]]] = ...) -> None: ...

class GetLibrarySymbol(_message.Message):
    __slots__ = ("document", "id")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    id: _base_types_pb2.LibraryIdentifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., id: _Optional[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]] = ...) -> None: ...

class GetLibrarySymbolResponse(_message.Message):
    __slots__ = ("symbol",)
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    symbol: _schematic_types_pb2.SchematicSymbol
    def __init__(self, symbol: _Optional[_Union[_schematic_types_pb2.SchematicSymbol, _Mapping]] = ...) -> None: ...

class SymbolLibraryInfo(_message.Message):
    __slots__ = ("nickname", "uri", "description", "enabled", "type")
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    nickname: str
    uri: str
    description: str
    enabled: bool
    type: str
    def __init__(self, nickname: _Optional[str] = ..., uri: _Optional[str] = ..., description: _Optional[str] = ..., enabled: bool = ..., type: _Optional[str] = ...) -> None: ...

class ListSymbolLibraries(_message.Message):
    __slots__ = ("document", "include_disabled")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISABLED_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    include_disabled: bool
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., include_disabled: bool = ...) -> None: ...

class ListSymbolLibrariesResponse(_message.Message):
    __slots__ = ("libraries",)
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    libraries: _containers.RepeatedCompositeFieldContainer[SymbolLibraryInfo]
    def __init__(self, libraries: _Optional[_Iterable[_Union[SymbolLibraryInfo, _Mapping]]] = ...) -> None: ...

class LibrarySymbolMatch(_message.Message):
    __slots__ = ("id", "description", "keywords")
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.LibraryIdentifier
    description: str
    keywords: str
    def __init__(self, id: _Optional[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]] = ..., description: _Optional[str] = ..., keywords: _Optional[str] = ...) -> None: ...

class SearchLibrarySymbols(_message.Message):
    __slots__ = ("document", "query", "library_nicknames", "max_results")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    LIBRARY_NICKNAMES_FIELD_NUMBER: _ClassVar[int]
    MAX_RESULTS_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    query: str
    library_nicknames: _containers.RepeatedScalarFieldContainer[str]
    max_results: int
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., query: _Optional[str] = ..., library_nicknames: _Optional[_Iterable[str]] = ..., max_results: _Optional[int] = ...) -> None: ...

class SearchLibrarySymbolsResponse(_message.Message):
    __slots__ = ("matches",)
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[LibrarySymbolMatch]
    def __init__(self, matches: _Optional[_Iterable[_Union[LibrarySymbolMatch, _Mapping]]] = ...) -> None: ...

class PlaceLibrarySymbol(_message.Message):
    __slots__ = ("document", "id", "position", "reference", "value", "unit", "orientation", "mirror_x", "mirror_y")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    MIRROR_X_FIELD_NUMBER: _ClassVar[int]
    MIRROR_Y_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    id: _base_types_pb2.LibraryIdentifier
    position: _base_types_pb2.Vector2
    reference: str
    value: str
    unit: int
    orientation: _schematic_types_pb2.SchematicSymbolOrientation
    mirror_x: bool
    mirror_y: bool
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., id: _Optional[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., reference: _Optional[str] = ..., value: _Optional[str] = ..., unit: _Optional[int] = ..., orientation: _Optional[_Union[_schematic_types_pb2.SchematicSymbolOrientation, str]] = ..., mirror_x: bool = ..., mirror_y: bool = ...) -> None: ...

class PlaceLibrarySymbolResponse(_message.Message):
    __slots__ = ("placed",)
    PLACED_FIELD_NUMBER: _ClassVar[int]
    placed: _schematic_types_pb2.SchematicSymbolInstance
    def __init__(self, placed: _Optional[_Union[_schematic_types_pb2.SchematicSymbolInstance, _Mapping]] = ...) -> None: ...
