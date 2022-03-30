#!/usr/bin/env python

from cli.game import Game
from cli.screen import Screen
from cli.color import Color
from logic.field import Field
from logic.gamestat import Stat
from blessed import Terminal
import time


field = Field(30, 20, 0.15)
term = Terminal()
screen = Screen()
game = Game(field)


username = 'Gamer1'
# tempname = input(f'Input another name if you are not {username}: ')
# if tempname:
    # username = tempname

stat = Stat()
stat.assignFile(username)
stat.readStatistic()

with term.cbreak(), term.hidden_cursor():
    screen.clear()
    game.draw()
    starttime = time.time()
    key = ''

    while key != "q" and game.status == 'active':
        key = term.inkey(timeout=3)
        if not key:
            continue

        game.keyAction(key)
        game.draw()

    stat['win'] = game.status == 'win'

stat['gametime'] = round(time.time() - starttime, 1)
stat.saveStatistic()
screen.setCursor(0, field.height + 6).setColor(Color.reset)
stat.print()
