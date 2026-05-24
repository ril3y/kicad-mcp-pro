from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WizardParameterDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WPDT_UNKNOWN: _ClassVar[WizardParameterDataType]
    WPDT_DISTANCE: _ClassVar[WizardParameterDataType]
    WPDT_AREA: _ClassVar[WizardParameterDataType]
    WPDT_VOLUME: _ClassVar[WizardParameterDataType]
    WPDT_TIME: _ClassVar[WizardParameterDataType]
    WPDT_ANGLE: _ClassVar[WizardParameterDataType]
    WPDT_STRING: _ClassVar[WizardParameterDataType]
    WPDT_INTEGER: _ClassVar[WizardParameterDataType]
    WPDT_REAL: _ClassVar[WizardParameterDataType]
    WPDT_BOOL: _ClassVar[WizardParameterDataType]

class WizardParameterCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WPC_UNKNOWN: _ClassVar[WizardParameterCategory]
    WPC_PACKAGE: _ClassVar[WizardParameterCategory]
    WPC_PADS: _ClassVar[WizardParameterCategory]
    WPC_3DMODEL: _ClassVar[WizardParameterCategory]
    WPC_METADATA: _ClassVar[WizardParameterCategory]
    WPC_RULES: _ClassVar[WizardParameterCategory]

class WizardContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WCT_UNKNOWN: _ClassVar[WizardContentType]
    WCT_SYMBOL: _ClassVar[WizardContentType]
    WCT_FOOTPRINT: _ClassVar[WizardContentType]

class WizardGenerationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WGS_UNKNOWN: _ClassVar[WizardGenerationStatus]
    WGS_OK: _ClassVar[WizardGenerationStatus]
    WGS_ERROR: _ClassVar[WizardGenerationStatus]
WPDT_UNKNOWN: WizardParameterDataType
WPDT_DISTANCE: WizardParameterDataType
WPDT_AREA: WizardParameterDataType
WPDT_VOLUME: WizardParameterDataType
WPDT_TIME: WizardParameterDataType
WPDT_ANGLE: WizardParameterDataType
WPDT_STRING: WizardParameterDataType
WPDT_INTEGER: WizardParameterDataType
WPDT_REAL: WizardParameterDataType
WPDT_BOOL: WizardParameterDataType
WPC_UNKNOWN: WizardParameterCategory
WPC_PACKAGE: WizardParameterCategory
WPC_PADS: WizardParameterCategory
WPC_3DMODEL: WizardParameterCategory
WPC_METADATA: WizardParameterCategory
WPC_RULES: WizardParameterCategory
WCT_UNKNOWN: WizardContentType
WCT_SYMBOL: WizardContentType
WCT_FOOTPRINT: WizardContentType
WGS_UNKNOWN: WizardGenerationStatus
WGS_OK: WizardGenerationStatus
WGS_ERROR: WizardGenerationStatus

class WizardIntParameter(_message.Message):
    __slots__ = ("value", "default", "min", "max", "multiple")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    value: int
    default: int
    min: int
    max: int
    multiple: int
    def __init__(self, value: _Optional[int] = ..., default: _Optional[int] = ..., min: _Optional[int] = ..., max: _Optional[int] = ..., multiple: _Optional[int] = ...) -> None: ...

class WizardRealParameter(_message.Message):
    __slots__ = ("value", "default", "min", "max")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    value: float
    default: float
    min: float
    max: float
    def __init__(self, value: _Optional[float] = ..., default: _Optional[float] = ..., min: _Optional[float] = ..., max: _Optional[float] = ...) -> None: ...

class WizardBoolParameter(_message.Message):
    __slots__ = ("value", "default")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    value: bool
    default: bool
    def __init__(self, value: bool = ..., default: bool = ...) -> None: ...

class WizardStringParameter(_message.Message):
    __slots__ = ("value", "default", "validation_regex")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_REGEX_FIELD_NUMBER: _ClassVar[int]
    value: str
    default: str
    validation_regex: str
    def __init__(self, value: _Optional[str] = ..., default: _Optional[str] = ..., validation_regex: _Optional[str] = ...) -> None: ...

class WizardParameterList(_message.Message):
    __slots__ = ("parameters",)
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    parameters: _containers.RepeatedCompositeFieldContainer[WizardParameter]
    def __init__(self, parameters: _Optional[_Iterable[_Union[WizardParameter, _Mapping]]] = ...) -> None: ...

class WizardParameter(_message.Message):
    __slots__ = ("identifier", "name", "description", "category", "type", "int", "real", "bool", "string")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    REAL_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    name: str
    description: str
    category: WizardParameterCategory
    type: WizardParameterDataType
    int: WizardIntParameter
    real: WizardRealParameter
    bool: WizardBoolParameter
    string: WizardStringParameter
    def __init__(self, identifier: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[_Union[WizardParameterCategory, str]] = ..., type: _Optional[_Union[WizardParameterDataType, str]] = ..., int: _Optional[_Union[WizardIntParameter, _Mapping]] = ..., real: _Optional[_Union[WizardRealParameter, _Mapping]] = ..., bool: _Optional[_Union[WizardBoolParameter, _Mapping]] = ..., string: _Optional[_Union[WizardStringParameter, _Mapping]] = ...) -> None: ...

class WizardInfo(_message.Message):
    __slots__ = ("meta", "parameters")
    META_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    meta: WizardMetaInfo
    parameters: _containers.RepeatedCompositeFieldContainer[WizardParameter]
    def __init__(self, meta: _Optional[_Union[WizardMetaInfo, _Mapping]] = ..., parameters: _Optional[_Iterable[_Union[WizardParameter, _Mapping]]] = ...) -> None: ...

class WizardMetaInfo(_message.Message):
    __slots__ = ("identifier", "name", "description", "types_generated")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPES_GENERATED_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    name: str
    description: str
    types_generated: _containers.RepeatedScalarFieldContainer[WizardContentType]
    def __init__(self, identifier: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., types_generated: _Optional[_Iterable[_Union[WizardContentType, str]]] = ...) -> None: ...

class WizardGeneratedContent(_message.Message):
    __slots__ = ("status", "content", "error_message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: WizardGenerationStatus
    content: _any_pb2.Any
    error_message: str
    def __init__(self, status: _Optional[_Union[WizardGenerationStatus, str]] = ..., content: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...
