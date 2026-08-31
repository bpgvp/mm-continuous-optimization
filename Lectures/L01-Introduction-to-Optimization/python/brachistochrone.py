"""
Brachistochrone -- the fastest slide, as a convex problem.

Lecture 1 demo, Continuous Optimization (MasterMath) -- Bart Van Parys.

Johann Bernoulli (1696): along which curve does a bead slide under gravity
from the origin to a point (L, H below) in the least time? By conservation
of energy the speed at depth y is sqrt(2 g y). Parametrising the curve by
its *depth* -- horizontal position x(y) for y in [0, H] -- the travel time

    T[x] = int_0^H sqrt(1 + x'(y)^2) / sqrt(2 g y) dy,   x(0)=0, x(H)=L,

is a CONVEX functional of x: the integrand depends on x only through x'(y)
(a linear operation), p |-> sqrt(1 + p^2) is convex, and the weight
1/sqrt(2 g y) is a positive constant for each y. Discretised on a depth
grid this is a small second-order-cone program. (The parametrisation
assumes the curve is a graph over depth, valid whenever L/H <= pi/2.)

The classical answer is a cycloid; we verify the solver rediscovers it.

Run locally with:  pip install cvxpy numpy  &&  python brachistochrone.py
"""

import numpy as np
import cvxpy as cp

g = 9.81      # gravity (m/s^2)
L, H = 1.0, 1.0  # end point: L to the right, H straight down (keep L/H <= pi/2)

# Discretise the depth interval [0, H] into N segments. On a straight segment
# the time int dy sqrt(1+(dx/h)^2) / sqrt(2 g y) integrates in closed form, so
# with these weights the objective is the EXACT travel time of the
# piecewise-linear path -- no quadrature error, only discretisation error.
N = 500
h = H / N
y = np.arange(N + 1) * h
w = np.sqrt(2 / g) * (np.sqrt(y[1:]) - np.sqrt(y[:-1])) / h

# Decision variable: horizontal position x_k at depth y_k = k h.
x = cp.Variable(N + 1)

# Segment length sqrt(h^2 + (x_{k+1}-x_k)^2): the norm of an affine expression.
seg = cp.norm(cp.vstack([np.full(N, h), cp.diff(x)]), 2, axis=0)

objective = cp.Minimize(w @ seg)       # total travel time (midpoint rule)
constraints = [x[0] == 0, x[N] == L]

problem = cp.Problem(objective, constraints)
problem.solve()

print(f"Status: {problem.status}")
print(f"Travel time (convex optimization) : {problem.value:.6f} s")

# Bernoulli's closed-form answer: a cycloid x = r(t - sin t), y = r(1 - cos t)
# through (L, H), reached at angle t = Theta, with travel time Theta sqrt(r/g).
from scipy.optimize import brentq

theta = brentq(lambda t: (t - np.sin(t)) / (1 - np.cos(t)) - L / H, 1e-3, np.pi)
r = H / (1 - np.cos(theta))
print(f"Travel time (Bernoulli's cycloid) : {theta * np.sqrt(r / g):.6f} s")

# A straight slide, for comparison (the same weights time it exactly).
straight = np.hypot(h, L / N) * np.sum(w)
print(f"Travel time (straight line)       : {straight:.6f} s")
