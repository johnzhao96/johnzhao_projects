"""
heap.py

Implementation of general (Min/Max) Heap data structure.

The underlying heap array is 0-indexed, thus each index k has children
	2k+1 and 2k+2.

By default, Heap implements a max heap. This behavior can be changed by
changing the input "comparator" comparison operator that a heap is
initialized with.
"""

class Heap:
	def __init__(self, comparator=lambda x,y: x < y):
		self._size = 0
		self._compare = comparator
		self._array = []

	def __getitem__(self, idx):
		return self._array[idx]

	def __setitem__(self, idx, elm):
		self._array[idx] = elm

	def __str__(self):
		return self._array[0:self._size].__str__()

	def __repr__(self):
		return self.__str__()

	def _sift_up(self, idx):
		elm = self._array[idx]
		curr = idx
		par = (idx-1) >> 1
		while (curr > 0) and self._compare(self._array[par], elm):
			self._array[curr] = self._array[par]
			curr = par
			par = (curr-1) >> 1
		self._array[curr] = elm

	def _sift_down(self, idx):
		elm = self._array[idx]
		curr = idx
		l_child = (idx << 1) + 1
		while l_child < self._size:
			r_child = l_child+1
			if l_child+1 < self._size and self._compare(self._array[l_child], self._array[r_child]):
				self._array[curr] = self._array[r_child]
				curr = r_child
				l_child = (curr << 1) + 1
			else:
				self._array[curr] = self._array[l_child]
				curr = l_child
				l_child = (curr << 1) + 1
		self._array[curr] = elm
		self._sift_up(curr)

	def peek(self):
		if self._size == 0:
			return None
		return self._array[0]

	def pop(self):
		if self._size == 0:
			return None
		elm = self._array[0]
		self._array[0] = self._array[self._size-1]
		self._size -= 1
		self._sift_down(0)
		return elm

	def push(self, elm):
		if self._size < len(self._array):
			self._array[self._size] = elm
		else:
			self._array.append(elm)
		self._size += 1
		self._sift_up(self._size-1)

	def delete(self, idx):
		if idx < 0 or idx >= self._size:
			return
		self._array[idx] = self._array[self._size-1]
		self._sift_up(idx)
		self._sift_down(idx)
		self._size -= 1

