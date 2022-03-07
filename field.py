from random import randint
from blessed import Terminal


def randCoord(size):
    return randint(0, size - 1), randint(0, size - 1)

class Field:
    OUTOFBOUND = -1
    BOMB = 9
    CLOSED = 0
    OPEN = 1
    PENDING = 2

    @staticmethod
    def isBomb(data):
        return data == Field.BOMB

    def __init__(self, size, bombsPercent):
        self.size = size
        self.field = [ [ 0 for _ in range(size) ] for _ in range(size) ]
        self.mask  = [ [ Field.CLOSED for _ in range(size) ] for _ in range(size) ]
        self.bombs = round(size * size * bombsPercent)
        self.__randomizeBombs()
        self.__calcFieldBombs()

    def __isOutOfBounds(self, row, column):
        if row < 0    or row >= self.size:    return True
        if column < 0 or column >= self.size: return True
        return False

    def __call__(self, row, column):
        if self.__isOutOfBounds(row, column):
            return Field.OUTOFBOUND
        return self.mask[row][column]

    #fix missunderstandint row/column and x/y args!!!
    def __getitem__(self, coords):
        row, column = coords
        if self.__isOutOfBounds(row, column):
            return Field.OUTOFBOUND
        return self.field[row][column]

    def __setitem__(self, coords, value):
        row, column = coords
        if self.__isOutOfBounds(row, column):
            raise ValueError('Out of bound coordinates')
        self.field[row][column] = value

    def __randomizeBombs(self):
        for i in range(self.bombs):
            x, y = randCoord(self.size)
            while Field.isBomb(self[x, y]):
                x, y = randCoord(self.size)
            self.field[x][y] = Field.BOMB

    def __calcFieldBombs(self):
        for i in range(self.size):
            for j in range(self.size):
                if Field.isBomb(self[i, j]): continue
                bombsAround = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0: continue
                        bombsAround += Field.isBomb(self[i + y, j + x])
                self[i, j] = bombsAround

    def __maskOpen(self, x, y):
        self.mask[x][y] = Field.OPEN

    def __maskPending(self, x, y):
        self.mask[x][y] = Field.PENDING

    def reveal(self, x, y):
        if Field.isBomb(self[x, y]): return True

        stack = [ (x, y) ]
        while len(stack):
            x, y = stack.pop()
            self.__maskOpen(x, y)
            for biasX in range(-1, 2):
                for biasY in range(-1, 2):
                    cx, cy = x + biasX, y + biasY
                    if self(cx, cy) == Field.CLOSED:
                        if self[cx, cy] == 0:
                            self.__maskPending(cx, cy)
                            stack.append((cx, cy))
                        elif not Field.isBomb(self[cx, cy]):
                            self.__maskOpen(cx, cy)

        return False


term = Terminal()
ONE   = term.color(38)
TWO   = term.color(73)
THREE = term.color(40)
FOUR  = term.color(136)
FIVE  = term.color(172)
SIX   = term.color(202)
SEVEN = term.color(161)
EIGHT = term.color(124)
BOMB  = term.color(9)
colors = [ term.normal, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, BOMB ]

field = Field(10, .1)
print(f'Field size: {field.size}x{field.size}')
print('Bombs:', field.bombs)

def printCell(cell):
    symb = ''
    if Field.isBomb(cell): symb = BOMB + '*'
    elif cell == 0: symb = term.normal + ' '
    else: symb = colors[cell] + str(cell)
    print(symb + term.normal, end='')

print('Field:')
for row in field.field:
    for cell in row:
        printCell(cell)
    print()

revCoord = (field.size // 2, field.size // 2)
print(f'Revealed at {revCoord}:', not field.reveal(revCoord[0], revCoord[1]))
for row in field.mask:
    for cell in row:
        print(cell if cell else ' ', end='')
    print()

print('Field with mask:')
for x in range(field.size):
    for y in range(field.size):
        if field(x, y) == Field.CLOSED: print('?', end='')
        else: printCell(field[x, y])
    print()
