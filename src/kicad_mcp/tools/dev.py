"""Development tools: use changed server code without restarting the server.

Enabled only with ``KICAD_MCP_DEV_TOOLS=1``. Restarting an MCP server normally needs
the user to reconnect it in their client. ``dev_reload_tools`` re-imports the tool
code into the running server instead, and ``dev_call_tool`` calls any tool by name,
including ones the client has not listed yet.
"""

from __future__ import annotations

import os
import sys
from typing import Any

from mcp.server.fastmcp import FastMCP

# Modules that hold live state and are therefore kept across a reload: the headless
# KiCad API servers, the review page's HTTP server, the configuration, and this module.
_KEPT = {
    "kicad_mcp.ipc.headless",
    "kicad_mcp.tools.review",
    "kicad_mcp.tools.dev",
}
TOOL_NAMES = {"dev_reload_tools", "dev_call_tool"}
_RELOADED_PREFIXES = ("kicad_mcp.tools", "kicad_mcp.utils", "kicad_mcp.ipc", "kicad_mcp.models")
_RELOADED_MODULES = ("kicad_mcp.connection", "kicad_mcp.discovery", "kicad_mcp.kicad.session")


def enabled() -> bool:
    """True when the development tools should be registered."""
    return os.environ.get("KICAD_MCP_DEV_TOOLS", "").strip().casefold() in {"1", "true", "yes"}


def _reloadable(name: str) -> bool:
    if name in _KEPT:
        return False
    if name in _RELOADED_MODULES:
        return True
    return any(name == prefix or name.startswith(prefix + ".") for prefix in _RELOADED_PREFIXES)


def reload_into(live: FastMCP) -> tuple[list[str], list[str]]:
    """Re-import the tool code and swap the running server's tools for the fresh ones.

    Returns ``(added, removed)`` tool names. The active sheet and the cached KiCad
    connection are reset; headless KiCad servers and the review page keep running.
    """
    from kicad_mcp import server as server_module

    before = set(live._tool_manager._tools)  # noqa: SLF001 - FastMCP has no public swap
    connection = sys.modules.get("kicad_mcp.connection")
    if connection is not None:
        connection.reset_connection()
    for name in [name for name in sys.modules if _reloadable(name)]:
        del sys.modules[name]

    from kicad_mcp.tools import router as fresh_router

    server_module.router = fresh_router  # type: ignore[attr-defined]
    profile = getattr(live, "active_profile", None)
    fresh = server_module.build_server(profile)
    ensure = getattr(fresh, "ensure_registered", None)
    if callable(ensure):
        ensure()
    live._tool_manager._tools.clear()  # noqa: SLF001
    live._tool_manager._tools.update(fresh._tool_manager._tools)  # noqa: SLF001
    live.allowed_tool_names = fresh.allowed_tool_names  # type: ignore[attr-defined]
    after = set(live._tool_manager._tools)  # noqa: SLF001
    return sorted(after - before), sorted(before - after)


# The server the client is connected to. This module is kept across reloads, so the
# reference survives; the tools registered on a rebuilt server must act on this one,
# not on the rebuilt copy they were registered with.
_live: FastMCP | None = None


def register(server: FastMCP) -> None:
    """Register the development tools."""
    global _live
    if _live is None:
        _live = server
    mcp = _live

    @server.tool()
    def dev_reload_tools() -> str:
        """Load changed server code into the running server, without a restart.

        For work on this MCP server itself: after editing its source, call this and
        the tools run the new code. Tools that are new since the client connected may
        not appear in the client's tool list; call those with dev_call_tool. The
        active sheet (sch_set_active_sheet) is reset to the root. Running headless
        KiCad servers and the review page are kept. A change to the headless or review
        code itself still needs a restart.
        """
        try:
            added, removed = reload_into(mcp)
        except Exception as exc:  # noqa: BLE001 - report the import error, keep serving
            return f"Reload failed, the previous tools stay in place: {type(exc).__name__}: {exc}"
        lines = [f"Reloaded. {len(mcp._tool_manager._tools)} tools registered."]  # noqa: SLF001
        if added:
            lines.append(f"New: {', '.join(added)} (call with dev_call_tool if not listed)")
        if removed:
            lines.append(f"Gone: {', '.join(removed)}")
        lines.append("The active sheet was reset to the root.")
        return "\n".join(lines)

    @server.tool()
    async def dev_call_tool(name: str, arguments: dict[str, Any] | None = None) -> Any:  # noqa: ANN401
        """Call any tool of this server by name, with its arguments as an object.

        Use it for tools added by dev_reload_tools that the client does not list yet.
        The result is whatever the named tool returns, pictures included.
        """
        result = await mcp.call_tool(name, arguments or {})
        content = result[0] if isinstance(result, tuple) else result
        return list(content)
