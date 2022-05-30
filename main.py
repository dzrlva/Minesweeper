#!/usr/bin/env python
"""Main file."""
import sys
from argparse import ArgumentParser
from cli.menu import startmenu


def main():
    """(Will) release start gui or cli minesweeper."""
    parser = ArgumentParser()
    parser.add_argument(
        "--cli",
        action="store_true",
        help="command line interface of minesweaper",
    )
    args = parser.parse_args()
    if True or args.cli:
        startmenu()
        # CLIAPP().mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
