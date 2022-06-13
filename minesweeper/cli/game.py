"""CLI version of game interface."""
from .screen import Screen, Color
from .box import Box
from minesweeper.util.minepoint import Flag, Mask, Value
from minesweeper.util.point import Point


VALUECOLORS = [0, 38, 73, 40, 136, 172, 202, 161, 124, 9]
KEYS = {
    "up": "w",
    "down": "s",
    "left": "a",
    "right": "d",
    "open": " ",
    "mark": "f",
    "cheats": "x",
}
screen = Screen()


class Game:
    """Game class."""

    def __init__(self, field):
        """Create game."""
        self.field = field
        self.oldPos = None
        self.pos = Point.random([field.width, field.height])
        self.cursor = Color(239, bg=True)
        self.stat = field.statistic()
        self.status = "active"
        self.box = Box(field.width + 1, field.height + 1, "soft")
        self.redraw = True
        self.fullredraw = True
        self.barsHeight = 2
        self.cheats = False

    def draw(self):
        """Draw game attributes."""
        if self.status == "active":
            if self.fullredraw:
                self.fullredraw = False
                self.redraw = True
                self.box.draw([0, self.barsHeight])
            if self.redraw:
                self.redraw = False
                self.drawField([1, self.barsHeight + 1])
            self.drawInfoBars()
            self.drawCursor([1, self.barsHeight + 1])
        elif self.status == "lose":
            self.gameover([1, self.barsHeight + 1])
        elif self.status == "win":
            self.drawField([0, self.barsHeight + 1])
            self.win([0, 0])
        else:
            screen[0, 0, Color.red].print(
                f"[Error] UNKNOWN GAME STATUS: {self.status}"
            ).whip()

    def drawCursor(self, offset):
        """Draw cursor in current position."""
        offset = Point(offset)
        char, color = self.cellInfo(self.pos)
        if self.cheats and self.field[self.pos] == Value.bomb:
            char = "*"
        screen.drawPixel(self.pos + offset, char, color + self.cursor)
        if self.oldPos is not None:
            char, color = self.cellInfo(self.oldPos)
            screen.drawPixel(self.oldPos + offset, char, color)

    def drawField(self, offset):
        """Draw field at current state."""
        offset = Point(offset)
        for x, y in self.field:
            char, color = self.cellInfo(x, y)
            screen.drawPixel(x + offset.x, y + offset.y, char, color)

    def drawInfoBars(self):
        """Draw info bars."""
        stat = self.stat
        cheats = " [CHEATS]" if self.cheats else ""
        screen[1, 0].print(f"Cells: {stat['cellsTotal']}/{self.field.size}").whip()
        screen[1, 1].print(
            f"Bombs{cheats}: {stat['bombsMarked']}/{self.field.bombs}"
        ).whip()

    def cellInfo(self, x, y=None):
        """Get cell draw character and color used."""
        if y is None:
            cell = self.field[Point(x)]
        else:
            cell = self.field[Point(x, y)]

        if cell == Mask.closed:
            if cell == Flag.noflag:
                return " ", Color.bg.grey
            elif cell == Flag.guess:
                return "G", Color("yellow", "grey")
            elif cell == Flag.sure:
                return "F", Color("banana", "grey")
        else:
            if cell == Value.bomb:
                return "*", Color.red
            elif cell == Value.empty:
                return " ", Color.white
            else:
                return str(cell), Color(VALUECOLORS[cell.value])

    def move(self, direct):
        """Move cursor at certain direction."""
        if self.field.inBounds(self.pos + direct):
            self.oldPos = Point(self.pos.x, self.pos.y)
            self.pos += direct

    def keyAction(self, key):
        """React to key press."""
        if key == KEYS["up"]:
            self.move(Point(0, -1))
        elif key == KEYS["down"]:
            self.move(Point(0, 1))
        elif key == KEYS["left"]:
            self.move(Point(-1, 0))
        elif key == KEYS["right"]:
            self.move(Point(1, 0))
        elif key == KEYS["cheats"]:
            self.cheats = not self.cheats
        else:
            if key == KEYS["mark"]:
                if self.field[self.pos] == Mask.closed:
                    self.field.cycleFlag(self.pos)
            elif key == KEYS["open"]:
                if self.field[self.pos] != Flag.sure:
                    if self.field[self.pos] == Value.bomb:
                        self.status = "lose"
                    else:
                        self.field.reveal(self.pos)
            self.redraw = True
            self.checkWin()

    def updateStat(self):
        """Update field statistic."""
        self.stat = self.field.statistic()
        return self.stat

    def checkWin(self):
        """Check if game is complete."""
        self.updateStat()
        if self.stat["cellsRemaning"] == 0 and self.stat["allBombsCorrect"]:
            self.status = "win"

    def win(self, offset):
        """Draw win state."""
        offset = Point(offset)
        screen[offset, Color.lime].print("Congrats!").whip()

    def gameover(self, offset):
        """Draw lose state."""
        offset = Point(offset)
        screen[0, 0, Color.red].print("You have lost!").whip()

        for x, y in self.field:
            if self.field[x, y] == Value.bomb:
                self.field[x, y] = Mask.opened
                char, color = self.cellInfo(x, y)
                screen.drawPixel(x + offset.x, y + offset.y, char, color)
        screen[offset + self.field.size]
