"""Run KiCad's IPC API without any editor window.

KiCad 11's ``kicad-cli api-server`` serves one document: started on a
``.kicad_sch`` it answers schematic commands, on a ``.kicad_pcb`` board commands.
With ``KICAD_MCP_HEADLESS=1`` this module starts one server per document on
demand and tells the IPC clients which socket to use for each command, so the
schematic and PCB editors do not have to be open.

Do not keep the same project open in KiCad's editors while headless servers are
editing it: two programs would be saving the same files.
"""

from __future__ import annotations

import atexit
import os
import subprocess  # noqa: S404 - runs the configured kicad-cli only
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Literal

Kind = Literal["schematic", "board"]

START_TIMEOUT_S = 30.0

_lock = threading.Lock()
_servers: dict[Kind, tuple[subprocess.Popen[bytes], str, Path]] = {}
_socket_dir: Path | None = None


def enabled() -> bool:
    """True when the server should drive headless API servers instead of the GUI."""
    return os.environ.get("KICAD_MCP_HEADLESS", "").strip().casefold() in {"1", "true", "yes"}


def _document_for(kind: Kind) -> Path:
    from kicad_mcp.config import get_config

    cfg = get_config()
    path = cfg.sch_file if kind == "schematic" else cfg.pcb_file
    if path is None or not Path(path).exists():
        raise RuntimeError(
            f"Headless mode needs a {kind} file, but the active project has none. "
            "Call kicad_set_project() first."
        )
    return Path(path)


def _ready(url: str, kind: Kind) -> bool:
    """True once the server has loaded its document and lists it as open."""
    import pynng

    from kicad_mcp._master_proto.mp.common.commands.editor_commands_pb2 import (
        GetOpenDocuments,
        GetOpenDocumentsResponse,
    )
    from kicad_mcp._master_proto.mp.common.envelope_pb2 import (
        ApiRequest,
        ApiResponse,
        ApiStatusCode,
    )
    from kicad_mcp._master_proto.mp.common.types.base_types_pb2 import DocumentType

    command = GetOpenDocuments()
    command.type = DocumentType.DOCTYPE_PCB if kind == "board" else DocumentType.DOCTYPE_SCHEMATIC
    request = ApiRequest()
    request.message.Pack(command)
    sock = pynng.Req0(recv_timeout=1500, send_timeout=1500)
    try:
        sock.dial(url)
        sock.send(request.SerializeToString())
        raw = sock.recv()
    except Exception:  # noqa: BLE001 - any failure means "not ready yet"
        return False
    finally:
        sock.close()
    reply = ApiResponse()
    reply.ParseFromString(raw)
    if reply.status.status != ApiStatusCode.AS_OK:
        return False  # still loading: "KiCad is not ready to reply"
    documents = GetOpenDocumentsResponse()
    reply.message.Unpack(documents)
    return len(documents.documents) > 0


def socket_for(kind: Kind) -> str:
    """Return the ``ipc://`` URL of the headless server for ``kind``, starting it if needed."""
    global _socket_dir
    with _lock:
        document = _document_for(kind)
        running = _servers.get(kind)
        if running is not None:
            process, url, served = running
            if process.poll() is None and served == document:
                return url
            _stop(kind)

        from kicad_mcp.config import get_config

        cli = get_config().kicad_cli
        if cli is None or not Path(cli).exists():
            raise RuntimeError("Headless mode needs kicad-cli (KICAD_MCP_KICAD_CLI).")
        if _socket_dir is None:
            # Unix socket paths are limited to about 100 characters; keep this one short.
            _socket_dir = Path(tempfile.mkdtemp(prefix="kmcp-", dir="/tmp"))  # noqa: S108
            atexit.register(stop_all)
        socket_path = _socket_dir / f"{kind}.sock"
        socket_path.unlink(missing_ok=True)
        process = subprocess.Popen(  # noqa: S603 - fixed argv
            [str(cli), "api-server", "--socket", str(socket_path), str(document)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        url = f"ipc://{socket_path}"
        deadline = time.monotonic() + START_TIMEOUT_S
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(
                    f"kicad-cli api-server exited at once (code {process.returncode}) "
                    f"for {document.name}."
                )
            if socket_path.exists() and _ready(url, kind):
                _servers[kind] = (process, url, document)
                return url
            time.sleep(0.25)
        process.terminate()
        raise RuntimeError(
            f"The headless KiCad API server for {document.name} did not answer within "
            f"{START_TIMEOUT_S:.0f} s."
        )


def _stop(kind: Kind) -> None:
    running = _servers.pop(kind, None)
    if running is None:
        return
    process = running[0]
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def stop(kind: Kind) -> None:
    """Stop the headless server for ``kind`` (it restarts on the next command)."""
    with _lock:
        _stop(kind)


def stop_all() -> None:
    """Stop every headless server this process started."""
    with _lock:
        for kind in list(_servers):
            _stop(kind)


def status() -> dict[str, str]:
    """Which headless servers are running, by kind."""
    with _lock:
        return {
            kind: f"{document.name} (pid {process.pid})"
            for kind, (process, _url, document) in _servers.items()
            if process.poll() is None
        }


_DOCTYPE_PCB = 3  # kiapi.common.types.DocumentType.DOCTYPE_PCB
_last_kind: Kind = "schematic"


def kind_of(command: Any) -> Kind:  # noqa: ANN401 - any protobuf message
    """Decide which document a command is for.

    Board and schematic commands are told apart by their package, then by the
    document they name; commands that name none (version, libraries) go to
    whichever server was used last.
    """
    global _last_kind
    name = command.DESCRIPTOR.full_name
    kind: Kind | None = None
    if name.startswith("kiapi.board."):
        kind = "board"
    elif name.startswith("kiapi.schematic."):
        kind = "schematic"
    elif name.endswith(".GetOpenDocuments"):
        kind = "board" if int(command.type) == _DOCTYPE_PCB else "schematic"
    else:
        for holder in (command, getattr(command, "header", None)):
            for field in ("document", "board"):
                specifier = getattr(holder, field, None) if holder is not None else None
                doc_type = getattr(specifier, "type", None)
                if doc_type:
                    kind = "board" if int(doc_type) == _DOCTYPE_PCB else "schematic"
                    break
            if kind is not None:
                break
    if kind is None:
        return _last_kind
    _last_kind = kind
    return kind
