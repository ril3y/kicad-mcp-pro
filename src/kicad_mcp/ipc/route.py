"""Route a track with KiCad's interactive (push-and-shove) router over the API.

Needs a KiCad build that serves ``kiapi.board.commands.RouteTrack``. The command
is not in the generated stubs, so its messages are declared here at run time in
the same descriptor pool; their field numbers must match KiCad's
``board_commands.proto``.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from ._master_client import MasterKiCadClient

_PACKAGE = "kiapi.board.commands"


@lru_cache(maxsize=1)
def messages() -> tuple[Any, Any]:
    """Return the ``RouteTrack`` and ``RouteTrackResponse`` message classes."""
    from google.protobuf import descriptor_pb2, message_factory

    from kicad_mcp._master_proto._pool import shared_pool
    from kicad_mcp._master_proto.mp.board import board_types_pb2  # noqa: F401 - registers deps
    from kicad_mcp._master_proto.mp.common.types import base_types_pb2  # noqa: F401

    field = descriptor_pb2.FieldDescriptorProto
    file = descriptor_pb2.FileDescriptorProto(
        name="mp/board/route_commands.proto", package=_PACKAGE, syntax="proto3"
    )
    file.dependency.extend(
        [
            "mp/common/types/base_types.proto",
            "mp/board/board_types.proto",
            "google/protobuf/any.proto",
        ]
    )

    mode = file.enum_type.add(name="RouteTrackMode")
    for number, name in enumerate(("RTM_UNKNOWN", "RTM_WALKAROUND", "RTM_SHOVE")):
        mode.value.add(name=name, number=number)

    def add(message: Any, name: str, number: int, type_name: str, **extra: Any) -> Any:  # noqa: ANN401
        kind = field.TYPE_ENUM if extra.pop("enum", False) else field.TYPE_MESSAGE
        return message.field.add(
            name=name,
            number=number,
            type=kind,
            type_name=type_name,
            label=extra.pop("label", field.LABEL_OPTIONAL),
            **extra,
        )

    def optional(message: Any, name: str, number: int, type_name: str, enum: bool = False) -> None:  # noqa: ANN401
        message.oneof_decl.add(name=f"_{name}")
        add(
            message,
            name,
            number,
            type_name,
            enum=enum,
            proto3_optional=True,
            oneof_index=len(message.oneof_decl) - 1,
        )

    waypoint = file.message_type.add(name="RouteTrackWaypoint")
    add(waypoint, "position", 1, ".kiapi.common.types.Vector2")
    optional(waypoint, "layer", 2, ".kiapi.board.types.BoardLayer", enum=True)

    request = file.message_type.add(name="RouteTrack")
    add(request, "header", 1, ".kiapi.common.types.ItemHeader")
    add(request, "start", 2, ".kiapi.common.types.Vector2")
    add(request, "layer", 3, ".kiapi.board.types.BoardLayer", enum=True)
    add(request, "waypoints", 4, f".{_PACKAGE}.RouteTrackWaypoint", label=field.LABEL_REPEATED)
    add(request, "end", 5, ".kiapi.common.types.Vector2")
    add(request, "mode", 6, f".{_PACKAGE}.RouteTrackMode", enum=True)
    optional(request, "width", 7, ".kiapi.common.types.Distance")

    response = file.message_type.add(name="RouteTrackResponse")
    add(response, "header", 1, ".kiapi.common.types.ItemHeader")
    add(response, "items", 2, ".google.protobuf.Any", label=field.LABEL_REPEATED)
    response.field.add(
        name="reached_end", number=3, type=field.TYPE_BOOL, label=field.LABEL_OPTIONAL
    )

    shared_pool.AddSerializedFile(file.SerializeToString())
    return (
        message_factory.GetMessageClass(
            shared_pool.FindMessageTypeByName(f"{_PACKAGE}.RouteTrack")
        ),
        message_factory.GetMessageClass(
            shared_pool.FindMessageTypeByName(f"{_PACKAGE}.RouteTrackResponse")
        ),
    )


def _nm(mm: float) -> int:
    return int(round(float(mm) * 1_000_000))


def route_track(
    start: tuple[float, float],
    end: tuple[float, float],
    layer: str,
    *,
    waypoints: list[dict[str, Any]] | None = None,
    shove: bool = False,
    width_mm: float = 0.0,
    client: MasterKiCadClient | None = None,
) -> dict[str, Any]:
    """Route one track from ``start`` to ``end`` (mm); return what KiCad's router laid.

    ``layer`` and a waypoint's ``layer`` are names like "F_Cu" or "In2.Cu". A
    waypoint is ``{"x", "y"}`` with an optional ``"layer"``: a different layer
    there places a via and continues on it. Returns ``tracks`` and ``vias`` (each
    a list of dicts in mm) and ``reached_end``.
    """
    from kicad_mcp._master_proto.mp.board import board_types_pb2 as board_types

    from .board_setup import _board_document

    def layer_value(name: str) -> int:
        return int(board_types.BoardLayer.Value("BL_" + name.replace(".", "_")))

    request_cls, response_cls = messages()
    client = client or MasterKiCadClient()
    request = request_cls()
    request.header.document.CopyFrom(_board_document(client))
    request.start.x_nm, request.start.y_nm = _nm(start[0]), _nm(start[1])
    request.end.x_nm, request.end.y_nm = _nm(end[0]), _nm(end[1])
    request.layer = layer_value(layer)
    request.mode = 2 if shove else 1
    if width_mm > 0:
        request.width.value_nm = _nm(width_mm)
    for entry in waypoints or []:
        waypoint = request.waypoints.add()
        waypoint.position.x_nm, waypoint.position.y_nm = _nm(entry["x"]), _nm(entry["y"])
        if entry.get("layer"):
            waypoint.layer = layer_value(str(entry["layer"]))

    response = client.send(request, response_cls)
    tracks: list[dict[str, Any]] = []
    vias: list[dict[str, Any]] = []
    for packed in response.items:
        track = board_types.Track()
        via = board_types.Via()
        if packed.Is(track.DESCRIPTOR) and packed.Unpack(track):
            tracks.append(
                {
                    "layer": board_types.BoardLayer.Name(track.layer).removeprefix("BL_"),
                    "x1": track.start.x_nm / 1e6,
                    "y1": track.start.y_nm / 1e6,
                    "x2": track.end.x_nm / 1e6,
                    "y2": track.end.y_nm / 1e6,
                    "width": track.width.value_nm / 1e6,
                }
            )
        elif packed.Is(via.DESCRIPTOR) and packed.Unpack(via):
            vias.append({"x": via.position.x_nm / 1e6, "y": via.position.y_nm / 1e6})
    return {"tracks": tracks, "vias": vias, "reached_end": bool(response.reached_end)}
