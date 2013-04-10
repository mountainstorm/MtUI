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


from Responder import Responder
from Rect import *
from copy import deepcopy
from Layout import *


class ViewConstraints(object):
	def __init__(self):
		self.left = None
		self.top = None
		self.width = None
		self.height = None
		self.right = None
		self.bottom = None


class View(Responder):
	# Initializing a View Object
	def __init__(self):
		Responder.__init__(self)
		self._window = None
		self._superview = None
		self._needsDisplay = None
		self._needsLayout = True
		self._subviews = []
		self._constraints = [] #set()
		self._needsUpdateConstraints = True
		self._tag = None

		self.top = LayoutVariable(self, u'top')
		self.left = LayoutVariable(self, u'left')
		self.bottom = LayoutVariable(self, u'bottom')
		self.right = LayoutVariable(self, u'right')
		self.width = LayoutVariable(self, u'width')
		self.height = LayoutVariable(self, u'height')

		self._frame = ViewConstraints()
		self._frame.right = self.right == self.left + self.width
		self._frame.bottom = self.bottom == self.top + self.height
		self.addConstraints([self._frame.right, self._frame.bottom])
		
	def __repr__(self):
		tag = self._tag.__repr__()
		if tag is None:
			tag = u'None'
		return u'<%s object with rect: %s and tag %s>' % (
			self.__class__.__name__, 
			self.frame(),
			tag
		)

	# frame Rectangles
	def frame(self):
		return Rect(
			x=self.left.intval, 
			y=self.top.intval,
			width=self.width.intval,
			height=self.height.intval
		)

	def frameConstraints(self):
		retval = Rect()
		if self._frame.left is not None:
			retval.origin.x = self._frame.left.rhs.constant
		if self._frame.top is not None:
			retval.origin.y = self._frame.top.rhs.constant
		if self._frame.width is not None:
			retval.size.width = self._frame.width.rhs.constant
		if self._frame.height is not None:
			retval.size.height = self._frame.height.rhs.constant
		return retval

	def setFrameConstraints(self, frameRect):
		# update all the constrains
		if self._frame.left is not None and self._frame.left in self._constraints:
			self.removeConstraint(self._frame.left)
		if frameRect.origin.x is not None:
			self._frame.left = self.left == frameRect.origin.x
			self.addConstraint(self._frame.left)

		if self._frame.top is not None and self._frame.top in self._constraints:
			self.removeConstraint(self._frame.top)
		if frameRect.origin.y is not None:
			self._frame.top = self.top == frameRect.origin.y
			self.addConstraint(self._frame.top)

		if self._frame.width is not None and self._frame.width in self._constraints:
			self.removeConstraint(self._frame.width)
		if frameRect.size.width is not None:
			self._frame.width = self.width == frameRect.size.width
			self.addConstraint(self._frame.width)

		if self._frame.height is not None and self._frame.height in self._constraints:
			self.removeConstraint(self._frame.height)
		if frameRect.size.height is not None:
			self._frame.height = self.height == frameRect.size.height
			self.addConstraint(self._frame.height)

	# Managing the View Hierarchy
	def superview(self):
		return self._superview

	def subviews(self):
		return self._subviews.copy()

	def window(self):
		return self._window

	def addSubview(self, view):
		self.insertSubviewAtIndex(view, len(self._subviews))

	def bringSubviewToFront(self, view):
		try:
			self._subviews.remove(view)
			self._subviews.append(view)
		except ValueError:
			raise ValueError(u'view not a subview')

	def sendSubviewToBack(self, view):
		try:
			self._subviews.remove(view)
			self._subviews.insert(0, view)
		except ValueError:
			raise ValueError(u'view not a subview')

	def removeFromSuperview(self):
		if self._superview is not None:
			responder = self._window.firstResponder()
			while responder is not None:
				if responder == self:
					self._window.makeFirstResponder(self._window)
					break
				responder = responder._superview

			self._superview.willRemoveSubview(self)
			self._willMoveToWindow(None)
			self.willMoveToSuperview(None)
			
			self._superview._subviews.remove(self)
			self._superview = None
			self._window = None
			if self._superview is not None:
				self._superview.setNeedsDisplay()

			self._didMoveToWindow()
			self.didMoveToSuperview()			

	def insertSubviewAtIndex(self, view, idx):
		if view is None:
			raise ValueError(u'Adding a None subview')

		if self.isDescendantOf(view):
			raise ValueError(u'Loop in the view tree')

		if idx < 0 or idx > len(self._subviews):
			raise ValueError(u'Index must be between 0 and len(subviews)')

		view.removeFromSuperview()
		view._willMoveToWindow(self._window)
		view.willMoveToSuperview(self)

		self._subviews.insert(idx, view)
		view._superview = self
		view._window = self._window
		view.setNeedsDisplay()

		view._didMoveToWindow()
		view.didMoveToSuperview()
		self.didAddSubview(view)

	def insertSubviewAboveSubview(self, view, otherView):
		if otherView is None:
			raise ValueError(u'otherView is None')

		if view == otherView:
			raise ValueError(u'view == otherView')

		try:
			idx = self._subviews.index(otherView)
			idx += 1
		except ValueError:
			raise ValueError(u'view not a subview')
		self.insertSubviewAtIndex(view, idx)

	def insertSubviewBelowSubview(self, view, otherView):
		if otherView is None:
			raise ValueError(u'otherView is None')

		if view == otherView:
			raise ValueError(u'view == otherView')

		try:
			idx = self._subviews.index(otherView)
		except ValueError:
			raise ValueError(u'view not a subview')
		self.insertSubviewAtIndex(view, idx)

	def exchangeSubviewAtIndexwithSubviewAtIndex(self, idx1, idx2):
		if (   idx1 < 0 
			or idx1 >= len(self._subviews) 
			or idx2 < 0
			or idx2 >= len(self._subviews)):
			raise ValueError(u'index not in range')
		item2 = self._subviews[idx2]
		item1 = self._subviews.pop(idx1)
		self._subviews.insert(idx1, item2)
		self._subviews.pop(idx2)
		self._subviews.inset(idx2, item1)

	def isDescendantOf(self, view):
		if self == view:
			return True
		if self._superview is None:
			return False
		if self._superview == view._superview:
			return True
		return self._superview.isDescendantOf(view)

	# Configuring the Resizing Behavior
	def sizeThatFits(self, size):
		return self.frame().size

	def sizeToFit(self):
		rect = self.frame()
		rect.size = sizeThatFits(None)
		self.setFrameConstraints(rect)

	# Laying out Subviews
	def layoutSubviews(self):
		self.setNeedsUpdateConstraints()
		for view in self._subviews:
			view._layoutSubviews()

	def setNeedsLayout(self):
		self._needsLayout = True
		for view in self._subviews:
			view.setNeedsLayout()

	def layoutIfNeeded(self):
		if self._needsLayout:
			top = self
			while top._superview is not None and top._superview._needsLayout:
				top = top._superview
			top._layoutSubviews()
			top.updateConstraintsIfNeeded()
			layout_update(top._gatherConstraints())

	# Managing Constraints
	def addConstraint(self, constraint):
		# We're going to test that all variables in this constraint are 
		# from desendent views of this one
		for var in layout_variables(constraint):
			if not var.view.isDescendantOf(self):
				raise ValueError(
					  u'LayoutVariable\'s view is not a descedant: ' 
					+ var.view.__str__()
					+ u' '
					+ self.__str__()
				)
		self._constraints.append(constraint)

	def addConstraints(self, constraints):
		for constraint in constraints:
			self.addConstraint(constraint)

	def removeConstraint(self, constraint):
		self._constraints.remove(constraint)

	def removeConstraints(self, constraints):
		for constraint in set(constraints):
			self.removeConstraint(constraint)

	# Triggering Constraint-Based Layout
	def updateConstraints(self):
		pass

	def setNeedsUpdateConstraints(self):
		self._needsUpdateConstraints = True

	def updateConstraintsIfNeeded(self):
		if self._needsUpdateConstraints:
			self.updateConstraints()
			# clear everything below us
			self._needsUpdateConstraints = False
		for view in self._subviews:
			view.updateConstraintsIfNeeded()

	# Drawing and Updating the View
	def drawRect(self, rect):
		pass

	def setNeedsDisplay(self):
		self._needsDisplay = True
		for view in self._subviews:
			view.setNeedsDisplay()		

	def setNeedsDisplayInRect(self, rect):
		if self._needsDisplay is None:
			self._needsDisplay = []
		if isinstance(self._needsDisplay, list):
			self._needsDisplay.append(rect)

	def displayIfNeeded(self):
		if self._needsDisplay is not None:
			if isinstance(self._needsDisplay, list):
				for rect in self._needsDisplay:
					self.drawRect(rect)
			else:
				self.drawRect(self._frame)
			self._needsDisplay = None
		for view in self._subviews:
			view.displayIfNeeded()

	# Identifying the View at Runtime
	def tag(self):
		return self._tag

	def setTag(self, tag):
		self._tag = tag

	def viewWithTag(self, tag):
		retval = None
		if self._tag is not None and self._tag == tag:
			retval = self
		else:
			for view in self._subviews:
				retval = view.viewWithTag(tag)
				if retval is not None:
					break
		return retval

	# Converting Between View Coordinate Systems
	def convertPointToView(self, point, view=None):
		retval = self._convertPointToWindow(point)
		if view is not None:
			retval = view._convertPointFromWindow(retval)
		return retval

	def convertPointFromView(self, point, view=None):
		retval = copy(point)
		if view is not None:
			retval = view._convertPointToWindow(point)
		retval = self._convertPointFromWindow(retval)
		return retval

	def _convertPointFromWindow(self, point):
		new = copy(point)
		cur = self
		while cur is not self._window:
			new.x -= cur.left.intval
			new.y -= cur.top.intval
			cur = cur._superview
		return new

	def _convertPointToWindow(self, point):
		new = copy(point)
		cur = self
		while cur is not self._window:
			new.x += cur.left.intval
			new.y += cur.top.intval
			cur = cur._superview
		return new

	# Hit Testing in a View
	def pointInsideWithEvent(self, point, event):
		retval = False
		if (    point.x >= self.left.intval 
			and point.x < (self.left.intval + self.width.intval)
			and point.y >= self.top.intval 
			and point.y < (self.top.intval + self.height.intval)):
			retval = True
		return retval

	def hitTestWithEvent(self, point, event):
		retval = self
		# reverse the subviews so the last one (the top one) is tested first
		for view in self._subviews[::-1]:
			if view.pointInsideWithEvent(point, event):
				retval = view
				p = self.convertPointToView(point, view)
				v = view.hitTestWithEvent(p, event)
				if v is not None:
					retval = v
				break
		return retval

	# TODO methods
	# clipsToBounds
	# convertRect:toView:
	# convertRect:fromView:

	# Observing View-Related Changes
	def didAddSubview(self, subview):
		pass

	def willRemoveSubview(self, subview):
		pass

	def willMoveToSuperview(self, superview):
		pass

	def didMoveToSuperview(self):
		pass

	def willMoveToWindow(self, window):
		pass

	def didMoveToWindow(self):
		pass

	# Responder methods
	def nextResponder(self):
		# TODO: return controller, if present
		return self._superview

	def isFirstResponder(self):
		if self._window is None:
			raise ValueError(
				u'View is not part of a view hierarchy: ' + self.__repr__()
			)
		return self._window.firstResponder() == self
		
	def canBecomeFirstResponder(self):
		return False

	def becomeFirstResponder(self):
		retval = False
		if self._window is None:
			raise ValueError(
				u'View is not part of a view hierarchy: ' + self.__repr__()
			)
		fr = self._window.firstResponder()
		if self.canBecomeFirstResponder():
			if fr is None or fr.resignFirstResponder():
				self._window._firstResponder = self
				retval = True
		return retval

	def canResignFirstResponder(self):
		return True

	def resignFirstResponder(self):
		if self._window is None:
			raise ValueError(
				u'View is not part of a view hierarchy: ' + self.__repr__()
			)
		fr = self._window.firstResponder()
		if fr != self:
			raise ValueError(
				u'Unable to resign first responder, as object is not first responder: ' + self.__repr__()
			)
		retval = self.canResignFirstResponder()
		if reval:
			self._window._firstResponder = None
			retval = True
		return retval

	# handle propogaton of changing window
	def _willMoveToWindow(self, window):
		self.willMoveToWindow(window)
		self._window = window
		for view in self._subviews:
			view._willMoveToWindow(window)

	def _didMoveToWindow(self):
		self.didMoveToWindow()
		for view in self._subviews:
			view._didMoveToWindow()

	def _layoutSubviews(self):
		self.layoutSubviews()
		self._needsLayout = False

	def _gatherConstraints(self):
		retval = copy(self._constraints)
		for view in self._subviews:
			retval += view._gatherConstraints()
		return retval

