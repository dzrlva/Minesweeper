#!/usr/bin/env python

"""Handle game statistics."""


class Stat:
    """Statistics about current game."""

    gametime = 0
    win = 0


def printstat():
    """Add new statistics in file and print summary statistics."""
    s = str(Stat.gametime) + ' ' + str(Stat.win) + '\n'
    with open("stat.txt", 'a') as f:
        f.write(s)
    with open("stat.txt", 'r') as f:
        st = f.read().splitlines()
    st = [i.split(' ') for i in st]
    bestwintime = -1
    meanwintime = 0
    gamewin = 0
    for i in st:
        gamewin += int(i[1])
        if i[1] == '1':
            meanwintime += float(i[0])
            if bestwintime == -1 or bestwintime > float(i[0]):
                bestwintime = float(i[0])
    winpercent = round(gamewin / len(st) * 100)
    meanwintime /= gamewin
    print(f"""\nTime: {Stat.gametime} sec
Best win time: {bestwintime} sec
Games played: {len(st)}
Games wined: {gamewin}
Wins percent: {winpercent}%
Mean win time: {meanwintime} sec""")
