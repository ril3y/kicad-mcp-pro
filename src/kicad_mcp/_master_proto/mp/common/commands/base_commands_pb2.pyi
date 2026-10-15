from mp.common.types import base_types_pb2 as _base_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetVersion(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetVersionResponse(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: _base_types_pb2.KiCadVersion
    def __init__(self, version: _Optional[_Union[_base_types_pb2.KiCadVersion, _Mapping]] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKiCadBinaryPath(_message.Message):
    __slots__ = ("binary_name",)
    BINARY_NAME_FIELD_NUMBER: _ClassVar[int]
    binary_name: str
    def __init__(self, binary_name: _Optional[str] = ...) -> None: ...

class PathResponse(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class GetTextExtents(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: _base_types_pb2.Text
    def __init__(self, text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ...) -> None: ...

class TextOrTextBox(_message.Message):
    __slots__ = ("text", "textbox")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TEXTBOX_FIELD_NUMBER: _ClassVar[int]
    text: _base_types_pb2.Text
    textbox: _base_types_pb2.TextBox
    def __init__(self, text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., textbox: _Optional[_Union[_base_types_pb2.TextBox, _Mapping]] = ...) -> None: ...

class GetTextAsShapes(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedCompositeFieldContainer[TextOrTextBox]
    def __init__(self, text: _Optional[_Iterable[_Union[TextOrTextBox, _Mapping]]] = ...) -> None: ...

class TextWithShapes(_message.Message):
    __slots__ = ("text", "shapes")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SHAPES_FIELD_NUMBER: _ClassVar[int]
    text: TextOrTextBox
    shapes: _base_types_pb2.CompoundShape
    def __init__(self, text: _Optional[_Union[TextOrTextBox, _Mapping]] = ..., shapes: _Optional[_Union[_base_types_pb2.CompoundShape, _Mapping]] = ...) -> None: ...

class GetTextAsShapesResponse(_message.Message):
    __slots__ = ("text_with_shapes",)
    TEXT_WITH_SHAPES_FIELD_NUMBER: _ClassVar[int]
    text_with_shapes: _containers.RepeatedCompositeFieldContainer[TextWithShapes]
    def __init__(self, text_with_shapes: _Optional[_Iterable[_Union[TextWithShapes, _Mapping]]] = ...) -> None: ...

class GetPluginSettingsPath(_message.Message):
    __slots__ = ("identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    def __init__(self, identifier: _Optional[str] = ...) -> None: ...

class StringResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...
