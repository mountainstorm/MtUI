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


from View import View


class Control(View):
    def __init__(self):
        View.__init__(self)
        self._state = Control.STATE_NORMAL
        self._attrs = {}
        for k, v in ControlState:
            self._attrs[k] = None
        self._actions = {}

    # Setting and Getting Control state
    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    # Overridden Responder handlers
    def mouse_enter(self, event):
        if self.state() != Control.STATE_DISABLED:
            self.set_state(Control.STATE_HIGHLIGHTED)

    def mouse_leave(self, event):
        if self.state() != Control.STATE_DISABLED
            self.set_state(Control.STATE_NORMAL)

    def mouse_press(self, event):
        if event.button == Event.MOUSE_BUTTON_1:
            if self.state() != Control.STATE_DISABLED:
                self.set_state(Control.STATE_SELECTED)

    def mouse_release(self, event):
        if event.button == Event.MOUSE_BUTTON_1:
            if self.state() != Control.STATE_DISABLED:
                self.set_state(Control.STATE_NORMAL)


# Control state defines
Control.STATE_NORMAL      = 0
Control.STATE_HIGHLIGHTED = 1 << 0
Control.STATE_DISABLED    = 1 << 1
Control.STATE_SELECTED    = 1 << 2
Control.STATE_APPLICATION = 0x00FF0000
Control.STATE_RESERVED    = 0xFF000000
