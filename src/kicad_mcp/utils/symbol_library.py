"""Read KiCad symbol libraries in either on-disk layout.

Up to KiCad 10 a library is one ``<name>.kicad_sym`` file holding every symbol.
KiCad 11 ships its stock libraries as ``<name>.kicad_symdir`` folders with one
``<symbol>.kicad_sym`` file per symbol; a derived symbol's parent (``extends``)
then lives in a sibling file. The readers here hide the difference by handing
callers one library text either way.
"""

from __future__ import annotations

import functools
import re
from pathlib import Path

FILE_SUFFIX = ".kicad_sym"
DIR_SUFFIX = ".kicad_symdir"

_FIRST_SYMBOL = re.compile(r'\(symbol\s+"')


def library_path(root: Path, library: str) -> Path | None:
    """Return the file or folder that holds ``library`` under ``root``, if any."""
    as_file = root / f"{library}{FILE_SUFFIX}"
    if as_file.is_file():
        return as_file
    as_dir = root / f"{library}{DIR_SUFFIX}"
    if as_dir.is_dir():
        return as_dir
    return None


def is_library(path: Path) -> bool:
    """True when ``path`` is a symbol library in either layout."""
    if path.is_dir():
        return path.suffix == DIR_SUFFIX
    return path.is_file() and path.suffix == FILE_SUFFIX


def library_names(root: Path) -> list[str]:
    """Names of every symbol library directly under ``root``, sorted."""
    names = {path.stem for path in root.glob(f"*{FILE_SUFFIX}") if path.is_file()}
    names.update(path.stem for path in root.glob(f"*{DIR_SUFFIX}") if path.is_dir())
    return sorted(names)


def symbol_files(path: Path) -> list[Path]:
    """The ``.kicad_sym`` files that make up the library at ``path``."""
    if path.is_dir():
        return sorted(child for child in path.glob(f"*{FILE_SUFFIX}") if child.is_file())
    return [path]


def symbol_blocks_of(text: str) -> str:
    """Strip the ``(kicad_symbol_lib ...)`` wrapper, leaving the symbol blocks."""
    match = _FIRST_SYMBOL.search(text)
    if match is None:
        return ""
    end = text.rstrip().rfind(")")
    return text[match.start() : end].rstrip()


@functools.lru_cache(maxsize=16)
def _merged_dir_text(path: Path, stamp: int) -> str:
    del stamp  # only part of the cache key
    parts = ["(kicad_symbol_lib"]
    for child in symbol_files(path):
        try:
            blocks = symbol_blocks_of(child.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
        if blocks:
            parts.append("\t" + blocks)
    parts.append(")")
    return "\n".join(parts) + "\n"


def read_library_text(path: Path) -> str:
    """Return the whole library at ``path`` as one ``kicad_symbol_lib`` text."""
    if path.is_dir():
        return _merged_dir_text(path, path.stat().st_mtime_ns)
    return path.read_text(encoding="utf-8", errors="ignore")


_EXTENDS = re.compile(r'\(extends\s+"((?:\\.|[^"\\])*)"')
_PIN = re.compile(r"\(pin\s+(\w+)\s+(\w+)\s*\(at\s+(-?[\d.]+)\s+(-?[\d.]+)(?:\s+(-?[\d.]+))?\)")


def symbol_block(library_text: str, name: str) -> str | None:
    """The ``(symbol "name" ...)`` block of a library text, or None."""
    from .sexpr import _extract_block

    match = re.search(r'\(symbol\s+"' + re.escape(name) + r'"', library_text)
    if match is None:
        return None
    block, _ = _extract_block(library_text, match.start())
    return block or None


def base_chain(library_text: str, name: str) -> list[str]:
    """``name`` followed by each symbol it derives from, ending at the base symbol.

    A stock symbol often "extends" another, which may extend a third; only the base
    holds the graphics and pins. Raises ``KeyError`` when a link is missing.
    """
    chain = [name]
    while True:
        block = symbol_block(library_text, chain[-1])
        if block is None:
            raise KeyError(chain[-1])
        parent = _EXTENDS.search(block)
        if parent is None or parent.group(1) in chain:
            return chain
        chain.append(parent.group(1))


def symbol_pins(block: str) -> list[dict[str, object]]:
    """Pins of a base symbol block: number, name, type, position and whether hidden."""
    from .sexpr import _extract_block

    pins: list[dict[str, object]] = []
    for match in _PIN.finditer(block):
        pin_block, _ = _extract_block(block, match.start())
        name = re.search(r'\(name\s+"((?:\\.|[^"\\])*)"', pin_block)
        number = re.search(r'\(number\s+"((?:\\.|[^"\\])*)"', pin_block)
        head = pin_block.split("(name", 1)[0]
        pins.append(
            {
                "number": number.group(1) if number else "",
                "name": name.group(1) if name else "",
                "type": match.group(1),
                "x": float(match.group(3)),
                "y": float(match.group(4)),
                "hidden": "(hide yes)" in head or re.search(r"\bhide\b", head) is not None,
            }
        )

    def order(pin: dict[str, object]) -> tuple[int, int | str]:
        text = str(pin["number"])
        return (0, int(text)) if text.isdigit() else (1, text)

    return sorted(pins, key=order)
