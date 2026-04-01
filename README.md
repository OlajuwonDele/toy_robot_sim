# Toy Robot Simulator

A Python-based simulation of a toy robot moving on a square 5x5 tabletop. The robot accepts commands to place itself, move, rotate, and report its position while preventing itself from falling off the table.

## Features
* **Safe Movement:** The robot ignores any move that would cause it to fall off the table.
* **Robust Parsing:** Handles whitespace, case-insensitivity, and inline comments (`#`) in input files.
* **Extensible:** Built with a clean command-pattern architecture using Python dataclasses.

---

## How to Use

### Running the Simulator
The simulator can be run as a module from the root directory. It supports both interactive manual input and .txt processing.

**1. Process a Command File:**
```bash
python3 -m src.main examples/example_a.txt
```

**2. Interactive Mode:**
Run without arguments to type commands manually. Press Ctrl+D to exit.

```bash
python3 -m src.main
```

**3. Custom Table Size:**

```bash
python3 -m src.main --width 10 --height 10
```

## Command Set
**PLACE X,Y,F:** Put the robot on the table at position X,Y facing NORTH, SOUTH, EAST, or WEST.

**MOVE:** Move the robot one unit forward in its current direction.

**LEFT:** Rotate the robot 90 degrees to the left.

**RIGHT:** Rotate the robot 90 degrees to the right.

**REPORT:** Output the current X,Y, and Facing of the robot.

## Testing
This project uses pytest for unit and integration testing.

Run all tests: 
```bash
pytest
```

Run specific test file:
```bash
pytest test/test_simulator.py
```

## Project Structure
src/: Contains the core logic (Robot, Table, Commands, Simulator).

test/: Contains unit tests.

examples/: Sample .txt files for batch processing and edge-case testing.