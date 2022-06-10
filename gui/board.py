"""Module that draws the game board."""

from util import loadImage
from util.point import Point
from math import sqrt
from .hexagon import Hexagon
from .colors import COLORS


IMAGES = {
    'flag': ['./resources/images/flag.png', (32, 32)],
}


class Board:
    def __init__(self, app, diagonal, *, debug=False):
        self.app = app
        self.debug = debug
        self.img = {}
        for res, resAttr in IMAGES.items():
            self.img[res] = loadImage(*resAttr)
        self.setDimensions(diagonal)
        self.board = { Point(row, col): dict() for row, col in Point.range([self.rows, self.cols]) }
        self.__createBoard()

    def __createBoard(self):
        y_offset = 30 if self.size < 20 else 90
        x = self.rows / 2
        for col in range(self.cols):
            offset = 0 if col % 2 else self.size * sqrt(3) / 2

            if col == 0:
                x_offset = self.rows
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
                hexX = row * self.size * sqrt(3) + offset + y_offset
                hexY = col * self.size * 1.5 + 30
                hexTags = f'{row}.{col}'
                hxg = Hexagon(
                    self.app.canvas, hexX, hexY,
                    self.size, COLORS['inactive'], COLORS['outline'], hexTags,
                    COLORS['hover'],
                )

                self.board[Point(row, col)]['hex'] = hxg
                if self.debug:
                    # textX = row * self.size * sqrt(3) + offset + self.size + y_offset - 20
                    # textY = col * self.size * 1.5 + self.size / 2 + 25
                    textX, textY = hxg.center - [10, 0]
                    debugCoords = self.app.canvas.create_text(
                        textX, textY, anchor='w', font="Purisa", fill="black", text=f'{row}, {col}'
                    )
                    self.board[Point(row, col)]['debug'] = debugCoords

    def draw(self):
        for cell in self.board.values():
            if cell is not None:
                cell['hex'].draw()
                if self.debug:
                    self.app.canvas.tag_raise(cell['debug'])
        # if self.debug:
            # for i, pos, cell in enumerate(self.board.items()):
                # if cell is not None:
                    # debugID = self.app.canvas.create_text(
                        # cell['hex'].center.x, cell['hex'].center.y,
                        # anchor='w', font="Purisa", fill="black", text=str(i)
                    # )
                    # self.board[pos]['debug'] = debugID

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
                coord.x, coord.y, image=self.img['flag'], state='disabled'
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
        # cell['hex'].deactivate()
        if text is not None and 'text' not in cell:
            text = self.app.canvas.create_text(
                cell['hex'].center.x, cell['hex'].center.y,
                anchor='c', fill='white', text=text,
                state='disabled'
            )
            cell['text'] = text
        return True
