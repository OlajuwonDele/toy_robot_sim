import pytest

from src.direction import Direction
from src.position import Position
from src.robot import Robot
from src.table import Table

class TestDirection:
    @pytest.mark.parametrize("start, expected", [
        (Direction.NORTH, Direction.WEST),
        (Direction.WEST,  Direction.SOUTH),
        (Direction.SOUTH, Direction.EAST),
        (Direction.EAST,  Direction.NORTH),
    ])
    def test_turn_left(self, start, expected):
        assert start.turn_left() == expected

    @pytest.mark.parametrize("start, expected", [
        (Direction.NORTH, Direction.EAST),
        (Direction.EAST,  Direction.SOUTH),
        (Direction.SOUTH, Direction.WEST),
        (Direction.WEST,  Direction.NORTH),
    ])
    def test_turn_right(self, start, expected):
        assert start.turn_right() == expected

    @pytest.mark.parametrize("start", list(Direction))
    def test_full_left_rotation_returns_to_start(self, start):
        d = start
        for _ in range(4):
            d = d.turn_left()
        assert d == start

    @pytest.mark.parametrize("start", list(Direction))
    def test_full_right_rotation_returns_to_start(self, start):
        d = start
        for _ in range(4):
            d = d.turn_right()
        assert d == start


class TestPosition:
    @pytest.mark.parametrize("direction, expected", [
    (Direction.NORTH, Position(2, 3)),
    (Direction.SOUTH, Position(2, 1)),
    (Direction.EAST,  Position(3, 2)),
    (Direction.WEST,  Position(1, 2)),
    ])
    def test_step(self, direction, expected):
        original = Position(2, 2)
        result = original.step(direction)
        assert result == expected          # new object is correct
        assert original == Position(2, 2)  # original unchanged


class TestRobot:
    @pytest.fixture
    def robot(self):
        return Robot(Position(2, 3), Direction.NORTH)

    @pytest.mark.parametrize("direction, expected_position", [
        (Direction.NORTH, Position(0, 1)),
        (Direction.EAST,  Position(1, 0)),
        (Direction.SOUTH, Position(0, -1)),
        (Direction.WEST,  Position(-1, 0)),
    ])
    def test_move(self, direction, expected_position):
        robot = Robot(Position(0, 0), direction)
        assert robot.move().position == expected_position

    def test_turn_left_changes_facing_only(self, robot):
        rotated = robot.turn_left()
        assert rotated.facing == Direction.WEST
        assert rotated.position == robot.position

    def test_turn_right_changes_facing_only(self, robot):
        rotated = robot.turn_right()
        assert rotated.facing == Direction.EAST
        assert rotated.position == robot.position

    @pytest.mark.parametrize("position, facing, expected", [
        (Position(1, 2), Direction.EAST,  "1,2,EAST"),
        (Position(0, 0), Direction.NORTH, "0,0,NORTH"),
        (Position(4, 4), Direction.WEST,  "4,4,WEST"),
    ])
    def test_report_format(self, position, facing, expected):
        assert Robot(position, facing).report() == expected

    def test_turn_left_does_not_mutate(self, robot):
        robot.turn_left()
        assert robot.facing == Direction.NORTH

    def test_turn_right_does_not_mutate(self, robot):
        robot.turn_right()
        assert robot.facing == Direction.NORTH


class TestTable:
    @pytest.fixture
    def table(self):
        return Table()

    def test_default_dimensions(self, table):
        assert table.width == 5
        assert table.height == 5

    @pytest.mark.parametrize("x,y", [(0, 0), (4, 4), (0, 4), (4, 0), (2, 2)])
    def test_valid_positions(self, table, x, y):
        assert table.is_valid_position(Position(x, y))

    @pytest.mark.parametrize("x,y", [(-1, 0), (0, -1), (5, 0), (0, 5), (5, 5), (-1, -1)])
    def test_invalid_positions(self, table, x, y):
        assert not table.is_valid_position(Position(x, y))

    def test_custom_table_size(self):
        table = Table(width=3, height=3)
        assert table.is_valid_position(Position(2, 2))
        assert not table.is_valid_position(Position(3, 3))