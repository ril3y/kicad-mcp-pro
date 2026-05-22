from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import enums_pb2 as _enums_pb2
from mp.common.types import project_settings_pb2 as _project_settings_pb2
from mp.board import board_pb2 as _board_pb2
from mp.board import board_types_pb2 as _board_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CustomRulesStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRS_UNKNOWN: _ClassVar[CustomRulesStatus]
    CRS_NONE: _ClassVar[CustomRulesStatus]
    CRS_VALID: _ClassVar[CustomRulesStatus]
    CRS_INVALID: _ClassVar[CustomRulesStatus]

class BoardOriginType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BOT_UNKNOWN: _ClassVar[BoardOriginType]
    BOT_GRID: _ClassVar[BoardOriginType]
    BOT_DRILL: _ClassVar[BoardOriginType]

class PadstackPresence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PSP_UNKNOWN: _ClassVar[PadstackPresence]
    PSP_PRESENT: _ClassVar[PadstackPresence]
    PSP_NOT_PRESENT: _ClassVar[PadstackPresence]

class DrcSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRS_UNKNOWN: _ClassVar[DrcSeverity]
    DRS_WARNING: _ClassVar[DrcSeverity]
    DRS_ERROR: _ClassVar[DrcSeverity]
    DRS_EXCLUSION: _ClassVar[DrcSeverity]
    DRS_IGNORE: _ClassVar[DrcSeverity]
    DRS_INFO: _ClassVar[DrcSeverity]
    DRS_ACTION: _ClassVar[DrcSeverity]
    DRS_DEBUG: _ClassVar[DrcSeverity]
    DRS_UNDEFINED: _ClassVar[DrcSeverity]

class InactiveLayerDisplayMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ILDM_UNKNOWN: _ClassVar[InactiveLayerDisplayMode]
    ILDM_NORMAL: _ClassVar[InactiveLayerDisplayMode]
    ILDM_DIMMED: _ClassVar[InactiveLayerDisplayMode]
    ILDM_HIDDEN: _ClassVar[InactiveLayerDisplayMode]

class NetColorDisplayMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NCDM_UNKNOWN: _ClassVar[NetColorDisplayMode]
    NCDM_ALL: _ClassVar[NetColorDisplayMode]
    NCDM_RATSNEST: _ClassVar[NetColorDisplayMode]
    NCDM_OFF: _ClassVar[NetColorDisplayMode]

class BoardFlipMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BFM_UNKNOWN: _ClassVar[BoardFlipMode]
    BFM_NORMAL: _ClassVar[BoardFlipMode]
    BFM_FLIPPED_X: _ClassVar[BoardFlipMode]

class RatsnestDisplayMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RDM_UNKNOWN: _ClassVar[RatsnestDisplayMode]
    RDM_ALL_LAYERS: _ClassVar[RatsnestDisplayMode]
    RDM_VISIBLE_LAYERS: _ClassVar[RatsnestDisplayMode]
CRS_UNKNOWN: CustomRulesStatus
CRS_NONE: CustomRulesStatus
CRS_VALID: CustomRulesStatus
CRS_INVALID: CustomRulesStatus
BOT_UNKNOWN: BoardOriginType
BOT_GRID: BoardOriginType
BOT_DRILL: BoardOriginType
PSP_UNKNOWN: PadstackPresence
PSP_PRESENT: PadstackPresence
PSP_NOT_PRESENT: PadstackPresence
DRS_UNKNOWN: DrcSeverity
DRS_WARNING: DrcSeverity
DRS_ERROR: DrcSeverity
DRS_EXCLUSION: DrcSeverity
DRS_IGNORE: DrcSeverity
DRS_INFO: DrcSeverity
DRS_ACTION: DrcSeverity
DRS_DEBUG: DrcSeverity
DRS_UNDEFINED: DrcSeverity
ILDM_UNKNOWN: InactiveLayerDisplayMode
ILDM_NORMAL: InactiveLayerDisplayMode
ILDM_DIMMED: InactiveLayerDisplayMode
ILDM_HIDDEN: InactiveLayerDisplayMode
NCDM_UNKNOWN: NetColorDisplayMode
NCDM_ALL: NetColorDisplayMode
NCDM_RATSNEST: NetColorDisplayMode
NCDM_OFF: NetColorDisplayMode
BFM_UNKNOWN: BoardFlipMode
BFM_NORMAL: BoardFlipMode
BFM_FLIPPED_X: BoardFlipMode
RDM_UNKNOWN: RatsnestDisplayMode
RDM_ALL_LAYERS: RatsnestDisplayMode
RDM_VISIBLE_LAYERS: RatsnestDisplayMode

class GetBoardStackup(_message.Message):
    __slots__ = ("board",)
    BOARD_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class BoardStackupResponse(_message.Message):
    __slots__ = ("stackup",)
    STACKUP_FIELD_NUMBER: _ClassVar[int]
    stackup: _board_pb2.BoardStackup
    def __init__(self, stackup: _Optional[_Union[_board_pb2.BoardStackup, _Mapping]] = ...) -> None: ...

class UpdateBoardStackup(_message.Message):
    __slots__ = ("board", "stackup")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    STACKUP_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    stackup: _board_pb2.BoardStackup
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., stackup: _Optional[_Union[_board_pb2.BoardStackup, _Mapping]] = ...) -> None: ...

class GetBoardEnabledLayers(_message.Message):
    __slots__ = ("board",)
    BOARD_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class BoardEnabledLayersResponse(_message.Message):
    __slots__ = ("copper_layer_count", "layers")
    COPPER_LAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    copper_layer_count: int
    layers: _containers.RepeatedScalarFieldContainer[_board_types_pb2.BoardLayer]
    def __init__(self, copper_layer_count: _Optional[int] = ..., layers: _Optional[_Iterable[_Union[_board_types_pb2.BoardLayer, str]]] = ...) -> None: ...

class SetBoardEnabledLayers(_message.Message):
    __slots__ = ("board", "copper_layer_count", "layers")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    COPPER_LAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    copper_layer_count: int
    layers: _containers.RepeatedScalarFieldContainer[_board_types_pb2.BoardLayer]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., copper_layer_count: _Optional[int] = ..., layers: _Optional[_Iterable[_Union[_board_types_pb2.BoardLayer, str]]] = ...) -> None: ...

class GetGraphicsDefaults(_message.Message):
    __slots__ = ("board",)
    BOARD_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class GraphicsDefaultsResponse(_message.Message):
    __slots__ = ("defaults",)
    DEFAULTS_FIELD_NUMBER: _ClassVar[int]
    defaults: _board_pb2.GraphicsDefaults
    def __init__(self, defaults: _Optional[_Union[_board_pb2.GraphicsDefaults, _Mapping]] = ...) -> None: ...

class GetBoardDesignRules(_message.Message):
    __slots__ = ("board",)
    BOARD_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SetBoardDesignRules(_message.Message):
    __slots__ = ("board", "rules")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    rules: _board_pb2.BoardDesignRules
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., rules: _Optional[_Union[_board_pb2.BoardDesignRules, _Mapping]] = ...) -> None: ...

class BoardDesignRulesResponse(_message.Message):
    __slots__ = ("rules", "custom_rules_status")
    RULES_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_RULES_STATUS_FIELD_NUMBER: _ClassVar[int]
    rules: _board_pb2.BoardDesignRules
    custom_rules_status: CustomRulesStatus
    def __init__(self, rules: _Optional[_Union[_board_pb2.BoardDesignRules, _Mapping]] = ..., custom_rules_status: _Optional[_Union[CustomRulesStatus, str]] = ...) -> None: ...

class GetCustomDesignRules(_message.Message):
    __slots__ = ("board",)
    BOARD_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SetCustomDesignRules(_message.Message):
    __slots__ = ("board", "rules")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    rules: _containers.RepeatedCompositeFieldContainer[_board_pb2.CustomRule]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., rules: _Optional[_Iterable[_Union[_board_pb2.CustomRule, _Mapping]]] = ...) -> None: ...

class CustomRulesResponse(_message.Message):
    __slots__ = ("status", "rules", "error_text")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    ERROR_TEXT_FIELD_NUMBER: _ClassVar[int]
    status: CustomRulesStatus
    rules: _containers.RepeatedCompositeFieldContainer[_board_pb2.CustomRule]
    error_text: str
    def __init__(self, status: _Optional[_Union[CustomRulesStatus, str]] = ..., rules: _Optional[_Iterable[_Union[_board_pb2.CustomRule, _Mapping]]] = ..., error_text: _Optional[str] = ...) -> None: ...

class GetBoardOrigin(_message.Message):
    __slots__ = ("board", "type")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    type: BoardOriginType
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., type: _Optional[_Union[BoardOriginType, str]] = ...) -> None: ...

class SetBoardOrigin(_message.Message):
    __slots__ = ("board", "type", "origin")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    type: BoardOriginType
    origin: _base_types_pb2.Vector2
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., type: _Optional[_Union[BoardOriginType, str]] = ..., origin: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ...) -> None: ...

class GetBoardLayerName(_message.Message):
    __slots__ = ("board", "layer")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    layer: _board_types_pb2.BoardLayer
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., layer: _Optional[_Union[_board_types_pb2.BoardLayer, str]] = ...) -> None: ...

class BoardLayerNameResponse(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetNets(_message.Message):
    __slots__ = ("board", "netclass_filter")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    NETCLASS_FILTER_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    netclass_filter: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., netclass_filter: _Optional[_Iterable[str]] = ...) -> None: ...

class NetsResponse(_message.Message):
    __slots__ = ("nets",)
    NETS_FIELD_NUMBER: _ClassVar[int]
    nets: _containers.RepeatedCompositeFieldContainer[_board_types_pb2.Net]
    def __init__(self, nets: _Optional[_Iterable[_Union[_board_types_pb2.Net, _Mapping]]] = ...) -> None: ...

class GetItemsByNet(_message.Message):
    __slots__ = ("header", "types", "nets")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    NETS_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    types: _containers.RepeatedScalarFieldContainer[_enums_pb2.KiCadObjectType]
    nets: _containers.RepeatedCompositeFieldContainer[_board_types_pb2.Net]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., types: _Optional[_Iterable[_Union[_enums_pb2.KiCadObjectType, str]]] = ..., nets: _Optional[_Iterable[_Union[_board_types_pb2.Net, _Mapping]]] = ...) -> None: ...

class GetItemsByNetClass(_message.Message):
    __slots__ = ("header", "types", "net_classes")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    NET_CLASSES_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    types: _containers.RepeatedScalarFieldContainer[_enums_pb2.KiCadObjectType]
    net_classes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., types: _Optional[_Iterable[_Union[_enums_pb2.KiCadObjectType, str]]] = ..., net_classes: _Optional[_Iterable[str]] = ...) -> None: ...

class GetConnectedItems(_message.Message):
    __slots__ = ("header", "items", "types")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    header: _base_types_pb2.ItemHeader
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    types: _containers.RepeatedScalarFieldContainer[_enums_pb2.KiCadObjectType]
    def __init__(self, header: _Optional[_Union[_base_types_pb2.ItemHeader, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., types: _Optional[_Iterable[_Union[_enums_pb2.KiCadObjectType, str]]] = ...) -> None: ...

class GetNetClassForNets(_message.Message):
    __slots__ = ("net",)
    NET_FIELD_NUMBER: _ClassVar[int]
    net: _containers.RepeatedCompositeFieldContainer[_board_types_pb2.Net]
    def __init__(self, net: _Optional[_Iterable[_Union[_board_types_pb2.Net, _Mapping]]] = ...) -> None: ...

class NetClassForNetsResponse(_message.Message):
    __slots__ = ("classes",)
    class ClassesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _project_settings_pb2.NetClass
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_project_settings_pb2.NetClass, _Mapping]] = ...) -> None: ...
    CLASSES_FIELD_NUMBER: _ClassVar[int]
    classes: _containers.MessageMap[str, _project_settings_pb2.NetClass]
    def __init__(self, classes: _Optional[_Mapping[str, _project_settings_pb2.NetClass]] = ...) -> None: ...

class RefillZones(_message.Message):
    __slots__ = ("board", "zones")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    ZONES_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    zones: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., zones: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...

class GetPadShapeAsPolygon(_message.Message):
    __slots__ = ("board", "pads", "layer")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    PADS_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    pads: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    layer: _board_types_pb2.BoardLayer
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., pads: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., layer: _Optional[_Union[_board_types_pb2.BoardLayer, str]] = ...) -> None: ...

class PadShapeAsPolygonResponse(_message.Message):
    __slots__ = ("pads", "polygons")
    PADS_FIELD_NUMBER: _ClassVar[int]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    pads: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    polygons: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.PolygonWithHoles]
    def __init__(self, pads: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., polygons: _Optional[_Iterable[_Union[_base_types_pb2.PolygonWithHoles, _Mapping]]] = ...) -> None: ...

class CheckPadstackPresenceOnLayers(_message.Message):
    __slots__ = ("board", "items", "layers")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    layers: _containers.RepeatedScalarFieldContainer[_board_types_pb2.BoardLayer]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., layers: _Optional[_Iterable[_Union[_board_types_pb2.BoardLayer, str]]] = ...) -> None: ...

class PadstackPresenceEntry(_message.Message):
    __slots__ = ("item", "layer", "presence")
    ITEM_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_FIELD_NUMBER: _ClassVar[int]
    item: _base_types_pb2.KIID
    layer: _board_types_pb2.BoardLayer
    presence: PadstackPresence
    def __init__(self, item: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., layer: _Optional[_Union[_board_types_pb2.BoardLayer, str]] = ..., presence: _Optional[_Union[PadstackPresence, str]] = ...) -> None: ...

class PadstackPresenceResponse(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[PadstackPresenceEntry]
    def __init__(self, entries: _Optional[_Iterable[_Union[PadstackPresenceEntry, _Mapping]]] = ...) -> None: ...

class InjectDrcError(_message.Message):
    __slots__ = ("board", "severity", "message", "position", "items")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    severity: DrcSeverity
    message: str
    position: _base_types_pb2.Vector2
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., severity: _Optional[_Union[DrcSeverity, str]] = ..., message: _Optional[str] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...

class InjectDrcErrorResponse(_message.Message):
    __slots__ = ("marker",)
    MARKER_FIELD_NUMBER: _ClassVar[int]
    marker: _base_types_pb2.KIID
    def __init__(self, marker: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ...) -> None: ...

class GetVisibleLayers(_message.Message):
    __slots__ = ("board",)
    BOARD_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class BoardLayerResponse(_message.Message):
    __slots__ = ("layer",)
    LAYER_FIELD_NUMBER: _ClassVar[int]
    layer: _board_types_pb2.BoardLayer
    def __init__(self, layer: _Optional[_Union[_board_types_pb2.BoardLayer, str]] = ...) -> None: ...

class BoardLayers(_message.Message):
    __slots__ = ("layers",)
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedScalarFieldContainer[_board_types_pb2.BoardLayer]
    def __init__(self, layers: _Optional[_Iterable[_Union[_board_types_pb2.BoardLayer, str]]] = ...) -> None: ...

class SetVisibleLayers(_message.Message):
    __slots__ = ("board", "layers")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    layers: _containers.RepeatedScalarFieldContainer[_board_types_pb2.BoardLayer]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., layers: _Optional[_Iterable[_Union[_board_types_pb2.BoardLayer, str]]] = ...) -> None: ...

class GetActiveLayer(_message.Message):
    __slots__ = ("board",)
    BOARD_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ...) -> None: ...

class SetActiveLayer(_message.Message):
    __slots__ = ("board", "layer")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    layer: _board_types_pb2.BoardLayer
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., layer: _Optional[_Union[_board_types_pb2.BoardLayer, str]] = ...) -> None: ...

class BoardEditorAppearanceSettings(_message.Message):
    __slots__ = ("inactive_layer_display", "net_color_display", "board_flip", "ratsnest_display")
    INACTIVE_LAYER_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    NET_COLOR_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    BOARD_FLIP_FIELD_NUMBER: _ClassVar[int]
    RATSNEST_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    inactive_layer_display: InactiveLayerDisplayMode
    net_color_display: NetColorDisplayMode
    board_flip: BoardFlipMode
    ratsnest_display: RatsnestDisplayMode
    def __init__(self, inactive_layer_display: _Optional[_Union[InactiveLayerDisplayMode, str]] = ..., net_color_display: _Optional[_Union[NetColorDisplayMode, str]] = ..., board_flip: _Optional[_Union[BoardFlipMode, str]] = ..., ratsnest_display: _Optional[_Union[RatsnestDisplayMode, str]] = ...) -> None: ...

class GetBoardEditorAppearanceSettings(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetBoardEditorAppearanceSettings(_message.Message):
    __slots__ = ("settings",)
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    settings: BoardEditorAppearanceSettings
    def __init__(self, settings: _Optional[_Union[BoardEditorAppearanceSettings, _Mapping]] = ...) -> None: ...

class InteractiveMoveItems(_message.Message):
    __slots__ = ("board", "items")
    BOARD_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    board: _base_types_pb2.DocumentSpecifier
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, board: _Optional[_Union[_base_types_pb2.DocumentSpecifier, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...
