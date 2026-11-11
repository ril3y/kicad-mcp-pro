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

class PlaceSymbolFromLibrary(_message.Message):
    __slots__ = ("header", "lib_id", "position", "orientation", "unit", "reference")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LIB_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    lib_id: _base_types_pb2.LibraryIdentifier
    position: _base_types_pb2.Vector2
    orientation: _schematic_types_pb2.SchematicSymbolOrientation
    unit: _schematic_types_pb2.SchematicSymbolUnit
    reference: str
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., lib_id: _Optional[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., orientation: _Optional[_Union[_schematic_types_pb2.SchematicSymbolOrientation, str]] = ..., unit: _Optional[_Union[_schematic_types_pb2.SchematicSymbolUnit, _Mapping]] = ..., reference: _Optional[str] = ...) -> None: ...
