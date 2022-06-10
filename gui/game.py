"""Module that uses logic.Field, draws board, handles user input."""
from util.point import Point
from util.coord import Coord
from .board import Board
from .colors import COLORS
from util.minepoint import Value, Mask


class Game():
    def __init__(self, app, field, *, maxBombStack=4):
        self.field = field
        self.app = app
        self.maxBombStack = maxBombStack
        if maxBombStack <= 0 or maxBombStack >= 6:
            raise ValueError('Maximum bomb stack should not allow impossible bombs!')

        self.board = Board(app, 12, debug=False)
        self.board.draw()
        self.marked = set()
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

    def updateBoard(self):
        for x, y in self.field:
            if self.field[x, y] == Mask.opened:
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

    def onRightClick(self, event):
        pos = Coord(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)
        if pos is not None:
            self.board.toggleFlag(pos)

    def onLeftClick(self, event):
        pos = Coord(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)
        if pos is not None:
            revealed = self.field.reveal(pos)
            if (revealed is None):
                print('Bro, you died')
            else:
                print(len(revealed), 'cell were opened')
            self.field[pos] = Mask.opened
            self.updateBoard()
        # clicked.openCell(COLORS['inactive'], text='I')
