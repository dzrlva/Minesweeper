"""Module that uses logic.Field, draws board, handles user input."""
from util.point import Point
from util.coord import Coord
from .board import Board
from .colors import COLORS
from util.minepoint import Value, Mask, Flag


class Game():
    def __init__(self, app, field, *, maxBombStack=4):
        self.field = field
        self.app = app
        self.maxBombStack = maxBombStack
        if maxBombStack <= 0 or maxBombStack >= 6:
            raise ValueError('Maximum bomb stack should not allow impossible bombs!')

        self.marked = 0
        self.markedRight = 0
        self.opened = 0

        self.board = Board(app, 12, debug=False)
        self.board.draw()
        self.app.canvas.bind("<Button-1>", self.onLeftClick)
        self.app.canvas.bind("<Button-3>", self.onRightClick)

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
            if self.field[x, y] == Value.bomb or self.field[x, y] == Mask.opened:
                if self.field[x, y] == Value.barrier:
                    color, text = COLORS['main'], ''
                elif self.field[x, y] == Value.bomb:
                    color, text = COLORS['cells']['bomb'], 'BOMB'
                elif self.field[x, y] == Value.empty:
                    color, text = COLORS['active'], None
                else:
                    text = str(self.field[x, y].value)
                    color = COLORS['cells'][text]
                self.board.openCell(Point(x, y), color, text)

    def gameOver(self):
        print('Bro, you died')

    def gameWin(self):
        print('BRO, YOU WON')

    def checkWin(self):
        if self.marked != self.markedRight:
            return False
        if self.opened + self.marked == self.field.size - self.barriers:
            return True
        return False

    def onRightClick(self, event):
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
        pos = Coord(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)
        if pos is None or self.field[pos] == Flag.sure:
            return

        revealed = self.field.reveal(pos)
        if revealed is None:
            self.field[pos] = Mask.opened
            self.gameOver()
        else:
            self.opened += len(revealed)
            if self.checkWin():
                self.gameWin()
        self.updateBoard()
        # clicked.openCell(COLORS['inactive'], text='I')
