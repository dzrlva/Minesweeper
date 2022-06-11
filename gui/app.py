"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .game import Game
from .colors import COLORS
from random import seed
from .events import EventMaster


class App(tk.Tk):
    def __init__(self, width=900, height=700):
        super().__init__()
        EventMaster(self)
        self.title = 'Minesweeper'
        self.canvas = tk.Canvas(self, width=width, height=height, bg=COLORS['main'])
        self.canvas.pack(expand='no', fill='both')
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.onDeath)

        self.bind("<Button-2>", self.newSession)
        self.bind("<<Foo>>", self.newSession)
        self.session = None
        self.newSession()

    def onDeath(self):
        print('App is dying')
        if self.session:
            del self.session
        self.canvas.destroy()
        self.destroy()

    def newSession(self, args=None):
        # if (args):
            # print(args)
        if self.session:
            self.session.destroy()
            self.session = None
        else:
            self.session = Game(self, 40, .1)
