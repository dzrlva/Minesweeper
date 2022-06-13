"""Main file to start the APP."""

import sys
from argparse import ArgumentParser
from minesweeper.gui.app import App as GUIAPP
from minesweeper.cli.menu import startmenu


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
    if args.cli:
        startmenu()
    else:
        GUIAPP().mainloop()
    sys.exit(0)
