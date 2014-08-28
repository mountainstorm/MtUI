#!/usr/bin/python
# coding: utf-8

# Copyright (c) 2014 Mountainstorm
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import time
from copy import copy


class Event(object):
    def __init__(self, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        self.timestamp = timestamp

    def dispatch_event(self, responder):
        raise TypeError(u'Unable to dispatch base event type')


class KeyEvent(Event):
    pass # helper to make it easy to check where to send it


class MouseEvent(Event):
    def __init__(self, view=None, timestamp=None):
        Event.__init__(self, timestamp)
        self.view = view


class KeyPressEvent(KeyEvent):
    def __init__(self, symbol, modifiers, timestamp=None):
        KeyEvent.__init__(self, timestamp)
        self.symbol = symbol
        self.modifiers = modifiers

    def dispatch_event(self, responder):
        responder.key_press(self)


class KeyReleaseEvent(KeyEvent):
    def __init__(self, symbol, modifiers, timestamp=None):
        KeyEvent.__init__(self, timestamp)
        self.symbol = symbol
        self.modifiers = modifiers

    def dispatch_event(self, responder):
        responder.key_release(self)


class TextEvent(KeyEvent):
    def __init__(self, text, timestamp=None):
        KeyEvent.__init__(self, timestamp)
        self.text = text

    def dispatch_event(self, responder):
        responder.text(self)


class TextMotionEvent(KeyEvent):
    def __init__(self, motion, timestamp=None):
        KeyEvent.__init__(self, timestamp)
        self.motion = motion

    def dispatch_event(self, responder):
        responder.text_motion(self)


class TextMotionSelectEvent(KeyEvent):
    def __init__(self, motion, timestamp=None):
        KeyEvent.__init__(self, timestamp)
        self.motion = motion

    def dispatch_event(self, responder):
        responder.text_motion_select(self)


class MouseDragEvent(MouseEvent):
    def __init__(self, origin, delta, buttons, modifiers, view, timestamp=None):
        MouseEvent.__init__(self, view, timestamp)
        self.origin = copy(origin)
        self.delta = copy(delta)
        self.buttons = buttons
        self.modifiers = modifiers

    def dispatch_event(self, responder):
        responder.mouse_drag(self)


class MouseEnterEvent(MouseEvent):
    def __init__(self, view, timestamp=None):
        MouseEvent.__init__(self, view, timestamp)

    def dispatch_event(self, responder):
        responder.mouse_enter(self)


class MouseLeaveEvent(MouseEvent):
    def __init__(self, view, timestamp=None):
        MouseEvent.__init__(self, view, timestamp)

    def dispatch_event(self, responder):
        responder.mouse_leave(self)


class MouseMotionEvent(MouseEvent):
    def __init__(self, origin, delta, view, timestamp=None):
        MouseEvent.__init__(self, view, timestamp)
        self.origin = copy(origin)
        self.delta = copy(delta)

    def dispatch_event(self, responder):
        responder.mouse_motion(self)


class MousePressEvent(MouseEvent):
    def __init__(self, origin, buttons, modifiers, view, timestamp=None):
        MouseEvent.__init__(self, view, timestamp)
        self.origin = copy(origin)
        self.buttons = buttons
        self.modifiers = modifiers

    def dispatch_event(self, responder):
        responder.mouse_press(self)


class MouseReleaseEvent(MouseEvent):
    def __init__(self, origin, buttons, modifiers, view, timestamp=None):
        MouseEvent.__init__(self, view, timestamp)
        self.origin = copy(origin)
        self.buttons = buttons
        self.modifiers = modifiers

    def dispatch_event(self, responder):
        responder.mouse_release(self)


class MouseScrollEvent(MouseEvent):
    def __init__(self, origin, delta, view, timestamp=None):
        MouseEvent.__init__(self, view, timestamp)
        self.origin = copy(origin)
        self.delta = copy(delta)

    def dispatch_event(self, responder):
        responder.mouse_scroll(self)


# class MouseEnterWindowEvent(MouseEvent):
#     def __init__(self, origin, view, timestamp=None):
#         MouseEvent.__init__(self, view, timestamp)
#         self.origin = copy(origin)

#     def dispatch_event(self, responder):
#         responder.mouse_enter_window(self)


# class MouseLeaveWindowEvent(MouseEvent):
#     def __init__(self, origin, view, timestamp=None):
#         MouseEvent.__init__(self, view, timestamp)
#         self.origin = copy(origin)

#     def dispatch_event(self, responder):
#         responder.mouse_leave_window(self)

