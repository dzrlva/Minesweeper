"""Single hexagon. WARNING: coordinates are sligtly messed up."""
from math import sin, cos, tan, radians, sqrt
from util.coord import Coord


ANGLE = 60
SIDES = 6
COEF = tan(radians(ANGLE))


class Hexagon:

    def __init__(self, canvas, x, y, length, color, outline, tags):
        self.canvas = canvas  # canvas

        self.length = length
        self.height = COEF * self.length / sqrt(COEF**2 + 1)
        self.width = COEF * self.height / 2
        self.topleft = Coord(x, y + self.height / 4, dtype=float)
        whH = Coord(self.width / 2, -self.height / 2, dtype=float)
        self.center = self.topleft + whH

        self.color = color
        self.outline = outline
        self.selected = False
        self.tags = tags
        self.__item = None
        self.__calculate()
        self.pos = Coord(self.coords[0], self.coords[1], dtype=float)

    def __calculate(self):
        startX, startY = self.center
        startY -= self.height
        offset, rotation = 0, 30
        self.coords = []
        for i in range(SIDES):
            endX = startX + self.length * cos(radians(ANGLE * (i + offset) + rotation))
            endY = startY + self.length * sin(radians(ANGLE * (i + offset) + rotation))
            self.coords.append(startX)
            self.coords.append(startY)
            startX, startY = endX, endY

    def distance(self, x, y=None):
        diff = Coord(x, y, dtype=float) - self.center
        return sqrt(diff.x**2 + diff.y**2)

    def changeFill(self, color):
        self.color = color
        if self.__item:
            self.canvas.itemconfigure(self.__item, fill=color)

    def draw(self):
        if self.__item:
            self.canvas.delete(self.__item)
        self.__item = self.canvas.create_polygon(
            *self.coords, fill=self.color, outline=self.outline, tags=self.tags
        )
        return self.__item
