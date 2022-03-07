from random import randint

size = 20
bombsPercent = .3


def randCoord(size):
    return randint(0, size - 1), randint(0, size - 1)

class Field:
    OUTOFBOUND = -1
    BOMB = 9

    @staticmethod
    def isBomb(data):
        return data == Field.BOMB

    def __init__(self, size, bombsPercent):
        self.size = size
        self.field = [ [ 0 for _ in range(size) ] for _ in range(size) ]
        self.bombs = round(size * size * bombsPercent)
        self.__randomizeBombs()
        self.__calcFieldBombs()

    def __isOutOfBounds(self, row, column):
        if row < 0    or row >= self.size:    return True
        if column < 0 or column >= self.size: return True
        return False

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

field = Field(size, bombsPercent)

for row in field.field:
    for cell in row:
        if Field.isBomb(cell): print('*', end='')
        elif cell: print(cell, end='')
        else: print(' ', end='')
    print()
