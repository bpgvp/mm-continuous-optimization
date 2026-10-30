# 9. Newton's Method

*Mon 2 Nov (wk 45)*

[&larr; Back to course homepage](https://bpgvp.github.io/mm-continuous-optimization/)

## Contents

- From the gradient method to Newton's method: minimising the best local quadratic approximation
- Examples where Newton's method fails far from the minimiser: undefined iterates and divergence
- Local quadratic convergence (Kantorovich): N = O(log log(1/&epsilon;)), but only locally
- Affine invariance of Newton's method, and why Kantorovich's result is not affine invariant
- Equality constrained problems: the constrained Newton step as the solution of a linear (KKT) system
- The null space method: reduction to an unconstrained problem
- Sequential quadratic optimization

## Materials

- [Lecture slides (PDF)](https://bpgvp.github.io/mm-continuous-optimization/L9-Newtons-Method.pdf)
- [Newton's method demo](https://colab.research.google.com/github/bpgvp/mm-continuous-optimization/blob/main/Lectures/L09-Newtons-Method/python/newton.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bpgvp/mm-continuous-optimization/blob/main/Lectures/L09-Newtons-Method/python/newton.ipynb)
- Related reading: sections 9.5 and 10.1&ndash;10.3 of [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf) by Boyd &amp; Vandenberghe
