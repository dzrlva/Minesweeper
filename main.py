#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from gui.app import App as GUIAPP
from cli.app import App as CLIAPP
from cli.menu import startmenu

def main():
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
    if True or args.cli:
        startmenu()
        #CLIAPP().mainloop()
    else:
        GUIAPP().mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
