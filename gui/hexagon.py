"""Single hexagon. WARNING: coordinates are sligtly messed up."""
import tkinter as tk
from math import sin, cos, tan, radians, sqrt
from util import Coord


ANGLE = 60
SIDES = 6
COEF = tan(radians(ANGLE))


class Hexagon:

    def __init__(self, canvas, x, y, length, color, outline, tags, hover=None):
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
        self.tags = tags
        self.__item = None
        self.__calculate()

    def destroy(self):
        try:
            if self.hover:
                self.deactivate()
            if self.__item:
                self.canvas.delete(self.__item)
        except tk._tkinter.TclError:
            pass

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
        diff = Coord(x, y, dtype=float) - self.center
        return sqrt(diff.x**2 + diff.y**2)

    def changeFill(self, color):
        self.color = color
        self.unhover = self.color
        if self.__item:
            self.canvas.itemconfigure(self.__item, fill=color)

    def onEnter(self, event):
        self.hovered = True
        if self.hover:
            temp = self.color
            self.changeFill(self.hover)
            self.unhover = temp

    def onLeave(self, event):
        self.hovered = False
        if self.hover:
            self.changeFill(self.unhover)

    def deactivate(self):
        self.hover = self.hovered = False
        self.canvas.tag_unbind(self.__item, '<Enter>', self.entBind)
        self.canvas.tag_unbind(self.__item, '<Leave>', self.lveBind)

    def activate(self):
        self.entBind = self.canvas.tag_bind(self.__item, '<Enter>', self.onEnter)
        self.lveBind = self.canvas.tag_bind(self.__item, '<Leave>', self.onLeave)

    def draw(self):
        if self.__item:
            self.destroy()
        self.__item = self.canvas.create_polygon(
            *self.coords, fill=self.color, outline=self.outline, tags=self.tags,
        )
        if self.hover:
            self.activate()
        return self.__item
