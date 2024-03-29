from GlyphsApp import *
from GlyphsApp.plugins import *
from .math import curvature, lineIntersection, area


# Get superness by matching areas
def getSuperness(self, originalArea, x1, y1, nx2_2, ny2_2, px, py, x5, y5):

	# Set boundaries for bisection
	s1 = 0
	s3 = 1
	superness = 0
	bisect = True

	while bisect == True:
		s2 = s1 + (s3 - s1) / 2

		# Create control points from superness
		nx3 = nx2_2 + (px - nx2_2) * s2
		ny3 = ny2_2 + (py - ny2_2) * s2
		nx4 = x5 + (px - x5) * s2
		ny4 = y5 + (py - y5) * s2

		# Calculate area of new path
		newArea = area([
			[(x1, y1), (nx2_2, ny2_2)],
			[(nx2_2, ny2_2), (nx3, ny3), (nx4, ny4), (x5, y5)],
			[(x5, y5), (x1, y1)]
		])

		if round(newArea) < round(originalArea):
			s1 = s2

		elif round(newArea) > round(originalArea):
			s3 = s2

		else:
			return s2


def smooth(self, value):
	for layer in Glyphs.font.selectedLayers:
		for path in layer.paths:
			for node in path.nodes:
				if node.selected == True:
					if node.smooth == True:
						# Previous node is line, next 3 nodes are curve
						if node.type == LINE:

							#Get all coordinates involved
							x1 = path.nodes[node.index - 1].position[0]
							y1 = path.nodes[node.index - 1].position[1]
							x2 = node.position[0]
							y2 = node.position[1]
							x3 = path.nodes[node.index + 1].position[0]
							y3 = path.nodes[node.index + 1].position[1]
							x4 = path.nodes[node.index + 2].position[0]
							y4 = path.nodes[node.index + 2].position[1]
							x5 = path.nodes[node.index + 3].position[0]
							y5 = path.nodes[node.index + 3].position[1]

							# Point of line intersection of tangent vectors
							p = lineIntersection(x2, y2, x3, y3, x4, y4, x5, y5)
							px = p[0]
							py = p[1]

							# Curvature of original curve in x1/y1
							originalCurvature = curvature(x2, y2, x3, y3, x4, y4, x5, y5, 0)
							#self.logToConsole(originalCurvature)

							# Superness of original curve
							if x2 != x3:
								s3 = (x3 - x2) / (px - x2)

							else:
								s3 = (y3 - y2) / (py - y2)

							if x4 != x5:
								s4 = (x4 - x5) / (px - x5)

							else:
								s4 = (y4 - y5) / (py - y5)

							originalSuperness = (s3 + s4) / 2

							# Area of original path
							originalArea = area([
								[(x1, y1), (x2, y2)],
								[(x2, y2), (x3, y3), (x4, y4), (x5, y5)],
								[(x5, y5), (x1, y1)]
							])




							# Set boundaries for bisection
							nx2_1 = x1
							ny2_1 = y1
							nx2_3 = x2
							ny2_3 = y2
							testing = True

							while testing == True:
								nx2_2 = nx2_3 - (nx2_3 - nx2_1) / 2
								ny2_2 = ny2_3 - (ny2_3 - ny2_1) / 2

								# Get best superness for the new curve
								newSuperness = getSuperness(self, originalArea, x1, y1, nx2_2, ny2_2, px, py, x5, y5)
								self.logToConsole(newSuperness)

								# Stop when change of tension is equal to improvement of continuity
								testing = False





						# Previous 3 nodes are curve, next node is line
						elif node.type == CURVE:
							# To-do: normalize path (work on copy?)
							print(node)

