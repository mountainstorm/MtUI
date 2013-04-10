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
from Rect import *
import urwid


class SolidView(View):
	def __init__(self):
		View.__init__(self)
		self._attr = None

	def attr(self):
		return self._attr

	def setAttr(self, attr):
		self._attr = attr

	# View Methods
	def drawRect(self, rect):
		canvas = urwid.SolidCanvas(u' ', self.width.intval, self.height.intval)
		canvas = urwid.CompositeCanvas(canvas)
		canvas.fill_attr(self._attr)
		xy = self.convertPointToView(
			Point(x=0, y=0)
		)
		self.context().canvas.overlay(
			canvas,
			xy.x,
			xy.y
		)