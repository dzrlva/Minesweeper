import tkinter as tk
from tkinter import messagebox
from functools import partial


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.switch_frame(MainMenu)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def show_info(static):
        messagebox.showinfo("Info", "please, choose one of possible options")

    def saved_info(self, master):
        messagebox.showinfo("Saved", "SETTINGS SAVED!")
        master.switch_frame(MainMenu)

    def quit(self):
        self.destroy()


class MainMenu:
    def __init__(self, app):
        self.app = app

        btnHeight = 2
        btnWidth = 40

        self.buttonsConfig = ([
            { 'text': 'New Game',
              'command': partial(self.switchEvent, 'NewGameMenu') },
            { 'text': 'Statistics',
              'command': partial(self.switchEvent, 'StatMenu') },
            { 'text': 'Settings',
              'command': partial(self.switchEvent, 'SettingsMenu') },
            { 'text': 'Quit',
              'command': app.destroy },
        ])

        self.buttons = []
        for buttonConfig in self.buttonsConfig:
            self.buttons.append(tk.Button(
                width=btnWidth, height=btnHeight,
                **buttonConfig, font=app.font
            ))

        self.title = tk.Label(text="Minesweeper", font=app.font)

        self.pack()

    def pack(self):
        self.title.pack(side="top", fill="x", pady=50, padx=50)
        for button in self.buttons:
            button.pack()

    def destroy(self):
        self.title.destroy()
        for button in self.buttons:
            button.destroy()

    def switchEvent(self, place):
        self.app.event_generate('<<Switch-Menu>>', data=place)


class NewGameMenu:
    def __init__(self, app, username=''):
        self.app = app
        self.labelFont = (app.font[0], 13)
        self.optionFont = (app.font[0], 10)
        self.buttonFont = (app.font[0], 13)

        self.title = tk.Label(app, text='New game', font=app.font)
        self.frame = tk.Frame(app)

        self.plInpTitle = tk.Label(self.frame, text='Player name', font=self.labelFont)
        self.plInp = tk.Entry(self.frame)
        self.plInp.insert(0, username)

        self.fieldSizes = {
            'tiny': 8,
            'small': 12,
            'medium': 14,
            'big': 16,
            'large': 20,
            'giant': 22
        }
        self.curFieldSize = tk.StringVar(self.frame, list(self.fieldSizes.keys())[0])
        self.fsInpTitle = tk.Label(self.frame,  text='Field size', font=self.labelFont)
        self.fsInpMenu = tk.OptionMenu(
            self.frame, self.curFieldSize, *list(self.fieldSizes.keys()),
        )
        self.fsInpMenu.config(width=10)

        self.difTitle = tk.Label(self.frame, text="Difficulty", font=self.optionFont)
        self.difficulties = [
            ('easy', '0.1'),
            ('medium', '0.2'),
            ('hard', '0.3'),
            ('extra hard', '0.4')
        ]

        self.curDif = tk.StringVar(self.frame, self.difficulties[0][1])
        self.difButtons = []
        for difficulty, value in self.difficulties:
            button = tk.Radiobutton(
                self.frame, text=difficulty, font=self.optionFont,
                variable=self.curDif, value=value,
            )
            self.difButtons.append(button)

        self.startBtn = tk.Button(
            app, text='Start', font=self.optionFont,
            width=20, height=1,
            command=self.onStartClick
        )
        self.backBtn = tk.Button(
            app, text='Back', font=self.optionFont,
            width=20, height=1,
            command=self.onBackClick
        )

        self.pack()

    def pack(self):
        self.title.pack(side="top", fill="x", padx=20, pady=38)

        self.plInpTitle.grid(row=0, column=0, padx=20)
        self.plInp.grid(row=0, column=1)

        self.fsInpTitle.grid(row=1, column=0)
        self.fsInpMenu.grid(row=1, column=1, sticky='E')

        self.difTitle.grid(row=2, column=0, padx=10, pady=(10, 5), columnspan=2)
        for i, difButton in enumerate(self.difButtons):
            difButton.grid(row=i + 3, column=0, padx=(90, 0), columnspan=2, sticky='w')

        self.frame.pack()

        self.startBtn.pack(side="top", fill="y", padx=30, pady=(15, 5))
        self.backBtn.pack(side="top", fill="y", padx=30, pady=5)

    def destroy(self):
        self.title.destroy()
        self.frame.destroy()
        self.startBtn.destroy()
        self.backBtn.destroy()

    def onStartClick(self):
        self.app.event_generate('<<Start-Game>>', data={
            'username': self.plInp.get(),
            'difficulty': float(self.curDif.get()),
            'fieldsize': self.fieldSizes[self.curFieldSize.get()],
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


class SettingsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        center = tk.Frame(self, borderwidth=0, relief="ridge")
        bottom = tk.Frame(self, borderwidth=0, relief="solid")
        header = tk.Frame(self, borderwidth=0, relief="ridge")
        tk.Label(bottom, text="\n\n")
        tk.Label(header, text="Settings", font=("Purisa", 23)).pack(side="top", fill="both", pady=50)
        tk.Label(center, text="Language", font=("Purisa", 16)).pack(side="top", fill="x", pady=10, padx=100)
        resoptions= ["English", "Russian"]
        resvar = tk.StringVar(master)
        resvar.set(resoptions_left[0])
        resmenu = tk.OptionMenu(center, resvar, *resoptions, command=lambda: master.getData())
        resmenu.pack(side="top", fill="x", pady=20)

        tk.Label(center, text="Colorscheme", font=("Purisa", 16)).pack(side="top", fill="x", pady=10)
        MODES = [("dark", "1"),
                 ("light", "2")]
        vs = tk.StringVar()
        vs.set("1")
        for text, mode in MODES:
            tk.Radiobutton(center, text=text, font=("Purisa", 13), variable=vs, value=mode).pack(side="left", fill="x", padx=50, pady=20)
        b1 = tk.Button(bottom, text="SAVE", font=("Purisa", 10), width=25, height=2,
                    command=lambda: master.saved_info(master.switch_frame(MainMenu)))
        b2 = tk.Button(bottom, text="CANCEL", font=("Purisa", 10), width=25, height=2,
                    command=lambda: master.switch_frame(MainMenu))

        b1.pack(side="bottom", padx=20, pady=10)
        b2.pack(side="bottom", padx=20, pady=20)

        header.grid(row=1, column=3)
        bottom.grid(row=5, column=3)
        center.grid(row=2, column=3)


if __name__ == "__main__":
    app = SampleApp()
    app.resvar = '800x600'
    app.geometry(app.resvar)
    app.resizable(0, 0)
    app.mainloop()
