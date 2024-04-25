from GlyphsApp import *
from GlyphsApp.plugins import *
from .math import curvature, lineIntersection, area
from .helpers import maxCurvature, getSpeed


def smooth(self, value):
	for layer in Glyphs.font.selectedLayers:
		for path in layer.paths:
			for node in path.nodes:
				if node.selected == True:
					if node.smooth == True:
						# Previous node is line, next 3 nodes are curve
						if node.type == LINE:

							# Get all coordinates involved
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

							# Area of original path
							originalArea = area([
								[(x1, y1), (x2, y2)],
								[(x2, y2), (x3, y3), (x4, y4), (x5, y5)],
								[(x5, y5), (x1, y1)]
							])

							# Set boundaries for trisection
							nx2_1 = x1
							ny2_1 = y1
							nx2_4 = x2
							ny2_4 = y2
							precision = 16
							trisect = True

							while trisect == True:
								nx2_2 = 2 * nx2_1 / 3 + nx2_4 / 3
								ny2_2 = 2 * ny2_1 / 3 + ny2_4 / 3
								nx2_3 = nx2_1 / 3 + 2 * nx2_4 / 3
								ny2_3 = ny2_1 / 3 + 2 * ny2_4 / 3

								points = [(nx2_2, ny2_2), (nx2_3, ny2_3)]
								minMax = []

								for point in points:
									speed = getSpeed(self, originalArea, x1, y1, point[0], point[1], px, py, x5, y5)

									nx3 = point[0] + (px - point[0]) * speed
									ny3 = point[1] + (py - point[1]) * speed
									nx4 = x5 + (px - x5) * speed
									ny4 = y5 + (py - y5) * speed

									min = curvature(point[0], point[1], nx3, ny3, nx4, ny4, x5, y5, 0)
									max = maxCurvature(self, point[0], point[1], nx3, ny3, nx4, ny4, x5, y5)
									minMax.append(min + max)

								if round(minMax[0], precision) < round(minMax[1], precision):
									nx2_4 = nx2_3
									ny2_4 = ny2_3

								elif round(minMax[1], precision) < round(minMax[0], precision):
									nx2_1 = nx2_2
									ny2_1 = ny2_2

								else:
									nx2 = nx2_2
									ny2 = ny2_2
									trisect = False

							nx2 = x2 - (x2 - nx2) * value
							ny2 = y2 - (y2 - ny2) * value
							nx3 = x3 - (x3 - nx3) * value
							ny3 = y3 - (y3 - ny3) * value
							nx4 = x4 - (x4 - nx4) * value
							ny4 = y4 - (y4 - ny4) * value

							node.position = NSPoint(nx2, ny2)
							node.nextNode.position = NSPoint(nx3, ny3)
							node.nextNode.nextNode.position = NSPoint(nx4, ny4)


						# Previous 3 nodes are curve, next node is line
						elif node.type == CURVE:
							# To-do: normalize path (work on copy?)
							print(node)
