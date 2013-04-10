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


import enumeration


class Event(object):
	def __init__(self, eventType, modifiers, timestamp, context):
		self.type = eventType
		self.modifiers = modifiers
		self.timestamp = timestamp
		self.context = context


class KeyEventType(enumeration.Enumeration):
	_values_ = [
		(u'KEY_DOWN', 0x10000000),
		u'KEY_UP',
		u'FLAGS_CHANGED'
	]


class KeyEvent(Event):
	def __init__(self, eventType, modifiers, timestamp, context, 
		characters, unmodCharacters, repeat):
		if eventType not in KeyEventType:
			raise ValueError(u'unexpected key event type')
		Event.__init__(self, eventType, modifiers, timestamp, context)
		self.characters = characters
		self.charactersIgnoringModifiers = unmodCharacters
		self.isARepeat = repeat


class MouseEventType(enumeration.Enumeration):
	_values_ = [
		(u'MOUSE_DOWN', 0x20000000),
		u'MOUSE_UP',
		u'RIGHT_MOUSE_DOWN',
		u'RIGHT_MOUSE_UP',
		u'MOUSE_DRAGGED',
		u'RIGHT_MOUSE_DRAGGED',
		u'OTHER_MOUSE_DOWN',
		u'OTHER_MOUSE_UP',
		u'OTHER_MOUSE_DRAGGED',
		u'SCROLL_WHEEL_UP',
		u'SCROLL_WHEEL_DOWN',
		u'MOUSE_MOVED'
	]


class MouseEvent(Event):
	def __init__(self, eventType, modifiers, timestamp, context, 
		location, clickCount, preassure):
		if eventType not in MouseEventType:
			raise ValueError(u'unexpected mouse event type')
		Event.__init__(self, eventType, modifiers, timestamp, context)
		self.locationInContext = location
		self.clickCount = clickCount
		self.preassure = preassure


class EnterExitEventType(enumeration.Enumeration):
	_values_ = [
		(u'MOUSE_ENTERED', 0x40000000),
		u'MOUSE_EXITED'
	]


class EnterExitEvent(Event):
	def __init__(self, eventType, modifiers, timestamp, context):
		if eventType not in EnterExitEventType:
			raise ValueError(u'unexpected enter/exit event type')
		Event.__init__(self, eventType, modifiers, timestamp, context)


