def lineIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
	x = ( (x2 - x1) * (x3 * y4 - y3 * x4) - (x4 - x3) * (x1 * y2 - y1 * x2) ) / ( (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3) )
	y = ( (y2 - y1) * (x3 * y4 - y3 * x4) - (y4 - y3) * (x1 * y2 - y1 * x2) ) / ( (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3) )

	return (x, y)


def area(segments):

	# Indefinite integral of Leibniz’ Sektorformel for a cubic Bézier curve
	def Fb(x0, x1, x2, x3, y0, y1, y2, y3, t):
		return \
			t*(\
				 6*t**4*(x0*y1 - 2*x0*y2 + x0*y3 - x1*y0 + 3*x1*y2 - 2*x1*y3 + 2*x2*y0 - 3*x2*y1 + x2*y3 - x3*y0 + 2*x3*y1 - x3*y2) + \
				15*t**3*(-2*x0*y1 + 3*x0*y2 - x0*y3 + 2*x1*y0 - 3*x1*y2 + x1*y3 - 3*x2*y0 + 3*x2*y1 + x3*y0 - x3*y1) + \
				10*t**2*(6*x0*y1 - 6*x0*y2 + x0*y3 - 6*x1*y0 + 3*x1*y2 + 6*x2*y0 - 3*x2*y1 - x3*y0) + \
				30*t*(-2*x0*y1 + x0*y2 + 2*x1*y0 - x2*y0) + 30*x0*y1 - 30*x1*y0 \
			)/10

	# Indefinite integral of Leibniz’ Sektorformel for a straight line
	def Fl(x0, x1, y0, y1, t):
		return t*(x0*y1 - x1*y0)

	area = 0

	for segment in segments:
		if len(segment) == 4:
			x0 = segment[0][0]
			x1 = segment[1][0]
			x2 = segment[2][0]
			x3 = segment[3][0]
			y0 = segment[0][1]
			y1 = segment[1][1]
			y2 = segment[2][1]
			y3 = segment[3][1]

			# Sektorformel
			curve_area = 1/2 * (Fb(x0, x1, x2, x3, y0, y1, y2, y3, 1) - Fb(x0, x1, x2, x3, y0, y1, y2, y3, 0))
			area += curve_area

		elif len(segment) == 2:
			x0 = segment[0][0]
			x1 = segment[1][0]
			y0 = segment[0][1]
			y1 = segment[1][1]

			# Sektorformel
			line_area = 1/2 * ( Fl(x0, x1, y0, y1, 1) - Fl(x0, x1, y0, y1, 0) )
			area += line_area

	return area
