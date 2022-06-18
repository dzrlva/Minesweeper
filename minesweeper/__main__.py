"""Start game as a module."""
from argparse import ArgumentParser
from minesweeper import main

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--gui",
        action="store_true",
        help="graphical user interface of minesweaper",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="command line interface of minesweaper",
    )
    args = parser.parse_args()
    main('cli' if args.cli else 'gui')
