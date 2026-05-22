# pyright: reportUnknownVariableType=false
"""Internal IPC client extensions for KiCad's nanomsg API.

This subpackage layers higher-level wrappers on top of :mod:`kipy` for
surfaces that kipy itself does not (yet) cover. Today the only inhabitant is
:class:`Schematic`, which mirrors :class:`kipy.board.Board` for eeschema
documents.

These wrappers exist because upstream KiCad implemented schematic item
creation (commit ``3dca4e0e38`` by Jon Evans, 2026-04-07) on the C++ side
without shipping a corresponding Python helper. We provide one here so the
MCP server can drive eeschema directly once we are running a KiCad build
that contains that commit.

.. warning::

   The mutation calls in :mod:`kicad_mcp.ipc.schematic` crash eeschema on
   any KiCad 10.0.x stable release (verified against 10.0.1 on 2026-05-21).
   They require KiCad master or a future release containing the
   ``3dca4e0e38`` commit. Runtime gating belongs to the MCP layer; this
   package does not enforce it.
"""

from __future__ import annotations

from kicad_mcp.ipc.runtime_gate import (
    SCH_IPC_OPT_IN_ENV,
    SCH_IPC_PERSISTENCE_HINT,
    reset_runtime_gate_cache,
    route_schematic_create,
    should_use_ipc_for_schematic_mutation,
)
from kicad_mcp.ipc.schematic import Schematic, open_schematic

__all__ = (
    "SCH_IPC_OPT_IN_ENV",
    "SCH_IPC_PERSISTENCE_HINT",
    "Schematic",
    "open_schematic",
    "reset_runtime_gate_cache",
    "route_schematic_create",
    "should_use_ipc_for_schematic_mutation",
)
