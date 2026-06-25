"""
Statistical risk -- worst-case probability of loss.

Python/CVXPY port of the Lecture 1 demo (originally Julia/JuMP).
Continuous Optimization (MasterMath) -- Bart Van Parys.

Given moment information about a revenue distribution R supported on n
equidistant points in [-10, 100], find the worst-case (largest) probability
of a loss P(R < 0) that is consistent with that information. This is a linear
program in the probability masses p_i = P(R = r_i).

Run locally with:  pip install cvxpy numpy  &&  python risk.py
"""

import numpy as np
import cvxpy as cp

# Support: n equidistant points on [-10, 100].
n = 100_000
r = np.linspace(-10, 100, n)

# Decision variable: the probability mass p_i = P(R = r_i).
p = cp.Variable(n, nonneg=True)

# p is a probability distribution + the given prior (moment) information.
constraints = [
    cp.sum(p) == 1,                                     # total probability
    cp.sum(cp.multiply(r, p)) >= 15,                    # E[R] in [15, 20]
    cp.sum(cp.multiply(r, p)) <= 20,
    cp.sum(cp.multiply(r**2, p)) >= 500,                # E[R^2] in [500, 600]
    cp.sum(cp.multiply(r**2, p)) <= 600,
    cp.sum(cp.multiply(3 * r**3 - 2 * r, p)) == 40000,  # E[3R^3 - 2R] = 40000
]

# Objective: maximise the probability of a loss, P(R < 0).
objective = cp.Maximize(cp.sum(p[r < 0]))

problem = cp.Problem(objective, constraints)
problem.solve()

print(f"Status: {problem.status}")
print(f"Worst-case probability of loss  P(R < 0) = {problem.value:.4f}")
