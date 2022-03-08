from blessed import Terminal
from field import Field
from minepoint import MinePoint, Value, Mask, Flag


def printCell(cell):
    if cell == Value.bomb:    color, char = BOMB, '*'
    elif cell == Value.empty: color, char = term.normal, ' '
    else: color, char = colors[cell.value], str(cell)
    print(color + char + term.normal, end='')


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

field = Field(20, .1)
print(f'Field size: {field.size}x{field.size}')
print('Bombs:', field.bombs)

print('Field:')
for x in range(field.size):
    for y in range(field.size):
        printCell(field[x, y])
    print()

revCoord = (field.size // 2, field.size // 2)
print(f'Revealed at (0, 0):', not field.reveal(0, 0))
print(f'Revealed at {revCoord}:', not field.reveal(revCoord[0], revCoord[1]))
for x in range(field.size):
    for y in range(field.size):
        print(field[x, y].mask if field[x, y].mask != Mask.closed else ' ', end='')
    print()

print('Field with mask:')
for x in range(field.size):
    for y in range(field.size):
        if field[x, y] == Mask.closed: print('?', end='')
        else: printCell(field[x, y])
    print()

