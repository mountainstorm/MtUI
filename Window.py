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
from Responder import Responder


class Window(View):
	def __init__(self):
		View.__init__(self)
		self._firstResponder = None
		self._window = self
		self._application = None
		self._screen = None

	# Config
	def screen(self):
		return self._screen

	# First Responder management
	def firstResponder(self):
		return self._firstResponder

	# View methods
	def hitTestWithEvent(self, point, event):
		retval = None
		if self.pointInsideWithEvent(point, event):
			retval = View.hitTestWithEvent(self, point, event)
		return retval

	# Making Windows Key
	def isKeyWindow(self):
		if self._application is None:
			raise ValueError(
				u'Window is not liked to an application ' + self.__repr__()
			)
		return self._application.keyWindow() == self
		
	def canBecomeKeyWindow(self):
		return False

	def becomeKeyWindow(self):
		retval = False
		if self._application is None:
			raise ValueError(
				u'Window is not linked to an application ' + self.__repr__()
			)
		kw = self._application.keyWindow()
		if self.canBecomeKeyWindow():
			if kw is None or kw.resignKeyWindow():
				self._application._keyWindow = self
				retval = True
		return retval

	def canResignKeyWindow(self):
		return True

	def resignKeyWindow(self):
		if self._application is None:
			raise ValueError(
				u'Window is not linked to an application ' + self.__repr__()
			)
		kw = self._application.keyWindow()
		if kw != self:
			raise ValueError(
				u'Unable to resign key window, as window is not key window ' + self.__repr__()
			)
		retval = self.canResignKeyWindow()
		if reval:
			self._application._keyWindow = None
			retval = True
		return retval

	# Linking to application
	def removeFromApplication(self):
		if self._application is not None:
			key = self._application.keyWindow()
		
			self._application.willRemoveWindow(self)
			self.willMoveToApplication(None)
			
			self._application._windows.remove(self)
			self._application = None

			self.didMoveToApplication()	

	# Observing application changes
	def willMoveToApplication(self, application):
		pass

	def didMoveToApplication(self):
		pass

	# prevent adding this into other views
	def willMoveToSuperview(self, superview):
		raise TypeError(u'Window cant be added to other views')

	def willMoveToWindow(self, window):
		raise TypeError(u'Window cant be added to other window')

	# we'll set nextResponder to the firstResponder - so that we deliver all 
	# events go to the right window
	def nextResponder(self):	
		return self._firstResponder


