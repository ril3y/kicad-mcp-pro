from google.protobuf import any_pb2 as _any_pb2
from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import embedded_files_pb2 as _embedded_files_pb2
from mp.common.types import enums_pb2 as _enums_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoardLayer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BL_UNKNOWN: _ClassVar[BoardLayer]
    BL_UNDEFINED: _ClassVar[BoardLayer]
    BL_UNSELECTED: _ClassVar[BoardLayer]
    BL_F_Cu: _ClassVar[BoardLayer]
    BL_In1_Cu: _ClassVar[BoardLayer]
    BL_In2_Cu: _ClassVar[BoardLayer]
    BL_In3_Cu: _ClassVar[BoardLayer]
    BL_In4_Cu: _ClassVar[BoardLayer]
    BL_In5_Cu: _ClassVar[BoardLayer]
    BL_In6_Cu: _ClassVar[BoardLayer]
    BL_In7_Cu: _ClassVar[BoardLayer]
    BL_In8_Cu: _ClassVar[BoardLayer]
    BL_In9_Cu: _ClassVar[BoardLayer]
    BL_In10_Cu: _ClassVar[BoardLayer]
    BL_In11_Cu: _ClassVar[BoardLayer]
    BL_In12_Cu: _ClassVar[BoardLayer]
    BL_In13_Cu: _ClassVar[BoardLayer]
    BL_In14_Cu: _ClassVar[BoardLayer]
    BL_In15_Cu: _ClassVar[BoardLayer]
    BL_In16_Cu: _ClassVar[BoardLayer]
    BL_In17_Cu: _ClassVar[BoardLayer]
    BL_In18_Cu: _ClassVar[BoardLayer]
    BL_In19_Cu: _ClassVar[BoardLayer]
    BL_In20_Cu: _ClassVar[BoardLayer]
    BL_In21_Cu: _ClassVar[BoardLayer]
    BL_In22_Cu: _ClassVar[BoardLayer]
    BL_In23_Cu: _ClassVar[BoardLayer]
    BL_In24_Cu: _ClassVar[BoardLayer]
    BL_In25_Cu: _ClassVar[BoardLayer]
    BL_In26_Cu: _ClassVar[BoardLayer]
    BL_In27_Cu: _ClassVar[BoardLayer]
    BL_In28_Cu: _ClassVar[BoardLayer]
    BL_In29_Cu: _ClassVar[BoardLayer]
    BL_In30_Cu: _ClassVar[BoardLayer]
    BL_B_Cu: _ClassVar[BoardLayer]
    BL_B_Adhes: _ClassVar[BoardLayer]
    BL_F_Adhes: _ClassVar[BoardLayer]
    BL_B_Paste: _ClassVar[BoardLayer]
    BL_F_Paste: _ClassVar[BoardLayer]
    BL_B_SilkS: _ClassVar[BoardLayer]
    BL_F_SilkS: _ClassVar[BoardLayer]
    BL_B_Mask: _ClassVar[BoardLayer]
    BL_F_Mask: _ClassVar[BoardLayer]
    BL_Dwgs_User: _ClassVar[BoardLayer]
    BL_Cmts_User: _ClassVar[BoardLayer]
    BL_Eco1_User: _ClassVar[BoardLayer]
    BL_Eco2_User: _ClassVar[BoardLayer]
    BL_Edge_Cuts: _ClassVar[BoardLayer]
    BL_Margin: _ClassVar[BoardLayer]
    BL_B_CrtYd: _ClassVar[BoardLayer]
    BL_F_CrtYd: _ClassVar[BoardLayer]
    BL_B_Fab: _ClassVar[BoardLayer]
    BL_F_Fab: _ClassVar[BoardLayer]
    BL_User_1: _ClassVar[BoardLayer]
    BL_User_2: _ClassVar[BoardLayer]
    BL_User_3: _ClassVar[BoardLayer]
    BL_User_4: _ClassVar[BoardLayer]
    BL_User_5: _ClassVar[BoardLayer]
    BL_User_6: _ClassVar[BoardLayer]
    BL_User_7: _ClassVar[BoardLayer]
    BL_User_8: _ClassVar[BoardLayer]
    BL_User_9: _ClassVar[BoardLayer]
    BL_Rescue: _ClassVar[BoardLayer]
    BL_User_10: _ClassVar[BoardLayer]
    BL_User_11: _ClassVar[BoardLayer]
    BL_User_12: _ClassVar[BoardLayer]
    BL_User_13: _ClassVar[BoardLayer]
    BL_User_14: _ClassVar[BoardLayer]
    BL_User_15: _ClassVar[BoardLayer]
    BL_User_16: _ClassVar[BoardLayer]
    BL_User_17: _ClassVar[BoardLayer]
    BL_User_18: _ClassVar[BoardLayer]
    BL_User_19: _ClassVar[BoardLayer]
    BL_User_20: _ClassVar[BoardLayer]
    BL_User_21: _ClassVar[BoardLayer]
    BL_User_22: _ClassVar[BoardLayer]
    BL_User_23: _ClassVar[BoardLayer]
    BL_User_24: _ClassVar[BoardLayer]
    BL_User_25: _ClassVar[BoardLayer]
    BL_User_26: _ClassVar[BoardLayer]
    BL_User_27: _ClassVar[BoardLayer]
    BL_User_28: _ClassVar[BoardLayer]
    BL_User_29: _ClassVar[BoardLayer]
    BL_User_30: _ClassVar[BoardLayer]
    BL_User_31: _ClassVar[BoardLayer]
    BL_User_32: _ClassVar[BoardLayer]
    BL_User_33: _ClassVar[BoardLayer]
    BL_User_34: _ClassVar[BoardLayer]
    BL_User_35: _ClassVar[BoardLayer]
    BL_User_36: _ClassVar[BoardLayer]
    BL_User_37: _ClassVar[BoardLayer]
    BL_User_38: _ClassVar[BoardLayer]
    BL_User_39: _ClassVar[BoardLayer]
    BL_User_40: _ClassVar[BoardLayer]
    BL_User_41: _ClassVar[BoardLayer]
    BL_User_42: _ClassVar[BoardLayer]
    BL_User_43: _ClassVar[BoardLayer]
    BL_User_44: _ClassVar[BoardLayer]
    BL_User_45: _ClassVar[BoardLayer]

class PadStackType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PST_UNKNOWN: _ClassVar[PadStackType]
    PST_NORMAL: _ClassVar[PadStackType]
    PST_FRONT_INNER_BACK: _ClassVar[PadStackType]
    PST_CUSTOM: _ClassVar[PadStackType]

class UnconnectedLayerRemoval(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ULR_UNKNOWN: _ClassVar[UnconnectedLayerRemoval]
    ULR_KEEP: _ClassVar[UnconnectedLayerRemoval]
    ULR_REMOVE: _ClassVar[UnconnectedLayerRemoval]
    ULR_REMOVE_EXCEPT_START_AND_END: _ClassVar[UnconnectedLayerRemoval]
    ULR_START_END_ONLY: _ClassVar[UnconnectedLayerRemoval]

class PadStackShape(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PSS_UNKNOWN: _ClassVar[PadStackShape]
    PSS_CIRCLE: _ClassVar[PadStackShape]
    PSS_RECTANGLE: _ClassVar[PadStackShape]
    PSS_OVAL: _ClassVar[PadStackShape]
    PSS_TRAPEZOID: _ClassVar[PadStackShape]
    PSS_ROUNDRECT: _ClassVar[PadStackShape]
    PSS_CHAMFEREDRECT: _ClassVar[PadStackShape]
    PSS_CUSTOM: _ClassVar[PadStackShape]

class ZoneConnectionStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZCS_UNKNOWN: _ClassVar[ZoneConnectionStyle]
    ZCS_INHERITED: _ClassVar[ZoneConnectionStyle]
    ZCS_NONE: _ClassVar[ZoneConnectionStyle]
    ZCS_THERMAL: _ClassVar[ZoneConnectionStyle]
    ZCS_FULL: _ClassVar[ZoneConnectionStyle]
    ZCS_PTH_THERMAL: _ClassVar[ZoneConnectionStyle]

class SolderMaskMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SMM_UNKNOWN: _ClassVar[SolderMaskMode]
    SMM_MASKED: _ClassVar[SolderMaskMode]
    SMM_UNMASKED: _ClassVar[SolderMaskMode]
    SMM_FROM_DESIGN_RULES: _ClassVar[SolderMaskMode]

class ViaCoveringMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VCM_UNKNOWN: _ClassVar[ViaCoveringMode]
    VCM_COVERED: _ClassVar[ViaCoveringMode]
    VCM_UNCOVERED: _ClassVar[ViaCoveringMode]
    VCM_FROM_DESIGN_RULES: _ClassVar[ViaCoveringMode]

class ViaPluggingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VPM_UNKNOWN: _ClassVar[ViaPluggingMode]
    VPM_PLUGGED: _ClassVar[ViaPluggingMode]
    VPM_UNPLUGGED: _ClassVar[ViaPluggingMode]
    VPM_FROM_DESIGN_RULES: _ClassVar[ViaPluggingMode]

class SolderPasteMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SPM_UNKNOWN: _ClassVar[SolderPasteMode]
    SPM_PASTE: _ClassVar[SolderPasteMode]
    SPM_NO_PASTE: _ClassVar[SolderPasteMode]
    SPM_FROM_DESIGN_RULES: _ClassVar[SolderPasteMode]

class DrillShape(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DS_UNKNOWN: _ClassVar[DrillShape]
    DS_CIRCLE: _ClassVar[DrillShape]
    DS_OBLONG: _ClassVar[DrillShape]
    DS_UNDEFINED: _ClassVar[DrillShape]

class ViaDrillCappingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VDCM_UNKNOWN: _ClassVar[ViaDrillCappingMode]
    VDCM_CAPPED: _ClassVar[ViaDrillCappingMode]
    VDCM_UNCAPPED: _ClassVar[ViaDrillCappingMode]
    VDCM_FROM_DESIGN_RULES: _ClassVar[ViaDrillCappingMode]

class ViaDrillFillingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VDFM_UNKNOWN: _ClassVar[ViaDrillFillingMode]
    VDFM_FILLED: _ClassVar[ViaDrillFillingMode]
    VDFM_UNFILLED: _ClassVar[ViaDrillFillingMode]
    VDFM_FROM_DESIGN_RULES: _ClassVar[ViaDrillFillingMode]

class ViaDrillPostMachiningMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VDPM_UNKNOWN: _ClassVar[ViaDrillPostMachiningMode]
    VDPM_NOT_POST_MACHINED: _ClassVar[ViaDrillPostMachiningMode]
    VDPM_COUNTERBORE: _ClassVar[ViaDrillPostMachiningMode]
    VDPM_COUNTERSINK: _ClassVar[ViaDrillPostMachiningMode]

class ViaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VT_UNKNOWN: _ClassVar[ViaType]
    VT_THROUGH: _ClassVar[ViaType]
    VT_BLIND_BURIED: _ClassVar[ViaType]
    VT_MICRO: _ClassVar[ViaType]
    VT_BLIND: _ClassVar[ViaType]
    VT_BURIED: _ClassVar[ViaType]

class ZoneLayerOverride(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZLO_UNKNOWN: _ClassVar[ZoneLayerOverride]
    ZLO_NONE: _ClassVar[ZoneLayerOverride]
    ZLO_FORCE_FLASHED: _ClassVar[ZoneLayerOverride]
    ZLO_FORCE_NO_ZONE_CONNECTION: _ClassVar[ZoneLayerOverride]

class BarcodeKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BK_UNKNOWN: _ClassVar[BarcodeKind]
    BK_CODE_39: _ClassVar[BarcodeKind]
    BK_CODE_128: _ClassVar[BarcodeKind]
    BK_DATA_MATRIX: _ClassVar[BarcodeKind]
    BK_QR_CODE: _ClassVar[BarcodeKind]
    BK_MICRO_QR_CODE: _ClassVar[BarcodeKind]

class BarcodeErrorCorrection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BEC_UNKNOWN: _ClassVar[BarcodeErrorCorrection]
    BEC_L: _ClassVar[BarcodeErrorCorrection]
    BEC_M: _ClassVar[BarcodeErrorCorrection]
    BEC_Q: _ClassVar[BarcodeErrorCorrection]
    BEC_H: _ClassVar[BarcodeErrorCorrection]

class PadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PT_UNKNOWN: _ClassVar[PadType]
    PT_PTH: _ClassVar[PadType]
    PT_SMD: _ClassVar[PadType]
    PT_EDGE_CONNECTOR: _ClassVar[PadType]
    PT_NPTH: _ClassVar[PadType]
    PT_NON_COMPONENT: _ClassVar[PadType]

class PadSimElectricalType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PSET_NONE: _ClassVar[PadSimElectricalType]
    PSET_SOURCE: _ClassVar[PadSimElectricalType]
    PSET_SINK: _ClassVar[PadSimElectricalType]

class PadFabricationProperty(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PFP_UNKNOWN: _ClassVar[PadFabricationProperty]
    PFP_NONE: _ClassVar[PadFabricationProperty]
    PFP_BGA: _ClassVar[PadFabricationProperty]
    PFP_FIDUCIAL_GLOBAL: _ClassVar[PadFabricationProperty]
    PFP_FIDUCIAL_LOCAL: _ClassVar[PadFabricationProperty]
    PFP_TESTPOINT: _ClassVar[PadFabricationProperty]
    PFP_HEATSINK: _ClassVar[PadFabricationProperty]
    PFP_CASTELLATED: _ClassVar[PadFabricationProperty]
    PFP_MECHANICAL: _ClassVar[PadFabricationProperty]
    PFP_PRESSFIT: _ClassVar[PadFabricationProperty]

class CustomPadShapeZoneFillStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CPSZ_UNKNOWN: _ClassVar[CustomPadShapeZoneFillStrategy]
    CPSZ_OUTLINE: _ClassVar[CustomPadShapeZoneFillStrategy]
    CPSZ_CONVEXHULL: _ClassVar[CustomPadShapeZoneFillStrategy]

class ZoneType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZT_UNKNOWN: _ClassVar[ZoneType]
    ZT_COPPER: _ClassVar[ZoneType]
    ZT_GRAPHICAL: _ClassVar[ZoneType]
    ZT_RULE_AREA: _ClassVar[ZoneType]
    ZT_TEARDROP: _ClassVar[ZoneType]

class ZoneTeardropType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZTDT_UNKNOWN: _ClassVar[ZoneTeardropType]
    ZTDT_NONE: _ClassVar[ZoneTeardropType]
    ZTDT_UNSPECIFIED: _ClassVar[ZoneTeardropType]
    ZTDT_VIA_PAD: _ClassVar[ZoneTeardropType]
    ZTDT_TRACK_END: _ClassVar[ZoneTeardropType]

class IslandRemovalMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IRM_UNKNOWN: _ClassVar[IslandRemovalMode]
    IRM_ALWAYS: _ClassVar[IslandRemovalMode]
    IRM_NEVER: _ClassVar[IslandRemovalMode]
    IRM_AREA: _ClassVar[IslandRemovalMode]

class ZoneFillMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZFM_UNKNOWN: _ClassVar[ZoneFillMode]
    ZFM_SOLID: _ClassVar[ZoneFillMode]
    ZFM_HATCHED: _ClassVar[ZoneFillMode]
    ZFM_COPPER_THIEVING: _ClassVar[ZoneFillMode]

class ZoneHatchSmoothing(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZHS_UNKNOWN: _ClassVar[ZoneHatchSmoothing]
    ZHS_NONE: _ClassVar[ZoneHatchSmoothing]
    ZHS_FILLET: _ClassVar[ZoneHatchSmoothing]
    ZHS_ARC_LOW_DEF: _ClassVar[ZoneHatchSmoothing]
    ZHS_ARC_HIGH_DEF: _ClassVar[ZoneHatchSmoothing]

class ZoneHatchFillBorderMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZHFBM_UNKNOWN: _ClassVar[ZoneHatchFillBorderMode]
    ZHFBM_USE_MIN_ZONE_THICKNESS: _ClassVar[ZoneHatchFillBorderMode]
    ZHFBM_USE_HATCH_THICKNESS: _ClassVar[ZoneHatchFillBorderMode]

class ThievingPattern(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TP_UNKNOWN: _ClassVar[ThievingPattern]
    TP_DOTS: _ClassVar[ThievingPattern]
    TP_SQUARES: _ClassVar[ThievingPattern]
    TP_CROSSHATCH: _ClassVar[ThievingPattern]

class PadTeardropMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PTM_UNKNOWN: _ClassVar[PadTeardropMode]
    PTM_DISABLED: _ClassVar[PadTeardropMode]
    PTM_ENABLED: _ClassVar[PadTeardropMode]

class ZoneCornerSmoothingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZCSM_UNKNOWN: _ClassVar[ZoneCornerSmoothingMode]
    ZCSM_NONE: _ClassVar[ZoneCornerSmoothingMode]
    ZCSM_CHAMFER: _ClassVar[ZoneCornerSmoothingMode]
    ZCSM_FILLET: _ClassVar[ZoneCornerSmoothingMode]

class PlacementRuleSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRST_UNKNOWN: _ClassVar[PlacementRuleSourceType]
    PRST_SHEET_NAME: _ClassVar[PlacementRuleSourceType]
    PRST_COMPONENT_CLASS: _ClassVar[PlacementRuleSourceType]
    PRST_GROUP: _ClassVar[PlacementRuleSourceType]
    PRST_DESIGN_BLOCK: _ClassVar[PlacementRuleSourceType]

class ZoneBorderStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ZBS_UNKNOWN: _ClassVar[ZoneBorderStyle]
    ZBS_SOLID: _ClassVar[ZoneBorderStyle]
    ZBS_DIAGONAL_FULL: _ClassVar[ZoneBorderStyle]
    ZBS_DIAGONAL_EDGE: _ClassVar[ZoneBorderStyle]
    ZBS_INVISIBLE: _ClassVar[ZoneBorderStyle]

class DimensionTextBorderStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DTBS_UNKNOWN: _ClassVar[DimensionTextBorderStyle]
    DTBS_NONE: _ClassVar[DimensionTextBorderStyle]
    DTBS_RECTANGLE: _ClassVar[DimensionTextBorderStyle]
    DTBS_CIRCLE: _ClassVar[DimensionTextBorderStyle]
    DTBS_ROUNDRECT: _ClassVar[DimensionTextBorderStyle]

class DimensionUnitFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DUF_UNKNOWN: _ClassVar[DimensionUnitFormat]
    DUF_NO_SUFFIX: _ClassVar[DimensionUnitFormat]
    DUF_BARE_SUFFIX: _ClassVar[DimensionUnitFormat]
    DUF_PAREN_SUFFIX: _ClassVar[DimensionUnitFormat]

class DimensionArrowDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DAD_UNKNOWN: _ClassVar[DimensionArrowDirection]
    DAD_INWARD: _ClassVar[DimensionArrowDirection]
    DAD_OUTWARD: _ClassVar[DimensionArrowDirection]

class DimensionPrecision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DP_UNKNOWN: _ClassVar[DimensionPrecision]
    DP_FIXED_0: _ClassVar[DimensionPrecision]
    DP_FIXED_1: _ClassVar[DimensionPrecision]
    DP_FIXED_2: _ClassVar[DimensionPrecision]
    DP_FIXED_3: _ClassVar[DimensionPrecision]
    DP_FIXED_4: _ClassVar[DimensionPrecision]
    DP_FIXED_5: _ClassVar[DimensionPrecision]
    DP_SCALED_IN_2: _ClassVar[DimensionPrecision]
    DP_SCALED_IN_3: _ClassVar[DimensionPrecision]
    DP_SCALED_IN_4: _ClassVar[DimensionPrecision]
    DP_SCALED_IN_5: _ClassVar[DimensionPrecision]

class DimensionTextPosition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DTP_UNKNOWN: _ClassVar[DimensionTextPosition]
    DTP_OUTSIDE: _ClassVar[DimensionTextPosition]
    DTP_INLINE: _ClassVar[DimensionTextPosition]
    DTP_MANUAL: _ClassVar[DimensionTextPosition]

class DimensionUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DU_UNKNOWN: _ClassVar[DimensionUnit]
    DU_INCHES: _ClassVar[DimensionUnit]
    DU_MILS: _ClassVar[DimensionUnit]
    DU_MILLIMETERS: _ClassVar[DimensionUnit]
    DU_AUTOMATIC: _ClassVar[DimensionUnit]

class ConstraintType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CT_UNKNOWN: _ClassVar[ConstraintType]
    CT_COINCIDENT: _ClassVar[ConstraintType]
    CT_HORIZONTAL: _ClassVar[ConstraintType]
    CT_VERTICAL: _ClassVar[ConstraintType]
    CT_PARALLEL: _ClassVar[ConstraintType]
    CT_PERPENDICULAR: _ClassVar[ConstraintType]
    CT_COLLINEAR: _ClassVar[ConstraintType]
    CT_SYMMETRIC: _ClassVar[ConstraintType]
    CT_EQUAL_LENGTH: _ClassVar[ConstraintType]
    CT_EQUAL_RADIUS: _ClassVar[ConstraintType]
    CT_POINT_ON_LINE: _ClassVar[ConstraintType]
    CT_MIDPOINT: _ClassVar[ConstraintType]
    CT_FIXED_POSITION: _ClassVar[ConstraintType]
    CT_FIXED_LENGTH: _ClassVar[ConstraintType]
    CT_CONCENTRIC: _ClassVar[ConstraintType]
    CT_FIXED_RADIUS: _ClassVar[ConstraintType]
    CT_ANGULAR_DIMENSION: _ClassVar[ConstraintType]
    CT_TANGENT: _ClassVar[ConstraintType]
    CT_ARC_ANGLE: _ClassVar[ConstraintType]

class ConstraintAnchor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CA_UNKNOWN: _ClassVar[ConstraintAnchor]
    CA_WHOLE: _ClassVar[ConstraintAnchor]
    CA_START: _ClassVar[ConstraintAnchor]
    CA_END: _ClassVar[ConstraintAnchor]
    CA_MID: _ClassVar[ConstraintAnchor]
    CA_CENTER: _ClassVar[ConstraintAnchor]
    CA_RADIUS: _ClassVar[ConstraintAnchor]
    CA_VERTEX: _ClassVar[ConstraintAnchor]

class FootprintMountingStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FMS_UNKNOWN: _ClassVar[FootprintMountingStyle]
    FMS_THROUGH_HOLE: _ClassVar[FootprintMountingStyle]
    FMS_SMD: _ClassVar[FootprintMountingStyle]
    FMS_UNSPECIFIED: _ClassVar[FootprintMountingStyle]

class Body3DKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BDK_UNKNOWN: _ClassVar[Body3DKind]
    BDK_EXTRUDED: _ClassVar[Body3DKind]
    BDK_MODEL: _ClassVar[Body3DKind]

class ExtrusionMaterial(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EM_UNKNOWN: _ClassVar[ExtrusionMaterial]
    EM_PLASTIC: _ClassVar[ExtrusionMaterial]
    EM_MATTE: _ClassVar[ExtrusionMaterial]
    EM_METAL: _ClassVar[ExtrusionMaterial]
    EM_COPPER: _ClassVar[ExtrusionMaterial]

class TableStrokeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TSM_UNKNOWN: _ClassVar[TableStrokeMode]
    TSM_DISABLED: _ClassVar[TableStrokeMode]
    TSM_ENABLED: _ClassVar[TableStrokeMode]

class DrillChartColumnId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DCC_UNKNOWN: _ClassVar[DrillChartColumnId]
    DCC_SYMBOL: _ClassVar[DrillChartColumnId]
    DCC_DRILL_DIAMETER: _ClassVar[DrillChartColumnId]
    DCC_SLOT_SIZE: _ClassVar[DrillChartColumnId]
    DCC_PLATING: _ClassVar[DrillChartColumnId]
    DCC_OPERATION_COUNT: _ClassVar[DrillChartColumnId]
    DCC_SITE_COUNT: _ClassVar[DrillChartColumnId]
    DCC_LAYER_SPAN: _ClassVar[DrillChartColumnId]
    DCC_OPERATION: _ClassVar[DrillChartColumnId]
    DCC_PROTECTION: _ClassVar[DrillChartColumnId]
    DCC_BACKDRILL_STUB: _ClassVar[DrillChartColumnId]
    DCC_ASPECT_RATIO: _ClassVar[DrillChartColumnId]
    DCC_DESCRIPTION: _ClassVar[DrillChartColumnId]

class TuningPatternMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TPM_UNKNOWN: _ClassVar[TuningPatternMode]
    TPM_SINGLE: _ClassVar[TuningPatternMode]
    TPM_DIFF_PAIR: _ClassVar[TuningPatternMode]
    TPM_DIFF_PAIR_SKEW: _ClassVar[TuningPatternMode]

class TuningPatternMeanderSide(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TPMS_UNKNOWN: _ClassVar[TuningPatternMeanderSide]
    TPMS_DEFAULT: _ClassVar[TuningPatternMeanderSide]
    TPMS_LEFT: _ClassVar[TuningPatternMeanderSide]
    TPMS_RIGHT: _ClassVar[TuningPatternMeanderSide]

class TuningPatternCornerStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TPCS_UNKNOWN: _ClassVar[TuningPatternCornerStyle]
    TPCS_CHAMFERED: _ClassVar[TuningPatternCornerStyle]
    TPCS_ROUNDED: _ClassVar[TuningPatternCornerStyle]

class TuningPatternStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TPS_UNKNOWN: _ClassVar[TuningPatternStatus]
    TPS_TOO_SHORT: _ClassVar[TuningPatternStatus]
    TPS_TOO_LONG: _ClassVar[TuningPatternStatus]
    TPS_TUNED: _ClassVar[TuningPatternStatus]

class TuningPatternTargetMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TPTM_UNKNOWN: _ClassVar[TuningPatternTargetMode]
    TPTM_LENGTH: _ClassVar[TuningPatternTargetMode]
    TPTM_TIME_DOMAIN: _ClassVar[TuningPatternTargetMode]

class ViaStitchLayout(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VSL_UNKNOWN: _ClassVar[ViaStitchLayout]
    VSL_PLAIN: _ClassVar[ViaStitchLayout]
    VSL_STAGGERED: _ClassVar[ViaStitchLayout]
    VSL_POISSON: _ClassVar[ViaStitchLayout]

class ViaStitchMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VSM_UNKNOWN: _ClassVar[ViaStitchMode]
    VSM_STITCH: _ClassVar[ViaStitchMode]
    VSM_GUARD: _ClassVar[ViaStitchMode]

class ViaStackStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VSK_UNKNOWN: _ClassVar[ViaStackStyle]
    VSK_STACKED: _ClassVar[ViaStackStyle]
    VSK_STAGGERED: _ClassVar[ViaStackStyle]

class StackupTableColumnId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STC_UNKNOWN: _ClassVar[StackupTableColumnId]
    STC_LAYER: _ClassVar[StackupTableColumnId]
    STC_TYPE: _ClassVar[StackupTableColumnId]
    STC_MATERIAL: _ClassVar[StackupTableColumnId]
    STC_THICKNESS: _ClassVar[StackupTableColumnId]
    STC_COLOR: _ClassVar[StackupTableColumnId]
    STC_EPSILON_R: _ClassVar[StackupTableColumnId]
    STC_LOSS_TANGENT: _ClassVar[StackupTableColumnId]
BL_UNKNOWN: BoardLayer
BL_UNDEFINED: BoardLayer
BL_UNSELECTED: BoardLayer
BL_F_Cu: BoardLayer
BL_In1_Cu: BoardLayer
BL_In2_Cu: BoardLayer
BL_In3_Cu: BoardLayer
BL_In4_Cu: BoardLayer
BL_In5_Cu: BoardLayer
BL_In6_Cu: BoardLayer
BL_In7_Cu: BoardLayer
BL_In8_Cu: BoardLayer
BL_In9_Cu: BoardLayer
BL_In10_Cu: BoardLayer
BL_In11_Cu: BoardLayer
BL_In12_Cu: BoardLayer
BL_In13_Cu: BoardLayer
BL_In14_Cu: BoardLayer
BL_In15_Cu: BoardLayer
BL_In16_Cu: BoardLayer
BL_In17_Cu: BoardLayer
BL_In18_Cu: BoardLayer
BL_In19_Cu: BoardLayer
BL_In20_Cu: BoardLayer
BL_In21_Cu: BoardLayer
BL_In22_Cu: BoardLayer
BL_In23_Cu: BoardLayer
BL_In24_Cu: BoardLayer
BL_In25_Cu: BoardLayer
BL_In26_Cu: BoardLayer
BL_In27_Cu: BoardLayer
BL_In28_Cu: BoardLayer
BL_In29_Cu: BoardLayer
BL_In30_Cu: BoardLayer
BL_B_Cu: BoardLayer
BL_B_Adhes: BoardLayer
BL_F_Adhes: BoardLayer
BL_B_Paste: BoardLayer
BL_F_Paste: BoardLayer
BL_B_SilkS: BoardLayer
BL_F_SilkS: BoardLayer
BL_B_Mask: BoardLayer
BL_F_Mask: BoardLayer
BL_Dwgs_User: BoardLayer
BL_Cmts_User: BoardLayer
BL_Eco1_User: BoardLayer
BL_Eco2_User: BoardLayer
BL_Edge_Cuts: BoardLayer
BL_Margin: BoardLayer
BL_B_CrtYd: BoardLayer
BL_F_CrtYd: BoardLayer
BL_B_Fab: BoardLayer
BL_F_Fab: BoardLayer
BL_User_1: BoardLayer
BL_User_2: BoardLayer
BL_User_3: BoardLayer
BL_User_4: BoardLayer
BL_User_5: BoardLayer
BL_User_6: BoardLayer
BL_User_7: BoardLayer
BL_User_8: BoardLayer
BL_User_9: BoardLayer
BL_Rescue: BoardLayer
BL_User_10: BoardLayer
BL_User_11: BoardLayer
BL_User_12: BoardLayer
BL_User_13: BoardLayer
BL_User_14: BoardLayer
BL_User_15: BoardLayer
BL_User_16: BoardLayer
BL_User_17: BoardLayer
BL_User_18: BoardLayer
BL_User_19: BoardLayer
BL_User_20: BoardLayer
BL_User_21: BoardLayer
BL_User_22: BoardLayer
BL_User_23: BoardLayer
BL_User_24: BoardLayer
BL_User_25: BoardLayer
BL_User_26: BoardLayer
BL_User_27: BoardLayer
BL_User_28: BoardLayer
BL_User_29: BoardLayer
BL_User_30: BoardLayer
BL_User_31: BoardLayer
BL_User_32: BoardLayer
BL_User_33: BoardLayer
BL_User_34: BoardLayer
BL_User_35: BoardLayer
BL_User_36: BoardLayer
BL_User_37: BoardLayer
BL_User_38: BoardLayer
BL_User_39: BoardLayer
BL_User_40: BoardLayer
BL_User_41: BoardLayer
BL_User_42: BoardLayer
BL_User_43: BoardLayer
BL_User_44: BoardLayer
BL_User_45: BoardLayer
PST_UNKNOWN: PadStackType
PST_NORMAL: PadStackType
PST_FRONT_INNER_BACK: PadStackType
PST_CUSTOM: PadStackType
ULR_UNKNOWN: UnconnectedLayerRemoval
ULR_KEEP: UnconnectedLayerRemoval
ULR_REMOVE: UnconnectedLayerRemoval
ULR_REMOVE_EXCEPT_START_AND_END: UnconnectedLayerRemoval
ULR_START_END_ONLY: UnconnectedLayerRemoval
PSS_UNKNOWN: PadStackShape
PSS_CIRCLE: PadStackShape
PSS_RECTANGLE: PadStackShape
PSS_OVAL: PadStackShape
PSS_TRAPEZOID: PadStackShape
PSS_ROUNDRECT: PadStackShape
PSS_CHAMFEREDRECT: PadStackShape
PSS_CUSTOM: PadStackShape
ZCS_UNKNOWN: ZoneConnectionStyle
ZCS_INHERITED: ZoneConnectionStyle
ZCS_NONE: ZoneConnectionStyle
ZCS_THERMAL: ZoneConnectionStyle
ZCS_FULL: ZoneConnectionStyle
ZCS_PTH_THERMAL: ZoneConnectionStyle
SMM_UNKNOWN: SolderMaskMode
SMM_MASKED: SolderMaskMode
SMM_UNMASKED: SolderMaskMode
SMM_FROM_DESIGN_RULES: SolderMaskMode
VCM_UNKNOWN: ViaCoveringMode
VCM_COVERED: ViaCoveringMode
VCM_UNCOVERED: ViaCoveringMode
VCM_FROM_DESIGN_RULES: ViaCoveringMode
VPM_UNKNOWN: ViaPluggingMode
VPM_PLUGGED: ViaPluggingMode
VPM_UNPLUGGED: ViaPluggingMode
VPM_FROM_DESIGN_RULES: ViaPluggingMode
SPM_UNKNOWN: SolderPasteMode
SPM_PASTE: SolderPasteMode
SPM_NO_PASTE: SolderPasteMode
SPM_FROM_DESIGN_RULES: SolderPasteMode
DS_UNKNOWN: DrillShape
DS_CIRCLE: DrillShape
DS_OBLONG: DrillShape
DS_UNDEFINED: DrillShape
VDCM_UNKNOWN: ViaDrillCappingMode
VDCM_CAPPED: ViaDrillCappingMode
VDCM_UNCAPPED: ViaDrillCappingMode
VDCM_FROM_DESIGN_RULES: ViaDrillCappingMode
VDFM_UNKNOWN: ViaDrillFillingMode
VDFM_FILLED: ViaDrillFillingMode
VDFM_UNFILLED: ViaDrillFillingMode
VDFM_FROM_DESIGN_RULES: ViaDrillFillingMode
VDPM_UNKNOWN: ViaDrillPostMachiningMode
VDPM_NOT_POST_MACHINED: ViaDrillPostMachiningMode
VDPM_COUNTERBORE: ViaDrillPostMachiningMode
VDPM_COUNTERSINK: ViaDrillPostMachiningMode
VT_UNKNOWN: ViaType
VT_THROUGH: ViaType
VT_BLIND_BURIED: ViaType
VT_MICRO: ViaType
VT_BLIND: ViaType
VT_BURIED: ViaType
ZLO_UNKNOWN: ZoneLayerOverride
ZLO_NONE: ZoneLayerOverride
ZLO_FORCE_FLASHED: ZoneLayerOverride
ZLO_FORCE_NO_ZONE_CONNECTION: ZoneLayerOverride
BK_UNKNOWN: BarcodeKind
BK_CODE_39: BarcodeKind
BK_CODE_128: BarcodeKind
BK_DATA_MATRIX: BarcodeKind
BK_QR_CODE: BarcodeKind
BK_MICRO_QR_CODE: BarcodeKind
BEC_UNKNOWN: BarcodeErrorCorrection
BEC_L: BarcodeErrorCorrection
BEC_M: BarcodeErrorCorrection
BEC_Q: BarcodeErrorCorrection
BEC_H: BarcodeErrorCorrection
PT_UNKNOWN: PadType
PT_PTH: PadType
PT_SMD: PadType
PT_EDGE_CONNECTOR: PadType
PT_NPTH: PadType
PT_NON_COMPONENT: PadType
PSET_NONE: PadSimElectricalType
PSET_SOURCE: PadSimElectricalType
PSET_SINK: PadSimElectricalType
PFP_UNKNOWN: PadFabricationProperty
PFP_NONE: PadFabricationProperty
PFP_BGA: PadFabricationProperty
PFP_FIDUCIAL_GLOBAL: PadFabricationProperty
PFP_FIDUCIAL_LOCAL: PadFabricationProperty
PFP_TESTPOINT: PadFabricationProperty
PFP_HEATSINK: PadFabricationProperty
PFP_CASTELLATED: PadFabricationProperty
PFP_MECHANICAL: PadFabricationProperty
PFP_PRESSFIT: PadFabricationProperty
CPSZ_UNKNOWN: CustomPadShapeZoneFillStrategy
CPSZ_OUTLINE: CustomPadShapeZoneFillStrategy
CPSZ_CONVEXHULL: CustomPadShapeZoneFillStrategy
ZT_UNKNOWN: ZoneType
ZT_COPPER: ZoneType
ZT_GRAPHICAL: ZoneType
ZT_RULE_AREA: ZoneType
ZT_TEARDROP: ZoneType
ZTDT_UNKNOWN: ZoneTeardropType
ZTDT_NONE: ZoneTeardropType
ZTDT_UNSPECIFIED: ZoneTeardropType
ZTDT_VIA_PAD: ZoneTeardropType
ZTDT_TRACK_END: ZoneTeardropType
IRM_UNKNOWN: IslandRemovalMode
IRM_ALWAYS: IslandRemovalMode
IRM_NEVER: IslandRemovalMode
IRM_AREA: IslandRemovalMode
ZFM_UNKNOWN: ZoneFillMode
ZFM_SOLID: ZoneFillMode
ZFM_HATCHED: ZoneFillMode
ZFM_COPPER_THIEVING: ZoneFillMode
ZHS_UNKNOWN: ZoneHatchSmoothing
ZHS_NONE: ZoneHatchSmoothing
ZHS_FILLET: ZoneHatchSmoothing
ZHS_ARC_LOW_DEF: ZoneHatchSmoothing
ZHS_ARC_HIGH_DEF: ZoneHatchSmoothing
ZHFBM_UNKNOWN: ZoneHatchFillBorderMode
ZHFBM_USE_MIN_ZONE_THICKNESS: ZoneHatchFillBorderMode
ZHFBM_USE_HATCH_THICKNESS: ZoneHatchFillBorderMode
TP_UNKNOWN: ThievingPattern
TP_DOTS: ThievingPattern
TP_SQUARES: ThievingPattern
TP_CROSSHATCH: ThievingPattern
PTM_UNKNOWN: PadTeardropMode
PTM_DISABLED: PadTeardropMode
PTM_ENABLED: PadTeardropMode
ZCSM_UNKNOWN: ZoneCornerSmoothingMode
ZCSM_NONE: ZoneCornerSmoothingMode
ZCSM_CHAMFER: ZoneCornerSmoothingMode
ZCSM_FILLET: ZoneCornerSmoothingMode
PRST_UNKNOWN: PlacementRuleSourceType
PRST_SHEET_NAME: PlacementRuleSourceType
PRST_COMPONENT_CLASS: PlacementRuleSourceType
PRST_GROUP: PlacementRuleSourceType
PRST_DESIGN_BLOCK: PlacementRuleSourceType
ZBS_UNKNOWN: ZoneBorderStyle
ZBS_SOLID: ZoneBorderStyle
ZBS_DIAGONAL_FULL: ZoneBorderStyle
ZBS_DIAGONAL_EDGE: ZoneBorderStyle
ZBS_INVISIBLE: ZoneBorderStyle
DTBS_UNKNOWN: DimensionTextBorderStyle
DTBS_NONE: DimensionTextBorderStyle
DTBS_RECTANGLE: DimensionTextBorderStyle
DTBS_CIRCLE: DimensionTextBorderStyle
DTBS_ROUNDRECT: DimensionTextBorderStyle
DUF_UNKNOWN: DimensionUnitFormat
DUF_NO_SUFFIX: DimensionUnitFormat
DUF_BARE_SUFFIX: DimensionUnitFormat
DUF_PAREN_SUFFIX: DimensionUnitFormat
DAD_UNKNOWN: DimensionArrowDirection
DAD_INWARD: DimensionArrowDirection
DAD_OUTWARD: DimensionArrowDirection
DP_UNKNOWN: DimensionPrecision
DP_FIXED_0: DimensionPrecision
DP_FIXED_1: DimensionPrecision
DP_FIXED_2: DimensionPrecision
DP_FIXED_3: DimensionPrecision
DP_FIXED_4: DimensionPrecision
DP_FIXED_5: DimensionPrecision
DP_SCALED_IN_2: DimensionPrecision
DP_SCALED_IN_3: DimensionPrecision
DP_SCALED_IN_4: DimensionPrecision
DP_SCALED_IN_5: DimensionPrecision
DTP_UNKNOWN: DimensionTextPosition
DTP_OUTSIDE: DimensionTextPosition
DTP_INLINE: DimensionTextPosition
DTP_MANUAL: DimensionTextPosition
DU_UNKNOWN: DimensionUnit
DU_INCHES: DimensionUnit
DU_MILS: DimensionUnit
DU_MILLIMETERS: DimensionUnit
DU_AUTOMATIC: DimensionUnit
CT_UNKNOWN: ConstraintType
CT_COINCIDENT: ConstraintType
CT_HORIZONTAL: ConstraintType
CT_VERTICAL: ConstraintType
CT_PARALLEL: ConstraintType
CT_PERPENDICULAR: ConstraintType
CT_COLLINEAR: ConstraintType
CT_SYMMETRIC: ConstraintType
CT_EQUAL_LENGTH: ConstraintType
CT_EQUAL_RADIUS: ConstraintType
CT_POINT_ON_LINE: ConstraintType
CT_MIDPOINT: ConstraintType
CT_FIXED_POSITION: ConstraintType
CT_FIXED_LENGTH: ConstraintType
CT_CONCENTRIC: ConstraintType
CT_FIXED_RADIUS: ConstraintType
CT_ANGULAR_DIMENSION: ConstraintType
CT_TANGENT: ConstraintType
CT_ARC_ANGLE: ConstraintType
CA_UNKNOWN: ConstraintAnchor
CA_WHOLE: ConstraintAnchor
CA_START: ConstraintAnchor
CA_END: ConstraintAnchor
CA_MID: ConstraintAnchor
CA_CENTER: ConstraintAnchor
CA_RADIUS: ConstraintAnchor
CA_VERTEX: ConstraintAnchor
FMS_UNKNOWN: FootprintMountingStyle
FMS_THROUGH_HOLE: FootprintMountingStyle
FMS_SMD: FootprintMountingStyle
FMS_UNSPECIFIED: FootprintMountingStyle
BDK_UNKNOWN: Body3DKind
BDK_EXTRUDED: Body3DKind
BDK_MODEL: Body3DKind
EM_UNKNOWN: ExtrusionMaterial
EM_PLASTIC: ExtrusionMaterial
EM_MATTE: ExtrusionMaterial
EM_METAL: ExtrusionMaterial
EM_COPPER: ExtrusionMaterial
TSM_UNKNOWN: TableStrokeMode
TSM_DISABLED: TableStrokeMode
TSM_ENABLED: TableStrokeMode
DCC_UNKNOWN: DrillChartColumnId
DCC_SYMBOL: DrillChartColumnId
DCC_DRILL_DIAMETER: DrillChartColumnId
DCC_SLOT_SIZE: DrillChartColumnId
DCC_PLATING: DrillChartColumnId
DCC_OPERATION_COUNT: DrillChartColumnId
DCC_SITE_COUNT: DrillChartColumnId
DCC_LAYER_SPAN: DrillChartColumnId
DCC_OPERATION: DrillChartColumnId
DCC_PROTECTION: DrillChartColumnId
DCC_BACKDRILL_STUB: DrillChartColumnId
DCC_ASPECT_RATIO: DrillChartColumnId
DCC_DESCRIPTION: DrillChartColumnId
TPM_UNKNOWN: TuningPatternMode
TPM_SINGLE: TuningPatternMode
TPM_DIFF_PAIR: TuningPatternMode
TPM_DIFF_PAIR_SKEW: TuningPatternMode
TPMS_UNKNOWN: TuningPatternMeanderSide
TPMS_DEFAULT: TuningPatternMeanderSide
TPMS_LEFT: TuningPatternMeanderSide
TPMS_RIGHT: TuningPatternMeanderSide
TPCS_UNKNOWN: TuningPatternCornerStyle
TPCS_CHAMFERED: TuningPatternCornerStyle
TPCS_ROUNDED: TuningPatternCornerStyle
TPS_UNKNOWN: TuningPatternStatus
TPS_TOO_SHORT: TuningPatternStatus
TPS_TOO_LONG: TuningPatternStatus
TPS_TUNED: TuningPatternStatus
TPTM_UNKNOWN: TuningPatternTargetMode
TPTM_LENGTH: TuningPatternTargetMode
TPTM_TIME_DOMAIN: TuningPatternTargetMode
VSL_UNKNOWN: ViaStitchLayout
VSL_PLAIN: ViaStitchLayout
VSL_STAGGERED: ViaStitchLayout
VSL_POISSON: ViaStitchLayout
VSM_UNKNOWN: ViaStitchMode
VSM_STITCH: ViaStitchMode
VSM_GUARD: ViaStitchMode
VSK_UNKNOWN: ViaStackStyle
VSK_STACKED: ViaStackStyle
VSK_STAGGERED: ViaStackStyle
STC_UNKNOWN: StackupTableColumnId
STC_LAYER: StackupTableColumnId
STC_TYPE: StackupTableColumnId
STC_MATERIAL: StackupTableColumnId
STC_THICKNESS: StackupTableColumnId
STC_COLOR: StackupTableColumnId
STC_EPSILON_R: StackupTableColumnId
STC_LOSS_TANGENT: StackupTableColumnId

class NetCode(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class Net(_message.Message):
    __slots__ = ("code", "name")
    CODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    code: NetCode
    name: str
    def __init__(self, code: _Optional[_Union[NetCode, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class Track(_message.Message):
    __slots__ = ("id", "start", "end", "width", "locked", "layer", "net", "parent", "solder_mask", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    NET_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    SOLDER_MASK_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    start: _base_types_pb2.Vector2
    end: _base_types_pb2.Vector2
    width: _base_types_pb2.Distance
    locked: _base_types_pb2.LockedState
    layer: BoardLayer
    net: Net
    parent: _base_types_pb2.KIID
    solder_mask: SolderMaskOverrides
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., start: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., end: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., net: _Optional[_Union[Net, _Mapping]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., solder_mask: _Optional[_Union[SolderMaskOverrides, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class Arc(_message.Message):
    __slots__ = ("id", "start", "mid", "end", "width", "locked", "layer", "net", "parent", "solder_mask", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    MID_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    NET_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    SOLDER_MASK_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    start: _base_types_pb2.Vector2
    mid: _base_types_pb2.Vector2
    end: _base_types_pb2.Vector2
    width: _base_types_pb2.Distance
    locked: _base_types_pb2.LockedState
    layer: BoardLayer
    net: Net
    parent: _base_types_pb2.KIID
    solder_mask: SolderMaskOverrides
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., start: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., mid: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., end: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., net: _Optional[_Union[Net, _Mapping]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., solder_mask: _Optional[_Union[SolderMaskOverrides, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class ChamferedRectCorners(_message.Message):
    __slots__ = ("top_left", "top_right", "bottom_left", "bottom_right")
    TOP_LEFT_FIELD_NUMBER: _ClassVar[int]
    TOP_RIGHT_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_LEFT_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_RIGHT_FIELD_NUMBER: _ClassVar[int]
    top_left: bool
    top_right: bool
    bottom_left: bool
    bottom_right: bool
    def __init__(self, top_left: bool = ..., top_right: bool = ..., bottom_left: bool = ..., bottom_right: bool = ...) -> None: ...

class ZoneConnectionSettings(_message.Message):
    __slots__ = ("zone_connection", "thermal_spokes")
    ZONE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    THERMAL_SPOKES_FIELD_NUMBER: _ClassVar[int]
    zone_connection: ZoneConnectionStyle
    thermal_spokes: ThermalSpokeSettings
    def __init__(self, zone_connection: _Optional[_Union[ZoneConnectionStyle, str]] = ..., thermal_spokes: _Optional[_Union[ThermalSpokeSettings, _Mapping]] = ...) -> None: ...

class SolderMaskOverrides(_message.Message):
    __slots__ = ("solder_mask_margin", "expose_copper")
    SOLDER_MASK_MARGIN_FIELD_NUMBER: _ClassVar[int]
    EXPOSE_COPPER_FIELD_NUMBER: _ClassVar[int]
    solder_mask_margin: _base_types_pb2.Distance
    expose_copper: bool
    def __init__(self, solder_mask_margin: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., expose_copper: bool = ...) -> None: ...

class SolderPasteOverrides(_message.Message):
    __slots__ = ("solder_paste_margin", "solder_paste_margin_ratio")
    SOLDER_PASTE_MARGIN_FIELD_NUMBER: _ClassVar[int]
    SOLDER_PASTE_MARGIN_RATIO_FIELD_NUMBER: _ClassVar[int]
    solder_paste_margin: _base_types_pb2.Distance
    solder_paste_margin_ratio: _base_types_pb2.Ratio
    def __init__(self, solder_paste_margin: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., solder_paste_margin_ratio: _Optional[_Union[_base_types_pb2.Ratio, _Mapping]] = ...) -> None: ...

class PadStackLayer(_message.Message):
    __slots__ = ("layer", "shape", "size", "corner_rounding_ratio", "chamfer_ratio", "chamfered_corners", "custom_shapes", "custom_anchor_shape", "zone_settings", "trapezoid_delta", "offset")
    LAYER_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    CORNER_ROUNDING_RATIO_FIELD_NUMBER: _ClassVar[int]
    CHAMFER_RATIO_FIELD_NUMBER: _ClassVar[int]
    CHAMFERED_CORNERS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_SHAPES_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ANCHOR_SHAPE_FIELD_NUMBER: _ClassVar[int]
    ZONE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TRAPEZOID_DELTA_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    layer: BoardLayer
    shape: PadStackShape
    size: _base_types_pb2.Vector2
    corner_rounding_ratio: float
    chamfer_ratio: float
    chamfered_corners: ChamferedRectCorners
    custom_shapes: _containers.RepeatedCompositeFieldContainer[BoardGraphicShape]
    custom_anchor_shape: PadStackShape
    zone_settings: ZoneConnectionSettings
    trapezoid_delta: _base_types_pb2.Vector2
    offset: _base_types_pb2.Vector2
    def __init__(self, layer: _Optional[_Union[BoardLayer, str]] = ..., shape: _Optional[_Union[PadStackShape, str]] = ..., size: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., corner_rounding_ratio: _Optional[float] = ..., chamfer_ratio: _Optional[float] = ..., chamfered_corners: _Optional[_Union[ChamferedRectCorners, _Mapping]] = ..., custom_shapes: _Optional[_Iterable[_Union[BoardGraphicShape, _Mapping]]] = ..., custom_anchor_shape: _Optional[_Union[PadStackShape, str]] = ..., zone_settings: _Optional[_Union[ZoneConnectionSettings, _Mapping]] = ..., trapezoid_delta: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., offset: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ...) -> None: ...

class PadStackOuterLayer(_message.Message):
    __slots__ = ("solder_mask_mode", "solder_paste_mode", "solder_mask_settings", "solder_paste_settings", "plugging_mode", "covering_mode")
    SOLDER_MASK_MODE_FIELD_NUMBER: _ClassVar[int]
    SOLDER_PASTE_MODE_FIELD_NUMBER: _ClassVar[int]
    SOLDER_MASK_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    SOLDER_PASTE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLUGGING_MODE_FIELD_NUMBER: _ClassVar[int]
    COVERING_MODE_FIELD_NUMBER: _ClassVar[int]
    solder_mask_mode: SolderMaskMode
    solder_paste_mode: SolderPasteMode
    solder_mask_settings: SolderMaskOverrides
    solder_paste_settings: SolderPasteOverrides
    plugging_mode: ViaPluggingMode
    covering_mode: ViaCoveringMode
    def __init__(self, solder_mask_mode: _Optional[_Union[SolderMaskMode, str]] = ..., solder_paste_mode: _Optional[_Union[SolderPasteMode, str]] = ..., solder_mask_settings: _Optional[_Union[SolderMaskOverrides, _Mapping]] = ..., solder_paste_settings: _Optional[_Union[SolderPasteOverrides, _Mapping]] = ..., plugging_mode: _Optional[_Union[ViaPluggingMode, str]] = ..., covering_mode: _Optional[_Union[ViaCoveringMode, str]] = ...) -> None: ...

class DrillProperties(_message.Message):
    __slots__ = ("start_layer", "end_layer", "diameter", "shape", "capped", "filled")
    START_LAYER_FIELD_NUMBER: _ClassVar[int]
    END_LAYER_FIELD_NUMBER: _ClassVar[int]
    DIAMETER_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    CAPPED_FIELD_NUMBER: _ClassVar[int]
    FILLED_FIELD_NUMBER: _ClassVar[int]
    start_layer: BoardLayer
    end_layer: BoardLayer
    diameter: _base_types_pb2.Vector2
    shape: DrillShape
    capped: ViaDrillCappingMode
    filled: ViaDrillFillingMode
    def __init__(self, start_layer: _Optional[_Union[BoardLayer, str]] = ..., end_layer: _Optional[_Union[BoardLayer, str]] = ..., diameter: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., shape: _Optional[_Union[DrillShape, str]] = ..., capped: _Optional[_Union[ViaDrillCappingMode, str]] = ..., filled: _Optional[_Union[ViaDrillFillingMode, str]] = ...) -> None: ...

class PostMachiningProperties(_message.Message):
    __slots__ = ("mode", "size", "depth", "angle")
    MODE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    mode: ViaDrillPostMachiningMode
    size: _base_types_pb2.Distance
    depth: _base_types_pb2.Distance
    angle: _base_types_pb2.Angle
    def __init__(self, mode: _Optional[_Union[ViaDrillPostMachiningMode, str]] = ..., size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., depth: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., angle: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ...) -> None: ...

class PadStack(_message.Message):
    __slots__ = ("type", "layers", "drill", "unconnected_layer_removal", "copper_layers", "angle", "front_outer_layers", "back_outer_layers", "zone_settings", "secondary_drill", "tertiary_drill", "front_post_machining", "back_post_machining")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    DRILL_FIELD_NUMBER: _ClassVar[int]
    UNCONNECTED_LAYER_REMOVAL_FIELD_NUMBER: _ClassVar[int]
    COPPER_LAYERS_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    FRONT_OUTER_LAYERS_FIELD_NUMBER: _ClassVar[int]
    BACK_OUTER_LAYERS_FIELD_NUMBER: _ClassVar[int]
    ZONE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_DRILL_FIELD_NUMBER: _ClassVar[int]
    TERTIARY_DRILL_FIELD_NUMBER: _ClassVar[int]
    FRONT_POST_MACHINING_FIELD_NUMBER: _ClassVar[int]
    BACK_POST_MACHINING_FIELD_NUMBER: _ClassVar[int]
    type: PadStackType
    layers: _containers.RepeatedScalarFieldContainer[BoardLayer]
    drill: DrillProperties
    unconnected_layer_removal: UnconnectedLayerRemoval
    copper_layers: _containers.RepeatedCompositeFieldContainer[PadStackLayer]
    angle: _base_types_pb2.Angle
    front_outer_layers: PadStackOuterLayer
    back_outer_layers: PadStackOuterLayer
    zone_settings: ZoneConnectionSettings
    secondary_drill: DrillProperties
    tertiary_drill: DrillProperties
    front_post_machining: PostMachiningProperties
    back_post_machining: PostMachiningProperties
    def __init__(self, type: _Optional[_Union[PadStackType, str]] = ..., layers: _Optional[_Iterable[_Union[BoardLayer, str]]] = ..., drill: _Optional[_Union[DrillProperties, _Mapping]] = ..., unconnected_layer_removal: _Optional[_Union[UnconnectedLayerRemoval, str]] = ..., copper_layers: _Optional[_Iterable[_Union[PadStackLayer, _Mapping]]] = ..., angle: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ..., front_outer_layers: _Optional[_Union[PadStackOuterLayer, _Mapping]] = ..., back_outer_layers: _Optional[_Union[PadStackOuterLayer, _Mapping]] = ..., zone_settings: _Optional[_Union[ZoneConnectionSettings, _Mapping]] = ..., secondary_drill: _Optional[_Union[DrillProperties, _Mapping]] = ..., tertiary_drill: _Optional[_Union[DrillProperties, _Mapping]] = ..., front_post_machining: _Optional[_Union[PostMachiningProperties, _Mapping]] = ..., back_post_machining: _Optional[_Union[PostMachiningProperties, _Mapping]] = ...) -> None: ...

class ZoneLayerOverrideEntry(_message.Message):
    __slots__ = ("layer", "override")
    LAYER_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    layer: BoardLayer
    override: ZoneLayerOverride
    def __init__(self, layer: _Optional[_Union[BoardLayer, str]] = ..., override: _Optional[_Union[ZoneLayerOverride, str]] = ...) -> None: ...

class Via(_message.Message):
    __slots__ = ("id", "position", "pad_stack", "locked", "net", "type", "parent", "teardrop", "zone_layer_overrides", "is_free", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    PAD_STACK_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    NET_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    TEARDROP_FIELD_NUMBER: _ClassVar[int]
    ZONE_LAYER_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    IS_FREE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    pad_stack: PadStack
    locked: _base_types_pb2.LockedState
    net: Net
    type: ViaType
    parent: _base_types_pb2.KIID
    teardrop: PadTeardropSettings
    zone_layer_overrides: _containers.RepeatedCompositeFieldContainer[ZoneLayerOverrideEntry]
    is_free: bool
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., pad_stack: _Optional[_Union[PadStack, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., net: _Optional[_Union[Net, _Mapping]] = ..., type: _Optional[_Union[ViaType, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., teardrop: _Optional[_Union[PadTeardropSettings, _Mapping]] = ..., zone_layer_overrides: _Optional[_Iterable[_Union[ZoneLayerOverrideEntry, _Mapping]]] = ..., is_free: bool = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class BoardGraphicShape(_message.Message):
    __slots__ = ("shape", "layer", "net", "id", "locked", "parent", "solder_mask", "custom_properties", "pad_custom_shape_options")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    NET_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    SOLDER_MASK_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PAD_CUSTOM_SHAPE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    shape: _base_types_pb2.GraphicShape
    layer: BoardLayer
    net: Net
    id: _base_types_pb2.KIID
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    solder_mask: SolderMaskOverrides
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    pad_custom_shape_options: PadCustomShapeOptions
    def __init__(self, shape: _Optional[_Union[_base_types_pb2.GraphicShape, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., net: _Optional[_Union[Net, _Mapping]] = ..., id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., solder_mask: _Optional[_Union[SolderMaskOverrides, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ..., pad_custom_shape_options: _Optional[_Union[PadCustomShapeOptions, _Mapping]] = ...) -> None: ...

class PadCustomShapeOptions(_message.Message):
    __slots__ = ("is_number_box", "is_thermal_spoke_template")
    IS_NUMBER_BOX_FIELD_NUMBER: _ClassVar[int]
    IS_THERMAL_SPOKE_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    is_number_box: bool
    is_thermal_spoke_template: bool
    def __init__(self, is_number_box: bool = ..., is_thermal_spoke_template: bool = ...) -> None: ...

class Barcode(_message.Message):
    __slots__ = ("id", "text", "kind", "error_correction", "position", "orientation", "layer", "width", "height", "show_text", "text_height", "knockout", "knockout_margin", "locked", "parent", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ERROR_CORRECTION_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SHOW_TEXT_FIELD_NUMBER: _ClassVar[int]
    TEXT_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    KNOCKOUT_FIELD_NUMBER: _ClassVar[int]
    KNOCKOUT_MARGIN_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    text: str
    kind: BarcodeKind
    error_correction: BarcodeErrorCorrection
    position: _base_types_pb2.Vector2
    orientation: _base_types_pb2.Angle
    layer: BoardLayer
    width: _base_types_pb2.Distance
    height: _base_types_pb2.Distance
    show_text: bool
    text_height: _base_types_pb2.Distance
    knockout: bool
    knockout_margin: _base_types_pb2.Vector2
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., text: _Optional[str] = ..., kind: _Optional[_Union[BarcodeKind, str]] = ..., error_correction: _Optional[_Union[BarcodeErrorCorrection, str]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., orientation: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., show_text: bool = ..., text_height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., knockout: bool = ..., knockout_margin: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class BoardText(_message.Message):
    __slots__ = ("id", "text", "layer", "knockout", "locked", "parent", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    KNOCKOUT_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    text: _base_types_pb2.Text
    layer: BoardLayer
    knockout: bool
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., knockout: bool = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class BoardTextBox(_message.Message):
    __slots__ = ("id", "textbox", "layer", "locked", "parent", "knockout", "custom_properties", "border_stroke")
    ID_FIELD_NUMBER: _ClassVar[int]
    TEXTBOX_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    KNOCKOUT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    BORDER_STROKE_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    textbox: _base_types_pb2.TextBox
    layer: BoardLayer
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    knockout: bool
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    border_stroke: _base_types_pb2.StrokeAttributes
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., textbox: _Optional[_Union[_base_types_pb2.TextBox, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., knockout: bool = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ..., border_stroke: _Optional[_Union[_base_types_pb2.StrokeAttributes, _Mapping]] = ...) -> None: ...

class ThermalSpokeSettings(_message.Message):
    __slots__ = ("width", "angle", "gap")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    GAP_FIELD_NUMBER: _ClassVar[int]
    width: _base_types_pb2.Distance
    angle: _base_types_pb2.Angle
    gap: _base_types_pb2.Distance
    def __init__(self, width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., angle: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ..., gap: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class SymbolPinInfo(_message.Message):
    __slots__ = ("name", "type", "no_connect")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NO_CONNECT_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: _base_types_pb2.ElectricalPinType
    no_connect: bool
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[_base_types_pb2.ElectricalPinType, str]] = ..., no_connect: bool = ...) -> None: ...

class Pad(_message.Message):
    __slots__ = ("id", "locked", "number", "net", "type", "pad_stack", "position", "copper_clearance_override", "pad_to_die_length", "symbol_pin", "pad_to_die_delay", "sim_electrical_type", "parent", "teardrop", "zone_layer_overrides", "fab_property", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    NET_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PAD_STACK_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    COPPER_CLEARANCE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    PAD_TO_DIE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_PIN_FIELD_NUMBER: _ClassVar[int]
    PAD_TO_DIE_DELAY_FIELD_NUMBER: _ClassVar[int]
    SIM_ELECTRICAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    TEARDROP_FIELD_NUMBER: _ClassVar[int]
    ZONE_LAYER_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    FAB_PROPERTY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    locked: _base_types_pb2.LockedState
    number: str
    net: Net
    type: PadType
    pad_stack: PadStack
    position: _base_types_pb2.Vector2
    copper_clearance_override: _base_types_pb2.Distance
    pad_to_die_length: _base_types_pb2.Distance
    symbol_pin: SymbolPinInfo
    pad_to_die_delay: _base_types_pb2.Time
    sim_electrical_type: PadSimElectricalType
    parent: _base_types_pb2.KIID
    teardrop: PadTeardropSettings
    zone_layer_overrides: _containers.RepeatedCompositeFieldContainer[ZoneLayerOverrideEntry]
    fab_property: PadFabricationProperty
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., number: _Optional[str] = ..., net: _Optional[_Union[Net, _Mapping]] = ..., type: _Optional[_Union[PadType, str]] = ..., pad_stack: _Optional[_Union[PadStack, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., copper_clearance_override: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., pad_to_die_length: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., symbol_pin: _Optional[_Union[SymbolPinInfo, _Mapping]] = ..., pad_to_die_delay: _Optional[_Union[_base_types_pb2.Time, _Mapping]] = ..., sim_electrical_type: _Optional[_Union[PadSimElectricalType, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., teardrop: _Optional[_Union[PadTeardropSettings, _Mapping]] = ..., zone_layer_overrides: _Optional[_Iterable[_Union[ZoneLayerOverrideEntry, _Mapping]]] = ..., fab_property: _Optional[_Union[PadFabricationProperty, str]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class HatchFillSettings(_message.Message):
    __slots__ = ("thickness", "gap", "orientation", "hatch_smoothing_ratio", "hatch_hole_min_area_ratio", "border_mode")
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    GAP_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    HATCH_SMOOTHING_RATIO_FIELD_NUMBER: _ClassVar[int]
    HATCH_HOLE_MIN_AREA_RATIO_FIELD_NUMBER: _ClassVar[int]
    BORDER_MODE_FIELD_NUMBER: _ClassVar[int]
    thickness: _base_types_pb2.Distance
    gap: _base_types_pb2.Distance
    orientation: _base_types_pb2.Angle
    hatch_smoothing_ratio: float
    hatch_hole_min_area_ratio: float
    border_mode: ZoneHatchFillBorderMode
    def __init__(self, thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., gap: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., orientation: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ..., hatch_smoothing_ratio: _Optional[float] = ..., hatch_hole_min_area_ratio: _Optional[float] = ..., border_mode: _Optional[_Union[ZoneHatchFillBorderMode, str]] = ...) -> None: ...

class ThievingFillSettings(_message.Message):
    __slots__ = ("pattern", "element_size", "gap", "line_width", "stagger", "orientation")
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_SIZE_FIELD_NUMBER: _ClassVar[int]
    GAP_FIELD_NUMBER: _ClassVar[int]
    LINE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    STAGGER_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    pattern: ThievingPattern
    element_size: _base_types_pb2.Distance
    gap: _base_types_pb2.Distance
    line_width: _base_types_pb2.Distance
    stagger: bool
    orientation: _base_types_pb2.Angle
    def __init__(self, pattern: _Optional[_Union[ThievingPattern, str]] = ..., element_size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., gap: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., line_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., stagger: bool = ..., orientation: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ...) -> None: ...

class ZoneTeardropSettings(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: ZoneTeardropType
    def __init__(self, type: _Optional[_Union[ZoneTeardropType, str]] = ...) -> None: ...

class PadTeardropSettings(_message.Message):
    __slots__ = ("mode", "curved_edges", "allow_multiple_track_segments", "prefer_zone_connection", "max_length", "max_width", "best_length_ratio", "best_width_ratio", "max_track_width_ratio")
    MODE_FIELD_NUMBER: _ClassVar[int]
    CURVED_EDGES_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MULTIPLE_TRACK_SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    PREFER_ZONE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_WIDTH_FIELD_NUMBER: _ClassVar[int]
    BEST_LENGTH_RATIO_FIELD_NUMBER: _ClassVar[int]
    BEST_WIDTH_RATIO_FIELD_NUMBER: _ClassVar[int]
    MAX_TRACK_WIDTH_RATIO_FIELD_NUMBER: _ClassVar[int]
    mode: PadTeardropMode
    curved_edges: bool
    allow_multiple_track_segments: bool
    prefer_zone_connection: bool
    max_length: _base_types_pb2.Distance
    max_width: _base_types_pb2.Distance
    best_length_ratio: float
    best_width_ratio: float
    max_track_width_ratio: float
    def __init__(self, mode: _Optional[_Union[PadTeardropMode, str]] = ..., curved_edges: bool = ..., allow_multiple_track_segments: bool = ..., prefer_zone_connection: bool = ..., max_length: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., max_width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., best_length_ratio: _Optional[float] = ..., best_width_ratio: _Optional[float] = ..., max_track_width_ratio: _Optional[float] = ...) -> None: ...

class CopperZoneSettings(_message.Message):
    __slots__ = ("connection", "clearance", "min_thickness", "island_mode", "min_island_area", "fill_mode", "hatch_settings", "net", "teardrop", "thieving_settings", "corner_smoothing", "corner_radius")
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    MIN_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    ISLAND_MODE_FIELD_NUMBER: _ClassVar[int]
    MIN_ISLAND_AREA_FIELD_NUMBER: _ClassVar[int]
    FILL_MODE_FIELD_NUMBER: _ClassVar[int]
    HATCH_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    NET_FIELD_NUMBER: _ClassVar[int]
    TEARDROP_FIELD_NUMBER: _ClassVar[int]
    THIEVING_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    CORNER_SMOOTHING_FIELD_NUMBER: _ClassVar[int]
    CORNER_RADIUS_FIELD_NUMBER: _ClassVar[int]
    connection: ZoneConnectionSettings
    clearance: _base_types_pb2.Distance
    min_thickness: _base_types_pb2.Distance
    island_mode: IslandRemovalMode
    min_island_area: int
    fill_mode: ZoneFillMode
    hatch_settings: HatchFillSettings
    net: Net
    teardrop: ZoneTeardropSettings
    thieving_settings: ThievingFillSettings
    corner_smoothing: ZoneCornerSmoothingMode
    corner_radius: _base_types_pb2.Distance
    def __init__(self, connection: _Optional[_Union[ZoneConnectionSettings, _Mapping]] = ..., clearance: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., island_mode: _Optional[_Union[IslandRemovalMode, str]] = ..., min_island_area: _Optional[int] = ..., fill_mode: _Optional[_Union[ZoneFillMode, str]] = ..., hatch_settings: _Optional[_Union[HatchFillSettings, _Mapping]] = ..., net: _Optional[_Union[Net, _Mapping]] = ..., teardrop: _Optional[_Union[ZoneTeardropSettings, _Mapping]] = ..., thieving_settings: _Optional[_Union[ThievingFillSettings, _Mapping]] = ..., corner_smoothing: _Optional[_Union[ZoneCornerSmoothingMode, str]] = ..., corner_radius: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class RuleAreaSettings(_message.Message):
    __slots__ = ("keepout_copper", "keepout_vias", "keepout_tracks", "keepout_pads", "keepout_footprints", "placement_enabled", "placement_source_type", "placement_source")
    KEEPOUT_COPPER_FIELD_NUMBER: _ClassVar[int]
    KEEPOUT_VIAS_FIELD_NUMBER: _ClassVar[int]
    KEEPOUT_TRACKS_FIELD_NUMBER: _ClassVar[int]
    KEEPOUT_PADS_FIELD_NUMBER: _ClassVar[int]
    KEEPOUT_FOOTPRINTS_FIELD_NUMBER: _ClassVar[int]
    PLACEMENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PLACEMENT_SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLACEMENT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    keepout_copper: bool
    keepout_vias: bool
    keepout_tracks: bool
    keepout_pads: bool
    keepout_footprints: bool
    placement_enabled: bool
    placement_source_type: PlacementRuleSourceType
    placement_source: str
    def __init__(self, keepout_copper: bool = ..., keepout_vias: bool = ..., keepout_tracks: bool = ..., keepout_pads: bool = ..., keepout_footprints: bool = ..., placement_enabled: bool = ..., placement_source_type: _Optional[_Union[PlacementRuleSourceType, str]] = ..., placement_source: _Optional[str] = ...) -> None: ...

class ZoneBorderSettings(_message.Message):
    __slots__ = ("style", "pitch")
    STYLE_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    style: ZoneBorderStyle
    pitch: _base_types_pb2.Distance
    def __init__(self, style: _Optional[_Union[ZoneBorderStyle, str]] = ..., pitch: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class ZoneFilledPolygons(_message.Message):
    __slots__ = ("layer", "shapes")
    LAYER_FIELD_NUMBER: _ClassVar[int]
    SHAPES_FIELD_NUMBER: _ClassVar[int]
    layer: BoardLayer
    shapes: _base_types_pb2.PolySet
    def __init__(self, layer: _Optional[_Union[BoardLayer, str]] = ..., shapes: _Optional[_Union[_base_types_pb2.PolySet, _Mapping]] = ...) -> None: ...

class ZoneLayerProperties(_message.Message):
    __slots__ = ("layer", "hatching_offset")
    LAYER_FIELD_NUMBER: _ClassVar[int]
    HATCHING_OFFSET_FIELD_NUMBER: _ClassVar[int]
    layer: BoardLayer
    hatching_offset: _base_types_pb2.Vector2
    def __init__(self, layer: _Optional[_Union[BoardLayer, str]] = ..., hatching_offset: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ...) -> None: ...

class Zone(_message.Message):
    __slots__ = ("id", "type", "layers", "outline", "name", "copper_settings", "rule_area_settings", "priority", "filled", "filled_polygons", "border", "locked", "layer_properties", "parent", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    OUTLINE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COPPER_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    RULE_AREA_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    FILLED_FIELD_NUMBER: _ClassVar[int]
    FILLED_POLYGONS_FIELD_NUMBER: _ClassVar[int]
    BORDER_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    LAYER_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    type: ZoneType
    layers: _containers.RepeatedScalarFieldContainer[BoardLayer]
    outline: _base_types_pb2.PolySet
    name: str
    copper_settings: CopperZoneSettings
    rule_area_settings: RuleAreaSettings
    priority: int
    filled: bool
    filled_polygons: _containers.RepeatedCompositeFieldContainer[ZoneFilledPolygons]
    border: ZoneBorderSettings
    locked: _base_types_pb2.LockedState
    layer_properties: _containers.RepeatedCompositeFieldContainer[ZoneLayerProperties]
    parent: _base_types_pb2.KIID
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., type: _Optional[_Union[ZoneType, str]] = ..., layers: _Optional[_Iterable[_Union[BoardLayer, str]]] = ..., outline: _Optional[_Union[_base_types_pb2.PolySet, _Mapping]] = ..., name: _Optional[str] = ..., copper_settings: _Optional[_Union[CopperZoneSettings, _Mapping]] = ..., rule_area_settings: _Optional[_Union[RuleAreaSettings, _Mapping]] = ..., priority: _Optional[int] = ..., filled: bool = ..., filled_polygons: _Optional[_Iterable[_Union[ZoneFilledPolygons, _Mapping]]] = ..., border: _Optional[_Union[ZoneBorderSettings, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., layer_properties: _Optional[_Iterable[_Union[ZoneLayerProperties, _Mapping]]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class AlignedDimensionAttributes(_message.Message):
    __slots__ = ("start", "end", "height", "extension_height")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    start: _base_types_pb2.Vector2
    end: _base_types_pb2.Vector2
    height: _base_types_pb2.Distance
    extension_height: _base_types_pb2.Distance
    def __init__(self, start: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., end: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., extension_height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class OrthogonalDimensionAttributes(_message.Message):
    __slots__ = ("start", "end", "height", "extension_height", "alignment")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    start: _base_types_pb2.Vector2
    end: _base_types_pb2.Vector2
    height: _base_types_pb2.Distance
    extension_height: _base_types_pb2.Distance
    alignment: _base_types_pb2.AxisAlignment
    def __init__(self, start: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., end: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., extension_height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., alignment: _Optional[_Union[_base_types_pb2.AxisAlignment, str]] = ...) -> None: ...

class RadialDimensionAttributes(_message.Message):
    __slots__ = ("center", "radius_point", "leader_length")
    CENTER_FIELD_NUMBER: _ClassVar[int]
    RADIUS_POINT_FIELD_NUMBER: _ClassVar[int]
    LEADER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    center: _base_types_pb2.Vector2
    radius_point: _base_types_pb2.Vector2
    leader_length: _base_types_pb2.Distance
    def __init__(self, center: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., radius_point: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., leader_length: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class LeaderDimensionAttributes(_message.Message):
    __slots__ = ("start", "end", "border_style")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    BORDER_STYLE_FIELD_NUMBER: _ClassVar[int]
    start: _base_types_pb2.Vector2
    end: _base_types_pb2.Vector2
    border_style: DimensionTextBorderStyle
    def __init__(self, start: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., end: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., border_style: _Optional[_Union[DimensionTextBorderStyle, str]] = ...) -> None: ...

class CenterDimensionAttributes(_message.Message):
    __slots__ = ("center", "end")
    CENTER_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    center: _base_types_pb2.Vector2
    end: _base_types_pb2.Vector2
    def __init__(self, center: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., end: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ...) -> None: ...

class Dimension(_message.Message):
    __slots__ = ("id", "locked", "layer", "text", "aligned", "orthogonal", "radial", "leader", "center", "override_text_enabled", "override_text", "prefix", "suffix", "unit", "unit_format", "arrow_direction", "precision", "suppress_trailing_zeroes", "line_thickness", "arrow_length", "extension_offset", "text_position", "keep_text_aligned", "parent", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    ALIGNED_FIELD_NUMBER: _ClassVar[int]
    ORTHOGONAL_FIELD_NUMBER: _ClassVar[int]
    RADIAL_FIELD_NUMBER: _ClassVar[int]
    LEADER_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_TEXT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_TEXT_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    UNIT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    ARROW_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_TRAILING_ZEROES_FIELD_NUMBER: _ClassVar[int]
    LINE_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    ARROW_LENGTH_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_OFFSET_FIELD_NUMBER: _ClassVar[int]
    TEXT_POSITION_FIELD_NUMBER: _ClassVar[int]
    KEEP_TEXT_ALIGNED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    locked: _base_types_pb2.LockedState
    layer: BoardLayer
    text: _base_types_pb2.Text
    aligned: AlignedDimensionAttributes
    orthogonal: OrthogonalDimensionAttributes
    radial: RadialDimensionAttributes
    leader: LeaderDimensionAttributes
    center: CenterDimensionAttributes
    override_text_enabled: bool
    override_text: str
    prefix: str
    suffix: str
    unit: DimensionUnit
    unit_format: DimensionUnitFormat
    arrow_direction: DimensionArrowDirection
    precision: DimensionPrecision
    suppress_trailing_zeroes: bool
    line_thickness: _base_types_pb2.Distance
    arrow_length: _base_types_pb2.Distance
    extension_offset: _base_types_pb2.Distance
    text_position: DimensionTextPosition
    keep_text_aligned: bool
    parent: _base_types_pb2.KIID
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., text: _Optional[_Union[_base_types_pb2.Text, _Mapping]] = ..., aligned: _Optional[_Union[AlignedDimensionAttributes, _Mapping]] = ..., orthogonal: _Optional[_Union[OrthogonalDimensionAttributes, _Mapping]] = ..., radial: _Optional[_Union[RadialDimensionAttributes, _Mapping]] = ..., leader: _Optional[_Union[LeaderDimensionAttributes, _Mapping]] = ..., center: _Optional[_Union[CenterDimensionAttributes, _Mapping]] = ..., override_text_enabled: bool = ..., override_text: _Optional[str] = ..., prefix: _Optional[str] = ..., suffix: _Optional[str] = ..., unit: _Optional[_Union[DimensionUnit, str]] = ..., unit_format: _Optional[_Union[DimensionUnitFormat, str]] = ..., arrow_direction: _Optional[_Union[DimensionArrowDirection, str]] = ..., precision: _Optional[_Union[DimensionPrecision, str]] = ..., suppress_trailing_zeroes: bool = ..., line_thickness: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., arrow_length: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., extension_offset: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., text_position: _Optional[_Union[DimensionTextPosition, str]] = ..., keep_text_aligned: bool = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class ReferenceImage(_message.Message):
    __slots__ = ("id", "layer", "position", "transform_origin_offset", "image_scale", "image_data", "locked", "parent", "custom_properties", "orientation", "opacity")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_ORIGIN_OFFSET_FIELD_NUMBER: _ClassVar[int]
    IMAGE_SCALE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    OPACITY_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    layer: BoardLayer
    position: _base_types_pb2.Vector2
    transform_origin_offset: _base_types_pb2.Vector2
    image_scale: _base_types_pb2.Ratio
    image_data: bytes
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    orientation: _base_types_pb2.Angle
    opacity: float
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., transform_origin_offset: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., image_scale: _Optional[_Union[_base_types_pb2.Ratio, _Mapping]] = ..., image_data: _Optional[bytes] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ..., orientation: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ..., opacity: _Optional[float] = ...) -> None: ...

class GridItemAffects(_message.Message):
    __slots__ = ("cursor", "routing", "placement")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    ROUTING_FIELD_NUMBER: _ClassVar[int]
    PLACEMENT_FIELD_NUMBER: _ClassVar[int]
    cursor: bool
    routing: bool
    placement: bool
    def __init__(self, cursor: bool = ..., routing: bool = ..., placement: bool = ...) -> None: ...

class CartesianGridItemAttributes(_message.Message):
    __slots__ = ("extent", "spacing")
    EXTENT_FIELD_NUMBER: _ClassVar[int]
    SPACING_FIELD_NUMBER: _ClassVar[int]
    extent: _base_types_pb2.Vector2
    spacing: _base_types_pb2.Vector2
    def __init__(self, extent: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., spacing: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ...) -> None: ...

class PolarGridItemAttributes(_message.Message):
    __slots__ = ("radius_extent", "radius_spacing", "phi_extent", "phi_spacing")
    RADIUS_EXTENT_FIELD_NUMBER: _ClassVar[int]
    RADIUS_SPACING_FIELD_NUMBER: _ClassVar[int]
    PHI_EXTENT_FIELD_NUMBER: _ClassVar[int]
    PHI_SPACING_FIELD_NUMBER: _ClassVar[int]
    radius_extent: _base_types_pb2.Distance
    radius_spacing: _base_types_pb2.Distance
    phi_extent: _base_types_pb2.Angle
    phi_spacing: _base_types_pb2.Angle
    def __init__(self, radius_extent: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., radius_spacing: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., phi_extent: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ..., phi_spacing: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ...) -> None: ...

class GridItem(_message.Message):
    __slots__ = ("id", "position", "orientation", "cartesian", "polar", "priority", "tick_interval", "affects", "locked", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    CARTESIAN_FIELD_NUMBER: _ClassVar[int]
    POLAR_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TICK_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    AFFECTS_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    orientation: _base_types_pb2.Angle
    cartesian: CartesianGridItemAttributes
    polar: PolarGridItemAttributes
    priority: int
    tick_interval: int
    affects: GridItemAffects
    locked: _base_types_pb2.LockedState
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., orientation: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ..., cartesian: _Optional[_Union[CartesianGridItemAttributes, _Mapping]] = ..., polar: _Optional[_Union[PolarGridItemAttributes, _Mapping]] = ..., priority: _Optional[int] = ..., tick_interval: _Optional[int] = ..., affects: _Optional[_Union[GridItemAffects, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ("id", "name", "items", "parent", "locked", "lib_id", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    LIB_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    name: str
    items: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    parent: _base_types_pb2.KIID
    locked: _base_types_pb2.LockedState
    lib_id: _base_types_pb2.LibraryIdentifier
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., name: _Optional[str] = ..., items: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., lib_id: _Optional[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class ConstraintMember(_message.Message):
    __slots__ = ("item", "anchor", "index")
    ITEM_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    item: _base_types_pb2.KIID
    anchor: ConstraintAnchor
    index: int
    def __init__(self, item: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., anchor: _Optional[_Union[ConstraintAnchor, str]] = ..., index: _Optional[int] = ...) -> None: ...

class Constraint(_message.Message):
    __slots__ = ("id", "type", "members", "value", "driving", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DRIVING_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    type: ConstraintType
    members: _containers.RepeatedCompositeFieldContainer[ConstraintMember]
    value: float
    driving: bool
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., type: _Optional[_Union[ConstraintType, str]] = ..., members: _Optional[_Iterable[_Union[ConstraintMember, _Mapping]]] = ..., value: _Optional[float] = ..., driving: bool = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class FieldId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class Field(_message.Message):
    __slots__ = ("id", "name", "text", "visible", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: FieldId
    name: str
    text: BoardText
    visible: bool
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[FieldId, _Mapping]] = ..., name: _Optional[str] = ..., text: _Optional[_Union[BoardText, _Mapping]] = ..., visible: bool = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class FootprintAttributes(_message.Message):
    __slots__ = ("description", "keywords", "not_in_schematic", "exclude_from_position_files", "exclude_from_bill_of_materials", "exempt_from_courtyard_requirement", "do_not_populate", "mounting_style", "allow_soldermask_bridges", "exclude_from_simulation")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    NOT_IN_SCHEMATIC_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_POSITION_FILES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_BILL_OF_MATERIALS_FIELD_NUMBER: _ClassVar[int]
    EXEMPT_FROM_COURTYARD_REQUIREMENT_FIELD_NUMBER: _ClassVar[int]
    DO_NOT_POPULATE_FIELD_NUMBER: _ClassVar[int]
    MOUNTING_STYLE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_SOLDERMASK_BRIDGES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_SIMULATION_FIELD_NUMBER: _ClassVar[int]
    description: str
    keywords: str
    not_in_schematic: bool
    exclude_from_position_files: bool
    exclude_from_bill_of_materials: bool
    exempt_from_courtyard_requirement: bool
    do_not_populate: bool
    mounting_style: FootprintMountingStyle
    allow_soldermask_bridges: bool
    exclude_from_simulation: bool
    def __init__(self, description: _Optional[str] = ..., keywords: _Optional[str] = ..., not_in_schematic: bool = ..., exclude_from_position_files: bool = ..., exclude_from_bill_of_materials: bool = ..., exempt_from_courtyard_requirement: bool = ..., do_not_populate: bool = ..., mounting_style: _Optional[_Union[FootprintMountingStyle, str]] = ..., allow_soldermask_bridges: bool = ..., exclude_from_simulation: bool = ...) -> None: ...

class FootprintVariant(_message.Message):
    __slots__ = ("name", "do_not_populate", "exclude_from_bill_of_materials", "exclude_from_position_files", "exclude_from_simulation", "fields")
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DO_NOT_POPULATE_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_BILL_OF_MATERIALS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_POSITION_FILES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_SIMULATION_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    do_not_populate: bool
    exclude_from_bill_of_materials: bool
    exclude_from_position_files: bool
    exclude_from_simulation: bool
    fields: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., do_not_populate: bool = ..., exclude_from_bill_of_materials: bool = ..., exclude_from_position_files: bool = ..., exclude_from_simulation: bool = ..., fields: _Optional[_Mapping[str, str]] = ...) -> None: ...

class FootprintUnitInfo(_message.Message):
    __slots__ = ("name", "pin_numbers")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PIN_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    pin_numbers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., pin_numbers: _Optional[_Iterable[str]] = ...) -> None: ...

class NetTieDefinition(_message.Message):
    __slots__ = ("pad_number",)
    PAD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    pad_number: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pad_number: _Optional[_Iterable[str]] = ...) -> None: ...

class FootprintDesignRuleOverrides(_message.Message):
    __slots__ = ("solder_mask", "solder_paste", "copper_clearance", "zone_connection")
    SOLDER_MASK_FIELD_NUMBER: _ClassVar[int]
    SOLDER_PASTE_FIELD_NUMBER: _ClassVar[int]
    COPPER_CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    ZONE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    solder_mask: SolderMaskOverrides
    solder_paste: SolderPasteOverrides
    copper_clearance: _base_types_pb2.Distance
    zone_connection: ZoneConnectionStyle
    def __init__(self, solder_mask: _Optional[_Union[SolderMaskOverrides, _Mapping]] = ..., solder_paste: _Optional[_Union[SolderPasteOverrides, _Mapping]] = ..., copper_clearance: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., zone_connection: _Optional[_Union[ZoneConnectionStyle, str]] = ...) -> None: ...

class Footprint3DModel(_message.Message):
    __slots__ = ("filename", "scale", "rotation", "offset", "visible", "opacity")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    OPACITY_FIELD_NUMBER: _ClassVar[int]
    filename: str
    scale: _base_types_pb2.Vector3D
    rotation: _base_types_pb2.Vector3D
    offset: _base_types_pb2.Vector3D
    visible: bool
    opacity: float
    def __init__(self, filename: _Optional[str] = ..., scale: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., rotation: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., offset: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., visible: bool = ..., opacity: _Optional[float] = ...) -> None: ...

class ExtrudedBody(_message.Message):
    __slots__ = ("height", "standoff", "outline_layer", "material", "color")
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    STANDOFF_FIELD_NUMBER: _ClassVar[int]
    OUTLINE_LAYER_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    height: _base_types_pb2.Distance
    standoff: _base_types_pb2.Distance
    outline_layer: BoardLayer
    material: ExtrusionMaterial
    color: _base_types_pb2.Color
    def __init__(self, height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., standoff: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., outline_layer: _Optional[_Union[BoardLayer, str]] = ..., material: _Optional[_Union[ExtrusionMaterial, str]] = ..., color: _Optional[_Union[_base_types_pb2.Color, _Mapping]] = ...) -> None: ...

class Body3D(_message.Message):
    __slots__ = ("id", "parent", "kind", "scale", "rotation", "offset", "visible", "extruded")
    ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    EXTRUDED_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    parent: _base_types_pb2.KIID
    kind: Body3DKind
    scale: _base_types_pb2.Vector3D
    rotation: _base_types_pb2.Vector3D
    offset: _base_types_pb2.Vector3D
    visible: bool
    extruded: ExtrudedBody
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., kind: _Optional[_Union[Body3DKind, str]] = ..., scale: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., rotation: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., offset: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., visible: bool = ..., extruded: _Optional[_Union[ExtrudedBody, _Mapping]] = ...) -> None: ...

class JumperGroup(_message.Message):
    __slots__ = ("pad_names",)
    PAD_NAMES_FIELD_NUMBER: _ClassVar[int]
    pad_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pad_names: _Optional[_Iterable[str]] = ...) -> None: ...

class JumperSettings(_message.Message):
    __slots__ = ("duplicate_names_are_jumpered", "groups")
    DUPLICATE_NAMES_ARE_JUMPERED_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    duplicate_names_are_jumpered: bool
    groups: _containers.RepeatedCompositeFieldContainer[JumperGroup]
    def __init__(self, duplicate_names_are_jumpered: bool = ..., groups: _Optional[_Iterable[_Union[JumperGroup, _Mapping]]] = ...) -> None: ...

class Footprint(_message.Message):
    __slots__ = ("id", "anchor", "attributes", "overrides", "net_ties", "private_layers", "reference_field", "value_field", "datasheet_field", "description_field", "items", "jumpers", "height")
    ID_FIELD_NUMBER: _ClassVar[int]
    ANCHOR_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    NET_TIES_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_LAYERS_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_FIELD_NUMBER: _ClassVar[int]
    DATASHEET_FIELD_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    JUMPERS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.LibraryIdentifier
    anchor: _base_types_pb2.Vector2
    attributes: FootprintAttributes
    overrides: FootprintDesignRuleOverrides
    net_ties: _containers.RepeatedCompositeFieldContainer[NetTieDefinition]
    private_layers: _containers.RepeatedScalarFieldContainer[BoardLayer]
    reference_field: Field
    value_field: Field
    datasheet_field: Field
    description_field: Field
    items: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    jumpers: JumperSettings
    height: _base_types_pb2.Distance
    def __init__(self, id: _Optional[_Union[_base_types_pb2.LibraryIdentifier, _Mapping]] = ..., anchor: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., attributes: _Optional[_Union[FootprintAttributes, _Mapping]] = ..., overrides: _Optional[_Union[FootprintDesignRuleOverrides, _Mapping]] = ..., net_ties: _Optional[_Iterable[_Union[NetTieDefinition, _Mapping]]] = ..., private_layers: _Optional[_Iterable[_Union[BoardLayer, str]]] = ..., reference_field: _Optional[_Union[Field, _Mapping]] = ..., value_field: _Optional[_Union[Field, _Mapping]] = ..., datasheet_field: _Optional[_Union[Field, _Mapping]] = ..., description_field: _Optional[_Union[Field, _Mapping]] = ..., items: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ..., jumpers: _Optional[_Union[JumperSettings, _Mapping]] = ..., height: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class FootprintInstance(_message.Message):
    __slots__ = ("id", "position", "orientation", "layer", "locked", "definition", "reference_field", "value_field", "datasheet_field", "description_field", "attributes", "overrides", "symbol_path", "symbol_sheet_name", "symbol_sheet_filename", "symbol_footprint_filters", "parent", "embedded_files", "custom_properties", "variants", "symbol_units")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_FIELD_NUMBER: _ClassVar[int]
    DATASHEET_FIELD_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_PATH_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_SHEET_NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_SHEET_FILENAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FOOTPRINT_FILTERS_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    EMBEDDED_FILES_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    VARIANTS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_UNITS_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    position: _base_types_pb2.Vector2
    orientation: _base_types_pb2.Angle
    layer: BoardLayer
    locked: _base_types_pb2.LockedState
    definition: Footprint
    reference_field: Field
    value_field: Field
    datasheet_field: Field
    description_field: Field
    attributes: FootprintAttributes
    overrides: FootprintDesignRuleOverrides
    symbol_path: _base_types_pb2.SheetPath
    symbol_sheet_name: str
    symbol_sheet_filename: str
    symbol_footprint_filters: str
    parent: _base_types_pb2.KIID
    embedded_files: _embedded_files_pb2.EmbeddedFiles
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    variants: _containers.RepeatedCompositeFieldContainer[FootprintVariant]
    symbol_units: _containers.RepeatedCompositeFieldContainer[FootprintUnitInfo]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., orientation: _Optional[_Union[_base_types_pb2.Angle, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., definition: _Optional[_Union[Footprint, _Mapping]] = ..., reference_field: _Optional[_Union[Field, _Mapping]] = ..., value_field: _Optional[_Union[Field, _Mapping]] = ..., datasheet_field: _Optional[_Union[Field, _Mapping]] = ..., description_field: _Optional[_Union[Field, _Mapping]] = ..., attributes: _Optional[_Union[FootprintAttributes, _Mapping]] = ..., overrides: _Optional[_Union[FootprintDesignRuleOverrides, _Mapping]] = ..., symbol_path: _Optional[_Union[_base_types_pb2.SheetPath, _Mapping]] = ..., symbol_sheet_name: _Optional[str] = ..., symbol_sheet_filename: _Optional[str] = ..., symbol_footprint_filters: _Optional[str] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., embedded_files: _Optional[_Union[_embedded_files_pb2.EmbeddedFiles, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ..., variants: _Optional[_Iterable[_Union[FootprintVariant, _Mapping]]] = ..., symbol_units: _Optional[_Iterable[_Union[FootprintUnitInfo, _Mapping]]] = ...) -> None: ...

class TableCell(_message.Message):
    __slots__ = ("text_box", "column_span", "row_span", "custom_properties")
    TEXT_BOX_FIELD_NUMBER: _ClassVar[int]
    COLUMN_SPAN_FIELD_NUMBER: _ClassVar[int]
    ROW_SPAN_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    text_box: BoardTextBox
    column_span: int
    row_span: int
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, text_box: _Optional[_Union[BoardTextBox, _Mapping]] = ..., column_span: _Optional[int] = ..., row_span: _Optional[int] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class Table(_message.Message):
    __slots__ = ("id", "column_count", "column_widths", "row_heights", "layer", "locked", "cells", "external_border", "header_separator", "border_stroke", "row_separators", "column_separators", "separators_stroke", "parent", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    COLUMN_COUNT_FIELD_NUMBER: _ClassVar[int]
    COLUMN_WIDTHS_FIELD_NUMBER: _ClassVar[int]
    ROW_HEIGHTS_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_BORDER_FIELD_NUMBER: _ClassVar[int]
    HEADER_SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    BORDER_STROKE_FIELD_NUMBER: _ClassVar[int]
    ROW_SEPARATORS_FIELD_NUMBER: _ClassVar[int]
    COLUMN_SEPARATORS_FIELD_NUMBER: _ClassVar[int]
    SEPARATORS_STROKE_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    column_count: int
    column_widths: _containers.RepeatedScalarFieldContainer[int]
    row_heights: _containers.RepeatedScalarFieldContainer[int]
    layer: BoardLayer
    locked: _base_types_pb2.LockedState
    cells: _containers.RepeatedCompositeFieldContainer[TableCell]
    external_border: TableStrokeMode
    header_separator: TableStrokeMode
    border_stroke: _base_types_pb2.StrokeAttributes
    row_separators: TableStrokeMode
    column_separators: TableStrokeMode
    separators_stroke: _base_types_pb2.StrokeAttributes
    parent: _base_types_pb2.KIID
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., column_count: _Optional[int] = ..., column_widths: _Optional[_Iterable[int]] = ..., row_heights: _Optional[_Iterable[int]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., cells: _Optional[_Iterable[_Union[TableCell, _Mapping]]] = ..., external_border: _Optional[_Union[TableStrokeMode, str]] = ..., header_separator: _Optional[_Union[TableStrokeMode, str]] = ..., border_stroke: _Optional[_Union[_base_types_pb2.StrokeAttributes, _Mapping]] = ..., row_separators: _Optional[_Union[TableStrokeMode, str]] = ..., column_separators: _Optional[_Union[TableStrokeMode, str]] = ..., separators_stroke: _Optional[_Union[_base_types_pb2.StrokeAttributes, _Mapping]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class DrillChartColumn(_message.Message):
    __slots__ = ("id", "heading", "align", "width", "hidden")
    ID_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    id: DrillChartColumnId
    heading: str
    align: _enums_pb2.HorizontalAlignment
    width: _base_types_pb2.Distance
    hidden: bool
    def __init__(self, id: _Optional[_Union[DrillChartColumnId, str]] = ..., heading: _Optional[str] = ..., align: _Optional[_Union[_enums_pb2.HorizontalAlignment, str]] = ..., width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., hidden: bool = ...) -> None: ...

class DrillChartFilter(_message.Message):
    __slots__ = ("plated", "non_plated", "vias", "slots", "backdrills", "castellated")
    PLATED_FIELD_NUMBER: _ClassVar[int]
    NON_PLATED_FIELD_NUMBER: _ClassVar[int]
    VIAS_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    BACKDRILLS_FIELD_NUMBER: _ClassVar[int]
    CASTELLATED_FIELD_NUMBER: _ClassVar[int]
    plated: bool
    non_plated: bool
    vias: bool
    slots: bool
    backdrills: bool
    castellated: bool
    def __init__(self, plated: bool = ..., non_plated: bool = ..., vias: bool = ..., slots: bool = ..., backdrills: bool = ..., castellated: bool = ...) -> None: ...

class DrillSpan(_message.Message):
    __slots__ = ("start_layer", "end_layer", "is_backdrill", "is_non_plated")
    START_LAYER_FIELD_NUMBER: _ClassVar[int]
    END_LAYER_FIELD_NUMBER: _ClassVar[int]
    IS_BACKDRILL_FIELD_NUMBER: _ClassVar[int]
    IS_NON_PLATED_FIELD_NUMBER: _ClassVar[int]
    start_layer: BoardLayer
    end_layer: BoardLayer
    is_backdrill: bool
    is_non_plated: bool
    def __init__(self, start_layer: _Optional[_Union[BoardLayer, str]] = ..., end_layer: _Optional[_Union[BoardLayer, str]] = ..., is_backdrill: bool = ..., is_non_plated: bool = ...) -> None: ...

class DrillChart(_message.Message):
    __slots__ = ("table", "filter", "columns", "units", "precision", "show_totals", "row_shapes", "symbol_column", "row_keys")
    class RowShapesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class RowKeysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    TABLE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    SHOW_TOTALS_FIELD_NUMBER: _ClassVar[int]
    ROW_SHAPES_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_COLUMN_FIELD_NUMBER: _ClassVar[int]
    ROW_KEYS_FIELD_NUMBER: _ClassVar[int]
    table: Table
    filter: DrillChartFilter
    columns: _containers.RepeatedCompositeFieldContainer[DrillChartColumn]
    units: _enums_pb2.Units
    precision: int
    show_totals: bool
    row_shapes: _containers.ScalarMap[int, int]
    symbol_column: int
    row_keys: _containers.ScalarMap[int, str]
    def __init__(self, table: _Optional[_Union[Table, _Mapping]] = ..., filter: _Optional[_Union[DrillChartFilter, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[DrillChartColumn, _Mapping]]] = ..., units: _Optional[_Union[_enums_pb2.Units, str]] = ..., precision: _Optional[int] = ..., show_totals: bool = ..., row_shapes: _Optional[_Mapping[int, int]] = ..., symbol_column: _Optional[int] = ..., row_keys: _Optional[_Mapping[int, str]] = ...) -> None: ...

class DrillMap(_message.Message):
    __slots__ = ("id", "layer", "position", "locked", "all_spans", "span", "outline_slots", "guide_cross", "symbol_size")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    ALL_SPANS_FIELD_NUMBER: _ClassVar[int]
    SPAN_FIELD_NUMBER: _ClassVar[int]
    OUTLINE_SLOTS_FIELD_NUMBER: _ClassVar[int]
    GUIDE_CROSS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_SIZE_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    layer: BoardLayer
    position: _base_types_pb2.Vector2
    locked: _base_types_pb2.LockedState
    all_spans: bool
    span: DrillSpan
    outline_slots: bool
    guide_cross: bool
    symbol_size: _base_types_pb2.Distance
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., all_spans: bool = ..., span: _Optional[_Union[DrillSpan, _Mapping]] = ..., outline_slots: bool = ..., guide_cross: bool = ..., symbol_size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class ReferencePoint(_message.Message):
    __slots__ = ("id", "layer", "position", "size", "locked", "parent", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    layer: BoardLayer
    position: _base_types_pb2.Vector2
    size: _base_types_pb2.Distance
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., position: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class TimeRange(_message.Message):
    __slots__ = ("min_as", "opt_as", "max_as")
    MIN_AS_FIELD_NUMBER: _ClassVar[int]
    OPT_AS_FIELD_NUMBER: _ClassVar[int]
    MAX_AS_FIELD_NUMBER: _ClassVar[int]
    min_as: int
    opt_as: int
    max_as: int
    def __init__(self, min_as: _Optional[int] = ..., opt_as: _Optional[int] = ..., max_as: _Optional[int] = ...) -> None: ...

class TuningPatternSettings(_message.Message):
    __slots__ = ("initial_side", "corner_style", "corner_radius_percent", "single_sided", "max_amplitude", "min_amplitude", "min_spacing")
    INITIAL_SIDE_FIELD_NUMBER: _ClassVar[int]
    CORNER_STYLE_FIELD_NUMBER: _ClassVar[int]
    CORNER_RADIUS_PERCENT_FIELD_NUMBER: _ClassVar[int]
    SINGLE_SIDED_FIELD_NUMBER: _ClassVar[int]
    MAX_AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    MIN_AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    MIN_SPACING_FIELD_NUMBER: _ClassVar[int]
    initial_side: TuningPatternMeanderSide
    corner_style: TuningPatternCornerStyle
    corner_radius_percent: int
    single_sided: bool
    max_amplitude: _base_types_pb2.Distance
    min_amplitude: _base_types_pb2.Distance
    min_spacing: _base_types_pb2.Distance
    def __init__(self, initial_side: _Optional[_Union[TuningPatternMeanderSide, str]] = ..., corner_style: _Optional[_Union[TuningPatternCornerStyle, str]] = ..., corner_radius_percent: _Optional[int] = ..., single_sided: bool = ..., max_amplitude: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_amplitude: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., min_spacing: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ...) -> None: ...

class TuningPatternState(_message.Message):
    __slots__ = ("status", "tuning_value")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TUNING_VALUE_FIELD_NUMBER: _ClassVar[int]
    status: TuningPatternStatus
    tuning_value: int
    def __init__(self, status: _Optional[_Union[TuningPatternStatus, str]] = ..., tuning_value: _Optional[int] = ...) -> None: ...

class TuningPattern(_message.Message):
    __slots__ = ("id", "layer", "origin", "end", "mode", "settings", "target_mode", "target_length", "target_delay", "target_skew", "target_skew_delay", "override_custom_rules", "state", "locked", "parent", "members", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TARGET_MODE_FIELD_NUMBER: _ClassVar[int]
    TARGET_LENGTH_FIELD_NUMBER: _ClassVar[int]
    TARGET_DELAY_FIELD_NUMBER: _ClassVar[int]
    TARGET_SKEW_FIELD_NUMBER: _ClassVar[int]
    TARGET_SKEW_DELAY_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_CUSTOM_RULES_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    layer: BoardLayer
    origin: _base_types_pb2.Vector2
    end: _base_types_pb2.Vector2
    mode: TuningPatternMode
    settings: TuningPatternSettings
    target_mode: TuningPatternTargetMode
    target_length: _base_types_pb2.MinOptMax
    target_delay: TimeRange
    target_skew: _base_types_pb2.MinOptMax
    target_skew_delay: TimeRange
    override_custom_rules: bool
    state: TuningPatternState
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    members: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., origin: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., end: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., mode: _Optional[_Union[TuningPatternMode, str]] = ..., settings: _Optional[_Union[TuningPatternSettings, _Mapping]] = ..., target_mode: _Optional[_Union[TuningPatternTargetMode, str]] = ..., target_length: _Optional[_Union[_base_types_pb2.MinOptMax, _Mapping]] = ..., target_delay: _Optional[_Union[TimeRange, _Mapping]] = ..., target_skew: _Optional[_Union[_base_types_pb2.MinOptMax, _Mapping]] = ..., target_skew_delay: _Optional[_Union[TimeRange, _Mapping]] = ..., override_custom_rules: bool = ..., state: _Optional[_Union[TuningPatternState, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., members: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class GridCell(_message.Message):
    __slots__ = ("i", "j")
    I_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    i: int
    j: int
    def __init__(self, i: _Optional[int] = ..., j: _Optional[int] = ...) -> None: ...

class ViaStitchGridSettings(_message.Message):
    __slots__ = ("origin_offset", "seed", "excluded_cells")
    ORIGIN_OFFSET_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_CELLS_FIELD_NUMBER: _ClassVar[int]
    origin_offset: _base_types_pb2.Vector2
    seed: int
    excluded_cells: _containers.RepeatedCompositeFieldContainer[GridCell]
    def __init__(self, origin_offset: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., seed: _Optional[int] = ..., excluded_cells: _Optional[_Iterable[_Union[GridCell, _Mapping]]] = ...) -> None: ...

class ViaStitchGuardSettings(_message.Message):
    __slots__ = ("guarded_net",)
    GUARDED_NET_FIELD_NUMBER: _ClassVar[int]
    guarded_net: Net
    def __init__(self, guarded_net: _Optional[_Union[Net, _Mapping]] = ...) -> None: ...

class ViaStitchArea(_message.Message):
    __slots__ = ("id", "layer", "outline", "pitch", "layout", "mode", "grid_settings", "guard_settings", "net", "excluded_positions", "via_template", "locked", "parent", "members", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    OUTLINE_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    GRID_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    GUARD_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    NET_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    VIA_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    layer: BoardLayer
    outline: _base_types_pb2.PolySet
    pitch: _base_types_pb2.Distance
    layout: ViaStitchLayout
    mode: ViaStitchMode
    grid_settings: ViaStitchGridSettings
    guard_settings: ViaStitchGuardSettings
    net: Net
    excluded_positions: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.Vector2]
    via_template: Via
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    members: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., layer: _Optional[_Union[BoardLayer, str]] = ..., outline: _Optional[_Union[_base_types_pb2.PolySet, _Mapping]] = ..., pitch: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., layout: _Optional[_Union[ViaStitchLayout, str]] = ..., mode: _Optional[_Union[ViaStitchMode, str]] = ..., grid_settings: _Optional[_Union[ViaStitchGridSettings, _Mapping]] = ..., guard_settings: _Optional[_Union[ViaStitchGuardSettings, _Mapping]] = ..., net: _Optional[_Union[Net, _Mapping]] = ..., excluded_positions: _Optional[_Iterable[_Union[_base_types_pb2.Vector2, _Mapping]]] = ..., via_template: _Optional[_Union[Via, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., members: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class ViaStack(_message.Message):
    __slots__ = ("id", "start_layer", "end_layer", "style", "pitch", "filled", "capped", "via_size", "via_drill", "use_netclass", "preset_name", "hops", "net", "locked", "parent", "members", "custom_properties")
    ID_FIELD_NUMBER: _ClassVar[int]
    START_LAYER_FIELD_NUMBER: _ClassVar[int]
    END_LAYER_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    FILLED_FIELD_NUMBER: _ClassVar[int]
    CAPPED_FIELD_NUMBER: _ClassVar[int]
    VIA_SIZE_FIELD_NUMBER: _ClassVar[int]
    VIA_DRILL_FIELD_NUMBER: _ClassVar[int]
    USE_NETCLASS_FIELD_NUMBER: _ClassVar[int]
    PRESET_NAME_FIELD_NUMBER: _ClassVar[int]
    HOPS_FIELD_NUMBER: _ClassVar[int]
    NET_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    id: _base_types_pb2.KIID
    start_layer: BoardLayer
    end_layer: BoardLayer
    style: ViaStackStyle
    pitch: _base_types_pb2.Distance
    filled: bool
    capped: bool
    via_size: _base_types_pb2.Distance
    via_drill: _base_types_pb2.Distance
    use_netclass: bool
    preset_name: str
    hops: _base_types_pb2.PolyLine
    net: Net
    locked: _base_types_pb2.LockedState
    parent: _base_types_pb2.KIID
    members: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.KIID]
    custom_properties: _containers.RepeatedCompositeFieldContainer[_base_types_pb2.CustomProperty]
    def __init__(self, id: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., start_layer: _Optional[_Union[BoardLayer, str]] = ..., end_layer: _Optional[_Union[BoardLayer, str]] = ..., style: _Optional[_Union[ViaStackStyle, str]] = ..., pitch: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., filled: bool = ..., capped: bool = ..., via_size: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., via_drill: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., use_netclass: bool = ..., preset_name: _Optional[str] = ..., hops: _Optional[_Union[_base_types_pb2.PolyLine, _Mapping]] = ..., net: _Optional[_Union[Net, _Mapping]] = ..., locked: _Optional[_Union[_base_types_pb2.LockedState, str]] = ..., parent: _Optional[_Union[_base_types_pb2.KIID, _Mapping]] = ..., members: _Optional[_Iterable[_Union[_base_types_pb2.KIID, _Mapping]]] = ..., custom_properties: _Optional[_Iterable[_Union[_base_types_pb2.CustomProperty, _Mapping]]] = ...) -> None: ...

class StackupTableColumn(_message.Message):
    __slots__ = ("id", "heading", "align", "width", "hidden")
    ID_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    id: StackupTableColumnId
    heading: str
    align: _enums_pb2.HorizontalAlignment
    width: _base_types_pb2.Distance
    hidden: bool
    def __init__(self, id: _Optional[_Union[StackupTableColumnId, str]] = ..., heading: _Optional[str] = ..., align: _Optional[_Union[_enums_pb2.HorizontalAlignment, str]] = ..., width: _Optional[_Union[_base_types_pb2.Distance, _Mapping]] = ..., hidden: bool = ...) -> None: ...

class StackupTable(_message.Message):
    __slots__ = ("table", "columns", "units", "precision", "row_keys")
    class RowKeysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    TABLE_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    ROW_KEYS_FIELD_NUMBER: _ClassVar[int]
    table: Table
    columns: _containers.RepeatedCompositeFieldContainer[StackupTableColumn]
    units: _enums_pb2.Units
    precision: int
    row_keys: _containers.ScalarMap[int, str]
    def __init__(self, table: _Optional[_Union[Table, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[StackupTableColumn, _Mapping]]] = ..., units: _Optional[_Union[_enums_pb2.Units, str]] = ..., precision: _Optional[int] = ..., row_keys: _Optional[_Mapping[int, str]] = ...) -> None: ...
