"""Plan where one connection goes before KiCad's router draws it.

KiCad's interactive router lays one rule-clean track on the layer it is given. It
does not choose a layer, find a via site or decide which way round a part to go.
This module does that part: a shortest-path search over grids that say, per layer
and cell, whether a track centred there is allowed (KiCad computes the grids with
its own rule engine, see ``ipc.route.clearance_map``).

The result is a short list of waypoints joined by straight pieces at 0, 45 or 90
degrees, with the layer changes marked; the router then draws each piece.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field

Cell = tuple[int, int, int]  # (layer index, column, row)

_MOVES = (
    (1, 0, 1.0),
    (-1, 0, 1.0),
    (0, 1, 1.0),
    (0, -1, 1.0),
    (1, 1, 1.41421356),
    (1, -1, 1.41421356),
    (-1, 1, 1.41421356),
    (-1, -1, 1.41421356),
)


@dataclass
class Grid:
    """Where a track of one net may go, per layer, as KiCad's rules see it."""

    columns: int
    rows: int
    blocked: list[bytes]  # per layer, one byte per cell, row by row; 1 = not allowed
    via_blocked: bytes = b""  # same layout; empty = no vias anywhere
    hard_blocked: list[bytes] | None = None  # the same with other nets' tracks ignored
    layer_cost: list[float] = field(default_factory=list)  # 0 = layer not to be used
    penalty: list[float] | None = None  # extra cost per cell, all layers

    def index(self, column: int, row: int) -> int:
        return row * self.columns + column

    def inside(self, column: int, row: int) -> bool:
        return 0 <= column < self.columns and 0 <= row < self.rows


@dataclass
class Plan:
    """A planned path: its cells, and the cells where it crosses other nets' tracks."""

    cells: list[Cell]
    through_tracks: list[Cell]


def find_path(
    grid: Grid,
    start: Cell,
    goal: Cell,
    *,
    via_cost: float = 30.0,
    rip_up_cost: float = 0.0,
    max_expansions: int = 1_500_000,
) -> Plan | None:
    """Cheapest path from ``start`` to ``goal`` over the grid, or None.

    A step costs its length in cells times the layer's cost. A layer change costs
    ``via_cost`` cells and needs a free via site. With ``rip_up_cost`` above zero
    the path may also cross cells that only other nets' tracks block, at that
    extra cost per cell; they are returned in ``Plan.through_tracks``.
    """
    layers = len(grid.blocked)
    costs = grid.layer_cost or [1.0] * layers
    usable = [cost for cost in costs if cost > 0]
    if not usable or costs[start[0]] <= 0 or costs[goal[0]] <= 0:
        return None
    cheapest = min(usable)
    columns = grid.columns
    size = columns * grid.rows
    free_cells = {start, goal}

    def step_cost(layer: int, cell: int, here: Cell) -> float | None:
        """Extra cost of entering a cell, or None when it cannot be entered."""
        if here in free_cells or not grid.blocked[layer][cell]:
            return 0.0
        if rip_up_cost > 0 and grid.hard_blocked is not None and not grid.hard_blocked[layer][cell]:
            return rip_up_cost
        return None

    goal_layer, goal_column, goal_row = goal

    def estimate(column: int, row: int) -> float:
        dx, dy = abs(column - goal_column), abs(row - goal_row)
        return cheapest * (max(dx, dy) + 0.41421356 * min(dx, dy))

    start_key = start[0] * size + grid.index(start[1], start[2])
    goal_key = goal_layer * size + grid.index(goal_column, goal_row)
    best: dict[int, float] = {start_key: 0.0}
    came: dict[int, int] = {}
    queue: list[tuple[float, float, int]] = [(estimate(start[1], start[2]), 0.0, start_key)]
    expansions = 0
    while queue:
        _, cost_here, key = heapq.heappop(queue)
        if key == goal_key:
            break
        if cost_here > best.get(key, float("inf")):
            continue
        expansions += 1
        if expansions > max_expansions:
            return None
        layer, cell = divmod(key, size)
        row, column = divmod(cell, columns)
        weight = costs[layer]
        for dc, dr, length in _MOVES:
            next_column, next_row = column + dc, row + dr
            if not grid.inside(next_column, next_row):
                continue
            next_cell = next_row * columns + next_column
            extra = step_cost(layer, next_cell, (layer, next_column, next_row))
            if extra is None:
                continue
            total = cost_here + length * weight + extra
            if grid.penalty is not None:
                total += grid.penalty[next_cell]
            next_key = layer * size + next_cell
            if total < best.get(next_key, float("inf")):
                best[next_key] = total
                came[next_key] = key
                heapq.heappush(queue, (total + estimate(next_column, next_row), total, next_key))
        if grid.via_blocked and not grid.via_blocked[cell]:
            for other in range(layers):
                if other == layer or costs[other] <= 0:
                    continue
                if step_cost(other, cell, (other, column, row)) != 0.0:
                    continue
                total = cost_here + via_cost
                next_key = other * size + cell
                if total < best.get(next_key, float("inf")):
                    best[next_key] = total
                    came[next_key] = key
                    heapq.heappush(queue, (total + estimate(column, row), total, next_key))
    else:
        return None
    if goal_key not in best:
        return None

    cells: list[Cell] = []
    key = goal_key
    while True:
        layer, cell = divmod(key, size)
        row, column = divmod(cell, columns)
        cells.append((layer, column, row))
        if key == start_key:
            break
        key = came[key]
    cells.reverse()
    through = [
        here
        for here in cells
        if here not in free_cells and grid.blocked[here[0]][grid.index(here[1], here[2])]
    ]
    return Plan(cells=cells, through_tracks=through)


def _line(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]] | None:
    """Cells of the straight piece from a to b, or None unless it is at 0, 45 or 90 degrees."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx and dy and abs(dx) != abs(dy):
        return None
    steps = max(abs(dx), abs(dy))
    sx = (dx > 0) - (dx < 0)
    sy = (dy > 0) - (dy < 0)
    return [(a[0] + sx * step, a[1] + sy * step) for step in range(steps + 1)]


def _corners(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:
    """Corner points of the two one-bend ways from a to b (diagonal first, straight first)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    diagonal = min(abs(dx), abs(dy))
    sx = (dx > 0) - (dx < 0)
    sy = (dy > 0) - (dy < 0)
    first = (a[0] + sx * diagonal, a[1] + sy * diagonal)
    second = (b[0] - sx * diagonal, b[1] - sy * diagonal)
    return [first, second] if first != second else [first]


def simplify(grid: Grid, plan: Plan) -> list[Cell]:
    """Reduce a planned path to its corner points.

    Consecutive points of the result are joined by straight pieces at 0, 45 or 90
    degrees that stay on cells the plan may use, so the router can draw each
    piece as it stands. A layer change shows as two points on the same cell.
    """
    allowed = set(plan.through_tracks) | {plan.cells[0], plan.cells[-1]}

    def clear(layer: int, a: tuple[int, int], b: tuple[int, int]) -> bool:
        cells = _line(a, b)
        if cells is None:
            return False
        blocked = grid.blocked[layer]
        return all(
            not blocked[grid.index(column, row)] or (layer, column, row) in allowed
            for column, row in cells
        )

    result: list[Cell] = []
    start = 0
    while start < len(plan.cells):
        layer = plan.cells[start][0]
        end = start
        while end + 1 < len(plan.cells) and plan.cells[end + 1][0] == layer:
            end += 1
        run = [(column, row) for _, column, row in plan.cells[start : end + 1]]
        points = [run[0]]
        at = 0
        while at < len(run) - 1:
            for target in range(len(run) - 1, at, -1):
                for corner in _corners(run[at], run[target]):
                    if clear(layer, run[at], corner) and clear(layer, corner, run[target]):
                        if corner not in (run[at], run[target]):
                            points.append(corner)
                        points.append(run[target])
                        at = target
                        break
                else:
                    continue
                break
            else:  # neighbouring cells always join; kept for safety
                points.append(run[at + 1])
                at += 1
        result.extend((layer, column, row) for column, row in points)
        start = end + 1
    return result


def circle_penalty(
    grid: Grid,
    circles: list[tuple[float, float, float, float]],
) -> list[float]:
    """Per-cell extra cost for keep-away areas given in cells: (column, row, radius, cost).

    The cost is highest at the centre and falls to zero at the radius.
    """
    penalty = [0.0] * (grid.columns * grid.rows)
    for centre_column, centre_row, radius, cost in circles:
        if radius <= 0 or cost <= 0:
            continue
        reach = int(radius) + 1
        for row in range(
            max(0, int(centre_row) - reach), min(grid.rows, int(centre_row) + reach + 1)
        ):
            for column in range(
                max(0, int(centre_column) - reach),
                min(grid.columns, int(centre_column) + reach + 1),
            ):
                distance = ((column - centre_column) ** 2 + (row - centre_row) ** 2) ** 0.5
                if distance < radius:
                    penalty[grid.index(column, row)] += cost * (1 - distance / radius)
    return penalty
