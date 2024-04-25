from .math import curvature, lineIntersection, area


# Get max curvature
def maxCurvature(self, x1, y1, x2, y2, x3, y3, x4, y4):
	t1 = 0
	t4 = 1
	max_curvature = 0
	precision = 6
	trisect = True

	while trisect == True:
		t2 = 2 * t1 / 3 + t4 / 3
		t3 = t1 / 3 + 2 * t4 / 3

		c_t2 = curvature(x1, y1, x2, y2, x3, y3, x4, y4, t2)
		c_t3 = curvature(x1, y1, x2, y2, x3, y3, x4, y4, t3)

		if c_t2 > c_t3:
			t4 = t3

		elif c_t3 > c_t2:
			t1 = t2

		elif c_t2 == c_t3:
			t1 = t2
			t4 = t3

		current_curvature = max(c_t2, c_t3)

		if round(current_curvature, precision * 2) == round(max_curvature, precision * 2):
			trisect = False

		max_curvature = current_curvature

	return max_curvature


# Get speed by matching areas
def getSpeed(self, originalArea, x1, y1, nx2_2, ny2_2, px, py, x5, y5):

	# Set boundaries for bisection
	s1 = 0
	s3 = 1

	while True:
		s2 = s1 + (s3 - s1) / 2

		# Create control points from speed
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
