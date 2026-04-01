from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Direction(Enum):
    """Enumerated direction class of North, East, South, West"""

    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"
    
    def _rotate(self, step: int) -> "Direction":
        idx = _CLOCKWISE.index(self)
        return _CLOCKWISE[(idx + step) % 4]

    def turn_left(self) -> "Direction":
        return self._rotate(-1)

    def turn_right(self) -> "Direction":
        return self._rotate(1)

_CLOCKWISE = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)