import tkinter as tk
from tkinter import messagebox

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


class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Minesweeper", font=("Purisa", 20)).pack(side="top", fill="x", pady=50, padx=50)
        tk.Button(self, text="NEW GAME", font=("Purisa", 13), width=40, height=3,
                  command=lambda: master.switch_frame(NewGameFrame)).pack()
        tk.Button(self, text="STATISTICS", font=("Purisa", 13), width=40, height=3,
                  command=lambda: master.switch_frame(StatisticsFrame)).pack()
        tk.Button(self, text='SETTINGS', font=("Purisa", 13), width=40, height=3,
                  command=lambda: master.switch_frame(SettingsFrame)).pack()
        tk.Button(self, text="QUIT", font=("Purisa", 13), width=40, height=3,
                  command=lambda: master.quit()).pack()
        tk.Button(self, text="HELP", font=("Purisa", 13), width=40, height=2,
                  command=lambda: master.show_info()).pack(pady=20)


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
        #center.grid(row=2, column=3)



class StatisticsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="STATISTICS", font=("Purisa", 20)).pack(side="top", fill="x", pady=100)
        listbox = tk.Frame(self)
        buttons = tk.Frame(self)
        loadgamelb = tk.Listbox(listbox, width=60, height=6)
        loadgamelb.insert(1, "<  player1: Empty  >")
        loadgamelb.insert(2, "<  player2: Empty  >")
        loadgamelb.insert(3, "<  player3: Empty  >")
        loadgamelb.insert(4, "<  player4: Empty  >")
        loadgamelb.insert(5, "<  player5: Empty  >")
        loadgamelb.insert(6, "<  player6: Empty  >")
        loadgamelb.insert(7, "<  player7: Empty  >")
        loadgamelb.insert(8, "<  player8: Empty  >")
        loadgamelb.insert(9, "<  player9: Empty  >")
        loadgamelb.insert(10, "<  player10: Empty  >")
        loadgamelb.insert(11, "<  player11: Empty  >")
        loadgamelb.insert(12, "<  player12: Empty  >")
        scrollbar = tk.Scrollbar(listbox, orient="vertical", command=loadgamelb.yview)
        scrollbar.pack(side="right", fill= "y")
        loadgamelb.config(yscrollcommand=scrollbar.set)
        loadgamelb.pack()
        #tk.Button(buttons, text="CONINUE GAME", state="disabled",
        #          command=lambda: master.switch_fame(MainMenu)).pack()
        tk.Button(buttons, text="CANCEL",font=("Purisa", 13), width=35, height=3,
                  command=lambda: master.switch_frame(MainMenu)).pack(side="top", fill="y", pady=100, padx=100)

        listbox.pack(side="top")
        buttons.pack(side="top")


class SettingsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        center = tk.Frame(self, borderwidth=0, relief="ridge")
        left = tk.Frame(self, borderwidth=0, relief="ridge")
        right = tk.Frame(self, borderwidth=0, relief="ridge")
        bottom = tk.Frame(self, borderwidth=0, relief="solid")
        header = tk.Frame(self, borderwidth=0, relief="ridge")
        tk.Label(bottom, text="\n\n")
        tk.Label(header, text="Settings", font=("Purisa", 23)).pack(side="top", fill="both", pady=50)
        #tk.Label(left, text="Game settings", font=("Purisa", 15)).pack(side="top", fill="x", pady=0)
        tk.Label(center, text="Language", font=("Purisa", 16)).pack(side="top", fill="x", pady=10, padx=100)
        resoptions_left = ["English", "Russian"]
        resvar_left = tk.StringVar(master)
        resvar_left.set(resoptions_left[0])
        resmenu_left = tk.OptionMenu(center, resvar_left, *resoptions_left, command=lambda: master.getData())
        resmenu_left.pack(side="top", fill="x", pady=20)

        tk.Label(center, text="Colorscheme", font=("Purisa", 16)).pack(side="top", fill="x", pady=10)
        MODES = [("dark", "1"),
                 ("light", "2")]
        vs = tk.StringVar()
        vs.set("1")
        for text, mode in MODES:
            tk.Radiobutton(center, text=text, font=("Purisa", 13), variable=vs, value=mode).pack(side="left", fill="x", padx=50, pady=20)
        #b1 = tk.Button(center, text="SAVE", font=("Purisa", 10), width=10, height=1,
        #            command=lambda: master.saved_info(master.switch_frame(MainMenu)))
        #b3 = tk.Button(bottom, text="HELP", font=("Purisa", 10), width=25, height=2,
        #               command=lambda: master.show_info())
        b2 = tk.Button(bottom, text="CANCEL", font=("Purisa", 10), width=25, height=2,
                    command=lambda: master.switch_frame(MainMenu))


        #b1.pack(side="bottom", padx=20)
        b2.pack(side="bottom", padx=20, pady=20)
        #b3.pack(side="bottom", padx=20, pady=10)

        header.grid(row=1, column=3)
        left.grid(row=2, column=2)
        right.grid(row=2, column=4)
        bottom.grid(row=5, column=3)
        center.grid(row=2, column=3)




if __name__ == "__main__":

    app = SampleApp()
    app.resvar = '800x600'
    app.geometry(app.resvar)
    app.resizable(0, 0)
    app.mainloop()

