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


from View import View
import enumeration


class ControlState(enumeration.Enumeration):
	_values_ = [
		u'NORMAL',
		u'HIGHLIGHTED',
		u'DISABLED',
		u'SELECTED'
	]


class Control(View):
	def __init__(self):
		View.__init__(self)
		self._state = ControlState.NORMAL
		self._attrs = {}
		for k, v in ControlState:
			self._attrs[k] = None
		self._actions = {}

	def state(self):
		return self._state

	def setState(self, state):
		if state not in ControlState:
			raise ValueError(u'unexpected state')
		self._state = state

	def attrs(self):
		return copy(self._attrs)

	def setAttrs(self, d):
		for k, v in d.iteritems():
			if k not in ControlState:
				raise ValueError(u'unexpected attr key')
			self._attrs[k] = v

	def actions(self):
		return copy(self._actions)

	def setActions(self, d):
		for k, v in d.iteritems():
			if not self.actionIsValidForControl(k):
				raise ValueError(u'unexpected action key')
			self._actions[k] = v

	def actionIsValidForControl(self, action):
		return False


