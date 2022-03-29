#!/usr/bin/env python

"""Handle game statistics."""

import pickle


class Stat:
    """Statistics about current game."""

    gametime = 0
    win = 0
    statfile = ""


def stat_menu():
    """Add new statistics in file and print summary statistics."""
    with open(Stat.statfile, "rb") as f:
        st = pickle.load(f)
    st.append([Stat.gametime, Stat.win])
    with open(Stat.statfile, "wb") as f:
        pickle.dump(st, f)
    bestwintime = -1
    meanwintime = 0
    gamewin = 0
    for i in st:
        gamewin += i[1]
        if i[1] == 1:
            meanwintime += i[0]
            if bestwintime == -1 or bestwintime > i[0]:
                bestwintime = i[0]
    winpercent = round(gamewin / len(st) * 100)
    meanwintime = meanwintime / gamewin if gamewin else 0
    print(
        f"""\nTime: {Stat.gametime} sec
Best win time: {bestwintime if bestwintime > 0 else '-'} sec
Games played: {len(st)}
Games wined: {gamewin}
Wins percent: {winpercent}%
Mean win time: {meanwintime if meanwintime > 0 else '-'} sec """
    )
