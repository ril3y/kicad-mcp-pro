"""Sanity probe using regenerated master protos.

Bypasses kipy entirely so we don't double-load the older descriptors
that kipy ships. Talks to KiCad's IPC socket directly via pynng.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Insert master proto package FIRST so all imports resolve to it.
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "kicad_mcp" / "_master_proto"))

import pynng  # noqa: E402
from common.commands.editor_commands_pb2 import (  # noqa: E402
    CreateItems,
    CreateItemsResponse,
    GetOpenDocuments,
    GetOpenDocumentsResponse,
)
from common.envelope_pb2 import ApiRequest, ApiResponse  # noqa: E402
from common.types.base_types_pb2 import DocumentType  # noqa: E402
from google.protobuf.any_pb2 import Any  # noqa: E402
from schematic.schematic_types_pb2 import GlobalLabel  # noqa: E402

# Default Windows KiCad IPC socket path. KICAD_API_SOCKET env override is ignored
# here — keep the script self-contained.
SOCK = "ipc:///C:/Users/riley/AppData/Local/Temp/kicad/api.sock"


def send(  # noqa: ANN201
    sock: pynng.Req0,
    command,  # noqa: ANN001 -- proto Message; any protobuf type with .Pack works
    response_cls,  # noqa: ANN001 -- proto Message class
):
    env = ApiRequest()
    env.message.Pack(command)
    sock.send(env.SerializeToString())
    reply_bytes = sock.recv()
    reply = ApiResponse()
    reply.ParseFromString(reply_bytes)
    if reply.status.status != 1:  # AS_OK
        raise RuntimeError(
            f"API error status={reply.status.status} msg={reply.status.error_message}"
        )
    out = response_cls()
    reply.message.Unpack(out)
    return out


def main() -> int:
    print("==> connect")
    sock = pynng.Req0()
    sock.dial(SOCK)

    print("==> list open schematic documents")
    gd = GetOpenDocuments()
    gd.type = DocumentType.DOCTYPE_SCHEMATIC
    docs_resp = send(sock, gd, GetOpenDocumentsResponse)
    docs = list(docs_resp.documents)
    print(f"   docs: {len(docs)}")
    for d in docs:
        print(f"   - project={d.project.name!r} file={d.board_filename!r}")
    if not docs:
        print("no schematic open")
        return 1

    print("==> build master-aligned GlobalLabel")
    label = GlobalLabel()
    label.position.x_nm = 10_000_000  # 10mm
    label.position.y_nm = 10_000_000
    # NEW master structure: label.text is directly base_types.Text (2-deep)
    label.text.text = "MASTER_OK"
    label.text.position.x_nm = 10_000_000
    label.text.position.y_nm = 10_000_000
    label.text.attributes.size.x_nm = 1_270_000
    label.text.attributes.size.y_nm = 1_270_000

    print("==> send CreateItems")
    cmd = CreateItems()
    cmd.header.document.CopyFrom(docs[0])
    any_item = Any()
    any_item.Pack(label)
    cmd.items.append(any_item)
    resp = send(sock, cmd, CreateItemsResponse)
    print(f"   response status: {resp.status}")
    print(f"   created_items: {len(resp.created_items)}")
    for r in resp.created_items:
        print(f"     status={r.status.code} item_type={r.item.type_url}")

    print()
    print(
        "Look at eeschema — there should be a global label 'MASTER_OK' "
        "at (10mm, 10mm) WITH VISIBLE TEXT."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
