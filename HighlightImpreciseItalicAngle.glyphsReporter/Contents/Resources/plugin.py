# encoding: utf-8

# Highlight Imprecise Italic Angle
# https://github.com/michaelrafailyk/HighlightImpreciseItalicAngle

import objc
from GlyphsApp import Glyphs, OFFCURVE
from GlyphsApp.plugins import ReporterPlugin, NSColor, NSBezierPath, NSMakeRect
from math import degrees, atan2, tan, pi

class HighlightImpreciseItalicAngle(ReporterPlugin):
	
	@objc.python_method
	def settings(self):
		self.menuName = 'Highlight Imprecise Italic Angle'
	
	@objc.python_method
	def foreground(self, layer):
		
		# precise italic angle
		anglePrecise = Glyphs.font.selectedFontMaster.italicAngle
		# observed angle (+ and -) around precise angle
		angleObserved = 10
		color = '#FF2850'
		opacity = 0.8
		lineThickness = 2
		dotDiameter = 6
		
		
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
					betweenHandles = nodeOne.type == OFFCURVE and nodeTwo.type == OFFCURVE
					betweenOpenPath = not path.closed and i == 0
					# do not display highlight between the handles, as well as between the last and first node of an open path
					if not betweenHandles and not betweenOpenPath:
						posOne = nodeOne.position
						posTwo = nodeTwo.position
						
						# calculate angle between nodes
						angle = degrees(atan2(posTwo.y - posOne.y, posTwo.x - posOne.x))
						angle = round((-angle - 90), 1)
						if angle <= -90: angle += 180
						# angle is within the observed range but not precise
						if (angle != anglePrecise) and (angle >= anglePrecise - angleObserved) and (angle <= anglePrecise + angleObserved):
							
							# find the horizontal difference between current node position and correct (for italic angle) node position
							angleSegment = 90 - anglePrecise
							dotLower = posOne
							dotUpper = posTwo
							if posOne.y > posTwo.y:
								dotLower = posTwo
								dotUpper = posOne
							xDifference = (dotLower.x + (dotUpper.y - dotLower.y) / tan(angleSegment * pi / 180)) - dotUpper.x
							# if one point movement will make the angle closer to precise italic angle
							if (abs(xDifference) >= 1) or (abs(abs(xDifference) - 1) < abs(xDifference)):
								xDifference = round(xDifference)
								
								# draw line segment between nodes
								NSColor.colorWithString_(color).colorWithAlphaComponent_(opacity).set()
								line = NSBezierPath.alloc().init()
								line.moveToPoint_(posOne)
								line.lineToPoint_(posTwo)
								line.setLineWidth_(lineThickness / scale)
								line.stroke()
								
								# draw direction dots
								# move dot position away from node if it is visible to close to the node when scaling down
								if (xDifference * scale) < 3:
									if xDifference > 0:
										xDifference += 3 / scale
									else:
										xDifference -= 3 / scale
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
								# draw lower dot
								if (nodeLowerIsOnCurve and nodeUpperIsOnCurve) or (not nodeLowerIsOnCurve and nodeUpperIsOnCurve):
									rectLower = NSMakeRect(dotLower.x - xDifference - (diameter / 2), dotLower.y - (diameter / 2), diameter, diameter)
									NSBezierPath.bezierPathWithOvalInRect_(rectLower).fill()
								# draw upper dot
								if (nodeLowerIsOnCurve and nodeUpperIsOnCurve) or (not nodeUpperIsOnCurve and nodeLowerIsOnCurve):
									rectUpper = NSMakeRect(dotUpper.x + xDifference - (diameter / 2), dotUpper.y - (diameter / 2), diameter, diameter)
									NSBezierPath.bezierPathWithOvalInRect_(rectUpper).fill()
	
	@objc.python_method
	def __file__(self):
		return __file__
