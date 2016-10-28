"""
main.py

Runs the solver to simulate the falling marble.
"""
from solver import solve
from math import sqrt, log, pi
from numvec import NumVec

# Radius of Earth
R = 2e7/pi
CIN = 9.8/R

def fmarble(time, Y):
	"""
	Differential function for the motion of the marble. Since we are given the function for the
	second derivative:
		p''(t) = - Cin p
	we will solve for both the marble's current x and y positions, as well as its current x and 
	y velocities.

	Y[0] = px	:	x position
	Y[1] = py   :	y position
	Y[2] = vx	:	x velocity
	Y[3] = vy	:	y velocity
	"""
	val = NumVec(4)
	
	val[0] = Y[2]
	val[1] = Y[3]
	
	val[2] = -Y[0] * CIN
	val[3] = -Y[1] * CIN
	return val

def marble_tracer(filepath):
	"""
	Takes an output file and constructs a tracer function that we will pass to the solver. At each 
	accepted forward step of the solver, the tracer function is responsible for writing to output 
	the marble's location, the current time, the time step used, and the current energy.
	"""
	trace_file = open(filepath, 'w')
	def tracer(stime, Y):
		# E(t) = [ (sq(px')+sq(py')) + Cin * (sq(px)+sq(py)) ]/2
		energy = (Y[2]*Y[2]+Y[3]*Y[3] + CIN*(Y[0]*Y[0]+Y[1]*Y[1])) / 2
		trace_file.write('{} {} {} {} {}\n'.format(Y[0], Y[1], stime.time, log(stime.dt, 10), energy))
	return tracer

initial_px = R
initial_vy = R*2*pi/(24*60*60)
solve(fmarble, 0.0, 10000.0, NumVec(4, [initial_px, 0.0, 0.0, initial_vy]), 1e-2, marble_tracer('plots/marble_trace.txt'))
