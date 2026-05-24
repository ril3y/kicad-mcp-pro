"""Vendored KiCad master proto stubs.

Regenerated from `X:/Projects/kicad-source/api/proto/` against the
KiCad master branch (commit 0895df3e3c) on 2026-05-22, with the proto
file paths re-rooted under ``mp/`` to avoid colliding with kipy's
older proto descriptors in the global protobuf descriptor pool.

Field shape mismatches with kipy 0.7.1:
* master: ``GlobalLabel.text -> base_types.Text`` (two-deep, text
  string at ``label.text.text``)
* kipy 0.7.1: ``GlobalLabel.text -> schematic_types.Text ->
  base_types.Text`` (three-deep, text string at
  ``label.text.text.text``)

The .proto files in `kicad-source/api/proto/` use simple imports like
``import "common/types/base_types.proto"`` which collide with kipy.
For our vendoring pass we prepend ``mp/`` to every internal import so
the resulting descriptor pool entries are ``mp/common/types/...`` —
no collision with kipy's ``common/types/...``.

This module side-effects sys.path: it inserts THIS directory so the
generated stubs' bare imports (``from mp.common.types import ...``)
resolve. This is the canonical way to vendor protoc output without
rewriting every generated .py.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
