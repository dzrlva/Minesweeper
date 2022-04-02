"""Module that draws the game board."""

from util import loadImage
from util import Point, Coord
from math import sqrt
from .hexagon import Hexagon


IMAGES = {
    'flag': ['./resources/flag.png', (40, 40)],
}
COLORS = {  # [!] Moved to another file
    'active': '#0081a3',
    'inactive': '#ffffff',
    'outline': '#003153',
    'hover': '#03dfaa',
    '0': "#ffffff"
    '1': '#59DF9F',
    '2': '#9BE382',
    '3': '#D0DA62',
    '4': '#DEBB60',
    '5': '#F0923C',
    '6': '#E46666',
    '7': '#ffffff',
    '8': '#ffffff',
    'bomb': '#AA0000',
}


class Board:  # [!] Board only should draw hexagons and text. Nothing more!
    def __init__(self, app, diagonal):
        self.app = app
        self.debug = False
        self.img = {}
        self.selected = set()  # delete as complete
        self.marked = dict()  # same
        for res, resAttr in IMAGES.items():
            self.img[res] = loadImage(*resAttr)
        self.setDimensions(diagonal)
        self.__createBoard()
        self.__draw()
        self.__data = {Point(row, col): dict() for row, col in Point.range([self.rows, self.cols])}

    def __draw(self):
        for i, hgn in enumerate(self.hexagons):
            hgn.draw()
        if self.debug:
            for i, hgn in enumerate(self.hexagons):
                self.app.canvas.create_text(
                    hgn.center.x, hgn.center.y,
                    anchor='w', font="Purisa", fill="black", text=str(i)
                )

    def __createBoard(self):
        self.hexagons = []
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
                    continue  # do not create hexagon if it out of field
                hexX = row * self.size * sqrt(3) + offset + y_offset
                hexY = col * self.size * 1.5 + 30
                hexTags = f'{row}.{col}'
                hxg = Hexagon(
                    self.app.canvas, hexX, hexY,
                    self.size, COLORS['inactive'], COLORS['outline'], hexTags,
                    COLORS['hover'],
                )
                self.__data[Point(row, col)]['hexagon'] = hxg

                self.hexagons.append(hxg)
                self.__data[Point(row, col)]['hexagon'] = hxg
                if self.debug:
                    textX = row * self.size * sqrt(3) + offset + self.size + y_offset - 15,
                    textY = col * self.size * 1.5 + self.size / 2 + 25
                    self.app.canvas.create_text(
                        textX, textY, anchor='w', font="Purisa", fill="black", text=f'{row}, {col}'
                    )

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

    def findClicked(self):
        for pos, cell in self.__data.items():
            if cell['hexagon'].hovered:
                return pos

    def drawBomb(self, x, y):
        ###

    def drawOpenCell(self, p, text):
        hgx = self.__data[p]['hexagon']
        coords = self.__data[p]['hexagon'].center
        self.can.itemconfigure(hgx, fill=COLORS[text])
        if text != '0':
            self.app.canvas.create_text(
                *coords,  anchor='w', font="Purisa 20", fill="white", text=text
            )

    def check_flag(self):
        x, y = clicked.center
        if clicked in self.marked:
            self.delete_flag(x, y)
        else:
            self.set_flag(x, y)

    def set_flag(self, x, y):
        self.__data[Point(x, y)]['flag'] = self.app.canvas.create_image(x, y, image=self.img['flag'],
                                                                                  state='disabled')
    def delete_flag(self, x, y):
        self.app.canvas.delete(self.__data[Point(x, y)]['flag'])
