"""
Brachistochrone -- the fastest slide, as a convex problem.

Lecture 1 demo, Continuous Optimization (MasterMath) -- Bart Van Parys.

Johann Bernoulli (1696): along which curve does a bead slide under gravity
from the origin to a point (L, H below) in the least time? By conservation
of energy the speed at depth y is sqrt(2 g y), so for a curve z(s) =
(x(s), y(s)), s in [0, 1], the travel time is

    T[z] = int_0^1 ||z'(s)|| / sqrt(2 g y(s)) ds.

T is not convex in z, but by Cauchy-Schwarz the ENERGY

    E[z] = int_0^1 ||z'(s)||^2 / (2 g y(s)) ds  >=  T[z]^2,

with equality at constant metric speed (any curve can be reparametrised so),
hence min E = (min T)^2. The integrand ||p||^2 / y is the perspective
function -- jointly convex in (p, y) -- so E is a convex functional of the
completely free curve z: a second-order-cone program after discretisation
(one quad_over_lin term per segment). A floor y <= d is a linear constraint.

The classical answer is a cycloid; we verify the solver rediscovers it.

Run locally with:  pip install cvxpy numpy scipy  &&  python brachistochrone.py
"""

import numpy as np
import cvxpy as cp

g = 9.81         # gravity (m/s^2)
L, H = 2.5, 1.0  # end point: L to the right, H straight down

# The curve z_k = (x_k, y_k) at s_k = k/N, completely free.
N = 300
Z = cp.Variable((N + 1, 2))
dZ = cp.diff(Z, axis=0)
y_seg = (Z[:-1, 1] + Z[1:, 1]) / 2      # mean depth of each segment

E = N * cp.sum(cp.vstack([cp.quad_over_lin(dZ[k], y_seg[k])
                          for k in range(N)])) / (2 * g)

problem = cp.Problem(cp.Minimize(E), [Z[0] == [0, 0], Z[N] == [L, H]])
problem.solve()

print(f"Status: {problem.status}")
print(f"Travel time = sqrt(E)             : {np.sqrt(problem.value):.6f} s")
print(f"Deepest point reached             : {Z.value[:, 1].max():.4f}")

# Bernoulli's closed-form answer: a cycloid x = r(t - sin t), y = r(1 - cos t)
# through (L, H), reached at angle Theta, with travel time Theta sqrt(r/g).
from scipy.optimize import brentq

theta = brentq(lambda t: (t - np.sin(t)) / (1 - np.cos(t)) - L / H,
               1e-3, 2 * np.pi - 1e-3)
r = H / (1 - np.cos(theta))
print(f"Travel time (Bernoulli's cycloid) : {theta * np.sqrt(r / g):.6f} s")

# A floor at depth d < the free dip: one linear constraint, no closed form.
d = 1.05
problem_f = cp.Problem(cp.Minimize(E),
                       [Z[0] == [0, 0], Z[N] == [L, H], Z[:, 1] <= d])
problem_f.solve()
print(f"Travel time with a floor at {d}  : {np.sqrt(problem_f.value):.6f} s")
