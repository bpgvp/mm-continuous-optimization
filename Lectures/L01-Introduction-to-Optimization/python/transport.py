"""
Transport logistics -- Dantzig's classical transportation problem.

Lecture 1 demo, Continuous Optimization (MasterMath) -- Bart Van Parys.

The canonical example from G. B. Dantzig, "Linear Programming and
Extensions" (1963), Chapter 3-3: two canneries (Seattle, San Diego) ship
cases of a product to three markets (New York, Chicago, Topeka). Shipping
costs $90 per case per thousand miles. Find the shipping plan of minimal
total cost meeting all demand within the available supply.

This is the linear program from the lecture with x_{ij} the amount shipped
from facility j to consumer i:

    min  sum_{ij} c_{ij} x_{ij}
    s.t. x_{ij} >= 0
         sum_i x_{ij} <= s_j   (supply at facility j)
         sum_j x_{ij} >= d_i   (demand of consumer i)

Run locally with:  pip install cvxpy numpy  &&  python transport.py
"""

import numpy as np
import cvxpy as cp

facilities = ["Seattle", "San Diego"]
consumers = ["New York", "Chicago", "Topeka"]

s = np.array([350, 600])       # supply s_j (cases)
d = np.array([325, 300, 275])  # demand d_i (cases)

# Distances in thousands of miles, consumers (rows) x facilities (columns).
dist = np.array([
    [2.5, 2.5],  # New York
    [1.7, 1.8],  # Chicago
    [1.8, 1.4],  # Topeka
])
c = 90 * dist  # marginal cost c_ij in $ per case: freight $90 per case per 1000 miles

# Decision variable: x_ij = amount shipped from facility j to consumer i.
x = cp.Variable((3, 2), nonneg=True)

constraints = [
    cp.sum(x, axis=0) <= s,  # ship no more than each facility stocks
    cp.sum(x, axis=1) >= d,  # meet every consumer's demand
]

objective = cp.Minimize(cp.sum(cp.multiply(c, x)))

problem = cp.Problem(objective, constraints)
problem.solve()

print(f"Status: {problem.status}")
print(f"Minimal total shipping cost = {problem.value:.2f} dollar")
print()
for i, market in enumerate(consumers):
    for j, plant in enumerate(facilities):
        if x.value[i, j] > 1e-6:
            print(f"  {plant:10s} -> {market:9s} : {x.value[i, j]:6.1f} cases")
