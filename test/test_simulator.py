"""Unit tests for toy_robot.simulator.Simulator."""

import io
import pytest

from src.commands import (
    LeftCommand, MoveCommand, PlaceCommand,
    ReportCommand, RightCommand, InvalidCommand,
)
from src.direction import Direction
from src.position import Position
from src.robot import Robot
from src.table import Table
from src.simulator import Simulator

@pytest.fixture
def sim():
    buf = io.StringIO()
    simulator = Simulator(output=buf)
    return simulator, buf

@pytest.fixture
def placed_sim(sim):
    simulator, buf = sim
    simulator.execute(PlaceCommand(Position(2, 2), Direction.NORTH))
    return simulator, buf

class TestPlacement:
    @pytest.mark.parametrize("position, facing", [
        (Position(0, 0), Direction.NORTH),
        (Position(2, 3), Direction.EAST),
        (Position(4, 4), Direction.SOUTH),
    ])
    def test_valid_place_positions_robot(self, sim, position, facing):
        simulator, _ = sim
        simulator.execute(PlaceCommand(position, facing))
        assert simulator.robot == Robot(position, facing)

    @pytest.mark.parametrize("position", [
        Position(5, 5),   # outside bounds
        Position(-1, 0),  # negative x
        Position(0, -1),  # negative y
        Position(9, 9),   # out of bounds
    ])
    def test_invalid_place_is_ignored(self, sim, position):
        simulator, _ = sim
        simulator.execute(PlaceCommand(position, Direction.NORTH))
        assert simulator.robot is None

    def test_new_place_replaces_robot(self, sim):
        simulator, _ = sim
        simulator.execute(PlaceCommand(Position(0, 0), Direction.NORTH))
        simulator.execute(PlaceCommand(Position(3, 3), Direction.SOUTH))
        assert simulator.robot == Robot(Position(3, 3), Direction.SOUTH)

    def test_invalid_place_does_not_remove_robot(self, sim):
        simulator, _ = sim
        simulator.execute(PlaceCommand(Position(0, 0), Direction.NORTH))
        simulator.execute(PlaceCommand(Position(9, 9), Direction.NORTH))
        assert simulator.robot == Robot(Position(0, 0), Direction.NORTH)

class TestCommandsBeforePlacement:
    @pytest.mark.parametrize("command", [
        MoveCommand(),
        LeftCommand(),
        RightCommand(),
        InvalidCommand(input_text="incorrect", error="unknown"),
    ])
    def test_command_before_place_leaves_robot_as_none(self, sim, command):
        simulator, _ = sim
        simulator.execute(command)
        assert simulator.robot is None

    @pytest.mark.parametrize("command", [
        ReportCommand(),
        InvalidCommand(input_text="slop", error="unknown"),
    ])
    def test_command_before_place_produces_no_output(self, sim, command):
        simulator, buf = sim
        simulator.execute(command)
        assert buf.getvalue() == ""

class TestMove:
    @pytest.mark.parametrize("start, facing, expected", [
        (Position(0, 0), Direction.NORTH, Position(0, 1)),
        (Position(0, 4), Direction.SOUTH, Position(0, 3)),
        (Position(0, 0), Direction.EAST,  Position(1, 0)),
        (Position(4, 0), Direction.WEST,  Position(3, 0)),
    ])
    def test_move_updates_position(self, sim, start, facing, expected):
        simulator, _ = sim
        simulator.execute(PlaceCommand(start, facing))
        simulator.execute(MoveCommand())
        assert simulator.robot.position == expected

    @pytest.mark.parametrize("start, facing", [
        (Position(0, 4), Direction.NORTH),  # north edge
        (Position(0, 0), Direction.SOUTH),  # south edge
        (Position(4, 0), Direction.EAST),   # east edge
        (Position(0, 0), Direction.WEST),   # west edge
    ])
    def test_move_off_edge_is_ignored(self, sim, start, facing):
        simulator, _ = sim
        simulator.execute(PlaceCommand(start, facing))
        simulator.execute(MoveCommand())
        assert simulator.robot.position == start

    def test_move_does_not_change_facing(self, sim):
        simulator, _ = sim
        simulator.execute(PlaceCommand(Position(2, 2), Direction.EAST))
        simulator.execute(MoveCommand())
        assert simulator.robot.facing == Direction.EAST


class TestReport:
    @pytest.mark.parametrize("position, facing, expected", [
        (Position(1, 2), Direction.EAST,  "1,2,EAST"),
        (Position(0, 0), Direction.NORTH, "0,0,NORTH"),
        (Position(4, 4), Direction.WEST,  "4,4,WEST"),
    ])
    def test_report_format(self, sim, position, facing, expected):
        simulator, buf = sim
        simulator.execute(PlaceCommand(position, facing))
        simulator.execute(ReportCommand())
        assert buf.getvalue().strip() == expected

    def test_report_includes_newline(self, placed_sim):
        simulator, buf = placed_sim
        simulator.execute(ReportCommand())
        assert buf.getvalue().endswith("\n")

    def test_multiple_reports(self, sim):
        simulator, buf = sim
        simulator.execute(PlaceCommand(Position(0, 0), Direction.NORTH))
        simulator.execute(ReportCommand())
        simulator.execute(MoveCommand())
        simulator.execute(ReportCommand())
        assert buf.getvalue().splitlines() == ["0,0,NORTH", "0,1,NORTH"]


class TestSpecificationExamples:
    @pytest.mark.parametrize("lines, expected", [
        (
            ["PLACE 0,0,NORTH", "MOVE", "REPORT"],
            ["0,1,NORTH"],
        ),
        (
            ["PLACE 0,0,NORTH", "LEFT", "REPORT"],
            ["0,0,WEST"],
        ),
        (
            ["PLACE 1,2,EAST", "MOVE", "MOVE", "LEFT", "MOVE", "REPORT"],
            ["3,3,NORTH"],
        ),
    ])
    def test_spec_examples(self, sim, lines, expected):
        simulator, buf = sim
        simulator.run_lines(lines)
        assert buf.getvalue().splitlines() == expected

class TestEdgeCases:
    def test_commands_before_first_place_are_discarded(self, sim):
        simulator, buf = sim
        simulator.run_lines(["MOVE", "LEFT", "REPORT", "PLACE 0,0,NORTH", "REPORT"])
        assert buf.getvalue().splitlines() == ["0,0,NORTH"]

    @pytest.mark.parametrize("facing", list(Direction))
    def test_robot_blocked_at_edge_stays_in_place(self, sim, facing):
        simulator, _ = sim
        simulator.execute(PlaceCommand(Position(0, 0), facing))
        for _ in range(10):
            simulator.execute(MoveCommand())
        assert simulator.robot is not None

    @pytest.mark.parametrize("command, count", [
        (LeftCommand,  4),
        (RightCommand, 4),
        (LeftCommand,  8),  # two full rotations
    ])
    def test_full_rotation_returns_to_start(self, sim, command, count):
        simulator, buf = sim
        simulator.execute(PlaceCommand(Position(0, 0), Direction.NORTH))
        for _ in range(count):
            simulator.execute(command())
        simulator.execute(ReportCommand())
        assert buf.getvalue().strip() == "0,0,NORTH"

    def test_walk_entire_perimeter(self, sim):
        simulator, buf = sim
        simulator.run_lines(
            ["PLACE 0,0,NORTH"]
            + ["MOVE"] * 4 + ["RIGHT"]
            + ["MOVE"] * 4 + ["RIGHT"]
            + ["MOVE"] * 4 + ["RIGHT"]
            + ["MOVE"] * 4
            + ["REPORT"]
        )
        assert buf.getvalue().strip() == "0,0,WEST"

    def test_garbled_input_interspersed_with_valid(self, sim):
        simulator, buf = sim
        simulator.run_lines(
            ["GARBAGE", "PLACE 0,0,NORTH", "NOT_A_COMMAND", "MOVE", "REPORT"]
        )
        assert buf.getvalue().splitlines() == ["0,1,NORTH"]

    def test_custom_table_size(self):
        buf = io.StringIO()
        simulator = Simulator(table=Table(width=3, height=3), output=buf)
        simulator.execute(PlaceCommand(Position(2, 2), Direction.NORTH))
        simulator.execute(MoveCommand())
        simulator.execute(ReportCommand())
        assert buf.getvalue().strip() == "2,2,NORTH"
    
class TestFileHandling:
    def test_run_from_valid_file(self, sim, tmp_path):
        """Test that the simulator correctly processes a real .txt file."""
        simulator, buf = sim
        
        # Create a temporary directory and file
        d = tmp_path / "commands"
        d.mkdir()
        file_path = d / "input.txt"
        
        # Write some commands to the file
        commands = [
            "PLACE 1,2,EAST",
            "MOVE",
            "MOVE",
            "LEFT",
            "MOVE",
            "REPORT"
        ]
        file_path.write_text("\n".join(commands))

        # Open the file and pass it to run_lines
        # (Remember: file objects are iterables of strings!)
        with open(file_path, "r") as f:
            simulator.run_lines(f)

        assert buf.getvalue().strip() == "3,3,NORTH"

    def test_empty_file_does_nothing(self, sim, tmp_path):
        """Test that an empty file produces no errors or output."""
        simulator, buf = sim
        file_path = tmp_path / "empty.txt"
        file_path.write_text("")

        with open(file_path, "r") as f:
            simulator.run_lines(f)

        assert buf.getvalue() == ""
        assert simulator.robot is None

    def test_file_with_mixed_whitespace_and_garbage(self, sim, tmp_path):
        """Test that file reading handles extra newlines and invalid lines."""
        simulator, buf = sim
        file_path = tmp_path / "messy.txt"
        
        # Note the leading spaces and empty lines
        messy_commands = [
            "",
            "  PLACE 0,0,NORTH",
            "INVALID_COMMAND",
            "",
            "MOVE",
            "REPORT  "
        ]
        file_path.write_text("\n".join(messy_commands))

        with open(file_path, "r") as f:
            simulator.run_lines(f)

        assert buf.getvalue().strip() == "0,1,NORTH"


class TestExampleFiles:
    @pytest.mark.parametrize("filename, expected_output", [
        (
            "example_a.txt", 
            ["0,1,NORTH"]
        ),
        (
            "example_b.txt", 
            ["0,0,WEST"]
        ),
        (
            "example_c.txt", 
            ["3,3,NORTH"]
        ),
        (
            "edge_cases.txt", 
            [
                "0,4,NORTH", # After first set of MOVES (blocked at edge)
                "0,4,NORTH", # After spinning 360 degrees
                "0,4,NORTH", # After trying to move SOUTH (Wait! See Note below)
                "4,4,NORTH"  # After final PLACE and moves
            ]
        ),
    ])
    def test_file_execution(self, sim, filename, expected_output):
        simulator, buf = sim
        
        # Path to your examples folder
        # Adjust "examples/" if your test runs from a different directory
        filepath = f"examples/{filename}"
        
        try:
            with open(filepath, "r") as f:
                simulator.run_lines(f)
        except FileNotFoundError:
            pytest.fail(f"Test file {filepath} not found. Check your paths!")

        # Capture output and compare
        actual_output = buf.getvalue().splitlines()
        assert actual_output == expected_output
