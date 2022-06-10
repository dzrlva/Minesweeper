"""Module that uses logic.Field, draws board, handles user input."""
from util.point import Point
from .board import Board
from .colors import COLORS
from util.minepoint import Value, Mask, Flag


class Game():
    def __init__(self, app, field):
        Flag
        self.field = field
        self.app = app
        self.board = Board(app, 12, debug=False)
        self.board.draw()
        self.marked = set()
        self.app.canvas.bind("<Button-1>", self.onLeftClick)
        self.app.canvas.bind("<Button-3>", self.onRightClick)

    def updateField(self):
        for pos, cell in self.board.board.items():
            if cell is None:
                self.field[pos] = Value.empty
        self.field.recalculate()

    def updateBoard(self):
        for x, y in self.field:
            if self.field[x, y] == Mask.opened:
                if self.field[x, y] == Value.bomb:
                    color, text = COLORS['cells']['bomb'], 'BOMB'
                elif self.field[x, y] == Value.empty:
                    color, text = COLORS['active'], None
                else:
                    text = str(self.field[x, y].value)
                    color = COLORS['cells'][text]
                self.board.openCell(Point(x, y), color, text)

    def onRightClick(self, event):
        pos = Point(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)
        if pos is not None:
            self.board.toggleFlag(pos)

    def onLeftClick(self, event):
        pos = Point(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)
        if pos is not None:
            self.field.reveal(pos)
            self.field[pos] = Mask.opened
            self.updateBoard()
        # clicked.openCell(COLORS['inactive'], text='I')
