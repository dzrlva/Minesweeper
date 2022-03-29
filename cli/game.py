from blessed import Terminal
from .screen import Screen, Color
from util.minepoint import Flag, Mask, Value
from util.coord import Coord
from logic.field import Field


VALUECOLORS = [ 0, 38, 73, 40, 136, 172, 202, 161, 124, 9 ]


def cellInfo(cell):
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


term = Terminal()
screen = Screen()
field = Field(10, .1)
cursor = Coord(0, 0)
cursorColor = Color(239, bg=True)

with term.cbreak(), term.hidden_cursor():
    screen.clear()
    key = ''

    while key != 'q':
        cellsOpened = 0
        allBombsCorrect = True
        bombsMarked = 0

        for x, y in field:
            screen.drawPixel(x, y + 3, *cellInfo(field[x, y]))
            if field[x, y] == Flag.sure or field[x, y] == Mask.opened:
                cellsOpened += 1
            if field[x, y] == Flag.sure:
                bombsMarked += 1
            if field[x, y] != Value.bomb and field[x, y] == Flag.sure:
                allBombsCorrect = False
        char, color = cellInfo(field[cursor])
        screen.drawPixel(cursor.x, cursor.y + 3, char, color + cursorColor)

        screen[0, 0].print(f'[Progress] | Cells: {cellsOpened}/{field.size**2}').whip()
        screen[0, 1].print(f'[Progress] Bombs left: {bombsMarked}/{field.bombs}').whip()
        screen[0, 2].print(f'[debug] {allBombsCorrect}').whip()

        if cellsOpened == field.size**2 and allBombsCorrect:
            screen[0, 0, Color.lime].print('Congrats!').whip()[0, field.size + 3]
            break

        key = term.inkey(timeout=3)
        if not key:
            continue
        if key.is_sequence:
            key = key.name

        if key == 'w':
            cursor.y = max(0, cursor.y - 1)
        elif key == 's':
            cursor.y = min(field.size - 1, cursor.y + 1)
        elif key == 'a':
            cursor.x = max(0, cursor.x - 1)
        elif key == 'd':
            cursor.x = min(field.size - 1, cursor.x + 1)
        elif key == 'f' or key == 'e':
            if field[cursor] == Mask.closed:
                field.cycleFlag(cursor)
        elif key == ' ' and field[cursor] != Flag.sure:
            if field.reveal(cursor):
                screen[0, 0, Color(32)].print('You lost').whip()

                sleepTime = 2.0 / field.bombs
                for x, y in field:
                    if field[x, y] == Value.bomb:
                        field[x, y] = Mask.opened
                        screen.drawPixel(x, y + 3, *cellInfo(field[x, y]))
                        if term.inkey(timeout=sleepTime) == 'q':
                            break
                        sleepTime = max(0, sleepTime - .001)
                screen[field.size + 3]
                break
