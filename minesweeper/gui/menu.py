"""Different Menus for gui app."""

import tkinter as tk
from functools import partial
from .colors import COLORS
from . import styles
from minesweeper.translation import _

TITLE_FONT_SIZE = 20
LABEL_FONT_SIZE = 13
OPTION_FONT_SIZE = 13
BUTTON_FONT_SIZE = 13
CTRL_BTN_GAP = 5
CTRL_BTN_MARGIN_BOTTOM = 80


class MainMenu:
    """Main menu of GUI app."""

    def __init__(self, app):
        """Create and display main menu."""
        self.app = app

        btnHeight = 2
        btnWidth = 40

        self.buttonsConfig = ([
            { 'text': _('New Game'),
              'command': partial(self.switchEvent, 'NewGameMenu') },
            { 'text': _('Settings'),
              'command': partial(self.switchEvent, 'SettingsMenu') },
            { 'text': _('Quit'),
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
            text='Minesweeper', font=app.font,
            **styles.COMMON_STYLE()
        )

        self.pack()

    def pack(self):
        """Show menu."""
        self.title.pack(side="top", fill="x", pady=50, padx=50)
        for button in self.buttons:
            button.pack(pady=5)

    def destroy(self):
        """Destroy all menu objects."""
        self.title.destroy()
        for button in self.buttons:
            button.destroy()

    def switchEvent(self, place):
        """Generate event on button press."""
        self.app.event_generate('<<Switch-Menu>>', data=place)


class NewGameMenu:
    """New game menu settings."""

    def __init__(self, app, username=''):
        """Create new game menu and show it."""
        self.app = app

        labelFont = (app.font[0], LABEL_FONT_SIZE)
        optionFont = (app.font[0], OPTION_FONT_SIZE)
        btnFont = (app.font[0], BUTTON_FONT_SIZE)

        self.title = tk.Label(
            app, text=_('New game'), font=app.font,
            **styles.COMMON_STYLE()
        )
        self.frame = tk.Frame(app, bg=COLORS['main'])

        # self.plInpTitle = tk.Label(
        #    self.frame, text='Player name', font=labelFont,
        #    **styles.COMMON_STYLE()
        # )
        # self.plInp = tk.Entry(self.frame)
        # self.plInp.insert(0, username)

        self.fieldSizes = {
            _('tiny'): 6,
            _('small'): 8,
            _('medium'): 12,
            _('big'): 16,
            _('large'): 20,
            _('extra large'): 24,
            _('giant'): 28,
            _('enormous'): 32
        }

        setFS = self.app.gameOpts['fieldsize-name']
        if setFS == 0:
            setFS = next(iter(self.fieldSizes))

        self.curFieldSize = tk.StringVar(self.frame, setFS)
        self.fsInpTitle = tk.Label(
            self.frame,  text=_('Field size'), font=labelFont,
            **styles.COMMON_STYLE()
        )
        self.fsInpMenu = tk.OptionMenu(
            self.frame, self.curFieldSize, *list(self.fieldSizes.keys()),
        )
        self.fsInpMenu.config(width=10, **styles.PUSH_BTTON_STYLE())
        self.fsInpMenu['menu'].config(**styles.OPTION_MENU_STYLE())

        self.difTitle = tk.Label(
            self.frame, text=_('Difficulty'), font=optionFont,
            **styles.COMMON_STYLE()
        )
        self.difficulties = [
            (_('easy'), '0.1'),
            (_('medium'), '0.2'),
            (_('hard'), '0.3'),
            (_('extra hard'), '0.4'),
            (_('impossible'), '0.7')
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
            self.btnFrame, text=_('Start'), font=btnFont,
            width=20, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onStartClick
        )
        self.backBtn = tk.Button(
            self.btnFrame, text=_('Back'), font=btnFont,
            width=20, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onBackClick
        )

        self.pack()

    def pack(self):
        """Draw menu."""
        self.title.pack(side="top", fill="x", padx=20, pady=38)

        # self.plInpTitle.grid(row=0, column=0, padx=20)
        # self.plInp.grid(row=0, column=1)

        self.fsInpTitle.grid(row=1, column=0, sticky='w')
        self.fsInpMenu.grid(row=1, column=1, sticky='E', pady=10)

        self.difTitle.grid(row=2, column=0, padx=(0, 10), columnspan=1, sticky='w')
        for i, difButton in enumerate(self.difButtons):
            difButton.grid(row=i + 2, column=0, padx=(100, 0), columnspan=2, sticky='w')

        self.startBtn.grid(row=0, column=0, pady=CTRL_BTN_GAP)
        self.backBtn.grid(row=1, column=0)

        self.frame.pack()
        self.btnFrame.pack(side=tk.BOTTOM, pady=CTRL_BTN_MARGIN_BOTTOM)

    def destroy(self):
        """Remove all menu objects."""
        self.title.destroy()
        self.frame.destroy()
        self.btnFrame.destroy()

    def onStartClick(self):
        """Generate start game event on 'Start' button press."""
        self.app.event_generate('<<Start-Game>>', data={
            # 'username': self.plInp.get(),
            'difficulty': float(self.curDif.get()),
            'fieldsize': self.fieldSizes[self.curFieldSize.get()],
            'fieldsize-name': self.curFieldSize.get(),
        })

    def onBackClick(self):
        """Generate event to return back."""
        self.app.event_generate('<<Switch-Menu>>', data='MainMenu')


class SettingsMenu:
    """Menu to configure app settings."""

    def __init__(self, app):
        """Create and show settings menu."""
        self.app = app
        labelFont = (app.font[0], 15)
        optionFont = (app.font[0], 12)

        self.title = tk.Label(
            text=_('Settings'), font=app.font, pady=10,
            **styles.COMMON_STYLE(),
        )
        self.frame = tk.Frame(app, bg=COLORS['main'])

        self.resOptions = ['700x600', '800x700', '1000x900', '1000x600', '1200x1000']
        self.resLabel = tk.Label(
            self.frame, text=_('Resolution'), font=labelFont,
            **styles.COMMON_STYLE(),
        )
        self.curRes = tk.StringVar(self.frame, app.appOpts['resolution'])
        self.resMenu = tk.OptionMenu(
            self.frame, self.curRes, *self.resOptions,
            command=self.onResChange
        )
        self.resMenu.config(width=10, **styles.PUSH_BTTON_STYLE())
        self.resMenu['menu'].config(**styles.OPTION_MENU_STYLE())
        if app.appOpts['fullscreen'] == 'True':
            self.resMenu['state'] = 'disabled'

        self.fsVar = tk.StringVar(self.frame, '1' if app.appOpts['fullscreen'] == 'True' else '0')
        self.fsLabel = tk.Label(
            self.frame, font=labelFont,
            text=_('Fullscreen'),
            **styles.COMMON_STYLE()
        )
        self.fsBtn = tk.Checkbutton(
            self.frame, font=labelFont,
            width=2, height=1, variable=self.fsVar,
            command=self.onFullscreenChange,
            **styles.RADIO_BUTTON_STYLE()
        )

        self.langOptions = ['English', 'Russian']
        self.langTitle = tk.Label(
            self.frame, text=_('Language'), font=labelFont,
            **styles.COMMON_STYLE(),
        )
        self.curLang = tk.StringVar(self.frame, app.appOpts['language'])
        self.langMenu = tk.OptionMenu(
            self.frame, self.curLang, *self.langOptions,
            command=self.onLangChange
        )
        self.langMenu.config(width=10, **styles.PUSH_BTTON_STYLE())
        self.langMenu['menu'].config(**styles.OPTION_MENU_STYLE())

        self.colorSchemes = { theme: theme for theme in COLORS.getThemeNames() }
        self.csTitle = tk.Label(
            self.frame, text=_('Colorscheme'), font=labelFont,
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
            self.btnFrame, text=_('Apply'), font=optionFont,
            width=20, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onApplyClick
        )
        self.backBtn = tk.Button(
            self.btnFrame, text=_('Back'), font=optionFont,
            width=20, height=1,
            **styles.PUSH_BTTON_STYLE(),
            command=self.onBackClick
        )

        self.applyBtn['state'] = 'disabled'
        self.pack()

    def pack(self):
        """Draw settings menu."""
        self.title.pack(pady=20)

        self.langTitle.grid(row=0, column=0, pady=20, sticky='W')
        self.langMenu.grid(row=0, column=1, columnspan=2, sticky='E')

        self.resLabel.grid(row=1, column=0, pady=(0, 20), sticky='W')
        self.resMenu.grid(row=1, column=1, columnspan=2, sticky='E')

        self.fsLabel.grid(row=2, column=0, pady=(0, 20), sticky='W')
        self.fsBtn.grid(row=2, column=1, pady=(0, 10), sticky='W')

        self.csTitle.grid(row=3, column=0, padx=(0, 10), sticky='W')
        for i, button in enumerate(self.csButtons):
            button.grid(row=3, column=i + 1, ipadx=10)

        self.applyBtn.grid(row=0, column=0, pady=CTRL_BTN_GAP)
        self.backBtn.grid(row=1, column=0)

        self.frame.pack()
        self.btnFrame.pack(side=tk.BOTTOM, pady=CTRL_BTN_MARGIN_BOTTOM)

    def destroy(self):
        """Destroy settings menu."""
        self.title.destroy()
        self.frame.destroy()
        self.btnFrame.destroy()

    def reloadLang(self):
        self.title.config(text=_('Settings'))
        self.resLabel.config(text=_('Resolution'))
        self.fsLabel.config(text=_('Fullscreen'))
        self.langTitle.config(text=_('Language'))
        self.csTitle.config(text=_('Colorscheme'))
        self.applyBtn.config(text=_('Apply'))
        self.backBtn.config(text=_('Back'))

    def reloadTheme(self):
        """Reload settings menu theme right now."""
        self.title.configure(**styles.COMMON_STYLE())
        self.resLabel.configure(**styles.COMMON_STYLE())
        self.fsLabel.configure(**styles.COMMON_STYLE())
        self.langTitle.configure(**styles.COMMON_STYLE())
        self.csTitle.configure(**styles.COMMON_STYLE())
        self.frame.configure(bg=COLORS['main'])
        self.btnFrame.configure(bg=COLORS['main'])
        for button in self.csButtons:
            button.configure(**styles.RADIO_BUTTON_STYLE())
        self.fsBtn.configure(**styles.RADIO_BUTTON_STYLE())
        self.resMenu.configure(**styles.PUSH_BTTON_STYLE())
        self.resMenu['menu'].config(**styles.OPTION_MENU_STYLE())
        self.langMenu.configure(**styles.PUSH_BTTON_STYLE())
        self.langMenu['menu'].config(**styles.OPTION_MENU_STYLE())
        self.applyBtn.configure(**styles.PUSH_BTTON_STYLE())
        self.backBtn.configure(**styles.PUSH_BTTON_STYLE())

    def onApplyClick(self):
        """Set settings."""
        self.applyBtn['state'] = 'disabled'
        self.app.event_generate('<<Save-Settings>>', data={
            'resolution': self.curRes.get(),
            'colorscheme': self.curCS.get(),
            'language': self.curLang.get(),
            'fullscreen': 'True' if self.fsVar.get() == '1' else 'False'
        })
        self.reloadTheme()
        self.reloadLang()

    def onBackClick(self):
        """Return back to main menu event."""
        self.app.event_generate('<<Switch-Menu>>', data='MainMenu')

    def onFullscreenChange(self):
        """Change fullscreen."""
        self.applyBtn['state'] = 'normal'
        if self.fsVar.get() == '1':
            self.resMenu['state'] = 'disabled'
            screenWidth = self.app.winfo_screenwidth()
            screenHeight = self.app.winfo_screenheight()
            self.curRes.set(f'{screenWidth}x{screenHeight}')
        else:
            self.resMenu['state'] = 'normal'
            self.curRes.set(self.resOptions[0])

    def onResChange(self, option):
        """Change resolution."""
        self.applyBtn['state'] = 'normal'

    def onLangChange(self, option):
        """Change language."""
        self.applyBtn['state'] = 'normal'

    def onThemeChange(self):
        """Change theme."""
        self.applyBtn['state'] = 'normal'
