from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from src.position import Position
from src.direction import Direction
@dataclass(frozen=True)
class Robot:
    """Represents the robot's current state (position + facing direction)."""

    position: Position
    facing: Direction

    def move(self) -> "Robot":
        """Return a new Robot stepped one unit forward (caller must validate)."""
        return Robot(self.position.step(self.facing), self.facing)

    def turn_left(self) -> "Robot":
        """Return a new Robot rotated 90° counter-clockwise."""
        return Robot(self.position, self.facing.turn_left())

    def turn_right(self) -> "Robot":
        """Return a new Robot rotated 90° clockwise."""
        return Robot(self.position, self.facing.turn_right())

    def report(self) -> str:
        """Return a human-readable state string."""
        return f"{self.position.x},{self.position.y},{self.facing.value}"