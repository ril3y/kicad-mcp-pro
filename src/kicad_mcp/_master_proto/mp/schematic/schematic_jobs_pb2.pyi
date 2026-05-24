from mp.common.types import jobs_pb2 as _jobs_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SchematicJobPageSize(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SJPS_UNKNOWN: _ClassVar[SchematicJobPageSize]
    SJPS_AUTO: _ClassVar[SchematicJobPageSize]
    SJPS_A4: _ClassVar[SchematicJobPageSize]
    SJPS_A: _ClassVar[SchematicJobPageSize]

class SchematicNetlistFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SNF_UNKNOWN: _ClassVar[SchematicNetlistFormat]
    SNF_KICAD_XML: _ClassVar[SchematicNetlistFormat]
    SNF_KICAD_SEXPR: _ClassVar[SchematicNetlistFormat]
    SNF_ORCAD_PCB2: _ClassVar[SchematicNetlistFormat]
    SNF_CADSTAR: _ClassVar[SchematicNetlistFormat]
    SNF_SPICE: _ClassVar[SchematicNetlistFormat]
    SNF_SPICE_MODEL: _ClassVar[SchematicNetlistFormat]
    SNF_PADS: _ClassVar[SchematicNetlistFormat]
    SNF_ALLEGRO: _ClassVar[SchematicNetlistFormat]

class BOMSortDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BSD_UNKNOWN: _ClassVar[BOMSortDirection]
    BSD_ASCENDING: _ClassVar[BOMSortDirection]
    BSD_DESCENDING: _ClassVar[BOMSortDirection]
SJPS_UNKNOWN: SchematicJobPageSize
SJPS_AUTO: SchematicJobPageSize
SJPS_A4: SchematicJobPageSize
SJPS_A: SchematicJobPageSize
SNF_UNKNOWN: SchematicNetlistFormat
SNF_KICAD_XML: SchematicNetlistFormat
SNF_KICAD_SEXPR: SchematicNetlistFormat
SNF_ORCAD_PCB2: SchematicNetlistFormat
SNF_CADSTAR: SchematicNetlistFormat
SNF_SPICE: SchematicNetlistFormat
SNF_SPICE_MODEL: SchematicNetlistFormat
SNF_PADS: SchematicNetlistFormat
SNF_ALLEGRO: SchematicNetlistFormat
BSD_UNKNOWN: BOMSortDirection
BSD_ASCENDING: BOMSortDirection
BSD_DESCENDING: BOMSortDirection

class SchematicPlotSettings(_message.Message):
    __slots__ = ("drawing_sheet", "default_font", "variant", "plot_all", "plot_drawing_sheet", "plot_pages", "show_hop_over", "black_and_white", "page_size", "use_background_color", "min_pen_width", "theme")
    DRAWING_SHEET_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FONT_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    PLOT_ALL_FIELD_NUMBER: _ClassVar[int]
    PLOT_DRAWING_SHEET_FIELD_NUMBER: _ClassVar[int]
    PLOT_PAGES_FIELD_NUMBER: _ClassVar[int]
    SHOW_HOP_OVER_FIELD_NUMBER: _ClassVar[int]
    BLACK_AND_WHITE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    USE_BACKGROUND_COLOR_FIELD_NUMBER: _ClassVar[int]
    MIN_PEN_WIDTH_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    drawing_sheet: str
    default_font: str
    variant: str
    plot_all: bool
    plot_drawing_sheet: bool
    plot_pages: _containers.RepeatedScalarFieldContainer[str]
    show_hop_over: bool
    black_and_white: bool
    page_size: SchematicJobPageSize
    use_background_color: bool
    min_pen_width: int
    theme: str
    def __init__(self, drawing_sheet: _Optional[str] = ..., default_font: _Optional[str] = ..., variant: _Optional[str] = ..., plot_all: bool = ..., plot_drawing_sheet: bool = ..., plot_pages: _Optional[_Iterable[str]] = ..., show_hop_over: bool = ..., black_and_white: bool = ..., page_size: _Optional[_Union[SchematicJobPageSize, str]] = ..., use_background_color: bool = ..., min_pen_width: _Optional[int] = ..., theme: _Optional[str] = ...) -> None: ...

class RunSchematicJobExportSvg(_message.Message):
    __slots__ = ("job_settings", "plot_settings")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    plot_settings: SchematicPlotSettings
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., plot_settings: _Optional[_Union[SchematicPlotSettings, _Mapping]] = ...) -> None: ...

class RunSchematicJobExportDxf(_message.Message):
    __slots__ = ("job_settings", "plot_settings")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    plot_settings: SchematicPlotSettings
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., plot_settings: _Optional[_Union[SchematicPlotSettings, _Mapping]] = ...) -> None: ...

class RunSchematicJobExportPdf(_message.Message):
    __slots__ = ("job_settings", "plot_settings", "property_popups", "hierarchical_links", "include_metadata")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PROPERTY_POPUPS_FIELD_NUMBER: _ClassVar[int]
    HIERARCHICAL_LINKS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_METADATA_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    plot_settings: SchematicPlotSettings
    property_popups: bool
    hierarchical_links: bool
    include_metadata: bool
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., plot_settings: _Optional[_Union[SchematicPlotSettings, _Mapping]] = ..., property_popups: bool = ..., hierarchical_links: bool = ..., include_metadata: bool = ...) -> None: ...

class RunSchematicJobExportPs(_message.Message):
    __slots__ = ("job_settings", "plot_settings")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLOT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    plot_settings: SchematicPlotSettings
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., plot_settings: _Optional[_Union[SchematicPlotSettings, _Mapping]] = ...) -> None: ...

class RunSchematicJobExportNetlist(_message.Message):
    __slots__ = ("job_settings", "format", "variant_name")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    VARIANT_NAME_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    format: SchematicNetlistFormat
    variant_name: str
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., format: _Optional[_Union[SchematicNetlistFormat, str]] = ..., variant_name: _Optional[str] = ...) -> None: ...

class BOMFormatSettings(_message.Message):
    __slots__ = ("preset_name", "field_delimiter", "string_delimiter", "ref_delimiter", "ref_range_delimiter", "keep_tabs", "keep_line_breaks")
    PRESET_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_DELIMITER_FIELD_NUMBER: _ClassVar[int]
    STRING_DELIMITER_FIELD_NUMBER: _ClassVar[int]
    REF_DELIMITER_FIELD_NUMBER: _ClassVar[int]
    REF_RANGE_DELIMITER_FIELD_NUMBER: _ClassVar[int]
    KEEP_TABS_FIELD_NUMBER: _ClassVar[int]
    KEEP_LINE_BREAKS_FIELD_NUMBER: _ClassVar[int]
    preset_name: str
    field_delimiter: str
    string_delimiter: str
    ref_delimiter: str
    ref_range_delimiter: str
    keep_tabs: bool
    keep_line_breaks: bool
    def __init__(self, preset_name: _Optional[str] = ..., field_delimiter: _Optional[str] = ..., string_delimiter: _Optional[str] = ..., ref_delimiter: _Optional[str] = ..., ref_range_delimiter: _Optional[str] = ..., keep_tabs: bool = ..., keep_line_breaks: bool = ...) -> None: ...

class BOMField(_message.Message):
    __slots__ = ("name", "label", "group_by")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    name: str
    label: str
    group_by: bool
    def __init__(self, name: _Optional[str] = ..., label: _Optional[str] = ..., group_by: bool = ...) -> None: ...

class BOMFieldSettings(_message.Message):
    __slots__ = ("preset_name", "fields", "sort_field", "sort_direction", "filter")
    PRESET_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_FIELD_NUMBER: _ClassVar[int]
    SORT_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    preset_name: str
    fields: _containers.RepeatedCompositeFieldContainer[BOMField]
    sort_field: str
    sort_direction: BOMSortDirection
    filter: str
    def __init__(self, preset_name: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[BOMField, _Mapping]]] = ..., sort_field: _Optional[str] = ..., sort_direction: _Optional[_Union[BOMSortDirection, str]] = ..., filter: _Optional[str] = ...) -> None: ...

class RunSchematicJobExportBOM(_message.Message):
    __slots__ = ("job_settings", "format", "fields", "exclude_dnp", "group_symbols", "variant_name")
    JOB_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_DNP_FIELD_NUMBER: _ClassVar[int]
    GROUP_SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    VARIANT_NAME_FIELD_NUMBER: _ClassVar[int]
    job_settings: _jobs_pb2.RunJobSettings
    format: BOMFormatSettings
    fields: BOMFieldSettings
    exclude_dnp: bool
    group_symbols: bool
    variant_name: str
    def __init__(self, job_settings: _Optional[_Union[_jobs_pb2.RunJobSettings, _Mapping]] = ..., format: _Optional[_Union[BOMFormatSettings, _Mapping]] = ..., fields: _Optional[_Union[BOMFieldSettings, _Mapping]] = ..., exclude_dnp: bool = ..., group_symbols: bool = ..., variant_name: _Optional[str] = ...) -> None: ...
