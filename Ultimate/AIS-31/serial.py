import math
from scipy.stats import chi2

def serial_test(bits, m=2):
    n = len(bits)
    def psi_m(m):
        counts = {}
        for i in range(n):
            pattern = ''.join(bits[(i + j) % n] for j in range(m))
            counts[pattern] = counts.get(pattern, 0) + 1
        return sum(v2 for v in counts.values()) * (2m) / n - n

    psim   = psi_m(m)
    psim1  = psi_m(m - 1)
    psim2  = psi_m(m - 2)

    delta1 = psim - psim1
    delta2 = psim - 2 * psim1 + psim2

    p1 = chi2.sf(delta1, df=2(m - 1))
    p2 = chi2.sf(delta2, df=2(m - 2))

    print(f"[Serial Test] Δ1 = {delta1:.4f}, p1 = {p1:.6f}, Δ2 = {delta2:.4f}, p2 = {p2:.6f}")
    return p1 >= 0.01 and p2 >= 0.01
