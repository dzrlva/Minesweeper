"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .game import Game
from .colors import COLORS
from random import seed


class Session:
    def __init__(self, app, replayCallback):
        self.app = app
        self.game = Game(app, None)
        self.app.bind('<<Foo>>', replayCallback)

    def __del__(self):
        self.game.destroy()


class App(tk.Tk):
    def __init__(self, width=900, height=900):
        super().__init__()
        self.title = 'Minesweeper'
        self.canvas = tk.Canvas(self, width=width, height=width, bg=COLORS['main'])
        self.canvas.pack(expand='no', fill='both')

        self.canvas.bind("<Button-2>", self.newSession)
        self.session = None
        self.newSession()

    def newSession(self, *args):
        if self.session:
            del self.session
            self.session = None
        else:
            self.session = Session(self, self.newSession)
