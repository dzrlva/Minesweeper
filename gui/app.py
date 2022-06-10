"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .game import Game
from .colors import COLORS
from random import seed


class App(tk.Tk):
    def __init__(self, width=900, height=700):
        super().__init__()
        self.title = 'Minesweeper'
        self.canvas = tk.Canvas(self, width=width, height=height, bg=COLORS['main'])
        self.canvas.pack(expand='no', fill='both')
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)

        self.canvas.bind("<Button-2>", self.newSession)
        self.session = None
        self.newSession()

    def newSession(self, *args):
        if self.session:
            del self.session
            self.session = None
        self.session = Game(self, 10, .1)
