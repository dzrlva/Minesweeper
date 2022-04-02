"""Module that uses logic.Field, draws board, handles user input."""

import tkinter as tk
from util.minepoint import Value, Mask
from util import Coord, Point
from .board import Board
from logic.field import Field


class Game(tk.Tk):
    def __init__(self, app):
        self.board = Board(app, 12)
        self.field = Field(self.board.rows, self.board.cols, .2)
        self.app.canvas.bind("<Button-1>", self.onLeftClick)
        self.app.canvas.bind("<Button-2>", self.onRightClick)
        pass

    def draw_hex(self, x, y):
        for x, y in self.field:
            if self.field[x, y] == Mask.opened:
                if self.field[x, y] == Value.bomb:
                    self.board.drawBomb(x, y)
                else:
                    self.board.drawOpenCell(x, y, color, str(self.field[x, y].value))

    def onRightClick(self, event):
        pixel = Coord(event.x, event.y)
        clicked = self.findClicked(pixel)

        if clicked in self.marked:
            flag = self.marked[clicked]
            self.app.canvas.delete(flag)
            del self.marked[clicked]
        else:
            x, y = clicked.center

            self.flag = self.app.canvas.create_image(x, y, image=self.img['flag'], state='disabled')

            self.marked[clicked] = flag

    def onLeftClick(self, event):
        pixel = Coord(event.x, event.y)
        clicked = self.findClicked(pixel)

        self.draw_hex()

        if clicked in self.selected:
            clicked.changeFill(COLORS['inactive'])
            self.selected.remove(clicked)
        else:
            clicked.changeFill(COLORS['active'])
            self.selected.add(clicked)

