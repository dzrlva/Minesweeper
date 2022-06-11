"""Module that draws the game board."""

import tkinter as tk
from util import loadImage, Coord, Point, dotdict
from math import sqrt
from .hexagon import Hexagon
from .colors import COLORS
from time import sleep


SCALE_FACTOR = 1.2
RESOURCES = {
    'flag': './resources/images/flag.png',
    'explosion': './resources/animations/explosion1.gif',
    'bomb': './resources/images/bomb.png',
}


class Board:
    def __init__(self, app, size, width, height):
        self.app = app

        # self.width = app.winfo_width() * width
        # self.height = app.winfo_height() * height
        self.width = self.app.width * width
        self.height = self.app.height * height

        size += size % 2
        if size < 8:
            raise ValueError('Only sizes 8 and more allowed')

        self.topleft = Coord(10, 10)
        self.cols, self.rows = size + 2, size

        self.hexLength, woh = Hexagon.getMaxLengthByGeom(
            (self.width - self.topleft.x) / self.cols,
            (self.height - self.topleft.y) / self.rows
        )
        if woh == 'h':
            self.hexLength -= self.hexLength * (4 / 3) / self.rows
        else:
            self.hexLength += self.hexLength * (4 / 3) / self.cols

        hexWidth, _ = Hexagon.getDimensions(self.hexLength)
        actualWidth = (self.cols - 1) * hexWidth - self.cols
        self.topleft.x = (self.width - actualWidth) / 2

        self.resources = {}
        for resName, resPath in RESOURCES.items():
            self.resources[resName] = loadImage(resPath, SCALE_FACTOR * self.hexLength)
        self.board = { Point(row, col): dict() for row, col in Point.range([self.rows, self.cols]) }
        self.__createBoard()

    def destroy(self):
        for cell in self.board.values():
            if cell is not None:
                cell['hex'].destroy()
                if 'text' in cell:
                    self.app.canvas.delete(cell['text'])
                if 'bomb' in cell:
                    self.app.canvas.delete(cell['bomb'])
                if 'anim' in cell:
                    cell['anim'].label.destroy()
        self.app = None

    def __createBoard(self):
        for col in range(self.cols):
            offset = 0 if col % 2 else self.hexLength * sqrt(3) / 2

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
                hexX = row * self.hexLength * sqrt(3) + offset + self.topleft.x
                hexY = col * self.hexLength * 1.5 + self.topleft.y
                self.board[Point(row, col)]['hex'] = Hexagon(
                    self.app.canvas, hexX, hexY,
                    self.hexLength,
                    COLORS['hexagon.inactive'], COLORS['hexagon.outline'],
                    COLORS['hexagon.hover'],
                )

    def draw(self):
        for cell in self.board.values():
            if cell is not None:
                cell['hex'].draw()

    def __animation(self, cell):
        frame = next(cell['anim'].frames, None)
        cell['anim'].label.config(image=frame)
        if frame:
            cell['anim'].label.after(cell['anim'].delay, self.__animation, cell)
        else:
            cell['anim'].label.destroy()
            callback = cell['anim'].callback
            del cell['anim']
            if callback:
                callback()

    def drawExplosion(self, pos, *, callback=None):
        rcs = self.resources['explosion']
        cell = self.board[pos]
        cell['anim'] = dotdict({
            'label': tk.Label(self.app, bg=COLORS['cells.bomb']),
            'frames': iter(rcs['frames']),
            'delay': rcs['delay'],
            'callback': callback
        })
        coord = cell['hex'].center - rcs['size'] / 2
        cell['anim'].label.place(x=coord.x, y=coord.y)
        self.__animation(cell)

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

        if text == 'BOMB':
            if 'flag' in cell:
                cell['hex'].changeFill(COLORS['cells.correct-flag'])
            else:
                cell['bomb'] = self.app.canvas.create_image(
                    cell['hex'].center.x, cell['hex'].center.y,
                    image=self.resources['bomb']
                )
        elif text is not None and 'text' not in cell and text:
            if 'flag' in cell:
                cell['hex'].changeFill(COLORS['cells.incorrect-flag'])
            else:
                text = self.app.canvas.create_text(
                    cell['hex'].center.x, cell['hex'].center.y,
                    anchor='c', fill=COLORS['hexagon.text'], text=text,
                    state='disabled', font=(self.app.font[0], 13)
                )
                cell['text'] = text
        return True

    def disable(self):
        for cell in self.board.values():
            if cell is not None:
                cell['hex'].hover = False
