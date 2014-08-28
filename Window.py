#!/usr/bin/python
# coding: utf-8

# Copyright (c) 2013 Mountainstorm
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


from Geometry import *
from View import View
from Responder import Responder
from Event import *
from Application import Application
from pyglet.gl import *
import pyglet


class PygletWindow(pyglet.window.Window):
    def __init__(self, window, style, resizable, width=None, height=None):
        pyglet.window.Window.__init__(self, 
                                      style=style, 
                                      resizable=resizable, 
                                      width=width, 
                                      height=height)
        self._window = window

    def on_activate(self):
        Application.shared_application()._bring_window_to_front(self._window)

    def on_deactivate(self):
        pass

    def on_close(self):
        self._window.remove_from_application()

    def on_draw(self):
        self.clear()
        self._window.set_needs_display()
        self._window.display_if_needed()

    def on_expose(self):
        pass

    def on_hide(self):
        pass

    def on_key_press(self, symbol, modifiers):
        Application.shared_application().post_event(KeyPressEvent(symbol, modifiers))

    def on_key_release(self, symbol, modifiers):
        Application.shared_application().post_event(KeyReleaseEvent(symbol, modifiers))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        origin = Point(x, y)
        delta = Point(dx, dy)
        view = self._window.hit_test_with_event(origin, None)
        Application.shared_application().post_event(MouseDragEvent(origin, delta, buttons, modifiers, view))

    def on_mouse_enter(self, x, y):
        pass
        #origin = Point(x, y)
        #Application.shared_application().post_event(MouseEnterWindowEvent(origin, self._window))

    def on_mouse_leave(self, x, y):
        pass
        #origin = Point(x, y)
        #Application.shared_application().post_event(MouseLeaveWindowEvent(origin, self._window))

    def on_mouse_motion(self, x, y, dx, dy):
        origin = Point(x, y)
        delta = Point(dx, dy)
        view = self._window.hit_test_with_event(origin, None)
        Application.shared_application().post_event(MouseMotionEvent(origin, delta, view))

    def on_mouse_press(self, x, y, button, modifiers):
        origin = Point(x, y)
        view = self._window.hit_test_with_event(origin, None)
        Application.shared_application().post_event(MousePressEvent(origin, button, modifiers, view))

    def on_mouse_release(self, x, y, button, modifiers):
        origin = Point(x, y)
        view = self._window.hit_test_with_event(origin, None)
        Application.shared_application().post_event(MouseReleaseEvent(origin, button, modifiers, view))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        origin = Point(x, y)
        delta = Point(scroll_x, scroll_y)
        view = self._window.hit_test_with_event(origin, None)
        Application.shared_application().post_event(MouseScrollEvent(origin, delta, view))

    def on_move(self, x, y):
        View.set_frame(self._window, Rect(x=x, y=y))
        
    def on_resize(self, width, height):
        pyglet.window.Window.on_resize(self, width, height)
        View.set_frame(self._window, Rect(width=width, height=height))

    def on_show(self):
        pass

    def on_text(self, text):
        Application.shared_application().post_event(TextEvent(text))

    def on_text_motion(self, motion):
        Application.shared_application().post_event(TextMotionEvent(motion))

    def on_text_motion_select(self, motion):
        Application.shared_application().post_event(TextMotionSelectEvent(motion))


class Window(View):
    # Window Style defines
    STYLE_BORDERLESS = pyglet.window.Window.WINDOW_STYLE_BORDERLESS
    STYLE_DEFAULT    = pyglet.window.Window.WINDOW_STYLE_DEFAULT
    STYLE_DIALOG     = pyglet.window.Window.WINDOW_STYLE_DIALOG
    STYLE_TOOL       = pyglet.window.Window.WINDOW_STYLE_TOOL

    def __init__(self, style=STYLE_DEFAULT, fixed_size=None):
        View.__init__(self)
        self._window = self
        self._first_responder = None
        self._title = None
        self._style = style
        self._resizable = fixed_size is None
        self._application = Application.shared_application()
        self._min_size = None
        self._max_size = None
        self._zoomed = False
        self._key_window = False
        self._main_window = False
        if fixed_size is None:
            # normal window
            self._pyglet = PygletWindow(self, 
                                        style=style, 
                                        resizable=True)
        else:
            # fixed size window
            self._pyglet = PygletWindow(self, 
                                        style=style, 
                                        resizable=False, 
                                        width=fixed_size.width, 
                                        height=fixed_size.height)
        x, y = self._pyglet.get_location()
        width, height = self._pyglet.get_size()
        View.set_frame(self, Rect(x, y, width, height))
        self._application._add_window(self)

    # Configuring Windows
    def style(self):
        return self._style

    def toggle_fullscreen(self):
        self._pyglet.set_fullscreen(not self._pyglet.fullscreen)

    def set_frame(self, rect):
        if (    self._resizable == False
            and (rect.size.width != None or rect.size.height != None)):
            raise ValueError(u'Window is not resizable')
        View.set_frame(self, rect)
        self._pyglet.set_location(self._frame.origin.x, self._frame.origin.y)
        self._pyglet.set_size(self._frame.size.width, self._frame.size.height)

    def title(self):
        return copy(self._title)

    def set_title(self, title):
        self._title = copy(title)
        self._pyglet.set_caption(title)

    # Sizing windows
    def min_size(self):
        return self._min_size

    def set_min_size(self, size):
        if not isinstance(size, Size):
            raise TypeError(u'min size must be a Size')
        self._min_size = size
        width = 0
        if size.width is not None:
            width = size.width
        height = 0
        if size.height is not None:
            height = size.height
        self._pyglet.set_minimum_size(width, height)

    def max_size(self):
        return self._max_size

    def set_max_size(self, size):
        if not isinstance(size, Size):
            raise TypeError(u'max size must be a Size')
        self._max_size = size
        width = 0
        if size.width is not None:
            width = size.width
        height = 0
        if size.height is not None:
            height = size.height
        self._pyglet.set_maximum_size(width, height)

    # Making Windows Key
    def is_key_window(self):
        return self._key_window

    def can_become_key_window(self):
        return True

    def become_key_window(self):
        self._key_window = True

    def resign_key_window(self):
        self._key_window = False

    # Closing Windows
    def close(self):
        if self._application is not None:
            self.remove_from_application()
        self._pyglet.close()

    # Distributng events
    def send_event(self, event):
        event.dispatch_event(self.first_responder())

    def update(self):
        self.layout_if_needed()

    # First Responder management
    def first_responder(self):
        return self._first_responder

    def make_first_responder(self, responder):
        retval = False
        if self._first_responder is not responder:
            if (    self._first_responder.can_resign_first_responder() 
                and responder.can_become_first_responder()):
                # actually change it
                self._first_responder.resign_first_responder()
                responder.become_first_responder()
                self._first_responder = responder
                retval = True
        return retval

    # Linking to application
    def remove_from_application(self):
        if self._application is not None:
            self.will_move_to_application(None) 
            self._application._remove_window(self)
            self._application = None
            if self._application is not None:
                self._pyglet.set_visible(True)
            else:
                self._pyglet.set_visible(False)
            self.did_move_to_application()

    def will_move_to_application(self, app):
        pass

    def did_move_to_application(self):
        pass

    # View Overrides
    def will_move_to_superview(self, superview):
        raise TypeError(u'Window cant be added to other views')

    def will_move_to_window(self, window):
        raise TypeError(u'Window cant be added to other window')

    # Responder overrides
    def next_responder(self):   
        return self._application # send events to application

