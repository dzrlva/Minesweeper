"""Module that uses logic.Field, draws board, handles user input."""

import tkinter as tk
from util.minepoint import Value, Mask
from util import Coord, Point
from .board import Board
from logic.field import Field


class Game():
    def __init__(self, app):
        self.board = Board(app, 12)
        self.field = Field(self.board.rows, self.board.cols, .2)
        self.app = app
        self.app.canvas.bind("<Button-1>", self.onLeftClick)
        self.app.canvas.bind("<Button-2>", self.onRightClick)
        pass

    def draw_hex(self, x, y):
        if self.field[x, y] == Mask.opened:
            if self.field[x, y] == Value.bomb:
                self.board.drawBomb(x, y)
            else:
                self.board.drawOpenCell(Point(x, y,), str(self.field[x, y].value))

    def onRightClick(self, event):
        clicked = self.findClicked()
        self.board.check_flag(clicked)

    def onLeftClick(self, event):
        points = self.field.reveal(self.findClicked())
        for p in points:
            self.draw_hex(p.x, p.y)
        '''
        if clicked in self.selected:
            clicked.changeFill(COLORS['inactive'])
            self.selected.remove(clicked)
        else:
            clicked.changeFill(COLORS['active'])
            self.selected.add(clicked)
        '''
