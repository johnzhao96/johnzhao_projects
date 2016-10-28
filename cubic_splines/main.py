"""
main.py

Runs and tests the Hermite Cubic Spline generator
"""

from math import sin, pi
from hermite import smoothCubic_DEC, not_a_knot

def poly(x):
	"""
	f(x) = x^3 + 2x^2 + 3x + 5
	q = HermiteCubic([0,1,5,7], [5, 11, 195, 467], [3, 10, 98, 178])
	"""
	x = float(x)
	return x*x*x + 2*x*x + 3*x + 5

def test_smoothCubic_DEC(f, p, dl, dr, num_test_points = 13):
	"""
	Takes a function f, a partition p, left and right derivatives dl and dr, and constructs a DEC spline,
	evaluating the actual function and the spline at num_test_points evenly spaced points.
	"""
	v = []
	for xi in p:
		v.append(f(xi))
	g = smoothCubic_DEC(p, v, dl, dr)

	print("Spline Derivatives: {}".format(g.d))

	a = float(p[0])
	b = float(p[-1])

	max_error = 0
	for i in range(0, num_test_points):
		ti = a+(b-a)/num_test_points*i
		actual = f(ti)
		spline = g(ti)
		error = abs(actual - spline)
		if error > max_error:
			max_error = error
		print("x: {}    Actual: {}    Spline: {}    Error: {}".format(ti, actual, spline, error))
	
	print("Max Error: {}".format(max_error))

def test_not_a_knot(f, p, num_test_points = 13):
	"""
	Takes a function f, a partition p, left and right derivatives dl and dr, and constructs a not-a-knot spline,
	evaluating the actual function and the spline at num_test_points evenly spaced points.
	"""
	v = []
	for xi in p:
		v.append(f(xi))
	g = not_a_knot(p, v)

	print("Spline Derivatives: {}".format(g.d))

	a = float(p[0])
	b = float(p[-1])

	max_error = 0
	for i in range(0, num_test_points):
		ti = a+(b-a)/num_test_points*i
		actual = f(ti)
		spline = g(ti)
		error = abs(actual - spline)
		if error > max_error:
			max_error = error
		print("x: {}    Actual: {}    Spline: {}    Error: {}".format(ti, actual, spline, error))
	
	print("Max Error: {}".format(max_error))

# Test the smoothCubic_DEC spline constructor
print("smoothCubic_DEC: f(x) = 5 + 3x + 2x^2 + x^3 with partition [0, 1, 2.3, 5, 6.5, 7]:")
test_smoothCubic_DEC(poly, [0,1,2.3,5,6.5, 7], 3, 178)

print("\nsmoothCubic_DEC: f(x) = sin(x) on [0, pi/2] with 4 intervals:")
test_smoothCubic_DEC(sin, [0, pi/8, 2*pi/8, 3*pi/8, pi/2], 1.0, 0.0)

print("\nsmoothCubic_DEC: f(x) = sin(x) on [0, pi/2] with 8 intervals:")
test_smoothCubic_DEC(sin, [0, pi/16, 2*pi/16, 3*pi/16, 4*pi/16, 5*pi/16, 6*pi/16, 7*pi/16, pi/2], 1.0, 0.0)

# Test the not_a_knot spline constructor
print("\n\nnot_a_knot: f(x) = 5 + 3x + 2x^2 + x^3 with partition [0, 1, 2.3, 5, 6.5, 7]:")
test_not_a_knot(poly, [0,1,2.3,5,6.5, 7])

print("\nnot_a_knot: f(x) = sin(x) on [0, pi/2] with 4 intervals:")
test_not_a_knot(sin, [0, pi/8, 2*pi/8, 3*pi/8, pi/2])

print("\nnot_a_knot: f(x) = sin(x) on [0, pi/2] with 8 intervals:")
test_not_a_knot(sin, [0, pi/16, 2*pi/16, 3*pi/16, 4*pi/16, 5*pi/16, 6*pi/16, 7*pi/16, pi/2])


