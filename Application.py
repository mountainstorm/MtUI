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
from Event import *
import pyglet
from copy import copy
import time
import threading


_application_instance = None


class ApplicationEventLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._quit = False
        self._event_queue = []
        self._process_events = threading.Event()
        self._awaiting_events =  threading.Event()
        self.start()

    def run(self):
        while self._quit == False:
            self._process_events.wait()
            if self._quit == False:
                while self._quit == False and len(self._event_queue) > 0:
                    event = self._event_queue.pop()
                    Application.shared_application().send_event(event)
                self._awaiting_events.set()

    def join(self, timeout=None):
        self._quit = True
        self._process_events.set()
        threading.Thread.join(self)

    def dispatch_events(self):
        self._process_events.set()
        self._awaiting_events.wait() 

    def post_event(self, event, at_start=False):
        idx = len(self._event_queue)
        if at_start == True:
            idx = 0
        self._event_queue.insert(idx, event)

    def next_event_matching(self, mask, until, dequeue):
        retval = None
        while self._quit == False and retval is None and time.time() < until:
            # check all events currently in the queue
            for i in range(0, len(self._event_queue)):
                Application.shared_application().update_windows()
                found = True
                if mask is not None:
                    found = False
                    for m in mask:
                        if isinstance(self._event_queue[i], m):
                            found = True
                            break
                if found == True:
                    retval = self._event_queue[i]
                    if dequeue == True:
                        self._event_queue.pop(i)
                    break
            if retval is None:
                # nothing - so wait until more events arrive
                self._awaiting_events.set()
                self._process_events.wait()
        return retval

    def discard_events_matching(self, mask, end_event):
        j = 0
        for i in range(0, len(self._event_queue)):
            if self._event_queue[j] == end_event:
                break
            remove = True
            if mask is not None:
                remove = False
                for m in mask:
                    if isinstance(self._event_queue[j], m):
                        remove = True
                        break
            if remove == True:
                self._event_queue.pop(j)
            else:
                j += 1      


class PygletEventLoop(pyglet.app.EventLoop):
    def __init__(self, eventloop):
        pyglet.app.EventLoop.__init__(self)
        self._eventloop = eventloop
        
    def idle(self):
        # we're going to let the 'runloop' thread run and process events from the 
        # application queue.  It will either complete send'ing all of them, or 
        # be caught up in something modal.  Either way we'll be signaled very quickly 
        # and can then go on.
        self._eventloop.dispatch_events()
        Application.shared_application().update_windows()
        return pyglet.app.EventLoop.idle(self)


class Application(Responder):
    def __init__(self):
        global _application_instance
        Responder.__init__(self)
        if _application_instance is not None:
            raise ValueError(u'Application instance already exits')
        _application_instance = self # set the application instance
        self._key_window = None
        self._windows = []
        self._main_menu = None
        self._event_queue = []
        self._eventloop = ApplicationEventLoop()
        self._mouse_view = None
        self._pyglet = PygletEventLoop(self._eventloop)
        pyglet.app.event_loop = self._pyglet

    def __del__(self):
        print "del"
        self._eventloop.join()

    # Getting the Application
    @classmethod
    def shared_application(self):
        global _application_instance
        return _application_instance

    # XXX: icon?

    # Terminating Applications
    def terminate(self):
        self.application_will_terminate()
        self.stop() # XXX: rework to support application_should_terminate

    # Managing the Event Loop
    def run(self):
        pyglet.app.run()

    def stop(self):
        self._eventloop.join()
        pyglet.app.exit()

    def send_event(self, event):
        if isinstance(event, KeyEvent):
            if self.key_window() is not None:
                self.key_window().send_event(event)
        else:
            event.dispatch_event(event.view)

    # Handling events
    def next_event_matching(self, mask, until=0xffffffffffffffff, dequeue=True):
        return self._eventloop.next_event_matching(mask, until, dequeue)

    def discard_events_matching(self, mask, end_event):
        self._eventloop.discard_events_matching(mask, end_event)

    # Posting events
    def post_event(self, event, at_start=False):
        if isinstance(event, MouseEvent):
            if event.view is not self._mouse_view:
                # we've moved to a another view - inject leave/enter
                if self._mouse_view is not None:
                    self._eventloop.post_event(MouseLeaveEvent(self._mouse_view, event.timestamp))
                self._mouse_view = event.view
                if self._mouse_view is not None:
                    self._eventloop.post_event(MouseEnterEvent(event.view, event.timestamp))
        if self._mouse_view is not None:
            self._eventloop.post_event(event, at_start)

    # Managing Windows
    def key_window(self):
        return self._key_window

    def windows(self):
        return copy(self._windows)
        
    # Update Windows
    def update_windows(self):
        for win in self._windows:
            win.update()

    # Accessing the Main Menu
    def main_menu(self):
        return self._main_menu

    def set_main_menu(self, menu):
        self._main_menu = menu # XXX:

    # Window Management - friend calls
    def _add_window(self, window):
        self._windows.insert(0, window)
        self.did_add_window(window)

    def _remove_window(self, window):
        self.will_remove_window(window)
        self._windows.remove(window)
        if self._key_window is window:
            self._key_window = None

    def _bring_window_to_front(self, window):
        # called when a user brings a window to the front
        self._windows.remove(window)
        self._windows.insert(0, window)

    # Observing Window-Related Changes
    def did_add_window(self, window):
        pass        

    def will_remove_window(self, window):
        pass    

    # Application state handlers
    def application_will_terminate(self):
        pass

    # Responder overrides
    def next_responder(self):   
        return None # XXX: should really go to the controller


# Applciation termination defines
Application.TERMINATE_CANCEL = 0
Application.TERMINATE_LATER  = 1

