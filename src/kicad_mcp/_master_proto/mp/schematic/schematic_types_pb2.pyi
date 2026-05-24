from google.protobuf import any_pb2 as _any_pb2
from mp.common.types import base_types_pb2 as _base_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SchematicLineType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SLT_UNKNOWN: _ClassVar[SchematicLineType]
    SLT_WIRE: _ClassVar[SchematicLineType]
    SLT_BUS: _ClassVar[SchematicLineType]
    SLT_GRAPHIC: _ClassVar[SchematicLineType]

class BusEntryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BET_UNKNOWN: _ClassVar[BusEntryType]
    BET_WIRE_TO_BUS: _ClassVar[BusEntryType]
    BET_BUS_TO_BUS: _ClassVar[BusEntryType]

class SchematicLabelShape(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SLSH_UNKNOWN: _ClassVar[SchematicLabelShape]
    SLSH_INPUT: _ClassVar[SchematicLabelShape]
    SLSH_OUTPUT: _ClassVar[SchematicLabelShape]
    SLSH_BIDI: _ClassVar[SchematicLabelShape]
    SLSH_TRISTATE: _ClassVar[SchematicLabelShape]
    SLSH_PASSIVE: _ClassVar[SchematicLabelShape]
    SLSH_DOT: _ClassVar[SchematicLabelShape]
    SLSH_CIRCLE: _ClassVar[SchematicLabelShape]
    SLSH_DIAMOND: _ClassVar[SchematicLabelShape]
    SLSH_RECTANGLE: _ClassVar[SchematicLabelShape]

class SchematicLabelSpinStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SLSS_UNKNOWN: _ClassVar[SchematicLabelSpinStyle]
    SLSS_LEFT: _ClassVar[SchematicLabelSpinStyle]
    SLSS_UP: _ClassVar[SchematicLabelSpinStyle]
    SLSS_RIGHT: _ClassVar[SchematicLabelSpinStyle]
    SLSS_BOTTOM: _ClassVar[SchematicLabelSpinStyle]

class SheetSide(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SHS_UNKNOWN: _ClassVar[SheetSide]
    SHS_LEFT: _ClassVar[SheetSide]
    SHS_RIGHT: _ClassVar[SheetSide]
    SHS_TOP: _ClassVar[SheetSide]
    SHS_BOTTOM: _ClassVar[SheetSide]

class SchematicSymbolType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SST_UNKNOWN: _ClassVar[SchematicSymbolType]
    SST_NORMAL: _ClassVar[SchematicSymbolType]
    SST_GLOBAL_POWER: _ClassVar[SchematicSymbolType]
    SST_LOCAL_POWER: _ClassVar[SchematicSymbolType]

class SchematicSymbolOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SSO_UNKNOWN: _ClassVar[SchematicSymbolOrientation]
    SSO_0: _ClassVar[SchematicSymbolOrientation]
    SSO_90: _ClassVar[SchematicSymbolOrientation]
    SSO_180: _ClassVar[SchematicSymbolOrientation]
    SSO_270: _ClassVar[SchematicSymbolOrientation]

class SchematicPinOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPO_UNKNOWN: _ClassVar[SchematicPinOrientation]
    SPO_RIGHT: _ClassVar[SchematicPinOrientation]
    SPO_LEFT: _ClassVar[SchematicPinOrientation]
    SPO_UP: _ClassVar[SchematicPinOrientation]
    SPO_DOWN: _ClassVar[SchematicPinOrientation]

class SchematicPinShape(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPS_UNKNOWN: _ClassVar[SchematicPinShape]
    SPS_LINE: _ClassVar[SchematicPinShape]
    SPS_INVERTED: _ClassVar[SchematicPinShape]
    SPS_CLOCK: _ClassVar[SchematicPinShape]
    SPS_INVERTED_CLOCK: _ClassVar[SchematicPinShape]
    SPS_INPUT_LOW: _ClassVar[SchematicPinShape]
    SPS_CLOCK_LOW: _ClassVar[SchematicPinShape]
    SPS_OUTPUT_LOW: _ClassVar[SchematicPinShape]
    SPS_FALLING_EDGE_CLOCK: _ClassVar[SchematicPinShape]
    SPS_NONLOGIC: _ClassVar[SchematicPinShape]
SLT_UNKNOWN: SchematicLineType
SLT_WIRE: SchematicLineType
SLT_BUS: SchematicLineType
SLT_GRAPHIC: SchematicLineType
BET_UNKNOWN: BusEntryType
BET_WIRE_TO_BUS: BusEntryType
BET_BUS_TO_BUS: BusEntryType
SLSH_UNKNOWN: SchematicLabelShape
SLSH_INPUT: SchematicLabelShape
SLSH_OUTPUT: SchematicLabelShape
SLSH_BIDI: SchematicLabelShape
SLSH_TRISTATE: SchematicLabelShape
SLSH_PASSIVE: SchematicLabelShape
SLSH_DOT: SchematicLabelShape
SLSH_CIRCLE: SchematicLabelShape
SLSH_DIAMOND: SchematicLabelShape
SLSH_RECTANGLE: SchematicLabelShape
SLSS_UNKNOWN: SchematicLabelSpinStyle
SLSS_LEFT: SchematicLabelSpinStyle
SLSS_UP: SchematicLabelSpinStyle
SLSS_RIGHT: SchematicLabelSpinStyle
SLSS_BOTTOM: SchematicLabelSpinStyle
SHS_UNKNOWN: SheetSide
SHS_LEFT: SheetSide
SHS_RIGHT: SheetSide
SHS_TOP: SheetSide
SHS_BOTTOM: SheetSide
SST_UNKNOWN: SchematicSymbolType
SST_NORMAL: SchematicSymbolType
SST_GLOBAL_POWER: SchematicSymbolType
SST_LOCAL_POWER: SchematicSymbolType
SSO_UNKNOWN: SchematicSymbolOrientation
SSO_0: SchematicSymbolOrientation
SSO_90: SchematicSymbolOrientation
SSO_180: SchematicSymbolOrientation
SSO_270: SchematicSymbolOrientation
SPO_UNKNOWN: SchematicPinOrientation
SPO_RIGHT: SchematicPinOrientation
SPO_LEFT: SchematicPinOrientation
SPO_UP: SchematicPinOrientation
SPO_DOWN: SchematicPinOrientation
SPS_UNKNOWN: SchematicPinShape
SPS_LINE: SchematicPinShape
SPS_INVERTED: SchematicPinShape
SPS_CLOCK: SchematicPinShape
SPS_INVERTED_CLOCK: SchematicPinShape
SPS_INPUT_LOW: SchematicPinShape
SPS_CLOCK_LOW: SchematicPinShape
SPS_OUTPUT_LOW: SchematicPinShape
SPS_FALLING_EDGE_CLOCK: SchematicPinShape
SPS_NONLOGIC: SchematicPinShape

class SchematicField(_message.Message):
    __slots__ = ("name", "text", "visible", "show_name", "allow_auto_place", "is_private")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    SHOW_NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOW_AUTO_PLACE_FIELD_NUMBER: _ClassVar[int]
    IS_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    text: _base_types_pb2.Text
    visible: bool
    show_name: bool
    allow_auto_place: bool
    is_private: bool
    def __init__(self, name: _Optional[str] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., visible: bool = ..., show_name: bool = ..., allow_auto_place: bool = ..., is_private: bool = ...) -> None: ...

class SchematicLine(_message.Message):
    __slots__ = ("id", "start", "end", "type", "stroke", "locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STROKE_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    start: _base_types_pb2.Vector2
    end: _base_types_pb2.Vector2
    type: SchematicLineType
    stroke: _base_types_pb2.StrokeAttributes
    locked: _base_types_pb2.LockedState
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., start: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., end: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., type: _Optional[_Union[SchematicLineType, str]] = ..., stroke: _Optional[_Union[_base_types_pb2.StrokeAttributes, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class Junction(_message.Message):
    __slots__ = ("id", "position", "diameter", "color", "locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DIAMETER_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    diameter: _base_types_pb2.Distance
    color: _base_types_pb2.Color
    locked: _base_types_pb2.LockedState
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., diameter: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., color: _Optional[_Union[_base_types_pb2.Color, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class NoConnectMarker(_message.Message):
    __slots__ = ("id", "position", "size", "locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    size: _base_types_pb2.Distance
    locked: _base_types_pb2.LockedState
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class BusEntry(_message.Message):
    __slots__ = ("id", "position", "size", "stroke", "locked", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    STROKE_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    size: _base_types_pb2.Vector2
    stroke: _base_types_pb2.StrokeAttributes
    locked: _base_types_pb2.LockedState
    type: BusEntryType
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., size: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., stroke: _Optional[_Union[_base_types_pb2.StrokeAttributes, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., type: _Optional[_Union[BusEntryType, str]] = ...) -> None: ...

class SchematicText(_message.Message):
    __slots__ = ("id", "text", "locked", "exclude_from_sim")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_SIM_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    text: _base_types_pb2.Text
    locked: _base_types_pb2.LockedState
    exclude_from_sim: bool
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., exclude_from_sim: bool = ...) -> None: ...

class SchematicTextBox(_message.Message):
    __slots__ = ("id", "textbox", "graphic_attributes", "locked", "exclude_from_sim", "margin_left", "margin_top", "margin_right", "margin_bottom")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEXTBOX_FIELD_NUMBER: _ClassVar[int]
    GRAPHIC_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_SIM_FIELD_NUMBER: _ClassVar[int]
    MARGIN_LEFT_FIELD_NUMBER: _ClassVar[int]
    MARGIN_TOP_FIELD_NUMBER: _ClassVar[int]
    MARGIN_RIGHT_FIELD_NUMBER: _ClassVar[int]
    MARGIN_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    textbox: _base_types_pb2.TextBox
    graphic_attributes: _base_types_pb2.GraphicAttributes
    locked: _base_types_pb2.LockedState
    exclude_from_sim: bool
    margin_left: _base_types_pb2.Distance
    margin_top: _base_types_pb2.Distance
    margin_right: _base_types_pb2.Distance
    margin_bottom: _base_types_pb2.Distance
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., textbox: _Optional[_Union[_base_types_pb2.TextBox, _Mapping]] = ..., graphic_attributes: _Optional[_Union[_base_types_pb2.GraphicAttributes, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., exclude_from_sim: bool = ..., margin_left: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., margin_top: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., margin_right: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., margin_bottom: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class SchematicGraphicShape(_message.Message):
    __slots__ = ("shape", "id", "locked")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    shape: _base_types_pb2.GraphicShape
    id: _base_types_pb2.KIID
    locked: _base_types_pb2.LockedState
    def __init__(self, shape: _Optional[_Union[_base_types_pb2.GraphicShape, _Mapping]] = ..., id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class SchematicImage(_message.Message):
    __slots__ = ("id", "position", "transform_origin_offset", "image_scale", "image_data", "locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_ORIGIN_OFFSET_FIELD_NUMBER: _ClassVar[int]
    IMAGE_SCALE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    transform_origin_offset: _base_types_pb2.Vector2
    image_scale: _base_types_pb2.Ratio
    image_data: bytes
    locked: _base_types_pb2.LockedState
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., transform_origin_offset: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., image_scale: _Optional[_Union[_base_types_pb2.Ratio, _Mapping]] = ..., image_data: _Optional[bytes] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class LocalLabel(_message.Message):
    __slots__ = ("id", "position", "text", "spin_style", "fields", "locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SPIN_STYLE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    text: _base_types_pb2.Text
    spin_style: SchematicLabelSpinStyle
    fields: _containers.RepeatedCompositeFieldContainer[SchematicField]
    locked: _base_types_pb2.LockedState
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., spin_style: _Optional[_Union[SchematicLabelSpinStyle, str]] = ..., fields: _Optional[_Iterable[_Union[SchematicField, _Mapping]]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class GlobalLabel(_message.Message):
    __slots__ = ("id", "position", "text", "spin_style", "shape", "fields", "locked", "intersheet_refs_field")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SPIN_STYLE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    INTERSHEET_REFS_FIELD_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    text: _base_types_pb2.Text
    spin_style: SchematicLabelSpinStyle
    shape: SchematicLabelShape
    fields: _containers.RepeatedCompositeFieldContainer[SchematicField]
    locked: _base_types_pb2.LockedState
    intersheet_refs_field: SchematicField
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., spin_style: _Optional[_Union[SchematicLabelSpinStyle, str]] = ..., shape: _Optional[_Union[SchematicLabelShape, str]] = ..., fields: _Optional[_Iterable[_Union[SchematicField, _Mapping]]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., intersheet_refs_field: _Optional[_Union[SchematicField, _Mapping]] = ...) -> None: ...

class HierarchicalLabel(_message.Message):
    __slots__ = ("id", "position", "text", "spin_style", "shape", "fields", "locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SPIN_STYLE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    text: _base_types_pb2.Text
    spin_style: SchematicLabelSpinStyle
    shape: SchematicLabelShape
    fields: _containers.RepeatedCompositeFieldContainer[SchematicField]
    locked: _base_types_pb2.LockedState
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., spin_style: _Optional[_Union[SchematicLabelSpinStyle, str]] = ..., shape: _Optional[_Union[SchematicLabelShape, str]] = ..., fields: _Optional[_Iterable[_Union[SchematicField, _Mapping]]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class DirectiveLabel(_message.Message):
    __slots__ = ("id", "position", "text", "spin_style", "shape", "fields", "locked", "pin_length", "symbol_size")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SPIN_STYLE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PIN_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_SIZE_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    text: _base_types_pb2.Text
    spin_style: SchematicLabelSpinStyle
    shape: SchematicLabelShape
    fields: _containers.RepeatedCompositeFieldContainer[SchematicField]
    locked: _base_types_pb2.LockedState
    pin_length: _base_types_pb2.Distance
    symbol_size: _base_types_pb2.Distance
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., spin_style: _Optional[_Union[SchematicLabelSpinStyle, str]] = ..., shape: _Optional[_Union[SchematicLabelShape, str]] = ..., fields: _Optional[_Iterable[_Union[SchematicField, _Mapping]]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., pin_length: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., symbol_size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ("id", "name", "items", "locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    name: str
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    locked: _base_types_pb2.LockedState
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., name: _Optional[str] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class SheetPin(_message.Message):
    __slots__ = ("id", "position", "text", "spin_style", "shape", "side", "locked")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SPIN_STYLE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    text: _base_types_pb2.Text
    spin_style: SchematicLabelSpinStyle
    shape: SchematicLabelShape
    side: SheetSide
    locked: _base_types_pb2.LockedState
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., spin_style: _Optional[_Union[SchematicLabelSpinStyle, str]] = ..., shape: _Optional[_Union[SchematicLabelShape, str]] = ..., side: _Optional[_Union[SheetSide, str]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ...) -> None: ...

class SheetSymbol(_message.Message):
    __slots__ = ("id", "position", "size", "border_stroke", "fill", "locked", "name_field", "filename_field", "user_fields", "pins", "exclude_from_sim", "exclude_from_bom", "exclude_from_board", "dnp", "path", "page_number")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    BORDER_STROKE_FIELD_NUMBER: _ClassVar[int]
    FILL_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_FIELD_NUMBER: _ClassVar[int]
    USER_FIELDS_FIELD_NUMBER: _ClassVar[int]
    PINS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_SIM_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_BOM_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_BOARD_FIELD_NUMBER: _ClassVar[int]
    DNP_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    size: _base_types_pb2.Vector2
    border_stroke: _base_types_pb2.StrokeAttributes
    fill: _base_types_pb2.GraphicFillAttributes
    locked: _base_types_pb2.LockedState
    name_field: SchematicField
    filename_field: SchematicField
    user_fields: _containers.RepeatedCompositeFieldContainer[SchematicField]
    pins: _containers.RepeatedCompositeFieldContainer[SheetPin]
    exclude_from_sim: bool
    exclude_from_bom: bool
    exclude_from_board: bool
    dnp: bool
    path: _base_types_pb2.SheetPath
    page_number: str
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., size: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., border_stroke: _Optional[_Union[_base_types_pb2.StrokeAttributes, _Mapping]] = ..., fill: _Optional[_Union[_base_types_pb2.GraphicFillAttributes, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., name_field: _Optional[_Union[SchematicField, _Mapping]] = ..., filename_field: _Optional[_Union[SchematicField, _Mapping]] = ..., user_fields: _Optional[_Iterable[_Union[SchematicField, _Mapping]]] = ..., pins: _Optional[_Iterable[_Union[SheetPin, _Mapping]]] = ..., exclude_from_sim: bool = ..., exclude_from_bom: bool = ..., exclude_from_board: bool = ..., dnp: bool = ..., path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ..., page_number: _Optional[str] = ...) -> None: ...

class SchematicPinAlternate(_message.Message):
    __slots__ = ("name", "shape", "electrical_type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    ELECTRICAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    shape: SchematicPinShape
    electrical_type: _base_types_pb2.ElectricalPinType
    def __init__(self, name: _Optional[str] = ..., shape: _Optional[_Union[SchematicPinShape, str]] = ..., electrical_type: _Optional[_Union[_base_types_pb2.ElectricalPinType, str]] = ...) -> None: ...

class SchematicPin(_message.Message):
    __slots__ = ("id", "name", "number", "position", "length", "orientation", "electrical_type", "shape", "visible", "name_text_size", "number_text_size", "alternates", "active_alternate")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    ELECTRICAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    NAME_TEXT_SIZE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_TEXT_SIZE_FIELD_NUMBER: _ClassVar[int]
    ALTERNATES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ALTERNATE_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    name: str
    number: str
    position: _base_types_pb2.Vector2
    length: _base_types_pb2.Distance
    orientation: SchematicPinOrientation
    electrical_type: _base_types_pb2.ElectricalPinType
    shape: SchematicPinShape
    visible: bool
    name_text_size: _base_types_pb2.Distance
    number_text_size: _base_types_pb2.Distance
    alternates: _containers.RepeatedCompositeFieldContainer[SchematicPinAlternate]
    active_alternate: str
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., name: _Optional[str] = ..., number: _Optional[str] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., length: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., orientation: _Optional[_Union[SchematicPinOrientation, str]] = ..., electrical_type: _Optional[_Union[_base_types_pb2.ElectricalPinType, str]] = ..., shape: _Optional[_Union[SchematicPinShape, str]] = ..., visible: bool = ..., name_text_size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., number_text_size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., alternates: _Optional[_Iterable[_Union[SchematicPinAlternate, _Mapping]]] = ..., active_alternate: _Optional[str] = ...) -> None: ...

class SchematicSymbolUnit(_message.Message):
    __slots__ = ("unit",)
    UNIT_FIELD_NUMBER: _ClassVar[int]
    unit: int
    def __init__(self, unit: _Optional[int] = ...) -> None: ...

class SchematicSymbolBodyStyle(_message.Message):
    __slots__ = ("style",)
    STYLE_FIELD_NUMBER: _ClassVar[int]
    style: int
    def __init__(self, style: _Optional[int] = ...) -> None: ...

class SchematicSymbolChild(_message.Message):
    __slots__ = ("item", "unit", "body_style", "is_private")
    ITEM_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    BODY_STYLE_FIELD_NUMBER: _ClassVar[int]
    IS_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    item: _any_pb2.Any
    unit: SchematicSymbolUnit
    body_style: SchematicSymbolBodyStyle
    is_private: bool
    def __init__(self, item: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., unit: _Optional[_Union[SchematicSymbolUnit, _Mapping]] = ..., body_style: _Optional[_Union[SchematicSymbolBodyStyle, _Mapping]] = ..., is_private: bool = ...) -> None: ...

class SchematicSymbolAttributes(_message.Message):
    __slots__ = ("exclude_from_simulation", "exclude_from_bill_of_materials", "exclude_from_board", "exclude_from_position_files", "do_not_populate")
    EXCLUDE_FROM_SIMULATION_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_BILL_OF_MATERIALS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_BOARD_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_POSITION_FILES_FIELD_NUMBER: _ClassVar[int]
    DO_NOT_POPULATE_FIELD_NUMBER: _ClassVar[int]
    exclude_from_simulation: bool
    exclude_from_bill_of_materials: bool
    exclude_from_board: bool
    exclude_from_position_files: bool
    do_not_populate: bool
    def __init__(self, exclude_from_simulation: bool = ..., exclude_from_bill_of_materials: bool = ..., exclude_from_board: bool = ..., exclude_from_position_files: bool = ..., do_not_populate: bool = ...) -> None: ...

class SchematicSymbolVariant(_message.Message):
    __slots__ = ("name", "description", "attributes", "fields")
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    attributes: SchematicSymbolAttributes
    fields: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., attributes: _Optional[_Union[SchematicSymbolAttributes, _Mapping]] = ..., fields: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SchematicSymbol(_message.Message):
    __slots__ = ("id", "type", "attributes", "reference_field", "value_field", "footprint_field", "datasheet_field", "description_field", "items", "unit_count", "body_style_count", "keywords", "footprint_filters")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_FIELD_NUMBER: _ClassVar[int]
    FOOTPRINT_FIELD_FIELD_NUMBER: _ClassVar[int]
    DATASHEET_FIELD_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    UNIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    BODY_STYLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    FOOTPRINT_FILTERS_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.LibraryIdentifier
    type: SchematicSymbolType
    attributes: SchematicSymbolAttributes
    reference_field: SchematicField
    value_field: SchematicField
    footprint_field: SchematicField
    datasheet_field: SchematicField
    description_field: SchematicField
    items: _containers.RepeatedCompositeFieldContainer[SchematicSymbolChild]
    unit_count: int
    body_style_count: int
    keywords: str
    footprint_filters: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]] = ..., type: _Optional[_Union[SchematicSymbolType, str]] = ..., attributes: _Optional[_Union[SchematicSymbolAttributes, _Mapping]] = ..., reference_field: _Optional[_Union[SchematicField, _Mapping]] = ..., value_field: _Optional[_Union[SchematicField, _Mapping]] = ..., footprint_field: _Optional[_Union[SchematicField, _Mapping]] = ..., datasheet_field: _Optional[_Union[SchematicField, _Mapping]] = ..., description_field: _Optional[_Union[SchematicField, _Mapping]] = ..., items: _Optional[_Iterable[_Union[SchematicSymbolChild, _Mapping]]] = ..., unit_count: _Optional[int] = ..., body_style_count: _Optional[int] = ..., keywords: _Optional[str] = ..., footprint_filters: _Optional[_Iterable[str]] = ...) -> None: ...

class SchematicSymbolTransform(_message.Message):
    __slots__ = ("orientation", "mirror_x", "mirror_y")
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    MIRROR_X_FIELD_NUMBER: _ClassVar[int]
    MIRROR_Y_FIELD_NUMBER: _ClassVar[int]
    orientation: SchematicSymbolOrientation
    mirror_x: bool
    mirror_y: bool
    def __init__(self, orientation: _Optional[_Union[SchematicSymbolOrientation, str]] = ..., mirror_x: bool = ..., mirror_y: bool = ...) -> None: ...

class SchematicSymbolInstance(_message.Message):
    __slots__ = ("id", "path", "position", "transform", "locked", "definition", "reference_field", "value_field", "footprint_field", "datasheet_field", "description_field", "attributes", "unit", "body_style", "show_pin_names", "show_pin_numbers", "pin_name_offset", "variants")
    ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_FIELD_NUMBER: _ClassVar[int]
    FOOTPRINT_FIELD_FIELD_NUMBER: _ClassVar[int]
    DATASHEET_FIELD_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    BODY_STYLE_FIELD_NUMBER: _ClassVar[int]
    SHOW_PIN_NAMES_FIELD_NUMBER: _ClassVar[int]
    SHOW_PIN_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    PIN_NAME_OFFSET_FIELD_NUMBER: _ClassVar[int]
    VARIANTS_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    path: _base_types_pb2.SheetPath
    position: _base_types_pb2.Vector2
    transform: SchematicSymbolTransform
    locked: _base_types_pb2.LockedState
    definition: SchematicSymbol
    reference_field: SchematicField
    value_field: SchematicField
    footprint_field: SchematicField
    datasheet_field: SchematicField
    description_field: SchematicField
    attributes: SchematicSymbolAttributes
    unit: SchematicSymbolUnit
    body_style: SchematicSymbolBodyStyle
    show_pin_names: bool
    show_pin_numbers: bool
    pin_name_offset: _base_types_pb2.Distance
    variants: _containers.RepeatedCompositeFieldContainer[SchematicSymbolVariant]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., transform: _Optional[_Union[SchematicSymbolTransform, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., definition: _Optional[_Union[SchematicSymbol, _Mapping]] = ..., reference_field: _Optional[_Union[SchematicField, _Mapping]] = ..., value_field: _Optional[_Union[SchematicField, _Mapping]] = ..., footprint_field: _Optional[_Union[SchematicField, _Mapping]] = ..., datasheet_field: _Optional[_Union[SchematicField, _Mapping]] = ..., description_field: _Optional[_Union[SchematicField, _Mapping]] = ..., attributes: _Optional[_Union[SchematicSymbolAttributes, _Mapping]] = ..., unit: _Optional[_Union[SchematicSymbolUnit, _Mapping]] = ..., body_style: _Optional[_Union[SchematicSymbolBodyStyle, _Mapping]] = ..., show_pin_names: bool = ..., show_pin_numbers: bool = ..., pin_name_offset: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., variants: _Optional[_Iterable[_Union[SchematicSymbolVariant, _Mapping]]] = ...) -> None: ...

class SheetInstance(_message.Message):
    __slots__ = ("path", "name", "filename", "page_number", "children")
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    path: _base_types_pb2.SheetPath
    name: str
    filename: str
    page_number: str
    children: _containers.RepeatedCompositeFieldContainer[SheetInstance]
    def __init__(self, path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ..., name: _Optional[str] = ..., filename: _Optional[str] = ..., page_number: _Optional[str] = ..., children: _Optional[_Iterable[_Union[SheetInstance, _Mapping]]] = ...) -> None: ...

class SchematicNetSheetContents(_message.Message):
    __slots__ = ("path", "items")
    PATH_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    path: _base_types_pb2.SheetPath
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    def __init__(self, path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ...) -> None: ...

class SchematicNet(_message.Message):
    __slots__ = ("name", "sheets")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHEETS_FIELD_NUMBER: _ClassVar[int]
    name: str
    sheets: _containers.RepeatedCompositeFieldContainer[SchematicNetSheetContents]
    def __init__(self, name: _Optional[str] = ..., sheets: _Optional[_Iterable[_Union[SchematicNetSheetContents, _Mapping]]] = ...) -> None: ...
