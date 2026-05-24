"""Thin pynng-based KiCad IPC client using master-aligned protos.

We can't reuse :mod:`kipy.client` here because it imports kipy's own
proto descriptors at module load, and those collide with the
:mod:`kicad_mcp._master_proto` descriptors (same proto file paths,
different field structures — kipy 0.7.1 lags master KiCad's wire
format). Loading both raises ``duplicate file name`` in the protobuf
descriptor pool.

This module provides just enough to send a request and unpack a
typed response, mirroring ``kipy.client.KiCadClient.send`` so the
upstream ``Schematic`` wrapper code stays mostly identical.
"""

from __future__ import annotations

import os
import platform
from tempfile import gettempdir
from typing import TYPE_CHECKING, TypeVar

import pynng  # type: ignore[import-untyped]

# Master protos. Path is injected in the package __init__ so all
# importers see them at the same location.
from google.protobuf.message_factory import GetMessageClass  # type: ignore[import-untyped]

from kicad_mcp._master_proto._pool import shared_pool
from kicad_mcp._master_proto.mp.common.envelope_pb2 import (
    ApiRequest,
    ApiResponse,
    ApiStatusCode,
)

# The master pool has its own ``google.protobuf.Any`` descriptor (seeded
# from the well-known proto in ``_pool.py``). Master-generated messages
# whose fields are typed ``google.protobuf.Any`` resolve to THIS class —
# not the stdlib ``google.protobuf.any_pb2.Any``. Mixing the two via
# CopyFrom / MergeFrom raises "Parameter must be instance of same class".
MasterAny = GetMessageClass(shared_pool.FindMessageTypeByName("google.protobuf.Any"))

if TYPE_CHECKING:
    from google.protobuf.message import Message  # type: ignore[import-untyped]


_R = TypeVar("_R", bound="Message")


class ApiError(RuntimeError):
    """Raised when KiCad returns a non-success status."""

    def __init__(
        self, message: str, *, status_code: int | None = None, raw_message: str = ""
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.raw_message = raw_message


class ConnectionError(RuntimeError):  # noqa: A001
    """Raised when the socket can't be reached."""


def default_socket_path() -> str:
    """Default IPC socket path, mirroring kipy's resolution order."""
    override = os.environ.get("KICAD_API_SOCKET")
    if override:
        return override
    if platform.system() == "Windows":
        return f"ipc://{gettempdir()}\\kicad\\api.sock"
    home = os.environ.get("HOME")
    if home:
        flatpak = f"{home}/.var/app/org.kicad.KiCad/cache/tmp/kicad/api.sock"
        if os.path.exists(flatpak):
            return f"ipc://{flatpak}"
    return "ipc:///tmp/kicad/api.sock"


class MasterKiCadClient:
    """Single-shot connect-on-send req/rep client over nanomsg.

    Instances are cheap: we don't hold the socket open across calls
    because the Req0 socket has a stateful conversation pattern that
    breaks if the peer restarts (which eeschema does whenever the
    user opens/closes a project). Each :meth:`send` dials, exchanges
    one envelope, and tears down.
    """

    def __init__(self, socket_path: str | None = None, *, timeout_ms: int = 5_000) -> None:
        self.socket_path = socket_path or default_socket_path()
        self.timeout_ms = timeout_ms

    def send(self, command: Message, response_cls: type[_R]) -> _R:
        """Send ``command``, expect ``response_cls`` back.

        Raises :class:`ApiError` on non-success status,
        :class:`ConnectionError` on socket failure.
        """
        env = ApiRequest()
        env.message.Pack(command)
        sock = pynng.Req0(recv_timeout=self.timeout_ms, send_timeout=self.timeout_ms)
        try:
            try:
                sock.dial(self.socket_path)
            except Exception as exc:
                raise ConnectionError(
                    f"Failed to connect to KiCad at {self.socket_path}: {exc}"
                ) from None
            try:
                sock.send(env.SerializeToString())
                reply_bytes = sock.recv()
            except Exception as exc:
                raise ConnectionError(f"IPC exchange failed: {exc}") from None
        finally:
            sock.close()
        reply = ApiResponse()
        reply.ParseFromString(reply_bytes)
        if reply.status.status != ApiStatusCode.AS_OK:
            raise ApiError(
                f"KiCad returned error: {reply.status.error_message}",
                status_code=reply.status.status,
                raw_message=reply.status.error_message,
            )
        out = response_cls()
        reply.message.Unpack(out)
        return out  # type: ignore[no-any-return]
