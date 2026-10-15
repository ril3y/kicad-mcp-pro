from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class KiCadObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KOT_UNKNOWN: _ClassVar[KiCadObjectType]
    KOT_PCB_FOOTPRINT: _ClassVar[KiCadObjectType]
    KOT_PCB_PAD: _ClassVar[KiCadObjectType]
    KOT_PCB_SHAPE: _ClassVar[KiCadObjectType]
    KOT_PCB_REFERENCE_IMAGE: _ClassVar[KiCadObjectType]
    KOT_PCB_FIELD: _ClassVar[KiCadObjectType]
    KOT_PCB_GENERATOR: _ClassVar[KiCadObjectType]
    KOT_PCB_TEXT: _ClassVar[KiCadObjectType]
    KOT_PCB_TEXTBOX: _ClassVar[KiCadObjectType]
    KOT_PCB_TABLE: _ClassVar[KiCadObjectType]
    KOT_PCB_TABLECELL: _ClassVar[KiCadObjectType]
    KOT_PCB_TRACE: _ClassVar[KiCadObjectType]
    KOT_PCB_VIA: _ClassVar[KiCadObjectType]
    KOT_PCB_ARC: _ClassVar[KiCadObjectType]
    KOT_PCB_MARKER: _ClassVar[KiCadObjectType]
    KOT_PCB_DIMENSION: _ClassVar[KiCadObjectType]
    KOT_PCB_ZONE: _ClassVar[KiCadObjectType]
    KOT_PCB_GROUP: _ClassVar[KiCadObjectType]
    KOT_SCH_MARKER: _ClassVar[KiCadObjectType]
    KOT_SCH_JUNCTION: _ClassVar[KiCadObjectType]
    KOT_SCH_NO_CONNECT: _ClassVar[KiCadObjectType]
    KOT_SCH_BUS_WIRE_ENTRY: _ClassVar[KiCadObjectType]
    KOT_SCH_BUS_BUS_ENTRY: _ClassVar[KiCadObjectType]
    KOT_SCH_LINE: _ClassVar[KiCadObjectType]
    KOT_SCH_SHAPE: _ClassVar[KiCadObjectType]
    KOT_SCH_BITMAP: _ClassVar[KiCadObjectType]
    KOT_SCH_TEXTBOX: _ClassVar[KiCadObjectType]
    KOT_SCH_TEXT: _ClassVar[KiCadObjectType]
    KOT_SCH_TABLE: _ClassVar[KiCadObjectType]
    KOT_SCH_TABLECELL: _ClassVar[KiCadObjectType]
    KOT_SCH_LABEL: _ClassVar[KiCadObjectType]
    KOT_SCH_GLOBAL_LABEL: _ClassVar[KiCadObjectType]
    KOT_SCH_HIER_LABEL: _ClassVar[KiCadObjectType]
    KOT_SCH_DIRECTIVE_LABEL: _ClassVar[KiCadObjectType]
    KOT_SCH_FIELD: _ClassVar[KiCadObjectType]
    KOT_SCH_SYMBOL: _ClassVar[KiCadObjectType]
    KOT_SCH_SHEET_PIN: _ClassVar[KiCadObjectType]
    KOT_SCH_SHEET: _ClassVar[KiCadObjectType]
    KOT_SCH_PIN: _ClassVar[KiCadObjectType]
    KOT_LIB_SYMBOL: _ClassVar[KiCadObjectType]
    KOT_WSG_LINE: _ClassVar[KiCadObjectType]
    KOT_WSG_RECT: _ClassVar[KiCadObjectType]
    KOT_WSG_POLY: _ClassVar[KiCadObjectType]
    KOT_WSG_TEXT: _ClassVar[KiCadObjectType]
    KOT_WSG_BITMAP: _ClassVar[KiCadObjectType]
    KOT_WSG_PAGE: _ClassVar[KiCadObjectType]
    KOT_SCH_GROUP: _ClassVar[KiCadObjectType]
    KOT_PCB_BARCODE: _ClassVar[KiCadObjectType]

class HorizontalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HA_UNKNOWN: _ClassVar[HorizontalAlignment]
    HA_LEFT: _ClassVar[HorizontalAlignment]
    HA_CENTER: _ClassVar[HorizontalAlignment]
    HA_RIGHT: _ClassVar[HorizontalAlignment]
    HA_INDETERMINATE: _ClassVar[HorizontalAlignment]

class VerticalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VA_UNKNOWN: _ClassVar[VerticalAlignment]
    VA_TOP: _ClassVar[VerticalAlignment]
    VA_CENTER: _ClassVar[VerticalAlignment]
    VA_BOTTOM: _ClassVar[VerticalAlignment]
    VA_INDETERMINATE: _ClassVar[VerticalAlignment]

class StrokeLineStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SLS_UNKNOWN: _ClassVar[StrokeLineStyle]
    SLS_DEFAULT: _ClassVar[StrokeLineStyle]
    SLS_SOLID: _ClassVar[StrokeLineStyle]
    SLS_DASH: _ClassVar[StrokeLineStyle]
    SLS_DOT: _ClassVar[StrokeLineStyle]
    SLS_DASHDOT: _ClassVar[StrokeLineStyle]
    SLS_DASHDOTDOT: _ClassVar[StrokeLineStyle]

class Units(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    U_UNKNOWN: _ClassVar[Units]
    U_INCH: _ClassVar[Units]
    U_MM: _ClassVar[Units]
    U_MILS: _ClassVar[Units]
    U_METERS: _ClassVar[Units]
    U_TENTHS: _ClassVar[Units]
KOT_UNKNOWN: KiCadObjectType
KOT_PCB_FOOTPRINT: KiCadObjectType
KOT_PCB_PAD: KiCadObjectType
KOT_PCB_SHAPE: KiCadObjectType
KOT_PCB_REFERENCE_IMAGE: KiCadObjectType
KOT_PCB_FIELD: KiCadObjectType
KOT_PCB_GENERATOR: KiCadObjectType
KOT_PCB_TEXT: KiCadObjectType
KOT_PCB_TEXTBOX: KiCadObjectType
KOT_PCB_TABLE: KiCadObjectType
KOT_PCB_TABLECELL: KiCadObjectType
KOT_PCB_TRACE: KiCadObjectType
KOT_PCB_VIA: KiCadObjectType
KOT_PCB_ARC: KiCadObjectType
KOT_PCB_MARKER: KiCadObjectType
KOT_PCB_DIMENSION: KiCadObjectType
KOT_PCB_ZONE: KiCadObjectType
KOT_PCB_GROUP: KiCadObjectType
KOT_SCH_MARKER: KiCadObjectType
KOT_SCH_JUNCTION: KiCadObjectType
KOT_SCH_NO_CONNECT: KiCadObjectType
KOT_SCH_BUS_WIRE_ENTRY: KiCadObjectType
KOT_SCH_BUS_BUS_ENTRY: KiCadObjectType
KOT_SCH_LINE: KiCadObjectType
KOT_SCH_SHAPE: KiCadObjectType
KOT_SCH_BITMAP: KiCadObjectType
KOT_SCH_TEXTBOX: KiCadObjectType
KOT_SCH_TEXT: KiCadObjectType
KOT_SCH_TABLE: KiCadObjectType
KOT_SCH_TABLECELL: KiCadObjectType
KOT_SCH_LABEL: KiCadObjectType
KOT_SCH_GLOBAL_LABEL: KiCadObjectType
KOT_SCH_HIER_LABEL: KiCadObjectType
KOT_SCH_DIRECTIVE_LABEL: KiCadObjectType
KOT_SCH_FIELD: KiCadObjectType
KOT_SCH_SYMBOL: KiCadObjectType
KOT_SCH_SHEET_PIN: KiCadObjectType
KOT_SCH_SHEET: KiCadObjectType
KOT_SCH_PIN: KiCadObjectType
KOT_LIB_SYMBOL: KiCadObjectType
KOT_WSG_LINE: KiCadObjectType
KOT_WSG_RECT: KiCadObjectType
KOT_WSG_POLY: KiCadObjectType
KOT_WSG_TEXT: KiCadObjectType
KOT_WSG_BITMAP: KiCadObjectType
KOT_WSG_PAGE: KiCadObjectType
KOT_SCH_GROUP: KiCadObjectType
KOT_PCB_BARCODE: KiCadObjectType
HA_UNKNOWN: HorizontalAlignment
HA_LEFT: HorizontalAlignment
HA_CENTER: HorizontalAlignment
HA_RIGHT: HorizontalAlignment
HA_INDETERMINATE: HorizontalAlignment
VA_UNKNOWN: VerticalAlignment
VA_TOP: VerticalAlignment
VA_CENTER: VerticalAlignment
VA_BOTTOM: VerticalAlignment
VA_INDETERMINATE: VerticalAlignment
SLS_UNKNOWN: StrokeLineStyle
SLS_DEFAULT: StrokeLineStyle
SLS_SOLID: StrokeLineStyle
SLS_DASH: StrokeLineStyle
SLS_DOT: StrokeLineStyle
SLS_DASHDOT: StrokeLineStyle
SLS_DASHDOTDOT: StrokeLineStyle
U_UNKNOWN: Units
U_INCH: Units
U_MM: Units
U_MILS: Units
U_METERS: Units
U_TENTHS: Units
