"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .board import Board


# [!] Move to another file
COLORS = {
    'main': '#003153',
}


# [!] Make so App spawns playble hexagon field
class App(tk.Tk):
    def __init__(self, width=900, height=900):
        super().__init__()
        self.title = 'Minesweeper'
        self.canvas = tk.Canvas(self, width=width, height=width, bg=COLORS['main'])
        self.canvas.pack(expand='no', fill='both')

        self.board = Board(self, 12)
