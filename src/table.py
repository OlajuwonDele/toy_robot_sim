from __future__ import annotations

from dataclasses import dataclass
from src.position import Position

@dataclass(frozen = True)
class Table:
    """Represents the square tabletop surface."""
    width: int = 5
    height: int = 5


    def is_valid_position(self, position: Position) -> bool:
        """Return True if *position* is within table bounds."""
        return 0 <= position.x < self.width and 0 <= position.y < self.height
