from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from smoothing.smooth import *
from smoothing.strings import pluginName, buttonTitle


class Smoothing(FilterWithDialog):

	# Definitions of IBOutlets

	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()

	# Text field in dialog
	myTextField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize(pluginName)

		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize(buttonTitle)

		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):

		# Set default value
		Glyphs.registerDefault('com.flachware.smoothing.default', 0.5)

		# Set value of text field
		self.myTextField.setStringValue_(Glyphs.defaults['com.flachware.smoothing.default'])

		# Set focus to text field
		self.myTextField.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setValue_(self, sender):

		# Store value coming in from dialog
		Glyphs.defaults['com.flachware.smoothing.value'] = sender.floatValue()

		# Trigger redraw
		self.update()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		value = float(Glyphs.defaults['com.flachware.smoothing.value'])
		smooth(self, value)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
