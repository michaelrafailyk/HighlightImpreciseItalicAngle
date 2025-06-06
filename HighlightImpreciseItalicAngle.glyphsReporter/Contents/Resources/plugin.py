# encoding: utf-8

# Highlight Imprecise Italic Angle
# https://github.com/michaelrafailyk/HighlightImpreciseItalicAngle

import objc
from GlyphsApp import Glyphs, OFFCURVE
from GlyphsApp.plugins import ReporterPlugin, NSColor, NSBezierPath, NSMakeRect
from math import degrees, atan2, tan, pi
import math
from Cocoa import NSMenuItem, NSOnState, NSOffState

class HighlightImpreciseItalicAngle(ReporterPlugin):
	
	@objc.python_method
	def settings(self):
		self.menuName = 'Highlight Imprecise Italic Angle'
		
		self.roundAngleDownStatus = True
		self.roundAngleDownMenu = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Round down to a smaller italic angle if it's between integer coordinates. When unchecked, it will round to a closest coordinate.", self.roundAngle, "")
		self.roundAngleDownMenu.setState_(NSOnState)
		self.generalContextMenus = [{"menu": self.roundAngleDownMenu}]
	
	def roundAngle(self):
		if self.roundAngleDownStatus:
			self.roundAngleDownStatus = False
			self.roundAngleDownMenu.setState_(NSOffState)
		else:
			self.roundAngleDownStatus = True
			self.roundAngleDownMenu.setState_(NSOnState)
		if Glyphs.redraw:
			Glyphs.redraw()
	
	@objc.python_method
	def foreground(self, layer):
		
		# precise italic angle
		anglePrecise = round(Glyphs.font.selectedFontMaster.italicAngle, 2)
		# observed angle (+ and -) around precise angle
		angleObserved = 10
		lineThickness = 2
		dotDiameter = 6
		opacity = 0.8
		# light mode colors
		color = '#FF2850'
		# dark mode colors
		if self.controller.graphicView().drawDark():
			color = '#FF6478'
		
		
		
		scale = self.getScale()
		toolSelect = Glyphs.font.tool == 'SelectTool'
		toolPen = Glyphs.font.tool == 'DrawTool'
		toolTempPreview = Glyphs.font.parent.windowController().toolTempSelection() != None
		if (toolSelect or toolPen) and not toolTempPreview:
			for path in layer.paths:
				nodes = path.nodes
				nodesCount = len(nodes)
				for i in range(nodesCount):
					nodeOne = nodes[(i-1) % nodesCount]
					nodeTwo = nodes[i]
					# do not display highlight between the handles, as well as between the last and first node of an open path
					betweenHandles = nodeOne.type == OFFCURVE and nodeTwo.type == OFFCURVE
					betweenOpenPath = not path.closed and i == 0
					if not betweenHandles and not betweenOpenPath:
						posOne = nodeOne.position
						posTwo = nodeTwo.position
						# calculate angle between nodes
						angle = degrees(atan2(posTwo.y - posOne.y, posTwo.x - posOne.x))
						angle = -angle - 90
						if angle <= -90: angle += 180
						angle = round(angle, 2)
						# angle is within the observed range but not precise
						if (angle != anglePrecise) and (angle >= anglePrecise - angleObserved) and (angle <= anglePrecise + angleObserved):
							# find the horizontal difference between current node position and correct (for italic angle) node position
							dotLower = posOne
							dotUpper = posTwo
							if posOne.y > posTwo.y:
								dotLower = posTwo
								dotUpper = posOne
							angleSegment = 90 - anglePrecise
							xDifference = (dotLower.x + (dotUpper.y - dotLower.y) / tan(angleSegment * pi / 180)) - dotUpper.x
							if self.roundAngleDownStatus:
								# choose a coordinate with a smaller new angle if precise angle is not available (default)
								xDifference = math.floor(xDifference)
							else:
								# choose a closest coordinate if precise angle is not available
								xDifference = round(xDifference)
							# if one point movement will make the angle closer to precise italic angle
							if (abs(xDifference) >= 1):
								
								
								
								# draw line between nodes
								NSColor.colorWithString_(color).colorWithAlphaComponent_(opacity).set()
								line = NSBezierPath.alloc().init()
								line.moveToPoint_(posOne)
								line.lineToPoint_(posTwo)
								line.setLineWidth_(lineThickness / scale)
								line.stroke()
								
								
								
								
								# in some cases, drawing dots requires to recalculate the x difference for better dots placement
								# if one node is a handle and the other is a smooth node, then use a next node on line segment instead of smooth node to calculate the x difference
								# in this case only the dot around handle will be drawn an it will be located along the straight line
								xDifferenceRecalculate = False
								if nodeOne.smooth and (nodeOne.type != OFFCURVE) and (nodeTwo.type == OFFCURVE) and (nodes[i-2].type != OFFCURVE):
									posOne = nodes[i-2].position
									xDifferenceRecalculate = True
								elif nodeTwo.smooth and (nodeTwo.type != OFFCURVE) and (nodeOne.type == OFFCURVE) and (nodes[i+1].type != OFFCURVE):
									posTwo = nodes[i+1].position
									xDifferenceRecalculate = True
								if xDifferenceRecalculate:
									dotLower = posOne
									dotUpper = posTwo
									if posOne.y > posTwo.y:
										dotLower = posTwo
										dotUpper = posOne
									xDifference = (dotLower.x + (dotUpper.y - dotLower.y) / tan(angleSegment * pi / 180)) - dotUpper.x
								
								
								
								# preparations for drawing placeholder dots and distance numbers
								xDifferenceShifted = xDifference
								# shift dot position a little away from a node if it is visible to close to the node when scaling down
								xShiftCorrection = 4
								if (xDifferenceShifted * scale) < xShiftCorrection:
									if xDifferenceShifted > 0:
										xDifferenceShifted += xShiftCorrection / scale
									else:
										xDifferenceShifted -= xShiftCorrection / scale
								# rounded x difference will be displayed as a number next to a placeholder dots
								xDifferenceRounded = round(xDifference)
								# correct rounded x difference if it is zero (after rounding) but the node is not in the correct position
								if xDifferenceRounded == 0:
									if xDifference > 0:
										xDifferenceRounded = 1
									elif xDifference < 0:
										xDifferenceRounded = -1
								# don't draw dots if current node is on curve but opposite node is handle (draw dot only for handle in this case)
								nodeLowerIsOnCurve = True
								nodeUpperIsOnCurve = True
								if posOne.y > posTwo.y:
									if nodeTwo.type == OFFCURVE:
										nodeLowerIsOnCurve = False
									if nodeOne.type == OFFCURVE:
										nodeUpperIsOnCurve = False
								else:
									if nodeOne.type == OFFCURVE:
										nodeLowerIsOnCurve = False
									if nodeTwo.type == OFFCURVE:
										nodeUpperIsOnCurve = False
								diameter = dotDiameter / scale
								textColor = NSColor.colorWithString_(color)
								textOffsetX = 5 / scale
								textOffsetY = 5 / scale
								textAlignRight = 'bottomright'
								textAlignLeft = 'bottomleft'
								if xDifference < 0:
									textOffsetX = -textOffsetX
									textAlignRight = 'bottomleft'
									textAlignLeft = 'bottomright'
								
								
								
								# draw placeholder dots and distance numbers
								if (nodeLowerIsOnCurve and nodeUpperIsOnCurve) or (not nodeLowerIsOnCurve and nodeUpperIsOnCurve):
									# lower dot
									rectLower = NSMakeRect(dotLower.x - xDifferenceShifted - (diameter / 2), dotLower.y - (diameter / 2), diameter, diameter)
									NSBezierPath.bezierPathWithOvalInRect_(rectLower).fill()
									# lower number
									self.drawTextAtPoint(str(abs(xDifferenceRounded)), (dotLower.x - xDifferenceShifted - textOffsetX, dotLower.y - textOffsetY), fontColor = textColor, align = textAlignRight)
								if (nodeLowerIsOnCurve and nodeUpperIsOnCurve) or (not nodeUpperIsOnCurve and nodeLowerIsOnCurve):
									# upper dot
									rectUpper = NSMakeRect(dotUpper.x + xDifferenceShifted - (diameter / 2), dotUpper.y - (diameter / 2), diameter, diameter)
									NSBezierPath.bezierPathWithOvalInRect_(rectUpper).fill()
									# upper number
									self.drawTextAtPoint(str(abs(xDifferenceRounded)), (dotUpper.x + xDifferenceShifted + textOffsetX, dotUpper.y - textOffsetY), fontColor = textColor, align = textAlignLeft)
	
	@objc.python_method
	def __file__(self):
		return __file__
