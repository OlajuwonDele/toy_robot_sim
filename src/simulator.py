from __future__ import annotations

import sys
from typing import IO, Iterable, Optional
from src.table import Table
from src.robot import Robot
from src.commands import (
    Command,
    InvalidCommand,
    LeftCommand,
    MoveCommand,
    PlaceCommand,
    ReportCommand,
    RightCommand,
    parse_command,
)

class Simulator:
    """Toy robot simulator environment"""
    def __init__(
        self,
        table: Table | None = None,
        output: IO[str] = sys.stdout,
        ) -> None:

        self._table: Table = table or Table()
        self._robot: Robot | None = None
        self._output: IO[str] = output

    @property
    def robot(self) -> Optional[Robot]:
        """The current robot state, or None if not yet placed."""
        return self._robot
    
    def execute(self, command: Command) -> None:
        """
        Apply a single command to the simulator.

        Invalid commands and commands issued before a valid PLACE are
        silently ignored.
        """
        if isinstance(command, InvalidCommand):
            return

        if isinstance(command, PlaceCommand):
            self._place(command)
        elif self._robot is None:
            return
        elif isinstance(command, MoveCommand):
            self._move()
        elif isinstance(command, LeftCommand):
            self._robot = self._robot.turn_left()
        elif isinstance(command, RightCommand):
            self._robot = self._robot.turn_right()
        elif isinstance(command, ReportCommand):
            self._output.write(self._robot.report() + "\n")


    def run_lines(self, lines: Iterable[str]) -> None:
        """Parse and execute an iterable of raw text lines."""
        for line in lines:
            self.execute(parse_command(line))

    def _place(self, command: PlaceCommand) -> None:
        if self._table.is_valid_position(command.position):
            self._robot = Robot(command.position, command.facing)

    def _move(self) -> None:
        assert self._robot is not None  
        candidate = self._robot.move()
        if self._table.is_valid_position(candidate.position):
            self._robot = candidate
