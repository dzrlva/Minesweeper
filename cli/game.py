from .screen import Color
from util.minepoint import Flag, Mask, Value
from util.coord import Coord


VALUECOLORS = [ 0, 38, 73, 40, 136, 172, 202, 161, 124, 9 ]
KEYS = { 'up': 'w', 'down': 's', 'left': 'a', 'right': 'd', 'open': ' ', 'mark': 'f' }


class Game:
    def __init__(self, screen, field):
        self.screen = screen
        self.field = field
        self.pos = Coord(0, 0)
        # self.pos = Coord.random(field.size)
        self.cursor = Color(239, bg=True)
        self.stat = field.statistic()
        self.status = 'active'

    def draw(self):
        if self.status == 'active':
            self.drawField([0, 4])
            self.drawInfoBars()
            self.drawCursor([0, 4])
        elif self.status == 'lose':
            self.gameover([0, 4])
        elif self.status == 'win':
            self.drawField([0, 4])
            self.win([0, 0])
        else:
            self.screen[0, 0, Color.red].print(f'[Error] UNKNOWN GAME STATUS: {self.status}').whip()

    def cellInfo(self, cell):
        """Draw cell by coordinates."""
        if cell == Mask.closed:
            if cell == Flag.noflag:
                return ' ', Color.bg.grey
            elif cell == Flag.guess:
                return 'G', Color.yellow
            elif cell == Flag.sure:
                return 'F', Color.banana
        else:
            if cell == Value.bomb:
                return '*', Color.red
            elif cell == Value.empty:
                return ' ', Color.white
            else:
                return str(cell), Color(VALUECOLORS[cell.value])

    def drawCursor(self, offset):
        pos = self.pos + Coord(offset)
        char, color = self.cellInfo(self.field[self.pos])
        self.screen.drawPixel(pos.x, pos.y, char, color + self.cursor)

    def drawField(self, offset):
        offset = Coord(offset)
        for x, y in self.field:
            char, color = self.cellInfo(self.field[x, y])
            self.screen.drawPixel(x + offset.x, y + offset.y, char, color)

    def drawInfoBars(self):
        stat = self.stat
        self.screen[0, 0].print(f"Cells: {stat['cellsTotal']}/{self.field.size**2}").whip()
        self.screen[0, 1].print(f"Bombs left: {stat['bombsMarked']}/{self.field.bombs}").whip()
        self.screen[0, 2].print('[debug]', stat).whip()

    def move(self, direct):
        if self.field.inBounds(self.pos + direct):
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
        self.screen[offset, Color.lime].print('Congrats!').whip()

    def gameover(self, offset):
        offset = Coord(offset)
        self.screen[0, 0, Color.red].print('You have lost!').whip()

        for x, y in self.field:
            if self.field[x, y] == Value.bomb:
                self.field[x, y] = Mask.opened
                char, color = self.cellInfo(self.field[x, y])
                self.screen.drawPixel(x + offset.x, y + offset.y, char, color)
        self.screen[offset + self.field.size]
