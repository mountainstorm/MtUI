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


"""This is a slim wrapper around the brilliant casuarius python library.  It is
upon this that all our layout code is based.  As a general rule views/controls
will give themselves non-required constraints - thus allowing you to break them
if need be.

To use this you need to create a constraint, you'll typically do that by 
creating an expression from a constraint variable e.g. a view's top, height 
members.

This code will produce a view which stretches the width of its parent and is 5
units high.

view1 = View(y=0, height=5)
c1 = view1.left == 0 # make the views left edge match its parents
c2 = view1.right == parent.right # make the views right edge match its parents

# must add subview before adding constraints, otherwise we can't validate the 
# variables (they use) views
parent.addSubview(view1) 
parent.addConstraint(c2) # constraints must be added to the highest view used
view1.addConstraint(c1)
"""


import casuarius


class ConstraintVariable(casuarius.ConstraintVariable):
	"""This is a simple wrapper class around the Cython ConstraintVariable.  
	This allows us to add the view member.  We can't override the constructor
	as the base class is Cython, but we'll use the LayoutVariable factory to 
	make if feel like we do.

	Just in case that isn't clear enough, "you should never create this class 
	directly".  Thats right kiddies, always create one via the by calling the 
	LayoutVariable factory method.

	To access the value of the variable you can do:
	  var.value # retrieves the float value
	  vat.intval # retrieves the int value (rounded up or down)
	"""
	intval = property(lambda self: int(self.value + 0.5))


def LayoutVariable(view, debug_name, value=0.0):
	"""The factory method for creating a constraint variable.  Its deliberatly 
	named as a class because we may, at some point, change this to be an actual
	class e.g. use a different layout library
	"""
	name = (view.__class__.__name__ + u'.' + debug_name).encode(u'utf-8')
	retval = ConstraintVariable(name, value)
	retval.view = view # set the view object
	return retval

def layout_variables(constraint):
	"""Helper method, returns the LayoutVariables present in a constraint.
	"""
	retval = set()
	if not isinstance(constraint, casuarius.LinearConstraint):
		raise TypeError(u'constraint is wrong type: ' + type(constraint))
	for term in (constraint.lhs.terms + constraint.rhs.terms):
		retval.add(term.var)
	return retval

def layout_update(constraints):
	"""Helper method, processes all the constraints and updates and variables
	they use
	"""
	solver = casuarius.Solver()
	for c in constraints:
		solver.add_constraint(c)
	solver.autosolve = True # this will cause all the variables to update

class LayoutStrength(object):
	"""Some common strength types for the constrainst
	"""
	REQUIRED = casuarius.required
	STRONG = casuarius.strong
	MEDIUM = casuarius.medium
	WEAK = casuarius.weak

	@classmethod
	def custom(cls, value):
		"""creates a custom stength
		"""
		pass # TODO: I've not figured out how the strength values work yet


