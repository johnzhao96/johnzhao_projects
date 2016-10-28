"""
numvec.py

Implementation of NumVec class, a class representation of vectors in R^n.
"""
from math import sqrt

class NumVec:
	def __init__(self, size, vals = None):
		self.size = size
		if vals is None:
			self.vec = [0.0] * size
		else:
			self.vec = vals

	def __getitem__(self, idx):
		return self.vec[idx]

	def __setitem__(self, idx, value):
		self.vec[idx] = value

	def __add__(self, other):
		vecsum = NumVec(self.size)
		for i in range(0, self.size):
			vecsum[i] = self[i] + other[i]
		return vecsum

	def __sub__(self, other):
		vecdif = NumVec(self.size)
		for i in range(0, self.size):
			vecdif[i] = self[i] - other[i]
		return vecdif

	def __mul__(self, scalar):
		"""
		Defines right scalar multiplication
		"""
		vecprod = NumVec(self.size)
		for i in range(0, self.size):
			vecprod[i] = scalar * self[i]
		return vecprod

	def __rmul__(self, scalar):
		"""
		Defines left scalar multiplication
		"""
		vecprod = NumVec(self.size)
		for i in range(0, self.size):
			vecprod[i] = scalar * self[i]
		return vecprod

	def __div__(self, scalar):
		"""
		Defines scalar division
		"""
		vecquot = NumVec(self.size)
		for i in range(0, self.size):
			vecquot[i] = self[i] / scalar
		return vecquot

	def __eq__(self, other):
		for i in range(self.size):
			if self[i] != other[i]:
				return False
		return True

	def __str__(self):
		return self.vec.__str__()

	def __repr__(self):
		return self.vec.__repr__()

	def norm(self):
		sum_squares = 0
		for xi in self.vec:
			sum_squares += xi*xi
		return sqrt(sum_squares)
