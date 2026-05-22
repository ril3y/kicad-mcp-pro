from google.protobuf import any_pb2 as _any_pb2
from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import enums_pb2 as _enums_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RunActionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RAS_UNKNOWN: _ClassVar[RunActionStatus]
    RAS_OK: _ClassVar[RunActionStatus]
    RAS_INVALID: _ClassVar[RunActionStatus]
    RAS_FRAME_NOT_OPEN: _ClassVar[RunActionStatus]

class CommitAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CMA_UNKNOWN: _ClassVar[CommitAction]
    CMA_COMMIT: _ClassVar[CommitAction]
    CMA_DROP: _ClassVar[CommitAction]

class ItemStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ISC_UNKNOWN: _ClassVar[ItemStatusCode]
    ISC_OK: _ClassVar[ItemStatusCode]
    ISC_INVALID_TYPE: _ClassVar[ItemStatusCode]
    ISC_EXISTING: _ClassVar[ItemStatusCode]
    ISC_NONEXISTENT: _ClassVar[ItemStatusCode]
    ISC_IMMUTABLE: _ClassVar[ItemStatusCode]
    ISC_INVALID_DATA: _ClassVar[ItemStatusCode]

class ItemDeletionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IDS_UNKNOWN: _ClassVar[ItemDeletionStatus]
    IDS_OK: _ClassVar[ItemDeletionStatus]
    IDS_NONEXISTENT: _ClassVar[ItemDeletionStatus]
    IDS_IMMUTABLE: _ClassVar[ItemDeletionStatus]

class BoundingBoxMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BBM_UNKNOWN: _ClassVar[BoundingBoxMode]
    BBM_ITEM_ONLY: _ClassVar[BoundingBoxMode]
    BBM_ITEM_AND_CHILD_TEXT: _ClassVar[BoundingBoxMode]

class HitTestResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HTR_UNKNOWN: _ClassVar[HitTestResult]
    HTR_NO_HIT: _ClassVar[HitTestResult]
    HTR_HIT: _ClassVar[HitTestResult]
RAS_UNKNOWN: RunActionStatus
RAS_OK: RunActionStatus
RAS_INVALID: RunActionStatus
RAS_FRAME_NOT_OPEN: RunActionStatus
CMA_UNKNOWN: CommitAction
CMA_COMMIT: CommitAction
CMA_DROP: CommitAction
ISC_UNKNOWN: ItemStatusCode
ISC_OK: ItemStatusCode
ISC_INVALID_TYPE: ItemStatusCode
ISC_EXISTING: ItemStatusCode
ISC_NONEXISTENT: ItemStatusCode
ISC_IMMUTABLE: ItemStatusCode
ISC_INVALID_DATA: ItemStatusCode
IDS_UNKNOWN: ItemDeletionStatus
IDS_OK: ItemDeletionStatus
IDS_NONEXISTENT: ItemDeletionStatus
IDS_IMMUTABLE: ItemDeletionStatus
BBM_UNKNOWN: BoundingBoxMode
BBM_ITEM_ONLY: BoundingBoxMode
BBM_ITEM_AND_CHILD_TEXT: BoundingBoxMode
HTR_UNKNOWN: HitTestResult
HTR_NO_HIT: HitTestResult
HTR_HIT: HitTestResult

class RefreshEditor(_message.Message):
    __slots__ = ("frame",)
    FRAME_FIELD_NUMBER: _ClassVar[int]
    frame: _base_types_pb2.FrameType
    def __init__(self, frame: _Optional[_Union[_base_types_pb2.FrameType, str]] = ...) -> None: ...

class GetOpenDocuments(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: _base_types_pb2.DocumentType
    def __init__(self, type: _Optional[_Union[_base_types_pb2.DocumentType, str]] = ...) -> None: ...

class GetOpenDocumentsResponse(_message.Message):
    __slots__ = ("documents",)
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    documents: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.DocumentSpecifier]
    def __init__(self, documents: _Optional[_Iterable[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]]] = ...) -> None: ...

class SaveOptions(_message.Message):
    __slots__ = ("overwrite", "include_project")
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PROJECT_FIELD_NUMBER: _ClassVar[int]
    overwrite: bool
    include_project: bool
    def __init__(self, overwrite: bool = ..., include_project: bool = ...) -> None: ...

class SaveCopyOfDocument(_message.Message):
    __slots__ = ("document", "path", "options")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    path: str
    options: SaveOptions
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., path: _Optional[str] = ..., options: _Optional[_Union[SaveOptions, _Mapping]] = ...) -> None: ...

class RevertDocument(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class RunAction(_message.Message):
    __slots__ = ("action",)
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: str
    def __init__(self, action: _Optional[str] = ...) -> None: ...

class RunActionResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: RunActionStatus
    def __init__(self, status: _Optional[_Union[RunActionStatus, str]] = ...) -> None: ...

class BeginCommit(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ...) -> None: ...

class BeginCommitResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ...) -> None: ...

class EndCommit(_message.Message):
    __slots__ = ("id", "action", "message", "header")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    action: CommitAction
    message: str
    header: _base_types_pb2.ItemHeader
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., action: _Optional[_Union[CommitAction, str]] = ..., message: _Optional[str] = ..., header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ...) -> None: ...

class EndCommitResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateItems(_message.Message):
    __slots__ = ("header", "items", "container")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    items: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    container: _base_types_pb2.KIID
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ..., container: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ...) -> None: ...

class ItemStatus(_message.Message):
    __slots__ = ("code", "error_message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: ItemStatusCode
    error_message: str
    def __init__(self, code: _Optional[_Union[ItemStatusCode, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class ItemCreationResult(_message.Message):
    __slots__ = ("status", "item")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    status: ItemStatus
    item: _any_pb2.Any
    def __init__(self, status: _Optional[_Union[ItemStatus, _Mapping]] = ..., item: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class CreateItemsResponse(_message.Message):
    __slots__ = ("header", "status", "created_items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    status: _base_types_pb2.ItemRequestStatus
    created_items: _containers.RepeatedCompositeFieldContainer[ItemCreationResult]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., status: _Optional[_Union[_base_types_pb2.ItemRequestStatus, str]] = ..., created_items: _Optional[_Iterable[_Union[ItemCreationResult, _Mapping]]] = ...) -> None: ...

class GetItems(_message.Message):
    __slots__ = ("header", "types")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    types: _containers.RepeatedScalarFieldContainer[_enums_pb2.KiCadObjectType]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., types: _Optional[_Iterable[_Union[_enums_pb2.KiCadObjectType, str]]] = ...) -> None: ...

class GetItemsById(_message.Message):
    __slots__ = ("header", "items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...

class GetItemsResponse(_message.Message):
    __slots__ = ("header", "status", "items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    status: _base_types_pb2.ItemRequestStatus
    items: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., status: _Optional[_Union[_base_types_pb2.ItemRequestStatus, str]] = ..., items: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class UpdateItems(_message.Message):
    __slots__ = ("header", "items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    items: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class ItemUpdateResult(_message.Message):
    __slots__ = ("status", "item")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    status: ItemStatus
    item: _any_pb2.Any
    def __init__(self, status: _Optional[_Union[ItemStatus, _Mapping]] = ..., item: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class UpdateItemsResponse(_message.Message):
    __slots__ = ("header", "status", "updated_items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    status: _base_types_pb2.ItemRequestStatus
    updated_items: _containers.RepeatedCompositeFieldContainer[ItemUpdateResult]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., status: _Optional[_Union[_base_types_pb2.ItemRequestStatus, str]] = ..., updated_items: _Optional[_Iterable[_Union[ItemUpdateResult, _Mapping]]] = ...) -> None: ...

class DeleteItems(_message.Message):
    __slots__ = ("header", "item_ids")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    item_ids: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., item_ids: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...

class ItemDeletionResult(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    status: ItemDeletionStatus
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., status: _Optional[_Union[ItemDeletionStatus, str]] = ...) -> None: ...

class DeleteItemsResponse(_message.Message):
    __slots__ = ("header", "status", "deleted_items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DELETED_ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    status: _base_types_pb2.ItemRequestStatus
    deleted_items: _containers.RepeatedCompositeFieldContainer[ItemDeletionResult]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., status: _Optional[_Union[_base_types_pb2.ItemRequestStatus, str]] = ..., deleted_items: _Optional[_Iterable[_Union[ItemDeletionResult, _Mapping]]] = ...) -> None: ...

class GetBoundingBox(_message.Message):
    __slots__ = ("header", "items", "mode")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    mode: BoundingBoxMode
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., mode: _Optional[_Union[BoundingBoxMode, str]] = ...) -> None: ...

class GetBoundingBoxResponse(_message.Message):
    __slots__ = ("items", "boxes")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    BOXES_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    boxes: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.Box2]
    def __init__(self, items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., boxes: _Optional[_Iterable[_Union[_base_types_pb2.Box2, _Mapping]]] = ...) -> None: ...

class GetSelection(_message.Message):
    __slots__ = ("header", "types")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    types: _containers.RepeatedScalarFieldContainer[_enums_pb2.KiCadObjectType]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., types: _Optional[_Iterable[_Union[_enums_pb2.KiCadObjectType, str]]] = ...) -> None: ...

class SelectionResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, items: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...

class AddToSelection(_message.Message):
    __slots__ = ("header", "items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...

class RemoveFromSelection(_message.Message):
    __slots__ = ("header", "items")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...

class ClearSelection(_message.Message):
    __slots__ = ("header",)
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ...) -> None: ...

class HitTest(_message.Message):
    __slots__ = ("header", "id", "position", "tolerance")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    tolerance: int
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., tolerance: _Optional[int] = ...) -> None: ...

class HitTestResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: HitTestResult
    def __init__(self, result: _Optional[_Union[HitTestResult, str]] = ...) -> None: ...

class GetTitleBlockInfo(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SetTitleBlockInfo(_message.Message):
    __slots__ = ("document", "title_block")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    TITLE_BLOCK_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    title_block: _base_types_pb2.TitleBlockInfo
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., title_block: _Optional[_Union[_base_types_pb2.TitleBlockInfo, _Mapping]] = ...) -> None: ...

class GetPageSettings(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SetPageSettings(_message.Message):
    __slots__ = ("document", "page_settings")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    page_settings: _base_types_pb2.PageSettings
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., page_settings: _Optional[_Union[_base_types_pb2.PageSettings, _Mapping]] = ...) -> None: ...

class SaveDocumentToString(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SavedDocumentResponse(_message.Message):
    __slots__ = ("document", "contents")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    contents: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., contents: _Optional[str] = ...) -> None: ...

class SaveSelectionToString(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SavedSelectionResponse(_message.Message):
    __slots__ = ("ids", "contents")
    IDS_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    contents: str
    def __init__(self, ids: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., contents: _Optional[str] = ...) -> None: ...

class ParseAndCreateItemsFromString(_message.Message):
    __slots__ = ("document", "contents")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    document: _base_types_pb2.DocumentSpecifier
    contents: str
    def __init__(self, document: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., contents: _Optional[str] = ...) -> None: ...
