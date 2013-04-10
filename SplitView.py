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
from Layout import *
from Event import *
import enumeration
import urwid


class SplitViewCollapse(enumeration.Enumeration):
	_values_ = [
		u'NONE_COLLAPSE',
		u'VIEW1_CAN_COLLAPSE',
		u'VIEW2_CAN_COLLAPSE'
	]


class SplitView(View):
	def __init__(self):
		View.__init__(self)
		self._vertical = True
		self._dividerStyle = u'│'
		self._dividerAttr = None

		self._dividerConstraint = None
		self._otherConstraints = None
		self._collapsed = None # stores the ratio when we are collapsed
		self._collapse = SplitViewCollapse.NONE_COLLAPSE
		self._leftView = None
		self._avail = None

	def dividerStyle(self):
		return self._dividerStyle

	def setDividerStyle(self, style):
		self._dividerStyle = style

	def dividerAttr(self):
		return self._dividerAttr

	def setDividerAttr(self, attr):
		self._dividerAttr = attr

	def setCollapse(self, collapse=True):
		if collapse:
			self._collapsed = self._dividerConstraint.rhs.terms[0].coeff
			self.setDivide(0.0)
		else:
			if self._collapsed is not None:
				self.setDivide(self._collapsed)
				self._collapsed = None

	def setDivide(self, ratio):
		if self._dividerConstraint is not None:
			self.removeConstraint(self._avail)
			self.removeConstraint(self._dividerConstraint)

		avail = LayoutVariable(self, u'avaliable-space')
		if self._vertical:
			self._avail = avail == self.width - 1
			self.addConstraint(self._avail)
			self._dividerConstraint = (
				self._subviews[1].width == avail * ratio
			)
		else:
			self._avail = avail == self.height - 1
			self.addConstraint(self._avail)
			self._dividerConstraint = (
				self._subviews[1].height == avail * ratio
			)
		self._dividerConstraint.strength = LayoutStrength.STRONG
		self.addConstraint(self._dividerConstraint)
		self.setNeedsLayout()
		self.setNeedsUpdateConstraints()
		self.setNeedsDisplay()

	# drawing the divider - allows subclasses to draw custom dividers
	def drawDividerInRect(self, rect):
		# draw the divider
		canvas = urwid.SolidCanvas(self._dividerStyle,
			rect.size.width,
			rect.size.height
		)
		canvas = urwid.CompositeCanvas(canvas)

		# draw the toggle
		if self._collapse != SplitViewCollapse.NONE_COLLAPSE:
			if self._vertical:
				loc = Point(0, 1)
			else:
				loc = Point(1, 0)

			if self._collapsed is None:
				toggle = u'-'
			else:
				toggle = u'+'
			toggleCanvas = urwid.SolidCanvas(toggle, 1, 1)
			toggleCanvas = urwid.CompositeCanvas(toggleCanvas)
			canvas.overlay(toggleCanvas, loc.x, loc.y)

		# composite if onto the view
		if self._dividerAttr is not None:
			canvas.fill_attr(self._dividerAttr)
		xy = self.convertPointToView(
			Point(x=rect.origin.x, y=rect.origin.y)
		)
		self.context().canvas.overlay(canvas, xy.x, xy.y)

	# View methods
	def displayIfNeeded(self):
		needDisplay = self._needsDisplay
		View.displayIfNeeded(self)
		if needDisplay is not None:
			if self._vertical:
				self.drawDividerInRect(Rect(
					self._leftView.width.intval, 
					0, 
					1, 
					self.height.intval
				))
			else:
				self.drawDividerInRect(Rect(
					0, 
					self._leftView.height.intval,
					self.width.intval, 
					1
				))

	def addSubviews(self, view1, view2, collapse, vertical=True):
		if collapse not in SplitViewCollapse:
			raise TypeError(u'Invalid collapse type')

		if 0:
			# remove all the existing bits and bobs
			for view in self._subviews:
				view.removeFromSuperview()
			self._vertical = vertical

			if self._dividerConstraint is not None:
				self.removeConstraint(self._dividerConstraint)
			if self._otherConstraints is not None:
				self.removeConstraints(self._otherConstraints)

			# create the constraints
		constraints = []		
		if 1:
			if self._vertical:
				constraints.append(view1.top == 0)
				constraints.append(view1.height == self.height)
				constraints.append(view1.left == 0)
				constraints.append(view1.width >= 0)
				constraints.append(view1.width <= self.width - 1)

				constraints.append(view2.top == 0)
				constraints.append(view2.height == self.height)
				constraints.append(view2.right == self.width) # TODO: why can't we specify self.right
				constraints.append(view2.width >= 0)
				constraints.append(view2.width <= self.width - 1)

				# the combined size is a weak constraint so we can collapse
				c = self.width == view1.width + 1 + view2.width
				c.strength = LayoutStrength.MEDIUM
				constraints.append(c)
			else:
				constraints.append(view1.left == 0)
				constraints.append(view1.width == self.width)
				constraints.append(view1.top == 0)
				constraints.append(view1.height >= 0)
				constraints.append(view1.height <= self.height - 1)

				constraints.append(view2.left == 0)
				constraints.append(view2.width == self.width)
				constraints.append(view2.bottom == self.height) # TODO: why can't we specify self.bottom
				constraints.append(view2.height >= 0)
				constraints.append(view2.height <= self.height - 1)

				# the combined size is a weak constraint so we can collapse
				c = self.height == view1.height + 1 + view2.height
				c.strength = LayoutStrength.WEAK
				constraints.append(c)

		# add the views - make sure if ones collapsable it goes last 
		# (so it can overlap)
		self._leftView = view1
		if collapse == SplitViewCollapse.VIEW2_CAN_COLLAPSE:
			View.addSubview(self, view2)
			View.addSubview(self, view1)
		else:
			# view 2 or none collapse
			View.addSubview(self, view1)
			View.addSubview(self, view2)

		# add the constraints
		self._otherConstraints = constraints
		self.addConstraints(self._otherConstraints)
		self.setDivide(0.6)
		self._collapse = collapse

	# prevent default subview manipulation
	def addSubview(self, view):
		raise TypeError(u'SplitView does not support adding directly')

	def bringSubviewToFront(self, view):
		raise TypeError(u'SplitView does not support reordering views')

	def sendSubviewToBack(self, view):
		raise TypeError(u'SplitView does not support reordering views')

	# TODO: remove or only allow via addSubviews
	#def insertSubviewAtIndex(self, view, idx):
	#	raise TypeError(u'SplitView does not support inserting at index')

	def insertSubviewAboveSubview(self, view, otherView):
		raise TypeError(u'SplitView does not support inserting at index')

	def insertSubviewBelowSubview(self, view, otherView):
		raise TypeError(u'SplitView does not support inserting at index')

	def exchangeSubviewAtIndexwithSubviewAtIndex(self, idx1, idx2):
		raise TypeError(u'SplitView does not support reordering views')

	# hit testing against divider
	def hitTestWithEvent(self, point, event):
		retval = None
		if (   (    self._vertical 
				and point.x == self._leftView.width.intval)
			or (    not self._vertical  
				and point.y == self._leftView.height.intval)):
				retval = self
		else:
			retval = View.hitTestWithEvent(self, point, event)
		return retval

	def mouseDown(self, event):
		# we need to double check if its a mouse down AND in the divider
		# any subviews will pass their responder
		point = self.convertPointFromView(event.locationInContext)
		if ( 	event.type == MouseEventType.MOUSE_DOWN
			and (	(    self._vertical 
					 and point.x == self._leftView.width.intval)
				 or (    not self._vertical  
					 and point.y == self._leftView.height.intval))):
				# in the divider
				if self._vertical:
					loc = Point(self._leftView.width.intval, 1)
				else:
					loc = Point(1, self._leftView.height.intval)
				if point.x == loc.x and point.y == loc.y:
					self.setCollapse(not self._collapsed)
		else:
			View.mouseDown(self, event)

