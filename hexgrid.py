#!/usr/bin/python

import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter.constants import *
from tkinter import PhotoImage
from math import cos, sin, sqrt, radians

diag = 12

class FillHexagon:
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def __init__(self, parent, x, y, length, color, tags):
        self.parent = parent  # canvas

        self.x = x  # top left x
        self.y = y  # top left y
        self.length = length  # length of a side
        self.color = color  # fill color
        self.selected = False
        self.tags = tags
        self.draw()

    def draw(self):
        start_x = self.x
        start_y = self.y
        angle = 60
        coords = []
        for i in range(6):
            end_x = start_x + self.length * cos(radians(angle * i))
            end_y = start_y + self.length * sin(radians(angle * i))
            coords.append([start_y, start_x])
            start_x = end_x
            start_y = end_y
        self.parent.create_polygon(coords[0][0],coords[0][1],
                                   coords[1][0],coords[1][1],
                                   coords[2][0],coords[2][1],
                                   coords[3][0],coords[3][1],
                                   coords[4][0],coords[4][1],
                                   coords[5][0],coords[5][1],
                                   fill=self.color,
                                   outline="#003153",
                                   tags=self.tags)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.img = Image.open("resources/flag0.png").resize((47, 47))
        self.img = ImageTk.PhotoImage(self.img)

        self.title("Hexagon Grid")
        self.can = tk.Canvas(self, width=900, height=900, bg="#003153")
        self.can.pack(expand=YES, fill=BOTH)
        self.hexagons = []

        if diag == 12:
            ssize = 34
        elif diag == 14:
            ssize = 28
        elif diag == 16:
            ssize = 26
        elif diag <= 20:
            ssize = 21
        elif diag <= 24:
            ssize = 17
        elif diag <= 28:
            ssize = 16
        elif diag <= 30:
            ssize = 15
        elif diag <= 34:
            ssize = 13
        elif diag <= 38:
            ssize = 12
        elif diag <= 42:
            ssize = 11
        else:
            ssize = 10

        self.initGrid(diag + 2, diag, ssize, debug=False)

        self.can.bind("<Button-1>", self.click)


    def initGrid(self, cols, rows, size, debug):
        """
        2d grid of hexagons
        """
        if size < 20:
            y_offset = 30
        else:
            y_offset = 90
        x = rows / 2
        for c in range(cols):
            if c % 2 == 0:
                offset = size * sqrt(3) / 2
            else:
                offset = 0

            if c == 0:
                x_offset = rows
            elif c == 1 or c == cols - 1:
                x_offset = rows / 4
                x = rows / 2
            else:
                if c < (rows / 2 + 1):
                    x += 1
                    if c % 2 == 0:
                        x_offset -= 1
                elif c == rows / 2 + 1:
                    x = rows
                    x_offset = 0
                else:
                    x -= 1
                    if c % 2 != 0:
                        x_offset += 1

            rx_offset = x + x_offset
            for r in range(rows):

                if r < x_offset or r >= rx_offset:
                    colour = "#003153"
                else :
                    colour = "#ffffff"

                h = FillHexagon(self.can,
                                c * (size * 1.5) + 30,
                                (r * (size * sqrt(3))) + offset + y_offset,
                                size,
                                colour,
                                "{}.{}".format(r, c))
                self.hexagons.append(h)

                if debug:
                    coords = "{}, {}".format(r, c)
                    self.can.create_text((r * (size * sqrt(3))) + offset + (size) +  y_offset - 15,
                                         c * (size * 1.5) + (size / 2) + 25, anchor=W, font="Purisa", fill="black",
                                         text=coords)
        self.can.create_text(400, 760, anchor=W, font="Purisa 20", fill="white", text="Minesweeper")

    def click(self, evt):
        """
        hexagon detection on mouse click
        """

        st = [0]*len(self.hexagons)
        x, y = evt.x, evt.y
        for i in self.hexagons:
            #i.selected = False
            i.isNeighbour = False
            self.can.itemconfigure(i.tags, fill=i.color)
        clicked = self.can.find_closest(x, y)[0]  # find closest
        print("CLICKED = ", clicked)
        st[int(clicked) - 1] = self.hexagons[int(clicked) - 1].selected

        self.hexagons[int(clicked) - 1].selected = True
        j = -1
        for i in self.hexagons:  # re-configure selected only
            j += 1
            if i.selected:
                self.can.create_image(i.y + 30, i.x + 15, image=self.img)
                if i.color == "#003153":
                    i.selected = False
                    st[j] = False
                elif st[j]:
                    self.can.itemconfigure(i.tags, fill="#003153")
                    i.selected = False
                    st[j] = False
                else:
                    self.can.itemconfigure(i.tags, fill="#ffffff")

            if i.isNeighbour:
                self.can.itemconfigure(i.tags, fill="#76d576")

if __name__ == '__main__':
    #print("Please, select the diameter of the playing field:")
    #print("(in range from 12 to 50 any multiple of 2)")
    #diag = int(input())
    app = App()
    app.mainloop()

