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


from types import NoneType
from copy import copy


class Point(object):
    u'''Basic point type, used for the origin of components

    x: x value (origin bottom left - 0 based float)
    y: y value (origin bottom left - 0 based float)
    '''
    def __init__(self, x, y):
        u'''Creates a new Point type

        x: x value (origin bottom left - 0 based float)
        y: y value (origin bottom left - 0 based float)
        ''' 
        if not isinstance(x, (NoneType, int, long, float)):
            raise TypeError(u'x must be a number')
        if not isinstance(y, (NoneType, int, long, float)):
            raise TypeError(u'y must be a number')

        self.x = x
        if self.x is not None:
            self.x = float(x)
        self.y = y
        if self.y is not None:
            self.y = float(y)

    def __repr__(self):
        x = "None"
        if self.x is not None:
            x = "%f" % self.x
        y = "None"
        if self.y is not None:
            y = "%f" % self.y
        return u'<Point object with x: %s, y: %s>' % (x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Size(object):
    u'''Basic size type, used to represent a size

    width: width value (float)
    height: height value (float)
    '''
    def __init__(self, width, height):
        u'''Creates a new size type

        width: width value (float)
        height: height value (float)
        '''
        if not isinstance(width, (NoneType, int, long, float)):
            raise TypeError(u'width must be a number')
        if not isinstance(height, (NoneType, int, long, float)):
            raise TypeError(u'height must be a number')

        self.width = width
        if self.width is not None:
            self.width = float(width)
        self.height = height
        if self.height is not None:
            self.height = float(height)

    def __repr__(self):
        width = "None"
        if self.width is not None:
            width = "%f" % self.width
        height = "None"
        if self.height is not None:
            height = "%f" % self.height
        return u'<Size object with width: %s, height: %s>' % (width, height)

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height


class Rect(object):
    u'''Basic rectangle type, combines a origin and size

    origin: a Point type which represents the top-left point
    size: a Size type which represents the size of the rectangle
    '''
    def __init__(self, x=None, y=None, width=None, height=None, 
                 origin=None, size=None):
        u'''Creates a new Rect type - optionally setting the origin and size

        You only specify x/y or origin, and width/height or size.  If you do 
        specify both, origin and size take precedence over x/y and width/height.
        
        x: None, or x value (origin bottom left - 0 based float)
        y: None, or y value (origin bottom left - 0 based float)
        width: None, or width value (float)
        height: None, or height value (float)
        origin: None, or a Point object (which we copy)
        size: None, or a Size object (which we copy)
        '''        
        self.origin = Point(x, y)
        self.size = Size(width, height)
        if origin is not None:
            self.origin = copy(origin)
        if size is not None:
            self.size = copy(size)

    def __repr__(self):
        return u'<Rect object with %s, %s >' % (self.origin, self.size)

    def __eq__(self, other):
        return self.origin == other.origin and self.size == other.size

    def get_min_x(self):
        u'''Returns the smallest value for the x coordinate'''
        return min(self.origin.x, self.origin.x + self.size.width)

    def get_max_x(self):
        u'''Returns the largest value for the x coordinate'''
        return max(self.origin.x, self.origin.x + self.size.width)

    def get_min_y(self):
        u'''Returns the smallest value for the y coordinate'''
        return min(self.origin.y, self.origin.y + self.size.height)

    def get_max_y(self):
        u'''Returns the largest value for the y coordinate'''
        return max(self.origin.y, self.origin.y + self.size.height)

