import tkinter as tk
from tkinter import messagebox
from functools import partial
#from util import loadImage


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


class ButtonArray():
    def __init__(self, buttons):
        self.buttons = []
        for button in buttons:
            self.buttons.append(tk.Button(**button))

    def pack(self):
        for button in self.buttons:
            button.pack()

    def destroy(self):
        for button in self.buttons:
            button.destroy()


class MainMenu():
    def __init__(self, app):
        self.app = app

        btnHeight = 2
        btnWidth = 40

        self.buttons = ButtonArray([
            { 'text': 'New Game',
              'width': btnWidth,
              'height': btnHeight,
              'command': partial(self.switchEvent, 'NewGameMenu') },
            { 'text': 'Statistics',
              'width': btnWidth,
              'height': btnHeight,
              'command': partial(self.switchEvent, 'StatMenu') },
            { 'text': 'Settings',
              'width': btnWidth,
              'height': btnHeight,
              'command': partial(self.switchEvent, 'SettingsMenu') },
            { 'text': 'Quit',
              'width': btnWidth,
              'height': btnHeight,
              'command': app.destroy },
        ])

        self.label = tk.Label(text="Minesweeper")

        self.label.pack(side="top", fill="x", pady=50, padx=50)
        self.buttons.pack()

    def destroy(self):
        self.label.destroy()
        self.buttons.destroy()

    def switchEvent(self, place):
        self.app.event_generate('<<Switch-Menu>>', data=place)


class NewGameFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #center = tk.Frame(self, borderwidth=0, relief="ridge")
        tk.Label(self, text="New game", font=("Purisa", 20)).pack(side="top", fill="x", padx=20, pady=38)
        tk.Label(self, text="Player name", font=("Purisa", 15)).pack(side="top", fill="x")
        e1 = tk.Entry(self)
        e1.pack(side="top", fill="x", padx=20, pady=10)
        tk.Label(self,  text="Field scale", font=("Purisa", 15)).pack(side="top", fill="x")
        resoptions = ["640x480", "800x600", "960x720"]
        resvar = tk.StringVar(self, master)
        resvar.set(resoptions[0])
        resmenu = tk.OptionMenu(self, resvar, *resoptions, command=lambda: master.getData())
        resmenu.pack(side="top", fill="x", pady=10)


        tk.Label(self, text="Difficulty", font=("Purisa", 15)).pack(side="top", fill="x", padx=10)
        MODES = [("easy", "1"),
                 ("medium", "2"),
                 ("hard", "3")]
        vs = tk.StringVar()
        vs.set("1")
        for text, mode in MODES:
            tk.Radiobutton(self, text=text, font=("Purisa", 13), variable=vs, value=mode).pack(side="top", fill="y",
                                                                                               padx=10)

        tk.Button(self, text="Start", font=("Purisa", 13), width=25, height=2,
                  command=lambda: master.switch_frame(MainMenu)).pack(side="top", fill="y", padx=30, pady=15)
        tk.Button(self, text="Cancel", font=("Purisa", 13), width=25, height=2,
                  command=lambda: master.switch_frame(MainMenu)).pack(side="top", fill="y", padx=30, pady=5)



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

