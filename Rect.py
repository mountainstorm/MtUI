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


from copy import copy


class Point(object):
	"""Basic point type, used for the origin of compoenents

	x: None, or a zero indexed value representing the left-right offset from 
	   the origin at top left
	y: None, or a zero indexed value representing the top-bottom offset from 
	   the origin at top left
	"""
	def __init__(self, x=None, y=None):
		"""Creates a new Point type

		x: None, or a zero indexed value representing the left-right offset from 
	   	   the origin at top left
		y: None, or a zero indexed value representing the top-bottom offset from 
	       the origin at top left
	    """
		self.x = x
		self.y = y

	def __repr__(self):
		return u'<Point object with x: %d, y: %d>' % (self.x, self.y)


class Size(object):
	"""Basic size type, used to represent a size

	width: None, or the width of an item
	height: None, or the height of an item
	"""
	def __init__(self, width=None, height=None):
		"""Creates a new size type

		width: None, or the width of an item
		height: None, or the height of an item
		"""
		self.width = width
		self.height = height

	def __repr__(self):
		return u'<Size object with width: %d, height: %d>' % (self.width, self.height)


class Rect(object):
	"""Basic rectangle type, combines a origin and size

	origin: a Point type which represents the offset from top-left
	size: a Size type which represents the size of the rectangle
	"""
	def __init__(self, x=None, y=None, width=None, height=None, origin=None, size=None):
		"""Creates a new Rect type - optionally setting the origin and size

		Typically you should only specify x/y or origin, and width/height or 
		size.  If you do specify both origin and size take precedence over x/y
		width/height.
		
		x: None, or a zero indexed value representing the left-right offset from 
	   	   the origin at top left
		y: None, or a zero indexed value representing the top-bottom offset from 
	   	   the origin at top left
		width: None, or the width of an item
		height: None, or the height of an item
		origin: None, or a Point object (which we copy)
		size: None, or a Size object (which we copy)
		"""	   	   
		self.origin = Point(x, y)
		self.size = Size(width, height)
		if origin is not None:
			self.origin = copy(origin)
		if size is not None:
			self.size = copy(size)

	def __repr__(self):
		return u'<Rect object with %s, %s >' % (self.origin, self.size)

