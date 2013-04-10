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


from Context import Context
from Rect import *
from Event import *
import urwid
import time
import threading


class UrwidAdapter(urwid.Widget):
	DWELL = 0.1 # a resonable minimum - 100wpm/5 letters word

	_selectable = True

	def __init__(self):
		urwid.Widget.__init__(self)
		self._context = Context(Rect(0, 0, 80, 24))
		self._lastButton = None
		self._lastTarget = None
		self.mainloop = None

	def rows(self, size, focus=False):
		return size

	def pack(self, size, focus=False):
		return size

	def render(self, size, focus=False):
		self._context.canvas = urwid.CompositeCanvas(
			urwid.SolidCanvas(u' ', size[0], size[1])
		)
		self._context.setFrameConstraints(Rect(0, 0, size[0], size[1]))

		self._context.setNeedsLayout()
		self._context.setNeedsDisplay()

		self._context.layoutIfNeeded()
		self._context.updateConstraintsIfNeeded()
		self._context.displayIfNeeded()
		return self._context.canvas

	def keypress(self, size, key):
		# pass to first responder
		target = self._context.firstResponder()
		char = key # TODO: strip off control chars ad shove into modifiers
		modifiers = []
		ev = KeyEvent(
			KeyEventType.KEY_DOWN, 
			modifiers, 
			time.time(), 
			self._context,
			[char], 
			[char], # we can't really undo the modifier flags 
			False
		)
		target.keyDown(ev)
		self.mainloop.set_alarm_in(UrwidAdapter.DWELL, self._keyUp, (target, ev))
		self._invalidate() # TODO: we need a better way to detect refresh

	def _keyUp(self, mainloop, data):
		target, ev = data
		ev = KeyEvent(
			KeyEventType.KEY_UP, 
			ev.modifiers, 
			time.time(), 
			self._context,
			ev.characters,
			ev.charactersIgnoringModifiers,
			ev.isARepeat
		)
		target.keyUp(ev) 
		self._invalidate() # TODO: we need a better way to detect refresh

	def mouse_event(self, size, event, button, col, row, focus):
		hit = Point(col, row)
		dispatch = None # dispatch method for the event

		# figure out event type and dispatch method
		modifiers = [] # TODO: parse out modifiers
		if event.endswith(u'mouse press'):
			if button == 1:
				eventType = MouseEventType.MOUSE_DOWN
				dispatch = u'mouseDown'
			elif button == 2:
				eventType = MouseEventType.OTHER_MOUSE_DOWN
				dispatch = u'otherMouseDown'
			elif button == 3:
				eventType = MouseEventType.RIGHT_MOUSE_DOWN
				dispatch = u'rightMouseDown'
			elif button == 4 or button == 5:
				eventType = MouseEventType.SCROLL_WHEEL_UP
				if button == 5:
					eventType = MouseEventType.SCROLL_WHEEL_DOWN
				dispatch = u'scrollWheel'
				button = None
		elif event.endswith(u'mouse release'):
			if self._lastButton == 1:
				eventType = MouseEventType.MOUSE_UP
				dispatch = u'mouseUp'
			elif self._lastButton == 2:
				eventType = MouseEventType.OTHER_MOUSE_UP
				dispatch = u'otherMouseUp'
			elif self._lastButton == 3:
				eventType = MouseEventType.RIGHT_MOUSE_UP
				dispatch = u'rightMouseUp'
			button = None
		elif event.endswith(u'mouse drag'):
			if button == 1:
				eventType = MouseEventType.MOUSE_DRAGGED
				dispatch = u'mouseDragged'
			elif button == 2:
				eventType = MouseEventType.OTHER_MOUSE_DRAGGED
				dispatch = u'otherMouseDragged'
			elif button == 3:
				eventType = MouseEventType.RIGHT_MOUSE_DRAGGED
				dispatch = u'rightMouseDragged'
		# TODO: mouseMoved once we find a terminal with support

		# create mouse event
		ev = MouseEvent(
			eventType, 
			modifiers,
			time.time(), 
			self._context,
			hit,
			1, 
			1.0
		)
		target = self._context.hitTestWithEvent(hit, ev)
		# fake mouse entered/exit messages
		if target != self._lastTarget:
			if self._lastTarget is not None:
				ex = EnterExitEvent(
					EnterExitEventType.MOUSE_EXITED,
					[],
					time.time(),
					self._context)
				self._lastTarget.mouseExited(ex)
			if target is not None:
				en = EnterExitEvent(
					EnterExitEventType.MOUSE_ENTERED,
					[],
					time.time(),
					self._context)
				target.mouseEntered(en)

		# deliver the event - remember the last button so we can correctly 
	 	# deliver mouse release; TODO: can we handle multiple buttons better?
		if target is not None and dispatch is not None:
			getattr(target, dispatch)(ev)

		self._lastTarget = target
		self._lastButton = button
		self._invalidate() # TODO: we need a better way to detect refresh

	def get_cursor_coords(self, size):
		pass

	def get_pref_col(self, size):
		pass

	def move_cursor_to_coords(self, size, col, row):
		pass

	def __getattr__(self, name):
		return getattr(self._context, name)


# TODO: in enumeration - access to invalid variable throws exception
if __name__ == u'__main__':
	from Layout import *
	from SolidView import *
	from View import *
	from Control import *
	from Label import *
	from Button import *
	from SplitView import *

	palette = [
		('header', '', '', '' , '#8ac', 'g10'),
		('header1', '', '', '' , 'g60', 'g20'),
		('body',  '', '', '', '#fff', 'g10'),
		('dif',  '', '', '', '#f00', 'g10'),
		('scroll', '', '', '', 'g20', 'g10'),
		('splitbar', '', '', '', 'g50', 'g10'),
		('menu', '', '', '', '#000', '#fff'),
		('menu-sep', '', '', '', 'g80', '#fff'),
		('highlight', '', '', '', '#fff', 'g50'),
		('red', '', '', '', '#0f0', '#f00'),
		('green', '', '', '', '#00f', '#0f0'),
		('blue', '', '', '', '#00f', '#00f'),

		('button.normal', '', '', '', 'g60', 'g20'),
		('button.highlighted', '', '', '', 'g70', 'g30'),
		('button.disabled', '', '', '', 'g40', 'g20'),
		('button.selected', '', '', '', 'g80', 'g40')
	]

	adapter = UrwidAdapter()
	if 1:
		l = Label()
		l.setText(u'Hello World')
		l.setAttrs({ControlState.NORMAL: u'dif'})
		l.setFrameConstraints(Rect(origin=Point(5, 2), size=l.sizeThatFits(Size(width=7))))
		l.setTextAlign(TextAlign.CENTER)
		l.setLineBreak(LineBreak.WORD_WRAP)
		adapter.addSubview(l)

		l = Label()
		l.setText(u'Bottom Right')
		l.setAttrs({ControlState.NORMAL: u'dif'})
		l.setTextAlign(TextAlign.CENTER)
		adapter.addSubview(l)
		
		c1 = l.bottom == adapter.height - 10
		c2 = l.right == adapter.right
		c3 = l.left == 0
		adapter.addConstraints([c1, c2, c3])
		
		l = SolidView()
		l.setAttr(u'red')
		c1 = l.width == adapter.width / 2
		c2 = l.height == adapter.height / 2
		c3 = l.left == (adapter.width - l.width) / 2
		c4 = l.top == (adapter.height - l.height) / 2
		adapter.addSubview(l)
		adapter.addConstraints([c1, c2, c3, c4])
		adapter.sendSubviewToBack(l)
		
		a = SolidView()
		a.setAttr(u'highlight')
		c1 = a.left == 2
		c2 = a.top == 2
		c3 = a.width == 10
		c4 = a.height == 5
		l.addSubview(a)
		l.addConstraints([c1, c2, c3, c4])
		
		def click(sender):
			pass #raise TypeValue(sender)
		
		b1 = Button()
		b1.setTag(u'b1')
		b1.setText(u'↴')
		b1.setFrameConstraints(Rect(x=0, y=0))
		b1.setAttrs({
			ControlState.NORMAL: u'button.normal',
			ControlState.HIGHLIGHTED: u'button.highlighted',
			ControlState.DISABLED: u'button.disabled',
			ControlState.SELECTED: u'button.selected'
		})
		b1.setActions({ButtonAction.CLICK: click})
		adapter.addSubview(b1)
		
		b2 = Button()
		b2.setTag(u'b2')
		b2.setText(u'↱')
		b2.setAttrs({
			ControlState.NORMAL: u'button.normal',
			ControlState.HIGHLIGHTED: u'button.highlighted',
			ControlState.DISABLED: u'button.disabled',
			ControlState.SELECTED: u'button.selected'
		})
		b2.setActions({ButtonAction.CLICK: click})
		adapter.addSubview(b2)
		adapter.addConstraint(b2.left == b1.right + 1)
		b2.becomeFirstResponder()
		
		b3 = Button()
		b3.setTag(u'b3')
		b3.setText(u'⤼')
		b3.setAttrs({
			ControlState.NORMAL: u'button.normal',
			ControlState.HIGHLIGHTED: u'button.highlighted',
			ControlState.DISABLED: u'button.disabled',
			ControlState.SELECTED: u'button.selected'
		})
		b3.setState(ControlState.DISABLED)
		b3.setActions({ButtonAction.CLICK: click})
		adapter.addSubview(b3)
		adapter.addConstraint(b3.left == b2.right + 1)

		b4 = Button()
		b4.setTag(u'b4')
		b4.setText(u'button4')
		b4.setAttrs({
			ControlState.NORMAL: u'button.normal',
			ControlState.HIGHLIGHTED: u'button.highlighted',
			ControlState.DISABLED: u'button.disabled',
			ControlState.SELECTED: u'button.selected'
		})
		b4.setState(ControlState.SELECTED)
		b4.setActions({ButtonAction.CLICK: click})
		adapter.addSubview(b4)
		adapter.addConstraint(b4.left == b3.right + 1)


	sv = SplitView()
	adapter.addSubview(sv)
	adapter.addConstraints([
		sv.width == adapter.width,
		sv.height == adapter.height - 5,
		sv.left == 0,
		sv.top == 5
	])


	s1 = SolidView()
	s1.setAttr(u'highlight')
	
	s2 = SolidView()
	s2.setAttr(u'green')
	
	sv.addSubviews(s1, s2, SplitViewCollapse.VIEW2_CAN_COLLAPSE)

	urwid.set_encoding("utf-8")
	loop = urwid.MainLoop(adapter, palette)
	adapter.mainloop = loop
	loop.screen.set_terminal_properties(colors=256)
	loop.screen.set_mouse_tracking()
	loop.run()

