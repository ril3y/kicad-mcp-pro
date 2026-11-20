"""The connection planner: around, through (a via) and under, on clearance grids."""

from __future__ import annotations

from kicad_mcp.utils import route_planner
from kicad_mcp.utils.route_planner import Grid


def _layer(rows: list[str]) -> bytes:
    return bytes(1 if char == "#" else 0 for row in rows for char in row)


def _straight_pieces(points: list[tuple[int, int, int]]) -> bool:
    for (la, ca, ra), (lb, cb, rb) in zip(points, points[1:], strict=False):
        if la != lb:
            if (ca, ra) != (cb, rb):
                return False
            continue
        dx, dy = abs(cb - ca), abs(rb - ra)
        if dx and dy and dx != dy:
            return False
    return True


def test_goes_around_an_obstacle_on_one_layer() -> None:
    top = _layer(
        [
            "..........",
            "....#.....",
            "....#.....",
            "....#.....",
            "..........",
        ]
    )
    grid = Grid(columns=10, rows=5, blocked=[top])

    plan = route_planner.find_path(grid, (0, 1, 2), (0, 8, 2))

    assert plan is not None and plan.through_tracks == []
    assert all(not top[grid.index(c, r)] for _, c, r in plan.cells)
    points = route_planner.simplify(grid, plan)
    assert points[0] == (0, 1, 2) and points[-1] == (0, 8, 2)
    assert 2 < len(points) <= 6 and _straight_pieces(points)


def test_uses_a_via_to_pass_under_a_wall() -> None:
    wall = _layer(["....#....."] * 5)
    empty = _layer([".........."] * 5)
    vias = _layer(["#........#"] * 5)  # no via room at the two edges
    grid = Grid(columns=10, rows=5, blocked=[wall, empty], via_blocked=vias, layer_cost=[1, 1.2])

    plan = route_planner.find_path(grid, (0, 1, 2), (0, 8, 2), via_cost=5)

    assert plan is not None
    layers = [layer for layer, _, _ in plan.cells]
    assert layers[0] == 0 and layers[-1] == 0 and 1 in layers
    changes = [(a, b) for a, b in zip(plan.cells, plan.cells[1:], strict=False) if a[0] != b[0]]
    assert len(changes) == 2
    assert all(a[1:] == b[1:] and not vias[grid.index(a[1], a[2])] for a, b in changes)
    assert _straight_pieces(route_planner.simplify(grid, plan))


def test_no_path_without_a_via_site_and_a_forbidden_layer_is_not_used() -> None:
    wall = _layer(["....#....."] * 5)
    empty = _layer([".........."] * 5)
    no_vias = _layer(["##########"] * 5)
    free_vias = _layer([".........."] * 5)

    assert (
        route_planner.find_path(
            Grid(columns=10, rows=5, blocked=[wall, empty], via_blocked=no_vias),
            (0, 1, 2),
            (0, 8, 2),
        )
        is None
    )
    assert (
        route_planner.find_path(
            Grid(
                columns=10, rows=5, blocked=[wall, empty], via_blocked=free_vias, layer_cost=[1, 0]
            ),
            (0, 1, 2),
            (0, 8, 2),
        )
        is None
    )


def test_crosses_another_nets_track_only_when_rip_up_is_allowed() -> None:
    track = _layer(["....#....."] * 5)  # blocked by a track of another net
    pads_only = _layer([".........."] * 5)
    grid = Grid(columns=10, rows=5, blocked=[track], hard_blocked=[pads_only])

    assert route_planner.find_path(grid, (0, 1, 2), (0, 8, 2)) is None
    plan = route_planner.find_path(grid, (0, 1, 2), (0, 8, 2), rip_up_cost=20)

    assert plan is not None and plan.through_tracks == [(0, 4, 2)]
    assert route_planner.simplify(grid, plan) == [(0, 1, 2), (0, 8, 2)]


def test_keep_away_area_bends_the_path() -> None:
    empty = _layer(["..........."] * 9)
    grid = Grid(columns=11, rows=9, blocked=[empty])
    straight = route_planner.find_path(grid, (0, 0, 4), (0, 10, 4))
    grid.penalty = route_planner.circle_penalty(grid, [(5, 4, 3, 50)])
    bent = route_planner.find_path(grid, (0, 0, 4), (0, 10, 4))

    assert straight is not None and all(row == 4 for _, _, row in straight.cells)
    assert bent is not None and (0, 5, 4) not in bent.cells


def test_route_tools_are_registered() -> None:
    """pcb_route_connection, pcb_route_open and pcb_route_map are on the server."""
    import asyncio

    from kicad_mcp.server import build_server

    names = {tool.name for tool in asyncio.run(build_server("full").list_tools())}
    assert {
        "pcb_route_connection",
        "pcb_route_open",
        "pcb_route_map",
        "pcb_route_track",
        "pcb_fanout_plane_nets",
        "pcb_escape_pins",
    } <= names


def test_nearest_site_finds_the_closest_acceptable_cell_around_obstacles() -> None:
    top = _layer(
        [
            "......",
            ".##...",
            ".#....",
            "......",
        ]
    )
    grid = Grid(columns=6, rows=4, blocked=[top])
    path = route_planner.nearest_site(
        grid, (2, 2), lambda column, row: (column, row) == (0, 0), max_steps=10
    )
    assert path is not None and path[0] == (2, 2) and path[-1] == (0, 0)
    assert all(not top[grid.index(c, r)] for c, r in path)
    assert route_planner.nearest_site(grid, (2, 2), lambda c, r: False, max_steps=10) is None


def test_match_net_rule_takes_the_first_matching_pattern() -> None:
    rules = {
        "/LED Driver/SW*": {"min_width_mm": 0.8, "no_vias": True},
        "/LED Driver/*": {"min_width_mm": 0.3},
    }
    assert route_planner.match_net_rule("/LED Driver/SW1", rules)["no_vias"] is True
    assert route_planner.match_net_rule("/LED Driver/ISP1", rules) == {"min_width_mm": 0.3}
    assert route_planner.match_net_rule("GND", rules) == {}
    assert route_planner.match_net_rule("GND", None) == {}


def test_route_connection_applies_width_layers_and_no_vias(monkeypatch) -> None:  # noqa: ANN001
    """pcb_route_connection: a net rule sets the width, the layers, and forbids narrowing."""
    import asyncio

    from kicad_mcp.ipc import route
    from kicad_mcp.server import build_server
    from kicad_mcp.tools import pcb

    calls: list[dict] = []

    def fake_plan(net, first, last, **kwargs):  # noqa: ANN001, ANN003, ANN202
        calls.append({"net": net, **kwargs})
        return {"ok": False, "reason": "blocked", "width": kwargs["width_mm"]}

    class Board:
        def get_nets(self):  # noqa: ANN202
            return []

    monkeypatch.setattr(route, "plan_connection", fake_plan)
    monkeypatch.setattr(pcb, "get_board", lambda: Board())
    server = build_server("full")
    rules = {"/SW": {"min_width_mm": 0.8, "no_vias": True}}

    async def call(arguments: dict) -> str:
        result = await server.call_tool("pcb_route_connection", arguments)
        content = result[0] if isinstance(result, tuple) else result
        return " ".join(getattr(item, "text", "") for item in content)

    text = asyncio.run(
        call({"start": "1,1", "end": "5,1", "net": "/SW", "net_rules": rules,
              "layer_costs": {"F_Cu": 1, "B_Cu": 1}})
    )  # fmt: skip
    assert "blocked" in text
    assert len(calls) == 1  # no second try at 0.2 mm
    assert calls[0]["width_mm"] == 0.8 and calls[0]["layer_costs"] == {"F_Cu": 1.0}

    text = asyncio.run(
        call({"start": "1,1", "end": "5,1", "net": "/SW", "net_rules": rules,
              "start_layer": "F_Cu", "end_layer": "B_Cu"})
    )  # fmt: skip
    assert "may not use vias" in text and len(calls) == 1
