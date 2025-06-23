# encoding: utf-8

# Highlight Imprecise Italic Angle
# https://github.com/michaelrafailyk/HighlightImpreciseItalicAngle

from __future__ import division
import objc
from GlyphsApp import Glyphs, OFFCURVE
from GlyphsApp.plugins import ReporterPlugin, NSColor, NSBezierPath, NSMakeRect
from math import degrees, atan2, tan, pi
import math

class HighlightImpreciseItalicAngle(ReporterPlugin):
	
	# reference to the slider
	sliderMenuView = objc.IBOutlet()
	textField = objc.IBOutlet()
	# threshold for rounding of Italic Angle with non-integer coordinate
	angleRoundingThreshold = 0.5
	
	@objc.python_method
	def settings(self):
		self.menuName = 'Highlight Imprecise Italic Angle'
		# load slider and add it to context menu
		self.loadNib("SliderView", __file__)
		self.generalContextMenus = [{"view": self.sliderMenuView}]
	
	# adjust the tolerance of rounding direction of Italic Angle with decimal coordinate, to the integer coordinate
	@objc.IBAction
	def slider_(self, sender):
		# turn the rounding gravite into rounding threshold
		self.angleRoundingThreshold = round(1 - sender.floatValue(), 1)
		# update slider label
		if self.angleRoundingThreshold == 1:
			self.textField.setStringValue_('Always round to a smaller angle')
		elif self.angleRoundingThreshold < 1 and self.angleRoundingThreshold > 0.5:
			self.textField.setStringValue_('Round to a smaller angle')
		elif self.angleRoundingThreshold == 0.5:
			self.textField.setStringValue_('Round angle to a closest coordinate')
		elif self.angleRoundingThreshold < 0.5 and self.angleRoundingThreshold > 0:
			self.textField.setStringValue_('Round to a greater angle')
		elif self.angleRoundingThreshold == 0:
			self.textField.setStringValue_('Always round to a greater angle')
		# update interface
		if Glyphs.redraw:
			Glyphs.redraw()
	
	# function for getting angle between two nodes
	@objc.python_method
	def getAngle(self, aX, aY, bX, bY):
		angle = degrees(atan2(bY - aY, bX - aX))
		angle = -angle - 90
		if angle <= -90: angle += 180
		angle = round(angle, 2)
		return angle
	
	@objc.python_method
	def foreground(self, layer):
		
		
		
		# user settings
		# observed angle around Italic Angle (if set to 10 it means from IA-10 degrees to IA+10 degrees, so the range will be 20 degrees in total)
		angleObserved = 10
		highlightThickness = 2
		dotDiameter = 6
		opacity = 0.8
		# index of the base color for the default Italic Angle
		colorDefault = 2
		colors = [
			'#00B464', # green
			'#FF9628', # yellow
			'#FF2850', # red
			'#AA32FF', # purple
			'#008CDC'  # cyan
		]
		if self.controller.graphicView().drawDark():
			colors = [
				'#14C878',
				'#FFB446',
				'#FF6478',
				'#C85AFF',
				'#00A0FF'
			]
		
		
		
		font = Glyphs.font
		toolSelect = font.tool == 'SelectTool'
		toolPen = font.tool == 'DrawTool'
		toolTempPreview = font.parent.windowController().toolTempSelection() != None
		if (toolSelect or toolPen) and not toolTempPreview:
			master = font.selectedFontMaster
			# get default Italic Angle of a current master, and set default color
			ItalicAngle = round(master.italicAngle, 2)
			color = colors[colorDefault]
			
			# get a custom Italic Angles if set in Font Info > Masters > Number Values
			ItalicAngles = []
			ItalicAnglesDefault = None
			ItalicAnglesClosest = None
			if font.numbers:
				for number in font.numbers:
					if 'Italic Angle' in number.name.title():
						ItalicAngleCustom = master.numbers[number.id]
						if ItalicAngleCustom != ItalicAngle and ItalicAngleCustom not in ItalicAngles:
							ItalicAngles.append(ItalicAngleCustom)
			if ItalicAngles:
				ItalicAngles.append(ItalicAngle)
				ItalicAngles.sort()
				ItalicAnglesDefault = ItalicAngles.index(ItalicAngle)
			
			# check the angle of each path segment
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
						# check if there is a "handle + tangens node + line" or "handle + tangens node + handle" scenario
						thisHandle_prevLine = nodeOne.smooth and (nodeOne.type != OFFCURVE) and (nodeTwo.type == OFFCURVE) and (nodes[(i-2) % nodesCount].type != OFFCURVE)
						thisHandle_nextLine = nodeTwo.smooth and (nodeTwo.type != OFFCURVE) and (nodeOne.type == OFFCURVE) and (nodes[(i+1) % nodesCount].type != OFFCURVE)
						thisHandle_prevHandle = nodeOne.smooth and (nodeOne.type != OFFCURVE) and (nodeTwo.type == OFFCURVE) and (nodes[(i-2) % nodesCount].type == OFFCURVE)
						thisHandle_nextHandle = nodeTwo.smooth and (nodeTwo.type != OFFCURVE) and (nodeOne.type == OFFCURVE) and (nodes[(i+1) % nodesCount].type == OFFCURVE)
						# calculate angle between nodes
						angle = self.getAngle(posOne.x, posOne.y, posTwo.x, posTwo.y)
						
						# if custom Italic Angles are set
						if ItalicAngles:
							# make the alias of angle (for internal checking) so it could be modified without changing the angle itself
							angleAlias = angle
							# for "handle + tangens node + line" case – use line angle instead of handle angle
							# this guarantees that both handle and line will be aligned to the same Italic Angle and highlighted with the same color
							if thisHandle_prevLine:
								angleAlias = self.getAngle(posOne.x, posOne.y, nodes[(i-2) % nodesCount].position.x, nodes[(i-2) % nodesCount].position.y)
							elif thisHandle_nextLine:
								angleAlias = self.getAngle(posTwo.x, posTwo.y, nodes[(i+1) % nodesCount].position.x, nodes[(i+1) % nodesCount].position.y)
							# find a closest Italic Angle from all default one and custom ones
							if angleAlias <= ItalicAngles[0]:
								ItalicAnglesClosest = 0
							elif angleAlias >= ItalicAngles[-1]:
								ItalicAnglesClosest = len(ItalicAngles) - 1
							else:
								ItalicAnglesIndex = 0
								for IA in ItalicAngles:
									if IA != ItalicAngles[-1]:
										IANext = ItalicAngles[ItalicAnglesIndex + 1]
										if angleAlias >= IA and angleAlias <= IANext:
											IABoundary = (IA + IANext) / 2
											if angleAlias <= IABoundary:
												ItalicAnglesClosest = ItalicAnglesIndex
											else:
												ItalicAnglesClosest = ItalicAnglesIndex + 1
											break
										ItalicAnglesIndex += 1
							colorCustom = (colorDefault + (ItalicAnglesClosest - ItalicAnglesDefault)) % len(colors)
							# custom highlight color
							color = colors[colorCustom]
							# custom Italic Angle
							ItalicAngle = ItalicAngles[ItalicAnglesClosest]
						
						# angle is within the observed range but not precise, and it's not left/right extremes with 0 degree angle
						if (angle != 0) and (angle != ItalicAngle) and (angle >= ItalicAngle - angleObserved) and (angle <= ItalicAngle + angleObserved):
							# find the horizontal difference between current node position and correct (for italic angle) node position
							posLower = posOne
							posUpper = posTwo
							if posOne.y > posTwo.y:
								posLower = posTwo
								posUpper = posOne
							angleSegment = 90 - ItalicAngle
							xDifferencePrecise = (posLower.x + (posUpper.y - posLower.y) / tan(angleSegment * pi / 180)) - posUpper.x
							xDifference = xDifferencePrecise
							# round to an integer coordinate if coordinate for precise Italic Angle is decimal
							# depending on the rounding value set in context menu slider
							if self.angleRoundingThreshold == 0.5:
								# round to a closest x coordinate
								xDifference = round(xDifference)
							else:
								xThreshold = xDifference - math.floor(xDifference + 1)
								if xThreshold < 0:
									xThreshold = xThreshold + 1
								# round down to a coordinate with a smaller angle
								if xThreshold < self.angleRoundingThreshold:
									xDifference = math.floor(xDifference)
								# round up to a coordinate with a greater angle
								else:
									xDifference = math.ceil(xDifference)
							# if one point movement will make the angle closer to precise italic angle
							if (abs(xDifference) >= 1):
								highlightPosOne = posOne
								highlightPosTwo = posTwo
								
								
								
								# line + tangent handle scenario
								# drawing dots requires to recalculate the x difference for better dots placement
								# if one node is a handle and the other is a smooth node, then use a next node on line segment instead of smooth node to calculate the x difference
								# in this case only the dot around handle will be drawn an it will be located along the straight line
								# additionally prevent to highlight handle if line has correct angle and handle is not broken
								line_handle = False
								line_handle_haveGoodAngle = False
								linePosOne = False
								linePosTwo = False
								# line before current handle
								if thisHandle_prevLine:
									line_handle = True
									posOne = nodes[(i-2) % nodesCount].position
									linePosOne = nodes[(i-2) % nodesCount].position
									linePosTwo = nodes[(i-1) % nodesCount].position
								# line after current handle
								elif thisHandle_nextLine:
									line_handle = True
									posTwo = nodes[(i+1) % nodesCount].position
									linePosOne = nodes[i].position
									linePosTwo = nodes[(i+1) % nodesCount].position
								if line_handle:
									posLower = posOne
									posUpper = posTwo
									linePosLower = linePosOne
									linePosUpper = linePosTwo
									if posOne.y > posTwo.y:
										posLower = posTwo
										posUpper = posOne
										linePosLower = linePosTwo
										linePosUpper = linePosOne
									# recaltulate x difference for extreme points of line segment + handle segment
									xDifference = (posLower.x + (posUpper.y - posLower.y) / tan(angleSegment * pi / 180)) - posUpper.x
									# calculate x difference for line segment and handle segment
									xDifferenceLine = (linePosLower.x + (linePosUpper.y - linePosLower.y) / tan(angleSegment * pi / 180)) - linePosUpper.x
									xDifferenceHandle = round(xDifferencePrecise, 2)
									# round to an integer coordinate if coordinate for precise Italic Angle is decimal
									# depending on the rounding value set in context menu slider
									if self.angleRoundingThreshold == 0.5:
										# round to a closest x coordinate
										xDifferenceLine = round(xDifferenceLine)
									else:
										xThreshold = xDifferenceLine - math.floor(xDifferenceLine + 1)
										if xThreshold < 0:
											xThreshold = xThreshold + 1
										# round down to a coordinate with a smaller angle
										if xThreshold < self.angleRoundingThreshold:
											xDifferenceLine = math.floor(xDifferenceLine)
										# round up to a coordinate with a greater angle
										else:
											xDifferenceLine = math.ceil(xDifferenceLine)
									angleLine = self.getAngle(linePosOne.x, linePosOne.y, linePosTwo.x, linePosTwo.y)
									# line has correct italic angle but handle is not
									# the difference of angles is very small so the handle is not broken after interpolation
									# it work fine for long segments, however, in very short segments the handle can still be highlighted
									if (xDifferenceLine == 0) and (xDifferenceHandle != 0) and (abs(angleLine - angle) < 0.5):
										line_handle_haveGoodAngle = True
								
								
								
								# handle + handle scenario
								# for preventing to always highlight one of handles around a smooth node if there is no way to set both of them simultaneously to a better position
								handle_handle = False
								handle_handle_haveGoodAngle = False
								handleOppositePosOne = False
								handleOppositePosTwo = False
								# opposite handle before current handle
								if thisHandle_prevHandle:
									handle_handle = True
									handleOppositePosOne = nodes[(i-2) % nodesCount].position
									handleOppositePosTwo = nodeOne.position
								# opposite handle after current handle
								elif thisHandle_nextHandle:
									handle_handle = True
									handleOppositePosOne = nodeTwo.position
									handleOppositePosTwo = nodes[(i+1) % nodesCount].position
								if handle_handle:
									handleOppositePosLower = handleOppositePosOne
									handleOppositePosUpper = handleOppositePosTwo
									if handleOppositePosOne.y > handleOppositePosTwo.y:
										handleOppositePosLower = handleOppositePosTwo
										handleOppositePosUpper = handleOppositePosOne
									# check if the opposite handle is in the correct position (not highlighted)
									xDifferenceHandleOpposite = (handleOppositePosLower.x + (handleOppositePosUpper.y - handleOppositePosLower.y) / tan(angleSegment * pi / 180)) - handleOppositePosUpper.x
									# round to an integer coordinate if coordinate for precise Italic Angle is decimal
									# depending on the rounding value set in context menu slider
									if self.angleRoundingThreshold == 0.5:
										# round to a closest x coordinate
										xDifferenceHandleOpposite = round(xDifferenceHandleOpposite)
									else:
										xThreshold = xDifferenceHandleOpposite - math.floor(xDifferenceHandleOpposite + 1)
										if xThreshold < 0:
											xThreshold = xThreshold + 1
										# round down to a coordinate with a smaller angle
										if xThreshold < self.angleRoundingThreshold:
											xDifferenceHandleOpposite = math.floor(xDifferenceHandleOpposite)
										# round up to a coordinate with a greater angle
										else:
											xDifferenceHandleOpposite = math.ceil(xDifferenceHandleOpposite)
									# get the angle of opposite handle
									angleOpposite = self.getAngle(handleOppositePosLower.x, handleOppositePosLower.y, handleOppositePosUpper.x, handleOppositePosUpper.y)
									# opposite handle is in the correct position (for italic angle) but the current handle is not
									# also the difference of angles is very small so the handles around the smooth node are not broken after interpolation
									if (xDifferenceHandleOpposite == 0) and (xDifference != 0) and (abs(angleOpposite - angle) < 0.5):
										# precalculate new angle for handle after possible correction
										angleNew = self.getAngle(posLower.x, posLower.y, posUpper.x + xDifference, posUpper.y)
										# precalculate x difference for opposite handle after possible correction
										xDifferenceHandleOppositeNew = (handleOppositePosLower.x + (handleOppositePosUpper.y - handleOppositePosLower.y) / tan((90 - angleNew) * pi / 180)) - handleOppositePosUpper.x
										xDifferenceHandleOppositeNew = round(xDifferenceHandleOppositeNew)
										# precalculate new angle for opposite handle after possible correction
										angleNewOpposite = self.getAngle(handleOppositePosLower.x, handleOppositePosLower.y, handleOppositePosUpper.x + xDifferenceHandleOppositeNew, handleOppositePosUpper.y)
										# if the opposite handle will be shifted after possible correction
										if xDifferenceHandleOppositeNew != 0:
											# average angle (average value between angles of both handles) before and after possible correction
											# this average values will be needed to check what is closer to Italic Angle
											angleAverage = (angle + angleOpposite) / 2
											angleAverageNew = (angleNew + angleNewOpposite) / 2
											# depending on the rounding value set in context menu slider
											# if set rounding to a closest coordinate (or rounding up)
											if self.angleRoundingThreshold <= 0.5:
												# if current average angle is closer to Italic Angle than avarage angle after possible correction
												if abs(ItalicAngle - angleAverage) < abs(ItalicAngle - angleAverageNew):
													handle_handle_haveGoodAngle = True
											# if set rounding down
											else:
												# all angles are lower than Italic Angle – allow to check what will be closer
												if angle <= ItalicAngle and angleOpposite <= ItalicAngle and angleNew <= ItalicAngle and angleNewOpposite <= ItalicAngle:
													# if current average angle is closer to Italic Angle than avarage angle after possible correction
													if abs(ItalicAngle - angleAverage) < abs(ItalicAngle - angleAverageNew):
														handle_handle_haveGoodAngle = True
												# both angles before correction are smaller of Italic Angle but after correction one of them will be larger of Italic Angle
												elif angle <= ItalicAngle and angleOpposite <= ItalicAngle and (angleNew > ItalicAngle or angleNewOpposite > ItalicAngle):
													handle_handle_haveGoodAngle = True
								
								
								
								# prevent to highlight handle if there is a smooth node and opposite line/handle has good angle
								if not line_handle_haveGoodAngle and not handle_handle_haveGoodAngle:
									scale = self.getScale()
									
									
									
									# draw highlight line between nodes
									NSColor.colorWithString_(color).colorWithAlphaComponent_(opacity).set()
									highlight = NSBezierPath.alloc().init()
									highlight.moveToPoint_(highlightPosOne)
									highlight.lineToPoint_(highlightPosTwo)
									highlight.setLineWidth_(highlightThickness / scale)
									highlight.stroke()
									
									
									
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
										rectLower = NSMakeRect(posLower.x - xDifferenceShifted - (diameter / 2), posLower.y - (diameter / 2), diameter, diameter)
										NSBezierPath.bezierPathWithOvalInRect_(rectLower).fill()
										# lower number
										self.drawTextAtPoint(str(abs(xDifferenceRounded)), (posLower.x - xDifferenceShifted - textOffsetX, posLower.y - textOffsetY), fontColor = textColor, align = textAlignRight)
									if (nodeLowerIsOnCurve and nodeUpperIsOnCurve) or (not nodeUpperIsOnCurve and nodeLowerIsOnCurve):
										# upper dot
										rectUpper = NSMakeRect(posUpper.x + xDifferenceShifted - (diameter / 2), posUpper.y - (diameter / 2), diameter, diameter)
										NSBezierPath.bezierPathWithOvalInRect_(rectUpper).fill()
										# upper number
										self.drawTextAtPoint(str(abs(xDifferenceRounded)), (posUpper.x + xDifferenceShifted + textOffsetX, posUpper.y - textOffsetY), fontColor = textColor, align = textAlignLeft)
	
	@objc.python_method
	def __file__(self):
		return __file__
