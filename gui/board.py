"""Module that draws the game board."""

import tkinter as tk
from util import loadImage, Coord, Point, dotdict
from math import sqrt
from .hexagon import Hexagon
from .colors import COLORS
from time import sleep


SCALE_FACTOR = 12
RESOURCES = {
    'flag': {
        'path': './resources/images/flag.png',
        'size': 32
    },
    'explosion': {
        'path': './resources/animations/explosion1.gif',
        'size': 38
    },
    'bomb': {
        'path': './resources/images/bomb.png',
        'size': 38
    }
}


class Board:
    def __init__(self, app, diagonal):
        self.app = app
        self.resources = {}
        for resName, resAttr in RESOURCES.items():
            self.resources[resName] = loadImage(resAttr, scale=SCALE_FACTOR / diagonal)
        self.setDimensions(diagonal)
        self.board = { Point(row, col): dict() for row, col in Point.range([self.rows, self.cols]) }
        self.topleft = Coord(10, 10)
        self.__createBoard()

    def __del__(self):
        for cell in self.board.values():
            if cell is not None:
                cell['hex'].destroy()
                if 'text' in cell:
                    self.app.canvas.delete(cell['text'])

    def __createBoard(self):
        for col in range(self.cols):
            offset = 0 if col % 2 else self.size * sqrt(3) / 2

            if col == 0:
                x = x_offset = self.rows
            elif col == 1 or col == self.cols - 1:
                x_offset = self.rows / 4
                x = self.rows / 2
            else:
                if col < (self.rows / 2 + 1):
                    x += 1
                    if col % 2 == 0:
                        x_offset -= 1
                elif col == self.rows / 2 + 1:
                    x = self.rows
                    x_offset = 0
                else:
                    x -= 1
                    if col % 2 != 0:
                        x_offset += 1

            rx_offset = x + x_offset
            for row in range(self.rows):
                if row < x_offset or row >= rx_offset:
                    self.board[Point(row, col)] = None
                    continue  # do not create hexagon if it out of field
                hexX = row * self.size * sqrt(3) + offset + self.topleft.x
                hexY = col * self.size * 1.5 + self.topleft.y
                hexTags = f'{row}.{col}'
                self.board[Point(row, col)]['hex'] = Hexagon(
                    self.app.canvas, hexX, hexY,
                    self.size, COLORS['inactive'], COLORS['outline'], hexTags,
                    COLORS['hover'],
                )

    def draw(self):
        for cell in self.board.values():
            if cell is not None:
                cell['hex'].draw()

    def __animation(self, anim):
        frame = next(anim.frames, None)
        anim.label.config(image=frame)
        if frame:
            anim.label.after(anim.delay, self.__animation, anim)
        else:
            anim.label.destroy()
            self.app.canvas.create_image(
                anim.center.x, anim.center.y, image=self.resources['bomb']
            )
            if anim.callback:
                anim.callback()

    def drawExplosion(self, pos, *, callback=None):
        rcs = self.resources['explosion']
        bomb = dotdict({
            'label': tk.Label(self.app, bg=COLORS['cells']['bomb']),
            'center': self.board[pos]['hex'].center,
            'frames': iter(rcs['frames']),
            'delay': rcs['delay'],
            'callback': callback
        })
        coord = bomb.center - rcs['size'] / 2
        bomb.label.place(x=coord.x, y=coord.y)
        self.__animation(bomb)

    def toggleFlag(self, pos):
        pos = Point(pos)
        if pos not in self.board or self.board[pos] is None:
            return

        cell = self.board[pos]
        if 'flag' in cell:
            self.app.canvas.delete(cell['flag'])
            del cell['flag']
        elif pos in self.board:
            coord = cell['hex'].center
            flag = self.app.canvas.create_image(
                coord.x, coord.y, image=self.resources['flag'], state='disabled'
            )
            self.board[pos]['flag'] = flag

    def setDimensions(self, diag):
        if diag == 12:
            self.size = 34
        elif diag == 14:
            self.size = 28
        elif diag == 16:
            self.size = 26
        elif diag <= 20:
            self.size = 21
        elif diag <= 24:
            self.size = 17
        elif diag <= 28:
            self.size = 16
        elif diag <= 30:
            self.size = 15
        elif diag <= 34:
            self.size = 13
        elif diag <= 38:
            self.size = 12
        elif diag <= 42:
            self.size = 11
        else:
            self.size = 10
        self.cols, self.rows = diag + 2, diag

    def findClicked(self, pos):
        for pos, cell in self.board.items():
            if cell is not None and cell['hex'].hovered:
                return pos
        return None

    def openCell(self, point, color, text=None):
        point = Point(point)
        if point not in self.board:
            return False
        cell = self.board[point]
        if cell is None:
            return False

        cell['hex'].changeFill(color)
        cell['hex'].deactivate()
        if text is not None and 'text' not in cell and text:
            text = self.app.canvas.create_text(
                cell['hex'].center.x, cell['hex'].center.y,
                anchor='c', fill='white', text=text,
                state='disabled'
            )
            cell['text'] = text
        return True

    def disable(self):
        for cell in self.board.values():
            if cell is not None:
                cell['hex'].hover = False
