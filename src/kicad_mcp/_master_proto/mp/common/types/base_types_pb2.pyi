from google.protobuf import field_mask_pb2 as _field_mask_pb2
from mp.common.types import enums_pb2 as _enums_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CS_UNKNOWN: _ClassVar[CommandStatus]
    CS_OK: _ClassVar[CommandStatus]
    CS_FAILED: _ClassVar[CommandStatus]

class FrameType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FT_UNKNOWN: _ClassVar[FrameType]
    FT_PROJECT_MANAGER: _ClassVar[FrameType]
    FT_SCHEMATIC_EDITOR: _ClassVar[FrameType]
    FT_PCB_EDITOR: _ClassVar[FrameType]
    FT_SPICE_SIMULATOR: _ClassVar[FrameType]
    FT_SYMBOL_EDITOR: _ClassVar[FrameType]
    FT_FOOTPRINT_EDITOR: _ClassVar[FrameType]
    FT_DRAWING_SHEET_EDITOR: _ClassVar[FrameType]

class DocumentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOCTYPE_UNKNOWN: _ClassVar[DocumentType]
    DOCTYPE_SCHEMATIC: _ClassVar[DocumentType]
    DOCTYPE_SYMBOL: _ClassVar[DocumentType]
    DOCTYPE_PCB: _ClassVar[DocumentType]
    DOCTYPE_FOOTPRINT: _ClassVar[DocumentType]
    DOCTYPE_DRAWING_SHEET: _ClassVar[DocumentType]
    DOCTYPE_PROJECT: _ClassVar[DocumentType]

class ItemRequestStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IRS_UNKNOWN: _ClassVar[ItemRequestStatus]
    IRS_OK: _ClassVar[ItemRequestStatus]
    IRS_DOCUMENT_NOT_FOUND: _ClassVar[ItemRequestStatus]
    IRS_FIELD_MASK_INVALID: _ClassVar[ItemRequestStatus]

class LockedState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LS_UNKNOWN: _ClassVar[LockedState]
    LS_UNLOCKED: _ClassVar[LockedState]
    LS_LOCKED: _ClassVar[LockedState]

class GraphicFillType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GFT_UNKNOWN: _ClassVar[GraphicFillType]
    GFT_UNFILLED: _ClassVar[GraphicFillType]
    GFT_FILLED: _ClassVar[GraphicFillType]
    GFT_FILLED_WITH_COLOR: _ClassVar[GraphicFillType]
    GFT_FILLED_WITH_BACKGROUND_BODY_COLOR: _ClassVar[GraphicFillType]
    GFT_HATCH: _ClassVar[GraphicFillType]
    GFT_REVERSE_HATCH: _ClassVar[GraphicFillType]
    GFT_CROSS_HATCH: _ClassVar[GraphicFillType]

class AxisAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AA_UNKNOWN: _ClassVar[AxisAlignment]
    AA_X_AXIS: _ClassVar[AxisAlignment]
    AA_Y_AXIS: _ClassVar[AxisAlignment]

class MapMergeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MMM_UNKNOWN: _ClassVar[MapMergeMode]
    MMM_MERGE: _ClassVar[MapMergeMode]
    MMM_REPLACE: _ClassVar[MapMergeMode]

class ElectricalPinType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EPT_UNKNOWN: _ClassVar[ElectricalPinType]
    EPT_INPUT: _ClassVar[ElectricalPinType]
    EPT_OUTPUT: _ClassVar[ElectricalPinType]
    EPT_BIDIRECTIONAL: _ClassVar[ElectricalPinType]
    EPT_TRISTATE: _ClassVar[ElectricalPinType]
    EPT_PASSIVE: _ClassVar[ElectricalPinType]
    EPT_FREE: _ClassVar[ElectricalPinType]
    EPT_UNSPECIFIED: _ClassVar[ElectricalPinType]
    EPT_POWER_INPUT: _ClassVar[ElectricalPinType]
    EPT_POWER_OUTPUT: _ClassVar[ElectricalPinType]
    EPT_OPEN_COLLECTOR: _ClassVar[ElectricalPinType]
    EPT_OPEN_EMITTER: _ClassVar[ElectricalPinType]
    EPT_NO_CONNECT: _ClassVar[ElectricalPinType]

class RuleSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RS_UNKNOWN: _ClassVar[RuleSeverity]
    RS_WARNING: _ClassVar[RuleSeverity]
    RS_ERROR: _ClassVar[RuleSeverity]
    RS_EXCLUSION: _ClassVar[RuleSeverity]
    RS_IGNORE: _ClassVar[RuleSeverity]
    RS_INFO: _ClassVar[RuleSeverity]
    RS_ACTION: _ClassVar[RuleSeverity]
    RS_DEBUG: _ClassVar[RuleSeverity]
    RS_UNDEFINED: _ClassVar[RuleSeverity]

class PageSize(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PS_UNKNOWN: _ClassVar[PageSize]
    PS_A5: _ClassVar[PageSize]
    PS_A4: _ClassVar[PageSize]
    PS_A3: _ClassVar[PageSize]
    PS_A2: _ClassVar[PageSize]
    PS_A1: _ClassVar[PageSize]
    PS_A0: _ClassVar[PageSize]
    PS_ANSI_A: _ClassVar[PageSize]
    PS_ANSI_B: _ClassVar[PageSize]
    PS_ANSI_C: _ClassVar[PageSize]
    PS_ANSI_D: _ClassVar[PageSize]
    PS_ANSI_E: _ClassVar[PageSize]
    PS_GERBER: _ClassVar[PageSize]
    PS_US_LETTER: _ClassVar[PageSize]
    PS_US_LEGAL: _ClassVar[PageSize]
    PS_US_LEDGER: _ClassVar[PageSize]
    PS_USER: _ClassVar[PageSize]

class PageOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PO_UNKNOWN: _ClassVar[PageOrientation]
    PO_LANDSCAPE: _ClassVar[PageOrientation]
    PO_PORTRAIT: _ClassVar[PageOrientation]
CS_UNKNOWN: CommandStatus
CS_OK: CommandStatus
CS_FAILED: CommandStatus
FT_UNKNOWN: FrameType
FT_PROJECT_MANAGER: FrameType
FT_SCHEMATIC_EDITOR: FrameType
FT_PCB_EDITOR: FrameType
FT_SPICE_SIMULATOR: FrameType
FT_SYMBOL_EDITOR: FrameType
FT_FOOTPRINT_EDITOR: FrameType
FT_DRAWING_SHEET_EDITOR: FrameType
DOCTYPE_UNKNOWN: DocumentType
DOCTYPE_SCHEMATIC: DocumentType
DOCTYPE_SYMBOL: DocumentType
DOCTYPE_PCB: DocumentType
DOCTYPE_FOOTPRINT: DocumentType
DOCTYPE_DRAWING_SHEET: DocumentType
DOCTYPE_PROJECT: DocumentType
IRS_UNKNOWN: ItemRequestStatus
IRS_OK: ItemRequestStatus
IRS_DOCUMENT_NOT_FOUND: ItemRequestStatus
IRS_FIELD_MASK_INVALID: ItemRequestStatus
LS_UNKNOWN: LockedState
LS_UNLOCKED: LockedState
LS_LOCKED: LockedState
GFT_UNKNOWN: GraphicFillType
GFT_UNFILLED: GraphicFillType
GFT_FILLED: GraphicFillType
GFT_FILLED_WITH_COLOR: GraphicFillType
GFT_FILLED_WITH_BACKGROUND_BODY_COLOR: GraphicFillType
GFT_HATCH: GraphicFillType
GFT_REVERSE_HATCH: GraphicFillType
GFT_CROSS_HATCH: GraphicFillType
AA_UNKNOWN: AxisAlignment
AA_X_AXIS: AxisAlignment
AA_Y_AXIS: AxisAlignment
MMM_UNKNOWN: MapMergeMode
MMM_MERGE: MapMergeMode
MMM_REPLACE: MapMergeMode
EPT_UNKNOWN: ElectricalPinType
EPT_INPUT: ElectricalPinType
EPT_OUTPUT: ElectricalPinType
EPT_BIDIRECTIONAL: ElectricalPinType
EPT_TRISTATE: ElectricalPinType
EPT_PASSIVE: ElectricalPinType
EPT_FREE: ElectricalPinType
EPT_UNSPECIFIED: ElectricalPinType
EPT_POWER_INPUT: ElectricalPinType
EPT_POWER_OUTPUT: ElectricalPinType
EPT_OPEN_COLLECTOR: ElectricalPinType
EPT_OPEN_EMITTER: ElectricalPinType
EPT_NO_CONNECT: ElectricalPinType
RS_UNKNOWN: RuleSeverity
RS_WARNING: RuleSeverity
RS_ERROR: RuleSeverity
RS_EXCLUSION: RuleSeverity
RS_IGNORE: RuleSeverity
RS_INFO: RuleSeverity
RS_ACTION: RuleSeverity
RS_DEBUG: RuleSeverity
RS_UNDEFINED: RuleSeverity
PS_UNKNOWN: PageSize
PS_A5: PageSize
PS_A4: PageSize
PS_A3: PageSize
PS_A2: PageSize
PS_A1: PageSize
PS_A0: PageSize
PS_ANSI_A: PageSize
PS_ANSI_B: PageSize
PS_ANSI_C: PageSize
PS_ANSI_D: PageSize
PS_ANSI_E: PageSize
PS_GERBER: PageSize
PS_US_LETTER: PageSize
PS_US_LEGAL: PageSize
PS_US_LEDGER: PageSize
PS_USER: PageSize
PO_UNKNOWN: PageOrientation
PO_LANDSCAPE: PageOrientation
PO_PORTRAIT: PageOrientation

class CommandStatusResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: CommandStatus
    def __init__(self, status: _Optional[_Union[CommandStatus, str]] = ...) -> None: ...

class KiCadVersion(_message.Message):
    __slots__ = ("major", "minor", "patch", "full_version")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    FULL_VERSION_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    patch: int
    full_version: str
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., patch: _Optional[int] = ..., full_version: _Optional[str] = ...) -> None: ...

class KIID(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class LibraryIdentifier(_message.Message):
    __slots__ = ("library_nickname", "entry_name")
    LIBRARY_NICKNAME_FIELD_NUMBER: _ClassVar[int]
    ENTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    library_nickname: str
    entry_name: str
    def __init__(self, library_nickname: _Optional[str] = ..., entry_name: _Optional[str] = ...) -> None: ...

class SheetPath(_message.Message):
    __slots__ = ("path", "path_human_readable")
    PATH_FIELD_NUMBER: _ClassVar[int]
    PATH_HUMAN_READABLE_FIELD_NUMBER: _ClassVar[int]
    path: _containers.RepeatedCompositeFieldContainer[KIID]
    path_human_readable: str
    def __init__(self, path: _Optional[_Iterable[_Union[KIID, _Mapping]]] = ..., path_human_readable: _Optional[str] = ...) -> None: ...

class ProjectSpecifier(_message.Message):
    __slots__ = ("name", "path")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    name: str
    path: str
    def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class DocumentSpecifier(_message.Message):
    __slots__ = ("type", "lib_id", "sheet_path", "board_filename", "project")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LIB_ID_FIELD_NUMBER: _ClassVar[int]
    SHEET_PATH_FIELD_NUMBER: _ClassVar[int]
    BOARD_FILENAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    type: DocumentType
    lib_id: LibraryIdentifier
    sheet_path: SheetPath
    board_filename: str
    project: ProjectSpecifier
    def __init__(self, type: _Optional[_Union[DocumentType, str]] = ..., lib_id: _Optional[_Union[LibraryIdentifier, _Mapping]] = ..., sheet_path: _Optional[_Union[SheetPath, _Mapping]] = ..., board_filename: _Optional[str] = ..., project: _Optional[_Union[ProjectSpecifier, _Mapping]] = ...) -> None: ...

class ItemHeader(_message.Message):
    __slots__ = ("document", "container", "field_mask")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    document: DocumentSpecifier
    container: KIID
    field_mask: _field_mask_pb2.FieldMask
    def __init__(self, document: _Optional[_Union[DocumentSpecifier, _Mapping]] = ..., container: _Optional[_Union[KIID, _Mapping]] = ..., field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class Vector2(_message.Message):
    __slots__ = ("x_nm", "y_nm")
    X_NM_FIELD_NUMBER: _ClassVar[int]
    Y_NM_FIELD_NUMBER: _ClassVar[int]
    x_nm: int
    y_nm: int
    def __init__(self, x_nm: _Optional[int] = ..., y_nm: _Optional[int] = ...) -> None: ...

class Vector3(_message.Message):
    __slots__ = ("x_nm", "y_nm", "z_nm")
    X_NM_FIELD_NUMBER: _ClassVar[int]
    Y_NM_FIELD_NUMBER: _ClassVar[int]
    Z_NM_FIELD_NUMBER: _ClassVar[int]
    x_nm: int
    y_nm: int
    z_nm: int
    def __init__(self, x_nm: _Optional[int] = ..., y_nm: _Optional[int] = ..., z_nm: _Optional[int] = ...) -> None: ...

class Vector3D(_message.Message):
    __slots__ = ("x_nm", "y_nm", "z_nm")
    X_NM_FIELD_NUMBER: _ClassVar[int]
    Y_NM_FIELD_NUMBER: _ClassVar[int]
    Z_NM_FIELD_NUMBER: _ClassVar[int]
    x_nm: float
    y_nm: float
    z_nm: float
    def __init__(self, x_nm: _Optional[float] = ..., y_nm: _Optional[float] = ..., z_nm: _Optional[float] = ...) -> None: ...

class Box2(_message.Message):
    __slots__ = ("position", "size")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    position: Vector2
    size: Vector2
    def __init__(self, position: _Optional[_Union[Vector2, _Mapping]] = ..., size: _Optional[_Union[Vector2, _Mapping]] = ...) -> None: ...

class Distance(_message.Message):
    __slots__ = ("value_nm",)
    VALUE_NM_FIELD_NUMBER: _ClassVar[int]
    value_nm: int
    def __init__(self, value_nm: _Optional[int] = ...) -> None: ...

class Angle(_message.Message):
    __slots__ = ("value_degrees",)
    VALUE_DEGREES_FIELD_NUMBER: _ClassVar[int]
    value_degrees: float
    def __init__(self, value_degrees: _Optional[float] = ...) -> None: ...

class Ratio(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...

class Time(_message.Message):
    __slots__ = ("value_as",)
    VALUE_AS_FIELD_NUMBER: _ClassVar[int]
    value_as: int
    def __init__(self, value_as: _Optional[int] = ...) -> None: ...

class Color(_message.Message):
    __slots__ = ("r", "g", "b", "a")
    R_FIELD_NUMBER: _ClassVar[int]
    G_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    r: float
    g: float
    b: float
    a: float
    def __init__(self, r: _Optional[float] = ..., g: _Optional[float] = ..., b: _Optional[float] = ..., a: _Optional[float] = ...) -> None: ...

class ArcStartMidEnd(_message.Message):
    __slots__ = ("start", "mid", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    MID_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: Vector2
    mid: Vector2
    end: Vector2
    def __init__(self, start: _Optional[_Union[Vector2, _Mapping]] = ..., mid: _Optional[_Union[Vector2, _Mapping]] = ..., end: _Optional[_Union[Vector2, _Mapping]] = ...) -> None: ...

class PolyLineNode(_message.Message):
    __slots__ = ("point", "arc")
    POINT_FIELD_NUMBER: _ClassVar[int]
    ARC_FIELD_NUMBER: _ClassVar[int]
    point: Vector2
    arc: ArcStartMidEnd
    def __init__(self, point: _Optional[_Union[Vector2, _Mapping]] = ..., arc: _Optional[_Union[ArcStartMidEnd, _Mapping]] = ...) -> None: ...

class PolyLine(_message.Message):
    __slots__ = ("nodes", "closed")
    NODES_FIELD_NUMBER: _ClassVar[int]
    CLOSED_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[PolyLineNode]
    closed: bool
    def __init__(self, nodes: _Optional[_Iterable[_Union[PolyLineNode, _Mapping]]] = ..., closed: bool = ...) -> None: ...

class PolygonWithHoles(_message.Message):
    __slots__ = ("outline", "holes")
    OUTLINE_FIELD_NUMBER: _ClassVar[int]
    HOLES_FIELD_NUMBER: _ClassVar[int]
    outline: PolyLine
    holes: _containers.RepeatedCompositeFieldContainer[PolyLine]
    def __init__(self, outline: _Optional[_Union[PolyLine, _Mapping]] = ..., holes: _Optional[_Iterable[_Union[PolyLine, _Mapping]]] = ...) -> None: ...

class PolySet(_message.Message):
    __slots__ = ("polygons",)
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    polygons: _containers.RepeatedCompositeFieldContainer[PolygonWithHoles]
    def __init__(self, polygons: _Optional[_Iterable[_Union[PolygonWithHoles, _Mapping]]] = ...) -> None: ...

class TextAttributes(_message.Message):
    __slots__ = ("font_name", "horizontal_alignment", "vertical_alignment", "angle", "line_spacing", "stroke_width", "italic", "bold", "underlined", "visible", "mirrored", "multiline", "keep_upright", "size", "color")
    FONT_NAME_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    LINE_SPACING_FIELD_NUMBER: _ClassVar[int]
    STROKE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    ITALIC_FIELD_NUMBER: _ClassVar[int]
    BOLD_FIELD_NUMBER: _ClassVar[int]
    UNDERLINED_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    MIRRORED_FIELD_NUMBER: _ClassVar[int]
    MULTILINE_FIELD_NUMBER: _ClassVar[int]
    KEEP_UPRIGHT_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    font_name: str
    horizontal_alignment: _enums_pb2.HorizontalAlignment
    vertical_alignment: _enums_pb2.VerticalAlignment
    angle: Angle
    line_spacing: float
    stroke_width: Distance
    italic: bool
    bold: bool
    underlined: bool
    visible: bool
    mirrored: bool
    multiline: bool
    keep_upright: bool
    size: Vector2
    color: Color
    def __init__(self, font_name: _Optional[str] = ..., horizontal_alignment: _Optional[_Union[_enums_pb2.HorizontalAlignment, str]] = ..., vertical_alignment: _Optional[_Union[_enums_pb2.VerticalAlignment, str]] = ..., angle: _Optional[_Union[Angle, _Mapping]] = ..., line_spacing: _Optional[float] = ..., stroke_width: _Optional[_Union[Distance, _Mapping]] = ..., italic: bool = ..., bold: bool = ..., underlined: bool = ..., visible: bool = ..., mirrored: bool = ..., multiline: bool = ..., keep_upright: bool = ..., size: _Optional[_Union[Vector2, _Mapping]] = ..., color: _Optional[_Union[Color, _Mapping]] = ...) -> None: ...

class Text(_message.Message):
    __slots__ = ("position", "attributes", "text", "hyperlink")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    HYPERLINK_FIELD_NUMBER: _ClassVar[int]
    position: Vector2
    attributes: TextAttributes
    text: str
    hyperlink: str
    def __init__(self, position: _Optional[_Union[Vector2, _Mapping]] = ..., attributes: _Optional[_Union[TextAttributes, _Mapping]] = ..., text: _Optional[str] = ..., hyperlink: _Optional[str] = ...) -> None: ...

class TextBox(_message.Message):
    __slots__ = ("top_left", "bottom_right", "attributes", "text")
    TOP_LEFT_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_RIGHT_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    top_left: Vector2
    bottom_right: Vector2
    attributes: TextAttributes
    text: str
    def __init__(self, top_left: _Optional[_Union[Vector2, _Mapping]] = ..., bottom_right: _Optional[_Union[Vector2, _Mapping]] = ..., attributes: _Optional[_Union[TextAttributes, _Mapping]] = ..., text: _Optional[str] = ...) -> None: ...

class StrokeAttributes(_message.Message):
    __slots__ = ("width", "style", "color")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    width: Distance
    style: _enums_pb2.StrokeLineStyle
    color: Color
    def __init__(self, width: _Optional[_Union[Distance, _Mapping]] = ..., style: _Optional[_Union[_enums_pb2.StrokeLineStyle, str]] = ..., color: _Optional[_Union[Color, _Mapping]] = ...) -> None: ...

class GraphicFillAttributes(_message.Message):
    __slots__ = ("fill_type", "color")
    FILL_TYPE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    fill_type: GraphicFillType
    color: Color
    def __init__(self, fill_type: _Optional[_Union[GraphicFillType, str]] = ..., color: _Optional[_Union[Color, _Mapping]] = ...) -> None: ...

class GraphicAttributes(_message.Message):
    __slots__ = ("stroke", "fill")
    STROKE_FIELD_NUMBER: _ClassVar[int]
    FILL_FIELD_NUMBER: _ClassVar[int]
    stroke: StrokeAttributes
    fill: GraphicFillAttributes
    def __init__(self, stroke: _Optional[_Union[StrokeAttributes, _Mapping]] = ..., fill: _Optional[_Union[GraphicFillAttributes, _Mapping]] = ...) -> None: ...

class GraphicSegmentAttributes(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: Vector2
    end: Vector2
    def __init__(self, start: _Optional[_Union[Vector2, _Mapping]] = ..., end: _Optional[_Union[Vector2, _Mapping]] = ...) -> None: ...

class GraphicRectangleAttributes(_message.Message):
    __slots__ = ("top_left", "bottom_right", "corner_radius")
    TOP_LEFT_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_RIGHT_FIELD_NUMBER: _ClassVar[int]
    CORNER_RADIUS_FIELD_NUMBER: _ClassVar[int]
    top_left: Vector2
    bottom_right: Vector2
    corner_radius: Distance
    def __init__(self, top_left: _Optional[_Union[Vector2, _Mapping]] = ..., bottom_right: _Optional[_Union[Vector2, _Mapping]] = ..., corner_radius: _Optional[_Union[Distance, _Mapping]] = ...) -> None: ...

class GraphicArcAttributes(_message.Message):
    __slots__ = ("start", "mid", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    MID_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: Vector2
    mid: Vector2
    end: Vector2
    def __init__(self, start: _Optional[_Union[Vector2, _Mapping]] = ..., mid: _Optional[_Union[Vector2, _Mapping]] = ..., end: _Optional[_Union[Vector2, _Mapping]] = ...) -> None: ...

class GraphicCircleAttributes(_message.Message):
    __slots__ = ("center", "radius_point")
    CENTER_FIELD_NUMBER: _ClassVar[int]
    RADIUS_POINT_FIELD_NUMBER: _ClassVar[int]
    center: Vector2
    radius_point: Vector2
    def __init__(self, center: _Optional[_Union[Vector2, _Mapping]] = ..., radius_point: _Optional[_Union[Vector2, _Mapping]] = ...) -> None: ...

class GraphicBezierAttributes(_message.Message):
    __slots__ = ("start", "control1", "control2", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    CONTROL1_FIELD_NUMBER: _ClassVar[int]
    CONTROL2_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: Vector2
    control1: Vector2
    control2: Vector2
    end: Vector2
    def __init__(self, start: _Optional[_Union[Vector2, _Mapping]] = ..., control1: _Optional[_Union[Vector2, _Mapping]] = ..., control2: _Optional[_Union[Vector2, _Mapping]] = ..., end: _Optional[_Union[Vector2, _Mapping]] = ...) -> None: ...

class GraphicEllipseAttributes(_message.Message):
    __slots__ = ("center", "major_radius", "minor_radius", "rotation")
    CENTER_FIELD_NUMBER: _ClassVar[int]
    MAJOR_RADIUS_FIELD_NUMBER: _ClassVar[int]
    MINOR_RADIUS_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    center: Vector2
    major_radius: Distance
    minor_radius: Distance
    rotation: Angle
    def __init__(self, center: _Optional[_Union[Vector2, _Mapping]] = ..., major_radius: _Optional[_Union[Distance, _Mapping]] = ..., minor_radius: _Optional[_Union[Distance, _Mapping]] = ..., rotation: _Optional[_Union[Angle, _Mapping]] = ...) -> None: ...

class GraphicEllipseArcAttributes(_message.Message):
    __slots__ = ("center", "major_radius", "minor_radius", "rotation", "start_angle", "end_angle")
    CENTER_FIELD_NUMBER: _ClassVar[int]
    MAJOR_RADIUS_FIELD_NUMBER: _ClassVar[int]
    MINOR_RADIUS_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    END_ANGLE_FIELD_NUMBER: _ClassVar[int]
    center: Vector2
    major_radius: Distance
    minor_radius: Distance
    rotation: Angle
    start_angle: Angle
    end_angle: Angle
    def __init__(self, center: _Optional[_Union[Vector2, _Mapping]] = ..., major_radius: _Optional[_Union[Distance, _Mapping]] = ..., minor_radius: _Optional[_Union[Distance, _Mapping]] = ..., rotation: _Optional[_Union[Angle, _Mapping]] = ..., start_angle: _Optional[_Union[Angle, _Mapping]] = ..., end_angle: _Optional[_Union[Angle, _Mapping]] = ...) -> None: ...

class GraphicShape(_message.Message):
    __slots__ = ("attributes", "segment", "rectangle", "arc", "circle", "polygon", "bezier", "ellipse", "ellipse_arc")
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_FIELD_NUMBER: _ClassVar[int]
    RECTANGLE_FIELD_NUMBER: _ClassVar[int]
    ARC_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    BEZIER_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_ARC_FIELD_NUMBER: _ClassVar[int]
    attributes: GraphicAttributes
    segment: GraphicSegmentAttributes
    rectangle: GraphicRectangleAttributes
    arc: GraphicArcAttributes
    circle: GraphicCircleAttributes
    polygon: PolySet
    bezier: GraphicBezierAttributes
    ellipse: GraphicEllipseAttributes
    ellipse_arc: GraphicEllipseArcAttributes
    def __init__(self, attributes: _Optional[_Union[GraphicAttributes, _Mapping]] = ..., segment: _Optional[_Union[GraphicSegmentAttributes, _Mapping]] = ..., rectangle: _Optional[_Union[GraphicRectangleAttributes, _Mapping]] = ..., arc: _Optional[_Union[GraphicArcAttributes, _Mapping]] = ..., circle: _Optional[_Union[GraphicCircleAttributes, _Mapping]] = ..., polygon: _Optional[_Union[PolySet, _Mapping]] = ..., bezier: _Optional[_Union[GraphicBezierAttributes, _Mapping]] = ..., ellipse: _Optional[_Union[GraphicEllipseAttributes, _Mapping]] = ..., ellipse_arc: _Optional[_Union[GraphicEllipseArcAttributes, _Mapping]] = ...) -> None: ...

class CompoundShape(_message.Message):
    __slots__ = ("shapes",)
    SHAPES_FIELD_NUMBER: _ClassVar[int]
    shapes: _containers.RepeatedCompositeFieldContainer[GraphicShape]
    def __init__(self, shapes: _Optional[_Iterable[_Union[GraphicShape, _Mapping]]] = ...) -> None: ...

class TitleBlockInfo(_message.Message):
    __slots__ = ("title", "date", "revision", "company", "comment1", "comment2", "comment3", "comment4", "comment5", "comment6", "comment7", "comment8", "comment9")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    COMMENT1_FIELD_NUMBER: _ClassVar[int]
    COMMENT2_FIELD_NUMBER: _ClassVar[int]
    COMMENT3_FIELD_NUMBER: _ClassVar[int]
    COMMENT4_FIELD_NUMBER: _ClassVar[int]
    COMMENT5_FIELD_NUMBER: _ClassVar[int]
    COMMENT6_FIELD_NUMBER: _ClassVar[int]
    COMMENT7_FIELD_NUMBER: _ClassVar[int]
    COMMENT8_FIELD_NUMBER: _ClassVar[int]
    COMMENT9_FIELD_NUMBER: _ClassVar[int]
    title: str
    date: str
    revision: str
    company: str
    comment1: str
    comment2: str
    comment3: str
    comment4: str
    comment5: str
    comment6: str
    comment7: str
    comment8: str
    comment9: str
    def __init__(self, title: _Optional[str] = ..., date: _Optional[str] = ..., revision: _Optional[str] = ..., company: _Optional[str] = ..., comment1: _Optional[str] = ..., comment2: _Optional[str] = ..., comment3: _Optional[str] = ..., comment4: _Optional[str] = ..., comment5: _Optional[str] = ..., comment6: _Optional[str] = ..., comment7: _Optional[str] = ..., comment8: _Optional[str] = ..., comment9: _Optional[str] = ...) -> None: ...

class RuleCheckerMarkerID(_message.Message):
    __slots__ = ("opaque_id",)
    OPAQUE_ID_FIELD_NUMBER: _ClassVar[int]
    opaque_id: str
    def __init__(self, opaque_id: _Optional[str] = ...) -> None: ...

class RuleCheckerMarker(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: RuleCheckerMarkerID
    def __init__(self, id: _Optional[_Union[RuleCheckerMarkerID, _Mapping]] = ...) -> None: ...

class MinOptMax(_message.Message):
    __slots__ = ("min", "opt", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    OPT_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: int
    opt: int
    max: int
    def __init__(self, min: _Optional[int] = ..., opt: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class PageSettings(_message.Message):
    __slots__ = ("page_size", "user_page_size", "orientation", "drawing_sheet")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    USER_PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    DRAWING_SHEET_FIELD_NUMBER: _ClassVar[int]
    page_size: PageSize
    user_page_size: Vector2
    orientation: PageOrientation
    drawing_sheet: str
    def __init__(self, page_size: _Optional[_Union[PageSize, str]] = ..., user_page_size: _Optional[_Union[Vector2, _Mapping]] = ..., orientation: _Optional[_Union[PageOrientation, str]] = ..., drawing_sheet: _Optional[str] = ...) -> None: ...
