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


from Control import Control
from Rect import *
from Layout import *
import enumeration
from kitchen.text.display import *
import urwid


class TextAlign(enumeration.Enumeration):
	_values_ = [
		u'LEFT',
		u'RIGHT',
		u'CENTER',
		u'NATURAL'
	]


class LineBreak(enumeration.Enumeration):
	_values_ = [
		u'WORD_WRAP',
		u'HEAD_TRUNCATION',
		u'TAIL_TRUNCATION',
		u'MIDDLE_TRUNCATION'
	]


class Label(Control):
	def __init__(self):
		Control.__init__(self)
		self._text = u''
		self._padding = (0, 0)
		self._textAlign = TextAlign.NATURAL
		self._lineBreak = LineBreak.TAIL_TRUNCATION
		self._labelWidth = None
		self._labelHeight = self.height >= 1
		self.addConstraint(self._labelHeight)

	def text(self):
		return self._text[self._padding[0]:-self._padding[1]]

	def setText(self, text):
		self._text = (u' ' * self._padding[0]) + text + (u' ' * self._padding[1])
		if self._labelWidth in self._constraints:
			self.removeConstraint(self._labelWidth)
		self._labelWidth = self.width >= textual_width(self._text)
		self._labelWidth.strength = LayoutStrength.WEAK
		self.addConstraint(self._labelWidth)		

	def padding(self):
		return copy(self._padding)

	def setPadding(self, padding):
		if len(padding) != 2:
			raise TypeError(u'padding must be a tuple with two entries')
		text = self.text()
		self._padding = copy(padding)
		self.setText(text)

	def textAlign(self):
		return self._textAlign

	def setTextAlign(self, align):
		if align not in TextAlign:
			raise ValueError(u'unexpected TextAlign value')
		self._textAlign = align

	def lineBreak(self):
		return self._lineBreak

	def setLineBreak(self, linebreak):
		if linebreak not in LineBreak:
			raise ValueError(u'unexpected LineBreak value')
		self._lineBreak = linebreak

	def _lineBrokenText(self):
		width = self.width.intval
		pad = u'..'
		# do line breaking
		if self._lineBreak == LineBreak.WORD_WRAP:
			retval = wrap(self._text, width)

		else:
			if textual_width(self._text) <= width:
				retval = [self._text]
	
			elif self._lineBreak == LineBreak.HEAD_TRUNCATION:
				retval = [pad + self._truncateTextHead(width - len(pad))]

			elif self._lineBreak == LineBreak.TAIL_TRUNCATION:
				retval = [self._truncateTextTail(width - len(pad)) + pad]

			elif self._lineBreak == LineBreak.MIDDLE_TRUNCATION:
				# truncate at front, and back then add ... in the middle
				w = width - len(pad)
				frontWidth = int(w / 2)
				backWidth = w - frontWidth
				front = self._truncateTextTail(frontWidth)
				back = self._truncateTextHead(backWidth)
				retval = [front + pad + back]
		return retval

	def _truncateTextHead(self, width):
		# spool backwards through string until length is right
		retval = self._text
		last = u''
		for c in self._text[::-1]:
			cur = c + last
			if textual_width(cur) > width:
				retval = last
				break
			last = cur
		return retval

	def _truncateTextTail(self, width):
		# spool forwards through string until length is right
		retval = self._text
		last = u''
		for c in self._text:
			cur = last + c
			if textual_width(cur) > width:
				retval = last
				break
			last = cur	
		return retval	

	# View Methods
	def drawRect(self, rect):
		lines = self._lineBrokenText()
		lines = lines[:self.height.intval] # trim to height

		# handle text alignment
		txt = []
		for line in lines:
			if (   self._textAlign == TextAlign.NATURAL
				or self._textAlign == TextAlign.LEFT
				or self._textAlign == TextAlign.RIGHT):
				txt.append(
					textual_width_fill(
						line, 
						self.width.intval, # pad out to width
						left=(self._textAlign != TextAlign.RIGHT)
					).encode(u'utf-8')
				)
			else:
				# center
				w = self.width.intval - textual_width(line)
				left = int(w / 2)
				right = w - left
				txt.append(
					(
						  textual_width_fill(u'', left)
						+ line 
						+ textual_width_fill(u'', right)
					).encode(u'utf-8')
				)
		canvas = urwid.TextCanvas(txt)
		canvas = urwid.CompositeCanvas(canvas)
		attr = self._attrs[self._state]
		if attr is not None:
			canvas.fill_attr(attr)
		xy = self.convertPointToView(
			Point(x=0, y=0)
		)
		self.context().canvas.overlay(
			canvas,
			xy.x,
			xy.y
		)

	def sizeThatFits(self, size):
		retval = None
		if size is None:
			retval = Size(
				textual_width(self._text), 
				int(self._labelHeight.rhs.value)
			)
		elif size.width is not None:
			retval = Size(size.width, len(wrap(self._text, size.width)))
		elif size.height is not None:
			# we'll do this iterativly - its a slow but the best we can do 
			# with kitchenAPI
			width = self.sizeThatFits(None).width
			lastwidth = width
			for i in range(width, 0, -1):
				if len(wrap(s, i)) > size.height:
					break
				lastwidth = i
			retval = Size(lastwidth, size.height)
		return retval







