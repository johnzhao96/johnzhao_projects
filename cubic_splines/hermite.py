"""
hermite.py

Implementation of HermiteCubic class
"""
from matrix import TridiagMatrix, Matrix

class HermiteCubic:
	def __init__(self, p, v, d):
		# Number of points in partition
		self.n = len(p)

		# Array of locations of partitioning points
		self.p = map(float, p)

		# Array of values of the function at the partitioning points
		self.v = map(float, v)

		# Array of values of derivatives at the partitioning points
		self.d = map(float, d)

		# Array of cubic functions corresponding to the interval I_i where they should be evaluated
		self.cubics = []
		for i in range(1, self.n):
			self.cubics.append(
				piecewise_cubic(self.p[i-1], self.p[i], self.v[i-1], self.v[i], self.d[i-1], self.d[i])
			)

	def __call__(self, x):
		"""
		Evaluate the Hermite Cubic at x
		"""
		i = self.find_interval(x)
		return self.cubics[i](x)

	def find_interval(self, x):
		"""
		Finds the index of the interval I_i in which x is located 
		"""
		if x < self.p[0] or x > self.p[self.n - 1]:
			print("ERROR: Evaluation out of range")
			return
		for i in range(0, self.n-1):
			if self.p[i] <= x <= self.p[i+1]:
				return i

def piecewise_cubic(a, b, fa, fb, da, db):
	"""
	Constructs one of the piecewise cubic functions on a given interval
	"""
	dp = b - a
	def q(x):
		# The value of x scaled and translated to the interval [0,1]
		x0 = (x-a)/dp
		
		# x0(x0-1)
		x_x_1 = x0 * (x0 - 1)

		# Values of Hermite basis functions at x0
		V0_x = 1 - 3*x0*x0 + 2*x0*x0*x0
		V1_x = 1 - V0_x
		S0_x = dp * x_x_1 * (x0 - 1)
		S1_x = dp * x_x_1 * x0

		return fa*V0_x + fb*V1_x + da*S0_x + db*S1_x
	return q

def smoothCubic_DEC(p, v, dl, dr):
	"""
	Construct a spline from data, given end derivatives
	"""
	# Construct the two matrices A and B which represent the system of equations we
	# need to solve in order to find the derivative values.
	n = len(p)
	A = TridiagMatrix(n, 0.0, 0.0, 0.0)
	B = Matrix(n,1)

	# We already know the end derivatives
	A[0,0] = 1
	A[n-1,n-1] = 1
	B[0,0] = float(dl)
	B[n-1,0] = float(dr)

	# Fill matrices with equations that make our output function C^2
	for i in range(1,n-1):
		dpi0 = p[i] - p[i-1]
		dpi1 = p[i+1] - p[i]
		B[i,0] = -(v[i-1]*(-6.0/(dpi0*dpi0)) + v[i]*(-6.0/(dpi1*dpi1) + 6.0/(dpi0*dpi0)) + v[i+1]*(6.0/(dpi1*dpi1)))
		A[i,i-1] = -2.0/dpi0
		A[i,i] = -4.0*(1.0/dpi0 + 1.0/dpi1)
		A[i,i+1] = -2.0/dpi1

	A.factor()
	X = TridiagMatrix.solve(A,B)

	d = []
	for i in range(0,n):
		d.append(X[i,0])

	return HermiteCubic(p, v, d)

def not_a_knot(p, v):
	"""
	Construct a not-a-knot spline from data
	"""
	# Construct the two matrices A and B which represent the system of equations we
	# need to solve in order to find the derivative values.
	n = len(p)
	A = TridiagMatrix(n, 0.0, 0.0, 0.0)
	B = Matrix(n,1)

	# Fill rows 1 to n-2 with equations that make our output function C^2 on interior points of the partition
	for i in range(1,n-1):
		dpi0 = p[i] - p[i-1]
		dpi1 = p[i+1] - p[i]
		B[i,0] = -(v[i-1]*(-6.0/(dpi0*dpi0)) + v[i]*(-6.0/(dpi1*dpi1) + 6.0/(dpi0*dpi0)) + v[i+1]*(6.0/(dpi1*dpi1)))
		A[i,i-1] = -2.0/dpi0
		A[i,i] = -4.0*(1.0/dpi0 + 1.0/dpi1)
		A[i,i+1] = -2.0/dpi1

	# Use row 1 to eliminate the element in the (0, 2) position. This makes the matrix tridiagonal.
	# This is equivalent to writing [[g''']] + mult_factor*[[g'']] = 0.
	dp1 = p[1] - p[0]
	dp2 = p[2] - p[1]
	mult_factor = -A[1,2] * dp2*dp2/6.0
	A[0,0] = mult_factor * (-6.0/(dp1*dp1)) + A[1,0]
	A[0,1] = mult_factor * (6.0/(dp2*dp2) - 6.0/(dp1*dp1)) + A[1,1]
	B[0,0] = mult_factor * -(v[0]*(-12.0/(dp1*dp1*dp1)) + v[1]*(12.0/(dp1*dp1*dp1) + 12.0/(dp2*dp2*dp2)) + v[2]*(-12.0/(dp2*dp2*dp2))) + B[1,0]

	# Use row n-2 to elminate the element in the (n-1, n-3) position. This makes the matrix tridiagonal.
	# This is equivalent to writing [[g''']] + mult_factor*[[g'']] = 0.
	dpn_2 = p[n-2] - p[n-3]
	dpn_1 = p[n-1] - p[n-2]
	mult_factor = A[n-2,n-3] * dpn_2*dpn_2/6.0
	A[n-1, n-2] = mult_factor * (6.0/(dpn_1*dpn_1) - 6.0/(dpn_2*dpn_2)) + A[n-2, n-2]
	A[n-1, n-1] = mult_factor * 6.0/(dpn_1*dpn_1) + A[n-2, n-1]
	B[n-1,0] = mult_factor * -(v[n-3]*(-12.0/(dpn_2*dpn_2*dpn_2)) + v[n-2]*(12.0/(dpn_2*dpn_2*dpn_2) + 12.0/(dpn_1*dpn_1*dpn_1)) 
				+ v[n-1]*(-12.0/(dpn_1*dpn_1*dpn_1))) + B[n-2,0]

	A.factor()
	X = TridiagMatrix.solve(A,B)	

	d = []
	for i in range(0,n):
		d.append(X[i,0])

	return HermiteCubic(p, v, d)

"""
# f(x) = x^3 + 2x^2 + 3x + 5
q = HermiteCubic([0,1,5,7], [5, 11, 195, 467], [3, 10, 98, 178])
print("q({}) = {}".format(6, q(6)))
print("q({}) = {}".format(6.5, q(6.5)))
print("q({}) = {}".format(6.75, q(6.75)))
print("q({}) = {}".format(3, q(3)))
print("q({}) = {}".format(2.3, q(2.3)))
print("q({}) = {}".format(7, q(7)))
"""
