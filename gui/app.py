"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .game import Game
from .colors import COLORS
from .events import EventMaster
from .menu import MainMenu, NewGameMenu, SettingsMenu
# from tkextrafont import Font


class App(tk.Tk):
    """Gui App class."""

    def __init__(self, width=900, height=700):
        """Initialize GUI app."""
        super().__init__()
        EventMaster(self)
        self.title = 'Minesweeper'
        self.username = 'Gamer1'

        # self.fontLoaded = Font(file="./resources/fonts/Purisa_Bold.ttf", size=20, family='Purisa')
        self.font = ('Purisa', 20)
        # self.font = ('Default', 20)

        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
        self.width, self.height = width, height

        self.protocol("WM_DELETE_WINDOW", self.onDeath)
        self.bind("<<Switch-Menu>>", self.switchMenu)
        self.bind("<<Start-Game>>", self.onGameInit)
        self.bind("<<Save-Settings>>", self.onSettingsSave)

        self.page = 'MainMenu'
        self.gameOpts = { 'difficulty': 0.1, 'fieldsize-name': 'tiny' }
        self.appOpts = { 'colorscheme': COLORS.schemeName, 'language': 'English' }

        COLORS.setTheme(self.appOpts['colorscheme'])
        self.configure(bg=COLORS['main'],)

        self.session = None
        self.newSession()

    def onDeath(self):
        """Application is closed."""
        # print('App is dying')
        self.destroy()

    def onSettingsSave(self, event):
        """Save settings given from menu."""
        self.appOpts['colorscheme'] = event.data['colorscheme']
        COLORS.setTheme(self.appOpts['colorscheme'])
        self.configure(bg=COLORS['main'])

    def onGameInit(self, event):
        """Init game with given options by menu."""
        self.gameOpts = event.data
        self.page = 'Game'
        self.newSession()

    def switchMenu(self, event):
        """Switch current view to given menu."""
        # print('Asked to switch menu to', event)
        if event.data != self.page:
            self.page = event.data
            self.newSession()

    def newSession(self, args=None):
        """Replace current view with new session based on self.page."""
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
