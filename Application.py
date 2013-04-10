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


from Responder import *
from Event import *
import urwid
import time
import threading


class Application(Responder):
	def __init__(self):
		Responder.__init__(self)
		self._dispatch = ApplicationEventDispatch(self)
		self._keyWindow = None
		self._windows = []
		self._windowMenu = None

	# Managing Menus
	def windowMenu(self):
		return self._windowMenu

	def setWindowMenu(self, menu):
		self._windowMenu = menu

	# Managing Windows
	def keyWindow(self):
		return self._keyWindow

	def windows(self):
		return copy(self._windows)

	def addWindow(self, window):
		self.insertWindowAtIndex(window, len(self._windows))

	def bringWindowToFront(self, window):
		try:
			self._windows.remove(window)
			self._windows.append(window)
		except ValueError:
			raise ValueError(u'window not in windows')

	def sendWindowToBack(self, window):
		try:
			self._windows.remove(window)
			self._windows.insert(0, window)
		except ValueError:
			raise ValueError(u'window not in windows')

	def insertWindowAtIndex(self, window, idx):
		if window is None:
			raise ValueError(u'Adding a None window')

		if idx < 0 or idx > len(self.windows):
			raise ValueError(u'Index must be between 0 and len(windows)')

		window.removeFromApplication()
		window.willMoveToApplication(self)

		self._windows.insert(idx, window)
		window._application = self
		window.setNeedsDisplay()

		window.didMoveToApplication()
		self.didAddWindow(window)

	def insertWindowAboveWindow(self, window, otherWindow):
		if otherWindow is None:
			raise ValueError(u'otherWindow is None')

		if window == otherWindow:
			raise ValueError(u'window == otherWindow')

		try:
			idx = self._windows.index(otherWindow)
			idx += 1
		except ValueError:
			raise ValueError(u'window not a windows')
		self.insertWindowAtIndex(window, idx)

	def insertWindowBelowWindow(self, window, otherWindow):
		if otherWindow is None:
			raise ValueError(u'otherWindow is None')

		if window == otherWindow:
			raise ValueError(u'window == otherWindow')

		try:
			idx = self._windows.index(otherWindow)
		except ValueError:
			raise ValueError(u'window not in windows')
		self.insertWindowAtIndex(window, idx)

	def exchangeSubviewAtIndexwithSubviewAtIndex(self, idx1, idx2):
		if (   idx1 < 0 
			or idx1 >= len(self._windows) 
			or idx2 < 0
			or idx2 >= len(self._windows)):
			raise ValueError(u'index not in range')
		item2 = self._windows[idx2]
		item1 = self._windows.pop(idx1)
		self._windows.insert(idx1, item2)
		self._windows.pop(idx2)
		self._windows.inset(idx2, item1)

	# Updating Windows
	def updateWindows(self):
		for window in self._windows:
			window.update()

	# Handling Events
	def currentEvent(self):
		retval = None
		if len(self._dispatch._events) > 0:
			retval = self._dispatch._events[0]
		return retval

	def nextEventMatching(self, types=None, dequeue=True, timeout=None):
		return self._dispatch.nextEventMatching(self, types, dequeue, timout)

	def discardEventsMatchingMask(self, types, lastEvent):
		self._dispatch.discardEventsMatchingMask(types, lastEvent)

	def postEvent(self, ev, atStart):
		self._dispatch.postEvent(ev, atStart)

	# Observing Window-Related Changes
	def didAddWindow(self):
		pass		

	def willRemoveWindow(self, window):
		pass	

	# we'll set nextResponder to the keyWindow - so that we deliver all events 
	# to the right window
	def nextResponder(self):	
		return self._keyWindow
		

class ApplicationEventDispatch(threading.Thread):
	def __init__(self, application):
		threading.Thread.__init__(self)
		# We don't actually want multiple threads, we just want the ability
		# to exec the event processing on a different stack - to allow nice
		# symantics when you shortcut the event processing 
		#
		# we should really just re-enter the event loop but that requires some
		# rather in-depth digging around which I don't fancy at the moment
		self._application = application
		self._events = []
		self._dispatchPaused = threading.Event()
		self._dispatchEvents = threading.Event()
		self.start()

		# the Responder dispatch routines for each event
		self._dispatch = {
			KeyEventType.KEY_DOWN: u'keyDown',
			KeyEventType.KEY_UP: u'keyUp',
			KeyEventType.FLAGS_CHANGED: u'flagsChanged',
			
			MouseEventType.MOUSE_DOWN: u'mouseDown',
			MouseEventType.OTHER_MOUSE_DOWN: u'otherMouseDown',
			MouseEventType.RIGHT_MOUSE_DOWN: u'rightMouseDown',
			MouseEventType.SCROLL_WHEEL_UP: u'scrollWheel',
			MouseEventType.SCROLL_WHEEL_DOWN: u'scrollWheel',

			MouseEventType.MOUSE_UP: u'mouseUp',
			MouseEventType.OTHER_MOUSE_UP: u'otherMouseUp',
			MouseEventType.RIGHT_MOUSE_UP: u'rightMouseUp',

			MouseEventType.MOUSE_DRAGGED: u'mouseDragged',
			MouseEventType.OTHER_MOUSE_DRAGGED: u'otherMouseDragged',
			MouseEventType.RIGHT_MOUSE_DRAGGED: u'rightMouseDragged',

			EnterExitEventType.MOUSE_ENTERED: u'mouseEntered',
			EnterExitEventType.MOUSE_EXITED: u'mouseExited'
		}

	def postEvent(self, ev, atStart):
		# this should only ever be able to be called when the handler thread
		# is waiting on _dispatchEvents
		if (   self._dispatchEvents.is_set() == True 
			or self._dispatchPaused.is_set() == False):
			raise RuntimeError(u'add called when event handler is running')
		idx = 0
		if not atStart:
			idx = len(self._events)
		self._events.insert(idx, ev)
		self._dispatchEvents.set()
		self._dispatchPaused.wait()

	def _waitForNextEvent(self):
		self._dispatchPaused.set()
		self._dispatchEvents.wait()

	def run(self):
		while True:
			if len(self._events) == 0:
				self._waitForNextEvent() # we're out of events
			# pop the first event off the queue and dispatch it
			ev = self._events.pop(0)
			dispatch = self._dispatch[ev.type]
			getattr(self._application, dispatch)(ev)

	def nextEventMatching(self, types=None, dequeue=True, timeout=None):
		# this is called by an event dispatcher i.e. on this classes thread
		# when it wants to shortcut normal event dispatching
		if threading.current_thread() != self:
			raise RuntimeError(
				u'You can only shortcut event dispatch from an event handler'
			)

		retval = None
		start = time.time()
		remaining = timeout
		while remaining is None or remaining > 0.0:
			if not self._waitForNextEvent(remaining):
				break # timeout occurred
			# we can ONLY get one event at a time - so its always the last 
			# event we need to examine
			if types == None:
				retval = self._events[-1]
				break
			else:
				if self._events[-1].type in types:
					retval = self._events[-1]
					break
			if timeout is not None:
				remaining = timeout - (time.time() - start)
		if retval is not None and dequeue:
			self._events.pop()
		return retval

	def discardEventsMatchingMask(self, types, lastEvent):
		if len(self._events) > 0:
			idx = 0
			while self._events[idx] != lastEvent:
				if types is None or self._events[idx].type in types:
					# throw away event
					self._events.pop(idx)
				else:
					idx += 1


