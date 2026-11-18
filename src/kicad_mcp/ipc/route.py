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
def messages() -> tuple[Any, ...]:
    """Return the classes: RouteTrack, its response, GetRoutingClearanceMap, its response."""
    from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

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
    request.field.add(
        name="allow_partial", number=8, type=field.TYPE_BOOL, label=field.LABEL_OPTIONAL
    )

    response = file.message_type.add(name="RouteTrackResponse")
    add(response, "header", 1, ".kiapi.common.types.ItemHeader")
    add(response, "items", 2, ".google.protobuf.Any", label=field.LABEL_REPEATED)
    response.field.add(
        name="reached_end", number=3, type=field.TYPE_BOOL, label=field.LABEL_OPTIONAL
    )

    def scalar(message: Any, name: str, number: int, kind: int, repeated: bool = False) -> None:  # noqa: ANN401
        message.field.add(
            name=name,
            number=number,
            type=kind,
            label=field.LABEL_REPEATED if repeated else field.LABEL_OPTIONAL,
        )

    map_request = file.message_type.add(name="GetRoutingClearanceMap")
    add(map_request, "board", 1, ".kiapi.common.types.DocumentSpecifier")
    scalar(map_request, "net_name", 2, field.TYPE_STRING)
    add(
        map_request,
        "layers",
        3,
        ".kiapi.board.types.BoardLayer",
        enum=True,
        label=field.LABEL_REPEATED,
    )
    add(map_request, "cell", 4, ".kiapi.common.types.Distance")
    optional(map_request, "track_width", 5, ".kiapi.common.types.Distance")
    scalar(map_request, "include_vias", 6, field.TYPE_BOOL)
    scalar(map_request, "ignore_tracks", 7, field.TYPE_BOOL)

    map_layer = file.message_type.add(name="RoutingClearanceMapLayer")
    add(map_layer, "layer", 1, ".kiapi.board.types.BoardLayer", enum=True)
    scalar(map_layer, "blocked", 2, field.TYPE_BYTES)

    map_response = file.message_type.add(name="RoutingClearanceMapResponse")
    add(map_response, "origin", 1, ".kiapi.common.types.Vector2")
    add(map_response, "cell", 2, ".kiapi.common.types.Distance")
    scalar(map_response, "columns", 3, field.TYPE_INT32)
    scalar(map_response, "rows", 4, field.TYPE_INT32)
    add(
        map_response,
        "layers",
        5,
        f".{_PACKAGE}.RoutingClearanceMapLayer",
        label=field.LABEL_REPEATED,
    )
    scalar(map_response, "via_blocked", 6, field.TYPE_BYTES)
    add(map_response, "track_width", 7, ".kiapi.common.types.Distance")
    add(map_response, "via_diameter", 8, ".kiapi.common.types.Distance")
    add(map_response, "via_drill", 9, ".kiapi.common.types.Distance")

    # A pool of its own: the shared pool outlives a code reload and would refuse a
    # second, changed copy of these messages.
    pool = descriptor_pool.DescriptorPool()
    added: set[str] = set()

    def copy(descriptor: Any) -> None:  # noqa: ANN401 - FileDescriptor
        if descriptor.name in added:
            return
        for dependency in descriptor.dependencies:
            copy(dependency)
        pool.AddSerializedFile(descriptor.serialized_pb)
        added.add(descriptor.name)

    for name in file.dependency:
        copy(shared_pool.FindFileByName(name))
    pool.AddSerializedFile(file.SerializeToString())
    names = ("RouteTrack", "RouteTrackResponse", "GetRoutingClearanceMap")
    names += ("RoutingClearanceMapResponse",)
    return tuple(
        message_factory.GetMessageClass(pool.FindMessageTypeByName(f"{_PACKAGE}.{name}"))
        for name in names
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
    allow_partial: bool = False,
    client: MasterKiCadClient | None = None,
) -> dict[str, Any]:
    """Route one track from ``start`` to ``end`` (mm); return what KiCad's router laid.

    ``layer`` and a waypoint's ``layer`` are names like "F_Cu" or "In2.Cu". A
    waypoint is ``{"x", "y"}`` with an optional ``"layer"``: a different layer
    there places a via and continues on it. Unless ``allow_partial`` is set, a
    route that cannot reach ``end`` adds nothing and raises. Returns ``tracks`` and ``vias`` (each
    a list of dicts in mm) and ``reached_end``.
    """
    from kicad_mcp._master_proto.mp.board import board_types_pb2 as board_types

    from .board_setup import _board_document

    def layer_value(name: str) -> int:
        return int(board_types.BoardLayer.Value("BL_" + name.replace(".", "_")))

    request_cls, response_cls = messages()[:2]
    client = client or MasterKiCadClient()
    request = request_cls()
    # The document comes from the shared pool's classes; go through bytes.
    request.header.document.MergeFromString(_board_document(client).SerializeToString())
    request.start.x_nm, request.start.y_nm = _nm(start[0]), _nm(start[1])
    request.end.x_nm, request.end.y_nm = _nm(end[0]), _nm(end[1])
    request.layer = layer_value(layer)
    request.mode = 2 if shove else 1
    request.allow_partial = allow_partial
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


def layer_value(name: str) -> int:
    """KiCad's number for a copper layer named like "F_Cu" or "In2.Cu"."""
    from kicad_mcp._master_proto.mp.board import board_types_pb2 as board_types

    return int(board_types.BoardLayer.Value("BL_" + name.replace(".", "_")))


def clearance_map(
    net_name: str,
    layers: list[str],
    *,
    cell_mm: float = 0.1,
    width_mm: float = 0.0,
    include_vias: bool = True,
    ignore_tracks: bool = False,
    client: MasterKiCadClient | None = None,
) -> dict[str, Any]:
    """Ask KiCad where a track (and a via) of ``net_name`` may be placed.

    Returns ``origin`` (x, y of the first cell, mm), ``cell`` (mm), ``columns``,
    ``rows``, ``blocked`` (layer name to bytes, one per cell, row by row, 1 = not
    allowed), ``via_blocked`` (bytes, same layout) and the ``track_width``,
    ``via_diameter`` and ``via_drill`` KiCad used (mm).
    """
    from .board_setup import _board_document

    request_cls, response_cls = messages()[2:]
    # The grid takes KiCad some seconds on a full board.
    client = client or MasterKiCadClient(timeout_ms=180_000)
    request = request_cls()
    request.board.MergeFromString(_board_document(client).SerializeToString())
    request.net_name = net_name
    request.layers.extend(layer_value(name) for name in layers)
    request.cell.value_nm = _nm(cell_mm)
    if width_mm > 0:
        request.track_width.value_nm = _nm(width_mm)
    request.include_vias = include_vias
    request.ignore_tracks = ignore_tracks
    response = client.send(request, response_cls)
    return {
        "origin": (response.origin.x_nm / 1e6, response.origin.y_nm / 1e6),
        "cell": response.cell.value_nm / 1e6,
        "columns": int(response.columns),
        "rows": int(response.rows),
        "blocked": {
            name: bytes(layer.blocked) for name, layer in zip(layers, response.layers, strict=True)
        },
        "via_blocked": bytes(response.via_blocked),
        "track_width": response.track_width.value_nm / 1e6,
        "via_diameter": response.via_diameter.value_nm / 1e6,
        "via_drill": response.via_drill.value_nm / 1e6,
    }


def plan_connection(
    net_name: str,
    start: tuple[float, float, str],
    end: tuple[float, float, str],
    *,
    layer_costs: dict[str, float],
    via_cost_mm: float = 3.0,
    avoid: list[dict[str, float]] | None = None,
    rip_up: bool = False,
    rip_up_cost_mm: float = 2.0,
    kept_copper: list[tuple[str, float, float, float, float, float]] | None = None,
    width_mm: float = 0.0,
    cell_mm: float = 0.1,
    client: MasterKiCadClient | None = None,
) -> dict[str, Any]:
    """Plan one connection on KiCad's clearance grids; draw nothing.

    ``start`` and ``end`` are ``(x_mm, y_mm, layer)``. ``layer_costs`` names the
    layers that may be used and how dear each is (1 = normal; 0 = not at all).
    ``avoid`` holds keep-away areas ``{"x", "y", "radius_mm", "cost_mm"}``: passing
    through the centre costs as much as ``cost_mm`` of extra track per cell.
    With ``rip_up`` the path may cross other nets' tracks; the places are returned
    in ``through`` as ``(layer, x_mm, y_mm)``.
    ``kept_copper`` lists tracks that must not be crossed even then, each
    ``(layer, x1, y1, x2, y2, half_width)`` in mm; a via is a zero-length piece
    with layer "*".

    Returns ``ok``; on success ``waypoints`` (for ``route_track``), ``through``,
    ``width`` (mm), ``vias`` (count) and ``length_mm``; otherwise ``reason``.
    """
    from kicad_mcp.utils import route_planner

    layers = [name for name, cost in layer_costs.items() if cost > 0 or name in (start[2], end[2])]
    costs = [layer_costs[name] if layer_costs.get(name, 0) > 0 else 10.0 for name in layers]
    for name in (start[2], end[2]):
        if name not in layers:
            layers.append(name)
            costs.append(10.0)
    full = clearance_map(
        net_name, layers, cell_mm=cell_mm, width_mm=width_mm, include_vias=True, client=client
    )
    hard = None
    if rip_up:
        hard = clearance_map(
            net_name,
            layers,
            cell_mm=cell_mm,
            width_mm=width_mm,
            include_vias=False,
            ignore_tracks=True,
            client=client,
        )
    cell = full["cell"]
    origin_x, origin_y = full["origin"]
    hard_layers: list[bytes] | None = None
    if hard:
        marked = [bytearray(hard["blocked"][name]) for name in layers]
        reach_extra = full["track_width"] / 2 + 0.2
        for layer_name, x1, y1, x2, y2, half_width in kept_copper or []:
            reach = half_width + reach_extra
            first_column = max(0, int((min(x1, x2) - reach - origin_x) / cell))
            last_column = min(full["columns"] - 1, int((max(x1, x2) + reach - origin_x) / cell) + 1)
            first_row = max(0, int((min(y1, y2) - reach - origin_y) / cell))
            last_row = min(full["rows"] - 1, int((max(y1, y2) + reach - origin_y) / cell) + 1)
            dx, dy = x2 - x1, y2 - y1
            span = dx * dx + dy * dy
            targets = [
                marked[index] for index, name in enumerate(layers) if layer_name in ("*", name)
            ]
            for row in range(first_row, last_row + 1):
                py = origin_y + row * cell
                for column in range(first_column, last_column + 1):
                    px = origin_x + column * cell
                    along = (
                        0.0
                        if span == 0
                        else max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / span))
                    )
                    gap = ((px - x1 - along * dx) ** 2 + (py - y1 - along * dy) ** 2) ** 0.5
                    if gap < reach:
                        for target in targets:
                            target[row * full["columns"] + column] = 1
        hard_layers = [bytes(layer) for layer in marked]
    grid = route_planner.Grid(
        columns=full["columns"],
        rows=full["rows"],
        blocked=[full["blocked"][name] for name in layers],
        via_blocked=full["via_blocked"],
        hard_blocked=hard_layers,
        layer_cost=costs,
    )

    def to_cell(x: float, y: float) -> tuple[int, int]:
        column = min(max(int(round((x - origin_x) / cell)), 0), grid.columns - 1)
        row = min(max(int(round((y - origin_y) / cell)), 0), grid.rows - 1)
        return column, row

    if avoid:
        grid.penalty = route_planner.circle_penalty(
            grid,
            [
                (
                    (area["x"] - origin_x) / cell,
                    (area["y"] - origin_y) / cell,
                    area["radius_mm"] / cell,
                    area.get("cost_mm", 5.0) / cell,
                )
                for area in avoid
            ],
        )
    first = (layers.index(start[2]), *to_cell(start[0], start[1]))
    last = (layers.index(end[2]), *to_cell(end[0], end[1]))
    plan = route_planner.find_path(
        grid,
        first,
        last,
        via_cost=via_cost_mm / cell,
        rip_up_cost=rip_up_cost_mm / cell if rip_up else 0.0,
    )
    if plan is None:
        return {
            "ok": False,
            "reason": "no path on the allowed layers",
            "width": full["track_width"],
        }

    def position(column: int, row: int) -> tuple[float, float]:
        return round(origin_x + column * cell, 4), round(origin_y + row * cell, 4)

    points = route_planner.simplify(grid, plan)
    waypoints: list[dict[str, Any]] = []
    for before, here in zip(points, points[1:], strict=False):
        x, y = position(here[1], here[2])
        if here[0] != before[0]:
            via_at = position(before[1], before[2])
            if waypoints and (waypoints[-1]["x"], waypoints[-1]["y"]) == via_at:
                waypoints[-1]["layer"] = layers[here[0]]
            else:
                waypoints.append({"x": via_at[0], "y": via_at[1], "layer": layers[here[0]]})
        else:
            waypoints.append({"x": x, "y": y})
    if waypoints and "layer" not in waypoints[-1]:
        waypoints.pop()  # the last cell is the end itself
    length = 0.0
    for (_, c1, r1), (_, c2, r2) in zip(plan.cells, plan.cells[1:], strict=False):
        length += ((c2 - c1) ** 2 + (r2 - r1) ** 2) ** 0.5 * cell
    return {
        "ok": True,
        "waypoints": waypoints,
        "through": [
            (layers[layer], *position(column, row)) for layer, column, row in plan.through_tracks
        ],
        "width": full["track_width"],
        "vias": sum(1 for waypoint in waypoints if "layer" in waypoint),
        "length_mm": round(length, 2),
    }
