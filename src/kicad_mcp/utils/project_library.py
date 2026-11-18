"""Project-local symbol and footprint libraries.

Parts that the stock libraries lack are kept inside the project, in ``<project>/libs``,
and listed in the project's ``sym-lib-table`` / ``fp-lib-table`` so that KiCad itself
(and therefore the IPC placement commands) can find them by ``library:name``.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

from .sexpr import _extract_block, _sexpr_string
from .symbol_library import symbol_blocks_of

LIBS_DIRNAME = "libs"
_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_.+-]+$")
_SYMBOL_LIB_HEADER = '(kicad_symbol_lib\n\t(version 20250316)\n\t(generator "kicad-mcp-pro")\n)\n'

LibraryKind = Literal["symbol", "footprint"]
_TABLE = {
    "symbol": ("sym-lib-table", "sym_lib_table"),
    "footprint": ("fp-lib-table", "fp_lib_table"),
}


def check_library_name(name: str) -> str:
    """Return ``name`` if it is safe as a library name and file name, else raise."""
    if not _NAME_PATTERN.match(name):
        raise ValueError(
            f"Invalid library name {name!r}. Use letters, digits and . _ + - (no spaces)."
        )
    return name


def register_library(project_dir: Path, kind: LibraryKind, name: str, uri: str) -> bool:
    """List ``name`` in the project library table. Returns False if already listed."""
    filename, root = _TABLE[kind]
    table = project_dir / filename
    if table.exists():
        text = table.read_text(encoding="utf-8", errors="ignore")
    else:
        text = f"({root}\n\t(version 7)\n)\n"
    if re.search(rf'\(name\s+"?{re.escape(name)}"?\s*\)', text):
        return False
    entry = (
        f'\t(lib (name {_sexpr_string(name)}) (type "KiCad") (uri {_sexpr_string(uri)})'
        ' (options "") (descr "Project library"))\n'
    )
    end = text.rstrip().rfind(")")
    table.write_text(text[:end].rstrip() + "\n" + entry + ")\n", encoding="utf-8")
    return True


def symbol_library_file(project_dir: Path, library: str) -> Path:
    """Path of the project symbol library ``library`` (it may not exist yet)."""
    return project_dir / LIBS_DIRNAME / f"{check_library_name(library)}.kicad_sym"


def footprint_library_dir(project_dir: Path, library: str) -> Path:
    """Path of the project footprint library ``library`` (it may not exist yet)."""
    return project_dir / LIBS_DIRNAME / f"{check_library_name(library)}.pretty"


def add_symbol_block(project_dir: Path, library: str, name: str, block: str) -> Path:
    """Put one ``(symbol "name" ...)`` block into project library ``library``.

    An older symbol of the same name is replaced. The library is created and listed
    in ``sym-lib-table`` when needed.
    """
    if not block.lstrip().startswith(f"(symbol {_sexpr_string(name)}"):
        raise ValueError(f"The symbol block does not define {name!r}.")
    lib_file = symbol_library_file(project_dir, library)
    lib_file.parent.mkdir(parents=True, exist_ok=True)
    if lib_file.exists():
        text = lib_file.read_text(encoding="utf-8", errors="ignore")
    else:
        text = _SYMBOL_LIB_HEADER

    start = text.find(f"(symbol {_sexpr_string(name)}")
    if start != -1:
        old_block, _ = _extract_block(text, start)
        if old_block:
            text = text[:start].rstrip() + "\n" + text[start + len(old_block) :].lstrip("\n")

    end = text.rstrip().rfind(")")
    lib_file.write_text(text[:end].rstrip() + "\n\t" + block.strip() + "\n)\n", encoding="utf-8")
    register_library(
        project_dir, "symbol", library, f"${{KIPRJMOD}}/{LIBS_DIRNAME}/{library}.kicad_sym"
    )
    return lib_file


def add_symbol(project_dir: Path, library: str, name: str, generated_library_text: str) -> Path:
    """Put the symbol ``name`` into project library ``library``, replacing an older copy.

    ``generated_library_text`` is a complete one-symbol ``kicad_symbol_lib`` text; only
    its symbol block is kept.
    """
    block = symbol_blocks_of(generated_library_text)
    if not block:
        raise ValueError("The generated text holds no symbol.")
    return add_symbol_block(project_dir, library, name, block)


_HIDDEN_FIELD = "(at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes))"


def set_symbol_fields(block: str, fields: dict[str, str]) -> str:
    """Set properties on a library symbol block, adding the ones it lacks (hidden)."""
    for field, value in fields.items():
        pattern = re.compile(
            r"(\(property\s+" + re.escape(_sexpr_string(field)) + r'\s+)"(?:\\.|[^"\\])*"'
        )
        quoted = _sexpr_string(value)
        if pattern.search(block):
            block = pattern.sub(lambda match, q=quoted: match.group(1) + q, block, count=1)
            continue
        # Insert after the last top-level property of the symbol.
        last = None
        for match in re.finditer(r'\n(\s*)\(property\s+"', block):
            sub_symbol = block.find('(symbol "', 1)
            if sub_symbol != -1 and match.start() > sub_symbol:
                break
            last = match
        entry = f"(property {_sexpr_string(field)} {quoted} {_HIDDEN_FIELD})"
        if last is None:
            head_end = block.index("\n") if "\n" in block else len(block)
            block = block[:head_end] + "\n\t\t" + entry + block[head_end:]
            continue
        prop_start = last.start() + 1 + len(last.group(1))
        prop_block, _ = _extract_block(block, prop_start)
        insert_at = prop_start + len(prop_block)
        block = block[:insert_at] + "\n" + last.group(1) + entry + block[insert_at:]
    return block


def derive_symbol_block(base_block: str, base_name: str, new_name: str) -> str:
    """Copy a library symbol block under a new name (its unit sub-symbols follow)."""
    if not _NAME_PATTERN.match(new_name):
        raise ValueError(
            f"Invalid symbol name {new_name!r}. Use letters, digits and . _ + - (no spaces)."
        )
    if re.search(r"\(extends\s", base_block):
        raise ValueError(
            f"{base_name!r} is derived from another symbol; derive from its parent instead."
        )
    block = base_block.replace(
        f"(symbol {_sexpr_string(base_name)}", f"(symbol {_sexpr_string(new_name)}", 1
    )
    return re.sub(
        r'\(symbol "' + re.escape(base_name) + r'_(\d+_\d+)"',
        lambda match: f'(symbol "{new_name}_{match.group(1)}"',
        block,
    )


def add_footprint(project_dir: Path, library: str, name: str, footprint_text: str) -> Path:
    """Write footprint ``name`` into project library ``library`` and list the library."""
    if not _NAME_PATTERN.match(name):
        raise ValueError(
            f"Invalid footprint name {name!r}. Use letters, digits and . _ + - (no spaces)."
        )
    lib_dir = footprint_library_dir(project_dir, library)
    lib_dir.mkdir(parents=True, exist_ok=True)
    fp_file = lib_dir / f"{name}.kicad_mod"
    fp_file.write_text(footprint_text.rstrip() + "\n", encoding="utf-8")
    register_library(
        project_dir, "footprint", library, f"${{KIPRJMOD}}/{LIBS_DIRNAME}/{library}.pretty"
    )
    return fp_file
