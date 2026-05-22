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
