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


from Responder import *
from Geometry import *
from pyglet.gl import *


class InvalidViewError(Exception):
    pass


class View(Responder):
    # Autoresize defines
    AUTORESIZING_NONE                   = 0
    AUTORESIZING_FLEXIBLE_LEFT_MARGIN   = 1 << 0
    AUTORESIZING_FLEXIBLE_WIDTH         = 1 << 1
    AUTORESIZING_FLEXIBLE_RIGHT_MARGIN  = 1 << 2
    AUTORESIZING_FLEXIBLE_TOP_MARGIN    = 1 << 3
    AUTORESIZING_FLEXIBLE_HEIGHT        = 1 << 4
    AUTORESIZING_FLEXIBLE_BOTTOM_MARGIN = 1 << 5

    def __init__(self):
        self._background_color = None
        self._clips_to_bounds = True
        self._frame = Rect(100, 100, 100, 100)
        self._superview = None
        self._subviews = []
        self._window = None
        self._autoresizing_mask = View.AUTORESIZING_NONE
        self._autoresizes_subviews = True
        self._needs_layout = True
        self._needs_display = True
        self._invalid_rectangles = []
        self._tag = None

    # Configuring a views visual appearance
    def background_color(self):
        return self._background_color

    def set_background_color(self, color):
        self._background_color = color

    def clips_to_bounds(self):
        return self._clips_to_bounds

    def set_clips_to_bounds(self, clip):
        self._clips_to_bounds = clip

    # Configuring frame
    def frame(self):
        return self._frame

    def set_frame(self, rect):
        if not isinstance(rect, Rect):
            raise TypeError(u'rect must be a Rect')
        # update any non None members
        old_size = copy(self.frame().size)

        if rect.origin.x is not None:
            self._frame.origin.x = rect.origin.x
        if rect.origin.y is not None:
            self._frame.origin.y = rect.origin.y
        if rect.size.width is not None:
            self._frame.size.width = rect.size.width
            self.set_needs_layout()
        if rect.size.height is not None:
            self._frame.size.height = rect.size.height
            self.set_needs_layout()

        for view in self._subviews:
            view.resize_with_old_superview_size(old_size)
            view.set_needs_layout()

    # Managing the view hierarchy
    def superview(self):
        return self._superview

    def subviews(self):
        return copy(self._subviews)

    def window(self):
        return self._window

    def add_subview(self, view):
        self.insert_subview_at_index(view, 0)

    def bring_subview_to_front(self, view):
        if not isinstance(view, View):
            raise TypeError(u'view must be a View or subclass of it')
        try:
            self._subviews.remove(view)
            self._subviews.insert(0, view)
        except ValueError:
            raise InvalidViewError(u'view is not a subview of this instance')

    def send_subview_to_back(self, view):
        if not isinstance(view, View):
            raise TypeError(u'view must be a View or subclass of it')
        try:
            self._subviews.remove(view)
            self._subviews.append(view)
        except:
            raise InvalidViewError(u'view is not a subview of this instance')

    def remove_from_superview(self):
        if self._superview is not None:
            # XXX: sort out first responder if were it?
            self._superview.will_remove_subview(self)
            self._will_move_to_window(None)
            self.will_move_to_superview(None)
            
            self._superview._subviews.remove(self)
            self._superview = None

            self._did_move_to_window()
            self.did_move_to_superview()
            self.set_needs_layout()

    def insert_subview_at_index(self, view, idx):
        if not isinstance(view, View):
            raise TypeError(u'view must be a View or subclass of it')
        if self.is_descendant_of(view):
            raise TypeError(u'this view is a descendant of view - adding would create a loop')
        if idx < 0 or idx > len(self._subviews):
            raise ValueError(u'Index must be between 0 and len(subviews)')

        view.remove_from_superview()
        if self._window is not None:
            view._will_move_to_window(self._window)
        view.will_move_to_superview(self)

        self._subviews.insert(idx, view)
        view._superview = self
        
        if self._window is not None:
            view._did_move_to_window()
        view.did_move_to_superview()
        self.did_add_subview(view)
        self.set_needs_layout()

    def insert_subview_above_subview(self, view, other_view):
        if not isinstance(view, View):
            raise TypeError(u'view must be a View or subclass of it')
        if not isinstance(other_view, View):
            raise TypeError(u'other_view must be a View or subclass of it')
        try:
            idx = self._subviews.index(other_view)
            self.insert_subview_at_index(view, idx)
        except ValueError:
            raise InvalidViewError(u'other_view is not a subview of this instance')

    def insert_subview_below_subview(self, view, other_view):
        if not isinstance(view, View):
            raise TypeError(u'view must be a View or subclass of it')
        if not isinstance(other_view, View):
            raise TypeError(u'other_view must be a View or subclass of it')
        try:
            idx = self._subviews.index(other_view)
            self.insert_subview_at_index(view, idx + 1)
        except ValueError:
            raise InvalidViewError(u'other_view is not a subview of this instance')

    def exchange_subview_at_index_with_subview_at_index(self, idx1, idx2):
        if (   idx1 < 0 
            or idx1 >= len(self._subviews)):
            raise ValueError(u'idx1 not in range')
        if (   idx2 < 0
            or idx2 >= len(self._subviews)):
            raise ValueError(u'idx2 not in range')
        item2 = self._subviews[idx2]
        item1 = self._subviews[idx1]
        self._subviews[idx1] = item2
        self._subviews[idx2] = item1

    def is_descendant_of(self, view):
        if not isinstance(view, View):
            raise TypeError(u'view must be a View or subclass of it')
        retval = False
        if view is not None:
            v = self
            while v is not None and v != view:
                v = v._superview
            retval = v == view
        return retval

    # Configuring the Resizing Behavior
    def autoresizing_mask(self):
        return self._autoresizing_mask

    def set_autoresizing_mask(self, mask):
        self._autoresizing_mask = mask

    def autoresizes_subviews(self):
        return self._autoresizes_subviews

    def set_autoresizes_subviews(self, resize):
        self._autoresizes_subviews = bool(resize)

    def size_that_fits(self, size):
        return self.frame().size

    def size_to_fit(self):
        rect = self.frame()
        rect.size = self.size_that_fits(self.frame().size)
        self.set_frame(rect)

    def resize_with_old_superview_size(self, old_size):
        frame = self.frame()
        tr = Point(frame.origin.x + frame.size.width, frame.origin.y + frame.size.height)
        bl = copy(frame.origin)
        new_size = self._superview.frame().size

        # the amounts to distributs amoungst the flexible borders
        flexx = 0
        flexy = 0
        
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_LEFT_MARGIN:
            flexx += 1
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_WIDTH:
            flexx += 1
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_RIGHT_MARGIN:
            flexx += 1

        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_TOP_MARGIN:
            flexy += 1
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_HEIGHT:
            flexy += 1
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_BOTTOM_MARGIN:
            flexy += 1

        # we now know how many bits we need to divide up the extra space over
        hd = 0
        vd = 0
        if flexx != 0:
            hd = (new_size.width - old_size.width) / flexx
        if flexy != 0:
            vd = (new_size.height - old_size.height) / flexy

        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_LEFT_MARGIN:
            bl.x += hd
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_WIDTH:
            tr.x += hd
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_RIGHT_MARGIN:
            pass

        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_TOP_MARGIN:
            pass
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_HEIGHT:
            tr.y += vd
        if self._autoresizing_mask & View.AUTORESIZING_FLEXIBLE_BOTTOM_MARGIN:
            bl.y += vd

        self.set_frame(Rect(origin=bl, size=Size(tr.x-bl.x, tr.y-bl.y)))

    # Laying out Subviews
    def layout_subviews(self):
        pass

    def set_needs_layout(self):
        self._needs_layout = True

    def layout_if_needed(self):
        if self._needs_layout == True:
            self.layout_subviews()
            self._needs_layout = False
        for view in self._subviews:
            view.layout_if_needed()

    # Drawing and Updating the View
    def draw_rect(self, rect):
        if self._background_color is not None:
            frame = self.frame()
            color = self._background_color
            glColor4f(color.red, color.green, color.blue, color.alpha)
            glRectf(0, 0, frame.size.width, frame.size.height);
        
    def set_needs_display(self):
        self._needs_display = True
        for view in self._subviews:
            view.set_needs_display()

    def set_needs_display_in_rect(self, rect):
        self._invalid_rectangles.append(rect)
        # XXX: should this do something to iss subview in this rect?

    def display_if_needed(self):
        if self._needs_display == True:
            self._draw_rect(self._frame)
        else:
            for rect in self._invalid_rectangles:
                self._draw_rect(rect)
        self._invalid_rectangles = []
        self._needs_display = False
        for view in self._subviews:
            view.display_if_needed()

    # Identifying the View at Runtime
    def tag(self):
        return self._tag

    def set_tag(self, tag):
        self._tag = tag

    def view_with_tag(self, tag):
        if tag is None:
            raise ValueError(u'None is not a valid tag value')
        retval = None
        if self._tag == tag:
            retval = self
        else:
            for view in self._subviews:
                retval = view.view_with_tag(tag)
                if retval is not None:
                    break
        return retval           

    # Converting Between View Coordinate Systems
    def convert_point_to_view(self, point, view=None):
        if view is not None:
            if not isinstance(view, View):
                raise TypeError(u'view must be a View or subclass of it')
            if self._window is None:
                raise InvalidViewError(u'reciever must be in a window')
            if view._window is None:
                raise InvalidViewError(u'view must be in a window')
            if self._window != view._window:
                raise InvalidViewError(u'view must be in same window as reciever')
        retval = copy(point)
        if view is not self:
            # convert point to window
            cur = self
            while cur is not self._window:
                frame = cur.frame()
                retval.x += frame.origin.x
                retval.y += frame.origin.y
                cur = cur._superview
            if view is not None:
                retval = view.convert_point_from_view(retval)
        return retval

    def convert_point_from_view(self, point, view=None):
        if view is not None:
            if not isinstance(view, View):
                raise TypeError(u'view must be a View or subclass of it')
            if self._window is None:
                raise InvalidViewError(u'reciever must be in a window')
            if view._window is None:
                raise InvalidViewError(u'view must be in a window')
            if self._window != view._window:
                raise InvalidViewError(u'view must be in same window as reciever')      
        retval = copy(point)
        if view is not self:
            if view is not None:
                retval = view.convert_point_to_view(point)
            # convert point to window
            cur = self
            while cur is not self._window:
                frame = cur.frame()
                retval.x -= frame.origin.x
                retval.y -= frame.origin.y
                cur = cur._superview
        return retval

    def convert_rect_to_view(self, rect, view=None):
        topleft = self.convert_point_to_view(rect.origin, view)
        br = Point(rect.origin.x + rect.size.width, rect.origin.y + rect.size.height)
        br = self.convert_point_to_view(br, view)
        return Rect(origin=topleft, width=br.x-rect.origin.x, height=br.y-rect.origin.y)

    def convert_rect_from_view(self, rect, view=None):
        topleft = self.convert_point_from_view(rect.origin, view)
        br = Point(rect.origin.x + rect.size.width, rect.origin.y + rect.size.height)
        br = self.convert_point_from_view(br, view)
        return Rect(origin=topleft, width=br.x-rect.origin.x, height=br.y-rect.origin.y)

    # Hit Testing in a View - in our coordinate system
    def point_inside_with_event(self, point, event=None):
        retval = False
        frame = copy(self.frame())
        # XXX: why does this need to be > 0 and <= size rather than >= 0 and < size?
        if (    point.x > 0 
            and point.x <= frame.size.width
            and point.y > 0 
            and point.y <= frame.size.height):
            retval = True
        return retval

    def hit_test_with_event(self, point, event=None):
        retval = None
        if self.point_inside_with_event(point, event):
            # if its inside us - check all our children
            for view in self._subviews:
                p = self.convert_point_to_view(point, view)
                v = view.hit_test_with_event(p, event)
                if v is not None:
                    retval = v
                    break
            if retval is None:
                retval = self
        return retval

    # Observing view changes
    def did_add_subview(self, view):
        pass

    def will_remove_subview(self, view):
        pass

    def will_move_to_superview(self, superview):
        pass

    def did_move_to_superview(self):
        pass

    def will_move_to_window(self, window):
        pass

    def did_move_to_window(self):
        pass

    # Responder overrides
    def next_responder(self):
        return self._superview

    #
    # Protected; propogation helpers
    #
    def _will_move_to_window(self, window):
        self.will_move_to_window(window)
        for view in self._subviews:
            view._will_move_to_window(window)
        self._window = window

    def _did_move_to_window(self):
        self.did_move_to_window()
        for view in self._subviews:
            view._did_move_to_window()

    def _draw_rect(self, rect):
        skip = False
        frame = self.frame()
        origin = Point(0, 0)
        extreme = Point(frame.size.width, frame.size.height)
        if self._window is not self:
            origin = self.convert_point_to_view(origin)
            extreme.x += origin.x
            extreme.y += origin.y
        glPushMatrix()
        glTranslatef(origin.x, origin.y, 0) # set transform for view
        if self._clips_to_bounds == True:
            glEnable(GL_SCISSOR_TEST)
            cur = self._superview
            while cur is not None and cur is not self._window:
                if cur.clips_to_bounds() == True:
                    f = cur.frame()
                    o = cur.convert_point_to_view(Point(0, 0))
                    e = cur.convert_point_to_view(Point(f.size.width, f.size.height))
                    if o.x > origin.x:
                        origin.x = o.x
                    if o.y > origin.y:
                        origin.y = o.y
                    if e.x < extreme.x:
                        extreme.x = e.x
                    if e.y < extreme.y:
                        extreme.y = e.y
                cur = cur._superview
            if extreme.x < origin.x or extreme.y < origin.y:
                skip = True
            else:
                glScissor(
                    int(origin.x), 
                    int(origin.y), 
                    int(extreme.x-origin.x), 
                    int(extreme.y-origin.y)
                )
        if skip == False:
            self.draw_rect(rect)
        if self._clips_to_bounds == True:
            glDisable(GL_SCISSOR_TEST)
        glPopMatrix()

