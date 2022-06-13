"""CLI app."""
from .game import Game
from .screen import Screen
from .color import Color
from minesweeper.logic.field import Field

# from logic.gamestat import Stat
from blessed import Terminal

# import time


class App:
    """Cli App class."""

    def mainloop(self):
        """Loop game until it's completed."""
        field = Field(30, 20, 0.15)
        term = Terminal()
        screen = Screen()
        game = Game(field)

        # username = 'Gamer1'
        # tempname = input(f'Input another name if you are not {username}: ')
        # if tempname:
        #    username = tempname

        # stat = Stat()
        # stat.assignFile(username)
        # stat.readStatistic()

        with term.cbreak(), term.hidden_cursor():
            screen.clear()
            game.draw()
            # starttime = time.time()
            key = ""

            while key != "q" and game.status == "active":
                key = term.inkey(timeout=3)
                if not key:
                    continue

                game.keyAction(key)
                game.draw()

            # stat['win'] = game.status == 'win'

        # stat['gametime'] = round(time.time() - starttime, 1)
        # stat.saveStatistic()
        screen.setCursor(0, field.height + 6).setColor(Color.reset)
        # stat.print()
