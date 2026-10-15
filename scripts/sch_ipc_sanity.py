"""
Schematic IPC sanity probe.

!!! DESTRUCTIVE — DO NOT RUN AGAINST A LIVE EESCHEMA WITH UNSAVED WORK !!!

When run against KiCad 10.0.1 on 2026-05-21, sending a single CreateItems
IPC message with a GlobalLabel proto CRASHED eeschema. The user lost all
unsaved in-memory edits. See memory file
`feedback_sch_ipc_mutation_crashes_eeschema.md` for the full incident.

The eeschema CreateItems handler at
`eeschema/api/api_handler_sch.cpp:134-285` is REGISTERED in 10.0.1 but
the input-validation path (`validateDocumentInternal` at line 52-62) is
a TODO stub. Bad input crashes instead of returning AS_BAD_REQUEST.

This file is retained as a REPRO for filing an upstream bug at
gitlab.com/kicad/code/kicad. Do not run it for any other reason. Before
re-running:

  - confirm upstream has added defensive validation
  - run in a throwaway project, not on real design work
  - assume eeschema will crash and any unsaved state will be lost
"""

from __future__ import annotations

import sys

from kipy import KiCad
from kipy.client import ApiError
from kipy.proto.common.commands.editor_commands_pb2 import (
    CreateItems,
    CreateItemsResponse,
)
from kipy.proto.common.types import DocumentType
from kipy.proto.schematic.schematic_types_pb2 import GlobalLabel
from kipy.util import pack_any

SACRIFICIAL_LABEL = "MCP_TEST_DELETEME_001"
# 100 mm, 100 mm -- KiCad protos use nanometers
PROBE_X_NM = 100_000_000
PROBE_Y_NM = 100_000_000


def main() -> int:
    print("==> connecting to KiCad IPC server")
    kicad = KiCad()
    version = kicad.get_version()
    print(f"    connected: KiCad {version}")

    print("==> listing open schematic documents")
    docs = list(kicad.get_open_documents(DocumentType.DOCTYPE_SCHEMATIC))
    if not docs:
        print("    no open schematic. open one in eeschema and retry.")
        return 1
    for i, d in enumerate(docs):
        print(
            f"    [{i}] board_filename={d.board_filename!r} "
            f"project={d.project.name!r} type={d.type}"
        )

    sch_doc = docs[0]
    print(f"==> target doc: {sch_doc.board_filename!r}")

    print("==> building GlobalLabel proto")
    label = GlobalLabel()
    label.position.x_nm = PROBE_X_NM
    label.position.y_nm = PROBE_Y_NM
    label.text.text.text = SACRIFICIAL_LABEL
    print(f"    name={SACRIFICIAL_LABEL!r} pos=({PROBE_X_NM / 1e6}mm, {PROBE_Y_NM / 1e6}mm)")

    print("==> sending CreateItems via IPC")
    cmd = CreateItems()
    cmd.header.document.CopyFrom(sch_doc)
    cmd.items.append(pack_any(label))

    try:
        response = kicad._client.send(cmd, CreateItemsResponse)
    except ApiError as e:
        print(f"    ApiError: {e}")
        return 2

    print(f"    response status: {response.status}")
    print(f"    created_items count: {len(response.created_items)}")
    for r in response.created_items:
        print(f"      - status={r.status} item_type={r.item.type_url}")

    print()
    print("Manual verification — look at eeschema NOW and answer:")
    print(f"  1. Did a label named '{SACRIFICIAL_LABEL}' appear at (~100mm, 100mm)?")
    print("  2. Is your USER_EDIT_DONT_LOSE label STILL THERE?")
    print("  3. Press Ctrl-Z once. Does ONLY the new label disappear, leaving your edit intact?")
    print()
    print(
        "If all three are YES, IPC mutation is a viable streaming path "
        "and we can build the kipy Schematic class on top of it."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
