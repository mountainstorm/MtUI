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


from Label import *
from Control import *
from kitchen.text.display import *
import enumeration
import urwid


class ButtonAction(enumeration.Enumeration):
	_values_ = [
		u'CLICK'
	]


class Button(Label):
	def __init__(self):
		Label.__init__(self)
		self.setPadding((1, 1))
		self._textAlign = TextAlign.CENTER
		self._lineBreak = LineBreak.MIDDLE_TRUNCATION
		self._previousState = None

	def canBecomeFirstResponder(self):
		return True

	def becomeFirstResponder(self):
		retval = Label.becomeFirstResponder(self)
		if retval:
			if self._state != ControlState.DISABLED:
				self._state = ControlState.HIGHLIGHTED
		return retval

	def resignFirstResponder(self):
		retval = Label.resignFirstResponder(self)
		if retval:
			if self._state != ControlState.DISABLED:
				self._state = ControlState.NORMAL	
		return retval

	# Responder methods
	def mouseDown(self, event):
		if self._state != ControlState.DISABLED:
			self._state = ControlState.SELECTED
			self.setNeedsDisplay()

	def mouseUp(self, event):
		if self._state != ControlState.DISABLED:
			self._state = ControlState.HIGHLIGHTED
			self.setNeedsDisplay()
			self._actions[ButtonAction.CLICK](self)

	def mouseEntered(self, event):
		if self._state != ControlState.DISABLED:
			self._previousState = self._state
			self._state = ControlState.HIGHLIGHTED
			self.setNeedsDisplay()

	def mouseExited(self, event):
		if self._state != ControlState.DISABLED:
			self._state = self._previousState
			self._previousState = None
			self.setNeedsDisplay()

	def keyDown(self, event):
		# TODO: check for correct key
		if self._state != ControlState.DISABLED:
			self._state = ControlState.SELECTED
			self.setNeedsDisplay()

	def keyUp(self, event):
		if self._state == ControlState.SELECTED:
			self._state = ControlState.HIGHLIGHTED
			self.setNeedsDisplay()
			self._actions[ButtonAction.CLICK](self)

	# Control methods
	def actionIsValidForControl(self, action):
		return action in ButtonAction

