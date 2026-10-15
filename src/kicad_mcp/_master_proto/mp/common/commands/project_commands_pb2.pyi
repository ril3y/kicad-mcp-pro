from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import project_settings_pb2 as _project_settings_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetNetClasses(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NetClassesResponse(_message.Message):
    __slots__ = ("net_classes",)
    NET_CLASSES_FIELD_NUMBER: _ClassVar[int]
    net_classes: _containers.RepeatedCompositeFieldContainer[_project_settings_pb2.NetClass]
    def __init__(self, net_classes: _Optional[_Iterable[_Union[_project_settings_pb2.NetClass, _Mapping]]] = ...) -> None: ...

class SetNetClasses(_message.Message):
    __slots__ = ("net_classes", "merge_mode")
    NET_CLASSES_FIELD_NUMBER: _ClassVar[int]
    MERGE_MODE_FIELD_NUMBER: _ClassVar[int]
    net_classes: _containers.RepeatedCompositeFieldContainer[_project_settings_pb2.NetClass]
    merge_mode: _base_types_pb2.MapMergeMode
    def __init__(self, net_classes: _Optional[_Iterable[_Union[_project_settings_pb2.NetClass, _Mapping]]] = ..., merge_mode: _Optional[_Union[_base_types_pb2.MapMergeMode, str]] = ...) -> None: ...

class ExpandTextVariables(_message.Message):
    __slots__ = ("document", "text")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    text: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., text: _Optional[_Iterable[str]] = ...) -> None: ...

class ExpandTextVariablesResponse(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, text: _Optional[_Iterable[str]] = ...) -> None: ...

class GetTextVariables(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SetTextVariables(_message.Message):
    __slots__ = ("document", "variables", "merge_mode")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    MERGE_MODE_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    variables: _project_settings_pb2.TextVariables
    merge_mode: _base_types_pb2.MapMergeMode
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., variables: _Optional[_Union[_project_settings_pb2.TextVariables, _Mapping]] = ..., merge_mode: _Optional[_Union[_base_types_pb2.MapMergeMode, str]] = ...) -> None: ...

class OpenDocument(_message.Message):
    __slots__ = ("type", "path")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    type: _base_types_pb2.DocumentType
    path: str
    def __init__(self, type: _Optional[_Union[_base_types_pb2.DocumentType, str]] = ..., path: _Optional[str] = ...) -> None: ...

class OpenDocumentResponse(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class CloseDocument(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SaveDocument(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...
