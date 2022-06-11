import tkinter as tk
from tkinter import messagebox
from functools import partial
from .colors import COLORS
from gui import styles

TITLE_FONT_SIZE = 20
LABEL_FONT_SIZE = 13
OPTION_FONT_SIZE = 13
BUTTON_FONT_SIZE = 13
CTRL_BTN_GAP = 5
CTRL_BTN_MARGIN_BOTTOM = 80


class MainMenu:
    def __init__(self, app):
        self.app = app

        btnHeight = 2
        btnWidth = 40

        self.buttonsConfig = ([
            { 'text': 'New Game',
              'command': partial(self.switchEvent, 'NewGameMenu') },
            # { 'text': 'Statistics',
              # 'command': partial(self.switchEvent, 'StatMenu') },
            { 'text': 'Settings',
              'command': partial(self.switchEvent, 'SettingsMenu') },
            { 'text': 'Quit',
              'command': app.destroy },
        ])

        self.buttons = []
        for buttonConfig in self.buttonsConfig:
            self.buttons.append(tk.Button(
                width=btnWidth, height=btnHeight,
                **buttonConfig, font=app.font,
                **styles.PUSH_BTTON_STYLE(),
            ))

        self.title = tk.Label(
            text="Minesweeper", font=app.font,
            **styles.COMMON_STYLE()
        )

        self.pack()

    def pack(self):
        self.title.pack(side="top", fill="x", pady=50, padx=50)
        for button in self.buttons:
            button.pack(pady=5)

    def destroy(self):
        self.title.destroy()
        for button in self.buttons:
            button.destroy()

    def switchEvent(self, place):
        self.app.event_generate('<<Switch-Menu>>', data=place)


class NewGameMenu:
    def __init__(self, app, username=''):
        self.app = app

        labelFont = (app.font[0], LABEL_FONT_SIZE)
        optionFont = (app.font[0], OPTION_FONT_SIZE)
        btnFont = (app.font[0], BUTTON_FONT_SIZE)

        self.title = tk.Label(
            app, text='New game', font=app.font,
            **styles.COMMON_STYLE()
        )
        self.frame = tk.Frame(app, bg=COLORS['main'])

        # self.plInpTitle = tk.Label(
            # self.frame, text='Player name', font=labelFont,
            # **styles.COMMON_STYLE()
        # )
        # self.plInp = tk.Entry(self.frame)
        # self.plInp.insert(0, username)

        self.fieldSizes = {
            'tiny': 8,
            'small': 12,
            'medium': 14,
            'big': 16,
            'large': 20,
            'giant': 22
        }

        self.curFieldSize = tk.StringVar(self.frame, self.app.gameOpts['fieldsize-name'])
        self.fsInpTitle = tk.Label(
            self.frame,  text='Field size', font=labelFont,
            **styles.COMMON_STYLE()
        )
        self.fsInpMenu = tk.OptionMenu(
            self.frame, self.curFieldSize, *list(self.fieldSizes.keys()),
        )
        self.fsInpMenu.config(width=10, **styles.PUSH_BTTON_STYLE())

        self.difTitle = tk.Label(
            self.frame, text="Difficulty", font=optionFont,
            **styles.COMMON_STYLE()
        )
        self.difficulties = [
            ('easy', '0.1'),
            ('medium', '0.3'),
            ('hard', '0.5'),
            ('extra hard', '0.8')
        ]

        self.curDif = tk.StringVar(self.frame, str(self.app.gameOpts['difficulty']))
        self.difButtons = []
        for difficulty, value in self.difficulties:
            button = tk.Radiobutton(
                self.frame, text=difficulty, font=optionFont,
                variable=self.curDif, value=value,
                **styles.RADIO_BUTTON_STYLE(),
            )
            self.difButtons.append(button)

        self.btnFrame = tk.Frame(app, bg=COLORS['main'])
        self.startBtn = tk.Button(
            self.btnFrame, text='Start', font=btnFont,
            width=20, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onStartClick
        )
        self.backBtn = tk.Button(
            self.btnFrame, text='Back', font=btnFont,
            width=20, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onBackClick
        )

        self.pack()

    def pack(self):
        self.title.pack(side="top", fill="x", padx=20, pady=38)

        # self.plInpTitle.grid(row=0, column=0, padx=20)
        # self.plInp.grid(row=0, column=1)

        self.fsInpTitle.grid(row=1, column=0)
        self.fsInpMenu.grid(row=1, column=1, sticky='E', pady=10)

        self.difTitle.grid(row=2, column=0, padx=10, columnspan=1)
        for i, difButton in enumerate(self.difButtons):
            difButton.grid(row=i + 2, column=0, padx=(90, 0), columnspan=2, sticky='w')

        self.startBtn.grid(row=0, column=0, pady=CTRL_BTN_GAP)
        self.backBtn.grid(row=1, column=0)

        self.frame.pack()
        self.btnFrame.pack(side=tk.BOTTOM, pady=CTRL_BTN_MARGIN_BOTTOM)

    def destroy(self):
        self.title.destroy()
        self.frame.destroy()
        self.btnFrame.destroy()

    def onStartClick(self):
        self.app.event_generate('<<Start-Game>>', data={
            # 'username': self.plInp.get(),
            'difficulty': float(self.curDif.get()),
            'fieldsize': self.fieldSizes[self.curFieldSize.get()],
            'fieldsize-name': self.curFieldSize.get(),
        })

    def onBackClick(self):
        self.app.event_generate('<<Switch-Menu>>', data='MainMenu')


class StatisticsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="STATISTICS", font=("Purisa", 20)).pack(side="top", fill="x", pady=100)
        listbox = tk.Frame(self)
        buttons = tk.Frame(self)
        loadgamelb = tk.Listbox(listbox, width=60, height=6)
        loadgamelb.insert(1, "<  player1: Empty  >")
        scrollbar = tk.Scrollbar(listbox, orient="vertical", command=loadgamelb.yview)
        scrollbar.pack(side="right", fill= "y")
        loadgamelb.config(yscrollcommand=scrollbar.set)
        loadgamelb.pack()
        tk.Button(buttons, text="Quit",font=("Purisa", 13), width=35, height=3,
                  command=lambda: master.switch_frame(MainMenu)).pack(side="top", fill="y", pady=100, padx=100)

        listbox.pack(side="top")
        buttons.pack(side="top")


class SettingsMenu:
    def __init__(self, app):
        self.app = app
        labelFont = (app.font[0], 15)
        optionFont = (app.font[0], 12)

        self.title = tk.Label(
            text="Settings", font=app.font, pady=10,
            **styles.COMMON_STYLE(),
        )
        self.frame = tk.Frame(app, bg=COLORS['main'])

        self.langOptions = ['English', 'Russian']
        self.langTitle = tk.Label(
            self.frame, text='Language', font=labelFont,
            **styles.COMMON_STYLE(),
        )
        self.curLang = tk.StringVar(self.frame, self.langOptions[0])
        self.langMenu = tk.OptionMenu(
            self.frame, self.curLang, *self.langOptions,
            command=self.onLangChange
        )
        self.langMenu.config(width=10, **styles.PUSH_BTTON_STYLE())

        self.colorSchemes = { 'light': 'light', 'dark': 'dark' }
        self.csTitle = tk.Label(
            self.frame, text='Colorscheme', font=labelFont,
            **styles.COMMON_STYLE(),
        )
        self.curCS = tk.StringVar(self.frame, app.appOpts['colorscheme'])

        self.csButtons = []
        for name, csid in self.colorSchemes.items():
            self.csButtons.append(tk.Radiobutton(
                self.frame, text=name, font=optionFont,
                variable=self.curCS, value=csid,
                **styles.RADIO_BUTTON_STYLE(),
                command=self.onThemeChange
            ))

        self.btnFrame = tk.Frame(bg=COLORS['main'])
        self.applyBtn = tk.Button(
            self.btnFrame, text='Apply', font=optionFont,
            width=20, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onApplyClick
        )
        self.backBtn = tk.Button(
            self.btnFrame, text='Back', font=optionFont,
            width=20, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onBackClick
        )

        self.applyBtn['state'] = 'disabled'
        self.pack()

    def pack(self):
        self.title.pack(pady=20)

        self.langTitle.grid(row=0, column=0, pady=20)
        self.langMenu.grid(row=0, column=1, columnspan=2, sticky='E')

        self.csTitle.grid(row=1, column=0, padx=10)
        for i, button in enumerate(self.csButtons):
            button.grid(row=1, column=i + 1, ipadx=10)

        self.applyBtn.grid(row=0, column=0, pady=CTRL_BTN_GAP)
        self.backBtn.grid(row=1, column=0)

        self.frame.pack()
        self.btnFrame.pack(side=tk.BOTTOM, pady=CTRL_BTN_MARGIN_BOTTOM)

    def destroy(self):
        self.title.destroy()
        self.frame.destroy()
        self.btnFrame.destroy()

    def reloadTheme(self):
        self.title.configure(**styles.COMMON_STYLE())
        self.langTitle.configure(**styles.COMMON_STYLE())
        self.csTitle.configure(**styles.COMMON_STYLE())
        self.frame.configure(bg=COLORS['main'])
        self.btnFrame.configure(bg=COLORS['main'])
        for button in self.csButtons:
            button.configure(**styles.RADIO_BUTTON_STYLE())
        self.langMenu.configure(**styles.PUSH_BTTON_STYLE())
        self.applyBtn.configure(**styles.PUSH_BTTON_STYLE())
        self.backBtn.configure(**styles.PUSH_BTTON_STYLE())

    def onApplyClick(self):
        self.applyBtn['state'] = 'disabled'
        self.app.event_generate('<<Save-Settings>>', data={
            'colorscheme': self.curCS.get(),
            'language': self.curLang.get()
        })
        self.reloadTheme()

    def onBackClick(self):
        self.app.event_generate('<<Switch-Menu>>', data='MainMenu')

    def onLangChange(self, option):
        self.applyBtn['state'] = 'normal'

    def onThemeChange(self):
        self.applyBtn['state'] = 'normal'
