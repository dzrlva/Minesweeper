"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .game import Game
from .colors import COLORS
from random import seed
from .events import EventMaster
from .menu import MainMenu, NewGameMenu, SettingsMenu
# from tkextrafont import Font


class App(tk.Tk):
    def __init__(self, width=900, height=700):
        super().__init__()
        EventMaster(self)
        self.title = 'Minesweeper'
        self.username = 'Gamer1'

        # self.font = Font(file="./resources/fonts/Purisa_Bold.ttf", size=20, family='Purisa')
        self.font = ('Default', 20)

        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
        self.width, self.height = width, height

        self.protocol("WM_DELETE_WINDOW", self.onDeath)
        self.bind("<Button-2>", self.newSession)
        self.bind("<<Switch-Menu>>", self.switchMenu)
        self.bind("<<Game-Complete>>", self.onGameComplition)
        self.bind("<<Start-Game>>", self.onGameInit)

        COLORS.setTheme('light')

        # self.page = 'MainMenu'
        self.page = 'SettingsMenu'
        self.session = None
        self.newSession()

    def onDeath(self):
        print('App is dying')
        self.destroy()

    def onGameInit(self, event):
        self.gameOpts = event.data
        self.page = 'Game'
        self.newSession()

    def onGameComplition(self, event):
        self.page = 'MainMenu'
        self.newSession()

    def switchMenu(self, event):
        print('Asked to switch menu to', event)
        if event.data != self.page:
            self.page = event.data
            self.newSession()

    def newSession(self, args=None):
        # if (args):
            # print(args)
        if self.session:
            self.session.destroy()
            self.session = None

        if self.page == 'MainMenu':
            self.session = MainMenu(self)
        elif self.page == 'NewGameMenu':
            self.session = NewGameMenu(self, self.username)
        elif self.page == 'SettingsMenu':
            self.session = SettingsMenu(self)
        elif self.page == 'Game':
            self.session = Game(
                self,
                self.gameOpts['fieldsize'],
                self.gameOpts['difficulty']
            )
