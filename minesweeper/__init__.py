"""Contains main function of the game."""
import sys
from minesweeper.gui.app import App as GUIAPP
from minesweeper.cli.menu import startmenu


def main(mode='gui'):
    """Run the game."""
    if mode == 'cli':
        startmenu()
    elif mode == 'gui':
        GUIAPP().mainloop()
    else:
        print('Unknown game mode:', mode)
        sys.exit(1)
    sys.exit(0)
