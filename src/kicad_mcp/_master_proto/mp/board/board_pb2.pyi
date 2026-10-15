from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.board import board_types_pb2 as _board_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoardStackupLayerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BSLT_UNKNOWN: _ClassVar[BoardStackupLayerType]
    BSLT_COPPER: _ClassVar[BoardStackupLayerType]
    BSLT_DIELECTRIC: _ClassVar[BoardStackupLayerType]
    BSLT_SILKSCREEN: _ClassVar[BoardStackupLayerType]
    BSLT_SOLDERMASK: _ClassVar[BoardStackupLayerType]
    BSLT_SOLDERPASTE: _ClassVar[BoardStackupLayerType]
    BSLT_UNDEFINED: _ClassVar[BoardStackupLayerType]

class BoardLayerClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BLC_UNKNOWN: _ClassVar[BoardLayerClass]
    BLC_SILKSCREEN: _ClassVar[BoardLayerClass]
    BLC_COPPER: _ClassVar[BoardLayerClass]
    BLC_EDGES: _ClassVar[BoardLayerClass]
    BLC_COURTYARD: _ClassVar[BoardLayerClass]
    BLC_FABRICATION: _ClassVar[BoardLayerClass]
    BLC_OTHER: _ClassVar[BoardLayerClass]

class TeardropTarget(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TDT_UNKNOWN: _ClassVar[TeardropTarget]
    TDT_ROUND: _ClassVar[TeardropTarget]
    TDT_RECT: _ClassVar[TeardropTarget]
    TDT_TRACK: _ClassVar[TeardropTarget]

class DrcErrorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRCET_UNKNOWN: _ClassVar[DrcErrorType]
    DRCET_UNCONNECTED_ITEMS: _ClassVar[DrcErrorType]
    DRCET_SHORTING_ITEMS: _ClassVar[DrcErrorType]
    DRCET_ALLOWED_ITEMS: _ClassVar[DrcErrorType]
    DRCET_TEXT_ON_EDGECUTS: _ClassVar[DrcErrorType]
    DRCET_CLEARANCE: _ClassVar[DrcErrorType]
    DRCET_CREEPAGE: _ClassVar[DrcErrorType]
    DRCET_TRACKS_CROSSING: _ClassVar[DrcErrorType]
    DRCET_EDGE_CLEARANCE: _ClassVar[DrcErrorType]
    DRCET_ZONES_INTERSECT: _ClassVar[DrcErrorType]
    DRCET_ISOLATED_COPPER: _ClassVar[DrcErrorType]
    DRCET_STARVED_THERMAL: _ClassVar[DrcErrorType]
    DRCET_DANGLING_VIA: _ClassVar[DrcErrorType]
    DRCET_DANGLING_TRACK: _ClassVar[DrcErrorType]
    DRCET_DRILLED_HOLES_TOO_CLOSE: _ClassVar[DrcErrorType]
    DRCET_DRILLED_HOLES_COLOCATED: _ClassVar[DrcErrorType]
    DRCET_HOLE_CLEARANCE: _ClassVar[DrcErrorType]
    DRCET_CONNECTION_WIDTH: _ClassVar[DrcErrorType]
    DRCET_TRACK_WIDTH: _ClassVar[DrcErrorType]
    DRCET_TRACK_ANGLE: _ClassVar[DrcErrorType]
    DRCET_TRACK_SEGMENT_LENGTH: _ClassVar[DrcErrorType]
    DRCET_ANNULAR_WIDTH: _ClassVar[DrcErrorType]
    DRCET_DRILL_OUT_OF_RANGE: _ClassVar[DrcErrorType]
    DRCET_VIA_DIAMETER: _ClassVar[DrcErrorType]
    DRCET_PADSTACK: _ClassVar[DrcErrorType]
    DRCET_PADSTACK_INVALID: _ClassVar[DrcErrorType]
    DRCET_MICROVIA_DRILL_OUT_OF_RANGE: _ClassVar[DrcErrorType]
    DRCET_OVERLAPPING_FOOTPRINTS: _ClassVar[DrcErrorType]
    DRCET_MISSING_COURTYARD: _ClassVar[DrcErrorType]
    DRCET_MALFORMED_COURTYARD: _ClassVar[DrcErrorType]
    DRCET_PTH_IN_COURTYARD: _ClassVar[DrcErrorType]
    DRCET_NPTH_IN_COURTYARD: _ClassVar[DrcErrorType]
    DRCET_DISABLED_LAYER_ITEM: _ClassVar[DrcErrorType]
    DRCET_INVALID_OUTLINE: _ClassVar[DrcErrorType]
    DRCET_MISSING_FOOTPRINT: _ClassVar[DrcErrorType]
    DRCET_DUPLICATE_FOOTPRINT: _ClassVar[DrcErrorType]
    DRCET_NET_CONFLICT: _ClassVar[DrcErrorType]
    DRCET_EXTRA_FOOTPRINT: _ClassVar[DrcErrorType]
    DRCET_SCHEMATIC_PARITY: _ClassVar[DrcErrorType]
    DRCET_SCHEMATIC_FIELDS_PARITY: _ClassVar[DrcErrorType]
    DRCET_FOOTPRINT_FILTERS: _ClassVar[DrcErrorType]
    DRCET_LIB_FOOTPRINT_ISSUES: _ClassVar[DrcErrorType]
    DRCET_LIB_FOOTPRINT_MISMATCH: _ClassVar[DrcErrorType]
    DRCET_UNRESOLVED_VARIABLE: _ClassVar[DrcErrorType]
    DRCET_ASSERTION_FAILURE: _ClassVar[DrcErrorType]
    DRCET_GENERIC_WARNING: _ClassVar[DrcErrorType]
    DRCET_GENERIC_ERROR: _ClassVar[DrcErrorType]
    DRCET_COPPER_SLIVER: _ClassVar[DrcErrorType]
    DRCET_SILK_CLEARANCE: _ClassVar[DrcErrorType]
    DRCET_SILK_MASK_CLEARANCE: _ClassVar[DrcErrorType]
    DRCET_SILK_EDGE_CLEARANCE: _ClassVar[DrcErrorType]
    DRCET_SOLDERMASK_BRIDGE: _ClassVar[DrcErrorType]
    DRCET_TEXT_HEIGHT: _ClassVar[DrcErrorType]
    DRCET_TEXT_THICKNESS: _ClassVar[DrcErrorType]
    DRCET_LENGTH_OUT_OF_RANGE: _ClassVar[DrcErrorType]
    DRCET_SKEW_OUT_OF_RANGE: _ClassVar[DrcErrorType]
    DRCET_VIA_COUNT_OUT_OF_RANGE: _ClassVar[DrcErrorType]
    DRCET_DIFF_PAIR_GAP_OUT_OF_RANGE: _ClassVar[DrcErrorType]
    DRCET_DIFF_PAIR_UNCOUPLED_LENGTH_TOO_LONG: _ClassVar[DrcErrorType]
    DRCET_FOOTPRINT: _ClassVar[DrcErrorType]
    DRCET_FOOTPRINT_TYPE_MISMATCH: _ClassVar[DrcErrorType]
    DRCET_PAD_TH_WITH_NO_HOLE: _ClassVar[DrcErrorType]
    DRCET_MIRRORED_TEXT_ON_FRONT_LAYER: _ClassVar[DrcErrorType]
    DRCET_NONMIRRORED_TEXT_ON_BACK_LAYER: _ClassVar[DrcErrorType]
    DRCET_MISSING_TUNING_PROFILE: _ClassVar[DrcErrorType]
    DRCET_TUNING_PROFILE_IMPLICIT_RULES: _ClassVar[DrcErrorType]
    DRCET_TRACK_ON_POST_MACHINED_LAYER: _ClassVar[DrcErrorType]
    DRCET_TRACK_NOT_CENTERED_ON_VIA: _ClassVar[DrcErrorType]

class CustomRuleLayerMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRLM_UNKNOWN: _ClassVar[CustomRuleLayerMode]
    CRLM_OUTER: _ClassVar[CustomRuleLayerMode]
    CRLM_INNER: _ClassVar[CustomRuleLayerMode]

class CustomRuleConstraintType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRCT_UNKNOWN: _ClassVar[CustomRuleConstraintType]
    CRCT_CLEARANCE: _ClassVar[CustomRuleConstraintType]
    CRCT_CREEPAGE: _ClassVar[CustomRuleConstraintType]
    CRCT_HOLE_CLEARANCE: _ClassVar[CustomRuleConstraintType]
    CRCT_HOLE_TO_HOLE: _ClassVar[CustomRuleConstraintType]
    CRCT_EDGE_CLEARANCE: _ClassVar[CustomRuleConstraintType]
    CRCT_HOLE_SIZE: _ClassVar[CustomRuleConstraintType]
    CRCT_COURTYARD_CLEARANCE: _ClassVar[CustomRuleConstraintType]
    CRCT_SILK_CLEARANCE: _ClassVar[CustomRuleConstraintType]
    CRCT_TEXT_HEIGHT: _ClassVar[CustomRuleConstraintType]
    CRCT_TEXT_THICKNESS: _ClassVar[CustomRuleConstraintType]
    CRCT_TRACK_WIDTH: _ClassVar[CustomRuleConstraintType]
    CRCT_TRACK_SEGMENT_LENGTH: _ClassVar[CustomRuleConstraintType]
    CRCT_ANNULAR_WIDTH: _ClassVar[CustomRuleConstraintType]
    CRCT_ZONE_CONNECTION: _ClassVar[CustomRuleConstraintType]
    CRCT_THERMAL_RELIEF_GAP: _ClassVar[CustomRuleConstraintType]
    CRCT_THERMAL_SPOKE_WIDTH: _ClassVar[CustomRuleConstraintType]
    CRCT_MIN_RESOLVED_SPOKES: _ClassVar[CustomRuleConstraintType]
    CRCT_SOLDER_MASK_EXPANSION: _ClassVar[CustomRuleConstraintType]
    CRCT_SOLDER_PASTE_ABS_MARGIN: _ClassVar[CustomRuleConstraintType]
    CRCT_SOLDER_PASTE_REL_MARGIN: _ClassVar[CustomRuleConstraintType]
    CRCT_DISALLOW: _ClassVar[CustomRuleConstraintType]
    CRCT_VIA_DIAMETER: _ClassVar[CustomRuleConstraintType]
    CRCT_LENGTH: _ClassVar[CustomRuleConstraintType]
    CRCT_SKEW: _ClassVar[CustomRuleConstraintType]
    CRCT_DIFF_PAIR_GAP: _ClassVar[CustomRuleConstraintType]
    CRCT_MAX_UNCOUPLED: _ClassVar[CustomRuleConstraintType]
    CRCT_DIFF_PAIR_INTRA_SKEW: _ClassVar[CustomRuleConstraintType]
    CRCT_VIA_COUNT: _ClassVar[CustomRuleConstraintType]
    CRCT_PHYSICAL_CLEARANCE: _ClassVar[CustomRuleConstraintType]
    CRCT_PHYSICAL_HOLE_CLEARANCE: _ClassVar[CustomRuleConstraintType]
    CRCT_ASSERTION: _ClassVar[CustomRuleConstraintType]
    CRCT_CONNECTION_WIDTH: _ClassVar[CustomRuleConstraintType]
    CRCT_TRACK_ANGLE: _ClassVar[CustomRuleConstraintType]
    CRCT_VIA_DANGLING: _ClassVar[CustomRuleConstraintType]
    CRCT_BRIDGED_MASK: _ClassVar[CustomRuleConstraintType]
    CRCT_SOLDER_MASK_SLIVER: _ClassVar[CustomRuleConstraintType]
    CRCT_NET_CHAIN_LENGTH: _ClassVar[CustomRuleConstraintType]
    CRCT_NET_CHAIN_STUB_LENGTH: _ClassVar[CustomRuleConstraintType]
    CRCT_NET_CHAIN_RETURN_PATH: _ClassVar[CustomRuleConstraintType]

class CustomRuleConstraintOption(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRCO_UNKNOWN: _ClassVar[CustomRuleConstraintOption]
    CRCO_SKEW_WITHIN_DIFF_PAIRS: _ClassVar[CustomRuleConstraintOption]
    CRCO_SPACE_DOMAIN: _ClassVar[CustomRuleConstraintOption]
    CRCO_TIME_DOMAIN: _ClassVar[CustomRuleConstraintOption]

class CustomRuleDisallowType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRDT_UNKNOWN: _ClassVar[CustomRuleDisallowType]
    CRDT_THROUGH_VIAS: _ClassVar[CustomRuleDisallowType]
    CRDT_MICRO_VIAS: _ClassVar[CustomRuleDisallowType]
    CRDT_BLIND_VIAS: _ClassVar[CustomRuleDisallowType]
    CRDT_BURIED_VIAS: _ClassVar[CustomRuleDisallowType]
    CRDT_TRACKS: _ClassVar[CustomRuleDisallowType]
    CRDT_PADS: _ClassVar[CustomRuleDisallowType]
    CRDT_ZONES: _ClassVar[CustomRuleDisallowType]
    CRDT_TEXTS: _ClassVar[CustomRuleDisallowType]
    CRDT_GRAPHICS: _ClassVar[CustomRuleDisallowType]
    CRDT_HOLES: _ClassVar[CustomRuleDisallowType]
    CRDT_FOOTPRINTS: _ClassVar[CustomRuleDisallowType]
BSLT_UNKNOWN: BoardStackupLayerType
BSLT_COPPER: BoardStackupLayerType
BSLT_DIELECTRIC: BoardStackupLayerType
BSLT_SILKSCREEN: BoardStackupLayerType
BSLT_SOLDERMASK: BoardStackupLayerType
BSLT_SOLDERPASTE: BoardStackupLayerType
BSLT_UNDEFINED: BoardStackupLayerType
BLC_UNKNOWN: BoardLayerClass
BLC_SILKSCREEN: BoardLayerClass
BLC_COPPER: BoardLayerClass
BLC_EDGES: BoardLayerClass
BLC_COURTYARD: BoardLayerClass
BLC_FABRICATION: BoardLayerClass
BLC_OTHER: BoardLayerClass
TDT_UNKNOWN: TeardropTarget
TDT_ROUND: TeardropTarget
TDT_RECT: TeardropTarget
TDT_TRACK: TeardropTarget
DRCET_UNKNOWN: DrcErrorType
DRCET_UNCONNECTED_ITEMS: DrcErrorType
DRCET_SHORTING_ITEMS: DrcErrorType
DRCET_ALLOWED_ITEMS: DrcErrorType
DRCET_TEXT_ON_EDGECUTS: DrcErrorType
DRCET_CLEARANCE: DrcErrorType
DRCET_CREEPAGE: DrcErrorType
DRCET_TRACKS_CROSSING: DrcErrorType
DRCET_EDGE_CLEARANCE: DrcErrorType
DRCET_ZONES_INTERSECT: DrcErrorType
DRCET_ISOLATED_COPPER: DrcErrorType
DRCET_STARVED_THERMAL: DrcErrorType
DRCET_DANGLING_VIA: DrcErrorType
DRCET_DANGLING_TRACK: DrcErrorType
DRCET_DRILLED_HOLES_TOO_CLOSE: DrcErrorType
DRCET_DRILLED_HOLES_COLOCATED: DrcErrorType
DRCET_HOLE_CLEARANCE: DrcErrorType
DRCET_CONNECTION_WIDTH: DrcErrorType
DRCET_TRACK_WIDTH: DrcErrorType
DRCET_TRACK_ANGLE: DrcErrorType
DRCET_TRACK_SEGMENT_LENGTH: DrcErrorType
DRCET_ANNULAR_WIDTH: DrcErrorType
DRCET_DRILL_OUT_OF_RANGE: DrcErrorType
DRCET_VIA_DIAMETER: DrcErrorType
DRCET_PADSTACK: DrcErrorType
DRCET_PADSTACK_INVALID: DrcErrorType
DRCET_MICROVIA_DRILL_OUT_OF_RANGE: DrcErrorType
DRCET_OVERLAPPING_FOOTPRINTS: DrcErrorType
DRCET_MISSING_COURTYARD: DrcErrorType
DRCET_MALFORMED_COURTYARD: DrcErrorType
DRCET_PTH_IN_COURTYARD: DrcErrorType
DRCET_NPTH_IN_COURTYARD: DrcErrorType
DRCET_DISABLED_LAYER_ITEM: DrcErrorType
DRCET_INVALID_OUTLINE: DrcErrorType
DRCET_MISSING_FOOTPRINT: DrcErrorType
DRCET_DUPLICATE_FOOTPRINT: DrcErrorType
DRCET_NET_CONFLICT: DrcErrorType
DRCET_EXTRA_FOOTPRINT: DrcErrorType
DRCET_SCHEMATIC_PARITY: DrcErrorType
DRCET_SCHEMATIC_FIELDS_PARITY: DrcErrorType
DRCET_FOOTPRINT_FILTERS: DrcErrorType
DRCET_LIB_FOOTPRINT_ISSUES: DrcErrorType
DRCET_LIB_FOOTPRINT_MISMATCH: DrcErrorType
DRCET_UNRESOLVED_VARIABLE: DrcErrorType
DRCET_ASSERTION_FAILURE: DrcErrorType
DRCET_GENERIC_WARNING: DrcErrorType
DRCET_GENERIC_ERROR: DrcErrorType
DRCET_COPPER_SLIVER: DrcErrorType
DRCET_SILK_CLEARANCE: DrcErrorType
DRCET_SILK_MASK_CLEARANCE: DrcErrorType
DRCET_SILK_EDGE_CLEARANCE: DrcErrorType
DRCET_SOLDERMASK_BRIDGE: DrcErrorType
DRCET_TEXT_HEIGHT: DrcErrorType
DRCET_TEXT_THICKNESS: DrcErrorType
DRCET_LENGTH_OUT_OF_RANGE: DrcErrorType
DRCET_SKEW_OUT_OF_RANGE: DrcErrorType
DRCET_VIA_COUNT_OUT_OF_RANGE: DrcErrorType
DRCET_DIFF_PAIR_GAP_OUT_OF_RANGE: DrcErrorType
DRCET_DIFF_PAIR_UNCOUPLED_LENGTH_TOO_LONG: DrcErrorType
DRCET_FOOTPRINT: DrcErrorType
DRCET_FOOTPRINT_TYPE_MISMATCH: DrcErrorType
DRCET_PAD_TH_WITH_NO_HOLE: DrcErrorType
DRCET_MIRRORED_TEXT_ON_FRONT_LAYER: DrcErrorType
DRCET_NONMIRRORED_TEXT_ON_BACK_LAYER: DrcErrorType
DRCET_MISSING_TUNING_PROFILE: DrcErrorType
DRCET_TUNING_PROFILE_IMPLICIT_RULES: DrcErrorType
DRCET_TRACK_ON_POST_MACHINED_LAYER: DrcErrorType
DRCET_TRACK_NOT_CENTERED_ON_VIA: DrcErrorType
CRLM_UNKNOWN: CustomRuleLayerMode
CRLM_OUTER: CustomRuleLayerMode
CRLM_INNER: CustomRuleLayerMode
CRCT_UNKNOWN: CustomRuleConstraintType
CRCT_CLEARANCE: CustomRuleConstraintType
CRCT_CREEPAGE: CustomRuleConstraintType
CRCT_HOLE_CLEARANCE: CustomRuleConstraintType
CRCT_HOLE_TO_HOLE: CustomRuleConstraintType
CRCT_EDGE_CLEARANCE: CustomRuleConstraintType
CRCT_HOLE_SIZE: CustomRuleConstraintType
CRCT_COURTYARD_CLEARANCE: CustomRuleConstraintType
CRCT_SILK_CLEARANCE: CustomRuleConstraintType
CRCT_TEXT_HEIGHT: CustomRuleConstraintType
CRCT_TEXT_THICKNESS: CustomRuleConstraintType
CRCT_TRACK_WIDTH: CustomRuleConstraintType
CRCT_TRACK_SEGMENT_LENGTH: CustomRuleConstraintType
CRCT_ANNULAR_WIDTH: CustomRuleConstraintType
CRCT_ZONE_CONNECTION: CustomRuleConstraintType
CRCT_THERMAL_RELIEF_GAP: CustomRuleConstraintType
CRCT_THERMAL_SPOKE_WIDTH: CustomRuleConstraintType
CRCT_MIN_RESOLVED_SPOKES: CustomRuleConstraintType
CRCT_SOLDER_MASK_EXPANSION: CustomRuleConstraintType
CRCT_SOLDER_PASTE_ABS_MARGIN: CustomRuleConstraintType
CRCT_SOLDER_PASTE_REL_MARGIN: CustomRuleConstraintType
CRCT_DISALLOW: CustomRuleConstraintType
CRCT_VIA_DIAMETER: CustomRuleConstraintType
CRCT_LENGTH: CustomRuleConstraintType
CRCT_SKEW: CustomRuleConstraintType
CRCT_DIFF_PAIR_GAP: CustomRuleConstraintType
CRCT_MAX_UNCOUPLED: CustomRuleConstraintType
CRCT_DIFF_PAIR_INTRA_SKEW: CustomRuleConstraintType
CRCT_VIA_COUNT: CustomRuleConstraintType
CRCT_PHYSICAL_CLEARANCE: CustomRuleConstraintType
CRCT_PHYSICAL_HOLE_CLEARANCE: CustomRuleConstraintType
CRCT_ASSERTION: CustomRuleConstraintType
CRCT_CONNECTION_WIDTH: CustomRuleConstraintType
CRCT_TRACK_ANGLE: CustomRuleConstraintType
CRCT_VIA_DANGLING: CustomRuleConstraintType
CRCT_BRIDGED_MASK: CustomRuleConstraintType
CRCT_SOLDER_MASK_SLIVER: CustomRuleConstraintType
CRCT_NET_CHAIN_LENGTH: CustomRuleConstraintType
CRCT_NET_CHAIN_STUB_LENGTH: CustomRuleConstraintType
CRCT_NET_CHAIN_RETURN_PATH: CustomRuleConstraintType
CRCO_UNKNOWN: CustomRuleConstraintOption
CRCO_SKEW_WITHIN_DIFF_PAIRS: CustomRuleConstraintOption
CRCO_SPACE_DOMAIN: CustomRuleConstraintOption
CRCO_TIME_DOMAIN: CustomRuleConstraintOption
CRDT_UNKNOWN: CustomRuleDisallowType
CRDT_THROUGH_VIAS: CustomRuleDisallowType
CRDT_MICRO_VIAS: CustomRuleDisallowType
CRDT_BLIND_VIAS: CustomRuleDisallowType
CRDT_BURIED_VIAS: CustomRuleDisallowType
CRDT_TRACKS: CustomRuleDisallowType
CRDT_PADS: CustomRuleDisallowType
CRDT_ZONES: CustomRuleDisallowType
CRDT_TEXTS: CustomRuleDisallowType
CRDT_GRAPHICS: CustomRuleDisallowType
CRDT_HOLES: CustomRuleDisallowType
CRDT_FOOTPRINTS: CustomRuleDisallowType

class BoardFinish(_message.Message):
    __slots__ = ("type_name",)
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    type_name: str
    def __init__(self, type_name: _Optional[str] = ...) -> None: ...

class BoardImpedanceControl(_message.Message):
    __slots__ = ("is_controlled",)
    IS_CONTROLLED_FIELD_NUMBER: _ClassVar[int]
    is_controlled: bool
    def __init__(self, is_controlled: bool = ...) -> None: ...

class BoardEdgeConnector(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Castellation(_message.Message):
    __slots__ = ("has_castellated_pads",)
    HAS_CASTELLATED_PADS_FIELD_NUMBER: _ClassVar[int]
    has_castellated_pads: bool
    def __init__(self, has_castellated_pads: bool = ...) -> None: ...

class EdgePlating(_message.Message):
    __slots__ = ("has_edge_plating",)
    HAS_EDGE_PLATING_FIELD_NUMBER: _ClassVar[int]
    has_edge_plating: bool
    def __init__(self, has_edge_plating: bool = ...) -> None: ...

class BoardEdgeSettings(_message.Message):
    __slots__ = ("connector", "castellation", "plating")
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    CASTELLATION_FIELD_NUMBER: _ClassVar[int]
    PLATING_FIELD_NUMBER: _ClassVar[int]
    connector: BoardEdgeConnector
    castellation: Castellation
    plating: EdgePlating
    def __init__(self, connector: _Optional[_Union[BoardEdgeConnector, _Mapping]] = ..., castellation: _Optional[_Union[Castellation, _Mapping]] = ..., plating: _Optional[_Union[EdgePlating, _Mapping]] = ...) -> None: ...

class BoardStackupCopperLayer(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BoardStackupDielectricProperties(_message.Message):
    __slots__ = ("epsilon_r", "loss_tangent", "material_name", "thickness")
    EPSILON_R_FIELD_NUMBER: _ClassVar[int]
    LOSS_TANGENT_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    epsilon_r: float
    loss_tangent: float
    material_name: str
    thickness: _base_types_pb2.Distance
    def __init__(self, epsilon_r: _Optional[float] = ..., loss_tangent: _Optional[float] = ..., material_name: _Optional[str] = ..., thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class BoardStackupDielectricLayer(_message.Message):
    __slots__ = ("layer",)
    LAYER_FIELD_NUMBER: _ClassVar[int]
    layer: _containers.RepeatedCompositeFieldContainer[BoardStackupDielectricProperties]
    def __init__(self, layer: _Optional[_Iterable[_Union[BoardStackupDielectricProperties, _Mapping]]] = ...) -> None: ...

class BoardStackupLayer(_message.Message):
    __slots__ = ("thickness", "layer", "enabled", "type", "dielectric", "color", "material_name", "user_name")
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DIELECTRIC_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    thickness: _base_types_pb2.Distance
    layer: _board_types_pb2.BoardLayer
    enabled: bool
    type: BoardStackupLayerType
    dielectric: BoardStackupDielectricLayer
    color: _base_types_pb2.Color
    material_name: str
    user_name: str
    def __init__(self, thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., layer: _Optional[_Union[_board_types_pb2.BoardLayer, str]] = ..., enabled: bool = ..., type: _Optional[_Union[BoardStackupLayerType, str]] = ..., dielectric: _Optional[_Union[BoardStackupDielectricLayer, _Mapping]] = ..., color: _Optional[_Union[_base_types_pb2.Color, _Mapping]] = ..., material_name: _Optional[str] = ..., user_name: _Optional[str] = ...) -> None: ...

class BoardStackup(_message.Message):
    __slots__ = ("finish", "impedance", "edge", "layers")
    FINISH_FIELD_NUMBER: _ClassVar[int]
    IMPEDANCE_FIELD_NUMBER: _ClassVar[int]
    EDGE_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    finish: BoardFinish
    impedance: BoardImpedanceControl
    edge: BoardEdgeSettings
    layers: _containers.RepeatedCompositeFieldContainer[BoardStackupLayer]
    def __init__(self, finish: _Optional[_Union[BoardFinish, _Mapping]] = ..., impedance: _Optional[_Union[BoardImpedanceControl, _Mapping]] = ..., edge: _Optional[_Union[BoardEdgeSettings, _Mapping]] = ..., layers: _Optional[_Iterable[_Union[BoardStackupLayer, _Mapping]]] = ...) -> None: ...

class BoardLayerGraphicsDefaults(_message.Message):
    __slots__ = ("layer", "text", "line_thickness")
    LAYER_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    LINE_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    layer: BoardLayerClass
    text: _base_types_pb2.TextAttributes
    line_thickness: _base_types_pb2.Distance
    def __init__(self, layer: _Optional[_Union[BoardLayerClass, str]] = ..., text: _Optional[_Union[_base_types_pb2.TextAttributes, _Mapping]] = ..., line_thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class GraphicsDefaults(_message.Message):
    __slots__ = ("layers",)
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedCompositeFieldContainer[BoardLayerGraphicsDefaults]
    def __init__(self, layers: _Optional[_Iterable[_Union[BoardLayerGraphicsDefaults, _Mapping]]] = ...) -> None: ...

class BoardSettings(_message.Message):
    __slots__ = ("graphics_defaults",)
    GRAPHICS_DEFAULTS_FIELD_NUMBER: _ClassVar[int]
    graphics_defaults: GraphicsDefaults
    def __init__(self, graphics_defaults: _Optional[_Union[GraphicsDefaults, _Mapping]] = ...) -> None: ...

class MinimumConstraints(_message.Message):
    __slots__ = ("min_clearance", "min_groove_width", "min_connection_width", "min_track_width", "min_via_annular_width", "min_via_size", "min_through_drill", "min_microvia_size", "min_microvia_drill", "copper_edge_clearance", "hole_clearance", "hole_to_hole_min", "silk_clearance", "min_resolved_spokes", "min_silk_text_height", "min_silk_text_thickness")
    MIN_CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    MIN_GROOVE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MIN_CONNECTION_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MIN_TRACK_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MIN_VIA_ANNULAR_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MIN_VIA_SIZE_FIELD_NUMBER: _ClassVar[int]
    MIN_THROUGH_DRILL_FIELD_NUMBER: _ClassVar[int]
    MIN_MICROVIA_SIZE_FIELD_NUMBER: _ClassVar[int]
    MIN_MICROVIA_DRILL_FIELD_NUMBER: _ClassVar[int]
    COPPER_EDGE_CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    HOLE_CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    HOLE_TO_HOLE_MIN_FIELD_NUMBER: _ClassVar[int]
    SILK_CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    MIN_RESOLVED_SPOKES_FIELD_NUMBER: _ClassVar[int]
    MIN_SILK_TEXT_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    MIN_SILK_TEXT_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    min_clearance: _base_types_pb2.Distance
    min_groove_width: _base_types_pb2.Distance
    min_connection_width: _base_types_pb2.Distance
    min_track_width: _base_types_pb2.Distance
    min_via_annular_width: _base_types_pb2.Distance
    min_via_size: _base_types_pb2.Distance
    min_through_drill: _base_types_pb2.Distance
    min_microvia_size: _base_types_pb2.Distance
    min_microvia_drill: _base_types_pb2.Distance
    copper_edge_clearance: _base_types_pb2.Distance
    hole_clearance: _base_types_pb2.Distance
    hole_to_hole_min: _base_types_pb2.Distance
    silk_clearance: _base_types_pb2.Distance
    min_resolved_spokes: int
    min_silk_text_height: _base_types_pb2.Distance
    min_silk_text_thickness: _base_types_pb2.Distance
    def __init__(self, min_clearance: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_groove_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_connection_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_track_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_via_annular_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_via_size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_through_drill: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_microvia_size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_microvia_drill: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., copper_edge_clearance: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., hole_clearance: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., hole_to_hole_min: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., silk_clearance: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_resolved_spokes: _Optional[int] = ..., min_silk_text_height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_silk_text_thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class PresetTrackWidth(_message.Message):
    __slots__ = ("width",)
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    width: _base_types_pb2.Distance
    def __init__(self, width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class PresetViaDimension(_message.Message):
    __slots__ = ("diameter", "drill")
    DIAMETER_FIELD_NUMBER: _ClassVar[int]
    DRILL_FIELD_NUMBER: _ClassVar[int]
    diameter: _base_types_pb2.Distance
    drill: _base_types_pb2.Distance
    def __init__(self, diameter: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., drill: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class PresetDiffPairDimension(_message.Message):
    __slots__ = ("width", "gap", "via_gap")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    GAP_FIELD_NUMBER: _ClassVar[int]
    VIA_GAP_FIELD_NUMBER: _ClassVar[int]
    width: _base_types_pb2.Distance
    gap: _base_types_pb2.Distance
    via_gap: _base_types_pb2.Distance
    def __init__(self, width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., gap: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., via_gap: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class PredefinedSizes(_message.Message):
    __slots__ = ("tracks", "vias", "diff_pairs")
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    VIAS_FIELD_NUMBER: _ClassVar[int]
    DIFF_PAIRS_FIELD_NUMBER: _ClassVar[int]
    tracks: _containers.RepeatedCompositeFieldContainer[PresetTrackWidth]
    vias: _containers.RepeatedCompositeFieldContainer[PresetViaDimension]
    diff_pairs: _containers.RepeatedCompositeFieldContainer[PresetDiffPairDimension]
    def __init__(self, tracks: _Optional[_Iterable[_Union[PresetTrackWidth, _Mapping]]] = ..., vias: _Optional[_Iterable[_Union[PresetViaDimension, _Mapping]]] = ..., diff_pairs: _Optional[_Iterable[_Union[PresetDiffPairDimension, _Mapping]]] = ...) -> None: ...

class SolderMaskPasteDefaults(_message.Message):
    __slots__ = ("mask_expansion", "mask_min_width", "mask_to_copper_clearance", "paste_margin", "paste_margin_ratio", "allow_soldermask_bridges_in_footprints")
    MASK_EXPANSION_FIELD_NUMBER: _ClassVar[int]
    MASK_MIN_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MASK_TO_COPPER_CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    PASTE_MARGIN_FIELD_NUMBER: _ClassVar[int]
    PASTE_MARGIN_RATIO_FIELD_NUMBER: _ClassVar[int]
    ALLOW_SOLDERMASK_BRIDGES_IN_FOOTPRINTS_FIELD_NUMBER: _ClassVar[int]
    mask_expansion: _base_types_pb2.Distance
    mask_min_width: _base_types_pb2.Distance
    mask_to_copper_clearance: _base_types_pb2.Distance
    paste_margin: _base_types_pb2.Distance
    paste_margin_ratio: float
    allow_soldermask_bridges_in_footprints: bool
    def __init__(self, mask_expansion: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., mask_min_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., mask_to_copper_clearance: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., paste_margin: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., paste_margin_ratio: _Optional[float] = ..., allow_soldermask_bridges_in_footprints: bool = ...) -> None: ...

class TeardropTargetParams(_message.Message):
    __slots__ = ("enabled", "max_length", "max_width", "best_length_ratio", "best_width_ratio", "width_to_size_filter_ratio", "curved_edges", "allow_two_tracks", "on_pads_in_zones")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_WIDTH_FIELD_NUMBER: _ClassVar[int]
    BEST_LENGTH_RATIO_FIELD_NUMBER: _ClassVar[int]
    BEST_WIDTH_RATIO_FIELD_NUMBER: _ClassVar[int]
    WIDTH_TO_SIZE_FILTER_RATIO_FIELD_NUMBER: _ClassVar[int]
    CURVED_EDGES_FIELD_NUMBER: _ClassVar[int]
    ALLOW_TWO_TRACKS_FIELD_NUMBER: _ClassVar[int]
    ON_PADS_IN_ZONES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    max_length: _base_types_pb2.Distance
    max_width: _base_types_pb2.Distance
    best_length_ratio: float
    best_width_ratio: float
    width_to_size_filter_ratio: float
    curved_edges: bool
    allow_two_tracks: bool
    on_pads_in_zones: bool
    def __init__(self, enabled: bool = ..., max_length: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., max_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., best_length_ratio: _Optional[float] = ..., best_width_ratio: _Optional[float] = ..., width_to_size_filter_ratio: _Optional[float] = ..., curved_edges: bool = ..., allow_two_tracks: bool = ..., on_pads_in_zones: bool = ...) -> None: ...

class TeardropTargetEntry(_message.Message):
    __slots__ = ("target", "params")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    target: TeardropTarget
    params: TeardropTargetParams
    def __init__(self, target: _Optional[_Union[TeardropTarget, str]] = ..., params: _Optional[_Union[TeardropTargetParams, _Mapping]] = ...) -> None: ...

class TeardropDefaults(_message.Message):
    __slots__ = ("target_vias", "target_pth_pads", "target_smd_pads", "target_track_to_track", "use_round_shapes_only", "target_params")
    TARGET_VIAS_FIELD_NUMBER: _ClassVar[int]
    TARGET_PTH_PADS_FIELD_NUMBER: _ClassVar[int]
    TARGET_SMD_PADS_FIELD_NUMBER: _ClassVar[int]
    TARGET_TRACK_TO_TRACK_FIELD_NUMBER: _ClassVar[int]
    USE_ROUND_SHAPES_ONLY_FIELD_NUMBER: _ClassVar[int]
    TARGET_PARAMS_FIELD_NUMBER: _ClassVar[int]
    target_vias: bool
    target_pth_pads: bool
    target_smd_pads: bool
    target_track_to_track: bool
    use_round_shapes_only: bool
    target_params: _containers.RepeatedCompositeFieldContainer[TeardropTargetEntry]
    def __init__(self, target_vias: bool = ..., target_pth_pads: bool = ..., target_smd_pads: bool = ..., target_track_to_track: bool = ..., use_round_shapes_only: bool = ..., target_params: _Optional[_Iterable[_Union[TeardropTargetEntry, _Mapping]]] = ...) -> None: ...

class ViaProtectionDefaults(_message.Message):
    __slots__ = ("tent_front", "tent_back", "cover_front", "cover_back", "plug_front", "plug_back", "cap", "fill")
    TENT_FRONT_FIELD_NUMBER: _ClassVar[int]
    TENT_BACK_FIELD_NUMBER: _ClassVar[int]
    COVER_FRONT_FIELD_NUMBER: _ClassVar[int]
    COVER_BACK_FIELD_NUMBER: _ClassVar[int]
    PLUG_FRONT_FIELD_NUMBER: _ClassVar[int]
    PLUG_BACK_FIELD_NUMBER: _ClassVar[int]
    CAP_FIELD_NUMBER: _ClassVar[int]
    FILL_FIELD_NUMBER: _ClassVar[int]
    tent_front: bool
    tent_back: bool
    cover_front: bool
    cover_back: bool
    plug_front: bool
    plug_back: bool
    cap: bool
    fill: bool
    def __init__(self, tent_front: bool = ..., tent_back: bool = ..., cover_front: bool = ..., cover_back: bool = ..., plug_front: bool = ..., plug_back: bool = ..., cap: bool = ..., fill: bool = ...) -> None: ...

class DrcSeveritySetting(_message.Message):
    __slots__ = ("rule_type", "severity")
    RULE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    rule_type: DrcErrorType
    severity: _base_types_pb2.RuleSeverity
    def __init__(self, rule_type: _Optional[_Union[DrcErrorType, str]] = ..., severity: _Optional[_Union[_base_types_pb2.RuleSeverity, str]] = ...) -> None: ...

class DrcExclusion(_message.Message):
    __slots__ = ("marker", "comment")
    MARKER_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    marker: _base_types_pb2.RuleCheckerMarker
    comment: str
    def __init__(self, marker: _Optional[_Union[_base_types_pb2.RuleCheckerMarker, _Mapping]] = ..., comment: _Optional[str] = ...) -> None: ...

class CustomRuleDisallowSettings(_message.Message):
    __slots__ = ("types",)
    TYPES_FIELD_NUMBER: _ClassVar[int]
    types: _containers.RepeatedScalarFieldContainer[CustomRuleDisallowType]
    def __init__(self, types: _Optional[_Iterable[_Union[CustomRuleDisallowType, str]]] = ...) -> None: ...

class CustomRuleConstraint(_message.Message):
    __slots__ = ("type", "name", "numeric", "disallow", "zone_connection", "assertion_expression", "options")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUMERIC_FIELD_NUMBER: _ClassVar[int]
    DISALLOW_FIELD_NUMBER: _ClassVar[int]
    ZONE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    ASSERTION_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    type: CustomRuleConstraintType
    name: str
    numeric: _base_types_pb2.MinOptMax
    disallow: CustomRuleDisallowSettings
    zone_connection: _board_types_pb2.ZoneConnectionStyle
    assertion_expression: str
    options: _containers.RepeatedScalarFieldContainer[CustomRuleConstraintOption]
    def __init__(self, type: _Optional[_Union[CustomRuleConstraintType, str]] = ..., name: _Optional[str] = ..., numeric: _Optional[_Union[_base_types_pb2.MinOptMax, _Mapping]] = ..., disallow: _Optional[_Union[CustomRuleDisallowSettings, _Mapping]] = ..., zone_connection: _Optional[_Union[_board_types_pb2.ZoneConnectionStyle, str]] = ..., assertion_expression: _Optional[str] = ..., options: _Optional[_Iterable[_Union[CustomRuleConstraintOption, str]]] = ...) -> None: ...

class CustomRule(_message.Message):
    __slots__ = ("condition", "constraints", "single_layer", "layer_mode", "severity", "name", "comments")
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    SINGLE_LAYER_FIELD_NUMBER: _ClassVar[int]
    LAYER_MODE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    condition: str
    constraints: _containers.RepeatedCompositeFieldContainer[CustomRuleConstraint]
    single_layer: _board_types_pb2.BoardLayer
    layer_mode: CustomRuleLayerMode
    severity: _base_types_pb2.RuleSeverity
    name: str
    comments: str
    def __init__(self, condition: _Optional[str] = ..., constraints: _Optional[_Iterable[_Union[CustomRuleConstraint, _Mapping]]] = ..., single_layer: _Optional[_Union[_board_types_pb2.BoardLayer, str]] = ..., layer_mode: _Optional[_Union[CustomRuleLayerMode, str]] = ..., severity: _Optional[_Union[_base_types_pb2.RuleSeverity, str]] = ..., name: _Optional[str] = ..., comments: _Optional[str] = ...) -> None: ...

class BoardDesignRules(_message.Message):
    __slots__ = ("constraints", "predefined_sizes", "solder_mask_paste", "teardrops", "via_protection", "severities", "exclusions")
    CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    PREDEFINED_SIZES_FIELD_NUMBER: _ClassVar[int]
    SOLDER_MASK_PASTE_FIELD_NUMBER: _ClassVar[int]
    TEARDROPS_FIELD_NUMBER: _ClassVar[int]
    VIA_PROTECTION_FIELD_NUMBER: _ClassVar[int]
    SEVERITIES_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIONS_FIELD_NUMBER: _ClassVar[int]
    constraints: MinimumConstraints
    predefined_sizes: PredefinedSizes
    solder_mask_paste: SolderMaskPasteDefaults
    teardrops: TeardropDefaults
    via_protection: ViaProtectionDefaults
    severities: _containers.RepeatedCompositeFieldContainer[DrcSeveritySetting]
    exclusions: _containers.RepeatedCompositeFieldContainer[DrcExclusion]
    def __init__(self, constraints: _Optional[_Union[MinimumConstraints, _Mapping]] = ..., predefined_sizes: _Optional[_Union[PredefinedSizes, _Mapping]] = ..., solder_mask_paste: _Optional[_Union[SolderMaskPasteDefaults, _Mapping]] = ..., teardrops: _Optional[_Union[TeardropDefaults, _Mapping]] = ..., via_protection: _Optional[_Union[ViaProtectionDefaults, _Mapping]] = ..., severities: _Optional[_Iterable[_Union[DrcSeveritySetting, _Mapping]]] = ..., exclusions: _Optional[_Iterable[_Union[DrcExclusion, _Mapping]]] = ...) -> None: ...
