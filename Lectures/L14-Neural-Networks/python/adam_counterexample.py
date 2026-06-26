"""
Adam can converge to the WRONG point: the Reddi-Kale-Kumar (2018) counterexample.
======================================================================================

Reference
    S. J. Reddi, S. Kale, S. Kumar.
    "On the Convergence of Adam and Beyond." ICLR 2018 (best paper).

The problem (online, one dimension, x constrained to [-1, 1])
    The gradient seen at step t is periodic with period 3:

        g_t =  +C   if  t % 3 == 1        (a large, RARE  gradient)
        g_t =  -1   otherwise             (a small, FREQUENT gradient)

    The cumulative loss over one period is (C - 2) * x, so for C > 2 it is
    INCREASING in x and the optimum sits at  x* = -1.  A sound method must
    therefore decrease x toward -1.

What each method does
    * SGD      uses the raw gradient: the rare +C step (magnitude C) outweighs the
               two -1 steps, so x drifts to -1.  Correct.
    * Adam     divides by sqrt(v), the running second moment.  This normalises the
               rare large gradient down to ~1, so it can no longer outvote the two
               frequent small gradients -> x drifts to +1.  WRONG corner.
    * AMSGrad  Reddi et al.'s fix: it uses v_hat = max-so-far, which keeps the
               denominator large after the big gradient, restoring convergence to -1.

We set beta1 = 0 to isolate the adaptive denominator 1/sqrt(v) -- the actual source
of the pathology (this matches the paper's deterministic Theorem 1).  With momentum
(beta1 = 0.9) the moving average can mask the effect on THIS particular sequence; the
paper's *stochastic* construction breaks Adam for any admissible (beta1, beta2).
beta2 = 0.7 lets v decay fast enough to expose the failure within a few thousand
steps; the same pathology occurs at the default beta2 = 0.999, but only for larger C
and far longer horizons.
"""

import numpy as np
import matplotlib.pyplot as plt


def gradient(t, C):
    """Periodic gradient of the Reddi counterexample (period 3)."""
    return C if (t % 3 == 1) else -1.0


def optimize(method, T, C, lr=0.02, beta1=0.0, beta2=0.7, eps=1e-8):
    """Run `method` in {'sgd','adam','amsgrad'} for T steps; return the trajectory x_t."""
    x, m, v, vhat_max = 0.0, 0.0, 0.0, 0.0
    xs = np.empty(T)
    for t in range(1, T + 1):
        g = gradient(t, C)
        m = beta1 * m + (1 - beta1) * g            # 1st moment (EMA of gradient)
        v = beta2 * v + (1 - beta2) * g * g        # 2nd moment (EMA of squared gradient)
        m_hat = m / (1 - beta1 ** t) if beta1 > 0 else m   # bias correction
        v_hat = v / (1 - beta2 ** t)

        if method == "sgd":
            x -= lr * g
        elif method == "adam":
            x -= lr * m_hat / (np.sqrt(v_hat) + eps)
        elif method == "amsgrad":
            vhat_max = max(vhat_max, v_hat)
            x -= lr * m_hat / (np.sqrt(vhat_max) + eps)
        else:
            raise ValueError(method)

        x = min(1.0, max(-1.0, x))                 # project onto the domain [-1, 1]
        xs[t - 1] = x
    return xs


def main():
    C = 2.2          # optimum is x* = -1 (since C > 2); Adam will head for +1 instead
    T = 3000

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))

    # --- (left) trajectories of the three methods ---------------------------------
    for method, color in [("adam", "C3"), ("sgd", "C0"), ("amsgrad", "C2")]:
        ax[0].plot(optimize(method, T, C), color=color, lw=1.8, label=method)
    ax[0].axhline(-1, ls="--", color="gray", lw=1)
    ax[0].text(T * 0.45, -0.93, r"optimum $x^\star=-1$", color="gray")
    ax[0].set(xlabel="iteration", ylabel=r"$x_t$", ylim=(-1.1, 1.1),
              title=rf"Reddi counterexample  ($C={C}$, $\beta_1=0$, $\beta_2=0.7$)")
    ax[0].legend()

    # --- (right) Adam's limit as a function of C: a whole failure BAND -------------
    Cs = np.linspace(2.0, 3.0, 60)
    finals = [optimize("adam", 8000, c)[-1] for c in Cs]
    ax[1].axhline(0, color="gray", lw=0.6)
    ax[1].plot(Cs, finals, "o-", ms=3, color="C3")
    ax[1].set(xlabel="C", ylabel=r"Adam's final $x$",
              title=r"Adam $\to +1$ over a band of $C$ (not a single fluke)")

    plt.tight_layout()
    plt.savefig("adam_counterexample.png", dpi=120)
    print("Saved adam_counterexample.png")
    for m in ("adam", "sgd", "amsgrad"):
        print(f"  final x  [{m:>7}] = {optimize(m, 8000, C)[-1]:+.3f}")


if __name__ == "__main__":
    main()
