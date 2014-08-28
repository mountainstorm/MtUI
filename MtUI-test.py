#!/usr/bin/python
# coding: utf-8
#
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


from Application import *
from Window import *
from View import *
from Color import *
from Event import *
from Cursor import *
from pyglet.gl import *


class HorizontalLayoutView(View):
    def insert_subview_at_index(self, view, idx):
        # we're going to pack all children - they only choose their width 
        view.set_autoresizing_mask(View.AUTORESIZING_FLEXIBLE_HEIGHT | View.AUTORESIZING_FLEXIBLE_RIGHT_MARGIN)
        View.insert_subview_at_index(self, view, idx)
    
    def layout_subviews(self):
        x = 0
        for v in self.subviews():
            size = v.size_that_fits(self.frame().size)
            rect = Rect(x, 0, size.width, self.frame().size.height)
            v.set_frame(rect)
            x += size.width
   
    def size_that_fits(self, size):
        x = 0
        for v in self.subviews():
            s = v.frame().size
            x += size.width
        return Size(x, size.height)


class SplitHandleView(View):
    def __init__(self, min_size):
        View.__init__(self)
        self._min_size = min_size

    def mouse_enter(self, event):
        Cursor.set_cursor(Cursor.SIZE_LEFT_RIGHT)

    def mouse_leave(self, event):
        Cursor.set_default()

    def mouse_press(self, event):
        subviews = self._superview.subviews()
        # dont rely on the delta int he event as we get 'rounding' errors
        target = subviews[subviews.index(self)-1]
        start = event.origin
        start_width = target.frame().size.width
        while True:
            # eat leave so we know when we leave the window - eat enter for balance
            ev = Application.shared_application().next_event_matching(
                (MouseReleaseEvent, MouseDragEvent, MouseEnterEvent, MouseLeaveEvent)
            )
            if isinstance(ev, MouseLeaveEvent) and ev.view == self._window:
                break # we have left the building
            if isinstance(ev, MouseReleaseEvent):
                break # done
            if isinstance(ev, MouseDragEvent):
                width = start_width + (ev.origin.x - start.x)
                if width < self._min_size:
                    width = self._min_size
                target.set_frame(Rect(width=width))
                self._superview.set_needs_layout()
        if isinstance(ev, MouseReleaseEvent):
            # XXX: this would be much easier if we got all events whilst we're in front
            v = self._window.hit_test_with_event(ev.origin, None)
            if v is self:
                Cursor.set_cursor(Cursor.SIZE_LEFT_RIGHT)
            else:
                # generate an enter event to set the pointer to whatever it should be
                self._eventloop.post_event(MouseLeaveEvent(self, event.timestamp))
                self._eventloop.post_event(MouseEnterEvent(event.view, event.timestamp))
        else:
            Cursor.set_default()


class HorizontalSplitView(HorizontalLayoutView):
    def insert_subview_at_index(self, view, idx):
        handle = SplitHandleView(10)
        handle.set_background_color(Color.from_hex(u'#262626'))
        handle.set_frame(Rect(0, 0, 10, 100))
        HorizontalLayoutView.insert_subview_at_index(self, handle, idx*2)
        HorizontalLayoutView.insert_subview_at_index(self, view, idx*2)


class TextView(View):
    def __init__(self, str):
        View.__init__(self)
        self._str = str
        self.label = pyglet.text.Label(self._str,
                                  font_name='Menlo', #Times New Roman',
                                  font_size=9,
                                  x=0, y=0,
                                  color=(255, 255, 255, 255),
                                  multiline=True,
                                  width=0xffff,
                                  anchor_x='left', anchor_y='top')
        self.scroll_y = self.frame().size.height

    def set_frame(self, rect):
        self.scroll_y = rect.size.height
        View.set_frame(self, rect)

    def mouse_scroll(self, event):
        self.scroll_y += event.delta.y * 4
        if self.scroll_y < self.frame().size.height:
            self.scroll_y = self.frame().size.height
        elif self.scroll_y > self.label.content_height:
            self.scroll_y = self.label.content_height

    def draw_rect(self, rect):
        View.draw_rect(self, rect)
        glPushMatrix()
        glTranslatef(0, int(self.scroll_y), 0)
        #glTranslatef(0, self.frame().size.height, 0) # top
        #glTranslatef(0, self.label.content_height, 0) # bottom
        View.draw_rect(self, rect)
        self.label.draw()
        glPopMatrix()


app = Application()

bg = Color.from_hex(u'#2d2d2d')

w = Window()
w.set_background_color(Color.from_hex(u'#8a8a8a'))
w.set_title(u'MyWin')
w.set_frame(Rect(width=640, height=480))

h = HorizontalSplitView()
h.set_background_color(bg)
h.set_autoresizing_mask(
      View.AUTORESIZING_FLEXIBLE_WIDTH 
    | View.AUTORESIZING_FLEXIBLE_HEIGHT 
)
h.set_frame(Rect(15, 15, w.frame().size.width-20, w.frame().size.height-20))
w.add_subview(h)


#f = open(u'../ktk.py', u'rt')
f = open(__file__, u'rt')
str = f.read().decode('utf-8')
#str = str[int(len(str)*0.9):]
f.close()


red = View()
red.set_background_color(bg)
red.set_frame(Rect(0, 0, 10, 100))
h.add_subview(red)

green = View()
green.set_background_color(bg)
green.set_frame(Rect(0, 0, 100, 80))
h.add_subview(green)

blue = TextView(str)
blue.set_background_color(bg)
blue.set_frame(Rect(0, 0, 50, 50))
h.add_subview(blue)

yellow = View()
yellow.set_background_color(bg)
yellow.set_frame(Rect(0, 0, 200, 100))
h.add_subview(yellow)

app.run()
