"""Single gui hexagon."""
from math import sin, cos, tan, radians, sqrt
from minesweeper.util import Coord


ANGLE = 60
SIDES = 6
COEF = tan(radians(ANGLE))


class Hexagon:
    """Draw hexagon."""

    @staticmethod
    def getDimensions(length):
        """Get width, height by hexagon side length."""
        return COEF * length, 2 * length

    @staticmethod
    def getMaxLengthByGeom(width, height):
        """Get maximum length of height with given width and height."""
        if width < height:
            return width / COEF, 'w'
        else:
            return height * (2 / 3), 'h'

    def __init__(self, canvas, x, y, length, color, outline, hover=None):
        """Create hexagon."""
        self.canvas = canvas  # canvas

        self.length = length
        # self.height = COEF * self.length / sqrt(COEF**2 + 1)
        self.height = 2 * self.length
        self.width = COEF * self.height / 2
        self.topleft = Coord(x, y + self.height / 4, dtype=float)
        # whH = Coord(self.width / 2, -self.height / 2, dtype=float)
        whH = Coord(self.width / 2, -self.height / 4, dtype=float)
        # self.center = self.topleft + whH
        self.center = Coord(x, y, dtype=float) + whH
        self.origin = Coord(x, y, dtype=float)

        self.hovered = False
        self.hover = hover
        self.unhover = color
        self.color = color
        self.outline = outline
        self.selected = False
        self.__item = None
        self.__calculate()

        self.entBind = self.lveBind = None

    def destroy(self):
        """Carefully remove hexagon without a trace."""
        self.deactivate()
        if self.__item:
            self.canvas.delete(self.__item)
        self.canvas = None

    def __calculate(self):
        startX, startY = self.origin
        startY -= self.height / 2
        offset, rotation = -1, 30
        self.coords = []

        for i in range(SIDES):
            endX = startX + self.length * cos(radians(ANGLE * (i + offset) + rotation))
            endY = startY + self.length * sin(radians(ANGLE * (i + offset) + rotation))
            self.coords.append(startX)
            self.coords.append(startY)
            startX, startY = endX, endY

    def distance(self, x, y=None):
        """Calculate distance from x, y to hexagon."""
        diff = Coord(x, y, dtype=float) - self.center
        return sqrt(diff.x**2 + diff.y**2)

    def changeFill(self, color):
        """Fill hexagon differently."""
        self.color = color
        self.unhover = self.color
        if self.__item:
            self.canvas.itemconfigure(self.__item, fill=color)

    def onEnter(self, event):
        """Event when mouse enters hexagon."""
        self.hovered = True
        if self.hover:
            temp = self.color
            self.changeFill(self.hover)
            self.unhover = temp

    def onLeave(self, event):
        """Event when mouse leaves hexagon."""
        self.hovered = False
        if self.hover:
            self.changeFill(self.unhover)

    def deactivate(self):
        """Disable hover action."""
        if not self.hover:
            return
        self.hover = self.hovered = False
        if self.entBind:
            self.canvas.tag_unbind(self.__item, '<Enter>', self.entBind)
        if self.lveBind:
            self.canvas.tag_unbind(self.__item, '<Leave>', self.lveBind)

    def activate(self):
        """Enable hover action."""
        self.entBind = self.canvas.tag_bind(self.__item, '<Enter>', self.onEnter)
        self.lveBind = self.canvas.tag_bind(self.__item, '<Leave>', self.onLeave)

    def draw(self):
        """Draw hexagon on canvas."""
        if self.__item:
            self.destroy()
        self.__item = self.canvas.create_polygon(
            *self.coords, fill=self.color, outline=self.outline
        )
        if self.hover:
            self.activate()
        return self.__item
