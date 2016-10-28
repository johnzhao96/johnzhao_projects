"""
solver.py

Implements Adam's Method for solving the ordinary differential equation:
	y' = f(t, y)
"""

from math import sqrt, pi, pow
from numvec import NumVec

def solve(f, a, b, y0, tol, tracer = (lambda args: None)):
	f_old = f(a, y0)
	f_now = f(a, y0)
	Y_now = y0

	stime = SimTime(a, b)
	while stime.time < stime.endTime:
		Y_now = advance(f, f_old, f_now, Y_now, stime, tol, tracer)
		f_old = f_now
		f_now = f(stime.time, Y_now)

	return Y_now

def step(f, f_old, f_now, dt_old, dt, time, Y_now):
	# Linear extrapolation of f at t_new
	f_new = f_now + (dt/dt_old) * (f_now-f_old)

	# Prediction approximation of f at t_new
	W = Y_now + dt*f_now + (dt*dt)/2 * (f_now-f_old)/dt_old

	# Approximation of f at t_new
	t_old = time-dt_old
	t_new = time+dt
	f_guess = f(t_new, W)

	# Corrected approximation of f at t_new. The integrated quadratic has been
	# factored and thus looks like how it does in the expression.
	Y_new = W + (f_guess-f_new) * (1.0/6.0)*(dt/dt_old)*(3*t_old - 2*time - t_new)
	return (Y_new, Y_new - W) 

def advance(f, f_old, f_now, Y_now, stime, tol, tracer):
	dt_old = stime.dt
	while True:
		test_step = step(f, f_old, f_now, dt_old, stime.dt, stime.time, Y_now)
		Y_guess = test_step[0]
		ei = test_step[1].norm()

		if (ei > tol) and (stime.dt > stime.dt_min):
			# Reject step
			stime.stepsSinceRejection = 0
			stime.stepsRejected += 1
			stime.dt /= 2
			if stime.dt < stime.dt_min:
				stime.dt = stime.dt_min
		else:
			# Accept step

			# Call tracer function to write to output
			tracer(stime, Y_guess)

			# Update metadata regarding step rejections
			stime.stepsSinceRejection += 1
			stime.stepsAccepted += 1
			stime.time += stime.dt

			# Grow or shrink dt
			if stime.stepsSinceRejection > 20:
				if ei < tol/4:
					stime.dt *= stime.agrow
				elif ei > tol*0.75:
					stime.dt *= stime.ashrink

			# End cases near endTime
			if stime.dt > stime.dt_max:
				stime.dt = stime.dt_max
			if stime.time+stime.dt > stime.endTime:
				stime.dt = stime.endTime - stime.time
			elif stime.time + 2*stime.dt > stime.endTime:
				stime.dt = (stime.endTime - stime.time)/2

			return Y_guess

class SimTime:
	def __init__(self, beginTime, endTime):
		self.time = beginTime
		self.dt = 1e-6
		self.dt_old = 0.1
		self.tol = 1e-2
		self.agrow = 1.25
		self.ashrink = 0.8
		self.dt_min = 1e-6
		self.dt_max = 1.0
		self.endTime = endTime
		
		self.stepsSinceRejection = 0
		self.stepsRejected = 0
		self.stepsAccepted = 0
