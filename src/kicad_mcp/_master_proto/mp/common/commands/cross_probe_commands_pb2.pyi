from mp.common.types import base_types_pb2 as _base_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CrossProbeStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CPS_UNSPECIFIED: _ClassVar[CrossProbeStatus]
    CPS_OK: _ClassVar[CrossProbeStatus]
    CPS_NOT_FOUND: _ClassVar[CrossProbeStatus]
    CPS_INVALID: _ClassVar[CrossProbeStatus]
    CPS_DISABLED: _ClassVar[CrossProbeStatus]

class SyncSelectionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SSM_UNKNOWN: _ClassVar[SyncSelectionMode]
    SSM_ITEMS_ONLY: _ClassVar[SyncSelectionMode]
    SSM_ITEMS_AND_NETS: _ClassVar[SyncSelectionMode]

class SyncSelectionContext(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SSC_UNKNOWN: _ClassVar[SyncSelectionContext]
    SSC_IMPLICIT: _ClassVar[SyncSelectionContext]
    SSC_EXPLICIT: _ClassVar[SyncSelectionContext]
CPS_UNSPECIFIED: CrossProbeStatus
CPS_OK: CrossProbeStatus
CPS_NOT_FOUND: CrossProbeStatus
CPS_INVALID: CrossProbeStatus
CPS_DISABLED: CrossProbeStatus
SSM_UNKNOWN: SyncSelectionMode
SSM_ITEMS_ONLY: SyncSelectionMode
SSM_ITEMS_AND_NETS: SyncSelectionMode
SSC_UNKNOWN: SyncSelectionContext
SSC_IMPLICIT: SyncSelectionContext
SSC_EXPLICIT: SyncSelectionContext

class CrossProbeAnnounce(_message.Message):
    __slots__ = ("frame_type", "socket_path", "api_token")
    FRAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOCKET_PATH_FIELD_NUMBER: _ClassVar[int]
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    frame_type: _base_types_pb2.FrameType
    socket_path: str
    api_token: str
    def __init__(self, frame_type: _Optional[_Union[_base_types_pb2.FrameType, str]] = ..., socket_path: _Optional[str] = ..., api_token: _Optional[str] = ...) -> None: ...

class CrossProbeAnnounceResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: CrossProbeStatus
    message: str
    def __init__(self, status: _Optional[_Union[CrossProbeStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class FootprintSelectionSpec(_message.Message):
    __slots__ = ("reference",)
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    reference: str
    def __init__(self, reference: _Optional[str] = ...) -> None: ...

class PadSelectionSpec(_message.Message):
    __slots__ = ("reference", "number")
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    reference: str
    number: str
    def __init__(self, reference: _Optional[str] = ..., number: _Optional[str] = ...) -> None: ...

class SelectionSpec(_message.Message):
    __slots__ = ("footprint", "pad", "sheet_path")
    FOOTPRINT_FIELD_NUMBER: _ClassVar[int]
    PAD_FIELD_NUMBER: _ClassVar[int]
    SHEET_PATH_FIELD_NUMBER: _ClassVar[int]
    footprint: FootprintSelectionSpec
    pad: PadSelectionSpec
    sheet_path: _base_types_pb2.SheetPath
    def __init__(self, footprint: _Optional[_Union[FootprintSelectionSpec, _Mapping]] = ..., pad: _Optional[_Union[PadSelectionSpec, _Mapping]] = ..., sheet_path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ...) -> None: ...

class SyncSelection(_message.Message):
    __slots__ = ("context", "mode", "focus_item", "items")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FOCUS_ITEM_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    context: SyncSelectionContext
    mode: SyncSelectionMode
    focus_item: SelectionSpec
    items: _containers.RepeatedCompositeFieldContainer[SelectionSpec]
    def __init__(self, context: _Optional[_Union[SyncSelectionContext, str]] = ..., mode: _Optional[_Union[SyncSelectionMode, str]] = ..., focus_item: _Optional[_Union[SelectionSpec, _Mapping]] = ..., items: _Optional[_Iterable[_Union[SelectionSpec, _Mapping]]] = ...) -> None: ...

class SyncSelectionResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: CrossProbeStatus
    message: str
    def __init__(self, status: _Optional[_Union[CrossProbeStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class HighlightNets(_message.Message):
    __slots__ = ("net_name",)
    NET_NAME_FIELD_NUMBER: _ClassVar[int]
    net_name: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, net_name: _Optional[_Iterable[str]] = ...) -> None: ...

class HighlightNetsResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: CrossProbeStatus
    message: str
    def __init__(self, status: _Optional[_Union[CrossProbeStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class FocusOnItem(_message.Message):
    __slots__ = ("focus_item",)
    FOCUS_ITEM_FIELD_NUMBER: _ClassVar[int]
    focus_item: SelectionSpec
    def __init__(self, focus_item: _Optional[_Union[SelectionSpec, _Mapping]] = ...) -> None: ...

class FocusOnItemResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: CrossProbeStatus
    message: str
    def __init__(self, status: _Optional[_Union[CrossProbeStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...
