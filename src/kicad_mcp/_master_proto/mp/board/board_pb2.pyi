from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.board import board_types_pb2 as _board_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoardEdgeConnectorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BECT_UNKNOWN: _ClassVar[BoardEdgeConnectorType]
    BECT_NONE: _ClassVar[BoardEdgeConnectorType]
    BECT_PLAIN: _ClassVar[BoardEdgeConnectorType]
    BECT_BEVELED: _ClassVar[BoardEdgeConnectorType]

class BoardStackupDielectricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BSDT_UNKNOWN: _ClassVar[BoardStackupDielectricType]
    BSDT_NONE: _ClassVar[BoardStackupDielectricType]
    BSDT_CORE: _ClassVar[BoardStackupDielectricType]
    BSDT_PREPREG: _ClassVar[BoardStackupDielectricType]

class DielectricModel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DM_UNKNOWN: _ClassVar[DielectricModel]
    DM_CONSTANT: _ClassVar[DielectricModel]
    DM_DJORDJEVIC_SARKAR: _ClassVar[DielectricModel]

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
BECT_UNKNOWN: BoardEdgeConnectorType
BECT_NONE: BoardEdgeConnectorType
BECT_PLAIN: BoardEdgeConnectorType
BECT_BEVELED: BoardEdgeConnectorType
BSDT_UNKNOWN: BoardStackupDielectricType
BSDT_NONE: BoardStackupDielectricType
BSDT_CORE: BoardStackupDielectricType
BSDT_PREPREG: BoardStackupDielectricType
DM_UNKNOWN: DielectricModel
DM_CONSTANT: DielectricModel
DM_DJORDJEVIC_SARKAR: DielectricModel
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

class Castellation(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BoardEdgeConnector(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: BoardEdgeConnectorType
    def __init__(self, type: _Optional[_Union[BoardEdgeConnectorType, str]] = ...) -> None: ...

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

class BoardStackupDielectricProperties(_message.Message):
    __slots__ = ("epsilon_r", "loss_tangent", "material_name", "thickness", "thickness_locked", "spec_frequency", "dielectric_model")
    EPSILON_R_FIELD_NUMBER: _ClassVar[int]
    LOSS_TANGENT_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_LOCKED_FIELD_NUMBER: _ClassVar[int]
    SPEC_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    DIELECTRIC_MODEL_FIELD_NUMBER: _ClassVar[int]
    epsilon_r: float
    loss_tangent: float
    material_name: str
    thickness: _base_types_pb2.Distance
    thickness_locked: bool
    spec_frequency: float
    dielectric_model: DielectricModel
    def __init__(self, epsilon_r: _Optional[float] = ..., loss_tangent: _Optional[float] = ..., material_name: _Optional[str] = ..., thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., thickness_locked: bool = ..., spec_frequency: _Optional[float] = ..., dielectric_model: _Optional[_Union[DielectricModel, str]] = ...) -> None: ...

class BoardStackupDielectricLayer(_message.Message):
    __slots__ = ("layer", "type")
    LAYER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    layer: _containers.RepeatedCompositeFieldContainer[BoardStackupDielectricProperties]
    type: BoardStackupDielectricType
    def __init__(self, layer: _Optional[_Iterable[_Union[BoardStackupDielectricProperties, _Mapping]]] = ..., type: _Optional[_Union[BoardStackupDielectricType, str]] = ...) -> None: ...

class BoardStackupSoldermaskLayer(_message.Message):
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

class BoardStackupSilkscreenLayer(_message.Message):
    __slots__ = ("material_name",)
    MATERIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    material_name: str
    def __init__(self, material_name: _Optional[str] = ...) -> None: ...

class BoardStackupLayer(_message.Message):
    __slots__ = ("thickness", "layer", "enabled", "type", "dielectric", "soldermask", "silkscreen", "color", "material_name", "user_name")
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DIELECTRIC_FIELD_NUMBER: _ClassVar[int]
    SOLDERMASK_FIELD_NUMBER: _ClassVar[int]
    SILKSCREEN_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    thickness: _base_types_pb2.Distance
    layer: _board_types_pb2.BoardLayer
    enabled: bool
    type: BoardStackupLayerType
    dielectric: BoardStackupDielectricLayer
    soldermask: BoardStackupSoldermaskLayer
    silkscreen: BoardStackupSilkscreenLayer
    color: _base_types_pb2.Color
    material_name: str
    user_name: str
    def __init__(self, thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., layer: _Optional[_Union[_board_types_pb2.BoardLayer, str]] = ..., enabled: bool = ..., type: _Optional[_Union[BoardStackupLayerType, str]] = ..., dielectric: _Optional[_Union[BoardStackupDielectricLayer, _Mapping]] = ..., soldermask: _Optional[_Union[BoardStackupSoldermaskLayer, _Mapping]] = ..., silkscreen: _Optional[_Union[BoardStackupSilkscreenLayer, _Mapping]] = ..., color: _Optional[_Union[_base_types_pb2.Color, _Mapping]] = ..., material_name: _Optional[str] = ..., user_name: _Optional[str] = ...) -> None: ...

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
