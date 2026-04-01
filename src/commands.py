from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from src.direction import Direction
from src.position import Position


@dataclass(frozen=True)
class PlaceCommand:
    position: Position
    facing: Direction


@dataclass(frozen=True)
class MoveCommand:
    ""
    pass


@dataclass(frozen=True)
class LeftCommand:
    pass


@dataclass(frozen=True)
class RightCommand:
    pass


@dataclass(frozen=True)
class ReportCommand:
    pass


@dataclass(frozen=True)
class InvalidCommand:
    """Represents an unrecognised or erroneous command line."""

    input_text: str
    error: str


Command = Union[
    PlaceCommand,
    MoveCommand,
    LeftCommand,
    RightCommand,
    ReportCommand,
    InvalidCommand,
]

def parse_command(line: str) -> Command:
    """
    Parse a single text line into a Command.

    Parameters
    ----------
    line:
        input_text input line (leading/trailing whitespace is stripped; the
        comparison is case-insensitive).

    Returns
    -------
    Command
        A typed command object, or ``InvalidCommand`` if the line cannot
        be parsed.
    """
    original_input = line
    line = line.split('#')[0].strip()
    
    if not line:
        return InvalidCommand(input_text=line, error="Empty or comment line")

    upper = line.upper()

    if upper == "MOVE":
        return MoveCommand()
    if upper == "LEFT":
        return LeftCommand()
    if upper == "RIGHT":
        return RightCommand()
    if upper == "REPORT":
        return ReportCommand()
    if upper.startswith("PLACE"):
        return _parse_place(original_input, line)

    return InvalidCommand(input_text=original_input, error=f"Unknown command: '{line}'")


def _parse_place(original_input: str, line: str) -> Command:
    """Parse a PLACE X,Y,F line."""
    parts = line.split(None, 1) 
    if len(parts) != 2:
        return InvalidCommand(input_text=original_input, error="PLACE requires X,Y,F arguments")

    args = parts[1].split(",")
    if len(args) != 3:
        return InvalidCommand(
            input_text=original_input, error="PLACE arguments must be in the form X,Y,F"
        )

    x_str, y_str, f_str = (a.strip() for a in args)

    try:
        x = int(x_str)
        y = int(y_str)
    except ValueError:
        return InvalidCommand(
            input_text=original_input, error=f"PLACE X and Y must be integers, got '{x_str}', '{y_str}'"
        )

    try:
        facing = Direction(f_str.upper())
    except ValueError:
        valid = "NORTH, SOUTH, EAST, WEST"
        return InvalidCommand(
            input_text=original_input,
            error=f"PLACE facing must be one of {valid}, got '{f_str}'",
        )

    return PlaceCommand(position=Position(x, y), facing=facing)
