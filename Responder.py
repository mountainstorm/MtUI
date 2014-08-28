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


class Responder(object):
    def __init__(self):
        self._first_responder = False

    # Managing the Responder Chain
    def next_responder(self):
        return None

    def is_first_responder(self):
        return self._first_responder

    def can_become_first_responder(self):
        return False

    def become_first_responder(self):
        self._first_responder = True

    def can_resign_first_responder(self):
        return True

    def resign_first_responder(self):
        self._first_responder = False

    # Events
    def key_press(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.key_press(event)

    def key_release(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.key_release(event)

    def mouse_drag(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.mouse_drag(event)

    def mouse_enter(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.mouse_enter(event)

    def mouse_leave(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.mouse_leave(event)

    def mouse_motion(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.mouse_motion(event)

    def mouse_press(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.mouse_press(event)

    def mouse_release(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.mouse_release(event)

    def mouse_scroll(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.mouse_scroll(event)

    # def mouse_enter_window(self, event):
    #     responder = self.next_responder()
    #     if responder is not None:
    #         responder.mouse_enter_window(event)     

    # def mouse_leave_window(self, event):
    #     responder = self.next_responder()
    #     if responder is not None:
    #         responder.mouse_leave_window(event)

    def text(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.text(event)

    def text_motion(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.text_motion(event)

    def text_motion_select(self, event):
        responder = self.next_responder()
        if responder is not None:
            responder.text_motion_select(event)

