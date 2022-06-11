"""Module that uses logic.Field, draws board, handles user input."""

import tkinter as tk
import tkinter.ttk as ttk
from util.point import Point
from util.coord import Coord
from .board import Board
from logic.field import Field
from .colors import COLORS
from util.minepoint import Value, Mask, Flag
from time import sleep
from threading import Timer
from gui import styles


class GameControls:
    def __init__(self, app, canvas):
        self.app = app
        self.canvas = canvas

        self.frame = tk.Frame(app, bg=COLORS['main'])
        self.resetBtn = tk.Button(
            self.frame, text='Reset',
            width=10, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onResetClick
        )
        self.backBtn = tk.Button(
            self.frame, text='Back',
            width=10, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onBackButton
        )

    def pack(self):
        self.resetBtn.grid(row=0, column=0, padx=10)
        self.backBtn.grid(row=0, column=1)
        # self.frame.pack()
        self.frame.pack(anchor='w', expand=True, padx=(20, 20))

    def destroy(self):
        self.frame.destroy()

    def onResetClick(self):
        self.app.event_generate('<<Reset-Game>>')

    def onBackButton(self):
        self.app.event_generate('<<Switch-Menu>>', data='NewGameMenu')


class Game:
    def __init__(self, app, size, difficulty, *, maxBombStack=8):
        self.app = app
        self.maxBombStack = maxBombStack
        if maxBombStack <= 0 or maxBombStack >= 12:
            raise ValueError('Maximum bomb stack should not allow impossible bombs!')

        self.canvas = tk.Canvas(
            self.app, bg=COLORS['main'],
            borderwidth=0, highlightthickness=0,
            width=app.width, height=app.height * .9,
        )
        self.canvas.pack(expand='no', fill='both')
        self.app.canvas = self.canvas

        self.size = size
        self.difficulty = difficulty
        self.board = None
        self.resetGame()

        self.ctrls = GameControls(app, self.canvas)
        self.ctrls.pack()

        self.statLabel = self.canvas.create_text(
            10, 60, anchor='nw',
            fill=COLORS['text'], text=f'Bombs left: {self.field.size - self.barriers}',
            state='disabled', font=(self.app.font[0], 10)
        )
        self.updateStat()

        self.label = self.canvas.create_text(
            10, 10, anchor='nw',
            fill=COLORS['text'], text='Minesweeper',
            state='disabled', font=(self.app.font[0], 20)
        )

        self.lmbBind = self.app.bind('<Button-1>', self.onLeftClick)
        self.rmbBind = self.app.bind('<Button-3>', self.onRightClick)
        self.rmbBind2 = self.app.bind("<Button-2>", self.onRightClick)
        self.rgBind = self.app.bind('<<Reset-Game>>', self.resetGame)

    def resetGame(self, event=None):
        self.marked = 0
        self.markedRight = 0
        self.opened = 0
        self.status = 'game'

        if self.board:
            self.board.destroy()
        self.board = Board(self.app, self.size, width=1, height=.9)
        self.field = Field(self.board.rows, self.board.cols, self.difficulty, kind='hexagon')
        self.board.draw()
        self.updateField()
        self.updateBoard()
        self.updateField()

    def destroy(self):
        self.app.unbind('<Button-1>', self.lmbBind)
        self.app.unbind('<Button-3>', self.rmbBind)
        self.app.unbind('<Button-2>', self.rmbBind2)
        self.app.unbind('<<Reset-Game>>', self.rgBind)
        self.board.destroy()
        self.canvas.delete(self.label)
        self.canvas.delete(self.statLabel)
        self.canvas.destroy()
        self.ctrls.destroy()
        self.app.canvas = None
        self.app = None

    def updateField(self):
        """Set barrier around playble area and remove impossible bombs"""
        for pos, cell in self.board.board.items():
            if cell is None:
                self.field[pos] = Value.barrier

        for crd in self.field:
            if self.field[crd] != Value.bomb:
                continue
            curBombStack = 0
            for bias in self.field.pattern(crd):
                curCrd = crd + bias
                if curCrd == crd:
                    continue
                if self.field[curCrd] == Value.bomb:
                    curBombStack += 2
                elif self.field[curCrd] == Value.barrier:
                    curBombStack += 1
                if curBombStack >= self.maxBombStack:
                    self.field[crd] = Value.empty
                    break

        self.field.recalculate()
        self.barriers = 0
        for crd in self.field:
            self.barriers += self.field[crd] == Value.barrier

    def updateBoard(self):
        for x, y in self.field:
            if self.field[x, y] == Mask.opened:
                text = None
                if self.field[x, y] == Value.barrier:
                    color = COLORS['main']
                elif self.field[x, y] == Value.bomb:
                    color, text = COLORS['cells.bomb'], 'BOMB'
                elif self.field[x, y] == Value.empty:
                    color = COLORS['cells.empty']
                else:
                    text = str(self.field[x, y].value)
                    color = COLORS['cells'][text]
                self.board.openCell(Point(x, y), color, text)

    def completeGame(self):
        for i, pos in enumerate(self.field):
            self.field[pos] = Mask.opened
        self.updateBoard()

        if self.status == 'lose':
            tk.messagebox.showinfo(title='Result', message='You Lose!\nTry better next time! ⚇')
        else:
            tk.messagebox.showinfo(title='Result', message='You won! Nice ☺')
            # if self.field[pos] == Value.bomb:
                # self.board.drawExplosion(pos)

        self.board.disable()
        # self.app.event_generate("<<Game-Complete>>", data=self.status)

    def gameOver(self, pos):
        if self.status == 'lose':
            return
        self.status = 'lose'
        print('Bro, you died')
        self.board.drawExplosion(pos, callback=self.completeGame)
        # self.completeGame()

    def gameWin(self):
        self.status = 'win'
        print('BRO, YOU WON')
        self.completeGame()

    def checkWin(self):
        if self.marked != self.markedRight:
            return False
        if self.opened + self.marked == self.field.size - self.barriers:
            return True
        return False

    def updateStat(self):
        left = self.field.size - self.barriers - self.opened - self.marked
        self.canvas.itemconfigure(self.statLabel, text=f'Bombs left: {left}')

    def onRightClick(self, event):
        if self.status != 'game':
            return

        pos = Coord(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)

        if pos is None or self.field[pos] == Mask.opened:
            return

        self.board.toggleFlag(pos)
        self.field.toggleFlag(pos)
        if self.field[pos] == Flag.sure:
            self.marked += 1
            self.markedRight += self.field[pos] == Value.bomb
        else:
            self.marked -= 1
            self.markedRight -= self.field[pos] == Value.bomb

        if self.checkWin():
            self.gameWin()
        self.updateStat()

    def onLeftClick(self, event):
        if self.status != 'game':
            return

        pos = Coord(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)
        if pos is None or self.field[pos] == Flag.sure:
            return

        revealed = self.field.reveal(pos)
        if revealed is None:
            self.field[pos] = Mask.opened
            self.gameOver(pos)
        elif len(revealed) > 0:
            self.opened += len(revealed)
            if self.checkWin():
                self.gameWin()
        self.updateBoard()
        self.updateStat()
        # clicked.openCell(COLORS['inactive'], text='I')
