from mp.common.types import base_types_pb2 as _base_types_pb2
from mp.common.types import jobs_pb2 as _jobs_pb2
from mp.common.types import enums_pb2 as _enums_pb2
from mp.board import board_types_pb2 as _board_types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlotDrillMarks(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PDM_UNKNOWN: _ClassVar[PlotDrillMarks]
    PDM_NONE: _ClassVar[PlotDrillMarks]
    PDM_SMALL: _ClassVar[PlotDrillMarks]
    PDM_FULL: _ClassVar[PlotDrillMarks]

class Board3DFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    B3D_UNKNOWN: _ClassVar[Board3DFormat]
    B3D_STEP: _ClassVar[Board3DFormat]
    B3D_STEPZ: _ClassVar[Board3DFormat]
    B3D_BREP: _ClassVar[Board3DFormat]
    B3D_XAO: _ClassVar[Board3DFormat]
    B3D_GLB: _ClassVar[Board3DFormat]
    B3D_VRML: _ClassVar[Board3DFormat]
    B3D_PLY: _ClassVar[Board3DFormat]
    B3D_STL: _ClassVar[Board3DFormat]
    B3D_U3D: _ClassVar[Board3DFormat]
    B3D_PDF: _ClassVar[Board3DFormat]

class RenderFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RF_UNKNOWN: _ClassVar[RenderFormat]
    RF_PNG: _ClassVar[RenderFormat]
    RF_JPEG: _ClassVar[RenderFormat]

class RenderQuality(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RQ_UNKNOWN: _ClassVar[RenderQuality]
    RQ_BASIC: _ClassVar[RenderQuality]
    RQ_HIGH: _ClassVar[RenderQuality]
    RQ_USER: _ClassVar[RenderQuality]
    RQ_JOB_SETTINGS: _ClassVar[RenderQuality]

class RenderBackgroundStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RBS_UNKNOWN: _ClassVar[RenderBackgroundStyle]
    RBS_DEFAULT: _ClassVar[RenderBackgroundStyle]
    RBS_TRANSPARENT: _ClassVar[RenderBackgroundStyle]
    RBS_OPAQUE: _ClassVar[RenderBackgroundStyle]

class RenderSide(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RS_UNKNOWN: _ClassVar[RenderSide]
    RS_TOP: _ClassVar[RenderSide]
    RS_BOTTOM: _ClassVar[RenderSide]
    RS_LEFT: _ClassVar[RenderSide]
    RS_RIGHT: _ClassVar[RenderSide]
    RS_FRONT: _ClassVar[RenderSide]
    RS_BACK: _ClassVar[RenderSide]

class BoardJobPaginationMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BJPM_UNKNOWN: _ClassVar[BoardJobPaginationMode]
    BJPM_ALL_LAYERS_ONE_PAGE: _ClassVar[BoardJobPaginationMode]
    BJPM_EACH_LAYER_OWN_PAGE: _ClassVar[BoardJobPaginationMode]
    BJPM_EACH_LAYER_OWN_FILE: _ClassVar[BoardJobPaginationMode]

class DrillFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DF_UNKNOWN: _ClassVar[DrillFormat]
    DF_EXCELLON: _ClassVar[DrillFormat]
    DF_GERBER: _ClassVar[DrillFormat]

class DrillOrigin(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DO_UNKNOWN: _ClassVar[DrillOrigin]
    DO_ABSOLUTE: _ClassVar[DrillOrigin]
    DO_PLOT: _ClassVar[DrillOrigin]

class DrillZerosFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DZF_UNKNOWN: _ClassVar[DrillZerosFormat]
    DZF_DECIMAL: _ClassVar[DrillZerosFormat]
    DZF_SUPPRESS_LEADING: _ClassVar[DrillZerosFormat]
    DZF_SUPPRESS_TRAILING: _ClassVar[DrillZerosFormat]
    DZF_KEEP_ZEROS: _ClassVar[DrillZerosFormat]

class DrillMapFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DMF_UNKNOWN: _ClassVar[DrillMapFormat]
    DMF_POSTSCRIPT: _ClassVar[DrillMapFormat]
    DMF_GERBER_X2: _ClassVar[DrillMapFormat]
    DMF_DXF: _ClassVar[DrillMapFormat]
    DMF_SVG: _ClassVar[DrillMapFormat]
    DMF_PDF: _ClassVar[DrillMapFormat]

class DrillGerberPrecision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DGP_UNKNOWN: _ClassVar[DrillGerberPrecision]
    DGP_4_5: _ClassVar[DrillGerberPrecision]
    DGP_4_6: _ClassVar[DrillGerberPrecision]

class DrillReportFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DRF_UNKNOWN: _ClassVar[DrillReportFormat]
    DRF_STANDARD: _ClassVar[DrillReportFormat]

class PositionSide(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PS_UNKNOWN: _ClassVar[PositionSide]
    PS_FRONT: _ClassVar[PositionSide]
    PS_BACK: _ClassVar[PositionSide]
    PS_BOTH: _ClassVar[PositionSide]

class PositionFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PF_UNKNOWN: _ClassVar[PositionFormat]
    PF_ASCII: _ClassVar[PositionFormat]
    PF_CSV: _ClassVar[PositionFormat]
    PF_GERBER: _ClassVar[PositionFormat]

class Ipc2581Version(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IPC2581V_UNKNOWN: _ClassVar[Ipc2581Version]
    IPC2581V_B: _ClassVar[Ipc2581Version]
    IPC2581V_C: _ClassVar[Ipc2581Version]

class OdbCompression(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ODBC_UNKNOWN: _ClassVar[OdbCompression]
    ODBC_NONE: _ClassVar[OdbCompression]
    ODBC_ZIP: _ClassVar[OdbCompression]
    ODBC_TGZ: _ClassVar[OdbCompression]

class StatsOutputFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOF_UNKNOWN: _ClassVar[StatsOutputFormat]
    SOF_REPORT: _ClassVar[StatsOutputFormat]
    SOF_JSON: _ClassVar[StatsOutputFormat]
PDM_UNKNOWN: PlotDrillMarks
PDM_NONE: PlotDrillMarks
PDM_SMALL: PlotDrillMarks
PDM_FULL: PlotDrillMarks
B3D_UNKNOWN: Board3DFormat
B3D_STEP: Board3DFormat
B3D_STEPZ: Board3DFormat
B3D_BREP: Board3DFormat
B3D_XAO: Board3DFormat
B3D_GLB: Board3DFormat
B3D_VRML: Board3DFormat
B3D_PLY: Board3DFormat
B3D_STL: Board3DFormat
B3D_U3D: Board3DFormat
B3D_PDF: Board3DFormat
RF_UNKNOWN: RenderFormat
RF_PNG: RenderFormat
RF_JPEG: RenderFormat
RQ_UNKNOWN: RenderQuality
RQ_BASIC: RenderQuality
RQ_HIGH: RenderQuality
RQ_USER: RenderQuality
RQ_JOB_SETTINGS: RenderQuality
RBS_UNKNOWN: RenderBackgroundStyle
RBS_DEFAULT: RenderBackgroundStyle
RBS_TRANSPARENT: RenderBackgroundStyle
RBS_OPAQUE: RenderBackgroundStyle
RS_UNKNOWN: RenderSide
RS_TOP: RenderSide
RS_BOTTOM: RenderSide
RS_LEFT: RenderSide
RS_RIGHT: RenderSide
RS_FRONT: RenderSide
RS_BACK: RenderSide
BJPM_UNKNOWN: BoardJobPaginationMode
BJPM_ALL_LAYERS_ONE_PAGE: BoardJobPaginationMode
BJPM_EACH_LAYER_OWN_PAGE: BoardJobPaginationMode
BJPM_EACH_LAYER_OWN_FILE: BoardJobPaginationMode
DF_UNKNOWN: DrillFormat
DF_EXCELLON: DrillFormat
DF_GERBER: DrillFormat
DO_UNKNOWN: DrillOrigin
DO_ABSOLUTE: DrillOrigin
DO_PLOT: DrillOrigin
DZF_UNKNOWN: DrillZerosFormat
DZF_DECIMAL: DrillZerosFormat
DZF_SUPPRESS_LEADING: DrillZerosFormat
DZF_SUPPRESS_TRAILING: DrillZerosFormat
DZF_KEEP_ZEROS: DrillZerosFormat
DMF_UNKNOWN: DrillMapFormat
DMF_POSTSCRIPT: DrillMapFormat
DMF_GERBER_X2: DrillMapFormat
DMF_DXF: DrillMapFormat
DMF_SVG: DrillMapFormat
DMF_PDF: DrillMapFormat
DGP_UNKNOWN: DrillGerberPrecision
DGP_4_5: DrillGerberPrecision
DGP_4_6: DrillGerberPrecision
DRF_UNKNOWN: DrillReportFormat
DRF_STANDARD: DrillReportFormat
PS_UNKNOWN: PositionSide
PS_FRONT: PositionSide
PS_BACK: PositionSide
PS_BOTH: PositionSide
PF_UNKNOWN: PositionFormat
PF_ASCII: PositionFormat
PF_CSV: PositionFormat
PF_GERBER: PositionFormat
IPC2581V_UNKNOWN: Ipc2581Version
IPC2581V_B: Ipc2581Version
IPC2581V_C: Ipc2581Version
ODBC_UNKNOWN: OdbCompression
ODBC_NONE: OdbCompression
ODBC_ZIP: OdbCompression
ODBC_TGZ: OdbCompression
SOF_UNKNOWN: StatsOutputFormat
SOF_REPORT: StatsOutputFormat
SOF_JSON: StatsOutputFormat

class BoardPlotSettings(_message.Message):
    __slots__ = ("layers", "common_layers", "color_theme", "drawing_sheet", "variant", "mirror", "black_and_white", "negative", "scale", "sketch_pads_on_fab_layers", "hide_dnp_footprints_on_fab_layers", "sketch_dnp_footprints_on_fab_layers", "crossout_dnp_footprints_on_fab_layers", "plot_footprint_values", "plot_reference_designators", "plot_drawing_sheet", "subtract_solder_mask_from_silk", "plot_pad_numbers", "drill_marks", "use_drill_origin", "check_zones_before_plot")
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    COMMON_LAYERS_FIELD_NUMBER: _ClassVar[int]
    COLOR_THEME_FIELD_NUMBER: _ClassVar[int]
    DRAWING_SHEET_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    MIRROR_FIELD_NUMBER: _ClassVar[int]
    BLACK_AND_WHITE_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    SKETCH_PADS_ON_FAB_LAYERS_FIELD_NUMBER: _ClassVar[int]
    HIDE_DNP_FOOTPRINTS_ON_FAB_LAYERS_FIELD_NUMBER: _ClassVar[int]
    SKETCH_DNP_FOOTPRINTS_ON_FAB_LAYERS_FIELD_NUMBER: _ClassVar[int]
    CROSSOUT_DNP_FOOTPRINTS_ON_FAB_LAYERS_FIELD_NUMBER: _ClassVar[int]
    PLOT_FOOTPRINT_VALUES_FIELD_NUMBER: _ClassVar[int]
    PLOT_REFERENCE_DESIGNATORS_FIELD_NUMBER: _ClassVar[int]
    PLOT_DRAWING_SHEET_FIELD_NUMBER: _ClassVar[int]
    SUBTRACT_SOLDER_MASK_FROM_SILK_FIELD_NUMBER: _ClassVar[int]
    PLOT_PAD_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    DRILL_MARKS_FIELD_NUMBER: _ClassVar[int]
    USE_DRILL_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    CHECK_ZONES_BEFORE_PLOT_FIELD_NUMBER: _ClassVar[int]
    layers: _containers.RepeatedScalarFieldContainer[_board_types_pb2.BoardLayer]
    common_layers: _containers.RepeatedScalarFieldContainer[_board_types_pb2.BoardLayer]
    color_theme: str
    drawing_sheet: str
    variant: str
    mirror: bool
    black_and_white: bool
    negative: bool
    scale: float
    sketch_pads_on_fab_layers: bool
    hide_dnp_footprints_on_fab_layers: bool
    sketch_dnp_footprints_on_fab_layers: bool
    crossout_dnp_footprints_on_fab_layers: bool
    plot_footprint_values: bool
    plot_reference_designators: bool
    plot_drawing_sheet: bool
    subtract_solder_mask_from_silk: bool
    plot_pad_numbers: bool
    drill_marks: PlotDrillMarks
    use_drill_origin: bool
    check_zones_before_plot: bool
    def __init__(self, layers: _Optional[_Iterable[_Union[_board_types_pb2.BoardLayer, str]]] = ..., common_layers: _Optional[_Iterable[_Union[_board_types_pb2.BoardLayer, str]]] = ..., color_theme: _Optional[str] = ..., drawing_sheet: _Optional[str] = ..., variant: _Optional[str] = ..., mirror: bool = ..., black_and_white: bool = ..., negative: bool = ..., scale: _Optional[float] = ..., sketch_pads_on_fab_layers: bool = ..., hide_dnp_footprints_on_fab_layers: bool = ..., sketch_dnp_footprints_on_fab_layers: bool = ..., crossout_dnp_footprints_on_fab_layers: bool = ..., plot_footprint_values: bool = ..., plot_reference_designators: bool = ..., plot_drawing_sheet: bool = ..., subtract_solder_mask_from_silk: bool = ..., plot_pad_numbers: bool = ..., drill_marks: _Optional[_Union[PlotDrillMarks, str]] = ..., use_drill_origin: bool = ..., check_zones_before_plot: bool = ...) -> None: ...

class RunBoardJobExport3D(_message.Message):
    __slots__ = ("job_settings", "variant", "format", "net_filter", "component_filter", "has_user_origin", "origin", "overwrite", "use_grid_origin", "use_drill_origin", "use_defined_origin", "use_pcb_center_origin", "include_unspecified", "include_dnp", "substitute_models", "board_outlines_chaining_epsilon", "board_only", "cut_vias_in_body", "export_board_body", "export_components", "export_tracks_and_vias", "export_pads", "export_zones", "export_inner_copper", "export_silkscreen", "export_soldermask", "fuse_shapes", "fill_all_vias", "optimize_step", "extra_pad_thickness", "vrml_units", "vrml_model_dir", "vrml_relative_paths")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    NET_FILTER_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FILTER_FIELD_NUMBER: _ClassVar[int]
    HAS_USER_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    USE_GRID_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    USE_DRILL_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    USE_DEFINED_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    USE_PCB_CENTER_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_UNSPECIFIED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DNP_FIELD_NUMBER: _ClassVar[int]
    SUBSTITUTE_MODELS_FIELD_NUMBER: _ClassVar[int]
    BOARD_OUTLINES_CHAINING_EPSILON_FIELD_NUMBER: _ClassVar[int]
    BOARD_ONLY_FIELD_NUMBER: _ClassVar[int]
    CUT_VIAS_IN_BODY_FIELD_NUMBER: _ClassVar[int]
    EXPORT_BOARD_BODY_FIELD_NUMBER: _ClassVar[int]
    EXPORT_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_TRACKS_AND_VIAS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_PADS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_ZONES_FIELD_NUMBER: _ClassVar[int]
    EXPORT_INNER_COPPER_FIELD_NUMBER: _ClassVar[int]
    EXPORT_SILKSCREEN_FIELD_NUMBER: _ClassVar[int]
    EXPORT_SOLDERMASK_FIELD_NUMBER: _ClassVar[int]
    FUSE_SHAPES_FIELD_NUMBER: _ClassVar[int]
    FILL_ALL_VIAS_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZE_STEP_FIELD_NUMBER: _ClassVar[int]
    EXTRA_PAD_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    VRML_UNITS_FIELD_NUMBER: _ClassVar[int]
    VRML_MODEL_DIR_FIELD_NUMBER: _ClassVar[int]
    VRML_RELATIVE_PATHS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    variant: str
    format: Board3DFormat
    net_filter: str
    component_filter: str
    has_user_origin: bool
    origin: _base_types_pb2.Vector2
    overwrite: bool
    use_grid_origin: bool
    use_drill_origin: bool
    use_defined_origin: bool
    use_pcb_center_origin: bool
    include_unspecified: bool
    include_dnp: bool
    substitute_models: bool
    board_outlines_chaining_epsilon: float
    board_only: bool
    cut_vias_in_body: bool
    export_board_body: bool
    export_components: bool
    export_tracks_and_vias: bool
    export_pads: bool
    export_zones: bool
    export_inner_copper: bool
    export_silkscreen: bool
    export_soldermask: bool
    fuse_shapes: bool
    fill_all_vias: bool
    optimize_step: bool
    extra_pad_thickness: bool
    vrml_units: _enums_pb2.Units
    vrml_model_dir: str
    vrml_relative_paths: bool
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., variant: _Optional[str] = ..., format: _Optional[_Union[Board3DFormat, str]] = ..., net_filter: _Optional[str] = ..., component_filter: _Optional[str] = ..., has_user_origin: bool = ..., origin: _Optional[_Union[_base_types_pb2.Vector2, _Mapping]] = ..., overwrite: bool = ..., use_grid_origin: bool = ..., use_drill_origin: bool = ..., use_defined_origin: bool = ..., use_pcb_center_origin: bool = ..., include_unspecified: bool = ..., include_dnp: bool = ..., substitute_models: bool = ..., board_outlines_chaining_epsilon: _Optional[float] = ..., board_only: bool = ..., cut_vias_in_body: bool = ..., export_board_body: bool = ..., export_components: bool = ..., export_tracks_and_vias: bool = ..., export_pads: bool = ..., export_zones: bool = ..., export_inner_copper: bool = ..., export_silkscreen: bool = ..., export_soldermask: bool = ..., fuse_shapes: bool = ..., fill_all_vias: bool = ..., optimize_step: bool = ..., extra_pad_thickness: bool = ..., vrml_units: _Optional[_Union[_enums_pb2.Units, str]] = ..., vrml_model_dir: _Optional[str] = ..., vrml_relative_paths: bool = ...) -> None: ...

class RunBoardJobExportRender(_message.Message):
    __slots__ = ("job_settings", "format", "quality", "background_style", "width", "height", "appearance_preset", "use_board_stackup_colors", "side", "zoom", "perspective", "rotation", "pan", "pivot", "procedural_textures", "floor", "anti_alias", "post_process", "light_top_intensity", "light_bottom_intensity", "light_camera_intensity", "light_side_intensity", "light_side_elevation")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_STYLE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    APPEARANCE_PRESET_FIELD_NUMBER: _ClassVar[int]
    USE_BOARD_STACKUP_COLORS_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    PERSPECTIVE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    PAN_FIELD_NUMBER: _ClassVar[int]
    PIVOT_FIELD_NUMBER: _ClassVar[int]
    PROCEDURAL_TEXTURES_FIELD_NUMBER: _ClassVar[int]
    FLOOR_FIELD_NUMBER: _ClassVar[int]
    ANTI_ALIAS_FIELD_NUMBER: _ClassVar[int]
    POST_PROCESS_FIELD_NUMBER: _ClassVar[int]
    LIGHT_TOP_INTENSITY_FIELD_NUMBER: _ClassVar[int]
    LIGHT_BOTTOM_INTENSITY_FIELD_NUMBER: _ClassVar[int]
    LIGHT_CAMERA_INTENSITY_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SIDE_INTENSITY_FIELD_NUMBER: _ClassVar[int]
    LIGHT_SIDE_ELEVATION_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    format: RenderFormat
    quality: RenderQuality
    background_style: RenderBackgroundStyle
    width: int
    height: int
    appearance_preset: str
    use_board_stackup_colors: bool
    side: RenderSide
    zoom: float
    perspective: bool
    rotation: _base_types_pb2.Vector3D
    pan: _base_types_pb2.Vector3D
    pivot: _base_types_pb2.Vector3D
    procedural_textures: bool
    floor: bool
    anti_alias: bool
    post_process: bool
    light_top_intensity: _base_types_pb2.Vector3D
    light_bottom_intensity: _base_types_pb2.Vector3D
    light_camera_intensity: _base_types_pb2.Vector3D
    light_side_intensity: _base_types_pb2.Vector3D
    light_side_elevation: int
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., format: _Optional[_Union[RenderFormat, str]] = ..., quality: _Optional[_Union[RenderQuality, str]] = ..., background_style: _Optional[_Union[RenderBackgroundStyle, str]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., appearance_preset: _Optional[str] = ..., use_board_stackup_colors: bool = ..., side: _Optional[_Union[RenderSide, str]] = ..., zoom: _Optional[float] = ..., perspective: bool = ..., rotation: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., pan: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., pivot: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., procedural_textures: bool = ..., floor: bool = ..., anti_alias: bool = ..., post_process: bool = ..., light_top_intensity: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., light_bottom_intensity: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., light_camera_intensity: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., light_side_intensity: _Optional[_Union[_base_types_pb2.Vector3D, _Mapping]] = ..., light_side_elevation: _Optional[int] = ...) -> None: ...

class RunBoardJobExportSvg(_message.Message):
    __slots__ = ("job_settings", "plot_settings", "fit_page_to_board", "precision", "page_mode")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FIT_PAGE_TO_BOARD_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    PAGE_MODE_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    plot_settings: BoardPlotSettings
    fit_page_to_board: bool
    precision: int
    page_mode: BoardJobPaginationMode
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., plot_settings: _Optional[_Union[BoardPlotSettings, _Mapping]] = ..., fit_page_to_board: bool = ..., precision: _Optional[int] = ..., page_mode: _Optional[_Union[BoardJobPaginationMode, str]] = ...) -> None: ...

class RunBoardJobExportDxf(_message.Message):
    __slots__ = ("job_settings", "plot_settings", "plot_graphic_items_using_contours", "polygon_mode", "units", "page_mode")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_GRAPHIC_ITEMS_USING_CONTOURS_FIELD_NUMBER: _ClassVar[int]
    POLYGON_MODE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    PAGE_MODE_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    plot_settings: BoardPlotSettings
    plot_graphic_items_using_contours: bool
    polygon_mode: bool
    units: _enums_pb2.Units
    page_mode: BoardJobPaginationMode
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., plot_settings: _Optional[_Union[BoardPlotSettings, _Mapping]] = ..., plot_graphic_items_using_contours: bool = ..., polygon_mode: bool = ..., units: _Optional[_Union[_enums_pb2.Units, str]] = ..., page_mode: _Optional[_Union[BoardJobPaginationMode, str]] = ...) -> None: ...

class RunBoardJobExportPdf(_message.Message):
    __slots__ = ("job_settings", "plot_settings", "front_footprint_property_popups", "back_footprint_property_popups", "include_metadata", "single_document", "page_mode", "background_color")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FRONT_FOOTPRINT_PROPERTY_POPUPS_FIELD_NUMBER: _ClassVar[int]
    BACK_FOOTPRINT_PROPERTY_POPUPS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_METADATA_FIELD_NUMBER: _ClassVar[int]
    SINGLE_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_MODE_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_COLOR_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    plot_settings: BoardPlotSettings
    front_footprint_property_popups: bool
    back_footprint_property_popups: bool
    include_metadata: bool
    single_document: bool
    page_mode: BoardJobPaginationMode
    background_color: str
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., plot_settings: _Optional[_Union[BoardPlotSettings, _Mapping]] = ..., front_footprint_property_popups: bool = ..., back_footprint_property_popups: bool = ..., include_metadata: bool = ..., single_document: bool = ..., page_mode: _Optional[_Union[BoardJobPaginationMode, str]] = ..., background_color: _Optional[str] = ...) -> None: ...

class RunBoardJobExportPs(_message.Message):
    __slots__ = ("job_settings", "plot_settings", "page_mode", "track_width_correction", "x_scale_adjust", "y_scale_adjust", "force_a4", "use_global_settings")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PAGE_MODE_FIELD_NUMBER: _ClassVar[int]
    TRACK_WIDTH_CORRECTION_FIELD_NUMBER: _ClassVar[int]
    X_SCALE_ADJUST_FIELD_NUMBER: _ClassVar[int]
    Y_SCALE_ADJUST_FIELD_NUMBER: _ClassVar[int]
    FORCE_A4_FIELD_NUMBER: _ClassVar[int]
    USE_GLOBAL_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    plot_settings: BoardPlotSettings
    page_mode: BoardJobPaginationMode
    track_width_correction: float
    x_scale_adjust: float
    y_scale_adjust: float
    force_a4: bool
    use_global_settings: bool
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., plot_settings: _Optional[_Union[BoardPlotSettings, _Mapping]] = ..., page_mode: _Optional[_Union[BoardJobPaginationMode, str]] = ..., track_width_correction: _Optional[float] = ..., x_scale_adjust: _Optional[float] = ..., y_scale_adjust: _Optional[float] = ..., force_a4: bool = ..., use_global_settings: bool = ...) -> None: ...

class RunBoardJobExportGerbers(_message.Message):
    __slots__ = ("job_settings", "layers")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    layers: _containers.RepeatedScalarFieldContainer[_board_types_pb2.BoardLayer]
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., layers: _Optional[_Iterable[_Union[_board_types_pb2.BoardLayer, str]]] = ...) -> None: ...

class ExcellonFormatOptions(_message.Message):
    __slots__ = ("mirror_y", "minimal_header", "combine_pth_npth", "route_oval_holes")
    MIRROR_Y_FIELD_NUMBER: _ClassVar[int]
    MINIMAL_HEADER_FIELD_NUMBER: _ClassVar[int]
    COMBINE_PTH_NPTH_FIELD_NUMBER: _ClassVar[int]
    ROUTE_OVAL_HOLES_FIELD_NUMBER: _ClassVar[int]
    mirror_y: bool
    minimal_header: bool
    combine_pth_npth: bool
    route_oval_holes: bool
    def __init__(self, mirror_y: bool = ..., minimal_header: bool = ..., combine_pth_npth: bool = ..., route_oval_holes: bool = ...) -> None: ...

class RunBoardJobExportDrill(_message.Message):
    __slots__ = ("job_settings", "format", "units", "origin", "zeros_format", "excellon", "map_format", "gerber_precision", "gerber_generate_tenting", "report_format", "report_filename")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ZEROS_FORMAT_FIELD_NUMBER: _ClassVar[int]
    EXCELLON_FIELD_NUMBER: _ClassVar[int]
    MAP_FORMAT_FIELD_NUMBER: _ClassVar[int]
    GERBER_PRECISION_FIELD_NUMBER: _ClassVar[int]
    GERBER_GENERATE_TENTING_FIELD_NUMBER: _ClassVar[int]
    REPORT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    REPORT_FILENAME_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    format: DrillFormat
    units: _enums_pb2.Units
    origin: DrillOrigin
    zeros_format: DrillZerosFormat
    excellon: ExcellonFormatOptions
    map_format: DrillMapFormat
    gerber_precision: DrillGerberPrecision
    gerber_generate_tenting: bool
    report_format: DrillReportFormat
    report_filename: str
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., format: _Optional[_Union[DrillFormat, str]] = ..., units: _Optional[_Union[_enums_pb2.Units, str]] = ..., origin: _Optional[_Union[DrillOrigin, str]] = ..., zeros_format: _Optional[_Union[DrillZerosFormat, str]] = ..., excellon: _Optional[_Union[ExcellonFormatOptions, _Mapping]] = ..., map_format: _Optional[_Union[DrillMapFormat, str]] = ..., gerber_precision: _Optional[_Union[DrillGerberPrecision, str]] = ..., gerber_generate_tenting: bool = ..., report_format: _Optional[_Union[DrillReportFormat, str]] = ..., report_filename: _Optional[str] = ...) -> None: ...

class RunBoardJobExportPosition(_message.Message):
    __slots__ = ("job_settings", "use_drill_place_file_origin", "smd_only", "exclude_footprints_with_th", "exclude_dnp", "exclude_from_bom", "negate_bottom_x", "single_file", "naked_filename", "side", "units", "format", "include_board_edge_for_gerber", "variant")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    USE_DRILL_PLACE_FILE_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    SMD_ONLY_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FOOTPRINTS_WITH_TH_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_DNP_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FROM_BOM_FIELD_NUMBER: _ClassVar[int]
    NEGATE_BOTTOM_X_FIELD_NUMBER: _ClassVar[int]
    SINGLE_FILE_FIELD_NUMBER: _ClassVar[int]
    NAKED_FILENAME_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_BOARD_EDGE_FOR_GERBER_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    use_drill_place_file_origin: bool
    smd_only: bool
    exclude_footprints_with_th: bool
    exclude_dnp: bool
    exclude_from_bom: bool
    negate_bottom_x: bool
    single_file: bool
    naked_filename: bool
    side: PositionSide
    units: _enums_pb2.Units
    format: PositionFormat
    include_board_edge_for_gerber: bool
    variant: str
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., use_drill_place_file_origin: bool = ..., smd_only: bool = ..., exclude_footprints_with_th: bool = ..., exclude_dnp: bool = ..., exclude_from_bom: bool = ..., negate_bottom_x: bool = ..., single_file: bool = ..., naked_filename: bool = ..., side: _Optional[_Union[PositionSide, str]] = ..., units: _Optional[_Union[_enums_pb2.Units, str]] = ..., format: _Optional[_Union[PositionFormat, str]] = ..., include_board_edge_for_gerber: bool = ..., variant: _Optional[str] = ...) -> None: ...

class RunBoardJobExportGencad(_message.Message):
    __slots__ = ("job_settings", "flip_bottom_pads", "use_individual_shapes", "store_origin_coords", "use_drill_origin", "use_unique_pins")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FLIP_BOTTOM_PADS_FIELD_NUMBER: _ClassVar[int]
    USE_INDIVIDUAL_SHAPES_FIELD_NUMBER: _ClassVar[int]
    STORE_ORIGIN_COORDS_FIELD_NUMBER: _ClassVar[int]
    USE_DRILL_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    USE_UNIQUE_PINS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    flip_bottom_pads: bool
    use_individual_shapes: bool
    store_origin_coords: bool
    use_drill_origin: bool
    use_unique_pins: bool
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., flip_bottom_pads: bool = ..., use_individual_shapes: bool = ..., store_origin_coords: bool = ..., use_drill_origin: bool = ..., use_unique_pins: bool = ...) -> None: ...

class RunBoardJobExportIpc2581(_message.Message):
    __slots__ = ("job_settings", "drawing_sheet", "variant", "units", "version", "precision", "compress", "internal_id_column", "manufacturer_part_number_column", "manufacturer_column", "distributor_part_number_column", "distributor_column", "bom_revision")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    DRAWING_SHEET_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    COMPRESS_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_ID_COLUMN_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_PART_NUMBER_COLUMN_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_COLUMN_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTOR_PART_NUMBER_COLUMN_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTOR_COLUMN_FIELD_NUMBER: _ClassVar[int]
    BOM_REVISION_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    drawing_sheet: str
    variant: str
    units: _enums_pb2.Units
    version: Ipc2581Version
    precision: int
    compress: bool
    internal_id_column: str
    manufacturer_part_number_column: str
    manufacturer_column: str
    distributor_part_number_column: str
    distributor_column: str
    bom_revision: str
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., drawing_sheet: _Optional[str] = ..., variant: _Optional[str] = ..., units: _Optional[_Union[_enums_pb2.Units, str]] = ..., version: _Optional[_Union[Ipc2581Version, str]] = ..., precision: _Optional[int] = ..., compress: bool = ..., internal_id_column: _Optional[str] = ..., manufacturer_part_number_column: _Optional[str] = ..., manufacturer_column: _Optional[str] = ..., distributor_part_number_column: _Optional[str] = ..., distributor_column: _Optional[str] = ..., bom_revision: _Optional[str] = ...) -> None: ...

class RunBoardJobExportIpcD356(_message.Message):
    __slots__ = ("job_settings",)
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ...) -> None: ...

class RunBoardJobExportODB(_message.Message):
    __slots__ = ("job_settings", "drawing_sheet", "variant", "units", "precision", "compression")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    DRAWING_SHEET_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    drawing_sheet: str
    variant: str
    units: _enums_pb2.Units
    precision: int
    compression: OdbCompression
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., drawing_sheet: _Optional[str] = ..., variant: _Optional[str] = ..., units: _Optional[_Union[_enums_pb2.Units, str]] = ..., precision: _Optional[int] = ..., compression: _Optional[_Union[OdbCompression, str]] = ...) -> None: ...

class RunBoardJobExportStats(_message.Message):
    __slots__ = ("job_settings", "format", "units", "exclude_footprints_without_pads", "subtract_holes_from_board_area", "subtract_holes_from_copper_areas")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_FOOTPRINTS_WITHOUT_PADS_FIELD_NUMBER: _ClassVar[int]
    SUBTRACT_HOLES_FROM_BOARD_AREA_FIELD_NUMBER: _ClassVar[int]
    SUBTRACT_HOLES_FROM_COPPER_AREAS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    format: StatsOutputFormat
    units: _enums_pb2.Units
    exclude_footprints_without_pads: bool
    subtract_holes_from_board_area: bool
    subtract_holes_from_copper_areas: bool
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., format: _Optional[_Union[StatsOutputFormat, str]] = ..., units: _Optional[_Union[_enums_pb2.Units, str]] = ..., exclude_footprints_without_pads: bool = ..., subtract_holes_from_board_area: bool = ..., subtract_holes_from_copper_areas: bool = ...) -> None: ...
