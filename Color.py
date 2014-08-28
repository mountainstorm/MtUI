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


from types import *


class Color(object):
    @classmethod
    def from_hex(cls, col):
        if not isinstance(col, StringTypes):
            raise TypeError(u'Invalid color specifier type; expected a string')
        if (    len(col) != len(u'#rrggbb')
            and len(col) != len(u'#rrggbbaa')
            and col[0] != u'#'):
            raise TypeError(u'Invalid color specifier; should be #rrggbb')
        red = int(col[1:3], 16)
        green = int(col[3:5], 16)
        blue = int(col[5:7], 16)
        alpha = 255
        if len(col) == len(u'#rrggbbaa'):
            alpha = int(col[7:9], 16)
        return Color(red / 255.0, green / 255.0, blue / 255.0, alpha / 255.0)

    def __init__(self, red, green, blue, alpha=1.0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        
    def blended_color(self, fraction, color):
        raise NotImplementedError(u'blended_color')

    def highlight(self, level):
        raise NotImplementedError(u'highlight')

    def shadow(self, level):
        raise NotImplementedError(u'shadow')


# define default colors
Color.BLACK   = Color.from_hex(u'#000000')
Color.RED     = Color.from_hex(u'#ff0000')
Color.GREEN   = Color.from_hex(u'#00ff00')
Color.YELLOW  = Color.from_hex(u'#ffff00')
Color.BLUE    = Color.from_hex(u'#0000ff')
Color.MAGENTA = Color.from_hex(u'#ff00ff')
Color.CYAN    = Color.from_hex(u'#00ffff')
Color.WHITE   = Color.from_hex(u'#ffffff')
