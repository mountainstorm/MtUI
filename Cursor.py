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


from Application import *
import pyglet


class Cursor(object):
	DEFAULT   	    = pyglet.window.Window.CURSOR_DEFAULT
	CROSSHAIR       = pyglet.window.Window.CURSOR_CROSSHAIR
	HAND 	        = pyglet.window.Window.CURSOR_HAND
	HELP 	        = pyglet.window.Window.CURSOR_HELP
	NO 		        = pyglet.window.Window.CURSOR_NO
	SIZE            = pyglet.window.Window.CURSOR_SIZE
	SIZE_DOWN       = pyglet.window.Window.CURSOR_SIZE_DOWN
	SIZE_DOWN_LEFT  = pyglet.window.Window.CURSOR_SIZE_DOWN_LEFT
	SIZE_DOWN_RIGHT = pyglet.window.Window.CURSOR_SIZE_DOWN_RIGHT
	SIZE_LEFT       = pyglet.window.Window.CURSOR_SIZE_LEFT
	SIZE_LEFT_RIGHT = pyglet.window.Window.CURSOR_SIZE_LEFT_RIGHT
	SIZE_RIGHT      = pyglet.window.Window.CURSOR_SIZE_RIGHT
	SIZE_UP			= pyglet.window.Window.CURSOR_SIZE_UP
	SIZE_UP_DOWN    = pyglet.window.Window.CURSOR_SIZE_UP_DOWN
	SIZE_UP_LEFT    = pyglet.window.Window.CURSOR_SIZE_UP_LEFT
	SIZE_UP_RIGHT   = pyglet.window.Window.CURSOR_SIZE_UP_RIGHT
	TEXT            = pyglet.window.Window.CURSOR_TEXT
	WAIT            = pyglet.window.Window.CURSOR_WAIT
	WAIT_ARROW      = pyglet.window.Window.CURSOR_WAIT_ARROW

	_custom_cursors = {}

	@classmethod
	def set_cursor(cls, cursor):
		win = Application.shared_application().windows()[0]._pyglet
		if cursor in cls._custom_cursors:
			csr = cls._custom_cursors[cursor]
		else:
			csr = win.get_system_mouse_cursor(cursor)
		win.set_mouse_cursor(csr)

	@classmethod
	def set_default(cls):
		win = Application.shared_application().windows()[0]._pyglet
		csr = win.get_system_mouse_cursor(Cursor.DEFAULT)
		win.set_mouse_cursor(csr)

	@classmethod
	def save_cursor(cls, name, img):
		cls._custom_cursors[name] = img
