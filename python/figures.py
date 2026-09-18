#!/usr/bin/env python3
"""
Regenerate Figs. 1-5 of the paper with matplotlib.
Output: fig1.png ... fig5.png at 300 dpi.
"""
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 11, "figure.figsize": (7, 5), "figure.dpi": 300})


def fig1():
    k = np.arange(1, 65)
    mu = 2.0 ** (-k)
    plt.figure()
    plt.semilogy(k, mu, "b-", lw=2, label=r"$\mu(F) = 1/B = 2^{-k}$ (simple frontier)")
    plt.semilogy(k, mu**2, "r--", lw=1.5, label=r"$\mu^2 = (1/B)^2$ (chain length 2)")
    plt.semilogy(k, mu**3, "g:", lw=1.5, label=r"$\mu^3 = (1/B)^3$ (chain length 3)")
    plt.axvspan(32, 64, alpha=0.15, color="gray", label="Practical bases ($k \\geq 32$)")
    plt.axvline(32, color="gray", ls=":", lw=1)
    plt.axvline(64, color="gray", ls=":", lw=1)
    plt.annotate("$B=2^{32}$", xy=(32, 2**-32), xytext=(36, 1e-6),
                 arrowprops=dict(arrowstyle="->"))
    plt.annotate("$B=2^{64}$", xy=(64, 2**-64), xytext=(52, 1e-16),
                 arrowprops=dict(arrowstyle="->"))
    plt.xlabel("$k$ (base $B = 2^k$)")
    plt.ylabel("Relative measure (log scale)")
    plt.title("Fig. 1 - Decay of the frontier set measure $\\mu(F) = 2^{-k}$")
    plt.legend(loc="upper right")
    plt.grid(True, which="both", ls=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig("fig1.png")
    plt.close()


def fig2():
    rng = np.random.default_rng(42)
    k_vals = np.arange(1, 17)
    N = 200_000
    empirical, theoretical = [], []
    for k in k_vals:
        B = 1 << k
        a = rng.integers(0, B, size=N, dtype=np.uint64)
        b = rng.integers(0, B, size=N, dtype=np.uint64)
        front = (a + b) == (B - 1)
        empirical.append(front.mean())
        theoretical.append(1.0 / B)

    fig, ax1 = plt.subplots()
    ax1.semilogy(k_vals, theoretical, "b-", lw=2, label="Theoretical $1/B$")
    ax1.semilogy(k_vals, empirical, "ro", ms=5, label="Empirical (N=200k)")
    ax1.set_xlabel("$k$")
    ax1.set_ylabel("Frontier frequency (log)")
    ax1.set_title("Fig. 2 - Empirical vs theoretical frontier frequency")
    ax1.legend(loc="lower left")
    ax1.grid(True, which="both", ls=":", alpha=0.5)

    ax2 = ax1.inset_axes([0.55, 0.55, 0.4, 0.35])
    rel_err = [(e - t) / t * 100 for e, t in zip(empirical, theoretical)]
    ax2.plot(k_vals, rel_err, "g-o", ms=3)
    ax2.set_xlabel("$k$")
    ax2.set_ylabel("Relative error (%)")
    ax2.set_title("Sampling noise", fontsize=9)
    ax2.grid(True, ls=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig("fig2.png")
    plt.close()


def fig3():
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, k in zip(axes.ravel(), [1, 2, 4, 8]):
        B = 1 << k
        N = 500_000
        a = rng.integers(0, B, size=N, dtype=np.uint64)
        b = rng.integers(0, B, size=N, dtype=np.uint64)
        front = ((a + b) == (B - 1)).astype(int)
        lengths = []
        run = 0
        for f in front:
            if f:
                run += 1
            elif run > 0:
                lengths.append(run)
                run = 0
        if run > 0:
            lengths.append(run)

        if lengths:
            max_l = max(lengths)
            counts = np.bincount(lengths, minlength=max_l + 1)[1:]
            freq = counts / counts.sum()
            ell = np.arange(1, max_l + 1)
            ax.bar(ell, freq, color="steelblue", alpha=0.7, label="Empirical")
            theory = np.array([(1.0 / B) ** l for l in ell])
            theory /= theory.sum()
            ax.plot(ell, theory, "r-o", ms=3, label="Theoretical $(1/B)^\\ell$")
        ax.set_title(f"$k = {k}$")
        ax.set_xlabel("Chain length $\\ell$")
        ax.set_ylabel("Relative frequency")
        ax.set_yscale("log")
        ax.legend(fontsize=8)
        ax.grid(True, which="both", ls=":", alpha=0.5)
    fig.suptitle("Fig. 3 - Distribution of frontier chain lengths")
    plt.tight_layout()
    plt.savefig("fig3.png")
    plt.close()


def fig4():
    k = np.arange(1, 65)
    frac = 1.0 - 2.0 ** (-k)
    plt.figure()
    plt.plot(k, frac * 100, "b-", lw=2)
    plt.axhline(100, color="gray", ls=":", lw=1)
    for ki, fi in [(1, 0.5), (4, 0.9375), (8, 0.996), (32, 1 - 2**-32), (64, 1 - 2**-64)]:
        plt.annotate(f"$k={ki}$\n{fi*100:.2f}%",
                     xy=(ki, fi*100), xytext=(ki + 3, fi*100 - 8),
                     arrowprops=dict(arrowstyle="->"), fontsize=9)
    plt.xlabel("$k$ (base $B = 2^k$)")
    plt.ylabel("Independent fraction (%)")
    plt.title("Fig. 4 - Fraction of nuclei deciding without waiting")
    plt.grid(True, ls=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig("fig4.png")
    plt.close()


def fig5():
    n = 1_000_000
    m = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
    seq = np.full_like(m, n, dtype=float)
    ideal = n / m
    overhead = ideal + 2

    plt.figure()
    plt.loglog(m, seq, "k--", lw=2, label="Sequential $O(n)$")
    plt.loglog(m, ideal, "b-", lw=2, label="Ideal parallel $O(n/m)$")
    plt.loglog(m, overhead, "ro", ms=7, label="Parallel + $O(1)$ flag overhead")
    plt.annotate("Speedup $\\times 1024$\nwith 1024 nuclei",
                 xy=(1024, n/1024), xytext=(30, 5e4),
                 arrowprops=dict(arrowstyle="->"))
    plt.xlabel("Number of nuclei $m$")
    plt.ylabel("Work units (log-log)")
    plt.title(f"Fig. 5 - Scalability ($n = {n:,}$ words)")
    plt.legend()
    plt.grid(True, which="both", ls=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig("fig5.png")
    plt.close()


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("Generated: fig1.png .. fig5.png")
