from .screen import Screen, Color
from .box import Box
from util.minepoint import Flag, Mask, Value
from util.coord import Coord


VALUECOLORS = [ 0, 38, 73, 40, 136, 172, 202, 161, 124, 9 ]
KEYS = { 'up': 'w', 'down': 's', 'left': 'a', 'right': 'd', 'open': ' ', 'mark': 'f' }
screen = Screen()


class Game:
    def __init__(self, field):
        self.field = field
        self.oldPos = None
        self.pos = Coord.random([field.width, field.height])
        self.cursor = Color(239, bg=True)
        self.stat = field.statistic()
        self.status = 'active'
        self.box = Box(field.width + 1, field.height + 1, 'soft')
        self.redraw = True
        self.fullredraw = True
        self.barsHeight = 2

    def draw(self):
        if self.status == 'active':
            if self.fullredraw:
                self.fullredraw = False
                self.redraw = True
                self.box.draw([0, self.barsHeight])
            if self.redraw:
                self.redraw = False
                self.drawField([1, self.barsHeight + 1])
                self.drawInfoBars()
            self.drawCursor([1, self.barsHeight + 1])
        elif self.status == 'lose':
            self.gameover([1, self.barsHeight + 1])
        elif self.status == 'win':
            self.drawField([0, self.barsHeight + 1])
            self.win([0, 0])
        else:
            screen[0, 0, Color.red].print(f'[Error] UNKNOWN GAME STATUS: {self.status}').whip()

    def drawCursor(self, offset):
        offset = Coord(offset)
        char, color = self.cellInfo(self.pos)
        screen.drawPixel(self.pos + offset, char, color + self.cursor)
        if self.oldPos is not None:
            char, color = self.cellInfo(self.oldPos)
            screen.drawPixel(self.oldPos + offset, char, color)

    def drawField(self, offset):
        offset = Coord(offset)
        for x, y in self.field:
            char, color = self.cellInfo(x, y)
            screen.drawPixel(x + offset.x, y + offset.y, char, color)

    def drawInfoBars(self):
        stat = self.stat
        screen[1, 0].print(f"Cells: {stat['cellsTotal']}/{self.field.size}").whip()
        screen[1, 1].print(f"Bombs left: {stat['bombsMarked']}/{self.field.bombs}").whip()

    def cellInfo(self, x, y=None):
        """Draw cell by coordinates."""
        if y is None:
            cell = self.field[Coord(x)]
        else:
            cell = self.field[Coord(x, y)]

        if cell == Mask.closed:
            if cell == Flag.noflag:
                return ' ', Color.bg.grey
            elif cell == Flag.guess:
                return 'G', Color('yellow', 'grey')
            elif cell == Flag.sure:
                return 'F', Color('banana', 'grey')
        else:
            if cell == Value.bomb:
                return '*', Color.red
            elif cell == Value.empty:
                return ' ', Color.white
            else:
                return str(cell), Color(VALUECOLORS[cell.value])

    def move(self, direct):
        if self.field.inBounds(self.pos + direct):
            self.oldPos = Coord(self.pos.x, self.pos.y)
            self.pos += direct

    def keyAction(self, key):
        if key == KEYS['up']:
            self.move(Coord(0, -1))
        elif key == KEYS['down']:
            self.move(Coord(0, 1))
        elif key == KEYS['left']:
            self.move(Coord(-1, 0))
        elif key == KEYS['right']:
            self.move(Coord(1, 0))
        else:
            if key == KEYS['mark']:
                if self.field[self.pos] == Mask.closed:
                    self.field.cycleFlag(self.pos)
            elif key == KEYS['open']:
                if self.field[self.pos] != Flag.sure and self.field.reveal(self.pos):
                    self.status = 'lose'
            self.redraw = True
            self.checkWin()

    def updateStat(self):
        self.stat = self.field.statistic()
        return self.stat

    def checkWin(self):
        self.updateStat()
        if self.stat['cellsRemaning'] == 0 and self.stat['allBombsCorrect']:
            self.status = 'win'

    def win(self, offset):
        offset = Coord(offset)
        screen[offset, Color.lime].print('Congrats!').whip()

    def gameover(self, offset):
        offset = Coord(offset)
        screen[0, 0, Color.red].print('You have lost!').whip()

        for x, y in self.field:
            if self.field[x, y] == Value.bomb:
                self.field[x, y] = Mask.opened
                char, color = self.cellInfo(x, y)
                screen.drawPixel(x + offset.x, y + offset.y, char, color)
        screen[offset + self.field.size]
