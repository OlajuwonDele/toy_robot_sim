from __future__ import annotations
import argparse
import sys
import io
from src.table import Table
from src.simulator import Simulator

def build_parser():
    parser = argparse.ArgumentParser(
        prog = "mars_rover",
        description="Toy Robot Simulator"
    )

    parser.add_argument(
        "input_file",
        nargs="?",
        metavar="FILE",
        help="Path to a command file. Reads from stdin if omitted.",
    )

    parser.add_argument(
        "--width",
        type=int,
        default=5,
        metavar="N",
        help="Table width, (default: 5)",
    )

    parser.add_argument(
        "--height",
        type=int,
        default=5,
        metavar="N",
        help="Table height, (default: 5)",
    )

    return parser

def run(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    output = io.TextIOWrapper(sys.stdout.buffer, line_buffering=True)
    table = Table(width = args.width, height = args.height)
    simulator = Simulator(table=table, output=output)

    if args.input_file:
        try:
            source = open(args.input_file, encoding="utf-8")
        except OSError as exc:
            parser.error(str(exc))
    else:
        source = sys.stdin

    try:
        simulator.run_lines(source)

    finally:
        if args.input_file:
            source.close()

if __name__ == "__main__":
    run()