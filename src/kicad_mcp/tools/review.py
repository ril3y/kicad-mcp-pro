"""A review page the owner can open in a browser.

Each item pairs what a datasheet shows (an example circuit, a recommended layout)
with what was built or is proposed for this project (a schematic sheet, a board
region), plus notes. Items live in ``<project>/review/`` as PNG files and an
``items.json``; ``index.html`` is regenerated on every change and can be opened
directly or served on localhost with ``review_serve``.
"""

from __future__ import annotations

import html
import json
import re
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from ..config import get_config
from .metadata import headless_compatible, requires_dependency

REVIEW_DIRNAME = "review"
_server: ThreadingHTTPServer | None = None
_server_lock = threading.Lock()


def _review_dir() -> Path:
    cfg = get_config()
    if cfg.project_dir is None:
        raise ValueError("No active project is configured. Call kicad_set_project() first.")
    folder = cfg.project_dir / REVIEW_DIRNAME
    (folder / "img").mkdir(parents=True, exist_ok=True)
    return folder


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")
    if not slug:
        raise ValueError("The title needs at least one letter or digit.")
    return slug[:60]


def _load(folder: Path) -> list[dict[str, Any]]:
    path = folder / "items.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="20">
<title>{project} review</title>
<style>
:root {{ --bg:#f6f5f1; --card:#ffffff; --ink:#1d1f21; --muted:#676b70; --line:#d9d6ce;
  --ref:#8a5a00; --mine:#0b5d6b; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#15171a; --card:#1e2125; --ink:#e8e6e1; --muted:#9a9ea4; --line:#33373d;
    --ref:#e0b25a; --mine:#6cc6d4; }}
}}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
  font: 15px/1.5 -apple-system, "Segoe UI", system-ui, sans-serif; }}
header, main {{ max-width: 1500px; margin: 0 auto; padding: 16px; }}
h1 {{ font-size: 22px; margin: 8px 0 2px; }}
h2 {{ font-size: 13px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted);
  margin: 28px 0 10px; border-bottom: 1px solid var(--line); padding-bottom: 6px; }}
.sub {{ color: var(--muted); margin: 0; }}
article {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px;
  padding: 16px; margin: 0 0 18px; }}
article h3 {{ margin: 0 0 4px; font-size: 18px; }}
.when {{ color: var(--muted); font-size: 12px; }}
.pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; }}
@media (max-width: 900px) {{ .pair {{ grid-template-columns: 1fr; }} }}
figure {{ margin: 0; min-width: 0; }}
figcaption {{ font-size: 12px; margin-bottom: 6px; }}
.tag {{ font-weight: 600; letter-spacing: .04em; text-transform: uppercase; font-size: 11px; }}
.ref .tag {{ color: var(--ref); }} .mine .tag {{ color: var(--mine); }}
.src {{ color: var(--muted); }}
img {{ width: 100%; height: auto; display: block; border: 1px solid var(--line);
  border-radius: 6px; background: #fff; }}
.none {{ border: 1px dashed var(--line); border-radius: 6px; padding: 24px; color: var(--muted);
  text-align: center; }}
.notes {{ margin: 12px 0 0; white-space: pre-wrap; }}
.empty {{ color: var(--muted); padding: 40px 0; }}
</style>
</head>
<body>
<header>
<h1>{project}: design review</h1>
<p class="sub">Left: what the datasheet shows. Right: what was built or is proposed.
Updated {updated}. The page reloads itself every 20 seconds.</p>
</header>
<main>
{body}
</main>
</body>
</html>
"""


def _figure(kind: str, tag: str, part: dict[str, Any] | None) -> str:
    if not part or not part.get("image"):
        return f'<figure class="{kind}"><figcaption><span class="tag">{tag}</span></figcaption><div class="none">nothing yet</div></figure>'  # noqa: E501
    caption = html.escape(str(part.get("caption", "")))
    image = html.escape(str(part["image"]))
    stamp = int(part.get("stamp", 0))
    return (
        f'<figure class="{kind}"><figcaption><span class="tag">{tag}</span> '
        f'<span class="src">{caption}</span></figcaption>'
        f'<a href="{image}"><img src="{image}?v={stamp}" alt="{caption}"></a></figure>'
    )


def write_page(folder: Path, items: list[dict[str, Any]]) -> Path:
    """Write ``items.json`` and regenerate ``index.html``."""
    (folder / "items.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
    sections: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        sections.setdefault(str(item.get("section") or "General"), []).append(item)
    chunks: list[str] = []
    for section, members in sections.items():
        chunks.append(f"<h2>{html.escape(section)}</h2>")
        for item in members:
            notes = html.escape(str(item.get("notes", "")))
            chunks.append(
                "<article>"
                f"<h3>{html.escape(str(item['title']))}</h3>"
                f'<div class="when">updated {html.escape(str(item.get("updated", "")))}</div>'
                '<div class="pair">'
                + _figure("ref", "From the datasheet", item.get("reference"))
                + _figure("mine", "Built / proposed", item.get("proposal"))
                + "</div>"
                + (f'<p class="notes">{notes}</p>' if notes else "")
                + "</article>"
            )
    if not chunks:
        chunks.append('<p class="empty">No review items yet.</p>')
    cfg = get_config()
    project = cfg.project_file.stem if cfg.project_file else folder.parent.name
    page = _PAGE.format(
        project=html.escape(project),
        updated=time.strftime("%Y-%m-%d %H:%M:%S"),
        body="\n".join(chunks),
    )
    index = folder / "index.html"
    index.write_text(page, encoding="utf-8")
    return index


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        _ = (format, args)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def serve(folder: Path, port: int) -> str:
    """Serve ``folder`` on localhost; reuse the running server when there is one."""
    global _server
    with _server_lock:
        if _server is not None:
            return f"http://127.0.0.1:{_server.server_address[1]}/"
        handler = partial(_QuietHandler, directory=str(folder))
        last_error: OSError | None = None
        for candidate in range(port, port + 20):
            try:
                _server = ThreadingHTTPServer(("127.0.0.1", candidate), handler)
                break
            except OSError as exc:
                last_error = exc
        if _server is None:
            raise OSError(f"No free port from {port} to {port + 19}: {last_error}")
        threading.Thread(target=_server.serve_forever, daemon=True).start()
        return f"http://127.0.0.1:{_server.server_address[1]}/"


def register(mcp: FastMCP) -> None:
    """Register the review-page tools."""

    @mcp.tool()
    @headless_compatible
    def review_serve(port: int = 8765) -> str:
        """Start the review page on localhost and return its address.

        The page shows every review item: the datasheet figure beside what was built
        or proposed. It is served only on this machine, from ``<project>/review/``,
        for as long as this MCP server runs; call this again after a reconnect.

        Args:
            port: First port to try; the next free one up to 19 higher is used.
        """
        folder = _review_dir()
        write_page(folder, _load(folder))
        try:
            url = serve(folder, port)
        except OSError as exc:
            return f"The review page could not be served: {exc}"
        return f"Review page: {url} ({len(_load(folder))} item(s)). Files: {folder}"

    @mcp.tool()
    @headless_compatible
    @requires_dependency("datasheets")
    def review_add(
        title: str,
        section: str = "",
        notes: str = "",
        datasheet_part: str = "",
        datasheet_page: int = 0,
        datasheet_crop: str = "",
        datasheet_caption: str = "",
        sheet: str = "",
        sheet_crop: str = "",
        board_region: str = "",
        board_layers: str = "F.Cu,F.Fab,F.CrtYd,Edge.Cuts",
        proposal_caption: str = "",
    ) -> str:
        """Add or update one item on the review page.

        An item pairs a datasheet figure with a picture of this project and notes.
        Give the datasheet side with ``datasheet_part`` and ``datasheet_page``; give the
        project side with either ``sheet`` (a schematic sheet) or ``board_region``.
        Either side may be left out. An item with the same title is replaced, so call
        this again after changing the design to refresh the picture.

        Args:
            title: Name of the item, e.g. "3.3 V buck: layout".
            section: Heading the item is grouped under, e.g. "3.3 V supply".
            notes: Plain text shown under the pictures: what matches, what differs, what
                is still open.
            datasheet_part: Part name as stored by ds_add().
            datasheet_page: Page number of the figure, starting at 1.
            datasheet_crop: Region of the page as "left,top,right,bottom" fractions.
            datasheet_caption: Caption; defaults to the part and page.
            sheet: Schematic sheet name to picture ("/" for the root sheet).
            sheet_crop: Region of the sheet as "left,top,right,bottom" fractions.
            board_region: Board area to picture as "x1,y1,x2,y2" in millimetres.
            board_layers: Layers drawn in the board picture.
            proposal_caption: Caption; defaults to the sheet or board region.

        Returns:
            Where the page is, and which pictures were made.
        """
        from . import datasheet as _datasheet
        from .render_support import render_board_png, render_sheet_png

        try:
            folder = _review_dir()
            slug = _slug(title)
            now = int(time.time())
            item: dict[str, Any] = {
                "title": title,
                "section": section,
                "notes": notes,
                "updated": time.strftime("%Y-%m-%d %H:%M"),
            }
            made: list[str] = []
            if datasheet_part and datasheet_page:
                pdf = _datasheet._pdf_for(datasheet_part)
                data = _datasheet._render_png(pdf, datasheet_page, 200, datasheet_crop)
                name = f"img/{slug}-datasheet.png"
                (folder / name).write_bytes(data)
                item["reference"] = {
                    "image": name,
                    "caption": datasheet_caption or f"{datasheet_part}, page {datasheet_page}",
                    "stamp": now,
                }
                made.append("datasheet figure")
            if sheet:
                root = sheet.strip() == "/"
                data = render_sheet_png("" if root else sheet, 250, sheet_crop)
                name = f"img/{slug}-project.png"
                (folder / name).write_bytes(data)
                item["proposal"] = {
                    "image": name,
                    "caption": proposal_caption or f"schematic sheet {sheet}",
                    "stamp": now,
                }
                made.append("schematic picture")
            elif board_region:
                data = render_board_png(board_layers, board_region, 2400)
                name = f"img/{slug}-project.png"
                (folder / name).write_bytes(data)
                item["proposal"] = {
                    "image": name,
                    "caption": proposal_caption or f"board, {board_region} mm",
                    "stamp": now,
                }
                made.append("board picture")
            items = [entry for entry in _load(folder) if entry.get("title") != title]
            items.append(item)
            index = write_page(folder, items)
        except (ValueError, OSError) as exc:
            return f"Review item not added: {exc}"
        where = (
            f"http://127.0.0.1:{_server.server_address[1]}/" if _server is not None else str(index)
        )
        return (
            f"Review item '{title}' saved ({', '.join(made) or 'notes only'}). "
            f"{len(items)} item(s) on the page: {where}"
            + ("" if _server is not None else " (call review_serve() to serve it)")
        )

    @mcp.tool()
    @headless_compatible
    def review_remove(title: str) -> str:
        """Remove one item from the review page by its title."""
        try:
            folder = _review_dir()
        except ValueError as exc:
            return str(exc)
        items = _load(folder)
        kept = [entry for entry in items if entry.get("title") != title]
        if len(kept) == len(items):
            return f"No review item titled '{title}'."
        write_page(folder, kept)
        return f"Removed '{title}'. {len(kept)} item(s) left."
