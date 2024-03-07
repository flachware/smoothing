from GlyphsApp import *
from GlyphsApp.plugins import *
from .helpers import lineIntersection, area


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

							# Create original segment list from nodes
							original = [
								[(x1, y1), (x2, y2)],
								[(x2, y2), (x3, y3), (x4, y4), (x5, y5)],
								[(x5, y5), (x1, y1)]
							]

							# Area of original path
							originalArea = area(original)


							# Create test path

							# Calculate n2 position (bisection)

							dx2 = x2 - x1
							dy2 = y2 - y1
							nx2 = x2 - dx2 / 2
							ny2 = y2 - dy2 / 2

							# Calculate n3 position (bisection)

							# Point of line intersection of tangent vectors
							p = lineIntersection(x2, y2, x3, y3, x4, y4, x5, y5)
							px = p[0]
							py = p[1]

							dx3 = px - nx2
							dy3 = py - ny2
							nx3 = px - dx3 * (1 - 0.55228) / 2
							ny3 = py - dy3 * (1 - 0.55228) / 2

							# Calculate n4 position (bisection)

							dx4 = px - x5
							dy4 = py - y5
							nx4 = px - dx4 * (1 - 0.55228) / 2
							ny4 = py - dy4 * (1 - 0.55228) / 2

							# New nodes

							n1 = (x1, y1)
							n2 = (nx2, ny2)
							n3 = (nx3, ny3)
							n4 = (nx4, ny4)
							n5 = (x5, y5)

							# New segment list

							new = [
								[n1, n2],
								[n2, n3, n4, n5],
								[n5, n1]
							]

							# Area of new path
							newArea = area(new)

							self.logToConsole(newArea)


						# Previous 3 nodes are curve, next node is line
						elif node.type == CURVE:
							# To-do: normalize path (work on copy?)
							print(node)

