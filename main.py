#!/usr/bin/env python
"""Main file to start the APP."""

import sys
from argparse import ArgumentParser
from gui.app import App as GUIAPP
from cli.menu import startmenu
from translation import _

print(_('Welcome'))


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
        # CLIAPP().mainloop()
    else:
        GUIAPP().mainloop()
    sys.exit(0)
