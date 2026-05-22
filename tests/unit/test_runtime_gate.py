# ruff: noqa: ANN401
# pyright: reportPrivateUsage=false, reportUnknownLambdaType=false
# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false
"""Unit tests for :mod:`kicad_mcp.ipc.runtime_gate`.

The gate decides whether a schematic mutation goes through the IPC path
(crash-prone on stable KiCad 10.0.x; safe on master/nightly) or the
hardened file-based path. These tests pin the decision matrix down so
that a future refactor cannot quietly re-enable the IPC path on a
release branch that lacks the upstream fix.

We use mocked KiCad clients everywhere — no real IPC, no socket, no
KiCad process required.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from kicad_mcp.ipc import runtime_gate
from kicad_mcp.ipc.runtime_gate import (
    SCH_IPC_OPT_IN_ENV,
    SCH_IPC_PERSISTENCE_HINT,
    _connected_kicad_has_fix,
    _env_opt_in,
    _full_version_has_fix,
    _has_open_schematic,
    _open_schematic_for_ipc,
    build_global_label_proto,
    build_hierarchical_label_proto,
    build_local_label_proto,
    build_wire_proto,
    reset_runtime_gate_cache,
    route_schematic_create,
    should_use_ipc_for_schematic_mutation,
)

# ---------------------------------------------------------------------------
# Scaffolding
# ---------------------------------------------------------------------------


class _FakeVersion:
    """Stand-in for :class:`kipy.kicad.KiCadVersion` exposing ``full_version``."""

    def __init__(self, full_version: str) -> None:
        self.full_version = full_version


class _FakeDoc:
    """Anything truthy works for the "doc list non-empty" check."""

    pass


class _FakeKiCad:
    """Stand-in for :class:`kipy.kicad.KiCad` with the bits the gate uses."""

    def __init__(
        self,
        full_version: str = "10.99.0-1059-g0895df3e3c",
        docs: list[Any] | None = None,
        get_version_exc: BaseException | None = None,
        get_documents_exc: BaseException | None = None,
    ) -> None:
        self._full_version = full_version
        self._docs = list(docs) if docs is not None else [_FakeDoc()]
        self._get_version_exc = get_version_exc
        self._get_documents_exc = get_documents_exc
        self.get_version_calls = 0
        self.get_documents_calls = 0

    def get_version(self) -> _FakeVersion:
        self.get_version_calls += 1
        if self._get_version_exc is not None:
            raise self._get_version_exc
        return _FakeVersion(self._full_version)

    def get_open_documents(self, _doctype: Any) -> list[Any]:
        self.get_documents_calls += 1
        if self._get_documents_exc is not None:
            raise self._get_documents_exc
        return list(self._docs)


@pytest.fixture(autouse=True)
def _reset_cache_each_test() -> None:
    """Each test starts with a clean version-detection cache."""

    reset_runtime_gate_cache()


@pytest.fixture
def fake_kicad() -> _FakeKiCad:
    return _FakeKiCad()


@pytest.fixture
def opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set the opt-in env var to a truthy value."""

    monkeypatch.setenv(SCH_IPC_OPT_IN_ENV, "1")


@pytest.fixture
def opt_out(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure the opt-in env var is unset (the default)."""

    monkeypatch.delenv(SCH_IPC_OPT_IN_ENV, raising=False)


# ---------------------------------------------------------------------------
# _full_version_has_fix — string heuristic
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "full_version",
    [
        "10.99.0-1059-g0895df3e3c",  # master / nightly
        "11.0.0",  # future release
        "11.2.5-7-gabcdef1234",  # future release patched
        "12.0.0-0-g0000000000",  # far-future
        "v10.99.0-1-gdeadbeef00",  # tolerant of leading "v"
        "10.0.0-99-g3dca4e0e38ff",  # explicit hash match
    ],
)
def test_full_version_has_fix_true(full_version: str) -> None:
    assert _full_version_has_fix(full_version) is True


@pytest.mark.parametrize(
    "full_version",
    [
        "",
        "garbage",
        "10.0.1",
        "10.0.3",
        "10.0.3-12-gabcdef1234",  # patched stable, fix uncertain
        "9.99.0",  # major < fixed
        "10.98.0",  # minor < fixed
        "not.a.version-15-ghashy",
    ],
)
def test_full_version_has_fix_false(full_version: str) -> None:
    assert _full_version_has_fix(full_version) is False


# ---------------------------------------------------------------------------
# _env_opt_in
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["1", "true", "yes", "on", "TRUE", " On "])
def test_env_opt_in_truthy(value: str) -> None:
    assert _env_opt_in({SCH_IPC_OPT_IN_ENV: value}) is True


@pytest.mark.parametrize("value", ["", "0", "false", "no", "off", "anything-else"])
def test_env_opt_in_falsy(value: str) -> None:
    assert _env_opt_in({SCH_IPC_OPT_IN_ENV: value}) is False


def test_env_opt_in_missing_key_is_false() -> None:
    assert _env_opt_in({}) is False


def test_env_opt_in_reads_os_environ_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(SCH_IPC_OPT_IN_ENV, "1")
    assert _env_opt_in() is True
    monkeypatch.delenv(SCH_IPC_OPT_IN_ENV)
    assert _env_opt_in() is False


# ---------------------------------------------------------------------------
# _connected_kicad_has_fix
# ---------------------------------------------------------------------------


def test_version_probe_returns_true_for_master() -> None:
    kicad = _FakeKiCad(full_version="10.99.0-1059-g0895df3e3c")
    assert _connected_kicad_has_fix(kicad_factory=lambda: kicad) is True
    assert kicad.get_version_calls == 1


def test_version_probe_returns_false_for_stable() -> None:
    kicad = _FakeKiCad(full_version="10.0.3")
    assert _connected_kicad_has_fix(kicad_factory=lambda: kicad) is False


def test_version_probe_returns_false_on_connect_failure() -> None:
    def boom() -> _FakeKiCad:
        raise RuntimeError("ipc unreachable")

    assert _connected_kicad_has_fix(kicad_factory=boom) is False


def test_version_probe_returns_false_when_get_version_raises() -> None:
    kicad = _FakeKiCad(get_version_exc=RuntimeError("transport reset"))
    assert _connected_kicad_has_fix(kicad_factory=lambda: kicad) is False


def test_version_probe_returns_false_when_full_version_missing() -> None:
    bad = MagicMock()
    bad.get_version.return_value = object()  # no ``full_version`` attribute
    assert _connected_kicad_has_fix(kicad_factory=lambda: bad) is False


def test_version_probe_caches_result_across_calls() -> None:
    kicad = _FakeKiCad(full_version="10.99.0-1-gdeadbeef00")

    first = _connected_kicad_has_fix(kicad_factory=lambda: kicad)
    second = _connected_kicad_has_fix(kicad_factory=lambda: kicad)

    assert first is True
    assert second is True
    # Cache hit means we only touched the IPC once even though the caller
    # asked twice. This is the property the docstring promises.
    assert kicad.get_version_calls == 1


def test_reset_runtime_gate_cache_forces_reprobe() -> None:
    kicad = _FakeKiCad(full_version="10.99.0-1-gdeadbeef00")

    _connected_kicad_has_fix(kicad_factory=lambda: kicad)
    reset_runtime_gate_cache()
    _connected_kicad_has_fix(kicad_factory=lambda: kicad)

    assert kicad.get_version_calls == 2


# ---------------------------------------------------------------------------
# _has_open_schematic
# ---------------------------------------------------------------------------


def test_has_open_schematic_true_when_doc_present(fake_kicad: _FakeKiCad) -> None:
    assert _has_open_schematic(kicad_factory=lambda: fake_kicad) is True


def test_has_open_schematic_false_when_empty() -> None:
    kicad = _FakeKiCad(docs=[])
    assert _has_open_schematic(kicad_factory=lambda: kicad) is False


def test_has_open_schematic_false_on_connect_failure() -> None:
    def boom() -> _FakeKiCad:
        raise RuntimeError("ipc unreachable")

    assert _has_open_schematic(kicad_factory=boom) is False


def test_has_open_schematic_false_when_get_documents_raises() -> None:
    kicad = _FakeKiCad(get_documents_exc=RuntimeError("api error"))
    assert _has_open_schematic(kicad_factory=lambda: kicad) is False


# ---------------------------------------------------------------------------
# should_use_ipc_for_schematic_mutation — the public decision
# ---------------------------------------------------------------------------


def test_decision_false_when_env_opt_in_off(fake_kicad: _FakeKiCad, opt_out: None) -> None:
    assert (
        should_use_ipc_for_schematic_mutation(
            kicad_factory=lambda: fake_kicad,
        )
        is False
    )
    # Version probe should not have been called — env gate short-circuits.
    assert fake_kicad.get_version_calls == 0


def test_decision_false_when_version_too_old(opt_in: None) -> None:
    kicad = _FakeKiCad(full_version="10.0.3")
    assert (
        should_use_ipc_for_schematic_mutation(
            kicad_factory=lambda: kicad,
        )
        is False
    )


def test_decision_false_when_no_open_schematic(opt_in: None) -> None:
    kicad = _FakeKiCad(full_version="10.99.0-1-gdeadbeef00", docs=[])
    assert (
        should_use_ipc_for_schematic_mutation(
            kicad_factory=lambda: kicad,
        )
        is False
    )


def test_decision_true_when_all_gates_pass(opt_in: None, fake_kicad: _FakeKiCad) -> None:
    assert (
        should_use_ipc_for_schematic_mutation(
            kicad_factory=lambda: fake_kicad,
        )
        is True
    )


def test_decision_uses_injected_env_over_os_environ(fake_kicad: _FakeKiCad) -> None:
    # Explicit env wins, even when os.environ has nothing.
    assert (
        should_use_ipc_for_schematic_mutation(
            env={SCH_IPC_OPT_IN_ENV: "1"},
            kicad_factory=lambda: fake_kicad,
        )
        is True
    )


def test_decision_short_circuits_on_connect_failure(opt_in: None) -> None:
    """A broken IPC must NOT take the IPC path."""

    def boom() -> _FakeKiCad:
        raise RuntimeError("connect refused")

    assert (
        should_use_ipc_for_schematic_mutation(
            kicad_factory=boom,
        )
        is False
    )


# ---------------------------------------------------------------------------
# _open_schematic_for_ipc
# ---------------------------------------------------------------------------


def test_open_schematic_for_ipc_returns_schematic(fake_kicad: _FakeKiCad) -> None:
    from kicad_mcp.ipc.schematic import Schematic

    result = _open_schematic_for_ipc(kicad_factory=lambda: fake_kicad)
    assert isinstance(result, Schematic)


def test_open_schematic_for_ipc_raises_when_no_doc() -> None:
    kicad = _FakeKiCad(docs=[])
    with pytest.raises(RuntimeError, match="No schematic document"):
        _open_schematic_for_ipc(kicad_factory=lambda: kicad)


def test_open_schematic_for_ipc_uses_get_kicad_when_factory_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default ``kicad_factory=None`` should fall back to ``connection.get_kicad``."""

    from kicad_mcp.ipc.schematic import Schematic

    fake_kicad = _FakeKiCad()
    monkeypatch.setattr("kicad_mcp.connection.get_kicad", lambda: fake_kicad)
    result = _open_schematic_for_ipc()
    assert isinstance(result, Schematic)
    assert fake_kicad.get_documents_calls == 1


def test_connected_kicad_has_fix_uses_get_kicad_when_factory_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default ``kicad_factory=None`` should fall back to ``connection.get_kicad``."""

    fake_kicad = _FakeKiCad(full_version="10.99.0-1-gdeadbeef00")
    monkeypatch.setattr("kicad_mcp.connection.get_kicad", lambda: fake_kicad)
    assert _connected_kicad_has_fix() is True


def test_has_open_schematic_uses_get_kicad_when_factory_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default ``kicad_factory=None`` should fall back to ``connection.get_kicad``."""

    fake_kicad = _FakeKiCad()
    monkeypatch.setattr("kicad_mcp.connection.get_kicad", lambda: fake_kicad)
    assert _has_open_schematic() is True


# ---------------------------------------------------------------------------
# route_schematic_create — the high-level routing helper
# ---------------------------------------------------------------------------


def test_route_takes_file_path_when_gate_refuses(opt_out: None) -> None:
    file_called: list[bool] = []

    def fallback() -> str:
        file_called.append(True)
        return "file-path-result"

    result = route_schematic_create(
        [build_wire_proto(0.0, 0.0, 2.54, 0.0)],
        fallback,
    )

    assert result == "file-path-result"
    assert file_called == [True]


def test_route_takes_ipc_path_when_gate_permits(
    opt_in: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Build a fake Schematic whose ``create_items`` records the call.
    seen_items: list[list[Any]] = []

    class _FakeSchematic:
        def create_items(self, items: list[Any]) -> list[Any]:
            seen_items.append(list(items))
            return list(items)

    def _fake_open(kicad_factory: Any = None) -> _FakeSchematic:
        return _FakeSchematic()

    monkeypatch.setattr(runtime_gate, "_open_schematic_for_ipc", _fake_open)

    fallback_called: list[bool] = []

    def fallback() -> str:
        fallback_called.append(True)
        return "file-path"

    fake_kicad = _FakeKiCad()
    items = [build_wire_proto(0.0, 0.0, 2.54, 0.0)]
    result = route_schematic_create(
        items,
        fallback,
        kicad_factory=lambda: fake_kicad,
    )

    assert fallback_called == []
    assert isinstance(result, str)
    assert SCH_IPC_PERSISTENCE_HINT in result
    assert "via IPC" in result
    assert seen_items == [items]


def test_route_logs_decision_each_time(opt_out: None) -> None:
    """The gate logs on every call so the user can audit path choice."""

    # Two distinct fallback calls — we just need to confirm no exception.
    out1 = route_schematic_create([], lambda: "a")
    out2 = route_schematic_create([], lambda: "b")
    assert out1 == "a"
    assert out2 == "b"


# ---------------------------------------------------------------------------
# Proto builders
# ---------------------------------------------------------------------------


def test_build_global_label_proto_has_text_and_position() -> None:
    proto = build_global_label_proto(10.0, 20.0, "NET1")
    assert proto.text.text.text == "NET1"
    # 1 mm = 1_000_000 nm; the kipy Vector2 helper uses round-half-to-even.
    assert proto.position.x_nm == 10_000_000
    assert proto.position.y_nm == 20_000_000


def test_build_local_label_proto_has_text_and_position() -> None:
    proto = build_local_label_proto(-1.27, 5.08, "SDA")
    assert proto.text.text.text == "SDA"
    assert proto.position.x_nm == -1_270_000
    assert proto.position.y_nm == 5_080_000


def test_build_hierarchical_label_proto_has_text_and_position() -> None:
    proto = build_hierarchical_label_proto(0.0, 0.0, "CLK")
    assert proto.text.text.text == "CLK"
    assert proto.position.x_nm == 0
    assert proto.position.y_nm == 0


def test_build_wire_proto_has_endpoints() -> None:
    proto = build_wire_proto(0.0, 0.0, 2.54, 5.08)
    assert proto.start.x_nm == 0
    assert proto.start.y_nm == 0
    assert proto.end.x_nm == 2_540_000
    assert proto.end.y_nm == 5_080_000


# ---------------------------------------------------------------------------
# Tool-level wiring — confirm each sch_add_* picks the right path.
#
# These tests touch ``kicad_mcp.tools.schematic`` to verify that the
# four wired tools dispatch through the runtime gate. We mock the IPC
# Schematic so the test never touches a real socket, and we monkeypatch
# the file-path transactional_write so the test stays hermetic.
# ---------------------------------------------------------------------------


@pytest.fixture
def fake_ipc_schematic(monkeypatch: pytest.MonkeyPatch) -> list[list[Any]]:
    """Capture the items passed to a fake Schematic.create_items().

    Returns the captured-items list so individual tests can assert on
    what was sent.
    """

    captured: list[list[Any]] = []

    class _FakeSchematic:
        def create_items(self, items: list[Any]) -> list[Any]:
            captured.append(list(items))
            return list(items)

    monkeypatch.setattr(
        runtime_gate,
        "_open_schematic_for_ipc",
        lambda kicad_factory=None: _FakeSchematic(),
    )
    return captured


def test_tool_sch_add_wire_uses_ipc_when_gate_permits(
    opt_in: None,
    monkeypatch: pytest.MonkeyPatch,
    fake_ipc_schematic: list[list[Any]],
) -> None:
    """sch_add_wire should hit the IPC path when the gate opens."""

    fake_kicad = _FakeKiCad()
    # Both probe helpers call into ``..connection.get_kicad``; patch that
    # global so route_schematic_create's default kicad_factory works.
    monkeypatch.setattr(
        "kicad_mcp.connection.get_kicad",
        lambda: fake_kicad,
    )

    from kicad_mcp.tools import schematic as schematic_tools

    # The file fallback would call transactional_write; if we ever hit
    # it, fail loudly.
    monkeypatch.setattr(
        schematic_tools,
        "transactional_write",
        lambda _mutator: pytest.fail("transactional_write was called; expected IPC path"),
    )

    # Build a tiny FastMCP shim that captures registered tools.
    registered: dict[str, Any] = {}

    class _FakeMCP:
        def tool(self, *_args: Any, **_kwargs: Any) -> Any:
            def deco(fn: Any) -> Any:
                registered[fn.__name__] = fn
                return fn

            return deco

    schematic_tools.register(_FakeMCP())

    result = registered["sch_add_wire"](0.0, 0.0, 2.54, 0.0)
    assert SCH_IPC_PERSISTENCE_HINT in result
    assert len(fake_ipc_schematic) == 1
    assert len(fake_ipc_schematic[0]) == 1  # one Line proto


def test_tool_sch_add_label_uses_file_path_when_gate_refuses(
    opt_out: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """sch_add_label should hit the file path when the env opt-in is off."""

    from kicad_mcp.tools import schematic as schematic_tools

    write_called: list[bool] = []

    def fake_write(_mutator: Any) -> str:
        write_called.append(True)
        return "wrote"

    monkeypatch.setattr(schematic_tools, "transactional_write", fake_write)
    monkeypatch.setattr(schematic_tools, "_reload_schematic", lambda: "reloaded")
    monkeypatch.setattr(
        schematic_tools,
        "_append_before_sheet_instances",
        lambda current, block: current + block,
    )

    registered: dict[str, Any] = {}

    class _FakeMCP:
        def tool(self, *_args: Any, **_kwargs: Any) -> Any:
            def deco(fn: Any) -> Any:
                registered[fn.__name__] = fn
                return fn

            return deco

    schematic_tools.register(_FakeMCP())

    result = registered["sch_add_label"]("NET1", 10.16, 12.7)
    assert write_called == [True]
    assert "reloaded" in result


def test_tool_sch_add_global_label_uses_ipc_when_gate_permits(
    opt_in: None,
    monkeypatch: pytest.MonkeyPatch,
    fake_ipc_schematic: list[list[Any]],
) -> None:
    fake_kicad = _FakeKiCad()
    monkeypatch.setattr("kicad_mcp.connection.get_kicad", lambda: fake_kicad)

    from kicad_mcp.tools import schematic as schematic_tools

    monkeypatch.setattr(
        schematic_tools,
        "transactional_write",
        lambda _mutator: pytest.fail("file path should not run"),
    )

    registered: dict[str, Any] = {}

    class _FakeMCP:
        def tool(self, *_args: Any, **_kwargs: Any) -> Any:
            def deco(fn: Any) -> Any:
                registered[fn.__name__] = fn
                return fn

            return deco

    schematic_tools.register(_FakeMCP())

    result = registered["sch_add_global_label"]("PWR_OK", 25.4, 25.4)
    assert SCH_IPC_PERSISTENCE_HINT in result
    assert len(fake_ipc_schematic) == 1


def test_tool_sch_add_hierarchical_label_uses_ipc_when_gate_permits(
    opt_in: None,
    monkeypatch: pytest.MonkeyPatch,
    fake_ipc_schematic: list[list[Any]],
) -> None:
    fake_kicad = _FakeKiCad()
    monkeypatch.setattr("kicad_mcp.connection.get_kicad", lambda: fake_kicad)

    from kicad_mcp.tools import schematic as schematic_tools

    monkeypatch.setattr(
        schematic_tools,
        "transactional_write",
        lambda _mutator: pytest.fail("file path should not run"),
    )

    registered: dict[str, Any] = {}

    class _FakeMCP:
        def tool(self, *_args: Any, **_kwargs: Any) -> Any:
            def deco(fn: Any) -> Any:
                registered[fn.__name__] = fn
                return fn

            return deco

    schematic_tools.register(_FakeMCP())

    result = registered["sch_add_hierarchical_label"]("CLK_IN", 12.7, 17.78)
    assert SCH_IPC_PERSISTENCE_HINT in result
    assert len(fake_ipc_schematic) == 1


def test_tool_sch_add_local_label_uses_ipc_when_gate_permits(
    opt_in: None,
    monkeypatch: pytest.MonkeyPatch,
    fake_ipc_schematic: list[list[Any]],
) -> None:
    """sch_add_label is the local-label MCP entrypoint."""

    fake_kicad = _FakeKiCad()
    monkeypatch.setattr("kicad_mcp.connection.get_kicad", lambda: fake_kicad)

    from kicad_mcp.tools import schematic as schematic_tools

    monkeypatch.setattr(
        schematic_tools,
        "transactional_write",
        lambda _mutator: pytest.fail("file path should not run"),
    )

    registered: dict[str, Any] = {}

    class _FakeMCP:
        def tool(self, *_args: Any, **_kwargs: Any) -> Any:
            def deco(fn: Any) -> Any:
                registered[fn.__name__] = fn
                return fn

            return deco

    schematic_tools.register(_FakeMCP())

    result = registered["sch_add_label"]("NET_A", 5.08, 5.08)
    assert SCH_IPC_PERSISTENCE_HINT in result
    assert len(fake_ipc_schematic) == 1
