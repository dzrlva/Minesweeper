"""Module that uses logic.Field, draws board, handles user input."""

import tkinter as tk
from tkinter import messagebox
from minesweeper.util.point import Point
from minesweeper.util.coord import Coord
from .board import Board
from minesweeper.logic.field import Field
from .colors import COLORS
from minesweeper.util.minepoint import Value, Mask, Flag
from . import styles
from random import shuffle
from minesweeper.translation import _


class GameControls:
    """Additional controls for game window."""

    def __init__(self, app, canvas):
        """Create controls button."""
        self.app = app
        self.canvas = canvas

        self.frame = tk.Frame(app, bg=COLORS["main"])
        self.resetBtn = tk.Button(
            self.frame,
            text=_("Reset"),
            width=10,
            height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onResetClick,
        )
        self.backBtn = tk.Button(
            self.frame,
            text=_("Back"),
            width=10,
            height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onBackButton,
        )
        self.helpBtn = tk.Button(
            self.frame,
            text=_("Help"),
            width=10,
            height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onHelpButton,
        )

    def pack(self):
        """Show control button."""
        self.resetBtn.grid(row=0, column=0, padx=(0, 10))
        self.backBtn.grid(row=0, column=1, padx=(0, 10))
        self.helpBtn.grid(row=0, column=2)
        # self.frame.pack()
        self.frame.pack(anchor="w", expand=True, padx=(20, 20))

    def destroy(self):
        """Remove control buttons."""
        self.frame.destroy()

    def onResetClick(self):
        """Reset game with event."""
        self.app.event_generate("<<Reset-Game>>")

    def onBackButton(self):
        """Return to preview menu."""
        self.app.event_generate("<<Switch-Menu>>", data="NewGameMenu")

    def onHelpButton(self):
        """Return to preview menu."""
        self.app.event_generate("<<Game-Help>>")

    def enableHelp(self):
        """Enable help button."""
        self.helpBtn["state"] = "normal"

    def disableHelp(self):
        """Disable help button."""
        self.helpBtn["state"] = "disabled"


class Game:
    """Class to paly hexagonal Minesweeper."""

    def __init__(self, app, size, difficulty, *, maxBombStack=8):
        """Create game with given size and difficulty."""
        self.app = app
        self.maxBombStack = maxBombStack
        if maxBombStack <= 0 or maxBombStack >= 12:
            raise ValueError("Maximum bomb stack should not allow impossible bombs!")

        self.canvas = tk.Canvas(
            self.app,
            bg=COLORS["main"],
            borderwidth=0,
            highlightthickness=0,
            width=app.width,
            height=app.height * 0.9,
        )
        self.canvas.pack(expand="no", fill="both")
        self.app.canvas = self.canvas

        self.size = size
        self.difficulty = difficulty
        self.board = None

        self.ctrls = GameControls(app, self.canvas)
        self.ctrls.pack()

        self.statLabel = self.canvas.create_text(
            10,
            60,
            anchor="nw",
            fill=COLORS["text"],
            text="",
            state="disabled",
            font=(self.app.font[0], 10),
        )

        self.label = self.canvas.create_text(
            10,
            10,
            anchor="nw",
            fill=COLORS["text"],
            text="Minesweeper",
            state="disabled",
            font=(self.app.font[0], 20),
        )
        self.resetGame()

        self.lmbBind = self.app.bind("<Button-1>", self.onLeftClick)
        self.rmbBind = self.app.bind("<Button-3>", self.onRightClick)
        self.rmbBind2 = self.app.bind("<Button-2>", self.onRightClick)
        self.rgBind = self.app.bind("<<Reset-Game>>", self.resetGame)
        self.helpBind = self.app.bind("<<Game-Help>>", self.helpPlayer)

    def resetGame(self, event=None):
        """Create new game."""
        self.marked = 0
        self.markedRight = 0
        self.opened = 0
        self.status = "game"
        self.ctrls.enableHelp()

        if self.board:
            self.board.destroy()
        self.board = Board(self.app, self.size, width=1, height=0.9)
        self.field = Field(
            self.board.rows, self.board.cols, self.difficulty, kind="hexagon"
        )
        self.board.draw()
        self.updateField()
        self.updateBoard()
        self.helps = int(len(self.field.bombsPos) * (1 - self.difficulty) / 2)
        if self.helps == 0:
            self.ctrls.disableHelp()
        self.updateStat()

    def destroy(self):
        """Remove all game's objects."""
        self.app.unbind("<Button-1>", self.lmbBind)
        self.app.unbind("<Button-3>", self.rmbBind)
        self.app.unbind("<Button-2>", self.rmbBind2)
        self.app.unbind("<<Reset-Game>>", self.rgBind)
        self.app.unbind("<<Game-help>>", self.helpBind)
        self.board.destroy()
        self.canvas.delete(self.label)
        self.canvas.delete(self.statLabel)
        self.canvas.destroy()
        self.ctrls.destroy()
        self.app.canvas = None
        self.app = None

    def updateField(self):
        """Set barrier around playble area and remove impossible bombs."""
        cells = []
        for pos, cell in self.board.board.items():
            if cell is None:
                self.field[pos] = Value.barrier
            else:
                cells.append(pos)
        shuffle(cells)

        bombs = list(self.field.bombsPos)
        shuffle(bombs)
        for crd in bombs:  # self.field:
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
        """Draw opened cell of the board."""
        for x, y in self.field:
            if self.field[x, y] == Mask.opened:
                text = None
                if self.field[x, y] == Value.barrier:
                    color = COLORS["main"]
                elif self.field[x, y] == Value.bomb:
                    color, text = COLORS["cells.bomb"], "BOMB"
                elif self.field[x, y] == Value.empty:
                    color = COLORS["cells.empty"]
                else:
                    text = str(self.field[x, y].value)
                    color = COLORS["cells"][text]
                self.board.openCell(Point(x, y), color, text)

    def completeGame(self):
        """Disable board and display message."""
        for i, pos in enumerate(self.field):
            self.field[pos] = Mask.opened
        self.updateBoard()

        if self.status == "lose":
            messagebox.showinfo(
                title="Result", message=_("You Lose!\nTry better next time! ⚇")
            )
        else:
            messagebox.showinfo(title="Result", message=_("You won! Nice ☺"))

        self.ctrls.disableHelp()
        self.board.disable()

    def gameOver(self, pos):
        """Set result on lose."""
        if self.status == "lose":
            return
        self.status = "lose"
        # print('Bro, you died')
        self.board.drawExplosion(pos, callback=self.completeGame)
        # self.completeGame()

    def gameWin(self):
        """Set result on win."""
        self.status = "win"
        # print('BRO, YOU WON')
        self.completeGame()

    def checkWin(self):
        """Check if player completed game."""
        if self.marked != self.markedRight:
            return False
        if self.opened + self.marked == self.field.size - self.barriers:
            return True
        return False

    def updateStat(self):
        """Update amount of left to open cells."""
        stat = {
            _("Cell left"): self.field.size - self.barriers - self.opened - self.marked,
            _("Bombs left"): len(self.field.bombsPos) - self.marked,
            _("Helps"): max(0, self.helps),
        }
        self.canvas.itemconfigure(
            self.statLabel, text="\n".join([f"{k}: {v}" for k, v in stat.items()])
        )

    def helpPlayer(self, event):
        """Provide player with some help."""
        bombs, found, fallback = list(self.field.bombsPos), False, None
        shuffle(bombs)
        for pos in bombs:
            if self.field[pos] != Flag.sure:
                fallback = pos
                for bias in self.field.pattern(pos):
                    curPos = pos + bias
                    if self.field[curPos] == Mask.opened:
                        found = True
                        break
                if found:
                    break
        if not found and fallback is not None:
            pos = fallback
        if self.field[pos] != Flag.sure:
            self.helps -= 1
            self.toggleFlag(pos)
            if self.helps - 1 < 0:
                self.ctrls.disableHelp()

    def toggleFlag(self, pos):
        """Toggle flag on given position."""
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

    def onRightClick(self, event):
        """Reaction to right click (place/remove flag)."""
        if self.status != "game":
            return

        pos = Coord(event.x, event.y, dtype=float)
        pos = self.board.findClicked(pos)

        if pos is None or self.field[pos] == Mask.opened:
            return
        self.toggleFlag(pos)

    def onLeftClick(self, event):
        """Open cell."""
        if self.status != "game":
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
