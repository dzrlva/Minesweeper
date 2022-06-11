"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .game import Game
from .colors import COLORS
from random import seed
from .events import EventMaster
from .menu import MainMenu
from tkextrafont import Font


class App(tk.Tk):
    def __init__(self, width=900, height=700):
        super().__init__()
        EventMaster(self)
        self.title = 'Minesweeper'

        self.font = Font(file="./resources/fonts/Purisa_Bold.ttf", size=20, family='Purisa')

        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
        self.width, self.height = width, height

        self.protocol("WM_DELETE_WINDOW", self.onDeath)
        self.bind("<Button-2>", self.newSession)
        self.bind("<<Switch-Menu>>", self.switchMenu)

        self.page = 'MainMenu'
        self.session = None
        self.newSession()

    def onDeath(self):
        print('App is dying')
        self.destroy()

    def switchMenu(self, event):
        print('Asked to switch menu to', event)
        if event.data == 'NewGameMenu':
            self.page = None
            self.newSession()

    def newSession(self, args=None):
        # if (args):
            # print(args)
        if self.session:
            self.session.destroy()
            self.session = None

        if self.page == 'MainMenu':
            self.session = MainMenu(self)
        else:
            self.session = Game(self, 8, .1)
