
from __future__ import annotations

from dataclasses import dataclass
from src.direction import Direction

@dataclass(frozen=True)
class Position:
    """An (x, y) coordinate on the table."""

    x: int
    y: int

    def step(self, direction: Direction) -> "Position":
        """Return the position one unit forward in *direction*."""
        deltas = {
            Direction.NORTH: (0, 1),
            Direction.SOUTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.WEST: (-1, 0),
        }
        dx, dy = deltas[direction]
        return Position(self.x + dx, self.y + dy)