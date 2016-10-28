"""
main.py

Full matrix solver tester
"""

from matrix import Matrix, TridiagMatrix

A = Matrix(4,4)
B = Matrix(4,2) 
X = Matrix(4,2)

for i in range(0, 4):
	for j in range(0, 4):
		A[i,j] = 0.01*i*i+0.02*j
  	A[i,i] += 3.0+0.3*i;
  	for j in range(0,2):
		X[i,j] = i+1.0+4.0*j

print("Test of full matrix\nThe results should be:")
print(X)

B = A*X;
A.factor();

X = Matrix.solve(A,B);

print("The results are:")
print(X)


print("\nTest of tridiagonal matrix\nThe results should be:")
print(X)

C = TridiagMatrix(4,-1.0, 3.0, -1.0)

for i in range(0,4):
	C[i,i] += 0.1*(i+1)-0.001*i*i
	if i == 3:
		break
	C[i+1,i] -= 0.02*(i+1)
	C[i,i+1] -= 0.03*i*i


B = C*X;
C.factor();
X = TridiagMatrix.solve(C,B);

print("The results are:")
print(X)
