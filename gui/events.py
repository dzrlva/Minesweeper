import tkinter as tk
from util import dotdict
from time import time
from functools import partial
import inspect


class EventMaster:
    def __init__(self, root):
        self.eventCounter = 0
        self.events = {}

        self.tkBind = root.bind
        self.tkEventGenerate = root.event_generate
        root.bind = self.bindWrap
        root.event_generate = self.dispatchEvent

    def virtEventWrap(self, callback, event):
        callback(self.getEvent(event))

    def bindWrap(self, name, callback):
        if name.startswith('<<') and name.endswith('>>'):
            return self.tkBind(name, partial(self.virtEventWrap, callback))
        else:
            return self.tkBind(name, callback)

    def getEvent(self, tkEvent):
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
        if 'data' not in kwargs:
            self.tkEventGenerate(name, **kwargs)
        else:
            eventId = self.eventCounter
            eventData = dotdict()
            for k in ['data', 'x', 'y']:
                if k in kwargs:
                    eventData[k] = kwargs[k]
                    del kwargs[k]

            eventData.name = name
            stack = inspect.stack()[1]
            if stack[0].f_locals and 'self' in stack[0].f_locals:
                eventData.target = stack[0].f_locals['self']
            eventData.caller = stack[3]

            self.events[eventId] = eventData
            self.tkEventGenerate(name, x=eventId, y=hash(eventData))
            self.eventCounter += 1
