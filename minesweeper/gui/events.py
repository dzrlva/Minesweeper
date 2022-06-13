"""Hacky way to introduce event data in tkinter."""

from minesweeper.util import dotdict
from functools import partial
import inspect


class EventMaster:
    """Make tkinter virtual event more usfull."""

    def __init__(self, root):
        """Replace tkinter bind/event_generate with better version."""
        self.eventCounter = 0
        self.events = {}

        self.tkBind = root.bind
        self.tkEventGenerate = root.event_generate
        root.bind = self.bindWrap
        root.event_generate = self.dispatchEvent

    def virtEventWrap(self, callback, event):
        """Parse EventMaster's event data."""
        callback(self.getEvent(event))

    def bindWrap(self, name, callback):
        """Replace original bind function."""
        if name.startswith("<<") and name.endswith(">>"):
            return self.tkBind(name, partial(self.virtEventWrap, callback))
        else:
            return self.tkBind(name, callback)

    def getEvent(self, tkEvent):
        """Parse virtual event for EventMaster data."""
        eventId = tkEvent.x
        if eventId not in self.events:
            return tkEvent

        eventHash = tkEvent.y
        eventData = self.events[eventId]
        if hash(eventData) != eventHash:
            return tkEvent
        del self.events[eventId]
        return eventData

    def dispatchEvent(self, name, **kwargs):
        """Replace original event_generate in order to add data."""
        if "data" not in kwargs:
            self.tkEventGenerate(name, **kwargs)
        else:
            eventId = self.eventCounter
            eventData = dotdict()
            for k in ["data", "x", "y"]:
                if k in kwargs:
                    eventData[k] = kwargs[k]
                    del kwargs[k]

            eventData.name = name
            stack = inspect.stack()[1]
            if stack[0].f_locals and "self" in stack[0].f_locals:
                eventData.target = stack[0].f_locals["self"]
            eventData.caller = stack[3]

            self.events[eventId] = eventData
            self.tkEventGenerate(name, x=eventId, y=hash(eventData))
            self.eventCounter += 1
