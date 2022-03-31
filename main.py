#!/usr/bin/env python
from sys import argv
from gui.app import App as GUIAPP
from cli.app import App as CLIAPP

app = None
if len(argv) == 2 and argv[1] == '--cli':
    app = CLIAPP()
else:
    app = GUIAPP()

app.mainloop()
