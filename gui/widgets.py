import tkinter as tk


class ButtonArray():
    def __init__(self, buttons, font):
        self.buttons = []
        for button in buttons:
            self.buttons.append(tk.Button(**button, font=font))

    def pack(self, **kwargs):
        for button in self.buttons:
            button.pack(**kwargs)

    def destroy(self):
        for button in self.buttons:
            button.destroy()


class LabeledInput:
    def __init__(self, app, label):
        self.app = app
        self.title = tk.Label(text=label, font=app.font)
        self.input = tk.Entry()

    def pack(self, **kwargs):
        self.title.pack(**kwargs)
        if 'pady' in kwargs:
            kwargs['pady'] -= 38
        self.input.pack(**kwargs)

    def destroy(self):
        self.title.destroy()
