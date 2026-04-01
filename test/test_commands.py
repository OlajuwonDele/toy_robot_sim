import pytest
from src.commands import (
    InvalidCommand,
    LeftCommand,
    MoveCommand,
    PlaceCommand,
    ReportCommand,
    RightCommand,
    parse_command,
)

from src.direction import Direction
from src.position import Position

class TestCommands:
    @pytest.mark.parametrize("test_input", ["MOVE", "move", "Move", "  MOVE  "])
    def test_move(self, test_input):
        assert parse_command(test_input) == MoveCommand()

    @pytest.mark.parametrize("test_input", ["LEFT", "left"])
    def test_left(self, test_input):
        assert parse_command(test_input) == LeftCommand()

    @pytest.mark.parametrize("test_input", ["RIGHT", "right"])
    def test_right(self, test_input):
        assert parse_command(test_input) == RightCommand()

    @pytest.mark.parametrize("test_input", ["REPORT", "rePort"])
    def test_report(self, test_input):
        assert parse_command(test_input) == ReportCommand()


class TestParsePlace:
    @pytest.mark.parametrize("test_input, expected", [
        ("PLACE 1,2,NORTH", PlaceCommand(Position(1, 2), Direction.NORTH)),
        ("PLACE 0,0,SOUTH", PlaceCommand(Position(0, 0), Direction.SOUTH)),
        ("PLACE 4,4,WEST",  PlaceCommand(Position(4, 4), Direction.WEST)),
        ])

    def test_place_validity(self, test_input, expected):
        assert parse_command(test_input) == expected

    @pytest.mark.parametrize("direction", list(Direction))
    def test_all_directions(self, direction):
        cmd = parse_command(f"PLACE 0,0,{direction.value}")
        assert isinstance(cmd, PlaceCommand)
        assert cmd.facing == direction
    
    @pytest.mark.parametrize("test_input", [
        "PLACE 0,0,north",   # lowercase
        "PLACE 0,0,North",   # mixed case
    ])
    def test_case_insensitive_direction(self, test_input):
        cmd = parse_command(test_input)
        assert isinstance(cmd, PlaceCommand)

    @pytest.mark.parametrize("line", [
        "PLACE 1 , 2 , EAST",   # spaces around commas
        "PLACE  1,2,EAST",      # extra space after PLACE
    ])
    def test_whitespace_tolerance(self, line):
        cmd = parse_command(line)
        assert isinstance(cmd, PlaceCommand)
        assert cmd.position == Position(1, 2)

    @pytest.mark.parametrize("line", [
        "PLACE",          # missing all args
        "PLACE 1,2",      # missing direction
        "PLACE a,2,NORTH",# non-integer x
        "PLACE 1.5, 2.3,NORTH",# float x,y
        "PLACE 1, 2, 4, NORTH",# len(args) > 3
        "PLACE 0,0,UP",   # invalid direction
    ])
    def test_invalid_place(self, line):
        assert isinstance(parse_command(line), InvalidCommand)

class TestParseInvalid:
    @pytest.mark.parametrize("line", ["", "   ", "jump", "bad INPUT"])
    def test_invalid_commands(self, line):
        assert isinstance(parse_command(line), InvalidCommand)

    def test_invalid_preserves_raw_input(self):
        raw = " bad INPUT"
        cmd = parse_command(raw)
        assert isinstance(cmd, InvalidCommand)
        assert cmd.input_text == raw
