"""
Newton's method -- local quadratic convergence and how it can fail.

Python port of the Lecture 9 examples (originally Julia).
Continuous Optimization (MasterMath) -- Bart Van Parys.

Newton's method minimises f by repeatedly minimising its second-order Taylor
model, which gives the iteration

    x_{k+1} = x_k - f''(x_k)^{-1} f'(x_k).

We run it on the two examples from the slides:

    Example I   f(x) = 7x - log(x)              minimiser x* = 1/7
    Example II  f(x) = log(exp(2x) + exp(-2x))   minimiser x* = 0

Near x* the number of correct digits doubles in every step, but far from x*
the iterates can leave the domain (Example I) or diverge (Example II).

Run locally with:  pip install numpy matplotlib  &&  python newton.py
"""

import numpy as np
import matplotlib.pyplot as plt

EXAMPLES = {
    "I": dict(
        name="Example I: f(x) = 7x - log(x)",
        f=lambda x: 7 * x - np.log(x),
        fp=lambda x: 7 - 1 / x,
        fpp=lambda x: 1 / x**2,
        domain=lambda x: x > 0,
        xstar=1 / 7,
        plot_range=(1e-3, 0.5),
    ),
    "II": dict(
        name="Example II: f(x) = log(exp(2x) + exp(-2x))",
        f=lambda x: np.logaddexp(2 * x, -2 * x),
        fp=lambda x: 2 * np.tanh(2 * x),
        fpp=lambda x: 4 / np.cosh(2 * x) ** 2,
        domain=lambda x: np.isfinite(x) and abs(x) < 1e3,
        xstar=0.0,
        plot_range=(-2.0, 2.0),
    ),
}


def newton(ex, x0, N):
    """Run N Newton steps from x0. Stops early if an iterate leaves the domain."""
    xs = [x0]
    status = "converging"
    for _ in range(N):
        x = xs[-1]
        with np.errstate(over="ignore", divide="ignore"):
            x_new = x - ex["fp"](x) / ex["fpp"](x)
        xs.append(x_new)
        if not ex["domain"](x_new):
            status = "left the domain" if np.isfinite(x_new) else "diverged"
            break
        if abs(x_new - ex["xstar"]) < 1e-16:
            break
    return np.array(xs), status


def show(key, x0, N=8):
    """Print the iterates and plot f with the Newton steps and the error |x_k - x*|."""
    ex = EXAMPLES[key]
    xs, status = newton(ex, x0, N)

    print(ex["name"], f"  x0 = {x0}")
    print(" k            x_k        |x_k - x*|")
    for k, x in enumerate(xs):
        print(f"{k:2d}  {x:16.10g}  {abs(x - ex['xstar']):12.3e}")
    print("Status:", status)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    # Left: f together with the quadratic models used by Newton's method.
    lo, hi = ex["plot_range"]
    t = np.linspace(lo, hi, 1000)
    ax1.plot(t, ex["f"](t), "k", label="$f$")
    for k, x in enumerate(xs[:-1]):
        if not (lo <= x <= hi):
            break
        q = ex["f"](x) + ex["fp"](x) * (t - x) + 0.5 * ex["fpp"](x) * (t - x) ** 2
        ax1.plot(t, q, color="tab:red", alpha=0.5, lw=1,
                 label="quadratic model" if k == 0 else None)
        ax1.plot(x, ex["f"](x), "o", color="tab:red", ms=4)
        ax1.annotate(f"$x_{k}$", (x, ex["f"](x)), textcoords="offset points",
                     xytext=(4, 4), fontsize=8)
    ax1.axvline(ex["xstar"], color="gray", ls=":", lw=1)
    fmin, fmax = ex["f"](t).min(), ex["f"](t).max()
    ax1.set_ylim(fmin - 0.1 * (fmax - fmin), fmax)
    ax1.set_xlim(lo, hi)
    ax1.set_xlabel("$x$")
    ax1.set_title(ex["name"])
    ax1.legend(loc="upper center")

    # Right: the error on a log scale (quadratic convergence = ever steeper drop).
    err = np.abs(xs - ex["xstar"])
    k = np.arange(len(xs))
    ax2.semilogy(k[err > 0], err[err > 0], "o-", color="tab:red")
    ax2.set_xlabel("$k$")
    ax2.set_ylabel("$|x_k - x^\\star|$")
    ax2.set_title(f"Status: {status}")
    ax2.grid(True, which="both", alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # The starting points of the tables on the slides.
    for key, x0 in [("I", 1.0), ("I", 0.01), ("I", 0.1), ("II", 0.6), ("II", 0.5)]:
        show(key, x0)
