"""Module that uses logic.Field, draws board, handles user input."""

import tkinter as tk
from util.point import Point
from util.coord import Coord
from .board import Board
from logic.field import Field
from .colors import COLORS
from util.minepoint import Value, Mask, Flag


class Game():
    def __init__(self, app, size, difficulty, *, maxBombStack=4):
        self.app = app
        self.maxBombStack = maxBombStack
        if maxBombStack <= 0 or maxBombStack >= 6:
            raise ValueError('Maximum bomb stack should not allow impossible bombs!')

        self.marked = 0
        self.markedRight = 0
        self.opened = 0
        self.status = 'game'

        self.board = Board(app, size, width=1, height=.8)
        self.field = Field(self.board.rows, self.board.cols, difficulty, kind='hexagon')
        self.board.draw()
        self.updateField()
        self.updateBoard()

        self.lmbBind = self.app.bind("<Button-1>", self.onLeftClick)
        self.rmbBind = self.app.bind("<Button-3>", self.onRightClick)

    def destroy(self):
        self.app.unbind("<Button-1>", self.lmbBind)
        self.app.unbind("<Button-3>", self.rmbBind)
        self.app = None
        self.board.destroy()

    def updateField(self):
        """Set barrier around playble area and remove impossible bombs"""
        for pos, cell in self.board.board.items():
            if cell is None:
                self.field[pos] = Value.barrier

        for crd in self.field:
            if self.field[crd] != Value.bomb:
                continue
            curBombStack = 0
            for bias in self.field.pattern(crd):
                curCrd = crd + bias
                if curCrd == crd:
                    continue
                if self.field[curCrd] == Value.bomb or self.field[curCrd] == Value.barrier:
                    curBombStack += 1
                    if curBombStack >= self.maxBombStack:
                        self.field[crd] = Value.empty
                        break

        self.field.recalculate()
        self.barriers = 0
        for crd in self.field:
            self.barriers += self.field[crd] == Value.barrier

    def updateBoard(self):
        for x, y in self.field:
            if self.field[x, y] == Mask.opened:
                text = None
                if self.field[x, y] == Value.barrier:
                    color = COLORS['main']
                elif self.field[x, y] == Value.bomb:
                    color = COLORS['cells']['bomb']
                elif self.field[x, y] == Value.empty:
                    color = COLORS['cells']['empty']
                else:
                    text = str(self.field[x, y].value)
                    color = COLORS['cells'][text]
                self.board.openCell(Point(x, y), color, text)

    def completeGame(self):
        self.board.disable()
        self.app.event_generate("<<Foo>>", data=self.status)

    def gameOver(self, pos):
        if self.status == 'gameover':
            return
        self.status = 'gameover'
        print('Bro, you died')
        self.board.drawExplosion(pos, callback=self.completeGame)

    def gameWin(self):
        self.status = 'win'
        print('BRO, YOU WON')
        self.completeGame()

    def checkWin(self):
        if self.marked != self.markedRight:
            return False
        if self.opened + self.marked == self.field.size - self.barriers:
            return True
        return False

    def onRightClick(self, event):
        if self.status != 'game':
            return

        pos = Coord(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)

        if pos is None or self.field[pos] == Mask.opened:
            return

        self.board.toggleFlag(pos)
        self.field.toggleFlag(pos)
        if self.field[pos] == Flag.sure:
            self.marked += 1
            self.markedRight += self.field[pos] == Value.bomb
        else:
            self.marked -= 1
            self.markedRight -= self.field[pos] == Value.bomb

        if self.checkWin():
            self.gameWin()

    def onLeftClick(self, event):
        if self.status != 'game':
            return

        pos = Coord(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)
        if pos is None or self.field[pos] == Flag.sure:
            return

        revealed = self.field.reveal(pos)
        if revealed is None:
            self.field[pos] = Mask.opened
            self.gameOver(pos)
        elif len(revealed) > 0:
            self.opened += len(revealed)
            if self.checkWin():
                self.gameWin()
        self.updateBoard()
        # clicked.openCell(COLORS['inactive'], text='I')
