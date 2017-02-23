import heapq
import sys
import random
import time
from heap import Heap

size = int(sys.argv[1])

l = []
for i in range(size):
	l.append(random.randint(0,4*size))
s = [0] * size

"""
# heapq implementation
t0 = time.clock()
h = []
for elm in l:
	heapq.heappush(h, elm)

for i in range(0, len(l)):
	s[i] = heapq.heappop(h)
t1 = time.clock()
print(t1-t0)

# my Heap implementation
t0 = time.clock()
h = Heap()
for elm in l:
	h.push(elm)

for i in range(0, len(l)):
	s[i] = h.pop()
t1 = time.clock()
print(t1-t0)
"""

def test_heap_invariant(h):
	for i in range(0, h._size):
		if 2*i+1 < h._size and h[i] > h[2*i+1]:
			return False
		if 2*i+2 < h._size and h[i] > h[2*i+2]:
			return False
	return True

myHeap = Heap(comparator = lambda x,y: x > y)
for x in l:
	myHeap.push(x)
	if random.randint(0,1) == 0:
		myHeap.pop()

print(myHeap)
print(test_heap_invariant(myHeap))

s = []
length = myHeap._size
for i in range(0, length):
	s.append(myHeap.pop())

print(s)



