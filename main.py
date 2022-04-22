#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from cli.app import App as CLIAPP
from cli.menu import startmenu

def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--cli",
        action="store_true",
        help="command line interface of minesweaper",
    )
    args = parser.parse_args()
    if True or args.cli:
        startmenu()
        #CLIAPP().mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
