"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .game import Game
from logic.field import Field
from .colors import COLORS
from random import seed


class Session:
    def __init__(self, app, replayCallback):
        self.app = app
        self.game = Game(app, None)
        # self.app.bind('<<Foo>>', replayCallback)
        self.field = Field(self.game.board.rows, self.game.board.cols, .3, kind='hexagon')
        self.game.field = self.field
        self.game.board.field = self.field
        self.game.updateField()
        self.game.updateBoard()


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
        self.session = Session(self, self.newSession)
