"""Work around gaps in released kipy (kicad-python <= 0.8) for footprints.

* kipy unwraps footprint items through a fixed table of the item types its
  release knows, and raises on anything else. KiCad master adds item types
  (``kiapi.board.types.ReferencePoint``, for example), so every footprint
  read fails. ``install()`` keeps such items as :class:`OpaqueItem` wrappers
  decoded with the vendored master protos, so a footprint read and written
  back with ``update_items`` keeps them.
* ``FootprintInstance.orientation`` rebuilds the footprint's item list from
  fields, pads, text, zones and shapes only, so rotating a footprint drops
  its 3D models, text boxes and anything else. ``install()`` puts those
  items back after the rotation.
* The position and orientation setters also move and rotate opaque items
  that have a position.

kicad-python main fixed the rotation and unknown-item handling in November
2026; remove this once a release with those fixes is in use.
"""

from __future__ import annotations

from typing import Any

from google.protobuf.message import Message  # type: ignore[import-untyped]
from google.protobuf.message_factory import GetMessageClass  # type: ignore[import-untyped]

_installed = False


class OpaqueItem:
    """A board item kipy has no wrapper for, kept as its master proto."""

    def __init__(self, proto: Message) -> None:
        self._proto = proto

    @property
    def proto(self) -> Message:
        return self._proto

    def _position(self) -> Any | None:  # noqa: ANN401
        if "position" not in self._proto.DESCRIPTOR.fields_by_name:
            return None
        return self._proto.position

    def translate(self, delta: Any) -> None:  # noqa: ANN401
        position = self._position()
        if position is not None:
            position.x_nm += delta.x
            position.y_nm += delta.y

    def rotate(self, delta: Any, center: Any) -> None:  # noqa: ANN401
        from kipy.geometry import Vector2

        position = self._position()
        if position is not None:
            rotated = Vector2.from_xy(position.x_nm, position.y_nm).rotate(delta, center)
            position.x_nm = rotated.x
            position.y_nm = rotated.y

    def __repr__(self) -> str:
        return f"OpaqueItem({self._proto.DESCRIPTOR.full_name})"


def _master_message(type_url: str) -> Message | None:
    import kicad_mcp._master_proto  # noqa: F401
    from kicad_mcp._master_proto._pool import shared_pool
    from kicad_mcp._master_proto.mp.board import board_types_pb2  # noqa: F401

    name = type_url.rsplit("/", 1)[-1]
    try:
        descriptor = shared_pool.FindMessageTypeByName(name)
    except KeyError:
        return None
    return GetMessageClass(descriptor)()


def install() -> None:
    """Patch kipy's board item unwrapping to tolerate unknown item types."""

    global _installed
    if _installed:
        return

    import kipy.board_types as board_types

    original_unwrap = board_types.unwrap

    def unwrap(message: Any) -> Any:  # noqa: ANN401
        try:
            return original_unwrap(message)
        except NotImplementedError:
            concrete = _master_message(message.type_url)
            if concrete is None or not message.Unpack(concrete):
                raise
            return OpaqueItem(concrete)

    board_types.unwrap = unwrap
    _patch_footprint_transforms(board_types)
    _installed = True


def _patch_footprint_transforms(board_types: Any) -> None:  # noqa: ANN401
    from kipy.geometry import Angle

    footprint = board_types.FootprintInstance
    rotated_types = (
        board_types.Field,
        board_types.Pad,
        board_types.BoardText,
        board_types.Zone,
        board_types.BoardShape,
    )
    position_prop = footprint.position
    orientation_prop = footprint.orientation

    def set_position(self: Any, position: Any) -> None:  # noqa: ANN401
        delta = position - self.position
        position_prop.fset(self, position)
        for item in self.definition.items:
            if isinstance(item, OpaqueItem):
                item.translate(delta)

    def set_orientation(self: Any, orientation: Any) -> None:  # noqa: ANN401
        before = self.orientation.degrees
        kept = [item for item in self.definition.items if not isinstance(item, rotated_types)]
        orientation_prop.fset(self, orientation)
        delta = Angle.from_degrees(self.orientation.degrees - before)
        for item in kept:
            if isinstance(item, OpaqueItem):
                item.rotate(delta, self.position)
        self.definition.items = [*self.definition.items, *kept]

    footprint.position = property(position_prop.fget, set_position, doc=position_prop.__doc__)
    footprint.orientation = property(
        orientation_prop.fget, set_orientation, doc=orientation_prop.__doc__
    )
