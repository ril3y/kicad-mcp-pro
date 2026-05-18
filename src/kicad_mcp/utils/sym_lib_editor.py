"""Safe structural editor for KiCad ``.kicad_sym`` libraries.

Every prior attempt in this repo to mutate a ``.kicad_sym`` file via
regex (e.g. PR-history attempts to rename pins on
``G2R-2-DC12V``) corrupted the file by miscounting parens inside
``(effects ...)`` blocks or string-literal values like
``"OMRON(欧姆龙)"``. This module wraps ``sexpdata`` (a real
S-expression parser) so edits operate on the tree, not the bytes,
and guarantees the result still loads in KiCad by running
``kicad-cli sym upgrade --force`` against the serialized output
before letting the caller persist it.
"""

from __future__ import annotations

import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import sexpdata  # type: ignore[import-untyped]
from sexpdata import Symbol


def _is_token(node: Any, name: str) -> bool:  # noqa: ANN401 — s-expr nodes are heterogeneous
    """Return True if ``node`` is the bare s-expression token ``name``."""
    return isinstance(node, Symbol) and node.value() == name


def load_sym_lib(path: Path) -> list[Any]:
    """Parse a ``.kicad_sym`` library file into a nested-list tree.

    Raises ``FileNotFoundError`` if the path doesn't exist and
    ``ValueError`` if the file is not a recognisable ``kicad_symbol_lib``
    document. Strings inside the tree keep their original Python ``str``
    type; bare tokens become ``sexpdata.Symbol`` instances. Both must be
    handled when walking the tree.
    """
    if not path.exists():
        raise FileNotFoundError(f"Symbol library not found: {path}")
    text = path.read_text(encoding="utf-8")
    tree = sexpdata.loads(text)
    if not (isinstance(tree, list) and tree and _is_token(tree[0], "kicad_symbol_lib")):
        raise ValueError(
            f"{path} does not look like a kicad_symbol_lib — first element "
            f"is {tree[0] if isinstance(tree, list) and tree else tree!r}"
        )
    return tree


def dump_sym_lib(tree: list[Any]) -> str:
    """Serialize a tree back to ``.kicad_sym`` text.

    ``sexpdata`` produces single-line output which is more compact than
    KiCad's canonical formatting. KiCad's parser is whitespace-agnostic
    so the file still loads correctly; when KiCad next saves it through
    eeschema or the Symbol Editor it'll re-canonicalize the layout.
    """
    # sexpdata isn't typed; mypy sees `dumps` as returning Any. The actual
    # return is a str — coerce explicitly so callers see a concrete type.
    return str(sexpdata.dumps(tree))


def iter_top_level_symbols(tree: list[Any]) -> Iterator[list[Any]]:
    """Yield each top-level ``(symbol "name" ...)`` block under
    ``kicad_symbol_lib``. Skips the leading ``kicad_symbol_lib`` token
    and any ``(version ...)`` / ``(generator ...)`` metadata children
    that aren't symbol blocks."""
    for child in tree[1:]:
        if isinstance(child, list) and len(child) >= 2 and _is_token(child[0], "symbol"):
            yield child


def find_symbol(tree: list[Any], symbol_name: str) -> list[Any] | None:
    """Find a top-level ``(symbol "<name>" ...)`` block by name. Returns
    the subtree (a Python list) or ``None`` if no match. Match is
    case-sensitive — that matches KiCad's own library-id resolution."""
    for sym in iter_top_level_symbols(tree):
        if sym[1] == symbol_name:
            return sym
    return None


def iter_pins(symbol_node: list[Any]) -> Iterator[list[Any]]:
    """Yield every ``(pin ...)`` block inside a symbol subtree.

    Pins normally live one level deeper than the top-level symbol
    (inside a sub-symbol named like ``Foo_0_1``), so this walks the
    whole subtree rather than just the top-level children.
    """

    def _walk(node: Any) -> Iterator[list[Any]]:  # noqa: ANN401
        if isinstance(node, list):
            if node and _is_token(node[0], "pin"):
                yield node
            else:
                for child in node:
                    yield from _walk(child)

    yield from _walk(symbol_node)


def find_pin(symbol_node: list[Any], pin_number: str) -> list[Any] | None:
    """Return the ``(pin ...)`` block whose ``(number "<n>" ...)`` child
    matches ``pin_number``, or ``None`` if no pin has that number."""
    target = str(pin_number)
    for pin in iter_pins(symbol_node):
        for child in pin:
            if (
                isinstance(child, list)
                and len(child) >= 2
                and _is_token(child[0], "number")
                and str(child[1]) == target
            ):
                return pin
    return None


def set_pin_name(pin_node: list[Any], new_name: str) -> bool:
    """Rewrite the ``(name "..." ...)`` child of a pin block. Returns
    True if the name was changed (or wasn't there and one was added),
    False if no change was made (e.g. the new name matched the old)."""
    for child in pin_node:
        if isinstance(child, list) and len(child) >= 2 and _is_token(child[0], "name"):
            if str(child[1]) == new_name:
                return False
            child[1] = new_name
            return True
    # No (name ...) child existed; append one. Place it before the
    # (number ...) child for consistency with how KiCad's own writer
    # orders these.
    new_child: list[Any] = [Symbol("name"), new_name]
    for index, child in enumerate(pin_node):
        if isinstance(child, list) and len(child) >= 2 and _is_token(child[0], "number"):
            pin_node.insert(index, new_child)
            return True
    pin_node.append(new_child)
    return True


def set_pin_type(pin_node: list[Any], new_type: str) -> bool:
    """Rewrite the pin electrical type. In ``(pin TYPE SHAPE ...)`` the
    type is the second element (after the ``pin`` token). KiCad's valid
    types include ``passive``, ``input``, ``output``, ``bidirectional``,
    ``tri_state``, ``power_in``, ``power_out``, ``open_collector``,
    ``open_emitter``, ``unspecified``, ``no_connect``, ``free``."""
    if len(pin_node) < 2:
        return False
    existing = pin_node[1]
    target = Symbol(new_type)
    if isinstance(existing, Symbol) and existing.value() == new_type:
        return False
    pin_node[1] = target
    return True


def validate_via_kicad_cli(
    text: str,
    kicad_cli: Path,
    *,
    timeout: int = 30,
) -> tuple[bool, str]:
    """Write ``text`` to a tempfile and run ``kicad-cli sym upgrade
    --force`` against it. Returns ``(ok, message)``. ``message`` is the
    CLI's combined stdout+stderr — useful when ``ok`` is False so the
    caller can surface the parse error to the user."""
    if not kicad_cli.exists():
        return False, f"kicad-cli not found at {kicad_cli}"
    with tempfile.NamedTemporaryFile(
        suffix=".kicad_sym",
        mode="w",
        encoding="utf-8",
        delete=False,
    ) as src_handle:
        src_handle.write(text)
        src_path = Path(src_handle.name)
    out_path = src_path.with_suffix(".validated.kicad_sym")
    try:
        result = subprocess.run(
            [
                str(kicad_cli),
                "sym",
                "upgrade",
                "--force",
                "-o",
                str(out_path),
                str(src_path),
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"{type(exc).__name__}: {exc}"
    finally:
        src_path.unlink(missing_ok=True)
        out_path.unlink(missing_ok=True)
    if result.returncode == 0:
        return True, (result.stdout + result.stderr).strip()
    return False, (result.stderr or result.stdout or "kicad-cli failed").strip()
