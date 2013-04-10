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


class Responder(object):
	# Managing the Responder Chain
	def nextResponder(self):
		return None

	# Responding to Mouse Events
	def mouseDown(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().mouseDown(event)

	def mouseDragged(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().mouseDragged(event)

	def mouseUp(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().mouseUp(event)

	def mouseMoved(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().mouseMoved(event)

	def mouseEntered(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().mouseEntered(event)

	def mouseExited(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().mouseExited(event)

	def rightMouseDown(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().rightMouseDown(event)

	def rightMouseDragged(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().rightMouseDragged(event)

	def rightMouseUp(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().rightMouseUp(event)

	def otherMouseDown(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().otherMouseDown(event)

	def otherMouseDragged(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().otherMouseDragged(event)

	def otherMouseUp(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().otherMouseUp(event)

	# Responding to Key Events
	def keyDown(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().keyDown(event)

	def keyUp(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().keyUp(event)

	# Responding to Other Kinds of Events
	def flagsChanged(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().flagsChanged(event)

	def scrollWheel(self, event):
		if self.nextResponder() is not None:
			self.nextResponder().scrollWheel(event)

	# TODO: do we want a customEvent handler?

	# Validating Commands
	def canPerformAction(action, sender):
		retval = True
		if action not in self.__dict__:
			retval = False
			if self.nextResponder() is not None:
				retval = self.nextResponder().canPerformAction(action, sender)
		return retval
