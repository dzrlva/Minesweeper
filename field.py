from random import randint
from minepoint import MinePoint, Value, Mask, Flag

def randCoord(size):
    return randint(0, size - 1), randint(0, size - 1)

class Field:
    OUTOFBOUND = -1

    def __init__(self, size, bombsPercent):
        self.size = size
        self.__field = [ [ MinePoint() for _ in range(size) ] for _ in range(size) ]
        self.bombs = round(size * size * bombsPercent)
        self.__randomizeBombs()
        self.__calcFieldBombs()

    def __isOutOfBounds(self, x, y):
        if x < 0 or x >= self.size: return True
        if y < 0 or y >= self.size: return True
        return False

    def __getitem__(self, coords):
        x, y = coords
        if self.__isOutOfBounds(x, y):
            return Field.OUTOFBOUND
        return self.__field[x][y]

    def __setitem__(self, coords, value):
        x, y = coords
        if self.__isOutOfBounds(x, y):
            raise ValueError(f'Coords {coords} are out of bounds')
        self.__field[x][y].set(value)

    def __randomizeBombs(self):
        for _ in range(self.bombs):
            x, y = randCoord(self.size)
            while self[x, y] == Value.bomb:
                x, y = randCoord(self.size)
            self[x, y] = Value.bomb

    def __calcFieldBombs(self):
        for x in range(self.size):
            for y in range(self.size):
                if self[x, y] == Value.bomb: continue
                bombsAround = 0
                for biasX in range(-1, 2):
                    for biasY in range(-1, 2):
                        if biasX == 0 and biasY == 0: continue
                        bombsAround += (self[x + biasX, y + biasY] == Value.bomb)
                self[x, y] = Value(bombsAround)

    #returns False is point was revealed without any problems; and True if there was a bomb
    def reveal(self, x, y):
        if self[x, y] == Value.bomb:  return True
        if self[x, y] == Mask.opened: return False

        stack = [ (x, y) ]
        while len(stack):
            x, y = stack.pop()
            self[x, y] = Mask.opened
            for biasX in range(-1, 2):
                for biasY in range(-1, 2):
                    cx, cy = x + biasX, y + biasY
                    if self[cx, cy] != Mask.closed: continue

                    if self[cx, cy] == Value.empty:
                        self[cx, cy] = Mask.pending
                        stack.append((cx, cy))
                    elif self[cx, cy] != Value.bomb:
                        self[cx, cy] = Mask.opened
        return False
