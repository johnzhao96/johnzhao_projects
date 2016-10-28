"""
matrix.py

Implementation of matrix operations.
Implements two classes: Matrix and TridiagMatrix
"""
import sys

class Matrix:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.matrix = []
		for i in range(0, rows):
			self.matrix.append([0.0]*cols)

	def __getitem__(self, loc):
		return self.matrix[loc[0]][loc[1]]

	def __setitem__(self, loc, value):
		self.matrix[loc[0]][loc[1]] = value

	def __mul__(self, other):
		if isinstance(other, Matrix):
			"""
			Matrix multiplication
			"""
			if self.cols != other.rows:
				print("ERROR: Incompatible sizes for matrix multiplication")
				return
			result = Matrix(self.rows, other.cols)
			for i in range(0, self.rows):
				for j in range(0, other.cols):
					for k in range(0, self.cols):
						result[i,j] += self[i,k] * other[k,j]
			return result
		else:
			"""
			Right Scalar multiplication
			"""
			result = Matrix(self.rows, self.cols)
			for i in range(0, self.rows):
				for j in range(0, self.cols):
					result[i,j] = self[i,j] * other
			return result

	def __rmul__(self, other):
		"""
		Left Scalar multiplication
		"""
		result = Matrix(self.rows, self.cols)
		for i in range(0, self.rows):
			for j in range(0, self.cols):
				result[i,j] = self[i,j] * other
		return result

	def __add__(self, other):
		if self.rows != other.rows or self.cols != other.cols:
			print("ERROR: Incompatible sizes for matrix addition")
			return
		result = Matrix(self.rows, self.cols)
		for i in range(0, self.rows):
			for j in range(0, self.cols):
				result[i,j] = self[i,j] + other[i,j]
		return result

	def __sub__(self, other):
		if self.rows != other.rows or self.cols != other.cols:
			print("ERROR: Incompatible sizes for matrix subtraction")
			return
		result = Matrix(self.rows, self.cols)
		for i in range(0, self.rows):
			for j in range(0, self.cols):
				result[i,j] = self[i,j] - other[i,j]
		return result

	def __repr__(self):
		representation = self.matrix[0].__repr__()
		for i in range(1, self.rows):
			representation += "\n" + self.matrix[i].__repr__()
		return representation

	def factor(self):
		if self.rows != self.cols:
			print("ERROR: Incompatible size for matrix factorization")
			return
		for i in range(0, self.rows):
			# Modify the ith row
			self[i,i] = 1.0 / self[i,i]
			for j in range(i+1, self.cols):
				self[i,j] = self[i,j] * self[i,i]

			# Modify the rest of the subsequent rows
			for k in range(i+1, self.cols):
				self[k, i] = -self[k,i]
				for j in range(i+1, self.cols):
					self[k,j] = self[k,j] + self[k,i]*self[i,j] 

	def solve(A, B):
		"""
		Assumes A is square and has been factored
		"""
		if A.rows != A.cols:
			print("ERROR: Matrix A must be square for solving")
			return
		if A.cols != B.rows:
			print("ERROR: Incompatible sizes for matrix solving")
			return
		
		result = Matrix(B.rows, B.cols)
		
		# Compute the matrix L^-1 * B, where A = LU, U upper triangular
		L1B = Matrix(B.rows, B.cols)
		for i in range(0, B.rows):
			for j in range(0, B.cols):
				L1B[i,j] = B[i,j]
		for i in range(0, B.rows):
			# Multiply by L_d
			for j in range(0, B.cols):
				L1B[i,j] = A[i,i] * L1B[i,j]
			# Multiply by L_c
			for k in range(i+1, B.rows):
				for j in range(0, B.cols):
					L1B[k,j] = L1B[k,j] + A[k,i]*L1B[i,j]

		# Solve the equation UX = L1B
		for i in range(B.rows-1, -1, -1):
			for k in range(0, B.cols):
				temp = 0
				for j in range(i+1, A.cols):
					temp += A[i,j] * result[j,k]
				result[i,k] = L1B[i,k] - temp

		return result


class TridiagMatrix:
	def __init__(self, r, bv, dv, av):
		self.rows = r
		self.matrix = [[float(bv)]*(r-1) , [float(dv)]*r , [float(av)]*(r-1)]

	def __getitem__(self, loc):
		if loc[0] >= self.rows or loc[1] >= self.rows:
			print("ERROR: TridiagMatrix index out of range")
			return
		if abs(loc[0] - loc[1]) > 1:
			return 0.0
		else:
			if loc[1] < loc[0]:
				return self.matrix[0][loc[1]]
			elif loc[1] == loc[0]:
				return self.matrix[1][loc[1]]
			else:
				return self.matrix[2][loc[1]-1]

	def __setitem__(self, loc, value):
		if loc[0] >= self.rows or loc[1] >= self.rows:
			print("ERROR: TridiagMatrix index out of range")
			return
		if abs(loc[0] - loc[1]) > 1:
			print("ERROR: Cannot modify non tridiagonal entries of TridiagMatrix: {} {}".format(loc[0], loc[1]))
			return
		else:
			if loc[1] < loc[0]:
				self.matrix[0][loc[1]] = value
			elif loc[1] == loc[0]:
				self.matrix[1][loc[1]] = value
			else:
				self.matrix[2][loc[1]-1] = value

	def __repr__(self):
		result = '['
		for j in range(0, self.rows):
			result += '{}, '.format(self[0,j])
		result += ']'
		for i in range(1, self.rows):
			result += '\n['
			for j in range(0, self.rows):
				result += '{}, '.format(self[i,j])
			result += ']'
		return result

	def __mul__(self, other):
		if isinstance(other, Matrix):
			if self.rows != other.rows:
				print("ERROR: Incompatible sizes for matrix multiplication")
				return
			result = Matrix(other.rows, other.cols)
			for i in range(0, other.rows):
				for j in range(0, other.cols):
					result[i,j] += self[i,i] * other[i,j]
					if i > 0:
						result[i,j] += self[i,i-1] * other[i-1,j]
					if i < self.rows - 1:
						result[i,j] += self[i,i+1] * other[i+1,j]
		else:
			result = TridiagMatrix(self.rows, 0, 0, 0)
			for i in range(0, self.rows-1):
				result.matrix[0][i] = self.matrix[0][i] * other
				result.matrix[1][i] = self.matrix[1][i] * other
				result.matrix[2][i] = self.matrix[2][i] * other
			result.matrix[1][self.rows-1] = self.matrix[1][self.rows-1] * other
		return result

	def factor(self):
		for i in range(0, self.rows):
			# Modify the ith row
			self[i,i] = 1.0 / self[i,i]
			if i+1 < self.rows:
				self[i,i+1] = self[i,i+1] * self[i,i]

			# Modify the (i+1)th row
			if i+1 < self.rows:
				self[i+1, i] = -self[i+1,i]
				self[i+1, i+1] = self[i+1,i+1] + self[i+1,i]*self[i,i+1]
				if (i+2 < self.rows):
					 self[i+1,i+2] = self[i+1,i+2] + self[i+1,i]*self[i,i+2]

	def solve(A, B):
		"""
		Assumes A is square and has been factored
		"""
		if A.rows != B.rows:
			print("ERROR: Incompatible sizes for matrix solving")
			return
		
		result = Matrix(B.rows, B.cols)
		
		# Compute the matrix L^-1 * B, where A = LU, U upper triangular
		L1B = Matrix(B.rows, B.cols)
		for i in range(0, B.rows):
			for j in range(0, B.cols):
				L1B[i,j] = B[i,j]
		for i in range(0, B.rows):
			# Multiply by L_d
			for j in range(0, B.cols):
				L1B[i,j] = A[i,i] * L1B[i,j]
			# Multiply by L_c
			if i+1 < B.rows:
				for j in range(0, B.cols):
					L1B[i+1,j] = L1B[i+1,j] + A[i+1,i]*L1B[i,j]

		# Solve the equation UX = L1B
		for i in range(B.rows-1, -1, -1):
			for k in range(0, B.cols):
				temp = 0
				for j in range(i+1, A.rows):
					temp += A[i,j] * result[j,k]
				result[i,k] = L1B[i,k] - temp

		return result


"""
# Matrix Arithmetic Tests
A = Matrix(2,2)
B = Matrix(2,2)

A[0,0] = 1.0
A[1,1] = 1.0

B[0,0] = 3.0
B[0,1] = 4.0

print(A)
print(B)

print("Addition:")
print(A+B)
print("Subtraction:")
print(A-B)
print("Multiplication:")
print(A*B)
"""
"""
# Matrix Factoring Test
A = Matrix(3,3)
for i in range(0,3):
	for j in range(0,3):
		A[i,j] = 3*i + j + 1
A[2,2] = 10

print(A)

print("Solution:")
A.factor()
print(A)
"""
"""
TridiagMatrix Arithmetic Tests
A = TridiagMatrix(4,1,2,3)
A[3,2] = 5.0
A[1,2] = 6.0

B = Matrix(4,4)
B.matrix = [
	[1,2,3,4],
	[5,6,7,8],
	[9,10,11,12],
	[13,14,15,16]
]

A0 = Matrix(4,4)
for i in range(0,4):
	for j in range(0,4):
		A0[i,j] = A[i,j]

print("A:")
print(A)
print("\nB:")
print(B)
print("\nA*B:")
print(A*B)
print("\nCorrect A*B")
print(A0*B)
print("\nA*3:")
print(A*3)
"""

