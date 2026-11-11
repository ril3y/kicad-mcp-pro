"""kipy_compat keeps board items a released kipy doesn't know about."""

from __future__ import annotations

from google.protobuf.any_pb2 import Any
from kipy.board_types import FootprintInstance, Pad
from kipy.proto.board import board_types_pb2

import kicad_mcp._master_proto  # noqa: F401
from kicad_mcp import kipy_compat
from kicad_mcp._master_proto.mp.board.board_types_pb2 import ReferencePoint


def _footprint_with_reference_point() -> board_types_pb2.FootprintInstance:
    proto = board_types_pb2.FootprintInstance()
    pad = Any()
    pad.Pack(board_types_pb2.Pad())
    point = ReferencePoint()
    point.id.value = "rp-1"
    unknown = Any()
    unknown.Pack(point)
    proto.definition.items.extend([pad, unknown])
    return proto


def test_unknown_items_are_kept_opaque_and_round_trip() -> None:
    kipy_compat.install()
    footprint = FootprintInstance(_footprint_with_reference_point())

    items = footprint.definition.items
    assert isinstance(items[0], Pad)
    assert isinstance(items[1], kipy_compat.OpaqueItem)
    assert len(footprint.definition.pads) == 1

    repacked = footprint.proto.definition.items
    assert [a.type_url.rsplit("/", 1)[-1] for a in repacked] == [
        "kiapi.board.types.Pad",
        "kiapi.board.types.ReferencePoint",
    ]
    restored = ReferencePoint()
    assert repacked[1].Unpack(restored)
    assert restored.id.value == "rp-1"


def test_install_is_idempotent() -> None:
    kipy_compat.install()
    kipy_compat.install()
    FootprintInstance(_footprint_with_reference_point())


def _footprint_with_model_and_point() -> FootprintInstance:
    kipy_compat.install()
    proto = board_types_pb2.FootprintInstance()
    model = Any()
    model.Pack(board_types_pb2.Footprint3DModel(filename="part.step"))
    point = ReferencePoint()
    point.position.x_nm = 1_000_000
    point.position.y_nm = 0
    packed_point = Any()
    packed_point.Pack(point)
    proto.definition.items.extend([model, packed_point])
    return FootprintInstance(proto)


def _types(footprint: FootprintInstance) -> list[str]:
    return [a.type_url.rsplit("/", 1)[-1] for a in footprint.proto.definition.items]


def test_rotation_keeps_3d_models_and_rotates_opaque_items() -> None:
    from kipy.geometry import Angle

    footprint = _footprint_with_model_and_point()
    footprint.orientation = Angle.from_degrees(90)

    assert sorted(_types(footprint)) == [
        "kiapi.board.types.Footprint3DModel",
        "kiapi.board.types.ReferencePoint",
    ]
    point = next(i for i in footprint.definition.items if isinstance(i, kipy_compat.OpaqueItem))
    assert abs(point.proto.position.x_nm) <= 1
    assert abs(abs(point.proto.position.y_nm) - 1_000_000) <= 1


def test_move_translates_opaque_items() -> None:
    from kipy.geometry import Vector2

    footprint = _footprint_with_model_and_point()
    footprint.position = Vector2.from_xy(5_000_000, 2_000_000)

    point = next(i for i in footprint.definition.items if isinstance(i, kipy_compat.OpaqueItem))
    assert point.proto.position.x_nm == 6_000_000
    assert point.proto.position.y_nm == 2_000_000
    assert "kiapi.board.types.Footprint3DModel" in _types(footprint)
